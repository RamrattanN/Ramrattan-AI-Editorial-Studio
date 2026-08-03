"""Tests for the Capability 5 architecture baseline."""

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


class Capability005ArchitectureTests(unittest.TestCase):
    def test_editorial_context_model_exists(self) -> None:
        path = (
            ROOT
            / "docs"
            / "architecture"
            / "Editorial_Context_Model.md"
        )

        self.assertTrue(path.is_file())

    def test_context_is_the_working_memory(self) -> None:
        content = normalized(
            "docs/architecture/"
            "Editorial_Context_Model.md"
        )

        self.assertIn("working memory", content)
        self.assertIn(
            "before the first article draft",
            content,
        )
        self.assertIn(
            "dependency intelligence",
            content.lower(),
        )

    def test_product_does_not_require_paths(self) -> None:
        content = normalized(
            "docs/architecture/"
            "Portable_Editorial_Project.md"
        )

        self.assertIn(
            "The Product does not require:",
            content,
        )
        self.assertIn(
            "must not burden the Author "
            "with reporting file paths",
            content,
        )

    def test_portable_project_is_author_owned(self) -> None:
        content = normalized(
            "docs/architecture/"
            "Portable_Editorial_Project.md"
        )

        self.assertIn(
            "The Studio's memory belongs to the Author",
            content,
        )
        self.assertIn(
            "stateless by default",
            content,
        )
        self.assertIn(
            "Resume an Existing Editorial Project",
            content,
        )

    def test_vcm_filename_standard_is_defined(self) -> None:
        content = normalized(
            "docs/architecture/"
            "Portable_Editorial_Project.md"
        )

        self.assertIn("YYYY.MM.DDvNN", content)
        self.assertIn(
            "Ramrattan-Editorial-Project_",
            content,
        )
        self.assertIn(
            "must never exceed 255 characters",
            content,
        )

    def test_expired_urls_are_supported(self) -> None:
        content = normalized(
            "docs/architecture/"
            "Portable_Editorial_Project.md"
        )

        self.assertIn(
            "URLs may expire or change",
            content,
        )
        self.assertIn(
            "concise durable summary",
            content,
        )
        self.assertIn(
            "remain understandable when a URL",
            content,
        )

    def test_paywalled_material_is_handled(self) -> None:
        content = normalized(
            "docs/architecture/"
            "Portable_Editorial_Project.md"
        )

        self.assertIn(
            "Authors may paste material "
            "from a paywalled source",
            content,
        )
        self.assertIn(
            "should not automatically place "
            "the complete paywalled article",
            content,
        )
        self.assertIn(
            "reverification may be needed",
            content,
        )

    def test_publication_urls_are_optional(self) -> None:
        content = normalized(
            "docs/architecture/"
            "Portable_Editorial_Project.md"
        )

        self.assertIn(
            "Publication URLs are optional",
            content,
        )
        self.assertIn(
            "must remain useful when a URL",
            content,
        )

    def test_editorial_integrity_is_first_class(self) -> None:
        content = normalized(
            "docs/architecture/"
            "Editorial_Integrity_Charter.md"
        )

        self.assertIn(
            "Editorial Integrity is a product capability",
            content,
        )
        self.assertIn(
            "harmful intent",
            content.lower(),
        )
        self.assertIn(
            "source reputation",
            content.lower(),
        )
        self.assertIn(
            "originality",
            content.lower(),
        )

    def test_definition_of_done_requires_demo(self) -> None:
        content = normalized(
            "docs/architecture/"
            "Definition_of_Done.md"
        )

        self.assertIn(
            "Every completed capability must include "
            "a demo document",
            content,
        )
        self.assertIn(
            "What did we learn",
            content,
        )

    def test_capability_demo_exists(self) -> None:
        path = (
            ROOT
            / "docs"
            / "demos"
            / "Capability-005-"
            "Adaptive-Editorial-Context.md"
        )

        self.assertTrue(path.is_file())

    def test_prd_v12_is_active(self) -> None:
        content = normalized(
            "docs/product/PRD_v1.2.md"
        )

        self.assertIn(
            "Active Capability 5 product baseline",
            content,
        )
        self.assertIn(
            "Portable Editorial Project",
            content,
        )
        self.assertIn(
            "maximum filename length of 255 characters",
            content,
        )
        self.assertIn(
            "must not require or depend on "
            "the storage path",
            content,
        )

    def test_article_first_scope_remains(self) -> None:
        content = normalized(
            "docs/product/PRD_v1.2.md"
        )

        self.assertIn(
            "publication-ready article package",
            content,
        )
        self.assertIn(
            "Hero Visual - 720 × 425",
            content,
        )
        self.assertIn(
            "carousel generation",
            content,
        )


if __name__ == "__main__":
    unittest.main()
