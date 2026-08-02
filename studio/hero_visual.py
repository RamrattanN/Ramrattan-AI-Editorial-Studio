"""Provider-independent Hero Visual System for Capability 010.

The system consumes an approved Hero Visual prompt and returns either a
validated 720 x 425 PNG artifact or an explicit, actionable failure state.
The built-in deterministic provider requires no network or external package.
"""

from __future__ import annotations

import hashlib
import struct
import zlib
from dataclasses import dataclass
from enum import Enum
from typing import Protocol


HERO_VISUAL_WIDTH = 720
HERO_VISUAL_HEIGHT = 425
SUPPORTED_IMAGE_FORMATS = ("png",)


class HeroVisualStatus(str, Enum):
    """Canonical Hero Visual generation outcomes."""

    READY = "ready"
    GENERATION_FAILED = "generation_failed"
    VALIDATION_FAILED = "validation_failed"
    UNSUPPORTED_PROVIDER = "unsupported_provider"
    MALFORMED_REQUEST = "malformed_request"
    BLOCKED = "blocked_by_policy_or_editorial_constraints"


class HeroVisualValidationStatus(str, Enum):
    """Artifact validation outcomes kept separate from generation state."""

    NOT_RUN = "not_run"
    PASSED = "passed"
    FAILED = "failed"


@dataclass(frozen=True)
class HeroVisualRequest:
    """Approved visual intent supplied at the Capability 009 boundary."""

    prompt: str
    visual_intent: str
    provider: str = "deterministic"
    width: int = HERO_VISUAL_WIDTH
    height: int = HERO_VISUAL_HEIGHT
    image_format: str = "png"
    brand_context: str | None = None
    allow_logo: bool = False
    allow_recognizable_faces: bool = False
    allow_text_overlay: bool = False


@dataclass(frozen=True)
class ProviderVisual:
    """Untrusted provider response validated by the core system."""

    artifact: bytes
    width: int
    height: int
    image_format: str
    provenance: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class HeroVisualResult:
    """Validated Hero Visual result or one explicit safe failure."""

    status: HeroVisualStatus
    validation_status: HeroVisualValidationStatus
    provider: str
    prompt: str
    visual_intent: str
    width: int
    height: int
    image_format: str
    artifact: bytes | None = None
    artifact_sha256: str | None = None
    provenance: tuple[tuple[str, str], ...] = ()
    failure_reason: str | None = None

    @property
    def ready(self) -> bool:
        """Return whether a validated artifact is available."""
        return (
            self.status is HeroVisualStatus.READY
            and self.validation_status is HeroVisualValidationStatus.PASSED
            and bool(self.artifact)
        )


class HeroVisualProviderError(RuntimeError):
    """Raised by a provider when generation cannot complete."""


class HeroVisualProvider(Protocol):
    """Stable provider boundary; provider details do not enter orchestration."""

    provider_name: str

    def generate(self, request: HeroVisualRequest) -> ProviderVisual:
        """Generate one untrusted provider response for core validation."""


def _png_chunk(kind: bytes, payload: bytes) -> bytes:
    checksum = zlib.crc32(kind + payload) & 0xFFFFFFFF
    return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", checksum)


