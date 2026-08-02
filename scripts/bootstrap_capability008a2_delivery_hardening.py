#!/usr/bin/env python3
"""Bootstrap Capability 008A.2 - Delivery Hardening.

Preview changes nothing. ``--apply`` deterministically writes the bounded
repository increment and runs the complete validation suite.
``--sync-project`` reuses the approved GitHub planning artifacts and leaves
Capability 008A.3 and Capability 009 Todo.
"""

from __future__ import annotations

import argparse
import base64
import gzip
import importlib.util
import json
import re
import subprocess
import sys
import textwrap
import time
from pathlib import Path
from typing import Any


EXPECTED_REPOSITORY = "Ramrattan-AI-Editorial-Studio"
EXPECTED_REMOTE = "RamrattanN/Ramrattan-AI-Editorial-Studio"
EXPECTED_BRANCH = "feature/capability-008a2-delivery-hardening"
REPOSITORY = "RamrattanN/Ramrattan-AI-Editorial-Studio"
OWNER = "RamrattanN"
PROJECT_NUMBER = 1
PROJECT_ID = "PVT_kwHOAuXHyM4BfHW9"
STATUS_FIELD_ID = "PVTSSF_lAHOAuXHyM4BfHW9zhZclQY"
IN_PROGRESS_OPTION_ID = "47fc9ee4"
ISSUE_TITLE = "Capability 008A.2 - Delivery Hardening"
SCRIPT_PATH = "scripts/bootstrap_capability008a2_delivery_hardening.py"
SENTINEL = "CAPABILITY_008A2_DELIVERY_HARDENING_COMPLETE"


def clean(value: str) -> str:
    """Dedent text and preserve one trailing newline."""
    return textwrap.dedent(value).strip() + "\n"


def decode(value: str) -> str:
    """Decode one deterministic gzip/base64 UTF-8 payload."""
    return gzip.decompress(base64.b64decode(value)).decode("utf-8")


CAPABILITY_DELIVERY_HELPER = decode(
    "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"
).replace(
    '            "--state",\n            "all",\n            "--json",',
    '            "--state",\n            "all",\n            "--limit",\n'
    '            "100",\n            "--json",',
)

WORKFLOW_TESTS = decode(
    "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"
    .replace("zJrdojoU", "zJrPojoU")
)

CAPABILITY_DELIVERY_WORKFLOW = decode(
    "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"
)

from bootstrap_workflow_governance_refinement import (
    refine_helper,
    refine_tests,
    refine_workflow,
)

CAPABILITY_DELIVERY_HELPER = refine_helper(CAPABILITY_DELIVERY_HELPER)
WORKFLOW_TESTS = refine_tests(WORKFLOW_TESTS)
CAPABILITY_DELIVERY_WORKFLOW = refine_workflow(CAPABILITY_DELIVERY_WORKFLOW)


CI_WORKFLOW = clean(
    """
    name: Validate repository

    on:
      push:
        branches:
          - main
          - develop
      pull_request:

    permissions:
      contents: read

    jobs:
      validate:
        runs-on: ubuntu-latest

        steps:
          - name: Check out repository
            uses: actions/checkout@v4

          - name: Set up Python
            uses: actions/setup-python@v5
            with:
              python-version: "3.12"

          - name: Compile Python sources
            run: python3 -m compileall -q studio scripts tests

          - name: Run complete unit-test suite
            run: python3 -m unittest discover -s tests -v

          - name: Validate repository
            run: python3 studio.py validate
    """
)


