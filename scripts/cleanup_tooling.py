#!/usr/bin/env python3
"""
Clean up temporary PR-004 automation safely.

Preview:
    python3 scripts/cleanup_pr004_tooling.py

Apply:
    python3 scripts/cleanup_pr004_tooling.py --apply

This script never commits, pushes, opens a pull request, or changes
GitHub Projects.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


EXPECTED_REPOSITORY = "Ramrattan-AI-Editorial-Studio"
EXPECTED_BRANCH = "feature/article-first-alignment"


TEMPORARY_SCRIPTS = (
    "scripts/bootstrap_pr004_article_first_alignment.py",
    "scripts/complete_pr004_article_first_alignment.py",
    "scripts/repair_pr004_validation.py",
    "scripts/finalize_pr004_validation.py",
)


REQUIRED_FILES = (
    "README.md",
    "CHANGELOG.md",
    "ROADMAP.md",
    "docs/Project_Charter.md",
    "docs/product/Current_Product_Focus.md",
    "docs/product/PRD_v1.1.md",
    "docs/product/Product_Principles.md",
    "docs/product/Studio_Contract.md",
    "docs/product/Glossary.md",
    "docs/product/Decision_Log.md",
    "docs/architecture/adr/"
    "ADR-003-adopt-an-article-first-publication-package.md",
    "studio/workflow/README.md",
    "tests/test_article_first_alignment.py",
    "scripts/update_kanban_sprint3.py",
)


class CleanupError(RuntimeError):
    """Raised when cleanup cannot proceed safely."""


def run(
    command: list[str],
    *,
    cwd: Path,
    capture: bool = False,
) -> subprocess.CompletedProcess[str]:
    """Run and display a command."""
    print("$", " ".join(command))

    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=capture,
        check=True,
    )


def output(command: list[str], *, cwd: Path) -> str:
    """Return stripped command output."""
    return run(
        command,
        cwd=cwd,
        capture=True,
    ).stdout.strip()


def repository_root() -> Path:
    """Locate and validate the repository."""
    try:
        root = Path(
            output(
                ["git", "rev-parse", "--show-toplevel"],
                cwd=Path.cwd(),
            )
        ).resolve()
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise CleanupError(
            "Run this script from inside the cloned repository."
        ) from exc

    if root.name != EXPECTED_REPOSITORY:
        raise CleanupError(
            f"Expected repository '{EXPECTED_REPOSITORY}', "
            f"found '{root.name}'."
        )

    return root


def verify_branch(root: Path) -> None:
    """Require the PR-004 working branch."""
    branch = output(
        ["git", "branch", "--show-current"],
        cwd=root,
    )

    print(f"Branch: {branch}")

    if branch != EXPECTED_BRANCH:
        raise CleanupError(
            f"Expected branch '{EXPECTED_BRANCH}', found '{branch}'."
        )


def verify_required_files(root: Path) -> None:
    """Ensure the validated PR-004 artifacts are present."""
    missing = [
        relative
        for relative in REQUIRED_FILES
        if not (root / relative).is_file()
    ]

    if missing:
        raise CleanupError(
            "Required PR-004 files are missing:\n"
            + "\n".join(f"  - {item}" for item in missing)
        )

    print("All required PR-004 artifacts are present.")


def validate_product_requirements(root: Path) -> None:
    """Check the most important agreed product language."""
    checks: dict[str, tuple[str, ...]] = {
        "README.md": (
            "publication-ready professional articles",
            "720 × 425 Hero Visual",
            "approximately 10 minutes",
            "Author Library",
        ),
        "docs/product/Current_Product_Focus.md": (
            "Author work is private by default.",
            "Carousels",
            "approximately 10 minutes",
        ),
        "docs/product/PRD_v1.1.md": (
            "Hero Visual - 720 × 425",
            "explain why the input is insufficient",
            "provide an example of a stronger input",
        ),
        "studio/workflow/README.md": (
            "Historical prototype notice",
            "not part",
            "current product scope",
        ),
    }

    for relative, phrases in checks.items():
        content = (root / relative).read_text(encoding="utf-8")
        normalized = " ".join(content.replace(">", " ").split())

        for phrase in phrases:
            if phrase not in normalized:
                raise CleanupError(
                    f"Expected phrase '{phrase}' in {relative}."
                )

    print("Product-alignment checks passed.")


def run_validation(root: Path) -> None:
    """Run the complete repository validation."""
    run(
        [
            sys.executable,
            "-m",
            "compileall",
            "-q",
            "studio",
            "tests",
        ],
        cwd=root,
    )

    run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "tests",
            "-v",
        ],
        cwd=root,
    )

    run(
        [sys.executable, "studio.py", "validate"],
        cwd=root,
    )

    print("Repository validation passed.")


def existing_temporary_scripts(root: Path) -> list[str]:
    """Return temporary scripts that currently exist."""
    return [
        relative
        for relative in TEMPORARY_SCRIPTS
        if (root / relative).exists()
    ]


def preview_cleanup(root: Path) -> None:
    """Display the intended cleanup without changing files."""
    existing = existing_temporary_scripts(root)

    print("\nCleanup preview:\n")

    if existing:
        print("The following temporary scripts will be removed:")

        for relative in existing:
            print(f"  - {relative}")
    else:
        print("No temporary PR-004 scripts remain.")

    print("\nThe following reusable scripts will be retained:")
    print("  - scripts/update_kanban_sprint3.py")
    print("  - scripts/cleanup_pr004_tooling.py")

    print("\nNo files have been changed.")
    print("\nApply with:")
    print("  python3 scripts/cleanup_pr004_tooling.py --apply")


def apply_cleanup(root: Path) -> None:
    """Remove only the temporary PR-004 automation."""
    existing = existing_temporary_scripts(root)

    for relative in existing:
        path = root / relative
        path.unlink()
        print(f"Removed {relative}")

    print("\nCleanup applied.")

    print("\nGit status:")
    run(["git", "status", "--short"], cwd=root)

    print("\nTracked change summary:")
    run(["git", "diff", "--stat"], cwd=root)

    print()
    print("PR-004 tooling cleanup completed.")
    print("Nothing has been committed, pushed, or changed on GitHub.")


def parse_args() -> argparse.Namespace:
    """Parse command-line options."""
    parser = argparse.ArgumentParser(
        description="Clean up temporary PR-004 scripts safely."
    )

    parser.add_argument(
        "--apply",
        action="store_true",
        help="Remove temporary PR-004 automation after validation.",
    )

    return parser.parse_args()


def main() -> int:
    """Validate and optionally clean up PR-004 tooling."""
    args = parse_args()

    try:
        root = repository_root()

        print(f"Repository: {root}")

        verify_branch(root)
        verify_required_files(root)
        validate_product_requirements(root)
        run_validation(root)

        if args.apply:
            apply_cleanup(root)
        else:
            preview_cleanup(root)

        return 0

    except CleanupError as exc:
        print(f"\nERROR: {exc}", file=sys.stderr)
        return 1

    except subprocess.CalledProcessError as exc:
        print(
            f"\nERROR: Command failed with exit code "
            f"{exc.returncode}.",
            file=sys.stderr,
        )
        return exc.returncode

    except Exception as exc:
        print(f"\nUNEXPECTED ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())