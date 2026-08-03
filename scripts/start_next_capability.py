#!/usr/bin/env python3
"""
Prepare the repository for Sprint 3A - Adaptive Editorial Context.

Preview:
    python3 scripts/start_next_capability.py

Apply:
    python3 scripts/start_next_capability.py --apply

The script itself may be untracked while it prepares the new feature
branch. No other working-tree changes are permitted.

It does not commit, push, create a pull request, or modify GitHub.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


EXPECTED_REPOSITORY = "Ramrattan-AI-Editorial-Studio"
EXPECTED_REMOTE_FRAGMENT = (
    "RamrattanN/Ramrattan-AI-Editorial-Studio"
)

BASE_BRANCH = "develop"
FEATURE_BRANCH = "feature/adaptive-editorial-context"

SCRIPT_RELATIVE_PATH = "scripts/start_next_capability.py"
SCRIPT_SENTINEL = "START_NEXT_CAPABILITY_SCRIPT_COMPLETE"


class PreparationError(RuntimeError):
    """Raised when Sprint 3 preparation cannot proceed safely."""


def run(
    command: list[str],
    *,
    cwd: Path,
    capture: bool = False,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    """Run and display a command."""
    print("$", " ".join(command))

    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=capture,
        check=check,
    )


def output(command: list[str], *, cwd: Path) -> str:
    """Run a command and return stripped standard output."""
    return run(
        command,
        cwd=cwd,
        capture=True,
    ).stdout.strip()


def repository_root() -> Path:
    """Locate and validate the expected repository."""
    try:
        root = Path(
            output(
                ["git", "rev-parse", "--show-toplevel"],
                cwd=Path.cwd(),
            )
        ).resolve()
    except (
        FileNotFoundError,
        subprocess.CalledProcessError,
    ) as exc:
        raise PreparationError(
            "Run this script from inside the cloned repository."
        ) from exc

    if root.name != EXPECTED_REPOSITORY:
        raise PreparationError(
            f"Expected repository '{EXPECTED_REPOSITORY}', "
            f"found '{root.name}'."
        )

    remote = output(
        ["git", "remote", "get-url", "origin"],
        cwd=root,
    )

    if EXPECTED_REMOTE_FRAGMENT not in remote:
        raise PreparationError(
            "The origin remote does not match the expected repository."
        )

    return root


def current_branch(root: Path) -> str:
    """Return the current Git branch."""
    return output(
        ["git", "branch", "--show-current"],
        cwd=root,
    )


def working_tree_lines(root: Path) -> list[str]:
    """Return non-empty porcelain-format Git status lines."""
    status = output(
        ["git", "status", "--porcelain"],
        cwd=root,
    )

    return [
        line
        for line in status.splitlines()
        if line.strip()
    ]


def verify_script_integrity() -> None:
    """Fail safely if the pasted script is incomplete."""
    script_path = Path(__file__).resolve()
    content = script_path.read_text(encoding="utf-8")

    if SCRIPT_SENTINEL not in content:
        raise PreparationError(
            "The script appears incomplete or truncated. "
            "The final sentinel is missing."
        )

    print("Script integrity check passed.")


def verify_allowed_working_tree(root: Path) -> None:
    """
    Permit only this preparation script as an untracked file.

    This allows the script to create the new feature branch and then
    become part of the upcoming Sprint 3 PR.
    """
    lines = working_tree_lines(root)

    allowed = {
        f"?? {SCRIPT_RELATIVE_PATH}",
    }

    unexpected = [
        line
        for line in lines
        if line not in allowed
    ]

    if unexpected:
        raise PreparationError(
            "Unexpected working-tree changes exist:\n"
            + "\n".join(unexpected)
            + "\n\nOnly the untracked preparation script is allowed."
        )

    if lines:
        print(
            "Working tree contains only the expected "
            "untracked preparation script."
        )
    else:
        print("Working tree is clean.")


def branch_exists_locally(
    root: Path,
    branch: str,
) -> bool:
    """Return whether a local branch exists."""
    result = subprocess.run(
        [
            "git",
            "show-ref",
            "--verify",
            "--quiet",
            f"refs/heads/{branch}",
        ],
        cwd=root,
    )

    return result.returncode == 0


def branch_exists_remotely(
    root: Path,
    branch: str,
) -> bool:
    """Return whether a remote branch exists."""
    result = subprocess.run(
        [
            "git",
            "ls-remote",
            "--exit-code",
            "--heads",
            "origin",
            branch,
        ],
        cwd=root,
        text=True,
        capture_output=True,
    )

    return result.returncode == 0


def preview(root: Path) -> None:
    """Display the intended Sprint 3 preparation."""
    print("\nSprint 3 preparation preview:\n")

    print(f"Current branch: {current_branch(root)}")
    print(f"Base branch: {BASE_BRANCH}")
    print(f"Target branch: {FEATURE_BRANCH}")

    print("\nThe script will:")

    print(f"  1. Switch to {BASE_BRANCH}")
    print("  2. Fetch and prune origin")
    print(f"  3. Fast-forward {BASE_BRANCH}")
    print(f"  4. Create or restore {FEATURE_BRANCH}")
    print("  5. Carry this untracked script onto the feature branch")
    print("  6. Confirm the final repository state")

    print("\nThe script will not:")

    print("  - generate product files")
    print("  - commit changes")
    print("  - push a branch")
    print("  - create a pull request")
    print("  - modify the Kanban board")

    print("\nNothing has been changed.")

    print("\nApply with:")

    print(
        "  python3 scripts/start_next_capability.py --apply"
    )


def switch_to_develop(root: Path) -> None:
    """Switch to and synchronize develop."""
    branch = current_branch(root)

    if branch != BASE_BRANCH:
        run(
            ["git", "switch", BASE_BRANCH],
            cwd=root,
        )
    else:
        print(f"Already on {BASE_BRANCH}.")

    verify_allowed_working_tree(root)

    run(
        ["git", "fetch", "origin", "--prune"],
        cwd=root,
    )

    run(
        [
            "git",
            "pull",
            "--ff-only",
            "origin",
            BASE_BRANCH,
        ],
        cwd=root,
    )


def create_or_restore_feature_branch(root: Path) -> None:
    """Create or restore the Sprint 3 feature branch."""
    if branch_exists_locally(root, FEATURE_BRANCH):
        run(
            ["git", "switch", FEATURE_BRANCH],
            cwd=root,
        )

        print(
            f"Restored existing local branch {FEATURE_BRANCH}."
        )
        return

    if branch_exists_remotely(root, FEATURE_BRANCH):
        run(
            [
                "git",
                "switch",
                "--track",
                f"origin/{FEATURE_BRANCH}",
            ],
            cwd=root,
        )

        print(
            f"Restored remote branch {FEATURE_BRANCH}."
        )
        return

    run(
        [
            "git",
            "switch",
            "-c",
            FEATURE_BRANCH,
        ],
        cwd=root,
    )

    print(f"Created {FEATURE_BRANCH}.")


def verify_final_state(root: Path) -> None:
    """Confirm the repository is ready for Sprint 3A."""
    branch = current_branch(root)

    if branch != FEATURE_BRANCH:
        raise PreparationError(
            f"Expected final branch '{FEATURE_BRANCH}', "
            f"found '{branch}'."
        )

    verify_allowed_working_tree(root)

    print("\nSprint 3 starting state verified.")
    print(f"Branch: {branch}")
    print(
        "Working tree: only the expected untracked "
        "preparation script"
    )


def apply(root: Path) -> None:
    """Prepare the repository for Sprint 3A."""
    switch_to_develop(root)
    create_or_restore_feature_branch(root)
    verify_final_state(root)

    print()
    print("Sprint 3A is ready to begin.")
    print()
    print("Capability:")
    print("  Adaptive Editorial Context")
    print()
    print("Nothing has been committed or pushed.")


def parse_args() -> argparse.Namespace:
    """Parse command-line options."""
    parser = argparse.ArgumentParser(
        description=(
            "Prepare the repository for Sprint 3A - "
            "Adaptive Editorial Context."
        )
    )

    parser.add_argument(
        "--apply",
        action="store_true",
        help=(
            "Synchronize develop and create the Sprint 3 "
            "feature branch."
        ),
    )

    return parser.parse_args()


def main() -> int:
    """Preview or apply the Sprint 3 preparation."""
    args = parse_args()

    try:
        root = repository_root()

        print(f"Repository: {root}")

        verify_script_integrity()
        verify_allowed_working_tree(root)

        if args.apply:
            apply(root)
        else:
            preview(root)

        return 0

    except PreparationError as exc:
        print(
            f"\nERROR: {exc}",
            file=sys.stderr,
        )
        return 1

    except subprocess.CalledProcessError as exc:
        print(
            f"\nERROR: Command failed with exit code "
            f"{exc.returncode}.",
            file=sys.stderr,
        )
        return exc.returncode

    except Exception as exc:
        print(
            f"\nUNEXPECTED ERROR: {exc}",
            file=sys.stderr,
        )
        return 1


# START_NEXT_CAPABILITY_SCRIPT_COMPLETE
# END OF SCRIPT - START NEXT CAPABILITY


if __name__ == "__main__":
    raise SystemExit(main())