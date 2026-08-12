"""Acceptance tests for V11-08 Session Completion and Artifacts."""

from __future__ import annotations

from dataclasses import replace
from datetime import date
import json
import unittest

from studio.author_journey import (
    AuthorJourney,
    AuthorJourneyError,
    AuthorJourneyState,
    InvalidAuthorJourneyTransition,
    WorkflowMode,
)
from studio.evidence_validation import EditorialConfidence, EditorialRisk
from studio.hero_visual import HeroVisualRequest, HeroVisualSystem
from studio.portable_editorial_project import (
    ProjectState,
    ResumeResult,
    deserialize_project,
    from_publication_package,
    serialize_project,
)
from studio.publication_package import (
    PackageReadiness,
    PublicationPackage,
    PublicationPackageBuilder,
)
from studio.publication_studio import PublicationStudio
from studio.session_completion import SessionCompletionError


TODAY = date(2026, 8, 5)
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


def journey_at_completion() -> AuthorJourney:
    journey = AuthorJourney()
    journey.workflow_mode = WorkflowMode.GUIDED
    journey.branding_preference = "business"
    journey._publication_studio = PublicationStudio.from_generation(
        package(),
        branding_summary="business; 1 Author-supplied reference",
        session_summary="Publish a professional article.",
    )
    journey.state = AuthorJourneyState.PUBLICATION_STUDIO
    journey.signal_completion()
    return journey


