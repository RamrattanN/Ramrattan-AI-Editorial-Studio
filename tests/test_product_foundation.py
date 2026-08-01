"""Tests for the product-foundation documentation."""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRODUCT = ROOT / "docs" / "product"

REQUIRED_FILES = (
    "PRD_v1.0.md",
    "Constitution.md",
    "Product_Principles.md",
    "Studio_Contract.md",
    "Adaptive_Editorial_Model.md",
    "Author_Journey.md",
    "Things_We_Will_Not_Do.md",
    "Glossary.md",
    "Decision_Log.md",
    "Editorial_Intelligence_Manifesto.md",
)


def normalized_text(path: Path) -> str:
    """
    Read Markdown and normalize whitespace.

    This prevents harmless Markdown line wrapping from causing
    false test failures.
    """
    content = path.read_text(encoding="utf-8")
    return " ".join(content.split())


class ProductFoundationTests(unittest.TestCase):
    def test_required_documents_exist(self) -> None:
        for filename in REQUIRED_FILES:
            with self.subTest(filename=filename):
                self.assertTrue(
                    (PRODUCT / filename).is_file(),
                    msg=f"Missing product document: {filename}",
                )

    def test_prd_is_not_url_first(self) -> None:
        content = normalized_text(PRODUCT / "PRD_v1.0.md")

        self.assertIn("adaptive editorial partner", content)
        self.assertIn("headline", content)
        self.assertIn("perspective", content)
        self.assertIn("Editorial Context", content)

    def test_constitution_preserves_reversibility(self) -> None:
        content = normalized_text(PRODUCT / "Constitution.md")

        self.assertIn("Everything Is Revisable", content)
        self.assertIn("Infer Before Asking", content)
        self.assertIn("Preserve Context", content)

    def test_adaptive_model_marks_linear_workflow_as_prototype(
        self,
    ) -> None:
        content = normalized_text(
            PRODUCT / "Adaptive_Editorial_Model.md"
        )

        self.assertIn(
            "not the final product interaction model",
            content,
        )

    def test_glossary_defines_author_and_context(self) -> None:
        content = normalized_text(PRODUCT / "Glossary.md")

        self.assertIn("## Author", content)
        self.assertIn("## Editorial Context", content)

    def test_readme_uses_adaptive_positioning(self) -> None:
        content = normalized_text(ROOT / "README.md")

        self.assertIn("adaptive editorial partner", content)
        self.assertIn("Authors May Begin With", content)
        self.assertIn(
            "The Studio interprets what is happening",
            content,
        )

    def test_adr_records_target_architecture(self) -> None:
        adr = (
            ROOT
            / "docs"
            / "architecture"
            / "adr"
            / "ADR-002-adopt-an-adaptive-editorial-context.md"
        )
        content = normalized_text(adr)

        self.assertIn(
            "evolving Editorial Context",
            content,
        )
        self.assertIn(
            "does not define the final product interaction model",
            content,
        )


if __name__ == "__main__":
    unittest.main()
