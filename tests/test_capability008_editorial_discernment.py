"""Runtime tests for Capability 008."""

from __future__ import annotations

import unittest

from studio.editorial_discernment import (
    Contribution,
    ContributionKind,
    EditorialComponent,
    EditorialDiscernmentEngine,
    EditorialIntent,
    EditorialSession,
    IntentAlignment,
    StageState,
    WorkspaceState,
)


class Capability008DiscernmentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = EditorialDiscernmentEngine()

        self.intent = EditorialIntent(
            primary_topic=(
                "AI governance in financial services"
            ),
            editorial_objective=(
                "Explain why accountable AI governance "
                "is an operating discipline"
            ),
            intended_audience=(
                "banking executives and risk leaders"
            ),
            publication_goal=(
                "publish a professional LinkedIn article"
            ),
            scope_terms=(
                "governance",
                "accountability",
                "financial services",
                "banking",
                "risk",
            ),
        )

        self.session = EditorialSession(
            intent=self.intent
        )

        self.session.activate()

    def test_intent_is_defined(self) -> None:
        self.assertTrue(self.intent.is_defined())

    def test_workspace_and_stage_states_are_distinct(
        self,
    ) -> None:
        self.assertEqual(
            self.session.workspace_state,
            WorkspaceState.ACTIVE,
        )
        self.assertEqual(
            self.session.stage_states[1],
            StageState.NOT_STARTED,
        )

    def test_related_source_continues(self) -> None:
        decision = self.engine.classify(
            self.session,
            Contribution(
                text=(
                    "Banking regulators are publishing "
                    "additional AI governance guidance."
                ),
                source_identifiers=("regulator.example",),
            ),
        )

        self.assertIn(
            decision.alignment,
            {
                IntentAlignment.ALIGNED,
                IntentAlignment.RELATED,
            },
        )
        self.assertTrue(
            decision.may_continue_current_session
        )
        self.assertFalse(
            decision.recommend_new_session
        )

    def test_unrelated_topic_recommends_new_session(
        self,
    ) -> None:
        decision = self.engine.classify(
            self.session,
            Contribution(
                text=(
                    "Leadership lessons from international "
                    "cricket captains"
                )
            ),
        )

        self.assertEqual(
            decision.alignment,
            IntentAlignment.SEPARATE_INTENT,
        )
        self.assertTrue(
            decision.recommend_new_session
        )
        self.assertFalse(
            decision.may_continue_current_session
        )
        self.assertIn(
            "different publication objective",
            decision.author_message,
        )

    def test_no_silent_scope_expansion(self) -> None:
        decision = self.engine.classify(
            self.session,
            Contribution(
                text=(
                    "Compare banking AI governance with "
                    "healthcare, retail, manufacturing, and "
                    "public-sector governance."
                )
            ),
        )

        self.assertIn(
            decision.alignment,
            {
                IntentAlignment.DIVERGING,
                IntentAlignment.SEPARATE_INTENT,
            },
        )

        self.assertTrue(
            decision.recommend_new_session
            or decision.requires_clarification
        )

    def test_targeted_cta_revision(self) -> None:
        self.session.approve(
            EditorialComponent.HEADLINE
        )
        self.session.approve(
            EditorialComponent.HOOK
        )

        decision = self.engine.classify(
            self.session,
            Contribution(
                text="I do not like this CTA.",
                target_component=EditorialComponent.CTA,
                declared_kind=(
                    ContributionKind.REVISE_COMPONENT
                ),
            ),
        )

        self.assertEqual(
            decision.affected_components,
            (EditorialComponent.CTA,),
        )
        self.assertIn(
            EditorialComponent.HEADLINE,
            decision.protected_components,
        )
        self.assertIn(
            EditorialComponent.HOOK,
            decision.protected_components,
        )

    def test_revision_applies_to_hero_visual(self) -> None:
        decision = self.engine.classify(
            self.session,
            Contribution(
                text="Revise the Hero Visual.",
                target_component=(
                    EditorialComponent.HERO_VISUAL
                ),
                declared_kind=(
                    ContributionKind.REVISE_COMPONENT
                ),
            ),
        )

        self.assertEqual(
            decision.affected_components,
            (EditorialComponent.HERO_VISUAL,),
        )

    def test_ambiguous_rejection_asks_one_question(
        self,
    ) -> None:
        decision = self.engine.classify(
            self.session,
            Contribution(text="I do not like this."),
        )

        self.assertTrue(
            decision.requires_clarification
        )
        self.assertIsNotNone(
            decision.clarification_question
        )
        self.assertEqual(
            decision.author_message.count("?"),
            1,
        )

    def test_pause_preserves_state(self) -> None:
        self.session.approve(
            EditorialComponent.HEADLINE
        )

        decision = self.engine.classify(
            self.session,
            Contribution(text="Pause this for now."),
        )

        self.engine.apply_decision(
            self.session,
            decision,
        )

        self.assertEqual(
            self.session.workspace_state,
            WorkspaceState.PAUSED,
        )
        self.assertIn(
            EditorialComponent.HEADLINE,
            self.session.approved_components,
        )

    def test_resume_after_pause(self) -> None:
        self.session.pause()

        decision = self.engine.classify(
            self.session,
            Contribution(text="Resume."),
        )

        self.engine.apply_decision(
            self.session,
            decision,
        )

        self.assertEqual(
            self.session.workspace_state,
            WorkspaceState.ACTIVE,
        )

    def test_abort_preserves_approvals(self) -> None:
        self.session.approve(
            EditorialComponent.HEADLINE
        )

        decision = self.engine.classify(
            self.session,
            Contribution(text="Abort this session."),
        )

        self.engine.apply_decision(
            self.session,
            decision,
        )

        self.assertEqual(
            self.session.workspace_state,
            WorkspaceState.ABORTED,
        )
        self.assertIn(
            EditorialComponent.HEADLINE,
            self.session.approved_components,
        )
        self.assertTrue(
            self.session.preserved_events
        )

    def test_aborted_session_can_resume(self) -> None:
        self.session.abort()
        self.session.resume()

        self.assertEqual(
            self.session.workspace_state,
            WorkspaceState.ACTIVE,
        )

    def test_cancel_is_distinct_from_abort(self) -> None:
        self.session.cancel()

        self.assertEqual(
            self.session.workspace_state,
            WorkspaceState.CANCELLED,
        )
        self.assertNotEqual(
            self.session.workspace_state,
            WorkspaceState.ABORTED,
        )

    def test_complete_requires_all_stages(self) -> None:
        with self.assertRaises(ValueError):
            self.session.complete()

    def test_complete_after_all_stages(self) -> None:
        for number in range(1, 6):
            self.session.mark_stage(
                number,
                StageState.COMPLETE,
            )

        self.session.complete()

        self.assertEqual(
            self.session.workspace_state,
            WorkspaceState.COMPLETED,
        )

    def test_completed_session_can_archive(self) -> None:
        for number in range(1, 6):
            self.session.mark_stage(
                number,
                StageState.COMPLETE,
            )

        self.session.complete()
        self.session.archive()

        self.assertEqual(
            self.session.workspace_state,
            WorkspaceState.ARCHIVED,
        )

    def test_empty_contribution_requires_clarification(
        self,
    ) -> None:
        decision = self.engine.classify(
            self.session,
            Contribution(text=""),
        )

        self.assertEqual(
            decision.contribution_kind,
            ContributionKind.CLARIFICATION_REQUIRED,
        )

    def test_declared_new_publication_is_preserved(
        self,
    ) -> None:
        decision = self.engine.classify(
            self.session,
            Contribution(
                text="Start a piece about cricket.",
                declared_kind=(
                    ContributionKind.NEW_PUBLICATION
                ),
            ),
        )

        self.assertTrue(
            decision.recommend_new_session
        )
        self.assertTrue(
            decision.preserve_existing_work
        )


if __name__ == "__main__":
    unittest.main()