class SessionCompletionTests(unittest.TestCase):
    def test_session_completion_presents_configuration_prompt(self) -> None:
        journey = journey_at_completion()
        self.assertIn("generate a Ramrattan AI Configuration", journey.completion_prompt())
        self.assertEqual(journey.state, AuthorJourneyState.SESSION_COMPLETION)

    def test_completion_is_rejected_from_any_other_state(self) -> None:
        journey = AuthorJourney()
        with self.assertRaises(InvalidAuthorJourneyTransition):
            journey.complete_session(
                generate_configuration=False,
                completed_on=TODAY,
            )

    def test_configuration_choice_must_be_explicit_boolean(self) -> None:
        journey = journey_at_completion()
        with self.assertRaises(AuthorJourneyError):
            journey.complete_session(
                generate_configuration="yes",  # type: ignore[arg-type]
                completed_on=TODAY,
            )
        self.assertEqual(journey.state, AuthorJourneyState.SESSION_COMPLETION)

    def test_declining_configuration_completes_without_error(self) -> None:
        artifacts = journey_at_completion().complete_session(
            generate_configuration=False,
            completed_on=TODAY,
        )
        self.assertIsNone(artifacts.configuration)

    def test_accepting_configuration_generates_supported_json_file(self) -> None:
        artifacts = journey_at_completion().complete_session(
            generate_configuration=True,
            completed_on=TODAY,
        )
        configuration = artifacts.configuration
        self.assertIsNotNone(configuration)
        assert configuration is not None
        self.assertEqual(
            configuration.filename,
            "Ramrattan-AI-Configuration-2026.08.05v01.json",
        )
        self.assertEqual(configuration.media_type, "application/json")
        self.assertEqual(
            json.loads(configuration.content),
            {"preferred_workflow": "guided", "branding_preference": "business"},
        )

    def test_final_package_reflects_live_author_edits(self) -> None:
        journey = journey_at_completion()
        journey.state = AuthorJourneyState.PUBLICATION_STUDIO
        journey.edit_publication(
            headline="The Author's Final Headline",
            article="# Final\n\nAuthor-edited article.\n",
            cta="What will you protect?",
        )
        journey.signal_completion()
        artifacts = journey.complete_session(
            generate_configuration=False,
            completed_on=TODAY,
        )
        final = artifacts.publication_package
        self.assertEqual(final.headline, "The Author's Final Headline")
        self.assertEqual(final.article_markdown, "# Final\n\nAuthor-edited article.\n")
        self.assertEqual(final.cta, "What will you protect?")

    def test_portable_project_reflects_live_author_edits(self) -> None:
        journey = journey_at_completion()
        journey.state = AuthorJourneyState.PUBLICATION_STUDIO
        journey.edit_publication(article="# Final\n\nAuthor-owned.\n")
        journey.signal_completion()
        artifacts = journey.complete_session(
            generate_configuration=False,
            completed_on=TODAY,
        )
        restored = deserialize_project(
            artifacts.portable_editorial_project.content.decode("utf-8")
        )
        self.assertEqual(restored.article_markdown, "# Final\n\nAuthor-owned.\n")

    def test_publication_package_uses_existing_project_attachment_contract(self) -> None:
        artifacts = journey_at_completion().complete_session(
            generate_configuration=False,
            completed_on=TODAY,
        )
        self.assertTrue(artifacts.publication_package.version_one_complete)
        self.assertIsNotNone(artifacts.publication_package.portable_editorial_project)

    def test_configuration_and_project_remain_distinct_artifacts(self) -> None:
        artifacts = journey_at_completion().complete_session(
            generate_configuration=True,
            completed_on=TODAY,
        )
        assert artifacts.configuration is not None
        configuration = artifacts.configuration.content.decode("utf-8")
        project = artifacts.portable_editorial_project.content.decode("utf-8")
        self.assertNotIn("article_markdown", configuration)
        self.assertNotIn("project_id", configuration)
        self.assertNotIn("preferred_workflow", project)

    def test_artifacts_are_byte_deterministic(self) -> None:
        first = journey_at_completion().complete_session(
            generate_configuration=True,
            completed_on=TODAY,
        )
        second = journey_at_completion().complete_session(
            generate_configuration=True,
            completed_on=TODAY,
        )
        self.assertEqual(first.publication_package, second.publication_package)
        self.assertEqual(first.portable_editorial_project, second.portable_editorial_project)
        self.assertEqual(first.configuration, second.configuration)

    def test_artifact_names_advance_without_overwrite(self) -> None:
        artifacts = journey_at_completion().complete_session(
            generate_configuration=True,
            completed_on=TODAY,
            existing_project_names=(
                "Ramrattan-Editorial-Project_Trust-Before-Convenience_2026.08.05v01.md",
            ),
            existing_configuration_names=(
                "Ramrattan-AI-Configuration-2026.08.05v01.json",
            ),
        )
        self.assertIn("v02.md", artifacts.portable_editorial_project.filename)
        assert artifacts.configuration is not None
        self.assertIn("v02.json", artifacts.configuration.filename)

    def test_configuration_failure_is_fail_closed(self) -> None:
        journey = journey_at_completion()
        journey.workflow_mode = None
        with self.assertRaises(SessionCompletionError) as context:
            journey.complete_session(
                generate_configuration=True,
                completed_on=TODAY,
            )
        partial = context.exception.partial_artifacts
        self.assertIsNotNone(partial)
        assert partial is not None
        self.assertIsNotNone(partial.publication_package)
        self.assertIsNotNone(partial.portable_editorial_project)
        self.assertIsNone(partial.configuration)
        self.assertEqual(journey.state, AuthorJourneyState.SESSION_COMPLETION)
        self.assertIsNotNone(journey.publication_studio)

    def test_decline_remains_available_when_configuration_cannot_be_generated(self) -> None:
        journey = journey_at_completion()
        journey.workflow_mode = None
        artifacts = journey.complete_session(
            generate_configuration=False,
            completed_on=TODAY,
        )
        self.assertIsNone(artifacts.configuration)
        self.assertEqual(journey.state, AuthorJourneyState.COMPLETE)

    def test_complete_retains_no_artifacts_or_session_state(self) -> None:
        journey = journey_at_completion()
        artifacts = journey.complete_session(
            generate_configuration=True,
            completed_on=TODAY,
        )
        self.assertIsNotNone(artifacts.configuration)
        self.assertEqual(journey.__dict__, {"state": AuthorJourneyState.COMPLETE})
        self.assertIsNone(journey.publication_studio)

    def test_complete_is_terminal(self) -> None:
        journey = journey_at_completion()
        journey.complete_session(generate_configuration=False, completed_on=TODAY)
        with self.assertRaises(InvalidAuthorJourneyTransition):
            journey.complete_session(generate_configuration=False, completed_on=TODAY)

    def test_ending_early_has_no_artifact_or_cleanup_api(self) -> None:
        journey = AuthorJourney()
        self.assertFalse(hasattr(journey, "session_artifacts"))
        self.assertFalse(hasattr(journey, "save_session"))
        self.assertFalse(hasattr(journey, "publish"))
        self.assertFalse(hasattr(journey, "cancel"))

    def test_resumed_project_completes_without_configuration_or_regeneration(self) -> None:
        original_package = package()
        original = from_publication_package(
            original_package,
            saved_on=TODAY,
            document_version="2026.08.05v01",
        )
        studio = PublicationStudio.from_resume(
            ResumeResult(ProjectState.READY, original, True, ("Temporal Integrity",))
        )
        studio.author_edit(headline="Resumed and Author Edited")
        journey = AuthorJourney()
        journey._publication_studio = studio
        journey.state = AuthorJourneyState.SESSION_COMPLETION
        artifacts = journey.complete_session(
            generate_configuration=False,
            completed_on=TODAY,
            existing_project_names=(
                "Ramrattan-Editorial-Project_Trust-Before-Convenience_2026.08.05v01.md",
            ),
        )
        restored = deserialize_project(
            artifacts.portable_editorial_project.content.decode("utf-8")
        )
        self.assertEqual(restored.project_id, original.project_id)
        self.assertEqual(restored.previous_version, original.document_version)
        self.assertEqual(restored.title, "Resumed and Author Edited")
        self.assertEqual(restored.hero_visual_sha256, original.hero_visual_sha256)

    def test_version_one_project_serialization_remains_unchanged(self) -> None:
        original = from_publication_package(
            package(), saved_on=TODAY, document_version="2026.08.05v01"
        )
        self.assertEqual(deserialize_project(serialize_project(original)), original)


if __name__ == "__main__":
    unittest.main()
