#!/usr/bin/env python3
"""Bootstrap Capability 010 - provider-independent Hero Visual System."""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
import textwrap
from pathlib import Path


EXPECTED_REPOSITORY = "Ramrattan-AI-Editorial-Studio"
EXPECTED_BRANCH = "feature/capability-010-hero-visual-system"
SCRIPT_PATH = "scripts/bootstrap_capability010_hero_visual_system.py"
CAPABILITY009_BOOTSTRAP = "scripts/bootstrap_capability009_article_engine_publication_package.py"
RC1_BOOTSTRAP = "scripts/bootstrap_rc1_checkpoint_authorization_hardening.py"
RC1_TEST = "tests/test_rc1_checkpoint.py"
SENTINEL = "CAPABILITY_010_HERO_VISUAL_SYSTEM_COMPLETE"
MARK_HASH = "b2cd1c22239b7176b43578892b0c37ac502ca5ab696b7c083a0b397bfe285727"
LOCKUP_HASH = "ae56f16f3e4b3a2bfbf5cefbf6ee807482cd8814e30b7496a917b9eae3a5ba72"
ARTICLE_ENGINE_HASH = "653db77e8881aa6532906fa1b17a8c771152cfe14ef1266383daba423d596868"
EDITORIAL_WORKSPACE_HASH = "2bb9a08fc9c11c496f518509019b569ee90d5b89653f08321b8b7d5ab5d1566c"


class CapabilityError(RuntimeError):
    """Raised when Capability 010 cannot continue safely."""


def clean(value: str) -> str:
    return textwrap.dedent(value).strip() + "\n"


