"""Governance contracts for Capability 008A.1."""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class Capability008A1GovernanceTests(unittest.TestCase):
    def content(self, relative: str) -> str:
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_agents_structure_and_required_contracts(self) -> None:
        content = self.content("AGENTS.md")
        self.assertEqual(len(re.findall(r"^```", content, re.MULTILINE)) % 2, 0)
        for heading in (
            "## Instruction Authority",
            "## Dirty-Tree Protection",
            "## Autonomous Execution",
            "## Approval Boundaries",
            "## Validation",
            "## Generated Files",
            "## Stopping Conditions",
            "## Governance Document Responsibilities",
        ):
            self.assertIn(heading, content)
        for command in (
            "python3 -m compileall -q studio scripts tests",
            "python3 -m unittest discover -s tests -v",
            "python3 studio.py validate",
        ):
            self.assertIn(command, content)

    def test_memory_is_advisory_and_append_oriented(self) -> None:
        content = self.content("AGENT_MEMORY.md")
        self.assertIn("advisory", content)
        self.assertIn("must not define current repository status", content)
        self.assertIn("append dated lessons", content)
        self.assertNotIn("The Author strongly prefers", content)

    def test_contributing_defers_to_governing_authorities(self) -> None:
        content = self.content("CONTRIBUTING.md")
        self.assertIn("Repository Maintainer's", content)
        self.assertIn("current request defines the maximum scope", content)
        self.assertIn("staging changes with `git add`", content)
        self.assertIn("scripts/capability_delivery.py", content)
        self.assertIn("python3 -m compileall -q studio scripts tests", content)
        self.assertIn("Never repair only a generated artifact", content)

    def test_adr_011_is_narrow_and_claims_no_governance_baseline(self) -> None:
        adr = self.content(
            "docs/architecture/adr/ADR-011-governance-authority.md"
        )
        self.assertIn("# ADR-011 - Governance Authority", adr)
        self.assertIn("Accepted", adr)
        self.assertIn("No new architecture baseline", adr)
        self.assertIn("does not change runtime", adr)
        self.assertNotIn("2026.08.01v07", adr)

    def test_adr_index_and_adr_002_disposition_are_honest(self) -> None:
        index = self.content("docs/architecture/adr/README.md")
        self.assertIn("ADR-011 - Governance Authority", index)
        self.assertIn("ADR-002 was never committed", index)
        self.assertFalse(
            any(
                path.name.startswith("ADR-002")
                for path in (ROOT / "docs/architecture/adr").iterdir()
            )
        )
        baseline = self.content(
            "docs/architecture/baselines/Architecture_Baseline_2026.08.01v01.md"
        )
        self.assertNotIn("ADR-002", baseline)
        self.assertIn("docs/architecture/Editorial_Context_Model.md", baseline)

    def test_status_records_agree(self) -> None:
        records = (
            "ROADMAP.md",
            "docs/VERSION_ONE_SCORECARD.md",
            "docs/product/Current_Product_Focus.md",
            "docs/product/Release_v1.0.md",
        )
        for relative in records:
            content = self.content(relative)
            self.assertIn("Capability 008 - Complete", content)
            self.assertIn(
                "Capability 008A.1 - Governance Consolidation - In Progress",
                content,
            )
            self.assertIn(
                "Capability 008A.2 - Delivery Hardening - Not started",
                content,
            )
            self.assertIn(
                "Capability 008A.3 - Editorial Integrity Hardening - Not started",
                content,
            )
            self.assertIn("Capability 009 - Not started", content)

    def test_current_baseline_references_are_v06(self) -> None:
        for relative in (
            "docs/product/Decision_Log.md",
            "docs/product/Release_v1.0.md",
        ):
            self.assertIn("2026.08.01v06", self.content(relative))

    def test_completed_runtime_is_not_listed_as_planned(self) -> None:
        scorecard = self.content("docs/VERSION_ONE_SCORECARD.md")
        for area in (
            "Editorial Workspace",
            "Editorial Intake",
            "Source Assessment",
            "Evidence Validation",
            "LMHS Editorial Risk",
            "Editorial Confidence Translation",
        ):
            row = next(line for line in scorecard.splitlines() if f"| {area} |" in line)
            self.assertIn("| Complete |", row)

    def test_owning_generators_include_reference_repairs(self) -> None:
        capability006 = self.content(
            "scripts/bootstrap_capability006_editorial_integrity.py"
        )
        capability006a = self.content(
            "scripts/bootstrap_capability006a_constitutional_freeze.py"
        )
        self.assertNotIn("ADR-002 - Adaptive Editorial Context", capability006)
        self.assertIn("2026.08.01v06", capability006)
        self.assertIn(
            "| Evidence Validation | Complete | Capability 008 runtime |",
            capability006a,
        )


if __name__ == "__main__":
    unittest.main()
