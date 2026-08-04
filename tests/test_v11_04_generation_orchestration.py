"""Acceptance tests for V11-04 Generation orchestration."""

from __future__ import annotations

from datetime import date
import unittest

from studio.article_engine import ArticleRequest, SourceAttribution
from studio.author_journey import (
    AuthorJourney,
    AuthorJourneyError,
    AuthorJourneyState,
    BrandingMaterial,
    BrandingMaterialKind,
    BrandingMode,
    EditorialInference,
    EditorialPlan,
    EditorialSourceKind,
    EditorialSourceMaterial,
    EntryPath,
    GenerationRequest,
    GenerationStatus,
    InvalidAuthorJourneyTransition,
    WorkflowMode,
)
from studio.evidence_validation import (
    Claim,
    ClaimClassification,
    EditorialRisk,
    EvidencePosition,
    EvidenceRecord,
)
from studio.hero_visual import HeroVisualRequest
from studio.publication_package import HeroVisualPackageState


CURRENT_ON = date(2026, 8, 4)
INFERENCE = EditorialInference(
    intent="Explain why evidence-led review protects trust.",
    audience="Editorial leaders",
    platform="LinkedIn",
    desired_outcome="Help leaders adopt an explicit review gate.",
)
PLAN = EditorialPlan(
    headline="Evidence-Led Review Protects Trust",
    hook="Disciplined review protects both speed and trust.",
    key_insights=(
        "Evidence exposes assumptions before they become polished claims.",
        "Approval preserves Author control before generation.",
    ),
    practical_takeaway="Require evidence gates for material claims.",
    call_to_action="Where would stronger review improve your decisions?",
)
CLAIM = Claim(
    identifier="claim-1",
    text="Structured review reduced avoidable rework.",
    classification=ClaimClassification.SOURCE_ASSERTION,
)


def evidence(supports: int = 2) -> tuple[EvidenceRecord, ...]:
    return tuple(
        EvidenceRecord(
            source_identifier=f"source-{number}",
            claim_identifier=CLAIM.identifier,
            position=EvidencePosition.SUPPORTS,
            independent_group=f"group-{number}",
            published_on=date(2026, 7, 1),
        )
        for number in range(1, supports + 1)
    )


def generation_request(
    *,
    supports: int = 2,
    provider: str = "deterministic",
    plan: EditorialPlan = PLAN,
) -> GenerationRequest:
    sources = tuple(
        SourceAttribution(
            item.source_identifier,
            f"{item.source_identifier} — reviewed evidence",
        )
        for item in evidence(supports)
    ) or (SourceAttribution("unverified", "Unverified source material"),)
    article = ArticleRequest(
        intent_identifier="v11-04-intent",
        editorial_intent=INFERENCE.intent,
        thesis=plan.headline,
        author_perspective=plan.hook,
        audience=INFERENCE.audience,
        insights=plan.key_insights,
        practical_takeaway=plan.practical_takeaway,
        cta_question=plan.call_to_action,
        hero_visual_prompt="A restrained editorial evidence checkpoint.",
        hashtags=("#EditorialIntegrity", "#Leadership"),
        linkedin_description="A practical case for evidence-led review.",
        source_attributions=sources,
    )
    return GenerationRequest(
        article=article,
        claims=(CLAIM,),
        evidence=evidence(supports),
        hero_visual=HeroVisualRequest(
            prompt=article.hero_visual_prompt,
            visual_intent="Show disciplined review protecting trust.",
            provider=provider,
            brand_context="Approved business branding",
        ),
        current_on=CURRENT_ON,
    )


def journey_at_generation() -> AuthorJourney:
    journey = AuthorJourney()
    journey.begin()
    journey.choose_entry_path(EntryPath.START_NEW_PUBLICATION)
    journey.skip_configuration()
    journey.select_workflow(WorkflowMode.GUIDED)
    journey.submit_editorial_source(
        EditorialSourceMaterial(
            EditorialSourceKind.NOTES,
            "Evidence-led review protects editorial trust.",
        ),
        inference=INFERENCE,
    )
    journey.submit_branding(
        BrandingMode.BUSINESS,
        (BrandingMaterial(BrandingMaterialKind.LOGO, "brand/logo.svg"),),
    )
    journey.approve_discovery()
    journey.propose_plan(PLAN)
    journey.approve_plan()
    return journey


