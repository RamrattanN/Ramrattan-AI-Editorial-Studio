"""Tests for Capability 006A Constitutional Freeze."""

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


class Capability006AConstitutionTests(unittest.TestCase):
    def test_start_here_exists(self) -> None:
        self.assertTrue(
            (ROOT / "docs/START_HERE.md").is_file()
        )

    def test_constitution_exists(self) -> None:
        self.assertTrue(
            (
                ROOT
                / "docs"
                / "constitution"
                / "Constitution.md"
            ).is_file()
        )

    def test_constitution_centres_trust(self) -> None:
        content = normalized(
            "docs/constitution/Constitution.md"
        )

        self.assertIn(
            "trust is the foundation",
            content.lower(),
        )
        self.assertIn(
            "Trust Above All",
            content,
        )

    def test_motto_is_defined(self) -> None:
        content = normalized(
            "docs/constitution/Constitution.md"
        )

        self.assertIn(
            "Trust earned. Confidence shared. "
            "Conversations inspired.",
            content,
        )

    def test_human_collaboration_model_exists(self) -> None:
        content = normalized(
            "docs/constitution/"
            "Human_Collaboration_Model.md"
        )

        self.assertIn("The Author", content)
        self.assertIn("The Editor", content)
        self.assertIn("The Reader", content)

    def test_author_owns_message(self) -> None:
        content = normalized(
            "docs/constitution/Constitution.md"
        )

        self.assertIn(
            "The Author Owns the Message",
            content,
        )

    def test_editor_charter_exists(self) -> None:
        content = normalized(
            "docs/constitution/Editor_Charter.md"
        )

        self.assertIn(
            "The Editor Will Never",
            content,
        )
        self.assertIn(
            "knowingly assist publication of materially "
            "false information",
            content,
        )

    def test_reader_principles_exist(self) -> None:
        content = normalized(
            "docs/constitution/"
            "Reader_Experience_Principles.md"
        )

        self.assertIn(
            "Respect the Reader's Intelligence",
            content,
        )
        self.assertIn(
            "Conversation Over Engagement",
            content,
        )

    def test_editorial_confidence_is_author_facing(self) -> None:
        content = normalized(
            "docs/constitution/"
            "Editorial_Behaviour_Standard.md"
        )

        self.assertIn(
            "primary Author-facing conclusion "
            "is Editorial Confidence",
            content,
        )

    def test_internal_risk_remains_lmhs(self) -> None:
        content = normalized(
            "docs/constitution/"
            "Product_Philosophy.md"
        )

        self.assertIn(
            "Editorial Risk remains an internal "
            "editorial assessment",
            content,
        )

    def test_component_collaboration_is_generic(self) -> None:
        content = normalized(
            "docs/constitution/Author_Journey.md"
        )

        for component in (
            "Hero Visual",
            "Headline",
            "Hook",
            "Practical Takeaway",
            "CTA",
            "Hashtags",
            "LinkedIn Description",
        ):
            self.assertIn(component, content)

    def test_three_options_and_author_option(self) -> None:
        content = normalized(
            "docs/constitution/Author_Journey.md"
        )

        self.assertIn(
            "Three editorially distinct options",
            content,
        )
        self.assertIn(
            "provide their own content",
            content,
        )

    def test_recommendation_comes_after_options(self) -> None:
        content = normalized(
            "docs/constitution/Author_Journey.md"
        )

        self.assertIn(
            "recommendation after all options",
            content,
        )

    def test_dependencies_require_permission(self) -> None:
        content = normalized(
            "docs/constitution/"
            "Editorial_Behaviour_Standard.md"
        )

        self.assertIn(
            "Ask before changing dependent components",
            content,
        )

    def test_cta_framework_exists(self) -> None:
        content = normalized(
            "docs/constitution/"
            "Editorial_Language_Framework.md"
        )

        self.assertIn(
            "Conversation Invitation Framework",
            content,
        )
        self.assertIn(
            "article-specific editorial question",
            content,
        )
        self.assertIn(
            "naturally varied",
            content,
        )

    def test_editorial_fingerprint_exists(self) -> None:
        content = normalized(
            "docs/constitution/"
            "Editorial_Fingerprint.md"
        )

        self.assertIn(
            "recognised not by what it says",
            content,
        )
        self.assertIn(
            "consistently it earns trust",
            content,
        )

    def test_canonical_session_exists(self) -> None:
        content = normalized(
            "docs/constitution/"
            "Canonical_Editorial_Session.md"
        )

        self.assertIn(
            "Version 1.0 acceptance demonstration",
            content,
        )
        self.assertIn(
            "Component Collaboration",
            content,
        )
        self.assertIn(
            "Export the publication package",
            content,
        )

    def test_constitutional_decision_register_exists(self) -> None:
        self.assertTrue(
            (
                ROOT
                / "docs"
                / "constitution"
                / "Constitutional_Decision_Register.md"
            ).is_file()
        )

    def test_adr_006_exists(self) -> None:
        path = (
            ROOT
            / "docs"
            / "architecture"
            / "adr"
            / "ADR-006-adopt-the-constitutional-model.md"
        )

        self.assertTrue(path.is_file())

    def test_constitutional_impact_review_exists(self) -> None:
        content = normalized(
            "docs/architecture/adr/"
            "ADR-006-adopt-the-constitutional-model.md"
        )

        self.assertIn(
            "Constitutional Impact Review",
            content,
        )

    def test_architecture_baseline_v02_exists(self) -> None:
        path = (
            ROOT
            / "docs"
            / "architecture"
            / "baselines"
            / "Architecture_Baseline_2026.08.01v02.md"
        )

        self.assertTrue(path.is_file())

    def test_vcm_same_day_rule_is_defined(self) -> None:
        content = normalized(
            "docs/architecture/baselines/"
            "Architecture_Baseline_2026.08.01v02.md"
        )

        self.assertIn(
            "Same-day revisions increment `vNN`",
            content,
        )

    def test_version_one_scorecard_exists(self) -> None:
        self.assertTrue(
            (
                ROOT
                / "docs"
                / "VERSION_ONE_SCORECARD.md"
            ).is_file()
        )


if __name__ == "__main__":
    unittest.main()
