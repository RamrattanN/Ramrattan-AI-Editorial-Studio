"""Documentation tests for the Capability 008 continuation."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class EvidenceDocumentationTests(unittest.TestCase):
    def content(self, relative):
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_runtime_architecture_records_verification_boundary(self):
        content = self.content("docs/architecture/Evidence_Validation_Runtime.md")
        self.assertIn("independent source groups", content)
        normalized = " ".join(content.split())
        self.assertIn("must never fabricate", normalized)

    def test_adr_and_baseline_exist(self):
        self.assertTrue((ROOT / "docs/architecture/adr/ADR-010-implement-evidence-validation-and-editorial-risk.md").is_file())
        self.assertIn(
            "2026.08.01v06",
            self.content("docs/architecture/baselines/Architecture_Baseline_2026.08.01v06.md"),
        )

    def test_canonical_vocabulary_is_extended(self):
        content = self.content("docs/constitution/Canonical_Vocabulary.md")
        self.assertIn("Claim Classification", content)
        self.assertIn("Editorial Confidence", content)

    def test_roadmap_records_increment_complete(self):
        content = self.content("ROADMAP.md")
        self.assertIn("[x] Evidence Validation", content)
        self.assertIn("[x] LMHS Editorial Risk", content)


if __name__ == "__main__":
    unittest.main()
