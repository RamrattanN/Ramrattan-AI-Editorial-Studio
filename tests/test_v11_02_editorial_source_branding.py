"""Acceptance tests for V11-02 Editorial Source and Branding Intake."""

from __future__ import annotations

import inspect
import json
import unittest

from studio.author_journey import (
    AuthorJourney,
    AuthorJourneyError,
    AuthorJourneyState,
    BrandingMaterial,
    BrandingMaterialKind,
    BrandingMode,
    EditorialInference,
    EditorialSourceKind,
    EditorialSourceMaterial,
    EntryPath,
    InvalidAuthorJourneyTransition,
    WorkflowMode,
)


FILENAME = "Ramrattan-AI-Configuration-2026.08.04v01.json"


def journey_at_source(
    mode: WorkflowMode = WorkflowMode.GUIDED,
    branding_preference: str | None = None,
) -> AuthorJourney:
    journey = AuthorJourney()
    journey.begin()
    journey.choose_entry_path(EntryPath.START_NEW_PUBLICATION)
    if branding_preference is None:
        journey.skip_configuration()
    else:
        journey.load_configuration(
            FILENAME,
            json.dumps(
                {
                    "preferred_workflow": mode.value,
                    "branding_preference": branding_preference,
                }
            ),
        )
    journey.select_workflow(mode)
    return journey


def source(kind: EditorialSourceKind = EditorialSourceKind.NOTES) -> EditorialSourceMaterial:
    return EditorialSourceMaterial(kind, "A source contribution")


class EditorialSourceTests(unittest.TestCase):
    def test_accepts_every_approved_editorial_source_form(self) -> None:
        self.assertEqual(
            tuple(EditorialSourceKind),
            (
                EditorialSourceKind.URL,
                EditorialSourceKind.ARTICLE,
                EditorialSourceKind.DOCUMENT,
                EditorialSourceKind.RESEARCH_MATERIAL,
                EditorialSourceKind.TOPIC,
                EditorialSourceKind.NOTES,
            ),
        )
        for kind in EditorialSourceKind:
            with self.subTest(kind=kind):
                journey = journey_at_source()
                journey.submit_editorial_source(source(kind))
                self.assertEqual(journey.editorial_source, source(kind))
                self.assertEqual(journey.state, AuthorJourneyState.BRANDING)

    def test_source_establishes_all_four_required_inferences(self) -> None:
        journey = journey_at_source()
        inference = journey.submit_editorial_source(source(EditorialSourceKind.TOPIC))
        self.assertTrue(inference.intent)
        self.assertTrue(inference.audience)
        self.assertTrue(inference.platform)
        self.assertTrue(inference.desired_outcome)
        self.assertEqual(journey.editorial_inference, inference)

    def test_explicit_inference_seam_is_preserved_exactly(self) -> None:
        expected = EditorialInference(
            intent="Explain the change",
            audience="Operations leaders",
            platform="LinkedIn",
            desired_outcome="Support an informed decision",
        )
        journey = journey_at_source()
        self.assertEqual(
            journey.submit_editorial_source(source(), inference=expected), expected
        )

    def test_source_input_and_inference_reject_invalid_values(self) -> None:
        with self.assertRaises(AuthorJourneyError):
            EditorialSourceMaterial(EditorialSourceKind.NOTES, "")
        journey = journey_at_source()
        with self.assertRaises(AuthorJourneyError):
            journey.submit_editorial_source("notes")  # type: ignore[arg-type]
        self.assertEqual(journey.state, AuthorJourneyState.EDITORIAL_SOURCE)


