"""Fail-closed Capability Delivery state observer and recommender.

The helper observes local Git and GitHub state, then recommends one safe
next transition. It never performs protected delivery mutations itself.
Unknown, unavailable, incomplete, or ambiguous evidence blocks advancement.
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


class ObservationState(str, Enum):
    """Result of observing an external artifact."""

    FOUND = "found"
    NOT_FOUND = "not_found"
    UNAVAILABLE = "unavailable"
    AMBIGUOUS = "ambiguous"


class RemoteState(str, Enum):
    """Freshness of direct remote evidence."""

    FRESH = "fresh"
    UNAVAILABLE = "unavailable"


class ReviewState(str, Enum):
    """Pull-request review readiness."""

    DRAFT = "draft"
    READY_FOR_REVIEW = "ready_for_review"
    REVIEW_REQUIRED = "review_required"
    CHANGES_REQUESTED = "changes_requested"
    APPROVED = "approved"
    UNAVAILABLE = "unavailable"


class MergeabilityState(str, Enum):
    """Normalized pull-request mergeability."""

    CLEAN = "clean"
    CONFLICTING = "conflicting"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"
    UNAVAILABLE = "unavailable"


class CheckState(str, Enum):
    """Aggregate CI/check state."""

    UNAVAILABLE = "unavailable"
    PENDING = "pending"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMED_OUT = "timed_out"
    ACTION_REQUIRED = "action_required"
    SUCCESSFUL = "successful"


class DeliveryState(str, Enum):
    """High-level capability delivery states."""

    REMOTE_VERIFICATION_FAILED = "remote_verification_failed"
    DEVELOP_DIRTY = "develop_dirty"
    DEVELOP_BEHIND = "develop_behind"
    READY_FOR_BRANCH = "ready_for_branch"
    READY_FOR_WORK = "ready_for_work"
    FEATURE_OUT_OF_SYNC = "feature_out_of_sync"
    READY_TO_STAGE = "ready_to_stage"
    READY_TO_COMMIT = "ready_to_commit"
    READY_TO_PUSH = "ready_to_push"
    READY_FOR_PR = "ready_for_pr"
    PR_DISCOVERY_UNAVAILABLE = "pr_discovery_unavailable"
    PR_DISCOVERY_AMBIGUOUS = "pr_discovery_ambiguous"
    PR_CLOSED = "pr_closed"
    PR_DRAFT = "pr_draft"
    PR_READY_FOR_REVIEW = "pr_ready_for_review"
    PR_REVIEW_REQUIRED = "pr_review_required"
    PR_CHANGES_REQUESTED = "pr_changes_requested"
    PR_CHECKS_UNAVAILABLE = "pr_checks_unavailable"
    PR_CHECKS_PENDING = "pr_checks_pending"
    PR_CHECKS_FAILED = "pr_checks_failed"
    PR_CHECKS_CANCELLED = "pr_checks_cancelled"
    PR_CHECKS_TIMED_OUT = "pr_checks_timed_out"
    PR_CHECKS_ACTION_REQUIRED = "pr_checks_action_required"
    PR_MERGE_CONFLICT = "pr_merge_conflict"
    PR_MERGE_BLOCKED = "pr_merge_blocked"
    PR_MERGEABILITY_UNKNOWN = "pr_mergeability_unknown"
    READY_TO_MERGE = "ready_to_merge"
    POST_MERGE_CLEANUP = "post_merge_cleanup"
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
class RemoteSnapshot:
    """Directly observed remote branch heads."""

    state: RemoteState
    base_head: str = ""
    feature_head: str | None = None
    reason: str = ""


@dataclass(frozen=True)
class RepositorySnapshot:
    """Current local repository state plus fresh remote evidence."""

    root: Path
    branch: str
    status_lines: tuple[str, ...]
    head: str
    base_head: str
    upstream: str | None
    ahead: int
    behind: int
    feature_branch_exists: bool
    remote: RemoteSnapshot

    @property
    def clean(self) -> bool:
        return not self.status_lines

    @property
    def on_base(self) -> bool:
        return self.branch == DEFAULT_BASE_BRANCH

    @property
    def base_is_current(self) -> bool:
        return (
            self.remote.state is RemoteState.FRESH
            and bool(self.base_head)
            and self.base_head == self.remote.base_head
        )


@dataclass(frozen=True)
class PullRequestSnapshot:
    """Normalized pull-request state."""

    number: int
    url: str
    state: str
    head_oid: str
    review: ReviewState
    mergeability: MergeabilityState
    checks: CheckState


@dataclass(frozen=True)
class PullRequestDiscovery:
    """Typed pull-request discovery result."""

    state: ObservationState
    matches: tuple[PullRequestSnapshot, ...] = ()
    reason: str = ""

    @property
    def match(self) -> PullRequestSnapshot | None:
        if self.state is ObservationState.FOUND and len(self.matches) == 1:
            return self.matches[0]
        return None


@dataclass(frozen=True)
class DeliveryRecommendation:
    """One resolved next action."""

    state: DeliveryState
    summary: str
    command: str | None = None
    explanation: str = ""


def run(command: list[str], *, cwd: Path) -> CommandResult:
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


def require_output(command: list[str], *, cwd: Path) -> str:
    """Run a command and require non-empty successful output."""
    result = run(command, cwd=cwd)
    if not result.ok or not result.stdout:
        detail = result.stderr or "command returned no output"
        raise RuntimeError(f"Command failed: {' '.join(command)}\n{detail}")
    return result.stdout


def repository_root() -> Path:
    """Locate the current Git repository."""
    result = run(["git", "rev-parse", "--show-toplevel"], cwd=Path.cwd())
    if not result.ok or not result.stdout:
        raise RuntimeError("Run this helper from inside the repository.")
    return Path(result.stdout).resolve()


def branch_exists(root: Path, branch: str) -> bool:
    """Return True when a local branch exists."""
    return run(
        ["git", "show-ref", "--verify", "--quiet", f"refs/heads/{branch}"],
        cwd=root,
    ).ok


def porcelain_status(root: Path) -> tuple[str, ...]:
    """Return full Git porcelain status lines."""
    result = run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=root,
    )
    if not result.ok:
        raise RuntimeError(result.stderr or "Git status is unavailable.")
    return tuple(line for line in result.stdout.splitlines() if line.strip())


def revision(root: Path, value: str) -> str:
    """Resolve a required local revision."""
    return require_output(["git", "rev-parse", value], cwd=root)


def upstream_name(root: Path) -> str | None:
    """Return the current upstream, or confirmed absence."""
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
    return result.stdout if result.ok and result.stdout else None


def observe_remote(root: Path, feature_branch: str) -> RemoteSnapshot:
    """Observe remote heads directly without trusting cached refs."""
    base_ref = f"refs/heads/{DEFAULT_BASE_BRANCH}"
    feature_ref = f"refs/heads/{feature_branch}"
    result = run(
        ["git", "ls-remote", "origin", base_ref, feature_ref],
        cwd=root,
    )
    if not result.ok:
        return RemoteSnapshot(
            state=RemoteState.UNAVAILABLE,
            reason=result.stderr or "Remote verification failed.",
        )

    observed: dict[str, str] = {}
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) != 2:
            return RemoteSnapshot(
                state=RemoteState.UNAVAILABLE,
                reason="Remote returned a malformed reference response.",
            )
        oid, ref = parts
        if ref not in {base_ref, feature_ref} or ref in observed:
            return RemoteSnapshot(
                state=RemoteState.UNAVAILABLE,
                reason="Remote returned an unexpected or duplicate reference.",
            )
        if len(oid) not in {40, 64} or any(
            character not in "0123456789abcdefABCDEF" for character in oid
        ):
            return RemoteSnapshot(
                state=RemoteState.UNAVAILABLE,
                reason="Remote returned a malformed object identifier.",
            )
        observed[ref] = oid

    if base_ref not in observed:
        return RemoteSnapshot(
            state=RemoteState.UNAVAILABLE,
            reason=f"Remote base branch {DEFAULT_BASE_BRANCH!r} was not observed.",
        )

    return RemoteSnapshot(
        state=RemoteState.FRESH,
        base_head=observed[base_ref],
        feature_head=observed.get(feature_ref),
    )


def ahead_behind(root: Path, remote_head: str | None) -> tuple[int, int]:
    """Compare HEAD with a freshly observed remote feature head."""
    if not remote_head:
        return 0, 0
    result = run(
        ["git", "rev-list", "--left-right", "--count", f"{remote_head}...HEAD"],
        cwd=root,
    )
    if not result.ok:
        raise RuntimeError(result.stderr or "Feature comparison failed.")
    parts = result.stdout.split()
    if len(parts) != 2 or not all(part.isdigit() for part in parts):
        raise RuntimeError("Feature comparison returned malformed output.")
    behind, ahead = (int(part) for part in parts)
    return ahead, behind


def snapshot(*, feature_branch: str) -> RepositorySnapshot:
    """Capture local state and direct remote evidence."""
    root = repository_root()
    branch = require_output(["git", "branch", "--show-current"], cwd=root)
    remote = observe_remote(root, feature_branch)
    ahead, behind = ahead_behind(root, remote.feature_head)
    return RepositorySnapshot(
        root=root,
        branch=branch,
        status_lines=porcelain_status(root),
        head=revision(root, "HEAD"),
        base_head=revision(root, DEFAULT_BASE_BRANCH),
        upstream=upstream_name(root),
        ahead=ahead,
        behind=behind,
        feature_branch_exists=branch_exists(root, feature_branch),
        remote=remote,
    )


def classify_checks(value: Any) -> CheckState:
    """Normalize a GitHub status-check rollup."""
    if not isinstance(value, list) or not value:
        return CheckState.UNAVAILABLE

    states: list[CheckState] = []
    for check in value:
        if not isinstance(check, dict):
            return CheckState.UNAVAILABLE
        status = str(check.get("status", "")).upper()
        conclusion = str(check.get("conclusion", "")).upper()
        context_state = str(check.get("state", "")).upper()

        if context_state:
            if context_state == "SUCCESS":
                states.append(CheckState.SUCCESSFUL)
            elif context_state in {"PENDING", "EXPECTED"}:
                states.append(CheckState.PENDING)
            elif context_state in {"FAILURE", "ERROR"}:
                states.append(CheckState.FAILED)
            else:
                return CheckState.UNAVAILABLE
            continue

        if status != "COMPLETED":
            if status in {"QUEUED", "IN_PROGRESS", "PENDING", "WAITING", "REQUESTED"}:
                states.append(CheckState.PENDING)
            else:
                return CheckState.UNAVAILABLE
            continue

        mapping = {
            "SUCCESS": CheckState.SUCCESSFUL,
            "NEUTRAL": CheckState.SUCCESSFUL,
            "SKIPPED": CheckState.SUCCESSFUL,
            "FAILURE": CheckState.FAILED,
            "STARTUP_FAILURE": CheckState.FAILED,
            "CANCELLED": CheckState.CANCELLED,
            "TIMED_OUT": CheckState.TIMED_OUT,
            "ACTION_REQUIRED": CheckState.ACTION_REQUIRED,
        }
        if conclusion not in mapping:
            return CheckState.UNAVAILABLE
        states.append(mapping[conclusion])

    for state in (
        CheckState.ACTION_REQUIRED,
        CheckState.TIMED_OUT,
        CheckState.CANCELLED,
        CheckState.FAILED,
        CheckState.PENDING,
        CheckState.UNAVAILABLE,
    ):
        if state in states:
            return state
    return CheckState.SUCCESSFUL


def classify_review(item: dict[str, Any]) -> ReviewState:
    """Normalize pull-request draft and review state."""
    is_draft = item.get("isDraft")
    if not isinstance(is_draft, bool):
        return ReviewState.UNAVAILABLE
    if is_draft:
        return ReviewState.DRAFT
    decision = item.get("reviewDecision", "")
    if decision is None:
        decision = ""
    if not isinstance(decision, str):
        return ReviewState.UNAVAILABLE
    return {
        "": ReviewState.READY_FOR_REVIEW,
        "REVIEW_REQUIRED": ReviewState.REVIEW_REQUIRED,
        "CHANGES_REQUESTED": ReviewState.CHANGES_REQUESTED,
        "APPROVED": ReviewState.APPROVED,
    }.get(decision.upper(), ReviewState.UNAVAILABLE)


def classify_mergeability(item: dict[str, Any]) -> MergeabilityState:
    """Normalize GitHub mergeability without optimistic defaults."""
    mergeable = item.get("mergeable")
    merge_state = item.get("mergeStateStatus")
    if not isinstance(mergeable, str) or not isinstance(merge_state, str):
        return MergeabilityState.UNAVAILABLE
    mergeable = mergeable.upper()
    merge_state = merge_state.upper()
    if mergeable == "CONFLICTING" or merge_state == "DIRTY":
        return MergeabilityState.CONFLICTING
    if mergeable == "UNKNOWN" or merge_state == "UNKNOWN":
        return MergeabilityState.UNKNOWN
    if mergeable != "MERGEABLE":
        return MergeabilityState.UNAVAILABLE
    if merge_state == "CLEAN":
        return MergeabilityState.CLEAN
    if merge_state in {"BLOCKED", "BEHIND", "UNSTABLE", "HAS_HOOKS", "DRAFT"}:
        return MergeabilityState.BLOCKED
    return MergeabilityState.UNAVAILABLE


def parse_pull_request(item: Any) -> PullRequestSnapshot:
    """Parse one complete pull-request response or raise ValueError."""
    if not isinstance(item, dict):
        raise ValueError("Pull-request response item is not an object.")
    number = item.get("number")
    url = item.get("url")
    state = item.get("state")
    head_oid = item.get("headRefOid")
    if not isinstance(number, int) or number <= 0:
        raise ValueError("Pull-request number is missing or malformed.")
    if not isinstance(url, str) or not url:
        raise ValueError("Pull-request URL is missing or malformed.")
    if state not in {"OPEN", "CLOSED", "MERGED"}:
        raise ValueError("Pull-request state is missing or malformed.")
    if not isinstance(head_oid, str) or not head_oid:
        raise ValueError("Pull-request head object is missing or malformed.")
    review = classify_review(item)
    mergeability = classify_mergeability(item)
    checks = classify_checks(item.get("statusCheckRollup"))
    if review is ReviewState.UNAVAILABLE:
        raise ValueError("Pull-request review state is unavailable.")
    return PullRequestSnapshot(
        number=number,
        url=url,
        state=state,
        head_oid=head_oid,
        review=review,
        mergeability=mergeability,
        checks=checks,
    )


def discover_pull_requests(root: Path, *, feature_branch: str) -> PullRequestDiscovery:
    """Discover zero, one, or multiple PRs without conflating failure and absence."""
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
            "all",
            "--limit",
            "100",
            "--json",
            (
                "number,url,state,isDraft,reviewDecision,mergeable,"
                "mergeStateStatus,statusCheckRollup,headRefOid"
            ),
        ],
        cwd=root,
    )
    if not result.ok:
        return PullRequestDiscovery(
            state=ObservationState.UNAVAILABLE,
            reason=result.stderr or "GitHub authentication or API request failed.",
        )
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        return PullRequestDiscovery(
            state=ObservationState.UNAVAILABLE,
            reason=f"GitHub returned malformed JSON: {exc}",
        )
    if not isinstance(payload, list):
        return PullRequestDiscovery(
            state=ObservationState.UNAVAILABLE,
            reason="GitHub pull-request response is not a list.",
        )
    if not payload:
        return PullRequestDiscovery(state=ObservationState.NOT_FOUND)
    try:
        matches = tuple(parse_pull_request(item) for item in payload)
    except ValueError as exc:
        return PullRequestDiscovery(
            state=ObservationState.UNAVAILABLE,
            reason=str(exc),
        )
    if len(matches) > 1:
        numbers = ", ".join(f"#{item.number}" for item in matches)
        return PullRequestDiscovery(
            state=ObservationState.AMBIGUOUS,
            matches=matches,
            reason=f"Multiple pull requests match this branch: {numbers}.",
        )
    return PullRequestDiscovery(state=ObservationState.FOUND, matches=matches)


def is_ancestor(root: Path, ancestor: str, descendant: str) -> bool | None:
    """Return ancestry, preserving command failure as unavailable."""
    result = run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=root,
    )
    if result.returncode == 0:
        return True
    if result.returncode == 1:
        return False
    return None


def shell_quote(value: str) -> str:
    """Return a safe double-quoted shell value."""
    escaped = (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("$", "\\$")
        .replace("`", "\\`")
    )
    return f'"{escaped}"'


def blocked(state: DeliveryState, summary: str, explanation: str = "") -> DeliveryRecommendation:
    """Create a recommendation with no mutating command."""
    return DeliveryRecommendation(state=state, summary=summary, explanation=explanation)


def post_merge_recommendation(
    repo: RepositorySnapshot,
    pr: PullRequestSnapshot,
    feature_branch: str,
) -> DeliveryRecommendation:
    """Recover deterministically from incomplete merge cleanup."""
    merged_into_remote = is_ancestor(repo.root, pr.head_oid, repo.remote.base_head)
    if merged_into_remote is not True:
        return blocked(
            DeliveryState.UNKNOWN,
            f"Pull request #{pr.number} is merged but its head is not verifiable on remote develop.",
            "Stop until merge ancestry can be confirmed.",
        )
    if not repo.on_base:
        if not repo.clean:
            return blocked(
                DeliveryState.POST_MERGE_CLEANUP,
                "The merged feature branch contains local changes.",
                "Preserve and review them before cleanup.",
            )
        return DeliveryRecommendation(
            state=DeliveryState.POST_MERGE_CLEANUP,
            summary=f"Pull request #{pr.number} is merged; return to develop.",
            command=f"git switch {DEFAULT_BASE_BRANCH}",
            explanation="Rerun the helper after this verified cleanup step.",
        )
    if not repo.clean:
        return blocked(DeliveryState.DEVELOP_DIRTY, "`develop` contains uncommitted changes.")
    if not repo.base_is_current:
        return DeliveryRecommendation(
            state=DeliveryState.DEVELOP_BEHIND,
            summary="Local `develop` does not match freshly observed `origin/develop`.",
            command=f"git pull --ff-only origin {DEFAULT_BASE_BRANCH}",
        )
    if repo.feature_branch_exists:
        return DeliveryRecommendation(
            state=DeliveryState.POST_MERGE_CLEANUP,
            summary="The merged local feature branch still exists.",
            command=f"git branch -d {feature_branch}",
            explanation="Branch deletion requires explicit Nilesh approval.",
        )
    if repo.remote.feature_head is not None:
        return DeliveryRecommendation(
            state=DeliveryState.POST_MERGE_CLEANUP,
            summary="The merged remote feature branch still exists.",
            command=f"git push origin --delete {feature_branch}",
            explanation="Branch deletion requires explicit Nilesh approval.",
        )
    return blocked(
        DeliveryState.COMPLETE,
        f"Pull request #{pr.number} is merged and repository cleanup is complete.",
    )


def open_pr_recommendation(pr: PullRequestSnapshot) -> DeliveryRecommendation:
    """Recommend from complete open-PR evidence."""
    if pr.review is ReviewState.DRAFT:
        return DeliveryRecommendation(
            state=DeliveryState.PR_DRAFT,
            summary=f"Pull request #{pr.number} is a draft.",
            command=f"gh pr ready {pr.number}",
            explanation="Marking a pull request ready requires explicit Nilesh approval.",
        )
    if pr.review is ReviewState.CHANGES_REQUESTED:
        return blocked(
            DeliveryState.PR_CHANGES_REQUESTED,
            f"Pull request #{pr.number} has changes requested.",
            "Inspect and resolve review feedback before advancing.",
        )
    if pr.review is ReviewState.REVIEW_REQUIRED:
        return blocked(
            DeliveryState.PR_REVIEW_REQUIRED,
            f"Pull request #{pr.number} requires review.",
        )

    check_states = {
        CheckState.UNAVAILABLE: DeliveryState.PR_CHECKS_UNAVAILABLE,
        CheckState.PENDING: DeliveryState.PR_CHECKS_PENDING,
        CheckState.FAILED: DeliveryState.PR_CHECKS_FAILED,
        CheckState.CANCELLED: DeliveryState.PR_CHECKS_CANCELLED,
        CheckState.TIMED_OUT: DeliveryState.PR_CHECKS_TIMED_OUT,
        CheckState.ACTION_REQUIRED: DeliveryState.PR_CHECKS_ACTION_REQUIRED,
    }
    if pr.checks in check_states:
        command = (
            f"gh pr checks {pr.number} --watch"
            if pr.checks is CheckState.PENDING
            else f"gh pr checks {pr.number}"
        )
        return DeliveryRecommendation(
            state=check_states[pr.checks],
            summary=f"Pull request #{pr.number} checks are {pr.checks.value}.",
            command=command,
            explanation=(
                "CI monitoring is read-only and may continue automatically."
                if pr.checks is CheckState.PENDING
                else "Do not merge until successful checks are confirmed."
            ),
        )

    if pr.mergeability is MergeabilityState.CONFLICTING:
        return blocked(
            DeliveryState.PR_MERGE_CONFLICT,
            f"Pull request #{pr.number} has merge conflicts.",
        )
    if pr.mergeability is MergeabilityState.UNKNOWN:
        return blocked(
            DeliveryState.PR_MERGEABILITY_UNKNOWN,
            f"Pull request #{pr.number} mergeability is unknown.",
        )
    if pr.mergeability is MergeabilityState.UNAVAILABLE:
        return blocked(
            DeliveryState.PR_MERGEABILITY_UNKNOWN,
            f"Pull request #{pr.number} mergeability is unavailable.",
        )
    if pr.mergeability is MergeabilityState.BLOCKED:
        if pr.review is ReviewState.READY_FOR_REVIEW:
            return blocked(
                DeliveryState.PR_READY_FOR_REVIEW,
                f"Pull request #{pr.number} is ready for review but merge remains blocked.",
            )
        return blocked(
            DeliveryState.PR_MERGE_BLOCKED,
            f"Pull request #{pr.number} is blocked from merge.",
        )
    if pr.review not in {ReviewState.READY_FOR_REVIEW, ReviewState.APPROVED}:
        return blocked(
            DeliveryState.UNKNOWN,
            f"Pull request #{pr.number} review state is unavailable.",
        )
    return DeliveryRecommendation(
        state=DeliveryState.READY_TO_MERGE,
        summary=f"Pull request #{pr.number} is ready for merge.",
        command=f"gh pr merge {pr.number} --merge --delete-branch",
        explanation="Merge and branch deletion require explicit Nilesh approval.",
    )


def recommend(*, feature_branch: str, commit_message: str, pr_title: str) -> DeliveryRecommendation:
    """Return the next safe capability-delivery action."""
    repo = snapshot(feature_branch=feature_branch)
    if repo.remote.state is RemoteState.UNAVAILABLE:
        return blocked(
            DeliveryState.REMOTE_VERIFICATION_FAILED,
            "Remote repository state is unavailable.",
            repo.remote.reason or "Stop until remote freshness can be verified.",
        )

    discovery = discover_pull_requests(repo.root, feature_branch=feature_branch)
    if discovery.state is ObservationState.UNAVAILABLE:
        return blocked(
            DeliveryState.PR_DISCOVERY_UNAVAILABLE,
            "Pull-request state is unavailable.",
            discovery.reason,
        )
    if discovery.state is ObservationState.AMBIGUOUS:
        return blocked(
            DeliveryState.PR_DISCOVERY_AMBIGUOUS,
            "Multiple pull requests match the feature branch.",
            discovery.reason,
        )
    pr = discovery.match

    if pr is not None and pr.state == "MERGED":
        return post_merge_recommendation(repo, pr, feature_branch)
    if pr is not None and pr.state == "CLOSED":
        return blocked(
            DeliveryState.PR_CLOSED,
            f"Pull request #{pr.number} is closed without a confirmed merge.",
            "Stop and decide whether the branch should be resumed or replaced.",
        )

    if repo.on_base:
        if not repo.clean:
            return blocked(
                DeliveryState.DEVELOP_DIRTY,
                "`develop` contains uncommitted changes.",
                "Resolve or preserve those changes before starting another capability.",
            )
        if not repo.base_is_current:
            return DeliveryRecommendation(
                state=DeliveryState.DEVELOP_BEHIND,
                summary="Local `develop` does not match freshly observed `origin/develop`.",
                command=f"git pull --ff-only origin {DEFAULT_BASE_BRANCH}",
            )
        if repo.feature_branch_exists:
            return DeliveryRecommendation(
                state=DeliveryState.READY_FOR_BRANCH,
                summary="The feature branch already exists.",
                command=f"git switch {feature_branch}",
            )
        if repo.remote.feature_head is not None:
            return DeliveryRecommendation(
                state=DeliveryState.READY_FOR_BRANCH,
                summary="The feature branch exists on origin.",
                command=(
                    f"git switch --track -c {feature_branch} "
                    f"origin/{feature_branch}"
                ),
            )
        if pr is not None:
            return blocked(
                DeliveryState.UNKNOWN,
                f"Pull request #{pr.number} exists but its feature branch is unavailable.",
            )
        return DeliveryRecommendation(
            state=DeliveryState.READY_FOR_BRANCH,
            summary="The repository is ready for a new feature branch.",
            command=f"git switch -c {feature_branch}",
        )

    if repo.branch != feature_branch:
        return blocked(
            DeliveryState.UNKNOWN,
            f"Current branch is `{repo.branch}`, not `{feature_branch}` or `develop`.",
            "Verify the intended capability before continuing.",
        )

    if pr is not None and repo.remote.feature_head is None:
        return blocked(
            DeliveryState.REMOTE_VERIFICATION_FAILED,
            f"Pull request #{pr.number} exists but the remote feature branch was not observed.",
        )
    if pr is not None and repo.remote.feature_head != pr.head_oid:
        return blocked(
            DeliveryState.REMOTE_VERIFICATION_FAILED,
            f"Pull request #{pr.number} head does not match the remote feature branch.",
        )

    if repo.behind > 0:
        return blocked(
            DeliveryState.FEATURE_OUT_OF_SYNC,
            "The local feature branch is behind or diverged from the remote branch.",
        )

    if repo.clean and repo.ahead > 0:
        return DeliveryRecommendation(
            state=DeliveryState.READY_TO_PUSH,
            summary="The feature branch contains unpushed commits.",
            command=f"git push origin {feature_branch}",
        )

    if not repo.clean:
        staged = run(["git", "diff", "--cached", "--quiet"], cwd=repo.root)
        unstaged = run(["git", "diff", "--quiet"], cwd=repo.root)
        untracked = any(line.startswith("??") for line in repo.status_lines)
        has_staged = not staged.ok
        has_unstaged = not unstaged.ok or untracked
        if has_staged and not has_unstaged:
            return DeliveryRecommendation(
                state=DeliveryState.READY_TO_COMMIT,
                summary="All current changes are staged.",
                command=f"git commit -m {shell_quote(commit_message)}",
            )
        return DeliveryRecommendation(
            state=DeliveryState.READY_TO_STAGE,
            summary="The feature branch contains uncommitted changes.",
            command="git add -A && git diff --cached --name-status",
            explanation="Staging requires explicit Nilesh approval and staged review.",
        )

    if pr is not None:
        return open_pr_recommendation(pr)

    if repo.head == repo.base_head and repo.remote.feature_head is None:
        return blocked(
            DeliveryState.READY_FOR_WORK,
            "The feature branch is ready for capability implementation.",
        )
    if repo.remote.feature_head is None:
        return DeliveryRecommendation(
            state=DeliveryState.READY_TO_PUSH,
            summary="The committed feature branch is not published.",
            command=f"git push --set-upstream origin {feature_branch}",
        )
    if repo.head != repo.remote.feature_head:
        return blocked(
            DeliveryState.FEATURE_OUT_OF_SYNC,
            "Local and remote feature branch heads do not agree.",
        )
    return DeliveryRecommendation(
        state=DeliveryState.READY_FOR_PR,
        summary="The branch is published and no pull request was found.",
        command=(
            "gh pr create \\\n"
            f"  --base {DEFAULT_BASE_BRANCH} \\\n"
            f"  --head {feature_branch} \\\n"
            f"  --title {shell_quote(pr_title)}"
        ),
        explanation="Creating a pull request requires explicit Nilesh approval.",
    )


def print_recommendation(recommendation: DeliveryRecommendation) -> None:
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
        description="Determine the next safe capability-delivery action."
    )
    parser.add_argument("--branch", required=True, help="Resolved feature branch name.")
    parser.add_argument("--commit-message", required=True, help="Resolved commit message.")
    parser.add_argument("--pr-title", required=True, help="Resolved pull-request title.")
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
    except (RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
