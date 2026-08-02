"""Behavioral tests for Capability 010 Hero Visual System."""

from datetime import date
import unittest

from studio.article_engine import ArticleEngine, ArticleRequest, SourceAttribution
from studio.evidence_validation import (
    Claim,
    ClaimClassification,
    EvidencePosition,
    EvidenceRecord,
    validate_evidence,
)
from studio.hero_visual import (
    HERO_VISUAL_HEIGHT,
    HERO_VISUAL_WIDTH,
    DeterministicHeroVisualProvider,
    HeroVisualProviderError,
    HeroVisualRequest,
    HeroVisualStatus,
    HeroVisualSystem,
    HeroVisualValidationStatus,
    ProviderVisual,
)
from studio.publication_package import (
    HeroVisualPackageState,
    PublicationPackageBuilder,
)


PROMPT = "A restrained editorial evidence checkpoint with calm geometric balance."


def request(**changes):
    values = {
        "prompt": PROMPT,
        "visual_intent": "Show disciplined review protecting trust.",
    }
    values.update(changes)
    return HeroVisualRequest(**values)


def evidence_report():
    claim = Claim(
        identifier="claim-1",
        text="Structured review reduced avoidable rework.",
        classification=ClaimClassification.SOURCE_ASSERTION,
    )
    records = tuple(
        EvidenceRecord(
            source_identifier=f"source-{number}",
            claim_identifier=claim.identifier,
            position=EvidencePosition.SUPPORTS,
            independent_group=f"group-{number}",
            published_on=date(2026, 7, 1),
        )
        for number in (1, 2)
    )
    return validate_evidence((claim,), records, current_on=date(2026, 8, 2))


def publication_package(*, hero_visual_prompt=PROMPT):
    article_request = ArticleRequest(
        intent_identifier="intent-1",
        editorial_intent="Explain why evidence-led review improves decisions.",
        thesis="Evidence-Led Review Strengthens Decisions",
        author_perspective="Disciplined review protects both speed and trust.",
        audience="Professional leaders",
        insights=("Evidence exposes assumptions before publication.",),
        practical_takeaway="Apply an explicit evidence gate.",
        cta_question="Where would stronger review improve your decisions?",
        hero_visual_prompt=hero_visual_prompt,
        hashtags=("#EditorialIntegrity",),
        linkedin_description="A practical case for evidence-led review.",
        source_attributions=(
            SourceAttribution("source-1", "Source 1"),
            SourceAttribution("source-2", "Source 2"),
        ),
    )
    report = evidence_report()
    draft = ArticleEngine().create_article(article_request, report)
    return PublicationPackageBuilder().build(draft, report)


class HeroVisualSystemTests(unittest.TestCase):
    def test_valid_request_produces_validated_720_by_425_png(self):
        result = HeroVisualSystem().generate(request())
        self.assertTrue(result.ready)
        self.assertEqual((result.width, result.height), (720, 425))
        self.assertEqual(result.image_format, "png")
        self.assertEqual(result.validation_status, HeroVisualValidationStatus.PASSED)
        self.assertTrue(result.artifact.startswith(b"\x89PNG"))
        self.assertEqual(dict(result.provenance)["provider"], "deterministic")

    def test_incorrect_dimensions_are_malformed(self):
        result = HeroVisualSystem().generate(request(width=721))
        self.assertEqual(result.status, HeroVisualStatus.MALFORMED_REQUEST)
        self.assertIn("720 x 425", result.failure_reason)
        self.assertIsNone(result.artifact)

    def test_approved_prompt_is_preserved(self):
        result = HeroVisualSystem().generate(request())
        self.assertEqual(result.prompt, PROMPT)
        self.assertEqual(result.visual_intent, "Show disciplined review protecting trust.")

    def test_provider_independent_orchestration(self):
        class AlternateProvider:
            provider_name = "alternate"

            def generate(self, visual_request):
                base = DeterministicHeroVisualProvider().generate(visual_request)
                return ProviderVisual(
                    artifact=base.artifact,
                    width=base.width,
                    height=base.height,
                    image_format=base.image_format,
                    provenance=(("provider", self.provider_name), ("provider_version", "1")),
                )

        result = HeroVisualSystem((AlternateProvider(),)).generate(request(provider="alternate"))
        self.assertTrue(result.ready)
        self.assertEqual(result.provider, "alternate")

    def test_deterministic_provider_is_repeatable(self):
        first = HeroVisualSystem().generate(request())
        second = HeroVisualSystem().generate(request())
        self.assertEqual(first.artifact, second.artifact)
        self.assertEqual(first.artifact_sha256, second.artifact_sha256)

    def test_unsupported_provider_is_explicit(self):
        result = HeroVisualSystem().generate(request(provider="missing"))
        self.assertEqual(result.status, HeroVisualStatus.UNSUPPORTED_PROVIDER)
        self.assertIn("not configured", result.failure_reason)

    def test_malformed_request_is_explicit(self):
        result = HeroVisualSystem().generate(request(prompt=""))
        self.assertEqual(result.status, HeroVisualStatus.MALFORMED_REQUEST)
        self.assertEqual(result.validation_status, HeroVisualValidationStatus.NOT_RUN)

    def test_generation_failure_is_not_reported_as_success(self):
        class FailingProvider:
            provider_name = "failing"

            def generate(self, visual_request):
                raise HeroVisualProviderError("provider unavailable")

        result = HeroVisualSystem((FailingProvider(),)).generate(request(provider="failing"))
        self.assertEqual(result.status, HeroVisualStatus.GENERATION_FAILED)
        self.assertFalse(result.ready)
        self.assertIn("unavailable", result.failure_reason)

    def test_validation_failure_is_distinct(self):
        class WrongDimensions:
            provider_name = "wrong"

            def generate(self, visual_request):
                base = DeterministicHeroVisualProvider().generate(visual_request)
                return ProviderVisual(base.artifact, 700, 425, "png", (("provider", "wrong"), ("provider_version", "1")))

        result = HeroVisualSystem((WrongDimensions(),)).generate(request(provider="wrong"))
        self.assertEqual(result.status, HeroVisualStatus.VALIDATION_FAILED)
        self.assertEqual(result.validation_status, HeroVisualValidationStatus.FAILED)

    def test_unapproved_logo_face_and_text_requests_are_blocked(self):
        for value in ("Add a logo", "Use a recognizable face", "Add a text overlay"):
            with self.subTest(prompt=value):
                result = HeroVisualSystem().generate(request(prompt=value))
                self.assertEqual(result.status, HeroVisualStatus.BLOCKED)
                self.assertFalse(result.ready)