class BrandingTests(unittest.TestCase):
    def journey_at_branding(self) -> AuthorJourney:
        journey = journey_at_source()
        journey.submit_editorial_source(source())
        return journey

    def test_branding_asks_personal_or_business(self) -> None:
        prompt = self.journey_at_branding().branding_prompt()
        self.assertEqual(
            prompt.choices, (BrandingMode.PERSONAL, BrandingMode.BUSINESS)
        )

    def test_accepts_every_approved_branding_material_form(self) -> None:
        self.assertEqual(
            tuple(BrandingMaterialKind),
            (
                BrandingMaterialKind.WEBSITE,
                BrandingMaterialKind.LOGO,
                BrandingMaterialKind.PROFESSIONAL_HEADSHOT,
                BrandingMaterialKind.BRAND_COLOURS,
                BrandingMaterialKind.BRAND_GUIDE,
                BrandingMaterialKind.PRESENTATION,
                BrandingMaterialKind.PREVIOUS_HERO_VISUAL,
                BrandingMaterialKind.OTHER_VISUAL_REFERENCE,
            ),
        )
        for kind in BrandingMaterialKind:
            with self.subTest(kind=kind):
                journey = self.journey_at_branding()
                material = BrandingMaterial(kind, f"reference:{kind.value}")
                selection = journey.submit_branding(
                    BrandingMode.PERSONAL, (material,)
                )
                self.assertEqual(selection.materials, (material,))
                self.assertEqual(
                    journey.state, AuthorJourneyState.EDITORIAL_DISCOVERY
                )

    def test_no_material_uses_professional_studio_theme(self) -> None:
        journey = self.journey_at_branding()
        selection = journey.submit_branding(BrandingMode.BUSINESS)
        self.assertEqual(selection.mode, BrandingMode.STUDIO_THEME)
        self.assertEqual(selection.materials, ())

    def test_branding_rejects_editorial_source_content(self) -> None:
        journey = self.journey_at_branding()
        with self.assertRaises(AuthorJourneyError):
            journey.submit_branding(
                BrandingMode.PERSONAL,
                (source(),),  # type: ignore[arg-type]
            )
        self.assertEqual(journey.state, AuthorJourneyState.BRANDING)

    def test_branding_signature_has_no_source_or_inference_data_path(self) -> None:
        parameters = inspect.signature(AuthorJourney.submit_branding).parameters
        self.assertEqual(tuple(parameters), ("self", "mode", "materials"))
        prompt_fields = set(AuthorJourney().branding_prompt.__annotations__)
        self.assertNotIn("source", parameters)
        self.assertNotIn("inference", parameters)
        self.assertNotIn("source", prompt_fields)

    def test_source_content_does_not_influence_branding_result(self) -> None:
        results = []
        for content in ("personal logo", "business brand guide"):
            journey = journey_at_source()
            journey.submit_editorial_source(
                EditorialSourceMaterial(EditorialSourceKind.NOTES, content)
            )
            results.append(journey.submit_branding(None))
        self.assertEqual(results[0], results[1])