ADR_012 = clean(
    """
    # ADR-012 - Delivery Hardening

    ## Status

    Accepted

    ## Date

    2026-08-02

    ## Decision Level

    D4 - Architecture

    ## Context

    The original Capability Delivery helper could turn failed GitHub discovery
    into apparent absence, treat an empty check rollup as success, ignore draft
    state, select the first of multiple pull requests, and recommend merge without
    complete review or mergeability evidence.

    PRs #30, #31, and #33 confirmed the draft-state defect: the helper reported
    `ready_to_merge` while GitHub still reported each pull request as a draft.
    Remote freshness and incomplete post-merge cleanup were also not represented
    as first-class evidence.

    These are trust failures. A delivery recommendation must not be more certain
    than the evidence used to produce it.

    ## Decision

    Adopt a fail-closed delivery observation model.

    ### Discovery Results

    External discovery returns one of:

    - `FOUND` - exactly one complete matching artifact was verified;
    - `NOT_FOUND` - a successful query confirmed zero matches;
    - `UNAVAILABLE` - authentication, network, API, parsing, or required evidence
      failed; or
    - `AMBIGUOUS` - more than one matching artifact was verified.

    `UNAVAILABLE` and `AMBIGUOUS` block advancement. Failure is never interpreted
    as absence.

    ### Remote Freshness

    Remote-dependent recommendations require direct observation of
    `origin/develop` and the feature branch. Cached remote-tracking references are
    insufficient freshness evidence.

    A command failure, malformed reference response, or missing remote base branch
    blocks the workflow.

    ### Pull-Request Evidence

    The helper models:

    - zero, one, or multiple branch-matching pull requests;
    - open, closed, and merged state;
    - draft and ready-for-review state;
    - review required, changes requested, and approved state;
    - clean, conflicting, blocked, unknown, and unavailable mergeability;
    - pull-request head identity; and
    - check availability and outcomes.

    A draft pull request is never ready to merge. The remote feature head must
    match the pull-request head before PR recommendations advance.

    ### CI Evidence

    An empty or missing check rollup is unavailable unless repository policy
    independently proves no checks are required. This repository requires CI, so
    zero checks block merge.

    Check outcomes are normalized as unavailable, pending, failed, cancelled,
    timed out, action required, or successful. Only successful checks can satisfy
    the CI gate.

    ### Recovery

    Merged state is observed independently from branch cleanup. The helper
    recommends one recovery step at a time when checkout, local branch deletion,
    remote branch deletion, baseline synchronization, or merge ancestry remains
    incomplete. The helper never repeats a confirmed merge.

    ### Approval Boundaries

    Read-only observation, validation, and CI monitoring may continue
    automatically inside an authorized phase. Protected mutations retain explicit
    role-based approval boundaries. The helper may recommend them but does not
    execute them.

    ## CI Contract

    ```bash
    python3 -m compileall -q studio scripts tests
    python3 -m unittest discover -s tests -v
    python3 studio.py validate
    ```

    ## Alternatives Considered

    Optimistic defaults, open-only discovery, zero-check success, and automatic
    protected mutations were rejected because each weakens verified evidence or
    explicit approval.

    ## Consequences

    Delivery recommendations cannot silently overstate external evidence, and
    partial cleanup is resumable. Delivery may pause more often when evidence is
    incomplete, and GitHub response-shape changes require parser maintenance.

    ## Architecture Baseline

    Recorded by Architecture Baseline `2026.08.01v07`.
    """
)


BASELINE_V07 = clean(
    """
    # Architecture Baseline - 2026.08.01v07

    ## Status

    Current engineering delivery baseline.

    ## Baseline ID

    `2026.08.01v07`

    ## Supersedes

    `2026.08.01v06`

    ## Reason for Revision

    Implement Capability 008A.2 - Delivery Hardening under ADR-012.

    ## Architecture

    The Capability Delivery helper is a fail-closed observer and recommender.
    Its evidence model contains direct remote freshness; explicit `FOUND`,
    `NOT_FOUND`, `UNAVAILABLE`, and `AMBIGUOUS` discovery; normalized draft,
    review, mergeability, and check state; verified PR/head agreement;
    deterministic post-merge recovery; and explicit approval boundaries.

    Remote, GitHub, parsing, or required-field failure blocks advancement.
    Missing or empty checks do not count as successful CI.

    ## CI Contract

    ```bash
    python3 -m compileall -q studio scripts tests
    python3 -m unittest discover -s tests -v
    python3 studio.py validate
    ```

    ## Generated Ownership

    `scripts/bootstrap_capability008a2_delivery_hardening.py` owns the hardened
    delivery artifacts. The original Capability Delivery bootstrap delegates its
    helper, workflow, and test templates to the 008A.2 canonical templates.

    ## Constitutional Impact

    No frozen constitutional rule changes. This baseline strengthens Engineering
    Stewardship and trust before convenience by refusing to convert unavailable
    evidence into a safe transition.

    ## Product Runtime Impact

    None. Evidence Validation, StageState, editorial runtime, Article Engine,
    Publication Package, Hero Visual, and Portable Project behavior are unchanged.
    """
)


