from __future__ import annotations

import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RC1CheckpointTests(unittest.TestCase):
    def text(self, relative):
        return (ROOT / relative).read_text(encoding="utf-8")

    def digest(self, relative):
        return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()

    def test_checkpoint_records_reproducible_evidence_and_blockers(self):
        checkpoint = self.text("docs/product/checkpoints/RC1_Checkpoint_2026.08.02.md")
        for phrase in ("b2ffc31b6f7fc366d8e8c3b181a4df93ad0a26bc", "2026.08.02v10", "256 passed", "Engineering readiness", "Complete RC1 readiness", "not achieved", "Capability 010", "Capability 011", "issue #18"):
            self.assertIn(phrase, checkpoint)
        self.assertNotRegex(checkpoint, r"\b\d{1,3}%")

    def test_brand_adoption_is_path_and_hash_verified(self):
        readme = self.text("README.md")
        match = re.search(r'<img src="([^"]+)"', readme)
        self.assertIsNotNone(match)
        self.assertTrue((ROOT / match.group(1)).is_file())
        self.assertEqual(self.digest("assets/brand/logo/master/editorial-compass-mark-master.png"), "b2cd1c22239b7176b43578892b0c37ac502ca5ab696b7c083a0b397bfe285727")
        self.assertEqual(self.digest("assets/brand/logo/master/editorial-compass-lockup-master.png"), "ae56f16f3e4b3a2bfbf5cefbf6ee807482cd8814e30b7496a917b9eae3a5ba72")
        self.assertFalse((ROOT / "assets/brand/review").exists())
        self.assertFalse((ROOT / "assets/brand/logo/source").exists())

    def test_editorial_runtime_is_unchanged(self):
        self.assertEqual(self.digest("studio/article_engine.py"), "653db77e8881aa6532906fa1b17a8c771152cfe14ef1266383daba423d596868")
        self.assertEqual(self.digest("studio/publication_package.py"), "ba3e4bf6e0d92ff088279e8a6a8bf5e74b33845ca8056bd82cf4e1c1eb136500")

    def test_current_status_records_are_reconciled(self):
        for relative in ("ROADMAP.md", "docs/VERSION_ONE_SCORECARD.md", "docs/product/Current_Product_Focus.md", "docs/product/Release_v1.0.md"):
            content = self.text(relative)
            self.assertIn("RC1_CHECKPOINT_CURRENT_STATUS", content)
            self.assertIn("Capability 009", content)
            self.assertIn("Complete", content)
            self.assertIn("Capability 010", content)
            self.assertIn("unstarted", content)
            self.assertIn("2026.08.02v10", content)
        release = self.text("docs/product/Release_v1.0.md")
        self.assertIn("Architecture baseline:\n\n```text\n2026.08.02v10\n```", release)

    def test_adr015_is_indexed_and_baseline_v11_is_proposed(self):
        self.assertIn("ADR-015", self.text("docs/architecture/adr/README.md"))
        baseline = self.text("docs/architecture/baselines/Architecture_Baseline_2026.08.02v11.md")
        self.assertIn("Proposed", baseline)
        self.assertIn("2026.08.02v10", baseline)

    def test_direct_adr_and_baseline_markdown_links_resolve(self):
        for directory in (ROOT / "docs/architecture/adr", ROOT / "docs/architecture/baselines"):
            for path in directory.glob("*.md"):
                for target in re.findall(r"\[[^]]+\]\(([^)#]+\.md)\)", path.read_text(encoding="utf-8")):
                    self.assertTrue((path.parent / target).resolve().is_file(), f"Broken link: {path} -> {target}")


if __name__ == "__main__":
    unittest.main()
