#!/usr/bin/env python3
"""Deterministically generate and validate V11-01 owned artifacts."""

from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import subprocess
import sys
from pathlib import Path


EXPECTED_REPOSITORY = "Ramrattan-AI-Editorial-Studio"
EXPECTED_BRANCH = "feature/v11-01-author-journey-foundation"
SCRIPT_PATH = "scripts/bootstrap_v11_01_author_journey_foundation.py"
SENTINEL = "V11_01_AUTHOR_JOURNEY_FOUNDATION_COMPLETE"

_BLOBS = {
    "studio/author_journey.py": "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",
    "tests/test_v11_01_author_journey.py": "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",
    "docs/architecture/V11_01_Author_Journey_Foundation.md": "H4sICMk4cmoAA1YxMV8wMV9BdXRob3JfSm91cm5leV9Gb3VuZGF0aW9uLm1kAIVUX2/aMBB/96c4ideQNa20Vt0T6mhHV5UJKtCehnEuxJtjR/aFKt9+55gCrSbtzbk4d/f7lxGsimJ8UcCko9p5eHSdt9jDvetsKUk7K8RoBEuS1AUhZk1rsEFLwytQzpKXiqDiTx80feu2MAuhQxhdX+TDl4vOkm4Q3KtFH2rdCrEJ1JXafZLDyF+/08i87TfxVgCqETy2Lmhyvh8HXSKg9IaPGML5XBHnrtEo12AGUy728ENSncGds5XedT7t+eRkmcHa+T+Vca+wRIMqvshA2jLOE2WcTB5lA951pO0OAj8EwEBya3SosYRtf2ArhxnBq5dtyGDbEZQOA1hHcW0jFQpeq3GlrvpsQLNi6HGPIr+AzbSMuLQ0y4RmAz5xlAibKIUtSasQGtm2vIkQ4zNsb/vdwuRuPH1+WfwcF9npfHl2vjo73+Tc5XE5f/5AzV4anYQeuDgwPA7KtYzYM3yXbt4KiN3u5s/3s4dxwbh4kV19VrsZOpzdufrHpeJzXOQoBbOEPPSgB7g9enCWS+ywSICqtcUB6nq++H7/NF/zaB6TljnWLmPTJflOEQMzILcBI4OuAhWpNEYmvZVBabs2gyD3mOSXnnQVTbxDtug51qfpZDV9DzWVrliqF9Y1OVjHNOwRtljLvWbpPTZSs5G1HdTfRVQ2WurkgwJa70pedwAjPeMkjMsjm0l1MWIhh5daB6i0iXlQzpfc8n0Aj6lKRma1RAwGyq02mnqm0vTJVl+xQu+xTLbmEC4w8BhYHfXfAA+TR/uT9DukocOXZPvrFE9NERnhLnGVi5OjYclZVvjfTpenTm+k5YdoiWOWjlABNdPoD32iaD2wnlz58NMaTJMBV/iK4Cf+hZnopriuZ405Yn8B5xBEDvEEAAA=",
}

FILES = {
    path: gzip.decompress(base64.b64decode(blob)).decode("utf-8").rstrip() + "\n"
    for path, blob in _BLOBS.items()
}

# V11_02_EDITORIAL_SOURCE_BRANDING_OWNER_SYNC_START
from bootstrap_v11_02_editorial_source_branding import (
    AUTHOR_JOURNEY as _v11_02_author_journey,
)

FILES["studio/author_journey.py"] = _v11_02_author_journey
# V11_02_EDITORIAL_SOURCE_BRANDING_OWNER_SYNC_END