ROADMAP_BLOCK = clean(
    """
    ## Capability 008A.2 - Delivery Hardening

    Status: **In Progress**

    Current authoritative sequence:

    - Capability 008 - Complete
    - Capability 008A.1 - Governance Consolidation - Complete
    - Capability 008A.2 - Delivery Hardening - In Progress
    - Capability 008A.3 - Editorial Integrity Hardening - Todo
    - Capability 009 - Todo

    Capability 008A.2 makes delivery observation fail closed, distinguishes
    unavailable state from confirmed absence, hardens PR and CI gates, and adds
    deterministic post-merge recovery. Product runtime does not change.

    ADR-012 records Delivery Hardening. Architecture Baseline `2026.08.01v07`
    records the resulting engineering architecture. Earlier status sections are
    historical delivery records; this section owns the active increment.
    """
)


FOCUS_BLOCK = clean(
    """
    ## Current Implementation Status - Capability 008A.2

    - Capability 008 - Complete
    - Capability 008A.1 - Governance Consolidation - Complete
    - Capability 008A.2 - Delivery Hardening - In Progress
    - Capability 008A.3 - Editorial Integrity Hardening - Todo
    - Capability 009 - Todo

    The active engineering focus is fail-closed capability delivery under
    ADR-012. Product runtime remains at Capability 008. Evidence Validation,
    StageState, and publication behavior do not change in this increment.

    Architecture Baseline `2026.08.01v07` records the hardened delivery
    architecture. Earlier focus sections remain delivery history.
    """
)


SCORECARD_BLOCK = clean(
    """
    ## Capability 008A Delivery Hardening Status

    - Capability 008A.1 - Complete
    - Capability 008A.2 - In Progress
    - Capability 008A.3 - Todo
    - Capability 009 - Todo

    | Delivery area | Status | Evidence |
    |---|---|---|
    | Fail-closed discovery | Complete | Helper and high-risk workflow tests |
    | Remote freshness | Complete | Direct remote observation tests |
    | Draft and review readiness | Complete | PR #30, #31, and #33 regressions |
    | Mergeability gating | Complete | Conflict, blocked, and unknown tests |
    | CI outcome gating | Complete | All check-state tests and CI workflow |
    | Post-merge recovery | Complete | Cleanup state tests |
    | Delivery architecture | Complete | ADR-012 and baseline v07 |

    Capability 008A.2 changes engineering delivery safety only. Version 1.0
    product-runtime readiness remains unchanged.
    """
)


DECISION_BLOCK = clean(
    """
    ## Capability 008A.2 Delivery Hardening Decisions

    | Date | Level | Decision | Rationale |
    |---|---:|---|---|
    | 2026-08-02 | D4 | Fail closed on unavailable or ambiguous delivery evidence | Missing evidence cannot justify a protected transition. |
    | 2026-08-02 | D4 | Observe remote heads directly | Cached remote-tracking references do not prove freshness. |
    | 2026-08-02 | D4 | Model draft, review, mergeability, and checks independently | PRs #30, #31, and #33 exposed optimistic state collapse. |
    | 2026-08-02 | D4 | Treat zero checks as unavailable | Repository policy requires canonical CI validation. |
    | 2026-08-02 | D4 | Recover post-merge cleanup one step at a time | Merge success does not prove cleanup completed. |
    | 2026-08-02 | D4 | Create Architecture Baseline 2026.08.01v07 | Delivery observation and recovery are durable engineering architecture. |
    """
)


