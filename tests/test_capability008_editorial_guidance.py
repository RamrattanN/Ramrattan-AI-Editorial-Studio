"""Author-facing Editorial Guidance tests."""

from __future__ import annotations

import unittest

from studio.editorial_discernment import (
    Contribution,
    EditorialDiscernmentEngine,
    EditorialIntent,
    EditorialSession,
    StageState,
)
from studio.editorial_guidance import (
    guidance_view,
    render_progress,
)


class Capability008GuidanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.session = EditorialSession(
            intent=EditorialIntent(
                primary_topic="AI governance",
                editorial_objective=(
                    "Explain accountable governance"
                ),
                intended_audience="executives",
                publication_goal="LinkedIn article",
                scope_terms=("governance", "accountable"),
            )
        )

        self.session.activate()

    def test_progress_displays_session_state(
        self,
    ) -> None:
        lines = render_progress(self.session)

        self.assertEqual(
            lines[0],
            "Editorial Workspace - Active",
        )

    def test_progress_uses_all_five_stages(
        self,
    ) -> None:
        lines = render_progress(self.session)

        self.assertEqual(len(lines), 6)

    def test_progress_distinguishes_in_progress(
        self,
    ) -> None:
        self.session.mark_stage(
            1,
            StageState.COMPLETE,
        )
        self.session.mark_stage(
            2,
            StageState.IN_PROGRESS,
        )

        lines = render_progress(self.session)

        self.assertIn(
            "✓ Understanding your input",
            lines,
        )
        self.assertIn(
            "◐ Assessing your sources",
            lines,
        )

    def test_separate_intent_guidance_is_conversational(
        self,
    ) -> None:
        engine = EditorialDiscernmentEngine()

        decision = engine.classify(
            self.session,
            Contribution(
                text="Cricket captain leadership lessons"
            ),
        )

        view = guidance_view(
            self.session,
            decision,
        )

        self.assertIn(
            "Reader trust",
            view.guidance,
        )
        self.assertNotIn(
            "ERROR",
            view.guidance,
        )


if __name__ == "__main__":
    unittest.main()
