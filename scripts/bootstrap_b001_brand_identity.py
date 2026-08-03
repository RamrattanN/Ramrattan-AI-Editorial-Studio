#!/usr/bin/env python3
"""Bootstrap Initiative B001 Pass 2 - adopt approved RC1 brand masters.

The Repository Author supplies the masters. This bootstrap verifies but never
writes them, generates only proportional PNG derivatives, synchronizes direct
brand records, and runs complete repository validation.
"""

from __future__ import annotations

import argparse
import hashlib
import shlex
import struct
import subprocess
import sys
import textwrap
from pathlib import Path


EXPECTED_REPOSITORY = "Ramrattan-AI-Editorial-Studio"
EXPECTED_REMOTE = "RamrattanN/Ramrattan-AI-Editorial-Studio"
EXPECTED_BRANCH = "feature/b001-brand-identity-visual-assets"
SCRIPT_PATH = "scripts/bootstrap_b001_brand_identity.py"
SHOWCASE = "assets/brand/concepts/Ramrattan AI Editorial Brand Showcase.png"
SHOWCASE_SHA256 = "04fd06b27d357b849b9c3d1e2fa02d7da0042395ca9f8bdd98f1a0d548beedc0"
MARK_MASTER = "assets/brand/logo/master/editorial-compass-mark-master.png"
MARK_SHA256 = "b2cd1c22239b7176b43578892b0c37ac502ca5ab696b7c083a0b397bfe285727"
MARK_DIMENSIONS = (1254, 1254)
LOCKUP_MASTER = "assets/brand/logo/master/editorial-compass-lockup-master.png"
LOCKUP_SHA256 = "ae56f16f3e4b3a2bfbf5cefbf6ee807482cd8814e30b7496a917b9eae3a5ba72"
LOCKUP_DIMENSIONS = (1717, 916)
MARK_SIZES = (1024, 512, 256, 128, 64, 32)
FAVICON_SIZE = 16
LOCKUP_WIDTHS = (1600, 1200, 800, 400)
ROADMAP_MARKER = "INITIATIVE_B001_BRAND_IDENTITY"
README_MARKER = "INITIATIVE_B001_BRAND_LOCKUP"


class BootstrapError(RuntimeError):
    """Raised when B001 Pass 2 cannot proceed safely."""


def clean(value: str) -> str:
    return textwrap.dedent(value).strip() + "\n"


BRAND_README = clean(
    '''
    # Ramrattan AI Editorial Studio Brand Assets

    ## Authority

    `logo/master/` contains the authoritative Repository Author-supplied RC1
    raster masters. `logo/exports/` contains deterministic proportional PNG
    derivatives. The masters are verified by recorded SHA-256 hashes and are
    never generated or overwritten by repository tooling.

    `concepts/Ramrattan AI Editorial Brand Showcase.png` is design provenance
    only. It is not production artwork or an export source.

    ## RC1 Identity

    The official standalone mark combines a shield, metallic R, and golden quill.
    The official horizontal lockup combines that mark with the RAMRATTAN AI and
    EDITORIAL STUDIO wordmark. Both approved masters are opaque RGB PNG files
    with baked white-to-light-grey backgrounds and no alpha channel.

    ## Canonical Inventory

    - `logo/master/editorial-compass-mark-master.png` — square official mark
    - `logo/master/editorial-compass-lockup-master.png` — horizontal official lockup
    - `logo/master/README.md` — immutable-master contract and approved hashes
    - `logo/exports/` — proportional PNG derivatives only

    ## Usage

    Use the lockup for wide README, documentation, demo, and release-note display.
    Use the mark for square icons and compact brand contexts. Do not recolour,
    crop internally, trace, simplify, reconstruct, or create unapproved variants.
    The 16-pixel favicon is a proportional reduction of the approved raster mark;
    its shield, R, and quill detail is necessarily limited at that size.

    ## Supporting Records

    - `palette.md` records the colours represented by the approved identity.
    - `typography.md` records the raster-wordmark constraint.
    - `prompts/` preserves design provenance only and does not generate masters.

    ## Version History

    - `2026-08-02 — RC1`: adopted the Repository Author-supplied shield, metallic
      R, and golden quill masters and generated proportional repository exports.
    '''
)