FILES = {
    "studio/hero_visual.py": clean("\"\"\"Provider-independent Hero Visual System for Capability 010.\n\nThe system consumes an approved Hero Visual prompt and returns either a\nvalidated 720 x 425 PNG artifact or an explicit, actionable failure state.\nThe built-in deterministic provider requires no network or external package.\n\"\"\"\n\nfrom __future__ import annotations\n\nimport hashlib\nimport struct\nimport zlib\nfrom dataclasses import dataclass\nfrom enum import Enum\nfrom typing import Protocol\n\n\nHERO_VISUAL_WIDTH = 720\nHERO_VISUAL_HEIGHT = 425\nSUPPORTED_IMAGE_FORMATS = (\"png\",)\n\n\nclass HeroVisualStatus(str, Enum):\n    \"\"\"Canonical Hero Visual generation outcomes.\"\"\"\n\n    READY = \"ready\"\n    GENERATION_FAILED = \"generation_failed\"\n    VALIDATION_FAILED = \"validation_failed\"\n    UNSUPPORTED_PROVIDER = \"unsupported_provider\"\n    MALFORMED_REQUEST = \"malformed_request\"\n    BLOCKED = \"blocked_by_policy_or_editorial_constraints\"\n\n\nclass HeroVisualValidationStatus(str, Enum):\n    \"\"\"Artifact validation outcomes kept separate from generation state.\"\"\"\n\n    NOT_RUN = \"not_run\"\n    PASSED = \"passed\"\n    FAILED = \"failed\"\n\n\n@dataclass(frozen=True)\nclass HeroVisualRequest:\n    \"\"\"Approved visual intent supplied at the Capability 009 boundary.\"\"\"\n\n    prompt: str\n    visual_intent: str\n    provider: str = \"deterministic\"\n    width: int = HERO_VISUAL_WIDTH\n    height: int = HERO_VISUAL_HEIGHT\n    image_format: str = \"png\"\n    brand_context: str | None = None\n    allow_logo: bool = False\n    allow_recognizable_faces: bool = False\n    allow_text_overlay: bool = False\n\n\n@dataclass(frozen=True)\nclass ProviderVisual:\n    \"\"\"Untrusted provider response validated by the core system.\"\"\"\n\n    artifact: bytes\n    width: int\n    height: int\n    image_format: str\n    provenance: tuple[tuple[str, str], ...]\n\n\n@dataclass(frozen=True)\nclass HeroVisualResult:\n    \"\"\"Validated Hero Visual result or one explicit safe failure.\"\"\"\n\n    status: HeroVisualStatus\n    validation_status: HeroVisualValidationStatus\n    provider: str\n    prompt: str\n    width: int\n    height: int\n    image_format: str\n    artifact: bytes | None = None\n    artifact_sha256: str | None = None\n    provenance: tuple[tuple[str, str], ...] = ()\n    failure_reason: str | None = None\n\n    @property\n    def ready(self) -> bool:\n        \"\"\"Return whether a validated artifact is available.\"\"\"\n        return (\n            self.status is HeroVisualStatus.READY\n            and self.validation_status is HeroVisualValidationStatus.PASSED\n            and bool(self.artifact)\n        )\n\n\nclass HeroVisualProviderError(RuntimeError):\n    \"\"\"Raised by a provider when generation cannot complete.\"\"\"\n\n\nclass HeroVisualProvider(Protocol):\n    \"\"\"Stable provider boundary; provider details do not enter orchestration.\"\"\"\n\n    provider_name: str\n\n    def generate(self, request: HeroVisualRequest) -> ProviderVisual:\n        \"\"\"Generate one untrusted provider response for core validation.\"\"\"\n\n\ndef _png_chunk(kind: bytes, payload: bytes) -> bytes:\n    checksum = zlib.crc32(kind + payload) & 0xFFFFFFFF\n    return struct.pack(\">I\", len(payload)) + kind + payload + struct.pack(\">I\", checksum)\n\n\ndef _deterministic_png(width: int, height: int, prompt: str) -> bytes:\n    \"\"\"Build a deterministic, brand-neutral RGB PNG using the standard library.\"\"\"\n    digest = hashlib.sha256(prompt.encode(\"utf-8\")).digest()\n    background = tuple(232 + value % 16 for value in digest[:3])\n    accent = tuple(48 + value % 144 for value in digest[3:6])\n    rows = bytearray()\n    for y in range(height):\n        rows.append(0)\n        transition = (y * 5) // max(height, 1)\n        for x in range(width):\n            stripe = ((x + transition * 37) // 120) % 6 == 0\n            rows.extend(accent if stripe else background)\n    signature = b\"\\x89PNG\\r\\n\\x1a\\n\"\n    header = struct.pack(\">IIBBBBB\", width, height, 8, 2, 0, 0, 0)\n    return (\n        signature\n        + _png_chunk(b\"IHDR\", header)\n        + _png_chunk(b\"IDAT\", zlib.compress(bytes(rows), level=9))\n        + _png_chunk(b\"IEND\", b\"\")\n    )\n\n\nclass DeterministicHeroVisualProvider:\n    \"\"\"Offline provider for tests, demos, and repository validation.\"\"\"\n\n    provider_name = \"deterministic\"\n\n    def generate(self, request: HeroVisualRequest) -> ProviderVisual:\n        artifact = _deterministic_png(request.width, request.height, request.prompt)\n        return ProviderVisual(\n            artifact=artifact,\n            width=request.width,\n            height=request.height,\n            image_format=request.image_format.casefold(),\n            provenance=(\n                (\"provider\", self.provider_name),\n                (\"provider_version\", \"1\"),\n                (\"deterministic\", \"true\"),\n                (\"prompt_sha256\", hashlib.sha256(request.prompt.encode(\"utf-8\")).hexdigest()),\n            ),\n        )\n\n\nclass HeroVisualSystem:\n    \"\"\"Validate requests, invoke a provider, and validate its artifact.\"\"\"\n\n    def __init__(self, providers: tuple[HeroVisualProvider, ...] | None = None) -> None:\n        configured = providers or (DeterministicHeroVisualProvider(),)\n        self._providers = {provider.provider_name: provider for provider in configured}\n\n    def generate(self, request: HeroVisualRequest) -> HeroVisualResult:\n        malformed = self._request_failure(request)\n        if malformed:\n            return self._failure(request, HeroVisualStatus.MALFORMED_REQUEST, malformed)\n\n        blocked = self._policy_failure(request)\n        if blocked:\n            return self._failure(request, HeroVisualStatus.BLOCKED, blocked)\n\n        provider = self._providers.get(request.provider)\n        if provider is None:\n            return self._failure(\n                request,\n                HeroVisualStatus.UNSUPPORTED_PROVIDER,\n                f\"Hero Visual provider '{request.provider}' is not configured.\",\n            )\n\n        try:\n            generated = provider.generate(request)\n        except Exception as exc:  # Providers are untrusted; fail closed.\n            reason = str(exc).strip() or \"The Hero Visual provider failed without detail.\"\n            return self._failure(request, HeroVisualStatus.GENERATION_FAILED, reason)\n\n        validation_failure = self._artifact_failure(generated, provider.provider_name)\n        if validation_failure:\n            return self._failure(\n                request,\n                HeroVisualStatus.VALIDATION_FAILED,\n                validation_failure,\n                provider=provider.provider_name,\n                validation_status=HeroVisualValidationStatus.FAILED,\n            )\n\n        return HeroVisualResult(\n            status=HeroVisualStatus.READY,\n            validation_status=HeroVisualValidationStatus.PASSED,\n            provider=provider.provider_name,\n            prompt=request.prompt,\n            width=generated.width,\n            height=generated.height,\n            image_format=generated.image_format,\n            artifact=generated.artifact,\n            artifact_sha256=hashlib.sha256(generated.artifact).hexdigest(),\n            provenance=generated.provenance,\n        )\n\n    @staticmethod\n    def _request_failure(request: HeroVisualRequest) -> str | None:\n        if not request.prompt.strip() or not request.visual_intent.strip():\n            return \"Hero Visual requests require an approved prompt and visual intent.\"\n        if request.width != HERO_VISUAL_WIDTH or request.height != HERO_VISUAL_HEIGHT:\n            return \"Hero Visual dimensions must be exactly 720 x 425.\"\n        if request.image_format.casefold() not in SUPPORTED_IMAGE_FORMATS:\n            return \"The requested Hero Visual image format is unsupported.\"\n        if not request.provider.strip():\n            return \"Hero Visual requests require a provider identifier.\"\n        if request.allow_logo and not (request.brand_context or \"\").strip():\n            return \"Logo use requires explicit approved brand context.\"\n        return None\n\n    @staticmethod\n    def _policy_failure(request: HeroVisualRequest) -> str | None:\n        prompt = request.prompt.casefold()\n        policies = (\n            ((\"logo\", \"watermark\"), request.allow_logo, \"logo or watermark\"),\n            ((\"recognizable face\", \"recognisable face\", \"headshot\", \"portrait\"), request.allow_recognizable_faces, \"recognizable face\"),\n            ((\"text overlay\", \"typography\", \"words on image\"), request.allow_text_overlay, \"text overlay\"),\n        )\n        for terms, allowed, label in policies:\n            if any(term in prompt for term in terms) and not allowed:\n                return f\"The request is blocked because {label} use was not explicitly approved.\"\n        return None\n\n    @staticmethod\n    def _artifact_failure(generated: ProviderVisual, provider_name: str) -> str | None:\n        if not generated.artifact:\n            return \"The provider returned an empty Hero Visual artifact.\"\n        if generated.width != HERO_VISUAL_WIDTH or generated.height != HERO_VISUAL_HEIGHT:\n            return \"The provider artifact dimensions are not 720 x 425.\"\n        if generated.image_format.casefold() != \"png\":\n            return \"The provider returned an unsupported Hero Visual format.\"\n        if len(generated.artifact) < 24 or not generated.artifact.startswith(b\"\\x89PNG\\r\\n\\x1a\\n\"):\n            return \"The provider artifact is not a valid PNG container.\"\n        width, height = struct.unpack(\">II\", generated.artifact[16:24])\n        if (width, height) != (HERO_VISUAL_WIDTH, HERO_VISUAL_HEIGHT):\n            return \"The PNG header dimensions are not 720 x 425.\"\n        provenance = dict(generated.provenance)\n        if provenance.get(\"provider\") != provider_name or not provenance.get(\"provider_version\"):\n            return \"The provider returned incomplete provenance metadata.\"\n        return None\n\n    @staticmethod\n    def _failure(\n        request: HeroVisualRequest,\n        status: HeroVisualStatus,\n        reason: str,\n        *,\n        provider: str | None = None,\n        validation_status: HeroVisualValidationStatus = HeroVisualValidationStatus.NOT_RUN,\n    ) -> HeroVisualResult:\n        return HeroVisualResult(\n            status=status,\n            validation_status=validation_status,\n            provider=provider or request.provider,\n            prompt=request.prompt,\n            width=request.width,\n            height=request.height,\n            image_format=request.image_format.casefold(),\n            failure_reason=reason,\n        )\n"),
    "studio/publication_package.py": clean("\"\"\"Textual Publication Package assembly for Capability 009.\n\nRendered Hero Visual generation remains Capability 010. Portable\nEditorial Project serialization remains Capability 011.\n\"\"\"\n\nfrom __future__ import annotations\n\nfrom dataclasses import dataclass, replace\nfrom enum import Enum\n\nfrom .article_engine import ArticleDraft, PublicationBlockedError\nfrom .evidence_validation import (\n    EditorialConfidence,\n    EditorialRisk,\n    EvidenceValidationReport,\n)\nfrom .hero_visual import HeroVisualResult, HeroVisualStatus\n\n\nclass PackageReadiness(str, Enum):\n    \"\"\"Capability 009 textual package readiness.\"\"\"\n\n    READY_FOR_HERO_VISUAL = \"ready_for_hero_visual\"\n    REVIEW_BEFORE_HERO_VISUAL = \"review_before_hero_visual\"\n\n\nclass HeroVisualPackageState(str, Enum):\n    \"\"\"Hero Visual state at the narrow Publication Package boundary.\"\"\"\n\n    PENDING = \"pending\"\n    READY = \"ready\"\n    FAILED = \"failed\"\n    BLOCKED = \"blocked\"\n\n\n@dataclass(frozen=True)\nclass PublicationPackage:\n    \"\"\"Validated textual package with later deliverables explicit.\"\"\"\n\n    article_markdown: str\n    hero_visual_prompt: str\n    headline: str\n    hook: str\n    insights: tuple[str, ...]\n    practical_takeaway: str\n    cta: str\n    source_and_attribution: tuple[str, ...]\n    hashtags: tuple[str, ...]\n    linkedin_description: str\n    editorial_confidence: EditorialConfidence\n    editorial_risk: EditorialRisk\n    readiness: PackageReadiness\n    review_findings: tuple[str, ...]\n    hero_visual_state: HeroVisualPackageState = HeroVisualPackageState.PENDING\n    rendered_hero_visual: HeroVisualResult | None = None\n    portable_editorial_project: None = None\n    deferred_components: tuple[str, ...] = (\n        \"Rendered Hero Visual - Capability 010\",\n        \"Portable Editorial Project - Capability 011\",\n    )\n    version_one_complete: bool = False\n\n    def required_text_components(self) -> tuple[str, ...]:\n        \"\"\"Return canonical textual components in package order.\"\"\"\n        return (\n            self.hero_visual_prompt,\n            self.headline,\n            self.hook,\n            *self.insights,\n            self.practical_takeaway,\n            self.cta,\n            *self.source_and_attribution,\n            *self.hashtags,\n            self.linkedin_description,\n            self.article_markdown,\n        )\n\n\nclass PublicationPackageBuilder:\n    \"\"\"Assemble one validated Capability 009 textual package.\"\"\"\n\n    def build(\n        self,\n        draft: ArticleDraft,\n        evidence_report: EvidenceValidationReport,\n    ) -> PublicationPackage:\n        if evidence_report.publication_blocked or evidence_report.editorial_risk in {\n            EditorialRisk.HIGH,\n            EditorialRisk.SEVERE,\n        }:\n            raise PublicationBlockedError(evidence_report.author_message)\n        readiness = {\n            EditorialConfidence.READY: PackageReadiness.READY_FOR_HERO_VISUAL,\n            EditorialConfidence.READY_WITH_REVIEW: (\n                PackageReadiness.REVIEW_BEFORE_HERO_VISUAL\n            ),\n        }.get(evidence_report.editorial_confidence)\n        if readiness is None:\n            raise PublicationBlockedError(\n                \"Editorial Confidence does not permit package assembly.\"\n            )\n        package = PublicationPackage(\n            article_markdown=draft.article_markdown,\n            hero_visual_prompt=draft.hero_visual_prompt,\n            headline=draft.headline,\n            hook=draft.hook,\n            insights=draft.insights,\n            practical_takeaway=draft.practical_takeaway,\n            cta=draft.cta,\n            source_and_attribution=tuple(\n                item.citation for item in draft.source_attributions\n            ),\n            hashtags=draft.hashtags,\n            linkedin_description=draft.linkedin_description,\n            editorial_confidence=evidence_report.editorial_confidence,\n            editorial_risk=evidence_report.editorial_risk,\n            readiness=readiness,\n            review_findings=evidence_report.significant_findings,\n        )\n        if not package.insights or any(\n            not value.strip() for value in package.required_text_components()\n        ):\n            raise ValueError(\n                \"Publication Packages require every textual component.\"\n            )\n        return package\n\n    def attach_hero_visual(\n        self,\n        package: PublicationPackage,\n        result: HeroVisualResult,\n    ) -> PublicationPackage:\n        \"\"\"Attach one existing result without regenerating textual components.\"\"\"\n        if package.hero_visual_state is not HeroVisualPackageState.PENDING:\n            raise ValueError(\"The Publication Package already has a Hero Visual result.\")\n        if result.prompt != package.hero_visual_prompt:\n            raise ValueError(\"The Hero Visual result must preserve the approved prompt.\")\n\n        if result.ready:\n            state = HeroVisualPackageState.READY\n            deferred = tuple(\n                item for item in package.deferred_components\n                if item != \"Rendered Hero Visual - Capability 010\"\n            )\n        elif result.status is HeroVisualStatus.BLOCKED:\n            state = HeroVisualPackageState.BLOCKED\n            deferred = package.deferred_components\n        else:\n            state = HeroVisualPackageState.FAILED\n            deferred = package.deferred_components\n\n        return replace(\n            package,\n            hero_visual_state=state,\n            rendered_hero_visual=result,\n            deferred_components=deferred,\n        )\n"),
    "tests/test_capability010_hero_visual.py": clean("\"\"\"Behavioral tests for Capability 010 Hero Visual System.\"\"\"\n\nfrom datetime import date\nimport unittest\n\nfrom studio.article_engine import ArticleEngine, ArticleRequest, SourceAttribution\nfrom studio.evidence_validation import (\n    Claim,\n    ClaimClassification,\n    EvidencePosition,\n    EvidenceRecord,\n    validate_evidence,\n)\nfrom studio.hero_visual import (\n    HERO_VISUAL_HEIGHT,\n    HERO_VISUAL_WIDTH,\n    DeterministicHeroVisualProvider,\n    HeroVisualProviderError,\n    HeroVisualRequest,\n    HeroVisualStatus,\n    HeroVisualSystem,\n    HeroVisualValidationStatus,\n    ProviderVisual,\n)\nfrom studio.publication_package import (\n    HeroVisualPackageState,\n    PublicationPackageBuilder,\n)\n\n\nPROMPT = \"A restrained editorial evidence checkpoint with calm geometric balance.\"\n\n\ndef request(**changes):\n    values = {\n        \"prompt\": PROMPT,\n        \"visual_intent\": \"Show disciplined review protecting trust.\",\n    }\n    values.update(changes)\n    return HeroVisualRequest(**values)\n\n\ndef evidence_report():\n    claim = Claim(\n        identifier=\"claim-1\",\n        text=\"Structured review reduced avoidable rework.\",\n        classification=ClaimClassification.SOURCE_ASSERTION,\n    )\n    records = tuple(\n        EvidenceRecord(\n            source_identifier=f\"source-{number}\",\n            claim_identifier=claim.identifier,\n            position=EvidencePosition.SUPPORTS,\n            independent_group=f\"group-{number}\",\n            published_on=date(2026, 7, 1),\n        )\n        for number in (1, 2)\n    )\n    return validate_evidence((claim,), records, current_on=date(2026, 8, 2))\n\n\ndef publication_package(*, hero_visual_prompt=PROMPT):\n    article_request = ArticleRequest(\n        intent_identifier=\"intent-1\",\n        editorial_intent=\"Explain why evidence-led review improves decisions.\",\n        thesis=\"Evidence-Led Review Strengthens Decisions\",\n        author_perspective=\"Disciplined review protects both speed and trust.\",\n        audience=\"Professional leaders\",\n        insights=(\"Evidence exposes assumptions before publication.\",),\n        practical_takeaway=\"Apply an explicit evidence gate.\",\n        cta_question=\"Where would stronger review improve your decisions?\",\n        hero_visual_prompt=hero_visual_prompt,\n        hashtags=(\"#EditorialIntegrity\",),\n        linkedin_description=\"A practical case for evidence-led review.\",\n        source_attributions=(\n            SourceAttribution(\"source-1\", \"Source 1\"),\n            SourceAttribution(\"source-2\", \"Source 2\"),\n        ),\n    )\n    report = evidence_report()\n    draft = ArticleEngine().create_article(article_request, report)\n    return PublicationPackageBuilder().build(draft, report)\n\n\nclass HeroVisualSystemTests(unittest.TestCase):\n    def test_valid_request_produces_validated_720_by_425_png(self):\n        result = HeroVisualSystem().generate(request())\n        self.assertTrue(result.ready)\n        self.assertEqual((result.width, result.height), (720, 425))\n        self.assertEqual(result.image_format, \"png\")\n        self.assertEqual(result.validation_status, HeroVisualValidationStatus.PASSED)\n        self.assertTrue(result.artifact.startswith(b\"\\x89PNG\"))\n        self.assertEqual(dict(result.provenance)[\"provider\"], \"deterministic\")\n\n    def test_incorrect_dimensions_are_malformed(self):\n        result = HeroVisualSystem().generate(request(width=721))\n        self.assertEqual(result.status, HeroVisualStatus.MALFORMED_REQUEST)\n        self.assertIn(\"720 x 425\", result.failure_reason)\n        self.assertIsNone(result.artifact)\n\n    def test_approved_prompt_is_preserved(self):\n        result = HeroVisualSystem().generate(request())\n        self.assertEqual(result.prompt, PROMPT)\n\n    def test_provider_independent_orchestration(self):\n        class AlternateProvider:\n            provider_name = \"alternate\"\n\n            def generate(self, visual_request):\n                base = DeterministicHeroVisualProvider().generate(visual_request)\n                return ProviderVisual(\n                    artifact=base.artifact,\n                    width=base.width,\n                    height=base.height,\n                    image_format=base.image_format,\n                    provenance=((\"provider\", self.provider_name), (\"provider_version\", \"1\")),\n                )\n\n        result = HeroVisualSystem((AlternateProvider(),)).generate(request(provider=\"alternate\"))\n        self.assertTrue(result.ready)\n        self.assertEqual(result.provider, \"alternate\")\n\n    def test_deterministic_provider_is_repeatable(self):\n        first = HeroVisualSystem().generate(request())\n        second = HeroVisualSystem().generate(request())\n        self.assertEqual(first.artifact, second.artifact)\n        self.assertEqual(first.artifact_sha256, second.artifact_sha256)\n\n    def test_unsupported_provider_is_explicit(self):\n        result = HeroVisualSystem().generate(request(provider=\"missing\"))\n        self.assertEqual(result.status, HeroVisualStatus.UNSUPPORTED_PROVIDER)\n        self.assertIn(\"not configured\", result.failure_reason)\n\n    def test_malformed_request_is_explicit(self):\n        result = HeroVisualSystem().generate(request(prompt=\"\"))\n        self.assertEqual(result.status, HeroVisualStatus.MALFORMED_REQUEST)\n        self.assertEqual(result.validation_status, HeroVisualValidationStatus.NOT_RUN)\n\n    def test_generation_failure_is_not_reported_as_success(self):\n        class FailingProvider:\n            provider_name = \"failing\"\n\n            def generate(self, visual_request):\n                raise HeroVisualProviderError(\"provider unavailable\")\n\n        result = HeroVisualSystem((FailingProvider(),)).generate(request(provider=\"failing\"))\n        self.assertEqual(result.status, HeroVisualStatus.GENERATION_FAILED)\n        self.assertFalse(result.ready)\n        self.assertIn(\"unavailable\", result.failure_reason)\n\n    def test_validation_failure_is_distinct(self):\n        class WrongDimensions:\n            provider_name = \"wrong\"\n\n            def generate(self, visual_request):\n                base = DeterministicHeroVisualProvider().generate(visual_request)\n                return ProviderVisual(base.artifact, 700, 425, \"png\", ((\"provider\", \"wrong\"), (\"provider_version\", \"1\")))\n\n        result = HeroVisualSystem((WrongDimensions(),)).generate(request(provider=\"wrong\"))\n        self.assertEqual(result.status, HeroVisualStatus.VALIDATION_FAILED)\n        self.assertEqual(result.validation_status, HeroVisualValidationStatus.FAILED)\n\n    def test_unapproved_logo_face_and_text_requests_are_blocked(self):\n        for value in (\"Add a logo\", \"Use a recognizable face\", \"Add a text overlay\"):\n            with self.subTest(prompt=value):\n                result = HeroVisualSystem().generate(request(prompt=value))\n                self.assertEqual(result.status, HeroVisualStatus.BLOCKED)\n                self.assertFalse(result.ready)\n\n\nclass PublicationPackageHeroVisualTests(unittest.TestCase):\n    def test_new_package_starts_pending(self):\n        package = publication_package()\n        self.assertEqual(package.hero_visual_state, HeroVisualPackageState.PENDING)\n        self.assertIsNone(package.rendered_hero_visual)\n\n    def test_ready_result_attaches_without_regeneration(self):\n        package = publication_package()\n        result = HeroVisualSystem().generate(request())\n        attached = PublicationPackageBuilder().attach_hero_visual(package, result)\n        self.assertEqual(attached.hero_visual_state, HeroVisualPackageState.READY)\n        self.assertIs(attached.rendered_hero_visual, result)\n        self.assertNotIn(\"Rendered Hero Visual - Capability 010\", attached.deferred_components)\n        self.assertIn(\"Portable Editorial Project - Capability 011\", attached.deferred_components)\n\n    def test_failed_result_remains_explicit(self):\n        package = publication_package()\n        result = HeroVisualSystem().generate(request(provider=\"missing\"))\n        attached = PublicationPackageBuilder().attach_hero_visual(package, result)\n        self.assertEqual(attached.hero_visual_state, HeroVisualPackageState.FAILED)\n        self.assertEqual(attached.rendered_hero_visual.status, HeroVisualStatus.UNSUPPORTED_PROVIDER)\n\n    def test_blocked_result_remains_distinct(self):\n        blocked_prompt = \"Add a logo\"\n        package = publication_package(hero_visual_prompt=blocked_prompt)\n        result = HeroVisualSystem().generate(request(prompt=blocked_prompt))\n        attached = PublicationPackageBuilder().attach_hero_visual(package, result)\n        self.assertEqual(attached.hero_visual_state, HeroVisualPackageState.BLOCKED)\n\n    def test_textual_package_content_is_unchanged(self):\n        package = publication_package()\n        before = package.required_text_components()\n        article = package.article_markdown\n        attached = PublicationPackageBuilder().attach_hero_visual(\n            package, HeroVisualSystem().generate(request())\n        )\n        self.assertEqual(attached.required_text_components(), before)\n        self.assertEqual(attached.article_markdown, article)\n\n    def test_prompt_mismatch_cannot_attach(self):\n        package = publication_package()\n        result = HeroVisualSystem().generate(request(prompt=\"Different approved prompt\"))\n        with self.assertRaisesRegex(ValueError, \"approved prompt\"):\n            PublicationPackageBuilder().attach_hero_visual(package, result)\n\n    def test_existing_result_cannot_be_silently_regenerated(self):\n        builder = PublicationPackageBuilder()\n        package = builder.attach_hero_visual(\n            publication_package(), HeroVisualSystem().generate(request())\n        )\n        with self.assertRaisesRegex(ValueError, \"already has\"):\n            builder.attach_hero_visual(package, HeroVisualSystem().generate(request()))\n\n\nif __name__ == \"__main__\":\n    unittest.main()\n"),
    "tests/test_capability010_documentation.py": clean("\"\"\"Architecture, scope, and generator contracts for Capability 010.\"\"\"\n\nimport hashlib\nimport sys\nimport unittest\nfrom pathlib import Path\n\n\nROOT = Path(__file__).resolve().parents[1]\nSCRIPTS = str(ROOT / \"scripts\")\nif SCRIPTS not in sys.path:\n    sys.path.insert(0, SCRIPTS)\n\n\nclass Capability010DocumentationTests(unittest.TestCase):\n    def content(self, relative):\n        return (ROOT / relative).read_text(encoding=\"utf-8\")\n\n    def digest(self, relative):\n        return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()\n\n    def test_adr_baseline_architecture_and_demo_exist(self):\n        required = (\n            \"docs/architecture/adr/ADR-016-hero-visual-system.md\",\n            \"docs/architecture/baselines/Architecture_Baseline_2026.08.02v12.md\",\n            \"docs/architecture/Hero_Visual_System.md\",\n            \"docs/demos/Capability-010-Hero-Visual-System.md\",\n        )\n        for relative in required:\n            self.assertTrue((ROOT / relative).is_file(), relative)\n\n    def test_current_authorities_define_the_narrow_scope(self):\n        for relative in (\n            \"ROADMAP.md\",\n            \"docs/VERSION_ONE_SCORECARD.md\",\n            \"docs/product/Current_Product_Focus.md\",\n            \"docs/product/PRD_v1.3.md\",\n            \"docs/product/Release_v1.0.md\",\n        ):\n            content = self.content(relative)\n            self.assertIn(\"CAPABILITY_010\", content)\n            self.assertIn(\"720\", content)\n            self.assertIn(\"425\", content)\n            self.assertIn(\"Capability 011\", content)\n\n    def test_no_deferred_runtime_subsystems_were_added(self):\n        forbidden = (\n            \"studio/portable_editorial_project.py\",\n            \"studio/editorial_workspace.py\",\n            \"studio/component_collaboration.py\",\n            \"studio/editorial_orchestrator.py\",\n            \"studio/hero_visual_ui.py\",\n        )\n        for relative in forbidden:\n            self.assertFalse((ROOT / relative).exists(), relative)\n\n    def test_article_engine_and_brand_masters_are_unchanged(self):\n        self.assertEqual(self.digest(\"studio/article_engine.py\"), \"653db77e8881aa6532906fa1b17a8c771152cfe14ef1266383daba423d596868\")\n        self.assertEqual(self.digest(\"assets/brand/logo/master/editorial-compass-mark-master.png\"), \"b2cd1c22239b7176b43578892b0c37ac502ca5ab696b7c083a0b397bfe285727\")\n        self.assertEqual(self.digest(\"assets/brand/logo/master/editorial-compass-lockup-master.png\"), \"ae56f16f3e4b3a2bfbf5cefbf6ee807482cd8814e30b7496a917b9eae3a5ba72\")\n\n    def test_capability009_bootstrap_preserves_the_integration(self):\n        import bootstrap_capability009_article_engine_publication_package as cap009\n        import bootstrap_capability010_hero_visual_system as cap010\n\n        live = self.content(\"studio/publication_package.py\")\n        self.assertEqual(cap009.FILES[\"studio/publication_package.py\"], live)\n        self.assertEqual(cap010.FILES[\"studio/publication_package.py\"], live)\n\n\nif __name__ == \"__main__\":\n    unittest.main()\n"),
    "docs/architecture/Hero_Visual_System.md": clean("# Hero Visual System\n\n## Status\n\nCapability 010 executable architecture.\n\n## Responsibility\n\nThe Hero Visual System consumes the approved Hero Visual prompt from the\nCapability 009 Publication Package and returns either a validated 720 × 425\nPNG artifact or one explicit failure state. It preserves the prompt and visual\nintent and never reports success when generation or validation fails.\n\n## Provider Boundary\n\n`HeroVisualProvider` is the stable provider-neutral interface. Providers return\nuntrusted artifact bytes, dimensions, format, and provenance. The core system\nvalidates every response independently before it can become `ready`.\n\nThe repository includes `DeterministicHeroVisualProvider` for tests, demos,\noffline validation, and repeatable generation. It uses only the Python standard\nlibrary and requires no network access.\n\n## Output Contract\n\nA ready Hero Visual requires:\n\n- width `720`;\n- height `425`;\n- PNG format;\n- a non-empty PNG artifact whose header dimensions match the contract;\n- provider name and version provenance;\n- `ready` generation status; and\n- `passed` validation status.\n\nThe runtime distinguishes ready, generation failed, validation failed,\nunsupported provider, malformed request, and policy/editorial blocking.\n\n## Publication Package Boundary\n\nThe Publication Package begins with a pending Hero Visual state. It may attach\none existing `HeroVisualResult` whose prompt matches the approved package\nprompt. Attachment never invokes a provider, regenerates textual content, or\nchanges an approved article. Ready, failed, and blocked states remain distinct.\n\n## Policy and Brand Neutrality\n\nBrand-neutral generation is the default. Logo, recognizable-face, or text\noverlay requests are blocked unless the request contract explicitly permits\nthe relevant category. Logo use additionally requires explicit approved brand\ncontext. The B001 brand masters are neither inputs nor outputs of this system.\n\n## Explicit Boundaries\n\nCapability 010 introduces no Portable Editorial Project, project resume or\nexport, workspace, collaboration, orchestration, UI, publication automation,\nrelease packaging, or Version 2 behavior.\n"),
    "docs/architecture/adr/ADR-016-hero-visual-system.md": clean("# ADR-016 - Hero Visual System\n\n## Status\n\nProposed during Capability 010. Becomes Accepted when the capability is\ndelivered.\n\n## Date\n\n2026-08-02\n\n## Decision Level\n\nD4 - Architecture\n\n## Context\n\nCapability 009 produces an approved Hero Visual prompt but intentionally does\nnot render an image. Version 1 requires a 720 × 425 Hero Visual while repository\nvalidation must remain deterministic, offline, and independent of any external\ngeneration service.\n\n## Decision\n\nAdopt one provider-independent Hero Visual System. The core validates requests,\napplies explicit policy constraints, invokes a selected provider, validates the\nreturned artifact and provenance, and exposes distinct success and failure\nstates.\n\nRequire a 720 × 425 PNG output contract for Version 1. Include an offline\ndeterministic provider for tests and demonstrations. Treat every provider\nresponse as untrusted until core validation passes.\n\nIntegrate with the Publication Package only by attaching one existing result\nwhose prompt matches the approved Capability 009 prompt. Do not silently invoke\na provider, regenerate approved content, or claim Portable Project completion.\n\n## Constitutional Impact\n\nThe decision implements Understanding Before Generation, Evidence Before\nAssertion, Trust Above All, Professional Judgement, Author ownership, and\napproved-component preservation. It changes no frozen constitutional principle\nor canonical term.\n\n## Alternatives Considered\n\n### Require one external image provider\n\nRejected because validation would depend on network access, credentials, and\nprovider availability, and provider behavior could leak into the core contract.\n\n### Trust provider metadata without validating the artifact\n\nRejected because dimensions, format, content availability, and provenance must\nbe verified rather than asserted.\n\n### Generate the visual during Publication Package assembly\n\nRejected because it would silently couple package construction to generation\nand make focused revision and failure recovery unsafe.\n\n### Implement Portable Project or UI behavior simultaneously\n\nRejected because those are later or separate product surfaces and would expand\nCapability 010 beyond its approved boundary.\n\n## Consequences\n\nThe repository can deterministically demonstrate and validate Hero Visual\ngeneration without an external service. Future providers may implement the\nsame boundary without changing Publication Package semantics. Version 1 remains\nincomplete until Capability 011 and end-to-end release-readiness work complete.\n\n## Architecture Baseline\n\nRecorded by Architecture Baseline `2026.08.02v12`.\n"),
    "docs/architecture/baselines/Architecture_Baseline_2026.08.02v12.md": clean("# Architecture Baseline - 2026.08.02v12\n\n## Status\n\nProposed during Capability 010. Becomes current only when Capability 010 is\ndelivered.\n\n## Baseline ID\n\n`2026.08.02v12`\n\n## Supersedes\n\n`2026.08.02v11`\n\n## Reason for Revision\n\nAdd the provider-independent Hero Visual System and the narrow Publication\nPackage attachment boundary required for a validated 720 × 425 visual.\n\n## Runtime Architecture\n\n- `studio/hero_visual.py` owns request validation, policy constraints, provider\n  selection, artifact validation, provenance, and explicit outcome states.\n- `HeroVisualProvider` is the stable provider-neutral generation boundary.\n- `DeterministicHeroVisualProvider` supplies an offline, repeatable PNG artifact\n  for tests, demos, and repository validation.\n- `studio/publication_package.py` attaches one existing result without invoking\n  generation or modifying textual package content.\n\n## Trust and Failure Model\n\nProvider output is untrusted until the core verifies format, dimensions,\nartifact presence, PNG header, and provenance. Malformed requests, unsupported\nproviders, generation failures, validation failures, and policy blocks remain\ndistinct and cannot be presented as ready.\n\n## Explicit Exclusions\n\nNo Portable Editorial Project, project resume or export, workspace,\ncollaboration, orchestration, UI, publishing automation, release packaging,\nB002, or Version 2 architecture is introduced.\n\n## Architecture Decision\n\nADR-016 records the durable decision.\n"),
    "docs/demos/Capability-010-Hero-Visual-System.md": clean("# Capability 010 Demo - Hero Visual System\n\n## Problem\n\nCapability 009 produced an approved Hero Visual prompt but had no safe,\nprovider-independent way to create or validate the required 720 × 425 visual.\n\n## What Changed\n\nThe Hero Visual System now validates the request, applies brand-neutral policy\nconstraints, invokes a provider behind a stable interface, validates the\nartifact and provenance, and returns an explicit outcome. The Publication\nPackage may attach the result without regenerating approved text.\n\n## Example\n\n```text\nApproved Capability 009 Hero Visual prompt\n                    |\n                    v\n       request and policy validation\n                    |\n        +-----------+-----------+\n        |                       |\n      blocked             selected provider\n                                |\n                                v\n                    untrusted visual artifact\n                                |\n                                v\n                format + dimensions + provenance\n                                |\n                    +-----------+-----------+\n                    |                       |\n             validation failed       ready 720 x 425 PNG\n                                            |\n                                            v\n                              attach to Publication Package\n```\n\n## Author Benefit\n\nThe Author receives a clear ready, failed, or blocked visual state without the\nStudio altering the approved article, changing the prompt, fabricating success,\nor requiring one external provider.\n\n## Acceptance Evidence\n\nBehavioral tests cover dimensions, prompt preservation, provider independence,\ndeterministic repeatability, malformed and unsupported requests, generation and\nvalidation failure, policy blocking, package pending/ready/failed/blocked\nstates, approved-content preservation, and no silent regeneration.\n\n## Learning\n\nGeneration and validation are separate trust decisions. Treating provider\noutput as untrusted makes external-provider evolution possible without\nweakening the stable publication contract.\n\n## Next\n\nCapability 011 remains responsible for Portable Editorial Project resume and\nexport. End-to-end RC1 release readiness remains separate.\n"),
}

