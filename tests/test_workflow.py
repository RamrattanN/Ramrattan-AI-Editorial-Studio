"""Tests for the editorial workflow system."""

from __future__ import annotations

import unittest

from studio.workflow import (
    ContentType,
    EditorialState,
    EditorialWorkflow,
    HeroCopyDirection,
    InvalidTransitionError,
    VisualStyle,
    WorkflowStage,
)


class EditorialWorkflowTests(unittest.TestCase):
    def create_source_workflow(self) -> EditorialWorkflow:
        workflow = EditorialWorkflow()

        workflow.analyze_source(
            source_url="https://example.com/article",
            source_title="Example Article",
            strongest_insight=(
                "Remote work changes building economics."
            ),
            supporting_statistic="$200 per month",
            provocative_claim=(
                "Utility models were not built for remote work."
            ),
        )

        return workflow

    def create_graphic_approved_workflow(
        self,
    ) -> EditorialWorkflow:
        workflow = self.create_source_workflow()

        workflow.choose_content_type(
            ContentType.ARTICLE
        )
        workflow.choose_visual_style(
            VisualStyle.EXECUTIVE_EDITORIAL
        )
        workflow.choose_hero_copy(
            direction=HeroCopyDirection.RECOMMENDED,
            headline=(
                "Remote Work Is Reshaping Rental Economics"
            ),
            supporting_text=(
                "Higher daytime occupancy is changing "
                "utility costs."
            ),
        )
        workflow.record_graphic(
            "generated-image-reference"
        )
        workflow.approve_graphic()

        return workflow

    def test_initial_stage_is_start(self) -> None:
        workflow = EditorialWorkflow()

        self.assertEqual(
            workflow.stage,
            WorkflowStage.START,
        )

    def test_complete_happy_path(self) -> None:
        workflow = self.create_graphic_approved_workflow()

        workflow.record_written_content(
            article_headline=(
                "Remote Work Is Reshaping Rental Economics"
            ),
            hook="Remote work changed more than commuting.",
            insight_1=(
                "Daytime occupancy increases utility usage."
            ),
            practical_takeaway=(
                "Use transparent utility allocation models."
            ),
            source_mention="@Example",
            cta="Surcharge or smarter metering?",
            hashtags=[
                "#RealEstate",
                "#RemoteWork",
                "#Multifamily",
                "#PropertyManagement",
                "#Utilities",
                "#AssetManagement",
            ],
            linkedin_description=(
                "An analysis of remote-work utility costs."
            ),
        )

        self.assertEqual(
            workflow.stage,
            WorkflowStage.FINAL_REVIEW,
        )

        workflow.approve_final_content()

        self.assertEqual(
            workflow.stage,
            WorkflowStage.COMPLETE,
        )
        self.assertTrue(
            workflow.state.final_content_approved
        )

    def test_cannot_choose_style_before_content_type(
        self,
    ) -> None:
        workflow = self.create_source_workflow()

        with self.assertRaises(
            InvalidTransitionError
        ):
            workflow.choose_visual_style(
                VisualStyle.DATA_STORY
            )

    def test_hero_copy_word_limits(self) -> None:
        workflow = self.create_source_workflow()

        workflow.choose_content_type(
            ContentType.ARTICLE
        )
        workflow.choose_visual_style(
            VisualStyle.EXECUTIVE_EDITORIAL
        )

        with self.assertRaises(ValueError):
            workflow.choose_hero_copy(
                direction=(
                    HeroCopyDirection.RECOMMENDED
                ),
                headline="Too Short",
                supporting_text="Supporting text.",
            )

    def test_changing_visual_style_resets_downstream(
        self,
    ) -> None:
        workflow = self.create_graphic_approved_workflow()

        workflow.choose_visual_style(
            VisualStyle.DATA_STORY
        )

        self.assertEqual(
            workflow.stage,
            WorkflowStage.VISUAL_STYLE_SELECTED,
        )
        self.assertIsNone(
            workflow.state.hero_headline
        )
        self.assertIsNone(
            workflow.state.hero_image_reference
        )
        self.assertFalse(
            workflow.state.hero_image_approved
        )

    def test_state_json_round_trip(self) -> None:
        state = EditorialState(
            source_url="https://example.com",
            content_type=ContentType.ARTICLE,
            visual_style=VisualStyle.DATA_STORY,
            hashtags=["#One", "#Two"],
        )

        restored = EditorialState.from_json(
            state.to_json()
        )

        self.assertEqual(
            restored.source_url,
            state.source_url,
        )
        self.assertEqual(
            restored.content_type,
            ContentType.ARTICLE,
        )
        self.assertEqual(
            restored.visual_style,
            VisualStyle.DATA_STORY,
        )
        self.assertEqual(
            restored.hashtags,
            ["#One", "#Two"],
        )

    def test_restart_clears_session(self) -> None:
        workflow = self.create_graphic_approved_workflow()

        workflow.restart()

        self.assertEqual(
            workflow.stage,
            WorkflowStage.START,
        )
        self.assertIsNone(
            workflow.state.source_url
        )


if __name__ == "__main__":
    unittest.main()