ISSUE_BODY = clean(
    """
    ## Objective

    Make Capability Delivery fail closed, distinguish unavailable state from
    confirmed absence, and base recommendations on complete local and GitHub
    evidence.

    ## Architecture

    - ADR-012
    - Architecture Baseline 2026.08.01v07

    ## Acceptance Criteria

    - Unknown, unavailable, incomplete, or ambiguous external state fails closed
    - Draft, review, mergeability, and CI states are explicit
    - Partial merge and cleanup states recover deterministically
    - CI runs the canonical complete validation suite
    - Protected mutations retain explicit approval boundaries
    """
)


PROJECT_README = """# Ramrattan AI Editorial Studio

## Governing principle

Trust is our most valuable feature.

## Current implementation

- Capabilities 001-008 - complete
- Capability 008A.1 - Governance Consolidation - Complete
- Capability 008A.2 - Delivery Hardening - In Progress
- Capability 008A.3 - Editorial Integrity Hardening - Todo
- Capability 009 - Article Engine and Publication Package - Todo

## Active engineering hardening increment

Capability 008A.2 hardens delivery-state discovery, remote freshness,
pull-request readiness, review and mergeability evidence, CI checks, and
post-merge recovery under ADR-012.

Capability 008A.3 and Capability 009 remain Todo and have not started.

The current architecture baseline remains 2026.08.01v06 while Capability
008A.2 is in progress. Architecture Baseline 2026.08.01v07 becomes current
only when Delivery Hardening is delivered.

## Program sequence

Capability 008A.1 is complete.
Capability 008A.2 must complete before Capability 008A.3 begins.
Capability 009 begins only after the complete Capability 008A program.
"""


OLD_BOOTSTRAP_OVERRIDE = clean(
    """
    # CAPABILITY_008A2_DELIVERY_HARDENING_OVERRIDE_START
    from bootstrap_capability008a2_delivery_hardening import (
        CAPABILITY_DELIVERY_HELPER as CAPABILITY_DELIVERY_HELPER_008A2,
        CAPABILITY_DELIVERY_WORKFLOW as CAPABILITY_DELIVERY_WORKFLOW_008A2,
        WORKFLOW_TESTS as WORKFLOW_TESTS_008A2,
    )

    CAPABILITY_DELIVERY_HELPER = CAPABILITY_DELIVERY_HELPER_008A2
    CAPABILITY_DELIVERY_WORKFLOW = CAPABILITY_DELIVERY_WORKFLOW_008A2
    WORKFLOW_TESTS = WORKFLOW_TESTS_008A2
    # CAPABILITY_008A2_DELIVERY_HARDENING_OVERRIDE_END
    """
)


FULL_FILES = {
    "scripts/capability_delivery.py": CAPABILITY_DELIVERY_HELPER,
    "tests/test_capability_delivery_workflow.py": WORKFLOW_TESTS,
    "docs/engineering/Capability_Delivery_Workflow.md": CAPABILITY_DELIVERY_WORKFLOW,
    ".github/workflows/validate.yml": CI_WORKFLOW,
    "docs/architecture/adr/ADR-012-delivery-hardening.md": ADR_012,
    "docs/architecture/baselines/Architecture_Baseline_2026.08.01v07.md": BASELINE_V07,
}

MARKER_BLOCKS = {
    "ROADMAP.md": ("CAPABILITY_008A2_ROADMAP", ROADMAP_BLOCK),
    "docs/product/Current_Product_Focus.md": (
        "CAPABILITY_008A2_CURRENT_FOCUS",
        FOCUS_BLOCK,
    ),
    "docs/VERSION_ONE_SCORECARD.md": (
        "CAPABILITY_008A2_SCORECARD",
        SCORECARD_BLOCK,
    ),
    "docs/product/Decision_Log.md": (
        "CAPABILITY_008A2_DECISION_LOG",
        DECISION_BLOCK,
    ),
}