FILES["tests/test_capability010_documentation.py"] = FILES[
    "tests/test_capability010_documentation.py"
].replace(
    '            "studio/editorial_workspace.py",\n',
    "",
).replace(
    '        self.assertEqual(self.digest("studio/article_engine.py"), "653db77e8881aa6532906fa1b17a8c771152cfe14ef1266383daba423d596868")\n',
    '        self.assertEqual(self.digest("studio/article_engine.py"), "653db77e8881aa6532906fa1b17a8c771152cfe14ef1266383daba423d596868")\n'
    '        self.assertEqual(self.digest("studio/editorial_workspace.py"), "2bb9a08fc9c11c496f518509019b569ee90d5b89653f08321b8b7d5ab5d1566c")\n',
)

FILES["studio/hero_visual.py"] = FILES["studio/hero_visual.py"].replace(
    "    provider: str\n    prompt: str\n    width: int\n",
    "    provider: str\n    prompt: str\n    visual_intent: str\n    width: int\n",
).replace(
    "            provider=provider.provider_name,\n            prompt=request.prompt,\n            width=generated.width,\n",
    "            provider=provider.provider_name,\n            prompt=request.prompt,\n            visual_intent=request.visual_intent,\n            width=generated.width,\n",
).replace(
    "            provider=provider or request.provider,\n            prompt=request.prompt,\n            width=request.width,\n",
    "            provider=provider or request.provider,\n            prompt=request.prompt,\n            visual_intent=request.visual_intent,\n            width=request.width,\n",
)
FILES["tests/test_capability010_hero_visual.py"] = FILES[
    "tests/test_capability010_hero_visual.py"
].replace(
    "        self.assertEqual(result.prompt, PROMPT)\n",
    "        self.assertEqual(result.prompt, PROMPT)\n"
    '        self.assertEqual(result.visual_intent, "Show disciplined review protecting trust.")\n',
)