class GenerationOrchestrationTests(unittest.TestCase):
    def test_approved_plan_reaches_generation(self) -> None:
        journey = journey_at_generation()
        self.assertEqual(journey.state, AuthorJourneyState.GENERATION)
        self.assertIs(journey.approved_editorial_plan, PLAN)

    def test_success_runs_complete_chain_and_enters_publication_studio(self) -> None:
        journey = journey_at_generation()
        outcome = journey.run_generation(generation_request())
        self.assertTrue(outcome.complete)
        self.assertEqual(outcome.status, GenerationStatus.COMPLETE)
        self.assertEqual(journey.state, AuthorJourneyState.PUBLICATION_STUDIO)
        self.assertIsNotNone(outcome.publication_package)
        self.assertEqual(
            outcome.publication_package.hero_visual_state,
            HeroVisualPackageState.READY,
        )

    def test_success_preserves_evidence_and_risk(self) -> None:
        outcome = journey_at_generation().run_generation(generation_request())
        self.assertIsNotNone(outcome.evidence_report)
        self.assertEqual(outcome.evidence_report.editorial_risk, EditorialRisk.LOW)
        self.assertEqual(
            outcome.publication_package.editorial_risk,
            outcome.evidence_report.editorial_risk,
        )
        self.assertEqual(
            outcome.publication_package.source_and_attribution,
            ("source-1 — reviewed evidence", "source-2 — reviewed evidence"),
        )

    def test_generation_rejects_unapproved_plan_data(self) -> None:
        journey = journey_at_generation()
        changed = EditorialPlan(
            headline="Different headline",
            hook=PLAN.hook,
            key_insights=PLAN.key_insights,
            practical_takeaway=PLAN.practical_takeaway,
            call_to_action=PLAN.call_to_action,
        )
        with self.assertRaisesRegex(AuthorJourneyError, "headline"):
            journey.run_generation(generation_request(plan=changed))
        self.assertEqual(journey.state, AuthorJourneyState.GENERATION)

    def test_generation_rejects_missing_approved_branding(self) -> None:
        journey = journey_at_generation()
        request = generation_request()
        changed_visual = HeroVisualRequest(
            prompt=request.hero_visual.prompt,
            visual_intent=request.hero_visual.visual_intent,
        )
        with self.assertRaisesRegex(AuthorJourneyError, "Branding"):
            journey.run_generation(
                GenerationRequest(
                    request.article,
                    request.claims,
                    request.evidence,
                    changed_visual,
                    request.current_on,
                )
            )

    def test_high_risk_generation_is_blocked_without_a_package(self) -> None:
        journey = journey_at_generation()
        outcome = journey.run_generation(generation_request(supports=0))
        self.assertEqual(outcome.status, GenerationStatus.BLOCKED)
        self.assertIn("Editorial Risk", outcome.explanation)
        self.assertIsNone(outcome.publication_package)
        self.assertEqual(journey.state, AuthorJourneyState.EDITORIAL_PLAN)

    def test_blocked_attempt_does_not_consume_generate_once(self) -> None:
        journey = journey_at_generation()
        journey.run_generation(generation_request(supports=0))
        journey.approve_plan()
        outcome = journey.run_generation(generation_request())
        self.assertTrue(outcome.complete)

    def test_hero_failure_is_distinct_from_risk_block(self) -> None:
        journey = journey_at_generation()
        outcome = journey.run_generation(generation_request(provider="missing"))
        self.assertEqual(outcome.status, GenerationStatus.FAILED)
        self.assertIn("independently of Editorial Risk", outcome.explanation)
        self.assertIsNone(outcome.publication_package)
        self.assertEqual(journey.state, AuthorJourneyState.EDITORIAL_PLAN)

    def test_failed_attempt_does_not_consume_generate_once(self) -> None:
        journey = journey_at_generation()
        journey.run_generation(generation_request(provider="missing"))
        journey.approve_plan()
        self.assertTrue(journey.run_generation(generation_request()).complete)

    def test_evidence_validation_failure_routes_safely(self) -> None:
        journey = journey_at_generation()
        request = generation_request()
        malformed = GenerationRequest(
            request.article,
            (),
            request.evidence,
            request.hero_visual,
            request.current_on,
        )
        outcome = journey.run_generation(malformed)
        self.assertEqual(outcome.status, GenerationStatus.FAILED)
        self.assertIsNone(outcome.evidence_report)
        self.assertEqual(journey.state, AuthorJourneyState.EDITORIAL_PLAN)

    def test_generate_once_rejects_a_second_entry(self) -> None:
        journey = journey_at_generation()
        journey.run_generation(generation_request())
        with self.assertRaises(InvalidAuthorJourneyTransition):
            journey.run_generation(generation_request())

    def test_generate_once_rejects_even_if_state_is_tampered(self) -> None:
        journey = journey_at_generation()
        journey.run_generation(generation_request())
        journey.state = AuthorJourneyState.GENERATION
        with self.assertRaisesRegex(InvalidAuthorJourneyTransition, "already completed"):
            journey.run_generation(generation_request())

    def test_publication_studio_cannot_reenter_generation(self) -> None:
        journey = journey_at_generation()
        journey.run_generation(generation_request())
        with self.assertRaises(InvalidAuthorJourneyTransition):
            journey.approve_plan()

    def test_invalid_generation_state_fails_closed(self) -> None:
        journey = AuthorJourney()
        with self.assertRaises(InvalidAuthorJourneyTransition):
            journey.run_generation(generation_request())

    def test_outcome_is_session_local(self) -> None:
        first = journey_at_generation()
        second = journey_at_generation()
        first.run_generation(generation_request())
        self.assertIsNone(second.generation_outcome)
        self.assertEqual(second.state, AuthorJourneyState.GENERATION)

    def test_version_one_session_remains_untouched(self) -> None:
        marker = object()
        journey = journey_at_generation()
        journey.editorial_session = marker  # type: ignore[assignment]
        journey.run_generation(generation_request())
        self.assertIs(journey.editorial_session, marker)


if __name__ == "__main__":
    unittest.main()
