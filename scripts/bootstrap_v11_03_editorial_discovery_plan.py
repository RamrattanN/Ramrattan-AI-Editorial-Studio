#!/usr/bin/env python3
"""Deterministically generate and validate V11-03 owned artifacts."""

from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import subprocess
import sys
from pathlib import Path


EXPECTED_REPOSITORY = "Ramrattan-AI-Editorial-Studio"
EXPECTED_BRANCH = "feature/v11-03-editorial-discovery-plan"
SCRIPT_PATH = "scripts/bootstrap_v11_03_editorial_discovery_plan.py"
V11_02_OWNER = "scripts/bootstrap_v11_02_editorial_source_branding.py"
SENTINEL = "V11_03_EDITORIAL_DISCOVERY_PLAN_COMPLETE"

_RUNTIME_BLOB = (
    "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"
)

_TEST_BLOB = (
    "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"
    "eTHW+MM4Mkirmlx6FHb6D4CGqHAGKAAA"
)


def decode(blob: str) -> str:
    return gzip.decompress(base64.b64decode(blob)).decode("utf-8").rstrip() + "\n"


AUTHOR_JOURNEY = decode(_RUNTIME_BLOB)
FILES = {
    "studio/author_journey.py": AUTHOR_JOURNEY,
    "tests/test_v11_03_editorial_discovery_plan.py": decode(_TEST_BLOB),
}

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
    """Raised when deterministic V11-03 generation cannot continue."""


def run(command: list[str], root: Path, *, capture: bool = False) -> str:
    result = subprocess.run(command, cwd=root, text=True, capture_output=capture, check=False)
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
    output = run(["git", "status", "--porcelain=v1", "--untracked-files=all"], root, capture=True)
    return {line[3:] for line in output.splitlines() if line}


def verify_context(root: Path) -> None:
    branch = run(["git", "branch", "--show-current"], root, capture=True).strip()
    if branch != EXPECTED_BRANCH:
        raise BootstrapError(f"Expected {EXPECTED_BRANCH}; found {branch}.")
    allowed = {*FILES, SCRIPT_PATH, V11_02_OWNER}
    unexpected = changed_paths(root) - allowed
    if unexpected:
        raise BootstrapError("Unexpected working-tree paths: " + ", ".join(sorted(unexpected)))


def verify_protected(root: Path) -> None:
    mismatches = [path for path, expected in PROTECTED_HASHES.items() if not (root / path).is_file() or digest(root / path) != expected]
    if mismatches:
        raise BootstrapError("Protected path mismatch: " + ", ".join(sorted(mismatches)))


def validate_generated(root: Path) -> None:
    mismatches = [path for path, expected in FILES.items() if not (root / path).is_file() or (root / path).read_text(encoding="utf-8") != expected]
    if mismatches:
        raise BootstrapError("Generated content mismatch: " + ", ".join(sorted(mismatches)))


def preview(root: Path) -> None:
    verify_context(root)
    validate_generated(root)
    verify_protected(root)
    print("V11-03 Editorial Discovery and Plan preview - no files changed.")
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
    run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], root)
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
        print(f"V11-03 bootstrap stopped: {exc}", file=sys.stderr)
        raise SystemExit(1)
