"""Tests for Capability 006 architecture and V1.0 baseline."""

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


class Capability006Tests(unittest.TestCase):
    def test_integrity_pipeline_exists(self) -> None:
        path = (
            ROOT
            / "docs"
            / "architecture"
            / "Editorial_Integrity_Pipeline.md"
        )

        self.assertTrue(path.is_file())

    def test_five_visible_stages_are_defined(self) -> None:
        content = normalized(
            "docs/architecture/"
            "Editorial_Integrity_Pipeline.md"
        )

        self.assertIn(
            "Understanding your input",
            content,
        )
        self.assertIn(
            "Assessing your sources",
            content,
        )
        self.assertIn(
            "Verifying the evidence",
            content,
        )
        self.assertIn(
            "Reviewing editorial risks",
            content,
        )
        self.assertIn(
            "Creating your publication package",
            content,
        )

    def test_lmhs_risk_is_defined(self) -> None:
        content = normalized(
            "docs/architecture/"
            "Editorial_Integrity_Pipeline.md"
        )

        for level in (
            "Low Editorial Risk",
            "Moderate Editorial Risk",
            "High Editorial Risk",
            "Severe Editorial Risk",
        ):
            self.assertIn(level, content)

        self.assertIn(
            "does not use arbitrary percentages",
            content,
        )

    def test_false_information_guardrail_exists(self) -> None:
        content = normalized(
            "docs/architecture/"
            "Editorial_Integrity_Pipeline.md"
        )

        self.assertIn(
            "must not knowingly disseminate",
            content,
        )
        self.assertIn(
            "materially false",
            content,
        )

    def test_progressive_recovery_exists(self) -> None:
        content = normalized(
            "docs/architecture/"
            "Editorial_Integrity_Pipeline.md"
        )

        self.assertIn(
            "Progressive Recovery",
            content,
        )
        self.assertIn(
            "maximize responsible forward progress",
            content,
        )

    def test_temporal_integrity_exists(self) -> None:
        content = normalized(
            "docs/architecture/"
            "Editorial_Integrity_Pipeline.md"
        )

        self.assertIn(
            "Temporal Integrity",
            content,
        )
        self.assertIn(
            "statistics may be outdated",
            content,
        )

    def test_option_interaction_has_three_choices(self) -> None:
        content = normalized(
            "docs/architecture/"
            "Editorial_Collaboration_Model.md"
        )

        self.assertIn(
            "provide three high-quality options",
            content,
        )
        self.assertIn(
            "must not label an option as Recommended",
            content,
        )
        self.assertIn(
            "provide their own content",
            content,
        )

    def test_recommendation_follows_options(self) -> None:
        content = normalized(
            "docs/architecture/"
            "Editorial_Collaboration_Model.md"
        )

        self.assertIn(
            "After all options are presented",
            content,
        )
        self.assertIn(
            "editorial opinion",
            content,
        )

    def test_dependency_updates_are_not_silent(self) -> None:
        content = normalized(
            "docs/architecture/"
            "Editorial_Collaboration_Model.md"
        )

        self.assertIn(
            "Change only the requested component",
            content,
        )
        self.assertIn(
            "must not silently regenerate",
            content,
        )

    def test_export_is_fast_path(self) -> None:
        content = normalized(
            "docs/architecture/"
            "Publication_Package_Contract.md"
        )

        self.assertIn(
            "Export the publication package",
            content,
        )
        self.assertIn(
            "first completion action",
            content,
        )

    def test_publication_package_components_exist(self) -> None:
        content = normalized(
            "docs/architecture/"
            "Publication_Package_Contract.md"
        )

        for phrase in (
            "Hero Visual prompt",
            "Hero Visual - 720 × 425",
            "Headline",
            "Hook",
            "Insight 1",
            "Practical Takeaway",
            "Call to Action",
            "Source and attribution",
            "Hashtags",
            "LinkedIn Description",
            "Portable Editorial Project",
        ):
            self.assertIn(phrase, content)

    def test_version_one_release_exists(self) -> None:
        path = (
            ROOT
            / "docs"
            / "product"
            / "Release_v1.0.md"
        )

        self.assertTrue(path.is_file())

    def test_version_one_excludes_carousels(self) -> None:
        content = normalized(
            "docs/product/Release_v1.0.md"
        )

        self.assertIn(
            "Carousel generation",
            content,
        )
        self.assertIn(
            "Version 1.0 excludes",
            content,
        )

    def test_product_vision_is_concise_reference(self) -> None:
        content = normalized(
            "docs/product/Product_Vision.md"
        )

        self.assertIn(
            "What It Will Not Become",
            content,
        )
        self.assertIn(
            "Detailed behaviour is defined",
            content,
        )

    def test_architecture_baseline_uses_vcm(self) -> None:
        content = normalized(
            "docs/architecture/baselines/"
            "Architecture_Baseline_2026.08.01v01.md"
        )

        self.assertIn(
            "2026.08.01v01",
            content,
        )
        self.assertIn(
            "Active Version 1.0 architecture baseline",
            content,
        )

    def test_prd_v13_is_active(self) -> None:
        content = normalized(
            "docs/product/PRD_v1.3.md"
        )

        self.assertIn(
            "Active Version 1.0 product baseline",
            content,
        )
        self.assertIn(
            "LMHS Editorial Risk",
            content,
        )
        self.assertIn(
            "Export the publication package",
            content,
        )


if __name__ == "__main__":
    unittest.main()
