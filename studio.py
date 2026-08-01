#!/usr/bin/env python3
"""Project utilities for Ramrattan AI Editorial Studio."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VERSION_FILE = ROOT / "VERSION"

REQUIRED_PATHS = (
    "README.md",
    "CHANGELOG.md",
    "ROADMAP.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "VERSION",
    "docs",
    "prompts",
    "examples",
    "releases",
    "tests",
    "templates",
    ".github",
)


def version() -> str:
    try:
        return VERSION_FILE.read_text(encoding="utf-8").strip()
    except OSError:
        return "unknown"


def show_status(_: argparse.Namespace) -> int:
    print("Ramrattan AI Editorial Studio")
    print(f"Version: {version()}")
    print("Sprint: Sprint 1 - The Foundation")
    print("Status: Release candidate")
    return 0


def show_version(_: argparse.Namespace) -> int:
    print(version())
    return 0


def show_structure(_: argparse.Namespace) -> int:
    for relative in REQUIRED_PATHS:
        marker = "✓" if (ROOT / relative).exists() else "✗"
        print(f"{marker} {relative}")
    return 0


def validate(_: argparse.Namespace) -> int:
    missing = [
        relative
        for relative in REQUIRED_PATHS
        if not (ROOT / relative).exists()
    ]

    if missing:
        print("Validation failed:", file=sys.stderr)
        for relative in missing:
            print(f"  - Missing: {relative}", file=sys.stderr)
        return 1

    if version() in {"", "unknown"}:
        print("Validation failed: VERSION is unreadable.", file=sys.stderr)
        return 1

    print(f"Validation passed for v{version()}.")
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Ramrattan AI Editorial Studio utilities."
    )
    commands = result.add_subparsers(dest="command", required=True)

    definitions = {
        "status": ("Display project status.", show_status),
        "version": ("Display project version.", show_version),
        "structure": ("Display required paths.", show_structure),
        "validate": ("Validate the repository.", validate),
    }

    for name, (help_text, handler) in definitions.items():
        command = commands.add_parser(name, help=help_text)
        command.set_defaults(handler=handler)

    return result


def main() -> int:
    args = parser().parse_args()
    return int(args.handler(args))


if __name__ == "__main__":
    raise SystemExit(main())
