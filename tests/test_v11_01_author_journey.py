"""Acceptance tests for V11-01 Author Journey Foundation."""

from __future__ import annotations

import json
import unittest

from studio.author_journey import (
    AuthorJourney,
    AuthorJourneyState,
    ConfigurationValidationError,
    EntryPath,
    InvalidAuthorJourneyTransition,
    StudioConfiguration,
    WorkflowMode,
    load_studio_configuration,
)


FILENAME = "Ramrattan-AI-Configuration-2024.01.03v01.json"


def configuration_json(
    workflow: str = "express",
    branding: str = "studio_theme",
    **extra: object,
) -> str:
    values: dict[str, object] = {
        "preferred_workflow": workflow,
        "branding_preference": branding,
    }
    values.update(extra)
    return json.dumps(values)


class EntryPathTests(unittest.TestCase):
    def test_initial_welcome_automatically_leads_to_entry_path(self) -> None:
        journey = AuthorJourney()
        self.assertEqual(journey.state, AuthorJourneyState.WELCOME)
        journey.begin()
        self.assertEqual(journey.state, AuthorJourneyState.ENTRY_PATH)

    def test_entry_path_has_exactly_two_choices(self) -> None:
        self.assertEqual(
            AuthorJourney.ENTRY_PATH_CHOICES,
            (
                EntryPath.START_NEW_PUBLICATION,
                EntryPath.RESUME_EXISTING_PROJECT,
            ),
        )

    def test_start_new_publication_routes_to_configuration_load(self) -> None:
        journey = AuthorJourney()
        journey.begin()
        journey.choose_entry_path(EntryPath.START_NEW_PUBLICATION)
        self.assertEqual(journey.state, AuthorJourneyState.CONFIGURATION_LOAD)

    def test_resume_routes_only_to_resume_validation_seam(self) -> None:
        journey = AuthorJourney()
        journey.begin()
        journey.choose_entry_path(EntryPath.RESUME_EXISTING_PROJECT)
        self.assertEqual(journey.state, AuthorJourneyState.RESUME_VALIDATION)
        self.assertFalse(journey.configuration_loaded)
        self.assertIsNone(journey.workflow_mode)
        self.assertIsNone(journey.branding_preference)

    def test_configuration_load_is_unreachable_from_resume(self) -> None:
        journey = AuthorJourney()
        journey.begin()
        journey.choose_entry_path(EntryPath.RESUME_EXISTING_PROJECT)
        with self.assertRaises(InvalidAuthorJourneyTransition):
            journey.load_configuration(FILENAME, configuration_json())
        with self.assertRaises(InvalidAuthorJourneyTransition):
            journey.skip_configuration()

    def test_invalid_transitions_fail_closed(self) -> None:
        journey = AuthorJourney()
        with self.assertRaises(InvalidAuthorJourneyTransition):
            journey.choose_entry_path(EntryPath.START_NEW_PUBLICATION)
        journey.begin()
        with self.assertRaises(InvalidAuthorJourneyTransition):
            journey.select_workflow(WorkflowMode.GUIDED)
        with self.assertRaises(InvalidAuthorJourneyTransition):
            journey.begin()


