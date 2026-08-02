#!/usr/bin/env python3
"""
Capability Delivery Workflow Bootstrap

Preview:

    python3 scripts/bootstrap_capability_delivery_workflow.py

Apply local repository changes:

    python3 scripts/bootstrap_capability_delivery_workflow.py --apply

Synchronize GitHub planning after local validation:

    python3 scripts/bootstrap_capability_delivery_workflow.py \
        --sync-project

This bootstrap establishes a repeatable capability delivery process.

It creates:

- Capability Delivery Workflow documentation
- A state-aware capability delivery helper
- Workflow tests
- A capability demo
- An engineering ADR
- A same-day Architecture Baseline revision
- Complementary repository documentation updates

The workflow covers:

1. Return to clean develop
2. Create or resume a feature branch
3. Preview a bootstrap
4. Apply changes safely
5. Recover from partial application
6. Validate locally
7. Synchronize GitHub planning
8. Review repository state
9. Stage changes
10. Review staged changes
11. Commit
12. Push
13. Create or discover a pull request
14. Check CI
15. Merge and delete the branch
16. Return to develop
17. Verify the clean baseline
18. Close the capability

The helper never commits, pushes, creates a pull request, or merges
without an explicit command.

Preview mode changes nothing.

--apply changes local repository files only.

--sync-project updates GitHub planning only after local validation.

This bootstrap does not commit, push, merge, or create a pull request.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import textwrap
import time
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------
# Repository configuration
# ---------------------------------------------------------------------

EXPECTED_REPOSITORY = "Ramrattan-AI-Editorial-Studio"

EXPECTED_REMOTE_FRAGMENT = (
    "RamrattanN/Ramrattan-AI-Editorial-Studio"
)

EXPECTED_BRANCH = (
    "feature/capability-delivery-workflow"
)

OWNER = "RamrattanN"

REPOSITORY = (
    "RamrattanN/Ramrattan-AI-Editorial-Studio"
)

PROJECT_NUMBER = 1

PROJECT_ID = "PVT_kwHOAuXHyM4BfHW9"

STATUS_FIELD_ID = (
    "PVTSSF_lAHOAuXHyM4BfHW9zhZclQY"
)

STATUS_OPTIONS = {
    "Todo": "f75ad846",
    "In Progress": "47fc9ee4",
    "Done": "98236657",
}

SCRIPT_RELATIVE_PATH = (
    "scripts/bootstrap_capability_delivery_workflow.py"
)

SCRIPT_SENTINEL = (
    "CAPABILITY_DELIVERY_WORKFLOW_BOOTSTRAP_COMPLETE"
)

CAPABILITY_ISSUE_TITLE = (
    "Engineering - Implement the Capability Delivery Workflow"
)

PREVIOUS_CAPABILITY_ISSUE_TITLE = (
    "Capability 007 - Implement Editorial Intake "
    "and Source Assessment"
)

ARCHITECTURE_BASELINE_VERSION = "2026.08.01v04"


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def clean(value: str) -> str:
    """Dedent text and ensure one trailing newline."""
    return textwrap.dedent(value).strip() + "\n"


def normalize_markdown(value: str) -> str:
    """Normalize Markdown for resilient validation."""
    return " ".join(
        value.replace(">", " ").split()
    )


# ---------------------------------------------------------------------
# Engineering documentation
# ---------------------------------------------------------------------

CAPABILITY_DELIVERY_WORKFLOW = clean(
    """
    # Capability Delivery Workflow

    ## Status

    Active engineering standard.

    ## Purpose

    This workflow defines the repeatable delivery process for every
    repository capability.

    It exists to prevent recurring procedural mistakes, reduce manual
    interpretation, preserve repository integrity, and ensure that each
    capability returns the project to a clean, known baseline.

    ## Governing Principles

    ### State Before Action

    Determine the repository's current state before providing or
    executing the next command.

    ### Exact Commands

    Commands must be paste-ready.

    Do not provide unresolved placeholders when the required value is
    already known.

    Incorrect:

    ```text
    gh pr checks <PR_NUMBER>
    ```

    Correct:

    ```text
    gh pr checks 24
    ```

    ### One Transition at a Time

    Provide one safe next action after verifying the previous action.

    Do not issue a long sequence that assumes every intermediate step
    will succeed.

    ### Recover Rather Than Restart

    Bootstrap scripts must permit deterministic reruns after a partial
    application.

    Expected generated files and managed documentation updates are not
    treated as unexpected changes during recovery.

    ### Trust Repository Evidence

    Use:

    - Git status
    - current branch
    - commit history
    - GitHub issue state
    - Project item state
    - pull-request state
    - CI state

    Do not infer repository state when it can be verified.

    ### Finish Where We Started

    A capability is not complete until:

    - the pull request is merged,
    - the feature branch is deleted locally,
    - the feature branch is deleted remotely,
    - the repository is back on `develop`,
    - `develop` matches `origin/develop`,
    - the working tree is clean,
    - the merge commit is visible,
    - and GitHub planning reflects reality.

    ## Capability Lifecycle

    ### Phase 1 - Establish the Baseline

    Confirm:

    ```bash
    git status
    git branch --show-current
    git log --oneline --decorate -3
    ```

    Required state:

    - branch is `develop`,
    - working tree is clean,
    - local `develop` matches `origin/develop`,
    - latest expected merge is present.

    If `develop` is behind:

    ```bash
    git pull --ff-only origin develop
    ```

    Do not create a feature branch from an uncertain baseline.

    ### Phase 2 - Create or Resume the Feature Branch

    First check whether the branch exists:

    ```bash
    git branch --list <branch-name>
    ```

    If absent:

    ```bash
    git switch -c <branch-name>
    ```

    If present:

    ```bash
    git switch <branch-name>
    ```

    Verify:

    ```bash
    git branch --show-current
    git log --oneline --decorate -3
    ```

    ### Phase 3 - Create the Bootstrap

    Repository-oriented instructions should use:

    > Create this file under `scripts`:

    followed by the filename.

    Avoid unnecessary path-oriented phrasing when the containing
    repository folder is already known.

    ### Phase 4 - Preview

    Run the capability bootstrap without flags.

    Preview mode must:

    - verify repository identity,
    - verify branch identity,
    - verify script integrity,
    - inspect the working tree,
    - list new files,
    - list managed-document updates,
    - list decisions being implemented,
    - and change nothing.

    ### Phase 5 - Apply

    Run:

    ```bash
    python3 scripts/<bootstrap-file>.py --apply
    ```

    Apply mode must:

    - write deterministic files,
    - update complementary documents,
    - validate required files,
    - validate canonical product language,
    - compile runtime and tests,
    - run the complete test suite,
    - run repository validation,
    - and display Git status.

    ### Phase 6 - Partial-Apply Recovery

    A bootstrap must tolerate its own expected changes after a failed
    validation.

    Working-tree validation must permit:

    - the bootstrap file,
    - declared new files,
    - declared managed-document updates.

    It must reject unrelated changes.

    Git porcelain parsing must:

    - preserve both status columns,
    - use `--untracked-files=all`,
    - and expand untracked directories into individual paths.

    ### Phase 7 - GitHub Synchronization

    Run:

    ```bash
    python3 scripts/<bootstrap-file>.py --sync-project
    ```

    Synchronization must:

    - rerun local validation,
    - verify GitHub authentication,
    - verify the expected Project,
    - reuse existing issues,
    - prevent duplicate issue creation,
    - retry delayed Project item propagation,
    - mark the previous capability Done where appropriate,
    - mark the current capability In Progress,
    - and update Project summary material.

    GitHub synchronization must not commit or push repository files.

    ### Phase 8 - Review Local Changes

    Run:

    ```bash
    git status --short
    ```

    Confirm:

    - only expected files changed,
    - no caches are present,
    - no editor backups are present,
    - no temporary files are present,
    - no unrelated files are present.

    ### Phase 9 - Stage

    Run:

    ```bash
    git add -A
    git diff --cached --name-status
    ```

    Review the entire staged set.

    Pager output such as `(END)` is not a Git entry.

    Exit the pager using:

    ```text
    q
    ```

    ### Phase 10 - Commit

    Use a capability-scoped message.

    Examples:

    ```text
    feat: implement Editorial Workspace intake and source assessment
    ```

    ```text
    docs: establish the Version 0.9 constitutional foundation
    ```

    ```text
    chore: establish the capability delivery workflow
    ```

    Verify the commit output before continuing.

    ### Phase 11 - Push

    Run the exact branch command:

    ```bash
    git push --set-upstream origin <resolved-branch-name>
    ```

    Terminal output is not a command.

    Do not paste push output back into the shell.

    If the push reports success, do not repeat it unless verification
    shows a problem.

    ### Phase 12 - Create or Discover the Pull Request

    Create the pull request with resolved values:

    ```bash
    gh pr create \\
      --base develop \\
      --head <resolved-branch-name> \\
      --title "<resolved-title>"
    ```

    Capture the actual pull-request number from the returned URL.

    If a pull request may already exist, resolve it first:

    ```bash
    gh pr list \\
      --head <resolved-branch-name> \\
      --base develop \\
      --state open \\
      --json number,title,url
    ```

    ### Phase 13 - Check CI

    Use the actual pull-request number:

    ```bash
    gh pr checks 24
    ```

    Never use an unresolved placeholder when the number is known.

    Do not merge while checks are:

    - pending,
    - failing,
    - cancelled,
    - or unavailable.

    ### Phase 14 - Merge and Delete the Branch

    When CI passes:

    ```bash
    gh pr merge 24 --merge --delete-branch
    ```

    This should:

    - merge into `develop`,
    - delete the remote feature branch,
    - delete the local feature branch,
    - and switch the repository to `develop`.

    ### Phase 15 - Return to Baseline

    Verify:

    ```bash
    git status
    git branch --show-current
    git log --oneline --decorate -3
    ```

    Required state:

    - branch is `develop`,
    - working tree is clean,
    - local `develop` matches `origin/develop`,
    - latest merge is present.

    ### Phase 16 - Close the Capability

    Confirm:

    - capability issue is Done,
    - milestone is updated where relevant,
    - Project board reflects the merged state,
    - Version 1.0 Scorecard is current,
    - next capability remains Todo until work begins.

    ## Recovery Matrix

    | Condition | Required response |
    |---|---|
    | Branch already exists | Switch to it instead of recreating it |
    | Partial bootstrap apply | Permit expected changes and rerun |
    | Exact validation phrase missing | Repair source and generated file |
    | GitHub issue already exists | Reuse it |
    | Project item is delayed | Retry with bounded waits |
    | PR already exists | Discover and reuse it |
    | CI pending | Wait and recheck |
    | CI failing | Stop and diagnose |
    | Push output pasted into shell | Ignore harmless shell errors and verify push |
    | Pager shows `(END)` | Exit with `q` |
    | Develop is dirty after merge | Stop and investigate |
    | Local develop is behind | Pull with `--ff-only` |

    ## Never Events

    The workflow must never:

    - create a branch from an unverified baseline;
    - use unresolved placeholders when values are known;
    - merge before CI passes;
    - silently ignore unrelated working-tree changes;
    - create duplicate GitHub issues unnecessarily;
    - assume Project items appear immediately;
    - treat terminal output as executable commands;
    - declare a capability complete while still on a feature branch;
    - leave the repository in a dirty or ambiguous state;
    - or skip the return-to-`develop` verification.

    ## Completion Standard

    A capability is complete only when repository state, GitHub state,
    documentation, tests, and branch state all agree.
    """
)


ENGINEERING_ADR = clean(
    """
    # ADR-008 - Adopt the Capability Delivery Workflow

    ## Status

    Accepted

    ## Date

    2026-08-01

    ## Context

    Repeated capability delivery exposed recurring procedural failure
    modes:

    - attempting to create an existing branch,
    - bootstraps rejecting their own partial-apply changes,
    - exact-language validation failures requiring repeated repairs,
    - GitHub Project propagation delays,
    - unresolved pull-request placeholders,
    - terminal output accidentally pasted into the shell,
    - duplicated manual reasoning,
    - and inconsistent return-to-baseline verification.

    These failures were individually resolved, but the resolutions were
    not consistently carried forward.

    ## Decision

    Adopt a state-aware, repeatable Capability Delivery Workflow.

    The workflow governs:

    - baseline verification,
    - branch creation or resumption,
    - bootstrap preview,
    - safe application,
    - partial-apply recovery,
    - local validation,
    - GitHub synchronization,
    - staging,
    - commit,
    - push,
    - pull-request creation,
    - CI checking,
    - merge,
    - branch cleanup,
    - return to `develop`,
    - and capability closure.

    ## Tooling

    Add:

    - `docs/engineering/Capability_Delivery_Workflow.md`
    - `scripts/capability_delivery.py`
    - `tests/test_capability_delivery_workflow.py`

    ## Command Standard

    Guidance must provide exact, paste-ready commands.

    When a value is known, placeholders are prohibited.

    ## State Model

    The helper determines the next safe action from repository and
    GitHub evidence.

    It does not blindly execute the complete lifecycle.

    ## Safety Boundary

    The helper may inspect and recommend.

    Mutating commands require explicit Author invocation.

    ## Consequences

    ### Positive

    - Reduces repeated procedural mistakes
    - Makes recovery predictable
    - Makes capability completion auditable
    - Prevents premature merge
    - Prevents ambiguous branch state
    - Preserves clean repository history
    - Improves command quality
    - Carries lessons forward automatically

    ### Costs

    - Adds engineering process documentation
    - Adds workflow-maintenance responsibility
    - Requires future bootstraps to comply
    - May stop work when repository state is ambiguous

    ## Alternatives Rejected

    ### Continue with Manual Memory

    Rejected because previously solved problems recurred.

    ### Fully Automatic Release Script

    Rejected because branch, commit, push, pull-request, and merge
    actions should remain explicit and reviewable.

    ### Document the Process Without Tooling

    Rejected because documentation alone does not detect actual
    repository state.
    """
)


ARCHITECTURE_BASELINE = clean(
    f"""
    # Architecture Baseline - {ARCHITECTURE_BASELINE_VERSION}

    ## Status

    Current engineering delivery baseline.

    ## Baseline ID

    ```text
    {ARCHITECTURE_BASELINE_VERSION}
    ```

    ## Baseline Family

    ```text
    2026.08.01
    ```

    ## Supersedes

    ```text
    2026.08.01v03
    ```

    ## Reason for Revision

    Establish the Capability Delivery Workflow as the repeatable
    engineering process for all subsequent capabilities.

    ## Additions

    This baseline adds:

    - state-aware delivery guidance,
    - exact command resolution,
    - branch-existence detection,
    - partial-apply recovery requirements,
    - complete Git porcelain handling,
    - duplicate issue prevention,
    - Project propagation retries,
    - pull-request discovery,
    - CI gating,
    - merge cleanup,
    - and return-to-`develop` verification.

    ## Engineering Rule

    A capability is not complete when code is committed.

    It is complete when:

    - the pull request is merged,
    - the feature branch is removed,
    - `develop` is current,
    - the working tree is clean,
    - repository validation passes,
    - and GitHub planning agrees.

    ## Workflow Authority

    `docs/engineering/Capability_Delivery_Workflow.md` is the active
    engineering delivery standard.

    ## Constitutional Impact

    This baseline does not change the Product Constitution.

    It operationalizes the existing principles of:

    - trust,
    - consistency,
    - transparency,
    - stewardship,
    - and deliberate refinement.
    """
)


CAPABILITY_DEMO = clean(
    """
    # Capability Delivery Workflow Demo

    ## Objective

    Demonstrate that the repository can determine the next safe
    capability-delivery action without repeating previously solved
    mistakes.

    ## Scenario 1 - Clean Develop

    State:

    - branch is `develop`,
    - working tree is clean,
    - local and remote develop match.

    Expected recommendation:

    - create or resume the requested feature branch.

    ## Scenario 2 - Existing Feature Branch

    The requested branch already exists.

    Expected recommendation:

    - switch to the existing branch;
    - do not attempt to recreate it.

    ## Scenario 3 - Partial Bootstrap Application

    Expected capability files already exist after validation failure.

    Expected behaviour:

    - permit declared capability changes;
    - reject unrelated changes;
    - rerun deterministically.

    ## Scenario 4 - Pull Request Exists

    An open pull request already targets `develop`.

    Expected recommendation:

    - reuse the existing pull request;
    - resolve its number automatically.

    ## Scenario 5 - CI Pending

    Expected recommendation:

    - run the resolved `gh pr checks` command;
    - do not merge.

    ## Scenario 6 - CI Passed

    Expected recommendation:

    - provide the exact merge command using the resolved PR number.

    ## Scenario 7 - Merge Complete

    Expected verification:

    - branch is `develop`,
    - working tree is clean,
    - feature branch is absent locally,
    - local and remote develop match,
    - latest merge is present.

    ## Scenario 8 - Terminal Output Re-entered

    Push output is accidentally pasted into the shell.

    Expected interpretation:

    - shell errors are harmless if the push already succeeded;
    - verify branch tracking rather than repeating commands blindly.

    ## Completion

    The workflow is complete when:

    - documentation exists,
    - helper state detection works,
    - exact commands are produced,
    - tests pass,
    - and later capability delivery can use the process directly.
    """
)


# ---------------------------------------------------------------------
# Capability delivery helper
# ---------------------------------------------------------------------

CAPABILITY_DELIVERY_HELPER = clean(
    '''
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
                f"Command failed: {' '.join(command)}\\n"
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
            .replace("\\\\", "\\\\\\\\")
            .replace('"', '\\\\"')
            .replace("$", "\\$")
            .replace("`", "\\`")
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
                    "gh pr create \\\\\\n"
                    f"  --base {DEFAULT_BASE_BRANCH} \\\\\\n"
                    f"  --head {feature_branch} \\\\\\n"
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
    '''
)


# ---------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------

WORKFLOW_TESTS = clean(
    '''
    """Tests for the Capability Delivery Workflow."""

    from __future__ import annotations

    import importlib.util
    import sys
    import unittest
    from pathlib import Path
    from unittest.mock import patch


    ROOT = Path(__file__).resolve().parents[1]

    MODULE_PATH = (
        ROOT
        / "scripts"
        / "capability_delivery.py"
    )

    SPEC = importlib.util.spec_from_file_location(
        "capability_delivery",
        MODULE_PATH,
    )

    assert SPEC is not None
    assert SPEC.loader is not None

    delivery = importlib.util.module_from_spec(SPEC)
    sys.modules[SPEC.name] = delivery
    SPEC.loader.exec_module(delivery)


    def snapshot(
        *,
        branch: str,
        clean: bool = True,
        base_current: bool = True,
        upstream: str | None = None,
        ahead: int = 0,
        behind: int = 0,
        feature_exists: bool = False,
    ):
        return delivery.RepositorySnapshot(
            root=ROOT,
            branch=branch,
            status_lines=() if clean else (" M README.md",),
            head="head",
            base_head="base",
            remote_base_head=(
                "base" if base_current else "remote-base"
            ),
            upstream=upstream,
            ahead=ahead,
            behind=behind,
            feature_branch_exists=feature_exists,
        )


    class CapabilityDeliveryWorkflowTests(unittest.TestCase):
        def test_clean_develop_creates_branch(self) -> None:
            with patch.object(
                delivery,
                "snapshot",
                return_value=snapshot(
                    branch="develop",
                    feature_exists=False,
                ),
            ):
                result = delivery.recommend(
                    feature_branch="feature/test",
                    commit_message="feat: test",
                    pr_title="Test capability",
                )

            self.assertEqual(
                result.command,
                "git switch -c feature/test",
            )

        def test_existing_branch_is_resumed(self) -> None:
            with patch.object(
                delivery,
                "snapshot",
                return_value=snapshot(
                    branch="develop",
                    feature_exists=True,
                ),
            ):
                result = delivery.recommend(
                    feature_branch="feature/test",
                    commit_message="feat: test",
                    pr_title="Test capability",
                )

            self.assertEqual(
                result.command,
                "git switch feature/test",
            )

        def test_dirty_develop_blocks_branch_creation(
            self,
        ) -> None:
            with patch.object(
                delivery,
                "snapshot",
                return_value=snapshot(
                    branch="develop",
                    clean=False,
                ),
            ):
                result = delivery.recommend(
                    feature_branch="feature/test",
                    commit_message="feat: test",
                    pr_title="Test capability",
                )

            self.assertEqual(
                result.state,
                delivery.DeliveryState.DEVELOP_DIRTY,
            )
            self.assertIsNone(result.command)

        def test_outdated_develop_uses_ff_only(self) -> None:
            with patch.object(
                delivery,
                "snapshot",
                return_value=snapshot(
                    branch="develop",
                    base_current=False,
                ),
            ):
                result = delivery.recommend(
                    feature_branch="feature/test",
                    commit_message="feat: test",
                    pr_title="Test capability",
                )

            self.assertEqual(
                result.command,
                "git pull --ff-only origin develop",
            )

        def test_clean_unpublished_feature_pushes(
            self,
        ) -> None:
            with patch.object(
                delivery,
                "snapshot",
                return_value=snapshot(
                    branch="feature/test",
                    upstream=None,
                ),
            ), patch.object(
                delivery,
                "discover_pull_request",
                return_value=None,
            ):
                result = delivery.recommend(
                    feature_branch="feature/test",
                    commit_message="feat: test",
                    pr_title="Test capability",
                )

            self.assertEqual(
                result.command,
                (
                    "git push --set-upstream origin "
                    "feature/test"
                ),
            )

        def test_published_branch_creates_pr(self) -> None:
            with patch.object(
                delivery,
                "snapshot",
                return_value=snapshot(
                    branch="feature/test",
                    upstream="origin/feature/test",
                ),
            ), patch.object(
                delivery,
                "discover_pull_request",
                return_value=None,
            ):
                result = delivery.recommend(
                    feature_branch="feature/test",
                    commit_message="feat: test",
                    pr_title="Test capability",
                )

            self.assertIn(
                "--head feature/test",
                result.command or "",
            )
            self.assertNotIn(
                "<PR_NUMBER>",
                result.command or "",
            )

        def test_pending_pr_uses_resolved_number(
            self,
        ) -> None:
            pr = delivery.PullRequestSnapshot(
                number=42,
                url="https://example.test/pr/42",
                state="OPEN",
                merge_state_status="BLOCKED",
                checks_pending=1,
                checks_failed=0,
            )

            with patch.object(
                delivery,
                "snapshot",
                return_value=snapshot(
                    branch="feature/test",
                    upstream="origin/feature/test",
                ),
            ), patch.object(
                delivery,
                "discover_pull_request",
                return_value=pr,
            ):
                result = delivery.recommend(
                    feature_branch="feature/test",
                    commit_message="feat: test",
                    pr_title="Test capability",
                )

            self.assertEqual(
                result.command,
                "gh pr checks 42",
            )

        def test_failed_pr_does_not_merge(self) -> None:
            pr = delivery.PullRequestSnapshot(
                number=42,
                url="https://example.test/pr/42",
                state="OPEN",
                merge_state_status="BLOCKED",
                checks_pending=0,
                checks_failed=1,
            )

            with patch.object(
                delivery,
                "snapshot",
                return_value=snapshot(
                    branch="feature/test",
                    upstream="origin/feature/test",
                ),
            ), patch.object(
                delivery,
                "discover_pull_request",
                return_value=pr,
            ):
                result = delivery.recommend(
                    feature_branch="feature/test",
                    commit_message="feat: test",
                    pr_title="Test capability",
                )

            self.assertEqual(
                result.state,
                delivery.DeliveryState.PR_CHECKS_FAILED,
            )
            self.assertNotIn(
                "merge",
                result.command or "",
            )

        def test_green_pr_uses_resolved_merge_command(
            self,
        ) -> None:
            pr = delivery.PullRequestSnapshot(
                number=42,
                url="https://example.test/pr/42",
                state="OPEN",
                merge_state_status="CLEAN",
                checks_pending=0,
                checks_failed=0,
            )

            with patch.object(
                delivery,
                "snapshot",
                return_value=snapshot(
                    branch="feature/test",
                    upstream="origin/feature/test",
                ),
            ), patch.object(
                delivery,
                "discover_pull_request",
                return_value=pr,
            ):
                result = delivery.recommend(
                    feature_branch="feature/test",
                    commit_message="feat: test",
                    pr_title="Test capability",
                )

            self.assertEqual(
                result.command,
                (
                    "gh pr merge 42 "
                    "--merge --delete-branch"
                ),
            )

        def test_unknown_branch_stops(self) -> None:
            with patch.object(
                delivery,
                "snapshot",
                return_value=snapshot(
                    branch="feature/other",
                ),
            ):
                result = delivery.recommend(
                    feature_branch="feature/test",
                    commit_message="feat: test",
                    pr_title="Test capability",
                )

            self.assertEqual(
                result.state,
                delivery.DeliveryState.UNKNOWN,
            )
            self.assertIsNone(result.command)

        def test_documentation_exists(self) -> None:
            self.assertTrue(
                (
                    ROOT
                    / "docs"
                    / "engineering"
                    / "Capability_Delivery_Workflow.md"
                ).is_file()
            )

        def test_workflow_forbids_known_placeholders(
            self,
        ) -> None:
            content = (
                ROOT
                / "docs"
                / "engineering"
                / "Capability_Delivery_Workflow.md"
            ).read_text(encoding="utf-8")

            self.assertIn(
                "Do not provide unresolved placeholders",
                content,
            )
            self.assertIn(
                "gh pr checks 24",
                content,
            )

        def test_workflow_requires_return_to_develop(
            self,
        ) -> None:
            content = (
                ROOT
                / "docs"
                / "engineering"
                / "Capability_Delivery_Workflow.md"
            ).read_text(encoding="utf-8")

            self.assertIn(
                "Return to Baseline",
                content,
            )
            self.assertIn(
                "branch is `develop`",
                content,
            )

        def test_workflow_requires_partial_apply_recovery(
            self,
        ) -> None:
            content = (
                ROOT
                / "docs"
                / "engineering"
                / "Capability_Delivery_Workflow.md"
            ).read_text(encoding="utf-8")

            self.assertIn(
                "Partial-Apply Recovery",
                content,
            )
            self.assertIn(
                "--untracked-files=all",
                content,
            )


    if __name__ == "__main__":
        unittest.main()
    '''
)


# ---------------------------------------------------------------------
# Managed documentation updates
# ---------------------------------------------------------------------

START_HERE_BLOCK = clean(
    """
    ## Capability Delivery Workflow

    Before delivering a new capability, read:

    - `engineering/Capability_Delivery_Workflow.md`

    Use:

    - `scripts/capability_delivery.py`

    to determine the next safe repository action.

    Commands must be resolved and paste-ready.

    A capability is not complete until the repository has returned to a
    clean, current `develop` baseline.
    """
)


DEFINITION_OF_DONE_BLOCK = clean(
    """
    ## Delivery Workflow Completion

    A capability is not Done until:

    - local validation passes;
    - GitHub planning is synchronized;
    - all intended files are staged;
    - the capability commit exists;
    - the feature branch is pushed;
    - the pull request exists;
    - CI passes;
    - the pull request is merged;
    - the local feature branch is deleted;
    - the remote feature branch is deleted;
    - the repository is on `develop`;
    - local `develop` matches `origin/develop`;
    - the working tree is clean;
    - and the merge commit is visible.

    Use `docs/engineering/Capability_Delivery_Workflow.md` as the
    governing procedure.
    """
)


README_BLOCK = clean(
    """
    ## Capability Delivery

    Repository capabilities use a state-aware, repeatable delivery
    workflow.

    Read:

    - `docs/engineering/Capability_Delivery_Workflow.md`

    Inspect the next safe action with:

    ```bash
    python3 scripts/capability_delivery.py \\
      --branch "feature/example" \\
      --commit-message "feat: implement example" \\
      --pr-title "Example: Implement capability"
    ```

    The helper resolves branch and pull-request state before suggesting
    the next command.
    """
)


ROADMAP_BLOCK = clean(
    """
    ## Engineering Enablement - Capability Delivery Workflow

    Status:

    ```text
    Complete when merged
    ```

    Deliverables:

    - [x] Capability Delivery Workflow
    - [x] State-aware delivery helper
    - [x] Exact command resolution
    - [x] Existing-branch detection
    - [x] Partial-apply recovery standard
    - [x] Duplicate issue prevention standard
    - [x] Project propagation retry standard
    - [x] Pull-request discovery
    - [x] CI gating
    - [x] Merge cleanup
    - [x] Return-to-develop verification
    - [x] Automated tests
    - [x] Engineering ADR
    - [x] Architecture Baseline 2026.08.01v04

    Capability 008 must use this workflow.
    """
)


CHANGELOG_BLOCK = clean(
    f"""
    ## Engineering - Capability Delivery Workflow

    ### Added

    - Capability Delivery Workflow documentation
    - State-aware capability delivery helper
    - Existing-branch detection
    - Exact command resolution
    - Pull-request discovery
    - CI-state inspection
    - Resolved merge command generation
    - Return-to-`develop` completion standard
    - Capability delivery tests
    - ADR-008
    - Architecture Baseline {ARCHITECTURE_BASELINE_VERSION}
    - Capability delivery demo

    ### Changed

    - Capability completion now requires a clean, current `develop`
      baseline after merge
    - Known values must replace command placeholders
    - Bootstrap recovery must permit expected partial-apply changes
    - GitHub issue and Project synchronization must be idempotent
    - CI must pass before merge
    """
)


DECISION_LOG_BLOCK = clean(
    f"""
    ## Capability Delivery Workflow Decisions

    | Date | Level | Decision | Rationale |
    |---|---:|---|---|
    | 2026-08-01 | D4 | Adopt a repeatable Capability Delivery Workflow | Previously solved procedural problems recurred. |
    | 2026-08-01 | D4 | Require exact paste-ready commands | Unresolved placeholders caused avoidable shell errors. |
    | 2026-08-01 | D4 | Detect existing branches before creation | Existing branches should be resumed, not recreated. |
    | 2026-08-01 | D4 | Require partial-apply recovery | Validation failures must not force repository reset. |
    | 2026-08-01 | D4 | Reuse existing GitHub issues and pull requests | Duplicate planning artifacts reduce trust. |
    | 2026-08-01 | D4 | Retry delayed Project item propagation | GitHub Project items may not appear immediately. |
    | 2026-08-01 | D4 | Require CI before merge | Local success does not replace repository checks. |
    | 2026-08-01 | D4 | Require return-to-develop verification | A capability is incomplete while repository state remains ambiguous. |
    | 2026-08-01 | D4 | Create Architecture Baseline {ARCHITECTURE_BASELINE_VERSION} | The engineering delivery process is now part of the architecture baseline. |
    """
)


SCORECARD_BLOCK = clean(
    """
    ## Engineering Delivery Readiness

    | Area | Status | Evidence |
    |---|---|---|
    | Delivery workflow | Complete | `docs/engineering/Capability_Delivery_Workflow.md` |
    | State-aware helper | Complete | `scripts/capability_delivery.py` |
    | Exact command resolution | Complete | Automated tests |
    | Existing branch detection | Complete | Automated tests |
    | Pull-request discovery | Complete | Automated tests |
    | CI gating | Complete | Automated tests |
    | Merge cleanup standard | Complete | Delivery workflow |
    | Return-to-develop verification | Complete | Delivery workflow |
    """
)


CONSTITUTION_BLOCK = clean(
    """
    ## Engineering Stewardship

    Capability delivery must preserve trust in the repository.

    Engineering guidance should:

    - verify state before action,
    - provide exact commands,
    - recover safely,
    - avoid duplicate artifacts,
    - require validation before merge,
    - and return the repository to a clean baseline.

    Previously solved operational problems should be converted into
    repeatable process rather than rediscovered.
    """
)


MARKER_BLOCKS = {
    "docs/START_HERE.md": (
        "CAPABILITY_DELIVERY_START_HERE",
        START_HERE_BLOCK,
    ),
    "docs/architecture/Definition_of_Done.md": (
        "CAPABILITY_DELIVERY_DEFINITION_OF_DONE",
        DEFINITION_OF_DONE_BLOCK,
    ),
    "README.md": (
        "CAPABILITY_DELIVERY_README",
        README_BLOCK,
    ),
    "ROADMAP.md": (
        "CAPABILITY_DELIVERY_ROADMAP",
        ROADMAP_BLOCK,
    ),
    "CHANGELOG.md": (
        "CAPABILITY_DELIVERY_CHANGELOG",
        CHANGELOG_BLOCK,
    ),
    "docs/product/Decision_Log.md": (
        "CAPABILITY_DELIVERY_DECISION_LOG",
        DECISION_LOG_BLOCK,
    ),
    "docs/VERSION_ONE_SCORECARD.md": (
        "CAPABILITY_DELIVERY_SCORECARD",
        SCORECARD_BLOCK,
    ),
    "docs/constitution/Constitution.md": (
        "CAPABILITY_DELIVERY_CONSTITUTION",
        CONSTITUTION_BLOCK,
    ),
}

# CAPABILITY_008A2_DELIVERY_HARDENING_OVERRIDE_START
from bootstrap_capability008a2_delivery_hardening import (
    CAPABILITY_DELIVERY_HELPER as CAPABILITY_DELIVERY_HELPER_008A2,
    CAPABILITY_DELIVERY_WORKFLOW as CAPABILITY_DELIVERY_WORKFLOW_008A2,
    WORKFLOW_TESTS as WORKFLOW_TESTS_008A2,
)

CAPABILITY_DELIVERY_HELPER = CAPABILITY_DELIVERY_HELPER_008A2
CAPABILITY_DELIVERY_WORKFLOW = CAPABILITY_DELIVERY_WORKFLOW_008A2
WORKFLOW_TESTS = WORKFLOW_TESTS_008A2
# Delegated templates include ADR-014 approval profiles and consolidation.
# CAPABILITY_008A2_DELIVERY_HARDENING_OVERRIDE_END

# RC1_CHECKPOINT_AUTHORIZATION_HARDENING_OWNER_SYNC_START
from bootstrap_rc1_checkpoint_authorization_hardening import (
    harden_helper as _rc1_harden_helper,
    harden_tests as _rc1_harden_tests,
    harden_workflow as _rc1_harden_workflow,
)

CAPABILITY_DELIVERY_HELPER = _rc1_harden_helper(CAPABILITY_DELIVERY_HELPER)
CAPABILITY_DELIVERY_WORKFLOW = _rc1_harden_workflow(CAPABILITY_DELIVERY_WORKFLOW)
WORKFLOW_TESTS = _rc1_harden_tests(WORKFLOW_TESTS)
# RC1_CHECKPOINT_AUTHORIZATION_HARDENING_OWNER_SYNC_END

NEW_FILES = {
    (
        "docs/engineering/"
        "Capability_Delivery_Workflow.md"
    ):
        CAPABILITY_DELIVERY_WORKFLOW,

    "scripts/capability_delivery.py":
        CAPABILITY_DELIVERY_HELPER,

    (
        "tests/"
        "test_capability_delivery_workflow.py"
    ):
        WORKFLOW_TESTS,

    (
        "docs/architecture/adr/"
        "ADR-008-adopt-the-capability-delivery-workflow.md"
    ):
        ENGINEERING_ADR,

    (
        "docs/architecture/baselines/"
        "Architecture_Baseline_2026.08.01v04.md"
    ):
        ARCHITECTURE_BASELINE,

    (
        "docs/demos/"
        "Capability-Delivery-Workflow.md"
    ):
        CAPABILITY_DEMO,
}


# ---------------------------------------------------------------------
# Errors and command execution
# ---------------------------------------------------------------------

class CapabilityError(RuntimeError):
    """Raised when the workflow bootstrap cannot proceed safely."""


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


def output(
    command: list[str],
    *,
    cwd: Path,
) -> str:
    """Return stripped command output."""
    return run(
        command,
        cwd=cwd,
        capture=True,
    ).stdout.strip()


def json_output(
    command: list[str],
    *,
    cwd: Path,
) -> Any:
    """Run a command and parse JSON output."""
    raw = output(command, cwd=cwd)

    if not raw:
        return {}

    return json.loads(raw)


# ---------------------------------------------------------------------
# Repository checks
# ---------------------------------------------------------------------

def repository_root() -> Path:
    """Locate and verify the expected repository."""
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
        raise CapabilityError(
            "Run this script from inside the cloned repository."
        ) from exc

    if root.name != EXPECTED_REPOSITORY:
        raise CapabilityError(
            f"Expected repository '{EXPECTED_REPOSITORY}', "
            f"found '{root.name}'."
        )

    remote = output(
        ["git", "remote", "get-url", "origin"],
        cwd=root,
    )

    if EXPECTED_REMOTE_FRAGMENT not in remote:
        raise CapabilityError(
            "The origin remote does not match the expected repository."
        )

    return root


def verify_branch(root: Path) -> None:
    """Require the workflow feature branch."""
    branch = output(
        ["git", "branch", "--show-current"],
        cwd=root,
    )

    print(f"Branch: {branch}")

    if branch != EXPECTED_BRANCH:
        raise CapabilityError(
            f"Expected branch '{EXPECTED_BRANCH}', "
            f"found '{branch}'."
        )


def verify_script_integrity() -> None:
    """Detect incomplete or damaged paste."""
    path = Path(__file__).resolve()
    content = path.read_text(encoding="utf-8")

    if SCRIPT_SENTINEL not in content:
        raise CapabilityError(
            "The script appears incomplete. "
            "The final integrity sentinel is missing."
        )

    try:
        compile(
            content,
            str(path),
            "exec",
        )

    except SyntaxError as exc:
        raise CapabilityError(
            f"The pasted script is not syntactically complete: {exc}"
        ) from exc

    print("Script integrity check passed.")


def working_tree_lines(root: Path) -> list[str]:
    """Return full Git porcelain lines."""
    result = run(
        [
            "git",
            "status",
            "--porcelain",
            "--untracked-files=all",
        ],
        cwd=root,
        capture=True,
    )

    return [
        line
        for line in result.stdout.splitlines()
        if line.strip()
    ]


def verify_expected_working_tree(root: Path) -> None:
    """Permit only expected workflow capability changes."""
    expected_paths = (
        set(NEW_FILES)
        | set(MARKER_BLOCKS)
        | {SCRIPT_RELATIVE_PATH}
    )

    unexpected: list[str] = []

    for line in working_tree_lines(root):
        relative = line[3:].strip()

        if " -> " in relative:
            relative = relative.split(" -> ", 1)[1].strip()

        if relative not in expected_paths:
            unexpected.append(line)

    if unexpected:
        raise CapabilityError(
            "Unexpected working-tree changes exist:\n"
            + "\n".join(unexpected)
            + "\n\nOnly expected Capability Delivery Workflow "
            "files and managed-document updates are allowed."
        )

    print(
        "Working tree contains only expected "
        "Capability Delivery Workflow changes."
    )


# ---------------------------------------------------------------------
# File operations
# ---------------------------------------------------------------------

def managed_block(
    marker_name: str,
    content: str,
) -> str:
    """Create one marker-managed Markdown block."""
    start = f"<!-- {marker_name}_START -->"
    end = f"<!-- {marker_name}_END -->"

    return (
        start
        + "\n\n"
        + content.rstrip()
        + "\n\n"
        + end
    )


def upsert_managed_block(
    path: Path,
    marker_name: str,
    content: str,
) -> None:
    """Insert or replace one managed Markdown block."""
    if not path.is_file():
        raise CapabilityError(
            f"Missing required existing document: {path}"
        )

    original = path.read_text(encoding="utf-8")

    start = f"<!-- {marker_name}_START -->"
    end = f"<!-- {marker_name}_END -->"

    has_start = start in original
    has_end = end in original

    if has_start != has_end:
        raise CapabilityError(
            f"Incomplete managed marker pair in {path}."
        )

    block = managed_block(
        marker_name,
        content,
    )

    if has_start:
        before = original.split(start, 1)[0].rstrip()
        after = original.split(end, 1)[1].lstrip()

        updated = before + "\n\n" + block

        if after:
            updated += "\n\n" + after

        updated = updated.rstrip() + "\n"

    else:
        updated = (
            original.rstrip()
            + "\n\n"
            + block
            + "\n"
        )

    path.write_text(
        updated,
        encoding="utf-8",
    )


def write_new_files(root: Path) -> None:
    """Write deterministic workflow files."""
    for relative, content in NEW_FILES.items():
        destination = root / relative

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        destination.write_text(
            content,
            encoding="utf-8",
        )

        print(f"Wrote {relative}")


def update_existing_documents(root: Path) -> None:
    """Update complementary repository documents."""
    for relative, (
        marker_name,
        content,
    ) in MARKER_BLOCKS.items():
        path = root / relative

        upsert_managed_block(
            path,
            marker_name,
            content,
        )

        print(f"Updated {relative}")


def apply_local_changes(root: Path) -> None:
    """Apply the workflow capability locally."""
    write_new_files(root)
    update_existing_documents(root)

    print()
    print(
        "Capability Delivery Workflow files have been written."
    )


# ---------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------

REQUIRED_FILES = tuple(NEW_FILES.keys())


def validate_required_files(root: Path) -> None:
    """Confirm every required file exists."""
    missing = [
        relative
        for relative in REQUIRED_FILES
        if not (root / relative).is_file()
    ]

    if missing:
        raise CapabilityError(
            "Missing Capability Delivery Workflow files:\n"
            + "\n".join(
                f"  - {relative}"
                for relative in missing
            )
        )

    print(
        "All required Capability Delivery Workflow files are present."
    )


def validate_product_language(root: Path) -> None:
    """Validate central workflow decisions."""
    checks: dict[str, tuple[str, ...]] = {
        (
            "docs/engineering/"
            "Capability_Delivery_Workflow.md"
        ): (
            "State Before Action",
            "Exact Commands",
            "Delegated Approval Profiles",
            "Change Consolidation",
            "Partial-Apply Recovery",
            "Return to Baseline",
            "gh pr checks 24",
            "gh pr merge 24 --merge --delete-branch",
            "branch is `develop`",
        ),

        "scripts/capability_delivery.py": (
            "class DeliveryState",
            "class ApprovalProfile",
            "Next profile boundary",
            "discover_pull_request",
            "git switch -c",
            "gh pr checks",
            "--merge --delete-branch",
        ),

        (
            "docs/architecture/adr/"
            "ADR-008-adopt-the-capability-delivery-workflow.md"
        ): (
            "Adopt a state-aware, repeatable "
            "Capability Delivery Workflow",
            "exact, paste-ready commands",
            "return to `develop`",
        ),

        (
            "docs/architecture/baselines/"
            "Architecture_Baseline_2026.08.01v04.md"
        ): (
            ARCHITECTURE_BASELINE_VERSION,
            "Capability Delivery Workflow",
            "return-to-`develop` verification",
        ),
    }

    for relative, phrases in checks.items():
        path = root / relative

        content = normalize_markdown(
            path.read_text(encoding="utf-8")
        )

        for phrase in phrases:
            if phrase not in content:
                raise CapabilityError(
                    f"Expected phrase '{phrase}' "
                    f"in {relative}."
                )

    print(
        "Capability Delivery Workflow language validation passed."
    )


def run_repository_validation(root: Path) -> None:
    """Run compilation, tests, and repository validation."""
    run(
        [
            sys.executable,
            "-m",
            "compileall",
            "-q",
            "studio",
            "scripts",
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
        [
            sys.executable,
            "studio.py",
            "validate",
        ],
        cwd=root,
    )

    print(
        "Capability Delivery Workflow repository validation passed."
    )


def show_status(root: Path) -> None:
    """Display resulting repository changes."""
    print("\nGit status:")

    run(
        ["git", "status", "--short"],
        cwd=root,
    )

    print("\nTracked change summary:")

    run(
        ["git", "diff", "--stat"],
        cwd=root,
    )


# ---------------------------------------------------------------------
# Preview
# ---------------------------------------------------------------------

def preview() -> None:
    """Show planned changes without modifying files."""
    print()
    print("Capability Delivery Workflow preview:")
    print()

    print("New files:")

    for relative in NEW_FILES:
        print(f"  - {relative}")

    print("\nManaged documentation updates:")

    for relative in MARKER_BLOCKS:
        print(f"  - {relative}")

    print("\nDecisions being implemented:")

    decisions = (
        "Adopt a repeatable Capability Delivery Workflow",
        "Verify state before action",
        "Provide exact paste-ready commands",
        "Detect existing branches before creation",
        "Support deterministic partial-apply recovery",
        "Preserve complete Git porcelain status columns",
        "Expand untracked directories",
        "Reuse existing GitHub issues",
        "Reuse existing pull requests",
        "Retry delayed Project item propagation",
        "Require local validation",
        "Require CI before merge",
        "Merge with branch deletion",
        "Return to clean develop",
        "Confirm local and remote develop match",
        "Create Architecture Baseline 2026.08.01v04",
    )

    for decision in decisions:
        print(f"  - {decision}")

    print("\nPreview mode changes nothing.")

    print("\nApply local files with:")

    print(
        "  python3 scripts/"
        "bootstrap_capability_delivery_workflow.py "
        "--apply"
    )


# ---------------------------------------------------------------------
# GitHub synchronization
# ---------------------------------------------------------------------

PROJECT_DESCRIPTION = (
    "Version 1.0 capability roadmap governed by the Constitution, "
    "Canonical Vocabulary, Editorial Integrity, Canonical Editorial "
    "Session, and the repeatable Capability Delivery Workflow."
)


PROJECT_README = f"""# Ramrattan AI Editorial Studio

