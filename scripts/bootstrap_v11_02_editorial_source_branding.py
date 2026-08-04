#!/usr/bin/env python3
"""Deterministically generate and validate V11-02 owned artifacts."""

from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import subprocess
import sys
from pathlib import Path


EXPECTED_REPOSITORY = "Ramrattan-AI-Editorial-Studio"
EXPECTED_BRANCH = "feature/v11-02-editorial-source-branding"
SCRIPT_PATH = "scripts/bootstrap_v11_02_editorial_source_branding.py"
V11_01_OWNER = "scripts/bootstrap_v11_01_author_journey_foundation.py"
SENTINEL = "V11_02_EDITORIAL_SOURCE_BRANDING_COMPLETE"

_RUNTIME_BLOB = (
    "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"
    "s6afXkylBSNrGn2iR3vCzTEX/kvdHgtNYkl0yyPVkWv3Du91a8HBoVxyFPIq8/gAmQpSt0G230NhCaG9VAoBV0kr3ZjvXWnOH2penezLlc1X7VYfZGpaY+w4"
    "32H8etPch7QBafek/MOk0m+QUPKYqdeHPvg4zNOqPO29jPuu/NzJ0ilOpY26bVZy2mTIAVe7N/aNmD1yUtlht2i6R1xraexkePxisO4o1fK9DrI2+ST9W92H"
    "HpmCwhDXKbnDPbNaUhOkN/QPjG2hJpjMTv/q7BkFf0kVpNtTsOxKXwVQNEruKUTZ2JDMlRn29NE4NZcmszc1N48pjpqUPzy+p0XSFSLRs3t+FNlaW9oU5nRX"
    "nz3siF9YwTscZ9UHG5V69uAfVN1Q1x0aSlT8tjqb1q8DUABG/56bNMtuwAp/YAA2FsvpgSDZXQGz16JloIeCGn4zsL/HgkftQVCm0nuJ04tppHjBxRyTRhfz"
    "fOr3EqYGrVmjCmoPf6h0EKZdIlObO7eUoTAXzaGh/lSNdNqvlQ/Vn59Ri+ifYVWdvDmUv/kV4heQn99r11nLJ3Ro25PtSJc5qEKyJ7qdWjR3unxf5zgiOqY3"
    "4FLNTJ+Ahj72GCZ16dTjvZb8qXjUD7XR4HcSyq3Lq4hvKayk60GD7Lvyt5oDMc3cNExW0h7p5vWBDdZ15EekNUvbOGPhWx4EIo/i/uzBQBUzOI+/VK4lxWb9"
    "qweN4IPCTu6rGeL/AJPa/ZFuPgAA"
)

_TEST_BLOB = (
    "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"
)


def decode(blob: str) -> str:
    return gzip.decompress(base64.b64decode(blob)).decode("utf-8").rstrip() + "\n"


AUTHOR_JOURNEY = decode(_RUNTIME_BLOB)
FILES = {
    "studio/author_journey.py": AUTHOR_JOURNEY,
    "tests/test_v11_02_editorial_source_branding.py": decode(_TEST_BLOB),
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
    """Raised when deterministic V11-02 generation cannot continue."""


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
    allowed = {*FILES, SCRIPT_PATH, V11_01_OWNER}
    unexpected = changed_paths(root) - allowed
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
    validate_generated(root)
    verify_protected(root)
    print("V11-02 Editorial Source and Branding preview - no files changed.")
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
        print(f"V11-02 bootstrap stopped: {exc}", file=sys.stderr)
        raise SystemExit(1)
