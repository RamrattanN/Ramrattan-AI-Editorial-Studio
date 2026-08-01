"""Tests for the article-first product alignment."""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def normalized(path: str) -> str:
    """Read a repository file and normalize Markdown whitespace."""
    content = (ROOT / path).read_text(encoding="utf-8")
    content = content.replace(">", " ")
    return " ".join(content.split())


class ArticleFirstAlignmentTests(unittest.TestCase):
    def test_readme_is_article_first(self) -> None:
        content = normalized("README.md")

        self.assertIn(
            "publication-ready professional articles",
            content,
        )
        self.assertIn("720 × 425 Hero Visual", content)
        self.assertIn("approximately 10 minutes", content)
        self.assertIn("Carousels", content)
        self.assertIn(
            "not part of the active product scope",
            content,
        )

    def test_prd_v11_exists(self) -> None:
        path = ROOT / "docs" / "product" / "PRD_v1.1.md"

        self.assertTrue(
            path.is_file(),
            msg="PRD v1.1 is missing.",
        )

    def test_prd_defines_input_quality_response(self) -> None:
        content = normalized("docs/product/PRD_v1.1.md")

        self.assertIn(
            "explain why the input is insufficient",
            content,
        )
        self.assertIn(
            "provide an example of a stronger input",
            content,
        )
        self.assertIn("approximately 10 minutes", content)

    def test_glossary_defines_hero_visual(self) -> None:
        content = normalized("docs/product/Glossary.md")

        self.assertIn("## Hero Visual", content)
        self.assertIn("720 × 425", content)
        self.assertIn("## Author Library", content)

    def test_adr_records_article_first_scope(self) -> None:
        content = normalized(
            "docs/architecture/adr/"
            "ADR-003-adopt-an-article-first-publication-package.md"
        )

        self.assertIn("article-first", content.lower())
        self.assertIn(
            "Carousels are removed from the active roadmap",
            content,
        )

    def test_legacy_workflow_is_clearly_labelled(self) -> None:
        content = normalized("studio/workflow/README.md")

        self.assertIn("Historical prototype notice", content)
        self.assertIn(
            "not part of the current product scope",
            content,
        )

    def test_current_focus_defines_author_library(self) -> None:
        content = normalized(
            "docs/product/Current_Product_Focus.md"
        )

        self.assertIn(
            "The Author Library stores paused or completed work",
            content,
        )
        self.assertIn("private by default", content)

    def test_publication_package_contains_hero_visual(self) -> None:
        content = normalized("docs/product/PRD_v1.1.md")

        self.assertIn("Hero Visual - 720 × 425", content)
        self.assertIn("Publication-ready article", content)


if __name__ == "__main__":
    unittest.main()
