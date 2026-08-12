"""Acceptance tests for V11-03 Editorial Discovery and Editorial Plan Gates."""

from __future__ import annotations

import unittest

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
    InvalidAuthorJourneyTransition,
    WorkflowMode,
)


INFERENCE = EditorialInference(
    intent="Explain why deliberate review protects trust",
    audience="Editorial leaders",
    platform="LinkedIn",
    desired_outcome="Help leaders adopt an explicit review gate",
)
SOURCE = EditorialSourceMaterial(
    EditorialSourceKind.NOTES,
    "Review catches unsupported assumptions before publication.",
)
BRANDING = BrandingMaterial(BrandingMaterialKind.LOGO, "brand/logo.svg")


def plan(headline: str = "Review Before You Publish") -> EditorialPlan:
    return EditorialPlan(
        headline=headline,
        hook="Speed without review can quietly erode trust.",
        key_insights=(
            "A visible review gate makes assumptions easier to challenge.",
            "Approval preserves Author control before generation.",
        ),
        practical_takeaway="Add one explicit approval before drafting.",
        call_to_action="Where would a review gate protect your work?",
    )


def journey_at_discovery(
    mode: WorkflowMode = WorkflowMode.GUIDED,
) -> AuthorJourney:
    journey = AuthorJourney()
    journey.begin()
    journey.choose_entry_path(EntryPath.START_NEW_PUBLICATION)
    journey.skip_configuration()
    journey.select_workflow(mode)
    journey.submit_editorial_source(SOURCE, inference=INFERENCE)
    journey.submit_branding(BrandingMode.BUSINESS, (BRANDING,))
    return journey


class EditorialDiscoveryTests(unittest.TestCase):
    def test_discovery_presents_complete_reviewable_understanding(self) -> None:
        journey = journey_at_discovery()
        understanding = journey.review_discovery()
        self.assertEqual(understanding.intent, INFERENCE.intent)
        self.assertEqual(understanding.audience, INFERENCE.audience)
        self.assertEqual(understanding.platform, INFERENCE.platform)
        self.assertEqual(understanding.desired_outcome, INFERENCE.desired_outcome)
        self.assertIs(understanding.branding, journey.branding_selection)

    def test_discovery_approval_enters_plan_without_proposing_one(self) -> None:
        journey = journey_at_discovery()
        journey.approve_discovery()
        self.assertEqual(journey.state, AuthorJourneyState.EDITORIAL_PLAN)
        self.assertIsNone(journey.editorial_plan)
        self.assertIsNone(journey.approved_editorial_plan)

    def test_source_refinement_preserves_branding_byte_identically(self) -> None:
        journey = journey_at_discovery()
        branding = journey.branding_selection
        journey.refine_editorial_source()
        self.assertEqual(journey.state, AuthorJourneyState.EDITORIAL_SOURCE)
        self.assertIs(journey.branding_selection, branding)
        self.assertEqual(journey.branding_selection, branding)

    def test_branding_refinement_preserves_source_and_inference_exactly(self) -> None:
        journey = journey_at_discovery()
        source = journey.editorial_source
        inference = journey.editorial_inference
        journey.refine_branding()
        self.assertEqual(journey.state, AuthorJourneyState.BRANDING)
        self.assertIs(journey.editorial_source, source)
        self.assertIs(journey.editorial_inference, inference)

    def test_refined_source_returns_through_branding_to_discovery(self) -> None:
        journey = journey_at_discovery()
        branding = journey.branding_selection
        journey.refine_editorial_source()
        revised_source = EditorialSourceMaterial(
            EditorialSourceKind.ARTICLE, "A revised source article"
        )
        revised_inference = EditorialInference(
            intent="Clarify the evidence",
            audience="Editors",
            platform="LinkedIn",
            desired_outcome="Improve review practice",
        )
        journey.submit_editorial_source(revised_source, inference=revised_inference)
        self.assertIs(journey.branding_selection, branding)
        journey.submit_branding(branding.mode, branding.materials)
        self.assertEqual(journey.state, AuthorJourneyState.EDITORIAL_DISCOVERY)
        self.assertIs(journey.editorial_source, revised_source)

    def test_discovery_choices_fail_closed_outside_discovery(self) -> None:
        journey = AuthorJourney()
        for action in (
            journey.review_discovery,
            journey.approve_discovery,
            journey.refine_editorial_source,
            journey.refine_branding,
        ):
            with self.subTest(action=action.__name__):
                with self.assertRaises(InvalidAuthorJourneyTransition):
                    action()

    def test_both_workflow_modes_use_the_same_discovery_gate(self) -> None:
        states = []
        for mode in WorkflowMode:
            journey = journey_at_discovery(mode)
            journey.approve_discovery()
            states.append(journey.state)
        self.assertEqual(
            states, [AuthorJourneyState.EDITORIAL_PLAN] * len(WorkflowMode)
        )