def _deterministic_png(width: int, height: int, prompt: str) -> bytes:
    """Build a deterministic, brand-neutral RGB PNG using the standard library."""
    digest = hashlib.sha256(prompt.encode("utf-8")).digest()
    background = tuple(232 + value % 16 for value in digest[:3])
    accent = tuple(48 + value % 144 for value in digest[3:6])
    rows = bytearray()
    for y in range(height):
        rows.append(0)
        transition = (y * 5) // max(height, 1)
        for x in range(width):
            stripe = ((x + transition * 37) // 120) % 6 == 0
            rows.extend(accent if stripe else background)
    signature = b"\x89PNG\r\n\x1a\n"
    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return (
        signature
        + _png_chunk(b"IHDR", header)
        + _png_chunk(b"IDAT", zlib.compress(bytes(rows), level=9))
        + _png_chunk(b"IEND", b"")
    )


class DeterministicHeroVisualProvider:
    """Offline provider for tests, demos, and repository validation."""

    provider_name = "deterministic"

    def generate(self, request: HeroVisualRequest) -> ProviderVisual:
        artifact = _deterministic_png(request.width, request.height, request.prompt)
        return ProviderVisual(
            artifact=artifact,
            width=request.width,
            height=request.height,
            image_format=request.image_format.casefold(),
            provenance=(
                ("provider", self.provider_name),
                ("provider_version", "1"),
                ("deterministic", "true"),
                ("prompt_sha256", hashlib.sha256(request.prompt.encode("utf-8")).hexdigest()),
            ),
        )


class HeroVisualSystem:
    """Validate requests, invoke a provider, and validate its artifact."""

    def __init__(self, providers: tuple[HeroVisualProvider, ...] | None = None) -> None:
        configured = providers or (DeterministicHeroVisualProvider(),)
        self._providers = {provider.provider_name: provider for provider in configured}

    def generate(self, request: HeroVisualRequest) -> HeroVisualResult:
        malformed = self._request_failure(request)
        if malformed:
            return self._failure(request, HeroVisualStatus.MALFORMED_REQUEST, malformed)

        blocked = self._policy_failure(request)
        if blocked:
            return self._failure(request, HeroVisualStatus.BLOCKED, blocked)

        provider = self._providers.get(request.provider)
        if provider is None:
            return self._failure(
                request,
                HeroVisualStatus.UNSUPPORTED_PROVIDER,
                f"Hero Visual provider '{request.provider}' is not configured.",
            )

        try:
            generated = provider.generate(request)
        except Exception as exc:  # Providers are untrusted; fail closed.
            reason = str(exc).strip() or "The Hero Visual provider failed without detail."
            return self._failure(request, HeroVisualStatus.GENERATION_FAILED, reason)

        validation_failure = self._artifact_failure(generated, provider.provider_name)
        if validation_failure:
            return self._failure(
                request,
                HeroVisualStatus.VALIDATION_FAILED,
                validation_failure,
                provider=provider.provider_name,
                validation_status=HeroVisualValidationStatus.FAILED,
            )

        return HeroVisualResult(
            status=HeroVisualStatus.READY,
            validation_status=HeroVisualValidationStatus.PASSED,
            provider=provider.provider_name,
            prompt=request.prompt,
            visual_intent=request.visual_intent,
            width=generated.width,
            height=generated.height,
            image_format=generated.image_format,
            artifact=generated.artifact,
            artifact_sha256=hashlib.sha256(generated.artifact).hexdigest(),
            provenance=generated.provenance,
        )

    @staticmethod
    def _request_failure(request: HeroVisualRequest) -> str | None:
        if not request.prompt.strip() or not request.visual_intent.strip():
            return "Hero Visual requests require an approved prompt and visual intent."
        if request.width != HERO_VISUAL_WIDTH or request.height != HERO_VISUAL_HEIGHT:
            return "Hero Visual dimensions must be exactly 720 x 425."
        if request.image_format.casefold() not in SUPPORTED_IMAGE_FORMATS:
            return "The requested Hero Visual image format is unsupported."
        if not request.provider.strip():
            return "Hero Visual requests require a provider identifier."
        if request.allow_logo and not (request.brand_context or "").strip():
            return "Logo use requires explicit approved brand context."
        return None

    @staticmethod
    def _policy_failure(request: HeroVisualRequest) -> str | None:
        prompt = request.prompt.casefold()
        policies = (
            (("logo", "watermark"), request.allow_logo, "logo or watermark"),
            (("recognizable face", "recognisable face", "headshot", "portrait"), request.allow_recognizable_faces, "recognizable face"),
            (("text overlay", "typography", "words on image"), request.allow_text_overlay, "text overlay"),
        )
        for terms, allowed, label in policies:
            if any(term in prompt for term in terms) and not allowed:
                return f"The request is blocked because {label} use was not explicitly approved."
        return None

    @staticmethod
    def _artifact_failure(generated: ProviderVisual, provider_name: str) -> str | None:
        if not generated.artifact:
            return "The provider returned an empty Hero Visual artifact."
        if generated.width != HERO_VISUAL_WIDTH or generated.height != HERO_VISUAL_HEIGHT:
            return "The provider artifact dimensions are not 720 x 425."
        if generated.image_format.casefold() != "png":
            return "The provider returned an unsupported Hero Visual format."
        if len(generated.artifact) < 24 or not generated.artifact.startswith(b"\x89PNG\r\n\x1a\n"):
            return "The provider artifact is not a valid PNG container."
        width, height = struct.unpack(">II", generated.artifact[16:24])
        if (width, height) != (HERO_VISUAL_WIDTH, HERO_VISUAL_HEIGHT):
            return "The PNG header dimensions are not 720 x 425."
        provenance = dict(generated.provenance)
        if provenance.get("provider") != provider_name or not provenance.get("provider_version"):
            return "The provider returned incomplete provenance metadata."
        return None

    @staticmethod
    def _failure(
        request: HeroVisualRequest,
        status: HeroVisualStatus,
        reason: str,
        *,
        provider: str | None = None,
        validation_status: HeroVisualValidationStatus = HeroVisualValidationStatus.NOT_RUN,
    ) -> HeroVisualResult:
        return HeroVisualResult(
            status=status,
            validation_status=validation_status,
            provider=provider or request.provider,
            prompt=request.prompt,
            visual_intent=request.visual_intent,
            width=request.width,
            height=request.height,
            image_format=request.image_format.casefold(),
            failure_reason=reason,
        )
