"""Behavioural tests for Capability 009's narrow runtime scope."""

from datetime import date
import unittest

from studio.article_engine import (
    ArticleDraft,
    ArticleEngine,
    ArticleEngineError,
    ArticleRequest,
    PublicationBlockedError,
    SourceAttribution,
)
from studio.evidence_validation import (
    Claim,
    ClaimClassification,
    EditorialConfidence,
    EditorialRisk,
    EvidencePosition,
    EvidenceRecord,
    validate_evidence,
)
from studio.publication_package import (
    PackageReadiness,
    PublicationPackageBuilder,
)


def report(*, supports=2, material=True, contradiction=False):
    claim = Claim(
        identifier="claim-1",
        text="Structured review reduced avoidable rework.",
        classification=ClaimClassification.SOURCE_ASSERTION,
        material=material,
    )
    records = [
        EvidenceRecord(
            source_identifier=f"source-{number}",
            claim_identifier="claim-1",
            position=EvidencePosition.SUPPORTS,
            independent_group=f"group-{number}",
            published_on=date(2026, 7, 1),
        )
        for number in range(1, supports + 1)
    ]
    if contradiction:
        records.append(
            EvidenceRecord(
                source_identifier="contradiction",
                claim_identifier="claim-1",
                position=EvidencePosition.CONTRADICTS,
                independent_group="contradiction",
            )
        )
    return validate_evidence(
        (claim,), records, current_on=date(2026, 8, 1)
    )


def request(*, sources=("source-1", "source-2")):
    return ArticleRequest(
        intent_identifier="intent-1",
        editorial_intent="Explain why evidence-led review improves decisions.",
        thesis="Evidence-Led Review Strengthens Editorial Decisions",
        author_perspective=(
            "In my experience, disciplined review protects both speed and trust."
        ),
        audience="Senior professional leaders",
        insights=(
            "Evidence exposes assumptions before they become polished claims.",
            "Clear editorial gates preserve confidence without replacing judgement.",
        ),
        practical_takeaway="Make material claims pass an explicit evidence gate.",
        cta_question="Where would stronger evidence review improve your decisions?",
        hero_visual_prompt="A restrained editorial evidence checkpoint.",
        hashtags=("#EditorialIntegrity", "#Leadership"),
        linkedin_description="A practical case for evidence-led editorial review.",
        source_attributions=tuple(
            SourceAttribution(item, f"{item} — reviewed evidence")
            for item in sources
        ),
    )


class ArticleRequestTests(unittest.TestCase):
    def test_request_requires_one_or_two_insights(self):
        values = request().__dict__ | {"insights": ()}
        with self.assertRaisesRegex(ArticleEngineError, "one or two"):
            ArticleRequest(**values)

    def test_cta_requires_article_specific_question(self):
        values = request().__dict__ | {"cta_question": "Share your view."}
        with self.assertRaisesRegex(ArticleEngineError, "question"):
            ArticleRequest(**values)

    def test_source_identifiers_must_be_unique(self):
        with self.assertRaisesRegex(ArticleEngineError, "unique"):
            request(sources=("Source", " source "))

    def test_source_and_attribution_is_required(self):
        with self.assertRaisesRegex(ArticleEngineError, "source and attribution"):
            request(sources=())


class ArticleEngineTests(unittest.TestCase):
    def test_low_risk_builds_original_structured_article(self):
        draft = ArticleEngine().create_article(request(), report())
        self.assertEqual(draft.intent_identifier, "intent-1")
        self.assertIn("# Evidence-Led Review", draft.article_markdown)
        self.assertIn("## Sources and Attribution", draft.article_markdown)
        self.assertNotIn("source material excerpt", draft.article_markdown)

    def test_high_risk_blocks_provider_before_generation(self):
        class NeverCalled:
            def create_draft(self, request, evidence_report):
                raise AssertionError("provider must not be called")

        with self.assertRaises(PublicationBlockedError):
            ArticleEngine(NeverCalled()).create_article(request(), report(supports=0))

    def test_severe_contradiction_blocks_generation(self):
        with self.assertRaises(PublicationBlockedError):
            ArticleEngine().create_article(
                request(sources=("source-1", "source-2", "contradiction")),
                report(contradiction=True),
            )

    def test_provider_cannot_change_approved_intent(self):
        class ChangedIntent:
            def create_draft(self, request, evidence_report):
                base = ArticleEngine().provider.create_draft(
                    request, evidence_report
                )
                return ArticleDraft(
                    **(base.__dict__ | {"intent_identifier": "different"})
                )

        with self.assertRaisesRegex(ArticleEngineError, "Editorial Intent"):
            ArticleEngine(ChangedIntent()).create_article(request(), report())

    def test_every_used_evidence_source_requires_attribution(self):
        with self.assertRaisesRegex(ArticleEngineError, "requires attribution"):
            ArticleEngine().create_article(
                request(sources=("source-1",)), report()
            )

    def test_provider_must_identify_validated_claims_used(self):
        class OmitsClaims:
            def create_draft(self, request, evidence_report):
                base = ArticleEngine().provider.create_draft(
                    request, evidence_report
                )
                return ArticleDraft(
                    **(base.__dict__ | {"used_claim_identifiers": ()})
                )

        with self.assertRaisesRegex(ArticleEngineError, "validated claims"):
            ArticleEngine(OmitsClaims()).create_article(request(), report())


class PublicationPackageTests(unittest.TestCase):
    def test_package_contains_every_capability009_component(self):
        evidence = report()
        draft = ArticleEngine().create_article(request(), evidence)
        package = PublicationPackageBuilder().build(draft, evidence)
        self.assertIs(
            package.readiness, PackageReadiness.READY_FOR_HERO_VISUAL
        )
        self.assertTrue(all(package.required_text_components()))
        self.assertIs(package.editorial_confidence, EditorialConfidence.READY)

    def test_moderate_risk_requires_review_before_hero_visual(self):
        evidence = report(supports=1, material=False)
        draft = ArticleEngine().create_article(
            request(sources=("source-1",)), evidence
        )
        package = PublicationPackageBuilder().build(draft, evidence)
        self.assertIs(package.editorial_risk, EditorialRisk.MODERATE)
        self.assertIs(
            package.readiness,
            PackageReadiness.REVIEW_BEFORE_HERO_VISUAL,
        )
        self.assertTrue(package.review_findings)

    def test_later_capability_outputs_are_explicitly_deferred(self):
        evidence = report()
        draft = ArticleEngine().create_article(request(), evidence)
        package = PublicationPackageBuilder().build(draft, evidence)
        self.assertIsNone(package.rendered_hero_visual)
        self.assertIsNone(package.portable_editorial_project)
        self.assertFalse(package.version_one_complete)
        self.assertEqual(
            package.deferred_components,
            (
                "Rendered Hero Visual - Capability 010",
                "Portable Editorial Project - Capability 011",
            ),
        )

    def test_blocked_report_cannot_assemble_package(self):
        evidence = report(supports=0)
        draft = ArticleDraft(
            intent_identifier="intent-1",
            headline="Headline",
            hook="Hook",
            insights=("Insight",),
            practical_takeaway="Takeaway",
            cta="Question? Conversation invitation.",
            source_attributions=(),
            hashtags=("#Tag",),
            linkedin_description="Description",
            hero_visual_prompt="Prompt",
            article_markdown="# Article",
            used_claim_identifiers=(),
        )
        with self.assertRaises(PublicationBlockedError):
            PublicationPackageBuilder().build(draft, evidence)


if __name__ == "__main__":
    unittest.main()