class EditorialPlanTests(unittest.TestCase):
    def journey_at_plan(self) -> AuthorJourney:
        journey = journey_at_discovery()
        journey.approve_discovery()
        return journey

    def test_plan_requires_every_approved_component(self) -> None:
        proposal = plan()
        self.assertTrue(proposal.headline)
        self.assertTrue(proposal.hook)
        self.assertGreaterEqual(len(proposal.key_insights), 1)
        self.assertTrue(proposal.practical_takeaway)
        self.assertTrue(proposal.call_to_action)
        for field_name in (
            "headline",
            "hook",
            "practical_takeaway",
            "call_to_action",
        ):
            values = {
                "headline": proposal.headline,
                "hook": proposal.hook,
                "key_insights": proposal.key_insights,
                "practical_takeaway": proposal.practical_takeaway,
                "call_to_action": proposal.call_to_action,
            }
            values[field_name] = ""
            with self.subTest(field=field_name):
                with self.assertRaises(AuthorJourneyError):
                    EditorialPlan(**values)

    def test_plan_cannot_be_proposed_before_discovery_approval(self) -> None:
        journey = journey_at_discovery()
        with self.assertRaises(InvalidAuthorJourneyTransition):
            journey.propose_plan(plan())
        self.assertEqual(journey.state, AuthorJourneyState.EDITORIAL_DISCOVERY)
        self.assertIsNone(journey.editorial_plan)

    def test_author_can_review_and_approve_the_proposed_plan(self) -> None:
        journey = self.journey_at_plan()
        proposal = plan()
        self.assertIs(journey.propose_plan(proposal), proposal)
        self.assertIs(journey.review_plan(), proposal)
        self.assertIs(journey.approve_plan(), proposal)
        self.assertEqual(journey.state, AuthorJourneyState.GENERATION)
        self.assertIs(journey.approved_editorial_plan, proposal)

    def test_revision_remains_in_plan_and_does_not_trigger_generation(self) -> None:
        journey = self.journey_at_plan()
        journey.propose_plan(plan())
        revised = plan("Trust Needs a Review Gate")
        self.assertIs(journey.revise_plan(revised), revised)
        self.assertEqual(journey.state, AuthorJourneyState.EDITORIAL_PLAN)
        self.assertIs(journey.editorial_plan, revised)
        self.assertIsNone(journey.approved_editorial_plan)

    def test_plan_cannot_be_approved_without_a_proposal(self) -> None:
        journey = self.journey_at_plan()
        with self.assertRaises(AuthorJourneyError):
            journey.approve_plan()
        self.assertEqual(journey.state, AuthorJourneyState.EDITORIAL_PLAN)
        self.assertIsNone(journey.approved_editorial_plan)

    def test_invalid_revision_fails_closed_without_losing_current_plan(self) -> None:
        journey = self.journey_at_plan()
        original = plan()
        journey.propose_plan(original)
        with self.assertRaises(AuthorJourneyError):
            journey.revise_plan("replacement")  # type: ignore[arg-type]
        self.assertEqual(journey.state, AuthorJourneyState.EDITORIAL_PLAN)
        self.assertIs(journey.editorial_plan, original)

    def test_generation_is_only_a_routing_seam(self) -> None:
        journey = self.journey_at_plan()
        journey.propose_plan(plan())
        journey.approve_plan()
        self.assertEqual(journey.state, AuthorJourneyState.GENERATION)
        for name in (
            "generate",
            "handle_generation_failure",
            "enter_publication_studio",
            "audit",
            "complete",
        ):
            self.assertFalse(hasattr(AuthorJourney, name), name)

    def test_plan_flow_is_stateless_and_deterministic(self) -> None:
        first = self.journey_at_plan()
        second = self.journey_at_plan()
        first.propose_plan(plan())
        second.propose_plan(plan())
        self.assertEqual(first.review_plan(), second.review_plan())
        first.approve_plan()
        self.assertEqual(second.state, AuthorJourneyState.EDITORIAL_PLAN)
        self.assertIsNone(second.approved_editorial_plan)

    def test_version_one_session_remains_untouched(self) -> None:
        marker = object()
        journey = AuthorJourney(editorial_session=marker)  # type: ignore[arg-type]
        journey.begin()
        journey.choose_entry_path(EntryPath.START_NEW_PUBLICATION)
        journey.skip_configuration()
        journey.select_workflow(WorkflowMode.GUIDED)
        journey.submit_editorial_source(SOURCE, inference=INFERENCE)
        journey.submit_branding(BrandingMode.BUSINESS, (BRANDING,))
        journey.approve_discovery()
        journey.propose_plan(plan())
        journey.approve_plan()
        self.assertIs(journey.editorial_session, marker)


if __name__ == "__main__":
    unittest.main()