OLD_BOOTSTRAP = "scripts/bootstrap_capability_delivery_workflow.py"
ADR_INDEX = "docs/architecture/adr/README.md"
ADR_INDEX_LINE = "- [ADR-012 - Delivery Hardening](ADR-012-delivery-hardening.md)"
A1_BOOTSTRAP = "scripts/bootstrap_capability008a1_governance_consolidation.py"
A1_TEST = "tests/test_capability008a1_governance.py"
A1_OLD_METHOD = "test_adr_011_is_narrow_and_no_new_baseline_exists"
A1_NEW_METHOD = "test_adr_011_is_narrow_and_claims_no_governance_baseline"
A1_NEW_ASSERTION = 'self.assertNotIn("2026.08.01v07", adr)'


class CapabilityError(RuntimeError):
    """Raised when the bootstrap cannot proceed safely."""


def run(
    command: list[str],
    *,
    cwd: Path,
    capture: bool = False,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    """Run a visible command."""
    print("$", " ".join(command))
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=capture,
        check=check,
    )


def output(command: list[str], *, cwd: Path) -> str:
    return run(command, cwd=cwd, capture=True).stdout.strip()


def json_output(command: list[str], *, cwd: Path) -> Any:
    raw = output(command, cwd=cwd)
    if not raw:
        raise CapabilityError("Required JSON response was empty.")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise CapabilityError(f"Malformed JSON response: {exc}") from exc


def repository_root() -> Path:
    root = Path(output(["git", "rev-parse", "--show-toplevel"], cwd=Path.cwd())).resolve()
    if root.name != EXPECTED_REPOSITORY:
        raise CapabilityError(f"Expected {EXPECTED_REPOSITORY}, found {root.name}.")
    remote = output(["git", "remote", "get-url", "origin"], cwd=root)
    if EXPECTED_REMOTE not in remote:
        raise CapabilityError("Origin does not match the expected repository.")
    return root


def verify_integrity() -> None:
    content = Path(__file__).read_text(encoding="utf-8")
    if SENTINEL not in content:
        raise CapabilityError("Bootstrap integrity sentinel is missing.")
    compile(content, str(Path(__file__)), "exec")


def verify_branch(root: Path) -> None:
    branch = output(["git", "branch", "--show-current"], cwd=root)
    print(f"Branch: {branch}")
    if branch != EXPECTED_BRANCH:
        raise CapabilityError(f"Expected branch {EXPECTED_BRANCH}, found {branch}.")


def expected_paths() -> set[str]:
    return set(FULL_FILES) | set(MARKER_BLOCKS) | {
        SCRIPT_PATH,
        OLD_BOOTSTRAP,
        ADR_INDEX,
        A1_BOOTSTRAP,
        A1_TEST,
    }


def verify_working_tree(root: Path) -> None:
    result = run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=root,
        capture=True,
    )
    raw = result.stdout
    unexpected: list[str] = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        relative = line[3:].strip()
        if " -> " in relative:
            relative = relative.split(" -> ", 1)[1].strip()
        if relative not in expected_paths():
            unexpected.append(line)
    if unexpected:
        raise CapabilityError(
            "Unexpected working-tree changes:\n" + "\n".join(unexpected)
        )
    print("Working tree contains only expected Capability 008A.2 paths.")


def managed_block(marker: str, content: str) -> str:
    return f"<!-- {marker}_START -->\n\n{content.rstrip()}\n\n<!-- {marker}_END -->"


def upsert_markdown(path: Path, marker: str, content: str) -> None:
    original = path.read_text(encoding="utf-8")
    start = f"<!-- {marker}_START -->"
    end = f"<!-- {marker}_END -->"
    if (start in original) != (end in original):
        raise CapabilityError(f"Incomplete marker pair in {path}.")
    block = managed_block(marker, content)
    if start in original:
        before = original.split(start, 1)[0].rstrip()
        after = original.split(end, 1)[1].lstrip()
        updated = before + "\n\n" + block
        if after:
            updated += "\n\n" + after
    else:
        updated = original.rstrip() + "\n\n" + block
    path.write_text(updated.rstrip() + "\n", encoding="utf-8")