PALETTE = clean(
    '''
    # RC1 Brand Palette

    | Name | Hex | Identity relationship |
    |---|---|---|
    | Deep Editorial Navy | `#1B263B` | Shield and primary wordmark relationship |
    | Warm Ivory | `#F8F6F2` | Light editorial field relationship |
    | Warm Copper | `#B7791F` | Golden quill and lockup accent relationship |
    | Slate | `#4A5568` | Supporting neutral relationship |

    These values document the approved identity relationship; they do not
    authorize recolouring or reconstructing the raster masters. The approved
    RC1 masters must be used exactly as supplied.
    '''
)


TYPOGRAPHY = clean(
    '''
    # RC1 Brand Typography

    The approved horizontal master contains the authoritative RAMRATTAN AI and
    EDITORIAL STUDIO wordmark as raster artwork. Its typography must not be
    reconstructed, substituted, traced, redrawn, or re-typeset by an
    Implementation Agent.

    No font files are added, bundled, or distributed by B001. Supporting product
    and documentation typography may use restrained repository-safe system
    fallbacks, but those recommendations do not alter the approved lockup.
    '''
)


PROVENANCE = clean(
    '''
    # RC1 Brand Provenance

    `assets/brand/concepts/Ramrattan AI Editorial Brand Showcase.png` remains
    design provenance only. The Repository Author subsequently supplied two
    human-approved RC1 raster PNG masters: the shield, metallic R, and golden
    quill mark, and the corresponding Ramrattan AI Editorial Studio lockup.

    This record is not an instruction for Codex to generate, reconstruct, trace,
    or reinterpret artwork. Authoritative masters belong in
    `assets/brand/logo/master/`; proportional derived PNGs belong in
    `assets/brand/logo/exports/`.
    '''
)


MASTER_README = clean(
    '''
    # Authoritative RC1 Brand Masters

    This folder contains the authoritative human-approved RC1 brand masters.

    ## Canonical Masters

    ### `editorial-compass-mark-master.png`

    Official standalone mark: shield, metallic R, and golden quill.

    - Format: PNG, 8-bit RGB, non-interlaced
    - Dimensions: 1254 × 1254 pixels
    - Colour mode: RGB without an embedded profile
    - Transparency: none; no alpha channel
    - Background: baked opaque white-to-light-grey raster background
    - SHA-256: `b2cd1c22239b7176b43578892b0c37ac502ca5ab696b7c083a0b397bfe285727`

    ### `editorial-compass-lockup-master.png`

    Official horizontal lockup: approved mark with the RAMRATTAN AI and
    EDITORIAL STUDIO wordmark.

    - Format: PNG, 8-bit RGB, non-interlaced
    - Dimensions: 1717 × 916 pixels
    - Colour mode: RGB without an embedded profile
    - Transparency: none; no alpha channel
    - Background: baked opaque white-to-light-grey raster background
    - SHA-256: `ae56f16f3e4b3a2bfbf5cefbf6ee807482cd8814e30b7496a917b9eae3a5ba72`

    ## Protection Contract

    Both masters are Repository Author-supplied raster PNGs. Implementation
    Agents must not redesign, reinterpret, redraw, recolour, retouch, crop
    internally, optimize, trace, vectorize, rename, overwrite, or otherwise alter
    them. Permitted processing is limited to proportional resizing and canvas
    fitting without distortion or clipping. Derived assets belong only in
    `assets/brand/logo/exports/`.

    Rejected artwork must not remain in the current repository tree. Git history
    preserves prior artwork. Replacing either master requires explicit Repository
    Author or authorized Repository Maintainer approval.

    B002 — Brand Identity Refinement is a future post-RC1 evolutionary refinement
    only. It does not authorize redesign or master alteration during B001.
    '''
)


