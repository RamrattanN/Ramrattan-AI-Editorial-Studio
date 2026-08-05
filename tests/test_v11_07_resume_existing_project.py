"""Acceptance tests for V11-07 Resume Existing Project integration."""

from __future__ import annotations

from dataclasses import replace
from datetime import date
import unittest

from studio.author_journey import (
    AuthorJourney,
    AuthorJourneyState,
    EntryPath,
    InvalidAuthorJourneyTransition,
)
from studio.editorial_discernment import (
    EditorialIntent,
    EditorialSession,
    WorkspaceState,
)
from studio.evidence_validation import EditorialConfidence, EditorialRisk
from studio.hero_visual import HeroVisualRequest, HeroVisualSystem
from studio.portable_editorial_project import (
    ProjectState,
    from_publication_package,
    serialize_project,
)
from studio.publication_package import (
    PackageReadiness,
    PublicationPackage,
    PublicationPackageBuilder,
)
from studio.publication_studio import CopyGateState, ResumedHeroVisualReference


CURRENT_ON = date(2026, 8, 5)
ARTICLE = (
    "# Trust Before Convenience\n\n"
    "Trust must be earned.\n\n"
    "## Insight 1\n\n"
    "Verification protects the Author.\n\n"
    "## Continue the Conversation\n\n"
    "What will you verify next?\n"
)


def package() -> PublicationPackage:
    pending = PublicationPackage(
        article_markdown=ARTICLE,
        hero_visual_prompt="A restrained editorial compass protecting evidence.",
        headline="Trust Before Convenience",
        hook="Trust must be earned.",
        insights=("Verification protects the Author.",),
        practical_takeaway="Review evidence before publication.",
        cta="What will you verify next?",
        source_and_attribution=("Internal editorial standard.",),
        hashtags=("#EditorialIntegrity",),
        linkedin_description="A concise trust-first editorial note.",
        editorial_confidence=EditorialConfidence.READY,
        editorial_risk=EditorialRisk.LOW,
        readiness=PackageReadiness.READY_FOR_HERO_VISUAL,
        review_findings=(),
    )
    visual = HeroVisualSystem().generate(
        HeroVisualRequest(
            prompt=pending.hero_visual_prompt,
            visual_intent="Protect editorial trust.",
        )
    )
    return PublicationPackageBuilder().attach_hero_visual(pending, visual)


def project_markdown(*, saved_on: date = CURRENT_ON, blocked: bool = False) -> str:
    project = from_publication_package(
        package(),
        saved_on=saved_on,
        document_version=f"{saved_on:%Y.%m.%d}v01",
    )
    if blocked:
        project = replace(project, integrity_blockers=("Unresolved claim.",))
    return serialize_project(project)


def paused_session() -> EditorialSession:
    return EditorialSession(
        intent=EditorialIntent(
            primary_topic="Trust Before Convenience",
            editorial_objective="Explain evidence-led review.",
            intended_audience="Professional Authors",
            publication_goal="Publish a professional article.",
        ),
        workspace_state=WorkspaceState.PAUSED,
    )


def journey_at_resume(session: EditorialSession | None = None) -> AuthorJourney:
    journey = AuthorJourney(session if session is not None else paused_session())
    journey.begin()
    journey.choose_entry_path(EntryPath.RESUME_EXISTING_PROJECT)
    return journey