PROTECTED_HASHES = {
    "studio/workflow/README.md": "2f98daa4f2f4760bd72c36867de1658a120bad5b06ab3348dad717f534eb3211",
    "studio/workflow/__init__.py": "9ac599af687b85520dcb0719fee72ed9d40f2cdc4e7e8dc825f8a7f1354a47e0",
    "studio/workflow/choices.py": "47cafc01797a57443ebbff5bb842cb82abb59fbe8a2f3d53dd2d5f752000c97d",
    "studio/workflow/state.py": "da7499c0a7759deebf8a396f7f290ca44a1ea322b048386e33edf0acbe4cf359",
    "studio/workflow/workflow.py": "2c34e2991a6115b583d9707a95f0b2d547ade31aa2f92dd84479189fbae2ab15",
    "scripts/bootstrap_sprint2_workflow.py": "292baa10ac966195d646d7deac63b4f08d745a6d744465b1186c1d46e58c6a80",
    "studio/article_engine.py": "653db77e8881aa6532906fa1b17a8c771152cfe14ef1266383daba423d596868",
    "studio/hero_visual.py": "d7ea2a8af41b255310f1b736c2e5795a399ec8d5aa80db45572c1f266594084d",
    "studio/evidence_validation.py": "97cb38d680792d2e85126475eb5d253912710e31ff572df2e90c217179814af2",
    "studio/publication_package.py": "859ba0c11430105da095d1a0cf4f402b6ea5649542007c7a14c8011517c301ad",
    "studio/portable_editorial_project.py": "108e863c2176aaf7b050b57a607f997904ba7c1df0a5c32808f772ce9869d65e",
    "assets/brand/logo/master/editorial-compass-mark-master.png": "b2cd1c22239b7176b43578892b0c37ac502ca5ab696b7c083a0b397bfe285727",
    "assets/brand/logo/master/editorial-compass-lockup-master.png": "ae56f16f3e4b3a2bfbf5cefbf6ee807482cd8814e30b7496a917b9eae3a5ba72",
}


class BootstrapError(RuntimeError):
    """Raised when deterministic V11-01 generation cannot continue."""


def run(command: list[str], root: Path, *, capture: bool = False) -> str:
    result = subprocess.run(
        command, cwd=root, text=True, capture_output=capture, check=False
    )
    if result.returncode:
        detail = (result.stderr or result.stdout or "command failed").strip()
        raise BootstrapError(f"{' '.join(command)}: {detail}")
    return result.stdout if capture else ""


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def repository_root() -> Path:
    root = Path(__file__).resolve().parents[1]
    if root.name != EXPECTED_REPOSITORY or not (root / ".git").exists():
        raise BootstrapError("Run from the expected repository.")
    return root


def changed_paths(root: Path) -> set[str]:
    output = run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        root,
        capture=True,
    )
    return {line[3:] for line in output.splitlines() if line}


def verify_context(root: Path) -> None:
    branch = run(["git", "branch", "--show-current"], root, capture=True).strip()
    if branch != EXPECTED_BRANCH:
        raise BootstrapError(f"Expected {EXPECTED_BRANCH}; found {branch}.")
    unexpected = changed_paths(root) - {*FILES, SCRIPT_PATH}
    if unexpected:
        raise BootstrapError(
            "Unexpected working-tree paths: " + ", ".join(sorted(unexpected))
        )


def verify_protected(root: Path) -> None:
    mismatches = [
        path
        for path, expected in PROTECTED_HASHES.items()
        if not (root / path).is_file() or digest(root / path) != expected
    ]
    if mismatches:
        raise BootstrapError(
            "Protected path mismatch: " + ", ".join(sorted(mismatches))
        )


def validate_generated(root: Path) -> None:
    mismatches = [
        path
        for path, expected in FILES.items()
        if not (root / path).is_file()
        or (root / path).read_text(encoding="utf-8") != expected
    ]
    if mismatches:
        raise BootstrapError(
            "Generated content mismatch: " + ", ".join(sorted(mismatches))
        )


def preview(root: Path) -> None:
    verify_context(root)
    verify_protected(root)
    print("V11-01 Author Journey Foundation preview - no files changed.")
    for path in sorted(FILES):
        print(f"- {path}")


def apply(root: Path) -> None:
    script_hash = digest(root / SCRIPT_PATH)
    for relative, content in FILES.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.is_file() or path.read_text(encoding="utf-8") != content:
            path.write_text(content, encoding="utf-8")
    if digest(root / SCRIPT_PATH) != script_hash:
        raise BootstrapError("Bootstrap modified itself during apply.")


def validate_repository(root: Path) -> None:
    run([sys.executable, "-m", "compileall", "-q", "studio", "scripts", "tests"], root)
    run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        root,
    )
    run([sys.executable, "studio.py", "validate"], root)
    run(["git", "diff", "--check"], root)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    root = repository_root()
    if not args.apply:
        preview(root)
        return 0
    verify_context(root)
    verify_protected(root)
    apply(root)
    verify_context(root)
    validate_generated(root)
    verify_protected(root)
    validate_repository(root)
    print(SENTINEL)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BootstrapError as exc:
        print(f"V11-01 bootstrap stopped: {exc}", file=sys.stderr)
        raise SystemExit(1)
