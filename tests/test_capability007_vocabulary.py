"""Documentation tests for Capability 007 canonical vocabulary."""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def normalized(relative: str) -> str:
    content = (
        ROOT / relative
    ).read_text(encoding="utf-8")

    return " ".join(
        content.replace(">", " ").split()
    )


class Capability007VocabularyTests(unittest.TestCase):
    def test_canonical_vocabulary_exists(self) -> None:
        self.assertTrue(
            (
                ROOT
                / "docs"
                / "constitution"
                / "Canonical_Vocabulary.md"
            ).is_file()
        )

    def test_one_concept_one_name_rule_exists(
        self,
    ) -> None:
        content = normalized(
            "docs/constitution/Canonical_Vocabulary.md"
        )

        self.assertIn(
            "One concept. One canonical name.",
            content,
        )

    def test_workspace_and_intake_are_distinct(
        self,
    ) -> None:
        content = normalized(
            "docs/constitution/Canonical_Vocabulary.md"
        )

        self.assertIn(
            "Editorial Workspace is not a synonym "
            "for Editorial Intake",
            content,
        )

    def test_identity_asset_is_defined(self) -> None:
        content = normalized(
            "docs/constitution/Canonical_Vocabulary.md"
        )

        self.assertIn(
            "An optional Author-supplied logo or headshot",
            content,
        )

    def test_brand_neutral_remains_default(self) -> None:
        content = normalized(
            "docs/ui/Editorial_Workspace.md"
        )

        self.assertIn(
            "Brand-neutral Hero Visual creation remains "
            "the default",
            content,
        )

    def test_rights_confirmation_is_required(
        self,
    ) -> None:
        content = normalized(
            "docs/ui/Editorial_Workspace.md"
        )

        self.assertIn(
            "Rights confirmation is required",
            content,
        )

    def test_baseline_v03_exists(self) -> None:
        self.assertTrue(
            (
                ROOT
                / "docs"
                / "architecture"
                / "baselines"
                / "Architecture_Baseline_2026.08.01v03.md"
            ).is_file()
        )

    def test_adr_007_exists(self) -> None:
        self.assertTrue(
            (
                ROOT
                / "docs"
                / "architecture"
                / "adr"
                / "ADR-007-editorial-intake-runtime.md"
            ).is_file()
        )


if __name__ == "__main__":
    unittest.main()