PUBLICATION_PACKAGE = FILES["studio/publication_package.py"]

MANAGED = {
    "docs/architecture/adr/README.md": ("CAPABILITY_010_ADR_INDEX", clean("## Capability 010 Decision\n\n- [ADR-016 - Hero Visual System](ADR-016-hero-visual-system.md)\n")),
    "docs/architecture/Publication_Package_Contract.md": ("CAPABILITY_010_PUBLICATION_PACKAGE_CONTRACT", clean("## Capability 010 Hero Visual Boundary\n\nThe Hero Visual System consumes the approved Hero Visual prompt and returns a\nvalidated 720 × 425 PNG or an explicit generation, validation, provider,\nrequest, or policy failure.\n\nThe Publication Package begins with a pending Hero Visual state and may attach\none existing result whose prompt matches the approved package prompt. Attachment\ndoes not invoke generation, modify textual components, or silently replace an\nalready attached result. Ready, failed, and blocked states remain distinct.\n\nPortable Editorial Project serialization, resume, and export remain Capability\n011. The complete Version 1.0 package remains incomplete until that capability\nand release-readiness evidence are delivered.\n")),
    "ROADMAP.md": ("CAPABILITY_010_ROADMAP", clean("## Capability 010 - Hero Visual System\n\nStatus: **In Progress**\n\nApproved scope:\n\n- [x] Provider-independent Hero Visual boundary\n- [x] Validated 720 × 425 PNG contract\n- [x] Deterministic offline validation provider\n- [x] Explicit generation, validation, provider, request, and policy states\n- [x] Narrow Publication Package attachment boundary\n- [x] Approved prompt and textual-content preservation\n\nCapability 011 remains Todo and unstarted. B002 remains Todo, Low Priority,\nPost-RC1, and non-blocking. Architecture Baseline `2026.08.02v11` remains the\ncurrent delivered baseline while proposed baseline `2026.08.02v12` records this\nincrement.\n\nNo Portable Project, workspace, collaboration, orchestration, UI, publishing\nautomation, release packaging, or Version 2 behavior is included.\n")),
    "docs/VERSION_ONE_SCORECARD.md": ("CAPABILITY_010_SCORECARD", clean("## Capability 010 Progress\n\n| Area | Status | Evidence |\n|---|---|---|\n| Capability 009 | Complete | Article Engine and textual Publication Package |\n| Hero Visual provider boundary | Complete locally | `studio/hero_visual.py` |\n| 720 × 425 output validation | Complete locally | Behavioral tests |\n| Deterministic offline provider | Complete locally | Repeatability tests |\n| Explicit failure states | Complete locally | Generation and validation tests |\n| Publication Package integration | Complete locally | Pending/ready/failed/blocked tests |\n| Capability 011 | Todo and unstarted | Issue #17 |\n| B002 | Todo, Low Priority, Post-RC1, non-blocking | Issue #41 |\n| Current delivered baseline | Complete | `2026.08.02v11` |\n| Proposed Capability 010 baseline | Pending delivery | `2026.08.02v12` |\n\nVersion 1 remains incomplete until Capability 011 and end-to-end release\nreadiness are delivered.\n")),
    "docs/product/Current_Product_Focus.md": ("CAPABILITY_010_CURRENT_FOCUS", clean("## Capability 010 Active Focus\n\nCapability 010 implements the provider-independent Hero Visual System for the\nexisting Capability 009 Publication Package. It consumes the approved prompt,\npreserves visual intent, validates a 720 × 425 PNG and its provenance, and\nreturns explicit safe failure states when generation cannot be trusted.\n\nThe Publication Package integration attaches one existing result without\nregenerating approved article content. Capability 011 remains Todo and\nunstarted. B002 remains deferred, Low Priority, Post-RC1, and non-blocking.\n\nNo Portable Project, workspace, collaboration, orchestration, UI, publishing\nautomation, release packaging, or Version 2 behavior is part of this focus.\n")),
    "docs/product/PRD_v1.3.md": ("CAPABILITY_010_PRD", clean("## Capability 010 Requirements\n\nVersion 1.0 shall provide a Hero Visual System that:\n\n- consumes the approved Capability 009 Hero Visual prompt;\n- preserves approved visual intent and editorial context;\n- uses a provider-independent generation boundary;\n- validates an exact 720 × 425 PNG artifact and provenance;\n- distinguishes ready, generation failed, validation failed, unsupported\n  provider, malformed request, and policy/editorial blocking;\n- includes an offline deterministic provider for repository validation;\n- remains brand-neutral unless explicit approved context permits otherwise;\n- never reports a failed or unvalidated artifact as ready; and\n- attaches one existing result without silently regenerating approved package\n  components.\n\nCapability 011 retains Portable Editorial Project serialization, resume, and\nexport. Capability 010 adds no workspace, collaboration, orchestration, UI,\npublishing automation, release packaging, or Version 2 product surface.\n")),
    "docs/product/Release_v1.0.md": ("CAPABILITY_010_RELEASE_STATUS", clean("## Capability 010 Release Contribution\n\nCapability 010 is In Progress and adds the provider-independent 720 × 425 Hero\nVisual System, deterministic validation provider, explicit failure states, and\nthe narrow Publication Package attachment boundary.\n\nThe current delivered architecture baseline is `2026.08.02v11`. Proposed\nbaseline `2026.08.02v12` becomes current only when Capability 010 is delivered.\n\nVersion 1 remains incomplete. Capability 011 Portable Editorial Project resume\nand export and issue #18 end-to-end release-readiness evidence remain\noutstanding. B002 remains non-blocking Post-RC1 work.\n")),
    "docs/architecture/Definition_of_Done.md": ("CAPABILITY_010_DEFINITION_OF_DONE", clean("## Capability 010 Completion Additions\n\nConfirm:\n\n- the approved Capability 009 Hero Visual prompt is preserved;\n- provider-specific behavior remains behind `HeroVisualProvider`;\n- ready output is a validated 720 × 425 PNG with provenance;\n- deterministic generation is offline and repeatable;\n- malformed, unsupported, failed, invalid, and blocked states remain distinct;\n- no failed or unvalidated artifact is reported ready;\n- Publication Package attachment does not regenerate or change textual content;\n- already attached results are protected from silent replacement;\n- approved brand masters remain unchanged and are not Hero Visual inputs;\n- no Portable Project, workspace, collaboration, orchestration, UI, publishing\n  automation, release packaging, or Version 2 behavior is introduced;\n- the Capability 010 demo is current; and\n- complete repository validation passes.\n")),
    "docs/product/Decision_Log.md": ("CAPABILITY_010_DECISION_LOG", clean("## Capability 010 Decisions\n\n| Date | Level | Decision | Rationale |\n|---|---:|---|---|\n| 2026-08-02 | D4 | Adopt a provider-independent Hero Visual boundary | Visual-generation providers must not define the stable product contract. |\n| 2026-08-02 | D4 | Validate every provider artifact in the core | Provider claims cannot substitute for verified dimensions, format, bytes, and provenance. |\n| 2026-08-02 | D4 | Include an offline deterministic provider | Tests, demos, bootstrap recovery, and repository validation must not require network access. |\n| 2026-08-02 | D4 | Attach results without implicit generation | Approved prompts and textual package components must not be silently regenerated. |\n\nADR-016 and proposed Architecture Baseline `2026.08.02v12` record the durable\narchitecture.\n")),
    "CHANGELOG.md": ("CAPABILITY_010_CHANGELOG", clean("### Added - Capability 010\n\n- Provider-independent Hero Visual System\n- Validated 720 × 425 PNG output contract\n- Offline deterministic Hero Visual provider\n- Explicit generation, validation, provider, request, and policy states\n- Narrow Publication Package Hero Visual attachment boundary\n- Approved prompt and textual-component preservation\n- ADR-016 and proposed Architecture Baseline 2026.08.02v12\n- Capability 010 behavioral, documentation, and demo coverage\n")),
}