## Governing principle

Trust is our most valuable feature.

## Engineering delivery

All capabilities use the repeatable Capability Delivery Workflow.

The workflow requires:

- verified baseline
- exact commands
- safe bootstrap recovery
- local validation
- GitHub synchronization
- staged review
- commit
- push
- pull request
- CI
- merge
- branch deletion
- return to clean develop

## Current engineering baseline

{ARCHITECTURE_BASELINE_VERSION}

## Next product capability

Capability 008 - Guided Editorial Session, Editorial Intent, and
Editorial Coherence.
"""


CAPABILITY_ISSUE_BODY = clean(
    """
    ## Objective

    Establish a repeatable, state-aware process for delivering every
    repository capability.

    ## Scope

    - Baseline verification
    - Existing-branch detection
    - Bootstrap preview
    - Safe apply
    - Partial-apply recovery
    - Local validation
    - GitHub synchronization
    - Staging review
    - Commit
    - Push
    - Pull-request discovery and creation
    - CI gating
    - Merge
    - Branch deletion
    - Return to clean develop
    - Capability closure

    ## Deliverables

    - Capability Delivery Workflow
    - State-aware helper
    - Automated tests
    - ADR-008
    - Architecture Baseline 2026.08.01v04
    - Capability demo
    - Complementary documentation updates

    ## Acceptance criteria

    - Exact paste-ready commands are generated
    - Existing branches are resumed safely
    - Partial applies are recoverable
    - Existing pull requests are reused
    - CI failures block merge
    - Resolved PR numbers are used
    - Merge command deletes the branch
    - Capability completion requires clean develop
    - Repository validation passes
    """
)


def project_payload(root: Path) -> dict[str, Any]:
    """Return GitHub Project metadata."""
    payload = json_output(
        [
            "gh",
            "project",
            "view",
            str(PROJECT_NUMBER),
            "--owner",
            OWNER,
            "--format",
            "json",
        ],
        cwd=root,
    )

    if not isinstance(payload, dict):
        return {}

    return payload


def validate_project(root: Path) -> None:
    """Confirm expected Project identity."""
    project = project_payload(root)

    if project.get("id") != PROJECT_ID:
        raise CapabilityError(
            "GitHub Project #1 does not match the expected project ID."
        )


def issue_list(root: Path) -> list[dict[str, Any]]:
    """Return repository issues."""
    payload = json_output(
        [
            "gh",
            "issue",
            "list",
            "--repo",
            REPOSITORY,
            "--state",
            "all",
            "--limit",
            "300",
            "--json",
            "number,title,url,state",
        ],
        cwd=root,
    )

    if not isinstance(payload, list):
        return []

    return payload


def find_issue(
    root: Path,
    title: str,
) -> dict[str, Any] | None:
    """Find an issue by exact title."""
    for issue in issue_list(root):
        if issue.get("title") == title:
            return issue

    return None


def ensure_issue(
    root: Path,
    title: str,
    body: str,
) -> dict[str, Any]:
    """Return an existing issue or create it."""
    existing = find_issue(root, title)

    if existing is not None:
        print(
            f"Issue already exists: "
            f"#{existing['number']} - {title}"
        )
        return existing

    run(
        [
            "gh",
            "issue",
            "create",
            "--repo",
            REPOSITORY,
            "--title",
            title,
            "--body",
            body,
        ],
        cwd=root,
    )

    for attempt in range(1, 6):
        created = find_issue(root, title)

        if created is not None:
            print(
                f"Created issue "
                f"#{created['number']} - {title}"
            )
            return created

        print(
            f"Issue is not visible yet "
            f"(attempt {attempt}/5); waiting..."
        )
        time.sleep(2)

    raise CapabilityError(
        f"Could not resolve issue after creation: {title}"
    )


def project_items(root: Path) -> list[dict[str, Any]]:
    """Return GitHub Project items."""
    payload = json_output(
        [
            "gh",
            "project",
            "item-list",
            str(PROJECT_NUMBER),
            "--owner",
            OWNER,
            "--limit",
            "300",
            "--format",
            "json",
        ],
        cwd=root,
    )

    if not isinstance(payload, dict):
        return []

    items = payload.get("items", [])

    if not isinstance(items, list):
        return []

    return items


def project_item_for_url(
    root: Path,
    url: str,
) -> dict[str, Any] | None:
    """Find a Project item for a GitHub URL."""
    for item in project_items(root):
        content = item.get("content") or {}

        if content.get("url") == url:
            return item

    return None


def ensure_project_item(
    root: Path,
    url: str,
) -> dict[str, Any]:
    """Add an issue to the Project with bounded retries."""
    existing = project_item_for_url(root, url)

    if existing is not None:
        return existing

    run(
        [
            "gh",
            "project",
            "item-add",
            str(PROJECT_NUMBER),
            "--owner",
            OWNER,
            "--url",
            url,
        ],
        cwd=root,
    )

    for attempt in range(1, 11):
        created = project_item_for_url(root, url)

        if created is not None:
            if attempt > 1:
                print(
                    "Resolved Project item after "
                    f"{attempt} lookup attempts."
                )

            return created

        print(
            f"Project item is not visible yet "
            f"(attempt {attempt}/10); waiting..."
        )
        time.sleep(2)

    raise CapabilityError(
        "GitHub accepted the Project item but it did not become "
        f"visible within the retry window: {url}"
    )


def set_status(
    root: Path,
    item_id: str,
    status: str,
) -> None:
    """Set Project item status."""
    run(
        [
            "gh",
            "project",
            "item-edit",
            "--id",
            item_id,
            "--project-id",
            PROJECT_ID,
            "--field-id",
            STATUS_FIELD_ID,
            "--single-select-option-id",
            STATUS_OPTIONS[status],
        ],
        cwd=root,
    )


def update_issue_status(
    root: Path,
    title: str,
    status: str,
) -> None:
    """Update one existing issue when present."""
    issue = find_issue(root, title)

    if issue is None:
        print(
            f"Issue not found, skipping status update: {title}"
        )
        return

    item = ensure_project_item(
        root,
        issue["url"],
    )

    set_status(
        root,
        item["id"],
        status,
    )

    print(
        f"Marked issue #{issue['number']} {status}."
    )


def sync_project(root: Path) -> None:
    """Synchronize GitHub planning."""
    validate_required_files(root)
    validate_product_language(root)
    run_repository_validation(root)

    run(
        ["gh", "auth", "status"],
        cwd=root,
    )

    validate_project(root)

    update_issue_status(
        root,
        PREVIOUS_CAPABILITY_ISSUE_TITLE,
        "Done",
    )

    capability_issue = ensure_issue(
        root,
        CAPABILITY_ISSUE_TITLE,
        CAPABILITY_ISSUE_BODY,
    )

    capability_item = ensure_project_item(
        root,
        capability_issue["url"],
    )

    set_status(
        root,
        capability_item["id"],
        "In Progress",
    )

    print(
        "Capability Delivery Workflow marked In Progress."
    )

    run(
        [
            "gh",
            "project",
            "edit",
            str(PROJECT_NUMBER),
            "--owner",
            OWNER,
            "--description",
            PROJECT_DESCRIPTION,
            "--readme",
            PROJECT_README,
        ],
        cwd=root,
    )

    print()
    print(
        "GitHub Project synchronized for the "
        "Capability Delivery Workflow."
    )


# ---------------------------------------------------------------------
# Arguments and main
# ---------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Establish the repeatable Capability Delivery Workflow."
        )
    )

    mode = parser.add_mutually_exclusive_group()

    mode.add_argument(
        "--apply",
        action="store_true",
        help=(
            "Write and validate local workflow files."
        ),
    )

    mode.add_argument(
        "--sync-project",
        action="store_true",
        help=(
            "Synchronize GitHub Project planning."
        ),
    )

    return parser.parse_args()


def main() -> int:
    """Preview, apply, or synchronize the workflow capability."""
    args = parse_args()

    try:
        root = repository_root()

        print(f"Repository: {root}")

        verify_script_integrity()
        verify_branch(root)

        if args.sync_project:
            sync_project(root)

        elif args.apply:
            verify_expected_working_tree(root)
            apply_local_changes(root)
            validate_required_files(root)
            validate_product_language(root)
            run_repository_validation(root)
            show_status(root)

            print()
            print(
                "Capability Delivery Workflow has been "
                "applied and validated."
            )
            print(
                "Nothing has been committed, pushed, "
                "or changed on GitHub."
            )

        else:
            verify_expected_working_tree(root)
            preview()

        return 0

    except CapabilityError as exc:
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

    except json.JSONDecodeError as exc:
        print(
            f"\nERROR: Could not parse GitHub CLI JSON: {exc}",
            file=sys.stderr,
        )
        return 1

    except Exception as exc:
        print(
            f"\nUNEXPECTED ERROR: {exc}",
            file=sys.stderr,
        )
        return 1


# CAPABILITY_DELIVERY_WORKFLOW_BOOTSTRAP_COMPLETE
# END OF SCRIPT - CAPABILITY DELIVERY WORKFLOW


if __name__ == "__main__":
    raise SystemExit(main())
