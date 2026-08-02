"""Editorial Workspace intake runtime for Capability 007.

This module implements:

- the Author-facing Editorial Workspace welcome experience,
- deterministic input recognition,
- the first two visible Editorial Integrity stages,
- initial source assessment,
- optional logo and headshot identity-asset handling,
- and rights confirmation.

It deliberately does not perform full evidence validation.
That responsibility belongs to Capability 008.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse


class InputKind(str, Enum):
    """Canonical Editorial Intake classifications."""

    URL = "url"
    PASTED_TEXT = "pasted_text"
    DOCUMENT = "document"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    PORTABLE_EDITORIAL_PROJECT = "portable_editorial_project"
    LOGO = "logo"
    HEADSHOT = "headshot"
    UNKNOWN = "unknown"


class WorkspaceStage(str, Enum):
    """Visible Editorial Integrity Pipeline stages."""

    UNDERSTANDING_INPUT = "understanding_input"
    ASSESSING_SOURCES = "assessing_sources"
    VERIFYING_EVIDENCE = "verifying_evidence"
    REVIEWING_EDITORIAL_RISKS = "reviewing_editorial_risks"
    CREATING_PUBLICATION_PACKAGE = "creating_publication_package"


class StageState(str, Enum):
    """Presentation state for a visible Workspace stage."""

    COMPLETE = "complete"
    ACTIVE = "active"
    PENDING = "pending"
    BLOCKED = "blocked"


class IdentityAssetKind(str, Enum):
    """Optional Author identity assets."""

    LOGO = "logo"
    HEADSHOT = "headshot"


class SourceQuality(str, Enum):
    """Initial source-quality assessment.

    Capability 007 provides an intake-level assessment only.
    It does not claim full verification.
    """

    HIGH = "high"
    MODERATE = "moderate"
    LIMITED = "limited"
    UNKNOWN = "unknown"


DOCUMENT_EXTENSIONS = {
    ".pdf",
    ".doc",
    ".docx",
    ".ppt",
    ".pptx",
    ".txt",
    ".rtf",
    ".md",
    ".odt",
}

IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif",
    ".tif",
    ".tiff",
    ".heic",
}

AUDIO_EXTENSIONS = {
    ".mp3",
    ".m4a",
    ".wav",
    ".aac",
    ".flac",
    ".ogg",
}

VIDEO_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".m4v",
    ".webm",
    ".avi",
    ".mkv",
}

PORTABLE_PROJECT_SUFFIXES = (
    ".editorial-project.md",
    ".portable-editorial-project.md",
)


@dataclass(frozen=True)
class WorkspaceStageView:
    """One visible stage in the Editorial Workspace."""

    number: int
    name: str
    state: StageState
    detail: str = ""


@dataclass(frozen=True)
class InputDescriptor:
    """Normalized description of supplied Author material."""

    kind: InputKind
    value: str
    display_name: str
    extension: str = ""
    host_supported: bool = True
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class IdentityAsset:
    """An optional logo or headshot supplied by the Author."""

    kind: IdentityAssetKind
    file_name: str
    rights_confirmed: bool = False
    usage_preference: str = "subtle"
    included_in_project_export: bool = False

    def validate(self) -> None:
        """Require rights confirmation before asset use."""
        if not self.rights_confirmed:
            raise ValueError(
                "Identity assets require confirmation that the "
                "Author is authorised to use them."
            )

        suffix = Path(self.file_name).suffix.lower()

        if suffix not in IMAGE_EXTENSIONS:
            raise ValueError(
                "Logo and headshot assets must use a supported "
                "image format."
            )


@dataclass(frozen=True)
class SourceAssessment:
    """Initial, non-verifying source assessment."""

    quality: SourceQuality
    source_identified: bool
    publication_date_known: bool
    primary_source_possible: bool
    requires_deeper_verification: bool
    observations: tuple[str, ...] = ()


@dataclass
class EditorialIntakeResult:
    """Result of the first two Workspace stages."""

    descriptor: InputDescriptor
    stages: list[WorkspaceStageView]
    source_assessment: SourceAssessment
    identity_assets: list[IdentityAsset] = field(
        default_factory=list
    )
    significant_findings: list[str] = field(
        default_factory=list
    )

    @property
    def brand_neutral(self) -> bool:
        """Return True when no identity assets are active."""
        return not self.identity_assets


class EditorialWorkspace:
    """Author-facing Editorial Workspace entry point."""

    WELCOME_HEADLINE = (
        "Create a professional article from almost any source."
    )

    TRUST_PROMISE = (
        "Every article is reviewed for source quality, factual "
        "accuracy, and editorial risk before publication."
    )

    SUPPORTED_INPUTS = (
        "Web URL",
        "Pasted text",
        "PDF, Word, PowerPoint, Markdown, or plain text document",
        "Image containing readable text",
        "Audio supported by the host platform",
        "Video supported by the host platform",
        "Portable Editorial Project",
        "Professional observation or article idea",
        "Optional logo or headshot for the Hero Visual",
    )

    STAGE_NAMES = (
        "Understanding your input",
        "Assessing your sources",
        "Verifying the evidence",
        "Reviewing editorial risks",
        "Creating your publication package",
    )

    def welcome_message(
        self,
        preferred_name: str | None = None,
    ) -> str:
        """Return concise Author-facing Workspace copy."""
        greeting = "Welcome."

        if preferred_name and preferred_name.strip():
            greeting = (
                f"Welcome back, {preferred_name.strip()}."
            )

        supported = "\n".join(
            f"- {item}"
            for item in self.SUPPORTED_INPUTS
        )

        return (
            f"{greeting}\n\n"
            f"{self.WELCOME_HEADLINE}\n\n"
            f"{self.TRUST_PROMISE}\n\n"
            "You may provide:\n"
            f"{supported}\n\n"
            "The Editor will:\n"
            "1. Understand your input\n"
            "2. Assess your sources\n"
            "3. Verify the evidence\n"
            "4. Review editorial risks\n"
            "5. Create your publication package\n\n"
            "You remain in control throughout."
        )

    def recognize_input(
        self,
        value: str,
        *,
        declared_file_name: str | None = None,
    ) -> InputDescriptor:
        """Classify Author input without requiring a menu."""
        normalized = value.strip()

        if not normalized:
            return InputDescriptor(
                kind=InputKind.UNKNOWN,
                value=value,
                display_name="Empty input",
                notes=("No usable material was supplied.",),
            )

        file_name = declared_file_name or normalized
        suffix = Path(file_name).suffix.lower()

        if self._is_url(normalized):
            parsed = urlparse(normalized)

            return InputDescriptor(
                kind=InputKind.URL,
                value=normalized,
                display_name=parsed.netloc or normalized,
                notes=(
                    "A URL is provenance, not durable memory.",
                ),
            )

        lower_name = file_name.lower()

        if lower_name.endswith(
            PORTABLE_PROJECT_SUFFIXES
        ) or (
            suffix == ".md"
            and "editorial-project" in lower_name
        ):
            return InputDescriptor(
                kind=InputKind.PORTABLE_EDITORIAL_PROJECT,
                value=normalized,
                display_name=Path(file_name).name,
                extension=suffix,
            )

        if suffix in DOCUMENT_EXTENSIONS:
            return InputDescriptor(
                kind=InputKind.DOCUMENT,
                value=normalized,
                display_name=Path(file_name).name,
                extension=suffix,
            )

        if suffix in AUDIO_EXTENSIONS:
            return InputDescriptor(
                kind=InputKind.AUDIO,
                value=normalized,
                display_name=Path(file_name).name,
                extension=suffix,
                notes=(
                    "Processing remains subject to host-platform "
                    "file and size limits.",
                ),
            )

        if suffix in VIDEO_EXTENSIONS:
            return InputDescriptor(
                kind=InputKind.VIDEO,
                value=normalized,
                display_name=Path(file_name).name,
                extension=suffix,
                notes=(
                    "Processing remains subject to host-platform "
                    "file and size limits.",
                ),
            )

        if suffix in IMAGE_EXTENSIONS:
            return InputDescriptor(
                kind=InputKind.IMAGE,
                value=normalized,
                display_name=Path(file_name).name,
                extension=suffix,
            )

        if self._looks_like_pasted_text(normalized):
            return InputDescriptor(
                kind=InputKind.PASTED_TEXT,
                value=normalized,
                display_name="Pasted text",
            )

        return InputDescriptor(
            kind=InputKind.PASTED_TEXT,
            value=normalized,
            display_name="Author description",
            notes=(
                "The material will be treated as an Author "
                "observation or article idea.",
            ),
        )

    def classify_identity_asset(
        self,
        file_name: str,
        *,
        declared_kind: IdentityAssetKind,
        rights_confirmed: bool,
        usage_preference: str = "subtle",
        included_in_project_export: bool = False,
    ) -> IdentityAsset:
        """Create and validate an optional identity asset."""
        asset = IdentityAsset(
            kind=declared_kind,
            file_name=file_name,
            rights_confirmed=rights_confirmed,
            usage_preference=usage_preference,
            included_in_project_export=(
                included_in_project_export
            ),
        )

        asset.validate()

        return asset

    def process(
        self,
        value: str,
        *,
        declared_file_name: str | None = None,
        identity_assets: Iterable[IdentityAsset] = (),
    ) -> EditorialIntakeResult:
        """Execute Understanding and Source Assessment."""
        descriptor = self.recognize_input(
            value,
            declared_file_name=declared_file_name,
        )

        assets = list(identity_assets)

        for asset in assets:
            asset.validate()

        assessment = self.assess_source(descriptor)

        stages = [
            WorkspaceStageView(
                number=1,
                name=self.STAGE_NAMES[0],
                state=StageState.COMPLETE,
                detail=(
                    f"Recognised {descriptor.kind.value}: "
                    f"{descriptor.display_name}"
                ),
            ),
            WorkspaceStageView(
                number=2,
                name=self.STAGE_NAMES[1],
                state=StageState.COMPLETE,
                detail=(
                    "Initial source assessment complete. "
                    "Full evidence verification follows in "
                    "Capability 008."
                ),
            ),
            WorkspaceStageView(
                number=3,
                name=self.STAGE_NAMES[2],
                state=StageState.PENDING,
            ),
            WorkspaceStageView(
                number=4,
                name=self.STAGE_NAMES[3],
                state=StageState.PENDING,
            ),
            WorkspaceStageView(
                number=5,
                name=self.STAGE_NAMES[4],
                state=StageState.PENDING,
            ),
        ]

        findings: list[str] = []

        if descriptor.kind is InputKind.UNKNOWN:
            findings.append(
                "The supplied material could not be understood."
            )

        if assessment.quality in {
            SourceQuality.LIMITED,
            SourceQuality.UNKNOWN,
        }:
            findings.append(
                "The current material requires deeper source "
                "verification before publication."
            )

        if assets:
            findings.append(
                "Optional identity assets are available for the "
                "Hero Visual. Brand-neutral generation remains "
                "available."
            )

        return EditorialIntakeResult(
            descriptor=descriptor,
            stages=stages,
            source_assessment=assessment,
            identity_assets=assets,
            significant_findings=findings,
        )

    def assess_source(
        self,
        descriptor: InputDescriptor,
    ) -> SourceAssessment:
        """Perform an initial source assessment.

        This is intentionally conservative. It does not claim that
        evidence has been independently verified.
        """
        if descriptor.kind is InputKind.URL:
            parsed = urlparse(descriptor.value)
            host = parsed.netloc.lower()
            observations = [
                "The source URL is identifiable.",
                "Publication date and authorship require retrieval.",
                "Important claims require independent verification.",
            ]

            quality = SourceQuality.MODERATE

            if host.endswith(".gov") or host.endswith(".edu"):
                quality = SourceQuality.HIGH
                observations.append(
                    "The domain may represent an institutional "
                    "source, but individual claims still require "
                    "review."
                )

            return SourceAssessment(
                quality=quality,
                source_identified=True,
                publication_date_known=False,
                primary_source_possible=True,
                requires_deeper_verification=True,
                observations=tuple(observations),
            )

        if descriptor.kind in {
            InputKind.DOCUMENT,
            InputKind.PORTABLE_EDITORIAL_PROJECT,
        }:
            return SourceAssessment(
                quality=SourceQuality.MODERATE,
                source_identified=True,
                publication_date_known=False,
                primary_source_possible=True,
                requires_deeper_verification=True,
                observations=(
                    "The supplied file is identifiable.",
                    "Authorship, date, and evidence must be "
                    "derived from its contents.",
                ),
            )

        if descriptor.kind in {
            InputKind.AUDIO,
            InputKind.VIDEO,
            InputKind.IMAGE,
        }:
            return SourceAssessment(
                quality=SourceQuality.LIMITED,
                source_identified=True,
                publication_date_known=False,
                primary_source_possible=True,
                requires_deeper_verification=True,
                observations=(
                    "The asset may contain primary material.",
                    "Speaker, creator, date, and context require "
                    "confirmation.",
                ),
            )

        if descriptor.kind is InputKind.PASTED_TEXT:
            return SourceAssessment(
                quality=SourceQuality.LIMITED,
                source_identified=False,
                publication_date_known=False,
                primary_source_possible=False,
                requires_deeper_verification=True,
                observations=(
                    "Pasted text does not establish provenance.",
                    "Material claims require source identification "
                    "and verification.",
                ),
            )

        return SourceAssessment(
            quality=SourceQuality.UNKNOWN,
            source_identified=False,
            publication_date_known=False,
            primary_source_possible=False,
            requires_deeper_verification=True,
            observations=(
                "No reliable source assessment can be made yet.",
            ),
        )

    @staticmethod
    def missing_identity_asset_message(
        *,
        logo_was_used: bool,
        headshot_was_used: bool,
    ) -> str:
        """Explain missing optional assets during project resume."""
        missing: list[str] = []

        if logo_was_used:
            missing.append("logo")

        if headshot_was_used:
            missing.append("headshot")

        if not missing:
            return (
                "No previously used identity assets are missing."
            )

        joined = " and ".join(missing)

        return (
            f"This project previously used a {joined}, but the "
            "original asset was not included. Upload it again, "
            "continue without it, or create a brand-neutral "
            "Hero Visual."
        )

    @staticmethod
    def _is_url(value: str) -> bool:
        parsed = urlparse(value)

        return (
            parsed.scheme in {"http", "https"}
            and bool(parsed.netloc)
        )

    @staticmethod
    def _looks_like_pasted_text(value: str) -> bool:
        return (
            len(value) >= 80
            or "\n" in value
            or value.count(" ") >= 12
        )