# RC1_CAPABILITY010_RECONCILIATION_OWNER_SYNC_START
from bootstrap_rc1_capability010_reconciliation import (
    CAPABILITY010_FILES as _rc1_capability010_files,
    CAPABILITY010_MANAGED as _rc1_capability010_managed,
)

FILES.update(_rc1_capability010_files)
MANAGED.update(_rc1_capability010_managed)
# RC1_CAPABILITY010_RECONCILIATION_OWNER_SYNC_END

OWNER_SYNC = clean("""
# CAPABILITY_010_HERO_VISUAL_OWNER_SYNC_START
from bootstrap_capability010_hero_visual_system import (
    PUBLICATION_PACKAGE as _capability010_publication_package,
)

FILES["studio/publication_package.py"] = _capability010_publication_package
# CAPABILITY_010_HERO_VISUAL_OWNER_SYNC_END
""")


def run(command: list[str], root: Path, *, capture: bool = False) -> str:
    result = subprocess.run(
        command, cwd=root, text=True, capture_output=capture, check=False
    )
    if result.returncode:
        detail = (result.stderr or result.stdout or "command failed").strip()
        raise CapabilityError(f"{' '.join(command)}: {detail}")
    return result.stdout if capture else ""


def repository_root() -> Path:
    root = Path(__file__).resolve().parents[1]
    if root.name != EXPECTED_REPOSITORY or not (root / ".git").exists():
        raise CapabilityError("Run from the expected repository.")
    return root