class ConfigurationAndWorkflowTests(unittest.TestCase):
    def test_guided_presents_source_and_branding_separately(self) -> None:
        journey = journey_at_source(WorkflowMode.GUIDED)
        self.assertEqual(
            journey.intake_presentation().visible_states,
            (AuthorJourneyState.EDITORIAL_SOURCE,),
        )
        journey.submit_editorial_source(source())
        self.assertEqual(journey.state, AuthorJourneyState.BRANDING)

    def test_express_combines_only_source_and_branding_presentation(self) -> None:
        journey = journey_at_source(WorkflowMode.EXPRESS)
        self.assertEqual(
            journey.intake_presentation().visible_states,
            (AuthorJourneyState.EDITORIAL_SOURCE, AuthorJourneyState.BRANDING),
        )
        self.assertNotIn(
            AuthorJourneyState.EDITORIAL_DISCOVERY,
            journey.intake_presentation().visible_states,
        )

    def test_express_uses_the_same_state_transitions_and_skips_no_approval(self) -> None:
        journey = journey_at_source(WorkflowMode.EXPRESS)
        journey.submit_editorial_source(source())
        self.assertEqual(journey.state, AuthorJourneyState.BRANDING)
        journey.submit_branding(None)
        self.assertEqual(journey.state, AuthorJourneyState.EDITORIAL_DISCOVERY)
        self.assertFalse(hasattr(AuthorJourney, "approve_editorial_discovery"))
        self.assertFalse(hasattr(AuthorJourney, "approve_editorial_plan"))

    def test_loaded_branding_is_displayed_but_never_silently_applied(self) -> None:
        journey = journey_at_source(
            WorkflowMode.EXPRESS, "business_branding_from_configuration"
        )
        presentation = journey.intake_presentation()
        self.assertEqual(
            presentation.carried_branding_preference,
            "business_branding_from_configuration",
        )
        self.assertIsNone(journey.branding_selection)
        journey.submit_editorial_source(source())
        prompt = journey.branding_prompt()
        self.assertEqual(
            prompt.carried_preference_to_confirm,
            "business_branding_from_configuration",
        )
        self.assertIsNone(journey.branding_selection)

    def test_carried_branding_can_be_changed_or_cleared_explicitly(self) -> None:
        changed = journey_at_source(
            WorkflowMode.GUIDED, "personal_branding_from_configuration"
        )
        changed.submit_editorial_source(source())
        material = BrandingMaterial(BrandingMaterialKind.LOGO, "new-logo.svg")
        self.assertEqual(
            changed.submit_branding(BrandingMode.BUSINESS, (material,)).mode,
            BrandingMode.BUSINESS,
        )

        cleared = journey_at_source(
            WorkflowMode.GUIDED, "personal_branding_from_configuration"
        )
        cleared.submit_editorial_source(source())
        self.assertEqual(
            cleared.submit_branding(None).mode, BrandingMode.STUDIO_THEME
        )


class TransitionAndCompatibilityTests(unittest.TestCase):
    def test_invalid_transitions_fail_closed_without_partial_mutation(self) -> None:
        journey = journey_at_source()
        with self.assertRaises(InvalidAuthorJourneyTransition):
            journey.submit_branding(None)
        self.assertEqual(journey.state, AuthorJourneyState.EDITORIAL_SOURCE)
        self.assertIsNone(journey.branding_selection)

        journey.submit_editorial_source(source())
        with self.assertRaises(InvalidAuthorJourneyTransition):
            journey.submit_editorial_source(source())
        self.assertEqual(journey.state, AuthorJourneyState.BRANDING)

    def test_discovery_is_a_routing_seam_with_no_later_slice_behavior(self) -> None:
        journey = journey_at_source()
        journey.submit_editorial_source(source())
        journey.submit_branding(None)
        self.assertEqual(journey.state, AuthorJourneyState.EDITORIAL_DISCOVERY)
        for name in ("discover", "plan", "generate", "publish", "complete"):
            self.assertFalse(hasattr(AuthorJourney, name), name)

    def test_operation_is_stateless_between_instances_and_deterministic(self) -> None:
        first = journey_at_source(WorkflowMode.EXPRESS)
        second = journey_at_source(WorkflowMode.EXPRESS)
        first_result = first.submit_editorial_source(source())
        second_result = second.submit_editorial_source(source())
        self.assertEqual(first_result, second_result)
        first.submit_branding(None)
        self.assertIsNone(second.branding_selection)
        self.assertEqual(second.state, AuthorJourneyState.BRANDING)

    def test_version_one_session_remains_wrapped_and_untouched(self) -> None:
        marker = object()
        journey = AuthorJourney(editorial_session=marker)  # type: ignore[arg-type]
        journey.begin()
        journey.choose_entry_path(EntryPath.START_NEW_PUBLICATION)
        journey.skip_configuration()
        journey.select_workflow(WorkflowMode.GUIDED)
        journey.submit_editorial_source(source())
        journey.submit_branding(None)
        self.assertIs(journey.editorial_session, marker)


if __name__ == "__main__":
    unittest.main()