def upsert_python_override(path: Path) -> None:
    original = path.read_text(encoding="utf-8")
    start = "# CAPABILITY_008A2_DELIVERY_HARDENING_OVERRIDE_START"
    end = "# CAPABILITY_008A2_DELIVERY_HARDENING_OVERRIDE_END"
    anchor = "NEW_FILES = {"
    if anchor not in original:
        raise CapabilityError("Original delivery bootstrap anchor is missing.")
    if (start in original) != (end in original):
        raise CapabilityError("Incomplete delivery-bootstrap override marker pair.")
    if start in original:
        before = original.split(start, 1)[0].rstrip()
        after = original.split(end, 1)[1].lstrip()
        updated = before + "\n\n" + OLD_BOOTSTRAP_OVERRIDE.rstrip() + "\n\n" + after
    else:
        updated = original.replace(
            anchor,
            OLD_BOOTSTRAP_OVERRIDE.rstrip() + "\n\n" + anchor,
            1,
        )
    path.write_text(updated.rstrip() + "\n", encoding="utf-8")


def ensure_adr_index(path: Path) -> None:
    content = path.read_text(encoding="utf-8")
    if ADR_INDEX_LINE not in content:
        prior = "- [ADR-011 - Governance Authority](ADR-011-governance-authority.md)"
        if prior not in content:
            raise CapabilityError("ADR-011 index anchor is missing.")
        content = content.replace(prior, prior + "\n" + ADR_INDEX_LINE, 1)
        path.write_text(content, encoding="utf-8")


def repair_a1_baseline_contract(path: Path) -> None:
    """Keep the historical 008A.1 test valid after approved baseline v07."""
    content = path.read_text(encoding="utf-8")
    content = content.replace(A1_OLD_METHOD, A1_NEW_METHOD)
    pattern = re.compile(
        r'(?m)^(?P<indent>[ \t]*)self\.assertFalse\(\n'
        r'(?P=indent)    any\(\n'
        r'(?P=indent)        path\.name\.endswith\("v07\.md"\)\n'
        r'(?P=indent)        for path in '
        r'\(ROOT / "docs/architecture/baselines"\)\.iterdir\(\)\n'
        r'(?P=indent)    \)\n'
        r'(?P=indent)\)'
    )
    content = pattern.sub(
        lambda match: match.group("indent") + A1_NEW_ASSERTION,
        content,
    )
    if A1_NEW_METHOD not in content or A1_NEW_ASSERTION not in content:
        raise CapabilityError(f"Could not synchronize the 008A.1 baseline contract in {path}.")
    path.write_text(content, encoding="utf-8")


def apply_files(root: Path) -> None:
    for relative, content in FULL_FILES.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"Wrote {relative}")
    for relative, (marker, content) in MARKER_BLOCKS.items():
        upsert_markdown(root / relative, marker, content)
        print(f"Updated {relative}")
    upsert_python_override(root / OLD_BOOTSTRAP)
    ensure_adr_index(root / ADR_INDEX)
    repair_a1_baseline_contract(root / A1_BOOTSTRAP)
    repair_a1_baseline_contract(root / A1_TEST)


