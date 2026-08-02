"""Contracts for Initiative B001 approved RC1 brand adoption."""

from __future__ import annotations

import hashlib
import runpy
import struct
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BRAND = ROOT / "assets/brand"
MASTER = BRAND / "logo/master"
EXPORTS = BRAND / "logo/exports"
SHOWCASE = BRAND / "concepts/Ramrattan AI Editorial Brand Showcase.png"
MARK_MASTER = MASTER / "editorial-compass-mark-master.png"
LOCKUP_MASTER = MASTER / "editorial-compass-lockup-master.png"
SHOWCASE_SHA256 = "04fd06b27d357b849b9c3d1e2fa02d7da0042395ca9f8bdd98f1a0d548beedc0"
MARK_SHA256 = "b2cd1c22239b7176b43578892b0c37ac502ca5ab696b7c083a0b397bfe285727"
LOCKUP_SHA256 = "ae56f16f3e4b3a2bfbf5cefbf6ee807482cd8814e30b7496a917b9eae3a5ba72"
MARK_SIZES = (1024, 512, 256, 128, 64, 32)
LOCKUP_WIDTHS = (1600, 1200, 800, 400)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def png_properties(path: Path) -> tuple[int, int, int, int]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise AssertionError(f"Invalid PNG: {path}")
    width, height = struct.unpack(">II", data[16:24])
    return width, height, data[24], data[25]


def lockup_height(width: int) -> int:
    return 916 * width // 1717


class BrandRC1Tests(unittest.TestCase):
    def test_approved_masters_match_hash_dimension_and_mode(self) -> None:
        expected = {
            MARK_MASTER: (MARK_SHA256, (1254, 1254)),
            LOCKUP_MASTER: (LOCKUP_SHA256, (1717, 916)),
        }
        for path, (expected_hash, dimensions) in expected.items():
            self.assertEqual(sha256(path), expected_hash, path.name)
            width, height, bit_depth, colour_type = png_properties(path)
            self.assertEqual((width, height), dimensions)
            self.assertEqual((bit_depth, colour_type), (8, 2))

    def test_master_contract_records_protection_and_properties(self) -> None:
        contract = (MASTER / "README.md").read_text(encoding="utf-8")
        for term in (
            "shield, metallic R, and golden quill",
            MARK_SHA256,
            LOCKUP_SHA256,
            "Transparency: none",
            "Repository Author",
            "Repository Maintainer",
            "B002",
        ):
            self.assertIn(term, contract)

    def test_required_mark_exports_have_exact_dimensions(self) -> None:
        for size in MARK_SIZES:
            path = EXPORTS / f"editorial-compass-mark-{size}.png"
            self.assertEqual(png_properties(path)[:2], (size, size), path.name)
        favicon = EXPORTS / "editorial-compass-favicon-16.png"
        self.assertEqual(png_properties(favicon)[:2], (16, 16))

    def test_lockup_exports_preserve_aspect_ratio(self) -> None:
        for width in LOCKUP_WIDTHS:
            path = EXPORTS / f"editorial-compass-lockup-{width}.png"
            dimensions = png_properties(path)[:2]
            self.assertEqual(dimensions, (width, lockup_height(width)), path.name)
            self.assertLessEqual(abs(dimensions[0] / dimensions[1] - 1717 / 916), .01)

    def test_no_rejected_candidate_or_svg_artwork_remains(self) -> None:
        self.assertFalse((BRAND / "review").exists())
        self.assertFalse((BRAND / "logo/source").exists())
        self.assertEqual(list((BRAND / "logo").rglob("*.svg")), [])
        self.assertEqual(list(BRAND.rglob(".DS_Store")), [])

    def test_brand_showcase_remains_design_provenance(self) -> None:
        self.assertEqual(sha256(SHOWCASE), SHOWCASE_SHA256)
        brief = (ROOT / "docs/brand/Brand_Design_Brief.md").read_text(encoding="utf-8")
        self.assertIn("design provenance only", brief)
        for term in ("Shield", "Metallic R", "Golden quill"):
            self.assertIn(term, brief)

    def test_root_readme_uses_existing_horizontal_export(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        relative = "assets/brand/logo/exports/editorial-compass-lockup-1200.png"
        self.assertIn(relative, readme)
        self.assertIn("shield with metallic R and golden quill", readme)
        self.assertTrue((ROOT / relative).is_file())

    def test_bootstrap_never_owns_or_writes_master_images(self) -> None:
        namespace = runpy.run_path(str(ROOT / "scripts/bootstrap_b001_brand_identity.py"))
        managed = namespace["FILES"]
        self.assertNotIn(str(MARK_MASTER.relative_to(ROOT)), managed)
        self.assertNotIn(str(LOCKUP_MASTER.relative_to(ROOT)), managed)
        self.assertEqual(namespace["MARK_SHA256"], MARK_SHA256)
        self.assertEqual(namespace["LOCKUP_SHA256"], LOCKUP_SHA256)

    def test_export_contract_is_green(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/export_brand_assets.py", "--check"],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_roadmap_records_b002_without_starting_capability009(self) -> None:
        roadmap = (ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        self.assertIn("B002 - Brand Identity Refinement", roadmap)
        self.assertIn("Post-RC1", roadmap)
        self.assertIn("does not block Capability 009", roadmap)
        normalized = " ".join(roadmap.split())
        self.assertIn("Capability 009 remains Todo and has not started", normalized)


if __name__ == "__main__":
    unittest.main()
