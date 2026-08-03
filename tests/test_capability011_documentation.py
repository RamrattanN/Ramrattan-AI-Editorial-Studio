"""Architecture, scope, and generator contracts for Capability 011."""

import hashlib
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = str(ROOT / "scripts")
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)


class Capability011DocumentationTests(unittest.TestCase):
    def content(self, relative):
        return (ROOT / relative).read_text(encoding="utf-8")

    def digest(self, relative):
        return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()

    def test_required_contracts_exist(self):
        for relative in (
            "studio/portable_editorial_project.py",
            "scripts/bootstrap_capability011_portable_editorial_project.py",
            "docs/architecture/adr/ADR-017-portable-editorial-project-resume-export.md",
            "docs/architecture/baselines/Architecture_Baseline_2026.08.02v13.md",
            "docs/demos/Capability-011-Portable-Editorial-Project.md",
        ):
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_delivery_status_is_current(self):
        adr = self.content(
            "docs/architecture/adr/ADR-017-portable-editorial-project-resume-export.md"
        )
        baseline = self.content(
            "docs/architecture/baselines/Architecture_Baseline_2026.08.02v13.md"
        )
        for content in (adr, baseline):
            self.assertIn("7962d140eabf28e492a3aca935f1e622e9ebc21a", content)
            self.assertIn("PR #50", content)
            self.assertNotIn("Proposed during Capability 011", content)
        self.assertIn("Accepted", adr)
        self.assertIn("Current delivered architecture baseline", baseline)

    def test_prd_and_architecture_narrow_the_legacy_schema(self):
        for relative in (
            "docs/product/PRD_v1.3.md",
            "docs/architecture/Portable_Editorial_Project.md",
            "docs/architecture/adr/ADR-017-portable-editorial-project-resume-export.md",
        ):
            content = self.content(relative)
            self.assertIn("RC1", content)
            self.assertIn("current runtime", content)
            self.assertIn("fabricat", content)
            self.assertIn("Adaptive Editorial Context", content)

    def test_no_deferred_runtime_is_introduced(self):
        forbidden = (
            "studio/adaptive_editorial_context.py",
            "studio/component_collaboration.py",
            "studio/editorial_orchestrator.py",
            "studio/hero_visual_ui.py",
        )
        for relative in forbidden:
            self.assertFalse((ROOT / relative).exists(), relative)

    def test_protected_runtime_and_brand_masters_are_unchanged(self):
        expected = {
            "studio/article_engine.py": "653db77e8881aa6532906fa1b17a8c771152cfe14ef1266383daba423d596868",
            "studio/editorial_workspace.py": "2bb9a08fc9c11c496f518509019b569ee90d5b89653f08321b8b7d5ab5d1566c",
            "assets/brand/logo/master/editorial-compass-mark-master.png": "b2cd1c22239b7176b43578892b0c37ac502ca5ab696b7c083a0b397bfe285727",
            "assets/brand/logo/master/editorial-compass-lockup-master.png": "ae56f16f3e4b3a2bfbf5cefbf6ee807482cd8814e30b7496a917b9eae3a5ba72",
        }
        for relative, digest in expected.items():
            self.assertEqual(self.digest(relative), digest, relative)

    def test_every_publication_package_owner_matches_live_file(self):
        import bootstrap_capability009_article_engine_publication_package as cap009
        import bootstrap_capability010_hero_visual_system as cap010
        import bootstrap_capability011_portable_editorial_project as cap011

        live = self.content("studio/publication_package.py")
        self.assertEqual(cap009.FILES["studio/publication_package.py"], live)
        self.assertEqual(cap010.FILES["studio/publication_package.py"], live)
        self.assertEqual(cap011.FILES["studio/publication_package.py"], live)

    def test_current_records_keep_capability_011_active(self):
        for relative in (
            "ROADMAP.md",
            "docs/VERSION_ONE_SCORECARD.md",
            "docs/product/Current_Product_Focus.md",
            "docs/product/Release_v1.0.md",
        ):
            content = self.content(relative)
            self.assertIn("Capability 011", content)
            self.assertIn("In Progress", content)
            self.assertIn("2026.08.02v13", content)


if __name__ == "__main__":
    unittest.main()
