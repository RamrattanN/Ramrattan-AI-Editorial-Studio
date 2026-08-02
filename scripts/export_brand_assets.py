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
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
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
