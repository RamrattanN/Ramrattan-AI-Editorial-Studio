from __future__ import annotations

import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def managed_section(content: str, marker: str) -> str:
    start = f"<!-- {marker}_START -->"
    end = f"<!-- {marker}_END -->"
    if start not in content or end not in content:
        raise AssertionError(f"Missing managed section: {marker}")
    return content.split(start, 1)[1].split(end, 1)[0]


def assert_capability010_complete(content: str) -> None:
    complete = re.search(
        r"(?m)^(?:[-|]\s*)?Capability 010\s*(?:[|-]|is)?\s*"
        r"(?:\*\*)?[Cc]omplete",
        content,
    ) or re.search(
        r"## Capability 010[^\n]*\n+\s*Status:\s*\*\*Complete\*\*", content
    )
    if not complete:
        raise AssertionError("Capability 010 must be Complete")
    if re.search(
        r"(?m)^(?:[-|]\s*)?Capability 010\s*(?:[|-]|is)?\s*"
        r"(?:In Progress|Todo|unstarted)",
        content,
    ):
        raise AssertionError("Capability 010 retains stale incomplete status")


class RC1CheckpointTests(unittest.TestCase):
    def text(self, relative):
        return (ROOT / relative).read_text(encoding="utf-8")

    def digest(self, relative):
        return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()

    def test_current_checkpoint_records_post_capability010_evidence(self):
        checkpoint = self.text(
            "docs/product/checkpoints/RC1_Checkpoint_2026.08.02v02.md"
        )
        for phrase in (
            "5f20cee82bad322976a0b5d3bed655f10a72d503",
            "2026.08.02v12",
            "299 passed",
            "Capabilities 001-010",
            "Capability 011 is Next, Todo,\nand unstarted",
            "issue #18",
            "B002 remains Todo, Low Priority, Post-RC1, and non-blocking",
            "Version 1 is not release-ready",
        ):
            self.assertIn(phrase, checkpoint)
        self.assertNotRegex(checkpoint, r"\b\d{1,3}%")

    def test_checkpoint_discovery_marks_old_checkpoint_historical(self):
        start_here = managed_section(
            self.text("docs/START_HERE.md"), "RC1_CHECKPOINT_DISCOVERY"
        )
        self.assertIn("RC1_Checkpoint_2026.08.02v02.md", start_here)
        self.assertIn("RC1_Checkpoint_2026.08.02.md", start_here)
        self.assertIn("historical evidence", start_here)
        self.assertTrue(
            (ROOT / "docs/product/checkpoints/RC1_Checkpoint_2026.08.02.md").is_file()
        )

    def test_brand_adoption_is_path_and_hash_verified(self):
        readme = self.text("README.md")
        match = re.search(r'<img src="([^"]+)"', readme)
        self.assertIsNotNone(match)
        self.assertTrue((ROOT / match.group(1)).is_file())
        self.assertEqual(
            self.digest("assets/brand/logo/master/editorial-compass-mark-master.png"),
            "b2cd1c22239b7176b43578892b0c37ac502ca5ab696b7c083a0b397bfe285727",
        )
        self.assertEqual(
            self.digest("assets/brand/logo/master/editorial-compass-lockup-master.png"),
            "ae56f16f3e4b3a2bfbf5cefbf6ee807482cd8814e30b7496a917b9eae3a5ba72",
        )

    def test_protected_editorial_runtime_is_unchanged(self):
        self.assertEqual(
            self.digest("studio/article_engine.py"),
            "653db77e8881aa6532906fa1b17a8c771152cfe14ef1266383daba423d596868",
        )

    def test_current_status_documents_agree(self):
        for relative in (
            "ROADMAP.md",
            "docs/VERSION_ONE_SCORECARD.md",
            "docs/product/Current_Product_Focus.md",
            "docs/product/Release_v1.0.md",
        ):
            section = managed_section(
                self.text(relative), "RC1_CHECKPOINT_CURRENT_STATUS"
            )
            assert_capability010_complete(section)
            self.assertIn("2026.08.02v13", section, relative)
            self.assertRegex(section, r"Capability 011[^\n]*Complete")
            self.assertIn("Issue #18", section)
            self.assertIn("In Progress", section)
            self.assertIn("B002", section, relative)

    def test_capability010_completion_records_are_current(self):
        roadmap = managed_section(self.text("ROADMAP.md"), "CAPABILITY_010_ROADMAP")
        scorecard = managed_section(
            self.text("docs/VERSION_ONE_SCORECARD.md"), "CAPABILITY_010_SCORECARD"
        )
        assert_capability010_complete(roadmap)
        assert_capability010_complete(scorecard)
        self.assertIn("PR #46", roadmap)
        self.assertIn("issue #16", scorecard)

        adr = self.text("docs/architecture/adr/ADR-016-hero-visual-system.md")
        baseline = self.text(
            "docs/architecture/baselines/Architecture_Baseline_2026.08.02v12.md"
        )
        self.assertRegex(adr, r"## Status\s+Accepted")
        self.assertRegex(baseline, r"## Status\s+Current delivered")

    def test_stale_capability010_status_cannot_validate(self):
        for stale in (
            "Capability 010 - In Progress",
            "Capability 010 - Todo and unstarted",
            "Capability 010 is unstarted",
        ):
            with self.subTest(stale=stale), self.assertRaises(AssertionError):
                assert_capability010_complete(stale)

    def test_readme_product_documentation_links_resolve(self):
        section = self.text("README.md").split("## Product Documentation", 1)[1]
        section = section.split("## Architecture Status", 1)[0]
        links = re.findall(r"\[[^]]+\]\(([^)]+\.md)\)", section)
        self.assertTrue(links)
        for target in links:
            self.assertTrue((ROOT / target).is_file(), target)
        self.assertIn("docs/architecture/Editorial_Context_Model.md", links)

    def test_direct_adr_and_baseline_markdown_links_resolve(self):
        for directory in (
            ROOT / "docs/architecture/adr",
            ROOT / "docs/architecture/baselines",
        ):
            for path in directory.glob("*.md"):
                for target in re.findall(
                    r"\[[^]]+\]\(([^)#]+\.md)\)",
                    path.read_text(encoding="utf-8"),
                ):
                    self.assertTrue(
                        (path.parent / target).resolve().is_file(),
                        f"Broken link: {path} -> {target}",
                    )


if __name__ == "__main__":
    unittest.main()