def changed_paths(root: Path) -> set[str]:
    output = run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        root,
        capture=True,
    )
    paths: set[str] = set()
    for line in output.splitlines():
        if not line:
            continue
        value = line[3:]
        if " -> " in value:
            value = value.split(" -> ", 1)[1]
        paths.add(value.strip('"'))
    return paths


def allowed_paths() -> set[str]:
    return {
        SCRIPT_PATH,
        CAPABILITY009_BOOTSTRAP,
        RC1_BOOTSTRAP,
        RC1_TEST,
        *FILES,
        *MANAGED,
    }


def verify_context(root: Path) -> None:
    branch = run(["git", "branch", "--show-current"], root, capture=True).strip()
    if branch != EXPECTED_BRANCH:
        raise CapabilityError(f"Expected {EXPECTED_BRANCH}; found {branch}.")
    unexpected = changed_paths(root) - allowed_paths()
    if unexpected:
        raise CapabilityError(
            "Unexpected working-tree paths: " + ", ".join(sorted(unexpected))
        )


def managed_text(original: str, marker: str, body: str) -> str:
    start = f"<!-- {marker}_START -->"
    end = f"<!-- {marker}_END -->"
    block = f"{start}\n\n{body.rstrip()}\n\n{end}"
    if start in original and end in original:
        prefix, rest = original.split(start, 1)
        _, suffix = rest.split(end, 1)
        return prefix.rstrip() + "\n\n" + block + suffix
    return original.rstrip() + "\n\n" + block + "\n"