DESIGN_BRIEF = clean(
    '''
    # Brand Design Brief — RC1 Identity

    ## Status

    Initiative B001 Pass 2 adopts the Repository Author-supplied RC1 brand
    identity. The masters are immutable raster PNG inputs verified by hash.

    ## Canonical Identity

    - **Shield:** protection, institutional trust, and process integrity.
    - **Metallic R:** Ramrattan authorship and a premium editorial signature.
    - **Golden quill:** writing, editorial craft, judgement, and publication.
    - **Horizontal lockup:** approved mark with RAMRATTAN AI and EDITORIAL STUDIO.

    The Brand Showcase remains design provenance only and is not a production
    source. Current operational identity is defined exclusively by the two files
    in `assets/brand/logo/master/`.

    ## Master and Export Contract

    Masters may not be redesigned, reconstructed, recoloured, retouched, traced,
    vectorized, internally cropped, optimized, or overwritten. Repository tooling
    verifies their hashes before and after generating proportional PNG derivatives
    under `assets/brand/logo/exports/`.

    ## Format and Background

    Both masters are opaque 8-bit RGB PNGs with no alpha channel, no embedded
    colour profile, and a baked white-to-light-grey background. Documentation
    must not claim transparency. No dark, light, monochrome, SVG, or transparent
    variant is approved in B001.

    ## Usage

    Use the lockup for wide display and the standalone mark for square/icon use.
    The 16-pixel favicon is a proportional mechanical reduction; fine metallic R
    and quill details are expected to be visually limited. Do not simplify or
    redraw it during B001.

    ## Future Refinement

    B002 may explore a flatter vector-first system after RC1 while preserving the
    established shield, R, and quill identity. B002 does not block Capability 009
    and does not authorize B001 redesign.

    ## Version History

    - `2026-08-02 — RC1`: adopted approved raster masters and proportional exports.
    '''
)