class ConfigurationTests(unittest.TestCase):
    def test_configuration_load_is_optional_and_skip_uses_defaults(self) -> None:
        journey = AuthorJourney()
        journey.begin()
        journey.choose_entry_path(EntryPath.START_NEW_PUBLICATION)
        journey.skip_configuration()
        self.assertEqual(journey.state, AuthorJourneyState.WORKFLOW_SELECTION)
        self.assertFalse(journey.configuration_loaded)
        self.assertIsNone(journey.workflow_mode)
        self.assertIsNone(journey.branding_preference)

    def test_json_configuration_restores_only_two_session_preferences(self) -> None:
        journey = AuthorJourney()
        journey.begin()
        journey.choose_entry_path(EntryPath.START_NEW_PUBLICATION)
        journey.load_configuration(
            FILENAME,
            configuration_json(branding="personal_branding_logo"),
        )
        self.assertEqual(journey.state, AuthorJourneyState.WORKFLOW_SELECTION)
        self.assertEqual(journey.workflow_mode, WorkflowMode.EXPRESS)
        self.assertEqual(journey.branding_preference, "personal_branding_logo")
        self.assertTrue(journey.configuration_loaded)
        self.assertEqual(
            set(vars(journey)),
            {
                "editorial_session",
                "state",
                "workflow_mode",
                "branding_preference",
                "configuration_loaded",
            },
        )

    def test_filename_is_json_only_and_age_is_not_a_rejection_reason(self) -> None:
        old = load_studio_configuration(FILENAME, configuration_json())
        self.assertEqual(old.preferred_workflow, WorkflowMode.EXPRESS)
        for invalid in (
            "Ramrattan-AI-Configuration-2024.01.03v01.md",
            "configuration.json",
            "Ramrattan-AI-Configuration-2024.01.03v1.json",
        ):
            with self.subTest(invalid=invalid):
                with self.assertRaisesRegex(
                    ConfigurationValidationError, "filename must match"
                ):
                    load_studio_configuration(invalid, configuration_json())

    def test_malformed_and_unsupported_content_is_rejected_specifically(self) -> None:
        cases = (
            ("{", "invalid JSON"),
            ("[]", "one object"),
            (json.dumps({"preferred_workflow": "guided"}), "missing fields"),
            (configuration_json(source="private"), "unsupported fields"),
            (configuration_json(workflow="automatic"), "guided or express"),
            (configuration_json(branding=""), "must not be empty"),
        )
        for content, message in cases:
            with self.subTest(message=message):
                with self.assertRaisesRegex(ConfigurationValidationError, message):
                    load_studio_configuration(FILENAME, content)

    def test_schema_cannot_carry_content_evidence_project_or_asset_bytes(self) -> None:
        forbidden = (
            "editorial_content",
            "evidence",
            "source_material",
            "portable_editorial_project",
            "logo_bytes",
            "audience",
        )
        for field in forbidden:
            with self.subTest(field=field):
                with self.assertRaisesRegex(
                    ConfigurationValidationError, "unsupported fields"
                ):
                    load_studio_configuration(
                        FILENAME, configuration_json(**{field: "forbidden"})
                    )

    def test_configuration_round_trip_is_identical_and_deterministic(self) -> None:
        configuration = StudioConfiguration(
            preferred_workflow=WorkflowMode.GUIDED,
            branding_preference="studio_theme",
        )
        first = configuration.to_json()
        second = configuration.to_json()
        restored = load_studio_configuration(FILENAME, first)
        self.assertEqual(first, second)
        self.assertEqual(restored, configuration)
        self.assertEqual(
            set(json.loads(first)),
            {"preferred_workflow", "branding_preference"},
        )

    def test_loaded_configuration_is_not_retained_outside_session(self) -> None:
        content = configuration_json(branding="studio_theme")
        journey = AuthorJourney()
        journey.begin()
        journey.choose_entry_path(EntryPath.START_NEW_PUBLICATION)
        journey.load_configuration(FILENAME, content)
        self.assertNotIn("filename", vars(journey))
        self.assertNotIn("content", vars(journey))
        self.assertNotIn(content, repr(vars(journey)))


class WorkflowSelectionTests(unittest.TestCase):
    def workflow_selection(self) -> AuthorJourney:
        journey = AuthorJourney()
        journey.begin()
        journey.choose_entry_path(EntryPath.START_NEW_PUBLICATION)
        journey.skip_configuration()
        return journey

    def test_workflow_selection_has_exactly_guided_and_express(self) -> None:
        self.assertEqual(
            AuthorJourney.WORKFLOW_CHOICES,
            (WorkflowMode.GUIDED, WorkflowMode.EXPRESS),
        )

    def test_loaded_workflow_is_preselected_but_must_be_confirmed_or_changed(self) -> None:
        journey = AuthorJourney()
        journey.begin()
        journey.choose_entry_path(EntryPath.START_NEW_PUBLICATION)
        journey.load_configuration(FILENAME, configuration_json("express"))
        self.assertEqual(journey.state, AuthorJourneyState.WORKFLOW_SELECTION)
        self.assertEqual(journey.workflow_mode, WorkflowMode.EXPRESS)
        journey.select_workflow(WorkflowMode.GUIDED)
        self.assertEqual(journey.workflow_mode, WorkflowMode.GUIDED)
        self.assertEqual(journey.state, AuthorJourneyState.EDITORIAL_SOURCE)

    def test_both_modes_visit_the_same_state_seam(self) -> None:
        destinations = []
        for mode in WorkflowMode:
            journey = self.workflow_selection()
            journey.select_workflow(mode)
            destinations.append(journey.state)
        self.assertEqual(
            destinations,
            [AuthorJourneyState.EDITORIAL_SOURCE] * len(WorkflowMode),
        )

    def test_no_later_slice_actions_or_abandonment_artifacts_exist(self) -> None:
        forbidden = (
            "cancel",
            "abort",
            "restart",
            "save",
            "generate",
            "resume_project",
            "enter_publication_studio",
            "complete",
        )
        for name in forbidden:
            self.assertFalse(hasattr(AuthorJourney, name), name)


if __name__ == "__main__":
    unittest.main()