def reconcile_release_baseline(content: str) -> str:
    old = "Architecture baseline:\n\n```text\n2026.08.02v10\n```"
    new = "Architecture baseline:\n\n```text\n2026.08.02v11\n```"
    if new in content:
        return content
    if content.count(old) != 1:
        raise CapabilityError("Could not reconcile the current Release baseline.")
    return content.replace(old, new, 1)


def synchronize_capability009_owner(content: str) -> str:
    start = "# CAPABILITY_010_HERO_VISUAL_OWNER_SYNC_START"
    end = "# CAPABILITY_010_HERO_VISUAL_OWNER_SYNC_END"
    if start in content and end in content:
        prefix, rest = content.split(start, 1)
        _, suffix = rest.split(end, 1)
        return prefix.rstrip() + "\n\n" + OWNER_SYNC.rstrip() + "\n\n" + suffix.lstrip()
    anchor = "\n\nMANAGED = {"
    if content.count(anchor) != 1:
        raise CapabilityError("Capability 009 owner synchronization anchor is ambiguous.")
    inserted = content.replace(anchor, "\n\n" + OWNER_SYNC.rstrip() + anchor, 1)
    return synchronize_capability009_owner(inserted)


def synchronize_rc1_test(content: str) -> str:
    return content.replace(
        "ba3e4bf6e0d92ff088279e8a6a8bf5e74b33845ca8056bd82cf4e1c1eb136500",
        "1e6cc91dda667f9b87eee248f563771f2cb99f0954346f3aef6f0e0bcb62d64b",
    ).replace(
        "Architecture baseline:\\n\\n```text\\n2026.08.02v10\\n```",
        "Architecture baseline:\\n\\n```text\\n2026.08.02v11\\n```",
    )