EXPORT_SCRIPT = clean(
    '''
    #!/usr/bin/env python3
    """Generate deterministic proportional PNG exports from immutable RC1 masters."""

    from __future__ import annotations

    import argparse
    import hashlib
    import shutil
    import struct
    import subprocess
    from pathlib import Path


    ROOT = Path(__file__).resolve().parents[1]
    MASTER_DIRECTORY = ROOT / "assets/brand/logo/master"
    EXPORT_DIRECTORY = ROOT / "assets/brand/logo/exports"
    MARK_MASTER = MASTER_DIRECTORY / "editorial-compass-mark-master.png"
    LOCKUP_MASTER = MASTER_DIRECTORY / "editorial-compass-lockup-master.png"
    MARK_SHA256 = "b2cd1c22239b7176b43578892b0c37ac502ca5ab696b7c083a0b397bfe285727"
    LOCKUP_SHA256 = "ae56f16f3e4b3a2bfbf5cefbf6ee807482cd8814e30b7496a917b9eae3a5ba72"
    MARK_DIMENSIONS = (1254, 1254)
    LOCKUP_DIMENSIONS = (1717, 916)
    MARK_SIZES = (1024, 512, 256, 128, 64, 32)
    FAVICON_SIZE = 16
    LOCKUP_WIDTHS = (1600, 1200, 800, 400)
    CONTROL_FILES: set[str] = set()


    def sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()


    def png_properties(path: Path) -> tuple[int, int, int, int]:
        data = path.read_bytes()
        if data[:8] != b"\\x89PNG\\r\\n\\x1a\\n" or data[12:16] != b"IHDR":
            raise RuntimeError(f"Not a valid PNG: {path}")
        width, height = struct.unpack(">II", data[16:24])
        return width, height, data[24], data[25]


    def verify_masters() -> dict[Path, str]:
        required = {
            MARK_MASTER: (MARK_SHA256, MARK_DIMENSIONS),
            LOCKUP_MASTER: (LOCKUP_SHA256, LOCKUP_DIMENSIONS),
        }
        hashes = {}
        for path, (expected_hash, expected_dimensions) in required.items():
            if not path.is_file():
                raise RuntimeError(f"Approved RC1 master is missing: {path.name}")
            actual_hash = sha256(path)
            if actual_hash != expected_hash:
                raise RuntimeError(f"Approved RC1 master hash changed: {path.name}")
            width, height, bit_depth, colour_type = png_properties(path)
            if (width, height) != expected_dimensions:
                raise RuntimeError(f"Approved RC1 master dimensions changed: {path.name}")
            if (bit_depth, colour_type) != (8, 2):
                raise RuntimeError(f"Approved RC1 master must remain opaque 8-bit RGB: {path.name}")
            hashes[path] = actual_hash
        return hashes


    def scaled_height(width: int) -> int:
        source_width, source_height = LOCKUP_DIMENSIONS
        return source_height * width // source_width


    def expected_exports() -> dict[Path, tuple[int, int]]:
        exports = {
            EXPORT_DIRECTORY / f"editorial-compass-mark-{size}.png": (size, size)
            for size in MARK_SIZES
        }
        exports[EXPORT_DIRECTORY / "editorial-compass-favicon-16.png"] = (
            FAVICON_SIZE, FAVICON_SIZE
        )
        exports.update({
            EXPORT_DIRECTORY / f"editorial-compass-lockup-{width}.png": (
                width, scaled_height(width)
            )
            for width in LOCKUP_WIDTHS
        })
        return exports


    def run_sips(arguments: list[str]) -> None:
        result = subprocess.run(arguments, text=True, capture_output=True, check=False)
        if result.returncode:
            raise RuntimeError(result.stderr.strip() or result.stdout.strip())


    def export() -> None:
        before = verify_masters()
        resampler = shutil.which("sips")
        if resampler is None:
            raise RuntimeError("Deterministic PNG export requires the available sips tool.")
        EXPORT_DIRECTORY.mkdir(parents=True, exist_ok=True)
        for size in (*MARK_SIZES, FAVICON_SIZE):
            name = (
                "editorial-compass-favicon-16.png" if size == FAVICON_SIZE
                else f"editorial-compass-mark-{size}.png"
            )
            run_sips([
                resampler, "-s", "format", "png", "--resampleHeightWidth",
                str(size), str(size), str(MARK_MASTER), "--out",
                str(EXPORT_DIRECTORY / name),
            ])
        for width in LOCKUP_WIDTHS:
            run_sips([
                resampler, "-s", "format", "png", "--resampleWidth", str(width),
                str(LOCKUP_MASTER), "--out",
                str(EXPORT_DIRECTORY / f"editorial-compass-lockup-{width}.png"),
            ])
        after = verify_masters()
        if before != after:
            raise RuntimeError("Approved RC1 master changed during export.")
        verify_exports()


    def verify_exports() -> None:
        verify_masters()
        expected = expected_exports()
        for path, dimensions in expected.items():
            if not path.is_file():
                raise RuntimeError(f"Required RC1 export is missing: {path.name}")
            width, height, bit_depth, colour_type = png_properties(path)
            if (width, height) != dimensions:
                raise RuntimeError(
                    f"Unexpected dimensions for {path.name}: {(width, height)} != {dimensions}"
                )
            if (bit_depth, colour_type) != (8, 2):
                raise RuntimeError(f"RC1 export must remain opaque 8-bit RGB: {path.name}")
        extras = {
            path.name for path in EXPORT_DIRECTORY.iterdir()
            if path.is_file() and path.name not in CONTROL_FILES and path not in expected
        }
        if extras:
            raise RuntimeError("Unexpected RC1 exports: " + ", ".join(sorted(extras)))


    def main() -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument("--check", action="store_true")
        args = parser.parse_args()
        try:
            if args.check:
                verify_exports()
            else:
                export()
            return 0
        except (OSError, RuntimeError) as exc:
            print(f"ERROR: {exc}")
            return 1


    if __name__ == "__main__":
        raise SystemExit(main())
    '''
)


TESTS = clean(
    '''
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
        if data[:8] != b"\\x89PNG\\r\\n\\x1a\\n" or data[12:16] != b"IHDR":
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
    '''
)