class ResumeExistingProjectTests(unittest.TestCase):
    def test_entry_path_routes_resume_to_validation(self) -> None:
        journey = journey_at_resume()
        self.assertEqual(journey.state, AuthorJourneyState.RESUME_VALIDATION)

    def test_valid_project_resumes_with_existing_version_one_semantics(self) -> None:
        session = paused_session()
        journey = journey_at_resume(session)
        outcome = journey.resume_existing_project(
            project_markdown(), current_on=CURRENT_ON
        )
        self.assertTrue(outcome.succeeded)
        self.assertEqual(outcome.state, ProjectState.READY)
        self.assertEqual(session.workspace_state, WorkspaceState.ACTIVE)
        self.assertIn("Temporal Integrity", session.preserved_events[-1])

    def test_valid_project_enters_publication_studio_directly(self) -> None:
        journey = journey_at_resume()
        outcome = journey.resume_existing_project(
            project_markdown(), current_on=CURRENT_ON
        )
        self.assertTrue(outcome.succeeded)
        self.assertEqual(journey.state, AuthorJourneyState.PUBLICATION_STUDIO)
        self.assertIs(journey.publication_studio.resumed_project, outcome.result.project)
        self.assertIsNone(journey.publication_studio.generated_package)

    def test_approved_article_content_is_restored_exactly(self) -> None:
        journey = journey_at_resume()
        journey.resume_existing_project(project_markdown(), current_on=CURRENT_ON)
        content = journey.publication_studio.editor.current_content
        self.assertEqual(content.headline, "Trust Before Convenience")
        self.assertEqual(content.hook, "Trust must be earned.")
        self.assertEqual(content.article, ARTICLE)
        self.assertEqual(content.cta, "What will you verify next?")

    def test_hero_visual_reference_is_restored_without_regeneration(self) -> None:
        journey = journey_at_resume()
        journey.resume_existing_project(project_markdown(), current_on=CURRENT_ON)
        visual = journey.publication_studio.hero_visual.visual
        self.assertIsInstance(visual, ResumedHeroVisualReference)
        self.assertTrue(visual.ready)
        self.assertIsNotNone(visual.artifact_sha256)
        self.assertFalse(hasattr(visual, "artifact"))

    def test_valid_pending_hero_visual_reference_is_preserved(self) -> None:
        project = from_publication_package(
            package(),
            saved_on=CURRENT_ON,
            document_version="2026.08.05v01",
        )
        project = replace(
            project,
            hero_visual_status="pending",
            hero_visual_sha256=None,
        )
        journey = journey_at_resume()
        outcome = journey.resume_existing_project(
            serialize_project(project), current_on=CURRENT_ON
        )
        self.assertTrue(outcome.succeeded)
        visual = journey.publication_studio.hero_visual.visual
        self.assertIsInstance(visual, ResumedHeroVisualReference)
        self.assertFalse(visual.ready)
        self.assertIsNone(visual.artifact_sha256)

    def test_resume_copy_gate_starts_unmatched(self) -> None:
        journey = journey_at_resume()
        journey.resume_existing_project(project_markdown(), current_on=CURRENT_ON)
        self.assertEqual(
            journey.publication_studio.copy_gate_state,
            CopyGateState.UNMATCHED,
        )
        self.assertFalse(journey.publication_studio.presentation().copy_action_enabled)

    def test_stale_project_preserves_temporal_integrity_result(self) -> None:
        journey = journey_at_resume()
        outcome = journey.resume_existing_project(
            project_markdown(saved_on=date(2026, 8, 2)),
            current_on=CURRENT_ON,
        )
        self.assertTrue(outcome.succeeded)
        self.assertEqual(outcome.state, ProjectState.STALE)
        self.assertTrue(outcome.result.temporal_integrity_review_required)
        self.assertIn("is stale", outcome.result.findings[0])
        self.assertIn("Temporal Integrity", journey.publication_studio.editorial_review.session_summary)

    def test_corrupted_project_fails_closed_and_returns_to_entry_path(self) -> None:
        journey = journey_at_resume()
        outcome = journey.resume_existing_project(
            "# corrupted project", current_on=CURRENT_ON
        )
        self.assertFalse(outcome.succeeded)
        self.assertEqual(outcome.state, ProjectState.MALFORMED)
        self.assertIn("cannot be resumed", outcome.explanation)
        self.assertEqual(journey.state, AuthorJourneyState.ENTRY_PATH)
        self.assertIsNone(journey.publication_studio)

    def test_unsupported_project_fails_closed(self) -> None:
        journey = journey_at_resume()
        changed = project_markdown().replace(
            '"schema_version": 1', '"schema_version": 2'
        )
        outcome = journey.resume_existing_project(changed, current_on=CURRENT_ON)
        self.assertFalse(outcome.succeeded)
        self.assertEqual(outcome.state, ProjectState.UNSUPPORTED)
        self.assertEqual(journey.state, AuthorJourneyState.ENTRY_PATH)

    def test_blocked_project_does_not_resume_session(self) -> None:
        session = paused_session()
        journey = journey_at_resume(session)
        outcome = journey.resume_existing_project(
            project_markdown(blocked=True), current_on=CURRENT_ON
        )
        self.assertFalse(outcome.succeeded)
        self.assertEqual(outcome.state, ProjectState.BLOCKED)
        self.assertEqual(session.workspace_state, WorkspaceState.PAUSED)
        self.assertEqual(journey.state, AuthorJourneyState.ENTRY_PATH)

    def test_missing_editorial_session_fails_closed(self) -> None:
        journey = AuthorJourney()
        journey.begin()
        journey.choose_entry_path(EntryPath.RESUME_EXISTING_PROJECT)
        outcome = journey.resume_existing_project(
            project_markdown(), current_on=CURRENT_ON
        )
        self.assertFalse(outcome.succeeded)
        self.assertIn("Editorial Session", outcome.explanation)
        self.assertEqual(journey.state, AuthorJourneyState.ENTRY_PATH)

    def test_configuration_load_is_structurally_unreachable_from_resume(self) -> None:
        journey = journey_at_resume()
        with self.assertRaises(InvalidAuthorJourneyTransition):
            journey.load_configuration(
                "Ramrattan-AI-Configuration-2026.08.05v01.json",
                '{"preferred_workflow":"express","branding_preference":"business"}',
            )
        self.assertEqual(journey.state, AuthorJourneyState.RESUME_VALIDATION)
        self.assertFalse(journey.configuration_loaded)

    def test_resume_never_applies_configuration_preferences(self) -> None:
        journey = journey_at_resume()
        journey.resume_existing_project(project_markdown(), current_on=CURRENT_ON)
        self.assertFalse(journey.configuration_loaded)
        self.assertIsNone(journey.workflow_mode)
        self.assertIsNone(journey.branding_preference)

    def test_resume_path_cannot_enter_generation(self) -> None:
        journey = journey_at_resume()
        journey.resume_existing_project(project_markdown(), current_on=CURRENT_ON)
        self.assertEqual(journey.state, AuthorJourneyState.PUBLICATION_STUDIO)
        self.assertFalse(hasattr(journey, "_generation_completed"))
        self.assertIsNone(journey.generation_outcome)

    def test_resumed_project_reaches_existing_completion_seam(self) -> None:
        journey = journey_at_resume()
        journey.resume_existing_project(project_markdown(), current_on=CURRENT_ON)
        journey.signal_completion()
        self.assertEqual(journey.state, AuthorJourneyState.SESSION_COMPLETION)

    def test_invalid_resume_does_not_start_new_publication_automatically(self) -> None:
        journey = journey_at_resume()
        journey.resume_existing_project("invalid", current_on=CURRENT_ON)
        self.assertEqual(journey.state, AuthorJourneyState.ENTRY_PATH)
        self.assertIsNone(journey.workflow_mode)
        self.assertIsNone(journey.editorial_source)

    def test_resume_sessions_are_stateless_and_independent(self) -> None:
        first = journey_at_resume()
        second = journey_at_resume()
        first.resume_existing_project(project_markdown(), current_on=CURRENT_ON)
        second.resume_existing_project(project_markdown(), current_on=CURRENT_ON)
        first.edit_publication(headline="First session only")
        self.assertNotEqual(
            first.publication_studio.editor.current_content.headline,
            second.publication_studio.editor.current_content.headline,
        )


if __name__ == "__main__":
    unittest.main()
