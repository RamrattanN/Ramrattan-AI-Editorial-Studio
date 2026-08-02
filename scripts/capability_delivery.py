"""State-aware capability delivery helper.

The helper inspects repository and GitHub state and returns the next
safe action.

It does not commit, push, create pull requests, or merge unless the
Author explicitly runs the displayed command.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any


DEFAULT_BASE_BRANCH = "develop"


class DeliveryState(str, Enum):
    """High-level capability delivery states."""

    DEVELOP_DIRTY = "develop_dirty"
    DEVELOP_BEHIND = "develop_behind"
    READY_FOR_BRANCH = "ready_for_branch"
    FEATURE_DIRTY = "feature_dirty"
    READY_TO_STAGE = "ready_to_stage"
    READY_TO_COMMIT = "ready_to_commit"
    READY_TO_PUSH = "ready_to_push"
    READY_FOR_PR = "ready_for_pr"
    PR_CHECKS_PENDING = "pr_checks_pending"
    PR_CHECKS_FAILED = "pr_checks_failed"
    READY_TO_MERGE = "ready_to_merge"
    MERGED_NEEDS_BASELINE_CHECK = "merged_needs_baseline_check"
    COMPLETE = "complete"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class CommandResult:
    """Normalized subprocess result."""

    command: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.returncode == 0


@dataclass(frozen=True)
class RepositorySnapshot:
    """Current local repository state."""

    root: Path
    branch: str
    status_lines: tuple[str, ...]
    head: str
    base_head: str
    remote_base_head: str
    upstream: str | None
    ahead: int
    behind: int
    feature_branch_exists: bool

    @property
    def clean(self) -> bool:
        return not self.status_lines

    @property
    def on_base(self) -> bool:
        return self.branch == DEFAULT_BASE_BRANCH

    @property
    def base_is_current(self) -> bool:
        return (
            self.base_head
            and self.base_head == self.remote_base_head
        )


@dataclass(frozen=True)
class PullRequestSnapshot:
    """Current pull-request state."""

    number: int
    url: str
    state: str
    merge_state_status: str
    checks_pending: int
    checks_failed: int

    @property
    def checks_passed(self) -> bool:
        return (
            self.checks_pending == 0
            and self.checks_failed == 0
        )


@dataclass(frozen=True)
class DeliveryRecommendation:
    """One resolved next action."""

    state: DeliveryState
    summary: str
    command: str | None = None
    explanation: str = ""


def run(
    command: list[str],
    *,
    cwd: Path,
) -> CommandResult:
    """Run a command without raising."""
    completed = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )

    return CommandResult(
        command=tuple(command),
        returncode=completed.returncode,
        stdout=completed.stdout.strip(),
        stderr=completed.stderr.strip(),
    )


def require_output(
    command: list[str],
    *,
    cwd: Path,
) -> str:
    """Run a command and require success."""
    result = run(command, cwd=cwd)

    if not result.ok:
        raise RuntimeError(
            f"Command failed: {' '.join(command)}\n"
            f"{result.stderr}"
        )

    return result.stdout


def repository_root() -> Path:
    """Locate the current Git repository."""
    result = run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=Path.cwd(),
    )

    if not result.ok:
        raise RuntimeError(
            "Run this helper from inside the repository."
        )

    return Path(result.stdout).resolve()


def branch_exists(
    root: Path,
    branch: str,
) -> bool:
    """Return True when a local branch exists."""
    result = run(
        [
            "git",
            "show-ref",
            "--verify",
            "--quiet",
            f"refs/heads/{branch}",
        ],
        cwd=root,
    )

    return result.ok


def porcelain_status(root: Path) -> tuple[str, ...]:
    """Return full Git porcelain status lines."""
    result = run(
        [
            "git",
            "status",
            "--porcelain",
            "--untracked-files=all",
        ],
        cwd=root,
    )

    if not result.ok:
        raise RuntimeError(result.stderr)

    return tuple(
        line
        for line in result.stdout.splitlines()
        if line.strip()
    )


def rev_parse(
    root: Path,
    revision: str,
) -> str:
    """Resolve a revision or return an empty string."""
    result = run(
        ["git", "rev-parse", revision],
        cwd=root,
    )

    return result.stdout if result.ok else ""


def upstream_name(root: Path) -> str | None:
    """Return current upstream name when configured."""
    result = run(
        [
            "git",
            "rev-parse",
            "--abbrev-ref",
            "--symbolic-full-name",
            "@{u}",
        ],
        cwd=root,
    )

    if not result.ok:
        return None

    return result.stdout


def ahead_behind(
    root: Path,
    upstream: str | None,
) -> tuple[int, int]:
    """Return commits ahead and behind the upstream."""
    if not upstream:
        return 0, 0

    result = run(
        [
            "git",
            "rev-list",
            "--left-right",
            "--count",
            f"{upstream}...HEAD",
        ],
        cwd=root,
    )

    if not result.ok:
        return 0, 0

    behind_raw, ahead_raw = result.stdout.split()

    return int(ahead_raw), int(behind_raw)


def snapshot(
    *,
    feature_branch: str,
) -> RepositorySnapshot:
    """Capture current repository state."""
    root = repository_root()

    branch = require_output(
        ["git", "branch", "--show-current"],
        cwd=root,
    )

    upstream = upstream_name(root)
    ahead, behind = ahead_behind(root, upstream)

    return RepositorySnapshot(
        root=root,
        branch=branch,
        status_lines=porcelain_status(root),
        head=rev_parse(root, "HEAD"),
        base_head=rev_parse(root, DEFAULT_BASE_BRANCH),
        remote_base_head=rev_parse(
            root,
            f"origin/{DEFAULT_BASE_BRANCH}",
        ),
        upstream=upstream,
        ahead=ahead,
        behind=behind,
        feature_branch_exists=branch_exists(
            root,
            feature_branch,
        ),
    )


def discover_pull_request(
    root: Path,
    *,
    feature_branch: str,
) -> PullRequestSnapshot | None:
    """Find an open pull request for the feature branch."""
    result = run(
        [
            "gh",
            "pr",
            "list",
            "--head",
            feature_branch,
            "--base",
            DEFAULT_BASE_BRANCH,
            "--state",
            "open",
            "--json",
            (
                "number,url,state,mergeStateStatus,"
                "statusCheckRollup"
            ),
        ],
        cwd=root,
    )

    if not result.ok:
        return None

    payload = json.loads(result.stdout or "[]")

    if not payload:
        return None

    item: dict[str, Any] = payload[0]
    checks = item.get("statusCheckRollup") or []

    pending = 0
    failed = 0

    for check in checks:
        status = str(
            check.get("status", "")
        ).upper()

        conclusion = str(
            check.get("conclusion", "")
        ).upper()

        if status and status != "COMPLETED":
            pending += 1
            continue

        if conclusion in {
            "FAILURE",
            "CANCELLED",
            "TIMED_OUT",
            "ACTION_REQUIRED",
            "STARTUP_FAILURE",
        }:
            failed += 1

    return PullRequestSnapshot(
        number=int(item["number"]),
        url=str(item["url"]),
        state=str(item.get("state", "OPEN")),
        merge_state_status=str(
            item.get("mergeStateStatus", "UNKNOWN")
        ),
        checks_pending=pending,
        checks_failed=failed,
    )


def shell_quote(value: str) -> str:
    """Return a safe double-quoted shell value."""
    escaped = (
        value
        .replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("$", "\$")
        .replace("`", "\`")
    )

    return f'"{escaped}"'


def recommend(
    *,
    feature_branch: str,
    commit_message: str,
    pr_title: str,
) -> DeliveryRecommendation:
    """Return the next safe capability-delivery action."""
    repo = snapshot(feature_branch=feature_branch)

    if repo.on_base:
        if not repo.clean:
            return DeliveryRecommendation(
                state=DeliveryState.DEVELOP_DIRTY,
                summary=(
                    "`develop` contains uncommitted changes."
                ),
                explanation=(
                    "Resolve or preserve those changes before "
                    "starting another capability."
                ),
            )

        if not repo.base_is_current:
            return DeliveryRecommendation(
                state=DeliveryState.DEVELOP_BEHIND,
                summary=(
                    "Local `develop` does not match "
                    "`origin/develop`."
                ),
                command=(
                    "git pull --ff-only origin develop"
                ),
            )

        if repo.feature_branch_exists:
            return DeliveryRecommendation(
                state=DeliveryState.READY_FOR_BRANCH,
                summary=(
                    "The feature branch already exists."
                ),
                command=(
                    f"git switch {feature_branch}"
                ),
            )

        return DeliveryRecommendation(
            state=DeliveryState.READY_FOR_BRANCH,
            summary=(
                "The repository is ready for a new "
                "feature branch."
            ),
            command=(
                f"git switch -c {feature_branch}"
            ),
        )

    if repo.branch != feature_branch:
        return DeliveryRecommendation(
            state=DeliveryState.UNKNOWN,
            summary=(
                f"Current branch is `{repo.branch}`, not "
                f"`{feature_branch}` or `develop`."
            ),
            explanation=(
                "Verify the intended capability before "
                "continuing."
            ),
        )

    pr = discover_pull_request(
        repo.root,
        feature_branch=feature_branch,
    )

    if repo.clean:
        if pr is not None:
            if pr.checks_failed:
                return DeliveryRecommendation(
                    state=DeliveryState.PR_CHECKS_FAILED,
                    summary=(
                        f"Pull request #{pr.number} has "
                        "failing checks."
                    ),
                    command=(
                        f"gh pr checks {pr.number}"
                    ),
                )

            if pr.checks_pending:
                return DeliveryRecommendation(
                    state=DeliveryState.PR_CHECKS_PENDING,
                    summary=(
                        f"Pull request #{pr.number} checks "
                        "are still running."
                    ),
                    command=(
                        f"gh pr checks {pr.number}"
                    ),
                )

            return DeliveryRecommendation(
                state=DeliveryState.READY_TO_MERGE,
                summary=(
                    f"Pull request #{pr.number} is ready "
                    "for merge."
                ),
                command=(
                    f"gh pr merge {pr.number} "
                    "--merge --delete-branch"
                ),
            )

        if repo.upstream is None:
            return DeliveryRecommendation(
                state=DeliveryState.READY_TO_PUSH,
                summary=(
                    "The feature branch is committed and "
                    "has no upstream."
                ),
                command=(
                    "git push --set-upstream origin "
                    f"{feature_branch}"
                ),
            )

        if repo.ahead > 0:
            return DeliveryRecommendation(
                state=DeliveryState.READY_TO_PUSH,
                summary=(
                    "The feature branch contains unpushed "
                    "commits."
                ),
                command=(
                    f"git push origin {feature_branch}"
                ),
            )

        return DeliveryRecommendation(
            state=DeliveryState.READY_FOR_PR,
            summary=(
                "The branch is published and no open pull "
                "request was found."
            ),
            command=(
                "gh pr create \\\n"
                f"  --base {DEFAULT_BASE_BRANCH} \\\n"
                f"  --head {feature_branch} \\\n"
                f"  --title {shell_quote(pr_title)}"
            ),
        )

    staged = run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=repo.root,
    )

    unstaged = run(
        ["git", "diff", "--quiet"],
        cwd=repo.root,
    )

    untracked = any(
        line.startswith("??")
        for line in repo.status_lines
    )

    has_staged = not staged.ok
    has_unstaged = not unstaged.ok or untracked

    if has_staged and not has_unstaged:
        return DeliveryRecommendation(
            state=DeliveryState.READY_TO_COMMIT,
            summary=(
                "All current changes are staged."
            ),
            command=(
                f"git commit -m "
                f"{shell_quote(commit_message)}"
            ),
        )

    return DeliveryRecommendation(
        state=DeliveryState.READY_TO_STAGE,
        summary=(
            "The feature branch contains uncommitted changes."
        ),
        command=(
            "git add -A && "
            "git diff --cached --name-status"
        ),
        explanation=(
            "Review the staged set before committing."
        ),
    )


def print_recommendation(
    recommendation: DeliveryRecommendation,
) -> None:
    """Render one recommendation."""
    print()
    print(f"State: {recommendation.state.value}")
    print()
    print(recommendation.summary)

    if recommendation.explanation:
        print()
        print(recommendation.explanation)

    if recommendation.command:
        print()
        print("Next command:")
        print()
        print(recommendation.command)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Determine the next safe capability-delivery action."
        )
    )

    parser.add_argument(
        "--branch",
        required=True,
        help="Resolved feature branch name.",
    )

    parser.add_argument(
        "--commit-message",
        required=True,
        help="Resolved commit message.",
    )

    parser.add_argument(
        "--pr-title",
        required=True,
        help="Resolved pull-request title.",
    )

    return parser.parse_args()


def main() -> int:
    """Inspect state and print the next action."""
    args = parse_args()

    try:
        recommendation = recommend(
            feature_branch=args.branch,
            commit_message=args.commit_message,
            pr_title=args.pr_title,
        )

        print_recommendation(recommendation)

        return 0

    except (
        RuntimeError,
        json.JSONDecodeError,
        ValueError,
    ) as exc:
        print(
            f"ERROR: {exc}",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
