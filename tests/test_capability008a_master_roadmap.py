"""Documentation contract for the Capability 008A program roadmap."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROADMAP_PATH = ROOT / "docs" / "programs" / "Capability_008A_Master_Roadmap.md"


class Capability008AMasterRoadmapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.roadmap = ROADMAP_PATH.read_text(encoding="utf-8")

    def test_master_roadmap_exists(self) -> None:
        self.assertTrue(ROADMAP_PATH.is_file())

    def test_increments_are_present_in_order(self) -> None:
        increments = (
            "Capability 008A.1 - Governance Consolidation",
            "Capability 008A.2 - Delivery Hardening",
            "Capability 008A.3 - Editorial Integrity Hardening",
        )
        positions = tuple(self.roadmap.index(increment) for increment in increments)
        self.assertEqual(positions, tuple(sorted(positions)))

    def test_adr_strategy_is_recorded(self) -> None:
        self.assertIn("ADR-011 - Governance Authority", self.roadmap)
        self.assertIn("ADR-012 - Delivery Hardening", self.roadmap)
        self.assertIn("ADR-013 - Editorial Integrity", self.roadmap)
        self.assertIn("Do not recreate ADR-002.", self.roadmap)

    def test_baseline_strategy_is_recorded(self) -> None:
        self.assertIn("No new architecture baseline.", self.roadmap)
        self.assertIn("Architecture Baseline v07.", self.roadmap)
        self.assertIn("Architecture Baseline v08.", self.roadmap)

    def test_program_principles_are_present(self) -> None:
        self.assertIn("## Capability 008A Principles", self.roadmap)
        self.assertIn("One concern per increment.", self.roadmap)
        self.assertIn(
            "Capability 009 shall begin only after all Capability 008A success criteria",
            self.roadmap,
        )

    def test_delivery_receipt_requirement_is_present(self) -> None:
        self.assertIn("Capability Delivery Receipt", self.roadmap)
        for field in (
            "capability or increment",
            "commit",
            "pull request",
            "merge commit",
            "tests",
            "validation",
            "ADR",
            "architecture baseline",
            "repository state",
            "GitHub planning state",
            "delivery profile",
        ):
            self.assertIn(field, self.roadmap)

    def test_root_roadmap_references_authoritative_program(self) -> None:
        root_roadmap = (ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        self.assertIn(
            "docs/programs/Capability_008A_Master_Roadmap.md",
            root_roadmap,
        )
        self.assertIn("authoritative implementation plan", root_roadmap)


if __name__ == "__main__":
    unittest.main()
