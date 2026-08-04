#!/usr/bin/env python3
"""Deterministically generate and validate V11-04 owned artifacts."""

from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import subprocess
import sys
from pathlib import Path


EXPECTED_REPOSITORY = "Ramrattan-AI-Editorial-Studio"
EXPECTED_BRANCH = "feature/v11-04-generation-orchestration"
SCRIPT_PATH = "scripts/bootstrap_v11_04_generation_orchestration.py"
V11_03_OWNER = "scripts/bootstrap_v11_03_editorial_discovery_plan.py"
SENTINEL = "V11_04_GENERATION_ORCHESTRATION_COMPLETE"

_RUNTIME_BLOB = "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"
_TEST_BLOB = "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"


def decode(blob: str) -> str:
    return gzip.decompress(base64.b64decode(blob)).decode("utf-8").rstrip() + "\n"


AUTHOR_JOURNEY = decode(_RUNTIME_BLOB)
FILES = {
    "studio/author_journey.py": AUTHOR_JOURNEY,
    "tests/test_v11_04_generation_orchestration.py": decode(_TEST_BLOB),
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
    """Raised when deterministic V11-04 generation cannot continue."""


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
    allowed = {*FILES, SCRIPT_PATH, V11_03_OWNER}
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
    print("V11-04 Generation orchestration preview - no files changed.")
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
        print(f"V11-04 bootstrap stopped: {exc}", file=sys.stderr)
        raise SystemExit(1)