def validate_generated_files(root: Path) -> None:
    for relative, expected in FULL_FILES.items():
        actual = (root / relative).read_text(encoding="utf-8")
        if actual != expected:
            raise CapabilityError(f"Generated artifact differs from bootstrap: {relative}")
    phrases = {
        "scripts/capability_delivery.py": (
            "class ObservationState",
            "class ApprovalProfile",
            "Next profile boundary",
            "REMOTE_VERIFICATION_FAILED",
            "PR_DRAFT",
            "PR_CHECKS_UNAVAILABLE",
            "POST_MERGE_CLEANUP",
        ),
        "docs/engineering/Capability_Delivery_Workflow.md": (
            "Fail Closed on Incomplete Evidence",
            "Delegated Approval Profiles",
            "Change Consolidation",
            "gh pr checks 24 --watch",
            "Zero reported checks are unavailable",
        ),
        "docs/architecture/adr/ADR-012-delivery-hardening.md": (
            "ADR-012 - Delivery Hardening",
            "PRs #30, #31, and #33",
        ),
        "docs/architecture/baselines/Architecture_Baseline_2026.08.01v07.md": (
            "2026.08.01v07",
            "fail-closed observer and recommender",
        ),
    }
    for relative, required in phrases.items():
        content = (root / relative).read_text(encoding="utf-8")
        for phrase in required:
            if phrase not in content:
                raise CapabilityError(f"Missing {phrase!r} in {relative}.")
    old_bootstrap = (root / OLD_BOOTSTRAP).read_text(encoding="utf-8")
    if OLD_BOOTSTRAP_OVERRIDE.strip() not in old_bootstrap:
        raise CapabilityError("Original delivery bootstrap is not delegated to 008A.2.")
    scripts_path = str(root / "scripts")
    if scripts_path not in sys.path:
        sys.path.insert(0, scripts_path)
    spec = importlib.util.spec_from_file_location(
        "capability_delivery_workflow_generator",
        root / OLD_BOOTSTRAP,
    )
    if spec is None or spec.loader is None:
        raise CapabilityError("Original delivery bootstrap cannot be loaded.")
    generator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(generator)
    delegated = {
        "scripts/capability_delivery.py": CAPABILITY_DELIVERY_HELPER,
        "tests/test_capability_delivery_workflow.py": WORKFLOW_TESTS,
        "docs/engineering/Capability_Delivery_Workflow.md": CAPABILITY_DELIVERY_WORKFLOW,
    }
    for relative, expected in delegated.items():
        if generator.NEW_FILES.get(relative) != expected:
            raise CapabilityError(f"Original delivery bootstrap is stale for {relative}.")
    if ADR_INDEX_LINE not in (root / ADR_INDEX).read_text(encoding="utf-8"):
        raise CapabilityError("ADR-012 is absent from the ADR index.")
    for relative in (A1_BOOTSTRAP, A1_TEST):
        content = (root / relative).read_text(encoding="utf-8")
        if A1_NEW_METHOD not in content or A1_NEW_ASSERTION not in content:
            raise CapabilityError(f"008A.1 baseline contract is stale in {relative}.")
    print("Generated artifacts and both delivery bootstraps are synchronized.")


def run_validation(root: Path) -> None:
    run([sys.executable, "-m", "compileall", "-q", "studio", "scripts", "tests"], cwd=root)
    run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=root,
    )
    run([sys.executable, "studio.py", "validate"], cwd=root)
    print("Capability 008A.2 repository validation passed.")


def preview() -> None:
    print("\nCapability 008A.2 preview:\n")
    print("Generated files:")
    for relative in FULL_FILES:
        print(f"  - {relative}")
    print("\nManaged updates:")
    for relative in (*MARKER_BLOCKS, OLD_BOOTSTRAP, ADR_INDEX, A1_BOOTSTRAP, A1_TEST):
        print(f"  - {relative}")
    print("\nDecisions:")
    for decision in (
        "Fail closed on unavailable or ambiguous evidence",
        "Verify remote freshness directly",
        "Model zero, one, and multiple pull requests",
        "Model draft, review, mergeability, and all CI outcomes",
        "Monitor pending CI automatically with a read-only command",
        "Recover incomplete post-merge cleanup one step at a time",
        "Preserve every protected approval boundary",
        "Create ADR-012 and Architecture Baseline 2026.08.01v07",
    ):
        print(f"  - {decision}")
    print("\nPreview mode changes nothing.")


def issue_list(root: Path) -> list[dict[str, Any]]:
    payload = json_output(
        [
            "gh", "issue", "list", "--repo", REPOSITORY, "--state", "all",
            "--limit", "300", "--json", "number,title,url,state",
        ],
        cwd=root,
    )
    if not isinstance(payload, list):
        raise CapabilityError("Issue response is not a list.")
    return payload


def ensure_issue(root: Path) -> dict[str, Any]:
    matches = [item for item in issue_list(root) if item.get("title") == ISSUE_TITLE]
    if len(matches) > 1:
        raise CapabilityError("Multiple Capability 008A.2 issues exist.")
    if matches:
        if matches[0].get("state") != "OPEN":
            raise CapabilityError("Capability 008A.2 issue exists but is not open.")
        return matches[0]
    run(
        ["gh", "issue", "create", "--repo", REPOSITORY, "--title", ISSUE_TITLE, "--body", ISSUE_BODY],
        cwd=root,
    )
    for _ in range(5):
        matches = [item for item in issue_list(root) if item.get("title") == ISSUE_TITLE]
        if len(matches) == 1:
            return matches[0]
        time.sleep(2)
    raise CapabilityError("Created issue could not be resolved.")


