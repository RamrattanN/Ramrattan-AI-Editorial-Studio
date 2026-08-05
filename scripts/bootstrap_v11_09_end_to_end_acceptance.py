#!/usr/bin/env python3
"""Deterministically generate and validate V11-09 acceptance evidence."""

from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import subprocess
import sys
from pathlib import Path


EXPECTED_REPOSITORY = "Ramrattan-AI-Editorial-Studio"
EXPECTED_BRANCH = "feature/v11-09-end-to-end-acceptance"
SCRIPT_PATH = "scripts/bootstrap_v11_09_end_to_end_acceptance.py"
SENTINEL = "V11_09_END_TO_END_ACCEPTANCE_COMPLETE"

_TEST_BLOB = "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"


def decode(blob: str) -> str:
    return gzip.decompress(base64.b64decode(blob)).decode("utf-8").rstrip() + "\n"


FILES = {
    "tests/test_v11_09_end_to_end_acceptance.py": decode(_TEST_BLOB),
}

PROTECTED_HASHES = {
    "studio/author_journey.py": "f4791965d68b61dd47de6ff33f8f6fd430856d1093ea9c18fcd0a4d4f2dac9ad",
    "studio/session_completion.py": "4c9d11e5a6421e835e2c85ef8c83ed9117f26fc23a2c19bf877408dde10c898b",
    "studio/publication_studio.py": "30991d09a781e404abc88109976b7b2b956f5fd8733aa7a60c8cbe6894d33198",
    "studio/publication_package.py": "859ba0c11430105da095d1a0cf4f402b6ea5649542007c7a14c8011517c301ad",
    "studio/portable_editorial_project.py": "108e863c2176aaf7b050b57a607f997904ba7c1df0a5c32808f772ce9869d65e",
    "studio/editorial_audit.py": "5800746ab3649903b6e5cc795955a57423d97821be45d486eea1b3852ff4e6c4",
    "studio/article_engine.py": "653db77e8881aa6532906fa1b17a8c771152cfe14ef1266383daba423d596868",
    "studio/hero_visual.py": "d7ea2a8af41b255310f1b736c2e5795a399ec8d5aa80db45572c1f266594084d",
    "studio/evidence_validation.py": "97cb38d680792d2e85126475eb5d253912710e31ff572df2e90c217179814af2",
    "scripts/bootstrap_v11_08_session_completion_artifacts.py": "92d5b493fffc13ff101d2dd7a4a3168e76e2a9b1d26984148a9cd81920c1d8d4",
    "tests/test_v11_08_session_completion.py": "e3ca9d83e980893882394dc5bb3cc165b3e6331374e1ef633e7ff12888efb5d7",
    "studio/workflow/README.md": "2f98daa4f2f4760bd72c36867de1658a120bad5b06ab3348dad717f534eb3211",
    "studio/workflow/__init__.py": "9ac599af687b85520dcb0719fee72ed9d40f2cdc4e7e8dc825f8a7f1354a47e0",
    "studio/workflow/choices.py": "47cafc01797a57443ebbff5bb842cb82abb59fbe8a2f3d53dd2d5f752000c97d",
    "studio/workflow/state.py": "da7499c0a7759deebf8a396f7f290ca44a1ea322b048386e33edf0acbe4cf359",
    "studio/workflow/workflow.py": "2c34e2991a6115b583d9707a95f0b2d547ade31aa2f92dd84479189fbae2ab15",
    "scripts/bootstrap_sprint2_workflow.py": "292baa10ac966195d646d7deac63b4f08d745a6d744465b1186c1d46e58c6a80",
    "assets/brand/logo/master/editorial-compass-mark-master.png": "b2cd1c22239b7176b43578892b0c37ac502ca5ab696b7c083a0b397bfe285727",
    "assets/brand/logo/master/editorial-compass-lockup-master.png": "ae56f16f3e4b3a2bfbf5cefbf6ee807482cd8814e30b7496a917b9eae3a5ba72",
}


class BootstrapError(RuntimeError):
    """Raised when deterministic V11-09 generation cannot continue."""


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
    allowed = {*FILES, SCRIPT_PATH}
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
    print("V11-09 End-to-End Author Acceptance preview - no files changed.")
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
        print(f"V11-09 bootstrap stopped: {exc}", file=sys.stderr)
        raise SystemExit(1)
