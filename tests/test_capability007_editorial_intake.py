"""Runtime tests for Capability 007."""

from __future__ import annotations

import unittest

from studio.editorial_intake import (
    EditorialWorkspace,
    IdentityAssetKind,
    InputKind,
    SourceQuality,
    StageState,
)


class Capability007RuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workspace = EditorialWorkspace()

    def test_welcome_uses_editorial_workspace_language(
        self,
    ) -> None:
        message = self.workspace.welcome_message()

        self.assertIn(
            "Create a professional article",
            message,
        )
        self.assertIn(
            "Every article is reviewed",
            message,
        )
        self.assertIn(
            "You remain in control",
            message,
        )

    def test_welcome_supports_optional_name(self) -> None:
        message = self.workspace.welcome_message(
            "Nilesh"
        )

        self.assertIn(
            "Welcome back, Nilesh.",
            message,
        )

    def test_url_is_recognised(self) -> None:
        descriptor = self.workspace.recognize_input(
            "https://example.org/article"
        )

        self.assertEqual(
            descriptor.kind,
            InputKind.URL,
        )

    def test_document_is_recognised(self) -> None:
        descriptor = self.workspace.recognize_input(
            "research.pdf",
            declared_file_name="research.pdf",
        )

        self.assertEqual(
            descriptor.kind,
            InputKind.DOCUMENT,
        )

    def test_audio_is_recognised(self) -> None:
        descriptor = self.workspace.recognize_input(
            "interview.m4a",
            declared_file_name="interview.m4a",
        )

        self.assertEqual(
            descriptor.kind,
            InputKind.AUDIO,
        )
        self.assertTrue(descriptor.notes)

    def test_video_is_recognised(self) -> None:
        descriptor = self.workspace.recognize_input(
            "meeting.mp4",
            declared_file_name="meeting.mp4",
        )

        self.assertEqual(
            descriptor.kind,
            InputKind.VIDEO,
        )

    def test_portable_project_is_recognised(self) -> None:
        descriptor = self.workspace.recognize_input(
            "Ramrattan-Editorial-Project_Test_"
            "2026.08.01v01.md",
            declared_file_name=(
                "Ramrattan-Editorial-Project_Test_"
                "2026.08.01v01.md"
            ),
        )

        self.assertEqual(
            descriptor.kind,
            InputKind.PORTABLE_EDITORIAL_PROJECT,
        )

    def test_pasted_text_is_recognised(self) -> None:
        descriptor = self.workspace.recognize_input(
            "This is a sufficiently detailed professional "
            "observation that should be treated as pasted text "
            "without requiring the Author to classify it first."
        )

        self.assertEqual(
            descriptor.kind,
            InputKind.PASTED_TEXT,
        )

    def test_stage_one_and_two_complete(self) -> None:
        result = self.workspace.process(
            "https://example.org/article"
        )

        self.assertEqual(
            result.stages[0].state,
            StageState.COMPLETE,
        )
        self.assertEqual(
            result.stages[1].state,
            StageState.COMPLETE,
        )

        for stage in result.stages[2:]:
            self.assertEqual(
                stage.state,
                StageState.PENDING,
            )

    def test_source_assessment_does_not_claim_verification(
        self,
    ) -> None:
        result = self.workspace.process(
            "https://example.org/article"
        )

        self.assertTrue(
            result.source_assessment
            .requires_deeper_verification
        )

    def test_pasted_text_has_limited_provenance(
        self,
    ) -> None:
        result = self.workspace.process(
            "This is a detailed but unattributed passage "
            "containing claims that require independent "
            "verification before publication."
        )

        self.assertEqual(
            result.source_assessment.quality,
            SourceQuality.LIMITED,
        )
        self.assertFalse(
            result.source_assessment.source_identified
        )

    def test_brand_neutral_is_default(self) -> None:
        result = self.workspace.process(
            "https://example.org/article"
        )

        self.assertTrue(result.brand_neutral)

    def test_logo_requires_rights_confirmation(
        self,
    ) -> None:
        with self.assertRaises(ValueError):
            self.workspace.classify_identity_asset(
                "logo.png",
                declared_kind=IdentityAssetKind.LOGO,
                rights_confirmed=False,
            )

    def test_headshot_requires_supported_image(
        self,
    ) -> None:
        with self.assertRaises(ValueError):
            self.workspace.classify_identity_asset(
                "headshot.pdf",
                declared_kind=IdentityAssetKind.HEADSHOT,
                rights_confirmed=True,
            )

    def test_logo_can_be_added(self) -> None:
        logo = self.workspace.classify_identity_asset(
            "logo.png",
            declared_kind=IdentityAssetKind.LOGO,
            rights_confirmed=True,
        )

        result = self.workspace.process(
            "https://example.org/article",
            identity_assets=[logo],
        )

        self.assertFalse(result.brand_neutral)
        self.assertEqual(
            result.identity_assets[0].kind,
            IdentityAssetKind.LOGO,
        )

    def test_resume_without_logo_remains_possible(
        self,
    ) -> None:
        message = (
            self.workspace.missing_identity_asset_message(
                logo_was_used=True,
                headshot_was_used=False,
            )
        )

        self.assertIn(
            "upload it again",
            message.lower(),
        )
        self.assertIn(
            "brand-neutral",
            message,
        )

    def test_empty_input_is_unknown(self) -> None:
        descriptor = self.workspace.recognize_input(
            "   "
        )

        self.assertEqual(
            descriptor.kind,
            InputKind.UNKNOWN,
        )


if __name__ == "__main__":
    unittest.main()