def project_items(root: Path) -> list[dict[str, Any]]:
    payload = json_output(
        [
            "gh", "project", "item-list", str(PROJECT_NUMBER), "--owner", OWNER,
            "--limit", "300", "--format", "json",
        ],
        cwd=root,
    )
    if not isinstance(payload, dict) or not isinstance(payload.get("items"), list):
        raise CapabilityError("Project item response is malformed.")
    return payload["items"]


def ensure_project_item(root: Path, issue: dict[str, Any]) -> dict[str, Any]:
    def matches() -> list[dict[str, Any]]:
        return [
            item for item in project_items(root)
            if (item.get("content") or {}).get("url") == issue.get("url")
        ]

    found = matches()
    if len(found) > 1:
        raise CapabilityError("Multiple Project items reference Capability 008A.2.")
    if found:
        return found[0]
    run(
        [
            "gh", "project", "item-add", str(PROJECT_NUMBER), "--owner", OWNER,
            "--url", str(issue["url"]),
        ],
        cwd=root,
    )
    for _ in range(10):
        found = matches()
        if len(found) == 1:
            return found[0]
        time.sleep(2)
    raise CapabilityError("Project item did not become visible.")


def sync_project(root: Path) -> None:
    validate_generated_files(root)
    run_validation(root)
    run(["gh", "auth", "status"], cwd=root)
    project = json_output(
        ["gh", "project", "view", str(PROJECT_NUMBER), "--owner", OWNER, "--format", "json"],
        cwd=root,
    )
    if not isinstance(project, dict) or project.get("id") != PROJECT_ID:
        raise CapabilityError("GitHub Project identity is unavailable or unexpected.")
    issue = ensure_issue(root)
    item = ensure_project_item(root, issue)
    run(
        [
            "gh", "project", "item-edit", "--id", str(item["id"]),
            "--project-id", PROJECT_ID, "--field-id", STATUS_FIELD_ID,
            "--single-select-option-id", IN_PROGRESS_OPTION_ID,
        ],
        cwd=root,
    )
    items = project_items(root)
    capability_009 = [item for item in items if item.get("title", "").startswith("Capability 009")]
    if len(capability_009) != 1 or capability_009[0].get("status") != "Todo":
        raise CapabilityError("Capability 009 is not uniquely verified Todo.")
    capability_008a3 = [item for item in items if "Capability 008A.3" in item.get("title", "")]
    if capability_008a3 and any(item.get("status") != "Todo" for item in capability_008a3):
        raise CapabilityError("Capability 008A.3 is not Todo.")
    run(
        [
            "gh", "project", "edit", str(PROJECT_NUMBER), "--owner", OWNER,
            "--readme", PROJECT_README,
        ],
        cwd=root,
    )
    print(f"GitHub planning synchronized with issue #{issue['number']} In Progress.")


def show_status(root: Path) -> None:
    run(["git", "status", "--short"], cwd=root)
    run(["git", "diff", "--stat"], cwd=root)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bootstrap Capability 008A.2 Delivery Hardening.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--sync-project", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        root = repository_root()
        verify_integrity()
        verify_branch(root)
        verify_working_tree(root)
        if args.sync_project:
            sync_project(root)
        elif args.apply:
            apply_files(root)
            validate_generated_files(root)
            run_validation(root)
            show_status(root)
        else:
            preview()
        return 0
    except (CapabilityError, subprocess.CalledProcessError, UnicodeError, ValueError) as exc:
        print(f"\nERROR: {exc}", file=sys.stderr)
        return 1


# CAPABILITY_008A2_DELIVERY_HARDENING_COMPLETE


if __name__ == "__main__":
    raise SystemExit(main())