ROADMAP_BLOCK = clean(
    '''
    ## Initiative B001 - Brand Identity & Visual Assets

    Status: **In Progress**

    B001 adopts the Repository Author-supplied RC1 shield, metallic R, and golden
    quill mark plus the approved Ramrattan AI Editorial Studio horizontal lockup.
    Immutable raster masters live in `assets/brand/logo/master/`; proportional
    derivatives live in `assets/brand/logo/exports/`.

    **B002 - Brand Identity Refinement** is a Low-priority, Post-RC1 evolutionary
    refinement and does not block Capability 009. Capability 009 remains Todo and
    has not started.
    '''
)


README_BLOCK = clean(
    '''
    <p align="center">
      <img src="assets/brand/logo/exports/editorial-compass-lockup-1200.png"
           alt="Ramrattan AI Editorial Studio shield with metallic R and golden quill"
           width="800">
    </p>
    '''
)


FILES = {
    "assets/brand/README.md": BRAND_README,
    "assets/brand/palette.md": PALETTE,
    "assets/brand/typography.md": TYPOGRAPHY,
    "assets/brand/prompts/editorial-compass-construction.md": PROVENANCE,
    "assets/brand/logo/master/README.md": MASTER_README,
    "docs/brand/Brand_Design_Brief.md": DESIGN_BRIEF,
    "scripts/export_brand_assets.py": EXPORT_SCRIPT,
    "tests/test_b001_brand_assets.py": TESTS,
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise BootstrapError(f"Not a valid PNG: {path}")
    return struct.unpack(">II", data[16:24])


def output(command: list[str], *, cwd: Path) -> str:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=True)
    return result.stdout.strip()


def repository_root() -> Path:
    root = Path(output(["git", "rev-parse", "--show-toplevel"], cwd=Path.cwd())).resolve()
    if root.name != EXPECTED_REPOSITORY:
        raise BootstrapError(f"Expected {EXPECTED_REPOSITORY}, found {root.name}.")
    remote = output(["git", "remote", "get-url", "origin"], cwd=root)
    if EXPECTED_REMOTE not in remote:
        raise BootstrapError("Origin does not match the expected repository.")
    return root


def lockup_height(width: int) -> int:
    return LOCKUP_DIMENSIONS[1] * width // LOCKUP_DIMENSIONS[0]


def export_paths() -> set[str]:
    paths = {
        f"assets/brand/logo/exports/editorial-compass-mark-{size}.png"
        for size in MARK_SIZES
    }
    paths.add("assets/brand/logo/exports/editorial-compass-favicon-16.png")
    paths.update(
        f"assets/brand/logo/exports/editorial-compass-lockup-{width}.png"
        for width in LOCKUP_WIDTHS
    )
    return paths


def expected_paths() -> set[str]:
    return set(FILES) | export_paths() | {
        SCRIPT_PATH, SHOWCASE, MARK_MASTER, LOCKUP_MASTER, "ROADMAP.md", "README.md"
    }


def status_path(line: str) -> str:
    parsed = shlex.split(line[3:].strip())
    return parsed[0] if parsed else ""


def verify_masters(root: Path) -> None:
    required = {
        MARK_MASTER: (MARK_SHA256, MARK_DIMENSIONS),
        LOCKUP_MASTER: (LOCKUP_SHA256, LOCKUP_DIMENSIONS),
    }
    for relative, (expected_hash, expected_dimensions) in required.items():
        path = root / relative
        if not path.is_file():
            raise BootstrapError(f"Approved RC1 master is missing: {relative}")
        if sha256(path) != expected_hash:
            raise BootstrapError(f"Approved RC1 master hash changed: {relative}")
        if png_dimensions(path) != expected_dimensions:
            raise BootstrapError(f"Approved RC1 master dimensions changed: {relative}")


def verify_state(root: Path) -> None:
    branch = output(["git", "branch", "--show-current"], cwd=root)
    if branch != EXPECTED_BRANCH:
        raise BootstrapError(f"Expected {EXPECTED_BRANCH}, found {branch}.")
    status = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=root, text=True, capture_output=True, check=True,
    ).stdout.splitlines()
    unexpected = [line for line in status if status_path(line) not in expected_paths()
                  and Path(status_path(line)).name != ".DS_Store"]
    if unexpected:
        raise BootstrapError("Unexpected working-tree changes:\n" + "\n".join(unexpected))
    verify_masters(root)