class PublicationPackageHeroVisualTests(unittest.TestCase):
    def test_new_package_starts_pending(self):
        package = publication_package()
        self.assertEqual(package.hero_visual_state, HeroVisualPackageState.PENDING)
        self.assertIsNone(package.rendered_hero_visual)

    def test_ready_result_attaches_without_regeneration(self):
        package = publication_package()
        result = HeroVisualSystem().generate(request())
        attached = PublicationPackageBuilder().attach_hero_visual(package, result)
        self.assertEqual(attached.hero_visual_state, HeroVisualPackageState.READY)
        self.assertIs(attached.rendered_hero_visual, result)
        self.assertNotIn("Rendered Hero Visual - Capability 010", attached.deferred_components)
        self.assertIn("Portable Editorial Project - Capability 011", attached.deferred_components)

    def test_failed_result_remains_explicit(self):
        package = publication_package()
        result = HeroVisualSystem().generate(request(provider="missing"))
        attached = PublicationPackageBuilder().attach_hero_visual(package, result)
        self.assertEqual(attached.hero_visual_state, HeroVisualPackageState.FAILED)
        self.assertEqual(attached.rendered_hero_visual.status, HeroVisualStatus.UNSUPPORTED_PROVIDER)

    def test_blocked_result_remains_distinct(self):
        blocked_prompt = "Add a logo"
        package = publication_package(hero_visual_prompt=blocked_prompt)
        result = HeroVisualSystem().generate(request(prompt=blocked_prompt))
        attached = PublicationPackageBuilder().attach_hero_visual(package, result)
        self.assertEqual(attached.hero_visual_state, HeroVisualPackageState.BLOCKED)

    def test_textual_package_content_is_unchanged(self):
        package = publication_package()
        before = package.required_text_components()
        article = package.article_markdown
        attached = PublicationPackageBuilder().attach_hero_visual(
            package, HeroVisualSystem().generate(request())
        )
        self.assertEqual(attached.required_text_components(), before)
        self.assertEqual(attached.article_markdown, article)

    def test_prompt_mismatch_cannot_attach(self):
        package = publication_package()
        result = HeroVisualSystem().generate(request(prompt="Different approved prompt"))
        with self.assertRaisesRegex(ValueError, "approved prompt"):
            PublicationPackageBuilder().attach_hero_visual(package, result)

    def test_existing_result_cannot_be_silently_regenerated(self):
        builder = PublicationPackageBuilder()
        package = builder.attach_hero_visual(
            publication_package(), HeroVisualSystem().generate(request())
        )
        with self.assertRaisesRegex(ValueError, "already has"):
            builder.attach_hero_visual(package, HeroVisualSystem().generate(request()))


if __name__ == "__main__":
    unittest.main()