def synchronize_rc1_owner(content: str) -> str:
    content = synchronize_rc1_test(content)
    content = content.replace(
        'PUBLICATION_PACKAGE_HASH = "ba3e4bf6e0d92ff088279e8a6a8bf5e74b33845ca8056bd82cf4e1c1eb136500"',
        'PUBLICATION_PACKAGE_HASH = "1e6cc91dda667f9b87eee248f563771f2cb99f0954346f3aef6f0e0bcb62d64b"',
    )
    content = content.replace(
        '        "Architecture baseline:\\n\\n```text\\n2026.08.01v06\\n```",\n'
        '        "Architecture baseline:\\n\\n```text\\n2026.08.02v10\\n```",',
        '        "Architecture baseline:\\n\\n```text\\n2026.08.02v10\\n```",\n'
        '        "Architecture baseline:\\n\\n```text\\n2026.08.02v11\\n```",',
    )
    return content


def expected_content(root: Path) -> dict[str, str]:
    expected = dict(FILES)
    for relative, (marker, body) in MANAGED.items():
        original = (root / relative).read_text(encoding="utf-8")
        if relative == "docs/product/Release_v1.0.md":
            original = reconcile_release_baseline(original)
        expected[relative] = managed_text(original, marker, body)
    expected[CAPABILITY009_BOOTSTRAP] = synchronize_capability009_owner(
        (root / CAPABILITY009_BOOTSTRAP).read_text(encoding="utf-8")
    )
    expected[RC1_BOOTSTRAP] = synchronize_rc1_owner(
        (root / RC1_BOOTSTRAP).read_text(encoding="utf-8")
    )
    expected[RC1_TEST] = synchronize_rc1_test(
        (root / RC1_TEST).read_text(encoding="utf-8")
    )
    return expected


def apply(root: Path) -> None:
    before = hashlib.sha256((root / SCRIPT_PATH).read_bytes()).hexdigest()
    for relative, content in expected_content(root).items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    after = hashlib.sha256((root / SCRIPT_PATH).read_bytes()).hexdigest()
    if before != after:
        raise CapabilityError("Bootstrap modified itself during apply.")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_generated(root: Path) -> None:
    for relative, expected in expected_content(root).items():
        path = root / relative
        if not path.is_file() or path.read_text(encoding="utf-8") != expected:
            raise CapabilityError(f"Generated content differs: {relative}")
    if digest(root / "studio/article_engine.py") != ARTICLE_ENGINE_HASH:
        raise CapabilityError("Capability 009 Article Engine changed.")
    if digest(root / "studio/editorial_workspace.py") != EDITORIAL_WORKSPACE_HASH:
        raise CapabilityError("Existing Editorial Workspace runtime changed.")
    if digest(root / "assets/brand/logo/master/editorial-compass-mark-master.png") != MARK_HASH:
        raise CapabilityError("Approved brand mark master changed.")
    if digest(root / "assets/brand/logo/master/editorial-compass-lockup-master.png") != LOCKUP_HASH:
        raise CapabilityError("Approved brand lockup master changed.")
    forbidden = (
        "studio/portable_editorial_project.py",
        "studio/component_collaboration.py",
        "studio/editorial_orchestrator.py",
        "studio/hero_visual_ui.py",
    )
    if any((root / relative).exists() for relative in forbidden):
        raise CapabilityError("A deferred runtime subsystem was introduced.")


def validate_repository(root: Path) -> None:
    run([sys.executable, "-m", "compileall", "-q", "studio", "scripts", "tests"], root)
    run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], root)
    run([sys.executable, "studio.py", "validate"], root)
    run(["git", "diff", "--check"], root)


def preview(root: Path) -> None:
    print("Capability 010 Hero Visual System preview.")
    print("No files will be changed.\n")
    print("Generated files:")
    for relative in sorted(FILES):
        print(f"- {relative}")
    print("\nManaged documents:")
    for relative in sorted(MANAGED):
        print(f"- {relative}")
    print("\nOwning bootstrap synchronization:")
    print(f"- {CAPABILITY009_BOOTSTRAP}")
    print("\nExplicitly deferred:")
    print("- Capability 011 Portable Editorial Project")
    print("- workspace, collaboration, orchestration, UI, and publishing automation")
    print("- B002, release packaging, and Version 2")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    root = repository_root()
    verify_context(root)
    if not args.apply:
        preview(root)
        return 0
    apply(root)
    verify_context(root)
    validate_generated(root)
    validate_repository(root)
    print(SENTINEL)
    run(["git", "status", "--short"], root)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CapabilityError as exc:
        print(f"Capability 010 bootstrap stopped: {exc}", file=sys.stderr)
        raise SystemExit(1)