def managed_block(marker: str, content: str) -> str:
    return f"<!-- {marker}_START -->\n\n{content.rstrip()}\n\n<!-- {marker}_END -->"


def update_managed_block(path: Path, marker: str, content: str, *, after_heading: bool = False) -> None:
    original = path.read_text(encoding="utf-8")
    start = f"<!-- {marker}_START -->"
    end = f"<!-- {marker}_END -->"
    if (start in original) != (end in original):
        raise BootstrapError(f"Incomplete {marker} marker pair.")
    block = managed_block(marker, content)
    if start in original:
        before = original.split(start, 1)[0].rstrip()
        after = original.split(end, 1)[1].lstrip()
        updated = before + "\n\n" + block
        if after:
            updated += "\n\n" + after
    elif after_heading:
        first, remainder = original.split("\n", 1)
        updated = first.rstrip() + "\n\n" + block + "\n\n" + remainder.lstrip()
    else:
        updated = original.rstrip() + "\n\n" + block
    path.write_text(updated.rstrip() + "\n", encoding="utf-8")


def remove_incidental_metadata(root: Path) -> None:
    for path in (root / "assets/brand").rglob(".DS_Store"):
        path.unlink()
        print(f"Removed {path.relative_to(root)}")


def apply(root: Path) -> None:
    before = {MARK_MASTER: sha256(root / MARK_MASTER), LOCKUP_MASTER: sha256(root / LOCKUP_MASTER)}
    remove_incidental_metadata(root)
    for relative, content in FILES.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"Wrote {relative}")
    update_managed_block(root / "ROADMAP.md", ROADMAP_MARKER, ROADMAP_BLOCK)
    update_managed_block(root / "README.md", README_MARKER, README_BLOCK, after_heading=True)
    subprocess.run([sys.executable, "scripts/export_brand_assets.py"], cwd=root, check=True)
    verify_masters(root)
    after = {MARK_MASTER: sha256(root / MARK_MASTER), LOCKUP_MASTER: sha256(root / LOCKUP_MASTER)}
    if before != after:
        raise BootstrapError("Approved RC1 master changed during Pass 2 apply.")


def validate(root: Path) -> None:
    for relative, expected in FILES.items():
        if (root / relative).read_text(encoding="utf-8") != expected:
            raise BootstrapError(f"Generated artifact differs from bootstrap: {relative}")
    verify_masters(root)
    if sha256(root / SHOWCASE) != SHOWCASE_SHA256:
        raise BootstrapError("The Brand Showcase provenance changed.")
    if (root / "assets/brand/review").exists() or (root / "assets/brand/logo/source").exists():
        raise BootstrapError("Superseded artwork directories remain.")
    if list((root / "assets/brand").rglob(".DS_Store")):
        raise BootstrapError("Incidental .DS_Store metadata remains in the B001 tree.")
    subprocess.run([sys.executable, "scripts/export_brand_assets.py", "--check"], cwd=root, check=True)
    subprocess.run([sys.executable, "-m", "compileall", "-q", "studio", "scripts", "tests"], cwd=root, check=True)
    subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=root, check=True)
    subprocess.run([sys.executable, "studio.py", "validate"], cwd=root, check=True)


def preview() -> None:
    print("Initiative B001 Pass 2 preview:\n")
    print("Immutable Repository Author-supplied masters:")
    print(f"  - {MARK_MASTER}")
    print(f"  - {LOCKUP_MASTER}")
    print("Generated proportional PNG exports:")
    for relative in sorted(export_paths()):
        print(f"  - {relative}")
    print("Synchronized direct records:")
    for relative in FILES:
        print(f"  - {relative}")
    print("  - README.md")
    print("  - ROADMAP.md")
    print("\nMasters are verified before and after export and are never written.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap Initiative B001 Pass 2 RC1 adoption.")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        root = repository_root()
        verify_state(root)
        if args.apply:
            apply(root)
            validate(root)
            subprocess.run(["git", "status", "--short"], cwd=root, check=True)
        else:
            preview()
        return 0
    except (BootstrapError, subprocess.CalledProcessError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
