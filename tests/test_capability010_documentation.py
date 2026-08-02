"""Architecture, scope, and generator contracts for Capability 010."""

import hashlib
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = str(ROOT / "scripts")
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)


class Capability010DocumentationTests(unittest.TestCase):
    def content(self, relative):
        return (ROOT / relative).read_text(encoding="utf-8")

    def digest(self, relative):
        return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()

    def test_adr_baseline_architecture_and_demo_exist(self):
        required = (
            "docs/architecture/adr/ADR-016-hero-visual-system.md",
            "docs/architecture/baselines/Architecture_Baseline_2026.08.02v12.md",
            "docs/architecture/Hero_Visual_System.md",
            "docs/demos/Capability-010-Hero-Visual-System.md",
        )
        for relative in required:
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_current_authorities_define_the_narrow_scope(self):
        for relative in (
            "ROADMAP.md",
            "docs/VERSION_ONE_SCORECARD.md",
            "docs/product/Current_Product_Focus.md",
            "docs/product/PRD_v1.3.md",
            "docs/product/Release_v1.0.md",
        ):
            content = self.content(relative)
            self.assertIn("CAPABILITY_010", content)
            self.assertIn("720", content)
            self.assertIn("425", content)
            self.assertIn("Capability 011", content)

    def test_no_deferred_runtime_subsystems_were_added(self):
        forbidden = (
            "studio/portable_editorial_project.py",
            "studio/component_collaboration.py",
            "studio/editorial_orchestrator.py",
            "studio/hero_visual_ui.py",
        )
        for relative in forbidden:
            self.assertFalse((ROOT / relative).exists(), relative)

    def test_article_engine_and_brand_masters_are_unchanged(self):
        self.assertEqual(self.digest("studio/article_engine.py"), "653db77e8881aa6532906fa1b17a8c771152cfe14ef1266383daba423d596868")
        self.assertEqual(self.digest("studio/editorial_workspace.py"), "2bb9a08fc9c11c496f518509019b569ee90d5b89653f08321b8b7d5ab5d1566c")
        self.assertEqual(self.digest("assets/brand/logo/master/editorial-compass-mark-master.png"), "b2cd1c22239b7176b43578892b0c37ac502ca5ab696b7c083a0b397bfe285727")
        self.assertEqual(self.digest("assets/brand/logo/master/editorial-compass-lockup-master.png"), "ae56f16f3e4b3a2bfbf5cefbf6ee807482cd8814e30b7496a917b9eae3a5ba72")

    def test_capability009_bootstrap_preserves_the_integration(self):
        import bootstrap_capability009_article_engine_publication_package as cap009
        import bootstrap_capability010_hero_visual_system as cap010

        live = self.content("studio/publication_package.py")
        self.assertEqual(cap009.FILES["studio/publication_package.py"], live)
        self.assertEqual(cap010.FILES["studio/publication_package.py"], live)


if __name__ == "__main__":
    unittest.main()
