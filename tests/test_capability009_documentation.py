"""Documentation and boundary tests for Capability 009."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class Capability009DocumentationTests(unittest.TestCase):
    def content(self, relative):
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_adr_and_baseline_record_narrow_scope(self):
        adr = self.content(
            "docs/architecture/adr/ADR-015-article-engine-publication-package.md"
        )
        baseline = self.content(
            "docs/architecture/baselines/Architecture_Baseline_2026.08.02v10.md"
        )
        adr = " ".join(adr.split())
        baseline = " ".join(baseline.split())
        for value in ("Article Engine", "Publication Package", "Capability 010", "Capability 011"):
            self.assertIn(value, adr)
            self.assertIn(value, baseline)

    def test_scope_conflict_is_resolved_in_authorities(self):
        for relative in (
            "ROADMAP.md",
            "docs/product/Current_Product_Focus.md",
            "docs/product/PRD_v1.3.md",
            "docs/programs/Capability_008A_Master_Roadmap.md",
        ):
            content = self.content(relative)
            self.assertIn("Capability 009 Scope Clarification", content)
            self.assertIn("Article Engine", content)
            self.assertIn("Publication Package", content)
            self.assertIn("Integrated Editorial Workspace", content)

    def test_scorecard_and_contract_do_not_claim_later_outputs(self):
        scorecard = self.content("docs/VERSION_ONE_SCORECARD.md")
        contract = self.content(
            "docs/architecture/Publication_Package_Contract.md"
        )
        self.assertIn("Textual Publication Package", scorecard)
        self.assertIn("rendered Hero Visual", contract)
        self.assertIn("Capability 010", contract)
        self.assertIn("Capability 011", contract)

    def test_demo_and_definition_of_done_exist(self):
        self.assertTrue(
            (ROOT / "docs/demos/Capability-009-Article-Engine-and-Publication-Package.md").is_file()
        )
        done = self.content("docs/architecture/Definition_of_Done.md")
        self.assertIn("Capability 009 Completion Additions", done)
        self.assertIn("no new Author-facing workflow", done)

    def test_brand_masters_remain_the_approved_baseline(self):
        master = self.content("assets/brand/logo/master/README.md")
        self.assertIn(
            "b2cd1c22239b7176b43578892b0c37ac502ca5ab696b7c083a0b397bfe285727",
            master,
        )
        self.assertIn(
            "ae56f16f3e4b3a2bfbf5cefbf6ee807482cd8814e30b7496a917b9eae3a5ba72",
            master,
        )


if __name__ == "__main__":
    unittest.main()
