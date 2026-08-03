#!/usr/bin/env python3
"""Bootstrap Capability 008A.1 - Governance Consolidation.

Preview by default:

    python3 scripts/bootstrap_capability008a1_governance_consolidation.py

Apply deterministic repository changes:

    python3 scripts/bootstrap_capability008a1_governance_consolidation.py --apply

Synchronize the authorized GitHub planning state:

    python3 scripts/bootstrap_capability008a1_governance_consolidation.py --sync-project
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import textwrap
import time
from pathlib import Path
from typing import Any


EXPECTED_REPOSITORY = "Ramrattan-AI-Editorial-Studio"
EXPECTED_REMOTE_FRAGMENT = "RamrattanN/Ramrattan-AI-Editorial-Studio"
EXPECTED_BRANCH = "feature/capability-008a1-governance-consolidation"
REPOSITORY = "RamrattanN/Ramrattan-AI-Editorial-Studio"
OWNER = "RamrattanN"
PROJECT_NUMBER = 1
PROJECT_ID = "PVT_kwHOAuXHyM4BfHW9"
STATUS_FIELD_ID = "PVTSSF_lAHOAuXHyM4BfHW9zhZclQY"
STATUS_OPTIONS = {
    "Todo": "f75ad846",
    "In Progress": "47fc9ee4",
    "Done": "98236657",
}
SCRIPT_PATH = "scripts/bootstrap_capability008a1_governance_consolidation.py"
SCRIPT_SENTINEL = "CAPABILITY_008A1_GOVERNANCE_BOOTSTRAP_COMPLETE"
ISSUE_TITLE = "Capability 008A.1 - Governance Consolidation"
CAPABILITY_009_TITLE = (
    "Capability 009 - Build the Article Engine and Publication Package"
)
CAPABILITY_008A2_TITLE = "Capability 008A.2 - Delivery Hardening"
CAPABILITY_008A3_TITLE = "Capability 008A.3 - Editorial Integrity Hardening"


def clean(value: str) -> str:
    return textwrap.dedent(value).strip() + "\n"


ADR_011 = clean(
    r"""
    # ADR-011 - Governance Authority

    ## Status

    Accepted

    ## Date

    2026-08-02

    ## Decision Level

    D4 - Architecture

    ## Context

    The repository contains constitutional, architectural, engineering,
    contributor, memory, planning, and release documents. Several documents
    repeated similar rules without defining which document owned each concept
    or how conflicts and status drift should be resolved.

    Capability 008A.1 must consolidate governance without changing product
    runtime behavior or inventing historical records.

    ## Decision

    Adopt an explicit governance authority model with one authoritative owner
    for every concept.

    The Repository Author's or an explicitly authorized Repository Maintainer's
    current request defines maximum task scope and authorization.
    Within that scope, repository authority is applied in this order:

    1. Verified repository and external-system state for factual questions
    2. Constitution
    3. Canonical Vocabulary
    4. Current architecture baseline and accepted ADRs
    5. Capability Delivery Workflow
    6. `AGENTS.md`
    7. `CONTRIBUTING.md`
    8. `AGENT_MEMORY.md`
    9. Conversation history

    More restrictive safety and approval requirements always apply.

    ## Authoritative Responsibilities

    | Artifact | Authoritative responsibility |
    |---|---|
    | Constitution | Enduring product principles and human responsibilities |
    | Canonical Vocabulary | Active product and editorial terminology |
    | Accepted ADRs | Durable architectural and governance decisions |
    | Current architecture baseline | Coherent implemented architecture at a point in time |
    | Capability Delivery Workflow | Canonical delivery lifecycle and recovery procedure |
    | `AGENTS.md` | Operational contract for repository agents |
    | `CONTRIBUTING.md` | Contributor-facing translation of repository governance |
    | `AGENT_MEMORY.md` | Advisory, chronological engineering experience |
    | `ROADMAP.md` | Current capability sequence and program status |
    | Version 1.0 Scorecard | Release-readiness evidence by required area |
    | Version 1.0 Release Definition | Product promise and release boundary |

    A document may summarize another authority but must link to it rather than
    create a competing rule.

    ## Lifecycle

    - The capability that changes a governed fact updates its authoritative
      artifact and affected summaries in the same increment.
    - Historical capability sections remain delivery records and must not be
      interpreted as current status when a later authoritative status section
      exists.
    - `AGENT_MEMORY.md` is append-oriented and advisory. Normative lessons must
      be promoted into the appropriate governing document before enforcement.
    - Changes to governance authority require an ADR, focused contract tests,
      generator synchronization, complete validation, and deliberate review.
    - Frozen constitutional or canonical vocabulary changes require explicit
      authorization beyond ordinary governance maintenance.

    ## Approval Boundaries

    Governance consolidation does not weaken approval boundaries. Staging,
    commit, push, pull-request mutations, merge, branch deletion, issue
    mutations, Project mutations, publication, and destructive operations
    remain protected unless the Repository Author or an explicitly authorized
    Repository Maintainer authorizes them in the current task or conversation.

    ## ADR-002 Reference Integrity

    Repository history contains no ADR-002 file or Git object. The surviving
    reference in Architecture Baseline v01 is therefore repaired to point to
    `docs/architecture/Editorial_Context_Model.md`, the historical architecture
    artifact that actually exists. ADR-002 is not recreated retroactively.

    ## Architecture Baseline

    No new architecture baseline is created for Capability 008A.1. This ADR
    clarifies governance authority without changing executable system
    architecture. Architecture Baseline `2026.08.01v06` remains current.

    ## Alternatives Considered

    ### Treat every governance document as equally authoritative

    Rejected because duplicated rules can conflict without a deterministic
    resolution path.

    ### Make `AGENT_MEMORY.md` normative

    Rejected because chronological experience should not silently change
    repository policy.

    ### Recreate ADR-002 from its broken reference

    Rejected because no historical ADR content exists and reconstruction would
    invent repository history.

    ### Create a new architecture baseline

    Rejected because governance clarification does not change runtime
    architecture.

    ## Consequences

    ### Positive

    - Conflicts resolve deterministically.
    - Every governance concept has one authoritative owner.
    - Advisory memory cannot silently become policy.
    - Current status is separated from historical delivery records.
    - Broken historical references are repaired honestly.

    ### Costs

    - Capabilities must update affected authorities and summaries together.
    - Governance contract tests add maintenance obligations.
    - Contributors must distinguish current status from historical records.
    """
)


GOVERNANCE_TESTS = clean(
    r'''
    """Governance contracts for Capability 008A.1."""

    import re
    import unittest
    from pathlib import Path


    ROOT = Path(__file__).resolve().parents[1]


    class Capability008A1GovernanceTests(unittest.TestCase):
        def content(self, relative: str) -> str:
            return (ROOT / relative).read_text(encoding="utf-8")

        def test_agents_structure_and_required_contracts(self) -> None:
            content = self.content("AGENTS.md")
            self.assertEqual(len(re.findall(r"^```", content, re.MULTILINE)) % 2, 0)
            for heading in (
                "## Instruction Authority",
                "## Dirty-Tree Protection",
                "## Autonomous Execution",
                "## Approval Boundaries",
                "## Validation",
                "## Generated Files",
                "## Stopping Conditions",
                "## Governance Document Responsibilities",
            ):
                self.assertIn(heading, content)
            for command in (
                "python3 -m compileall -q studio scripts tests",
                "python3 -m unittest discover -s tests -v",
                "python3 studio.py validate",
            ):
                self.assertIn(command, content)

        def test_memory_is_advisory_and_append_oriented(self) -> None:
            content = self.content("AGENT_MEMORY.md")
            self.assertIn("advisory", content)
            self.assertIn("must not define current repository status", content)
            self.assertIn("append dated lessons", content)
            self.assertNotIn("The Author strongly prefers", content)

        def test_contributing_defers_to_governing_authorities(self) -> None:
            content = self.content("CONTRIBUTING.md")
            self.assertIn("Repository Maintainer's", content)
            self.assertIn("current request defines the maximum scope", content)
            self.assertIn("staging changes with `git add`", content)
            self.assertIn("scripts/capability_delivery.py", content)
            self.assertIn("python3 -m compileall -q studio scripts tests", content)
            self.assertIn("Never repair only a generated artifact", content)

        def test_adr_011_is_narrow_and_claims_no_governance_baseline(self) -> None:
            adr = self.content(
                "docs/architecture/adr/ADR-011-governance-authority.md"
            )
            self.assertIn("# ADR-011 - Governance Authority", adr)
            self.assertIn("Accepted", adr)
            self.assertIn("No new architecture baseline", adr)
            self.assertIn("does not change runtime", adr)
            self.assertNotIn("2026.08.01v07", adr)

        def test_adr_index_and_adr_002_disposition_are_honest(self) -> None:
            index = self.content("docs/architecture/adr/README.md")
            self.assertIn("ADR-011 - Governance Authority", index)
            self.assertIn("ADR-002 was never committed", index)
            self.assertFalse(
                any(
                    path.name.startswith("ADR-002")
                    for path in (ROOT / "docs/architecture/adr").iterdir()
                )
            )
            baseline = self.content(
                "docs/architecture/baselines/Architecture_Baseline_2026.08.01v01.md"
            )
            self.assertNotIn("ADR-002", baseline)
            self.assertIn("docs/architecture/Editorial_Context_Model.md", baseline)

        def test_status_records_agree(self) -> None:
            records = (
                "ROADMAP.md",
                "docs/VERSION_ONE_SCORECARD.md",
                "docs/product/Current_Product_Focus.md",
                "docs/product/Release_v1.0.md",
            )
            for relative in records:
                content = self.content(relative)
                self.assertIn("Capability 008 - Complete", content)
                self.assertIn(
                    "Capability 008A.1 - Governance Consolidation - In Progress",
                    content,
                )
                self.assertIn(
                    "Capability 008A.2 - Delivery Hardening - Not started",
                    content,
                )
                self.assertIn(
                    "Capability 008A.3 - Editorial Integrity Hardening - Not started",
                    content,
                )
                self.assertIn("Capability 009 - Not started", content)

        def test_current_baseline_references_are_v06(self) -> None:
            for relative in (
                "docs/product/Decision_Log.md",
                "docs/product/Release_v1.0.md",
            ):
                self.assertIn("2026.08.01v06", self.content(relative))

        def test_completed_runtime_is_not_listed_as_planned(self) -> None:
            scorecard = self.content("docs/VERSION_ONE_SCORECARD.md")
            for area in (
                "Editorial Workspace",
                "Editorial Intake",
                "Source Assessment",
                "Evidence Validation",
                "LMHS Editorial Risk",
                "Editorial Confidence Translation",
            ):
                row = next(line for line in scorecard.splitlines() if f"| {area} |" in line)
                self.assertIn("| Complete |", row)

        def test_owning_generators_include_reference_repairs(self) -> None:
            capability006 = self.content(
                "scripts/bootstrap_capability006_editorial_integrity.py"
            )
            capability006a = self.content(
                "scripts/bootstrap_capability006a_constitutional_freeze.py"
            )
            self.assertNotIn("ADR-002 - Adaptive Editorial Context", capability006)
            self.assertIn("2026.08.01v06", capability006)
            self.assertIn(
                "| Evidence Validation | Complete | Capability 008 runtime |",
                capability006a,
            )


    if __name__ == "__main__":
        unittest.main()
    ''')


CONTRIBUTING = clean(
    r"""
    # Contributing

    Thank you for contributing to Ramrattan AI Editorial Studio.

    Trust before convenience.

    The repository is the source of truth for repository state. Contributions
    follow the Constitution and the Capability Delivery Workflow.

    ## Authority and Required Reading

    The Repository Author's or an explicitly authorized Repository Maintainer's
    current request defines the maximum scope and authorization for a task.
    Repository governance defines how authorized work is performed.

    Before capability work, read:

    - `AGENTS.md`
    - `AGENT_MEMORY.md`
    - `CONTRIBUTING.md`
    - `docs/constitution/Constitution.md`
    - `docs/constitution/Canonical_Vocabulary.md`
    - `docs/engineering/Capability_Delivery_Workflow.md`
    - the current architecture baseline and relevant ADRs
    - the active capability plan, roadmap, and scorecard

    `AGENTS.md` is the operational agent contract. `AGENT_MEMORY.md` is
    advisory experience and never overrides normative repository guidance.

    ## Development Model

    - `main` contains stable releases.
    - `develop` contains integrated work for the next release.
    - Feature and documentation branches contain one focused increment.

    Verify a clean, synchronized `develop` before branch creation. Treat
    pre-existing changes as human-owned work and never discard, overwrite, stage,
    or relocate them without explicit authorization.

    Recommended branch names:

    ```text
    feature/short-description
    docs/short-description
    fix/short-description
    test/short-description
    ```

    ## Capability Delivery Workflow

    Use `scripts/capability_delivery.py` to determine the next safe state. Do
    not reconstruct or skip the workflow manually.

    The canonical lifecycle is:

    1. Verify baseline.
    2. Create or resume the feature branch.
    3. Create the bootstrap.
    4. Preview.
    5. Apply.
    6. Recover from partial apply when necessary.
    7. Validate.
    8. Synchronize GitHub planning.
    9. Review local changes.
    10. Stage and review staged changes.
    11. Commit.
    12. Push.
    13. Create or reuse the pull request.
    14. Wait for successful CI and required review state.
    15. Merge and delete the feature branch.
    16. Return to clean, synchronized `develop`.
    17. Synchronize completion planning.

    Resume from the helper's verified state. Recover a partial transition
    instead of restarting it.

    ## Autonomous Work and Approval Profiles

    Inspection, in-scope editing, bootstrap preview and apply, validation,
    non-destructive repair, and diff review may proceed autonomously once the
    phase is authorized.

    Explicit approval from the Repository Author or an explicitly authorized
    Repository Maintainer is required before:

    - staging changes with `git add`;
    - commit;
    - push;
    - creating or mutating a pull request;
    - merge;
    - deleting branches;
    - creating, editing, closing, or reopening issues;
    - changing GitHub Project or milestone state;
    - changing the frozen Constitution or Canonical Vocabulary;
    - publication or external submission;
    - dependency installation; or
    - destructive or difficult-to-recover operations.

    An approval applies only to the described action, targets, and verified state.
    The Standard delegated delivery profile groups conditional authorization into
    Start, Publish, and Complete. Start ends before publication, Publish ends
    before merge, and Complete ends after verified cleanup and planning
    synchronization. Each prerequisite must be verified before advancing, and one
    profile never authorizes a later profile. Use the Conservative profile when
    approval is required at each mutation boundary. Read-only CI monitoring does
    not require a separate approval.

    ## Change Consolidation

    Before editing, inspect for other approved pending changes to the same files or
    tightly coupled concern. Consolidate them when scope, risk profile, and
    delivery timing agree. Separate them only for materially different scope,
    different risk or approval authority, safer rollback or recovery, conflicting
    delivery timing, or an explicit repository constraint. Do not split work merely
    to demonstrate incremental progress.

    ## Validation

    Before staging or commit, all contributions must pass:

    ```bash
    python3 -m compileall -q studio scripts tests
    python3 -m unittest discover -s tests -v
    python3 studio.py validate
    ```

    Repair failures within scope, regenerate when required, and rerun the
    complete suite. A merge, regeneration, or code change invalidates earlier
    validation.

    ## Generated Files

    Bootstrap scripts are canonical for the files and managed sections they
    declare. Generated artifacts are derived.

    When generated behavior or documentation changes:

    1. Update every affected implementation or document.
    2. Update every owning generator.
    3. Regenerate.
    4. Validate.
    5. Confirm the repair survives regeneration.

    Never repair only a generated artifact or only its generator.

    ## Governance and Architecture

    Create or update an ADR when a change establishes a lasting constraint,
    changes the system model, changes governance authority, or rejects a
    credible alternative.

    Update the architecture baseline only when executable architecture changes.
    Governance-only clarification does not require a new baseline.

    Planning and status artifacts are maintained by the capability that changes
    their facts. Do not create a separate reconciliation exercise unless it is
    explicitly required.

    ## Commits and Pull Requests

    Use a concise conventional commit message for one coherent increment.

    Pull requests must explain:

    - summary;
    - problem;
    - rationale;
    - changes;
    - validation;
    - architecture decision impact;
    - related issues; and
    - rollback.

    CI must pass before merge.

    ## Stopping Conditions

    Stop when the requested phase is complete, the next action is protected, a
    conflict requires the Repository Author's judgment, unrelated work makes continuation
    unsafe, validation cannot be repaired within scope, or the task would
    materially exceed its approved budget.

    ## Engineering Principles

    Prefer deterministic behavior, explicit state, reproducible workflows,
    repository evidence, focused changes, and comprehensive behavioral tests.

    Participation is governed by [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
    """
)


AGENTS_BLOCK = clean(
    r"""
    ## Governance Document Responsibilities

    Apply one authoritative owner for each governance concept:

    - the Constitution owns enduring product principles;
    - Canonical Vocabulary owns active product terminology;
    - accepted ADRs own durable architecture and governance decisions;
    - the current architecture baseline owns the coherent implemented
      architecture checkpoint;
    - the Capability Delivery Workflow owns delivery sequence and recovery;
    - `AGENTS.md` owns the operational contract for repository agents;
    - `CONTRIBUTING.md` translates repository governance for contributors;
    - `AGENT_MEMORY.md` preserves advisory, chronological experience;
    - `ROADMAP.md` owns current capability sequence and program status;
    - the Version 1.0 Scorecard owns release-readiness evidence; and
    - the Version 1.0 Release Definition owns the product promise and release
      boundary.

    Summaries must reference their authority rather than create competing
    rules. The capability that changes a governed fact updates its authority
    and affected summaries in the same increment.

    Historical capability sections are delivery records. They do not override
    a later, explicitly identified current-status section.

    A change to governance authority requires a focused ADR, contract tests,
    generator synchronization, complete validation, and deliberate review.
    """
)


MEMORY_BLOCK = clean(
    r"""
    # Authority and Lifecycle

    `AGENT_MEMORY.md` is advisory. It records engineering experience but never
    overrides the Constitution, Canonical Vocabulary, accepted ADRs, the
    current architecture baseline, the Capability Delivery Workflow,
    `AGENTS.md`, or `CONTRIBUTING.md`.

    This file must not define current repository status or silently create
    normative policy.

    Maintain it chronologically:

    - append dated lessons rather than rewriting history;
    - annotate a correction when an earlier lesson is no longer reliable;
    - promote a normative lesson into its authoritative governance document;
    - keep repository and GitHub state in their designated current-status
      records; and
    - keep entries concise, evidence-based, and actionable.
    """
)


ADR_INDEX = clean(
    r"""
    # Architecture Decision Records

    Architecture Decision Records - ADRs - capture significant product,
    architecture, engineering, and governance decisions.

    Each ADR explains:

    - Context
    - Decision
    - Alternatives considered
    - Consequences
    - Status

    ## Status Values

    - Proposed
    - Accepted
    - Superseded
    - Deprecated
    - Rejected

    ## Complete Record Index

    - [ADR-000 - Build AI Products Like Software](ADR-000-build-ai-products-like-software.md)
    - [ADR-001 - The Workflow Is the Product](ADR-001-the-workflow-is-the-product.md)
    - ADR-002 was never committed. Architecture Baseline v01 now references
      the surviving Adaptive Editorial Context architecture directly; no ADR
      has been recreated retroactively.
    - [ADR-003 - Adopt an Article-First Publication Package](ADR-003-adopt-an-article-first-publication-package.md)
    - [ADR-004 - Adopt Portable Editorial Projects](ADR-004-adopt-portable-editorial-projects.md)
    - [ADR-005 - Adopt the Editorial Integrity Pipeline](ADR-005-adopt-the-editorial-integrity-pipeline.md)
    - [ADR-006 - Adopt the Constitutional Model](ADR-006-adopt-the-constitutional-model.md)
    - [ADR-007 - Editorial Intake Runtime](ADR-007-editorial-intake-runtime.md)
    - [ADR-008 - Adopt the Capability Delivery Workflow](ADR-008-adopt-the-capability-delivery-workflow.md)
    - [ADR-009 - Adopt Editorial Discernment and Intent Preservation](ADR-009-adopt-editorial-discernment-and-intent-preservation.md)
    - [ADR-010 - Implement Evidence Validation and Editorial Risk](ADR-010-implement-evidence-validation-and-editorial-risk.md)
    - [ADR-011 - Governance Authority](ADR-011-governance-authority.md)
    """
)


STATUS_LINES = clean(
    """
    - Capability 008 - Complete
    - Capability 008A.1 - Governance Consolidation - In Progress
    - Capability 008A.2 - Delivery Hardening - Not started
    - Capability 008A.3 - Editorial Integrity Hardening - Not started
    - Capability 009 - Not started
    """
)


ROADMAP_BLOCK = (
    clean(
        """
    ## Capability 008A.1 - Governance Consolidation

    Status: **In Progress**

    Current authoritative sequence:
    """
    )
    + "\n"
    + STATUS_LINES
    + "\n"
    + clean(
        """
    Capability 008A.1 consolidates governance authority, repairs the broken
    ADR-002 reference honestly, aligns current status records, and adds focused
    governance contracts. It does not change product runtime or delivery-helper
    behavior.

    Architecture Baseline `2026.08.01v06` remains current. Capability 008A.1
    creates ADR-011 and no new architecture baseline.

    Earlier capability-specific status sections in this roadmap are historical
    delivery records. This section is authoritative for the active increment.
    """
    )
)


SCORECARD_BLOCK = (
    clean(
        """
    ## Capability 008A Engineering Hardening Status
    """
    )
    + "\n"
    + STATUS_LINES
    + "\n"
    + clean(
        """
    | Governance area | Status | Evidence |
    |---|---|---|
    | Agent operating contract | Complete | `AGENTS.md` and governance tests |
    | Advisory memory lifecycle | Complete | `AGENT_MEMORY.md` |
    | Contributor workflow alignment | Complete | `CONTRIBUTING.md` |
    | Governance authority | Complete | ADR-011 |
    | ADR-002 reference integrity | Complete | Baseline v01 direct architecture reference |
    | Current baseline | Complete | `2026.08.01v06` |

    Capability 008A.1 changes governance and status integrity only. It does not
    advance product-runtime release readiness.
    """
    )
)


CURRENT_FOCUS_BLOCK = (
    clean(
        """
    ## Current Implementation Status - Capability 008A.1
    """
    )
    + "\n"
    + STATUS_LINES
    + "\n"
    + clean(
        """
    The active engineering focus is Governance Consolidation. Product runtime
    remains at the completed Capability 008 baseline while governance
    authority, current status, and historical reference integrity are hardened.

    Earlier capability focus sections are delivery records. This section owns
    the current implementation status until the next increment updates it.
    """
    )
)


DECISION_LOG_BLOCK = clean(
    r"""
    ## Capability 008A.1 Governance Decisions

    | Date | Level | Decision | Rationale |
    |---|---:|---|---|
    | 2026-08-02 | D4 | Adopt explicit Governance Authority | Each governance concept requires one authoritative owner and deterministic precedence. |
    | 2026-08-02 | D4 | Keep `AGENT_MEMORY.md` advisory | Chronological experience must not silently become policy or current status. |
    | 2026-08-02 | D4 | Assign current-status responsibilities | Roadmap, scorecard, release definition, and architecture records answer different status questions. |
    | 2026-08-02 | D4 | Do not recreate ADR-002 | No ADR-002 artifact exists in repository history; the broken reference is repaired to surviving architecture evidence. |
    | 2026-08-02 | D4 | Retain Architecture Baseline 2026.08.01v06 | Governance clarification does not change executable architecture. |

    ADR-011 records the durable governance decision.
    """
)


RELEASE_BLOCK = (
    clean(
        """
    ## Current Version 1.0 Implementation Status
    """
    )
    + "\n"
    + STATUS_LINES
    + "\n"
    + clean(
        """
    Architecture Baseline `2026.08.01v06` remains the current runtime baseline.
    Capability 008A.1 hardens governance and does not add Version 1.0 product
    behavior. Capability 009 remains not started until all Capability 008A
    handoff criteria are satisfied.
    """
    )
)


ISSUE_BODY = clean(
    r"""
    ## Objective

    Establish an unambiguous, testable governance authority model before
    Delivery Hardening or further product implementation begins.

    ## Scope

    - Validate the complete `AGENTS.md` operating contract
    - Define the advisory lifecycle of `AGENT_MEMORY.md`
    - Align `CONTRIBUTING.md` with current governance
    - Record ADR-011 - Governance Authority
    - Repair ADR-002 reference integrity without inventing history
    - Reconcile the current roadmap, scorecard, product focus, decision log,
      release status, and baseline references assigned to 008A.1
    - Add focused governance contract tests
    - Keep generated artifacts and owning bootstraps synchronized

    ## Exclusions

    - Product runtime
    - Evidence Validation
    - StageState
    - Delivery-helper behavior
    - CI changes
    - Capability 008A.2, Capability 008A.3, or Capability 009 implementation

    ## Architecture

    - ADR-011 required
    - No new architecture baseline
    - Architecture Baseline 2026.08.01v06 remains current

    ## Budget

    Hard limit: approximately 10-15 files. Material excess requires re-scoping.

    ## Acceptance Criteria

    - Governance authority and document responsibilities are explicit
    - Approval, validation, generator, dirty-tree, autonomy, and stopping rules
      remain complete
    - `AGENT_MEMORY.md` is explicitly advisory and append-oriented
    - ADR-002 is not recreated without evidence
    - Current status records agree
    - Capability 008A.2 and 008A.3 remain not started
    - Capability 009 remains Todo
    - Complete repository validation passes
    """
)


PROJECT_README = clean(
    r"""
    # Ramrattan AI Editorial Studio

    ## Governing principle

    Trust is our most valuable feature.

    ## Current implementation

    - Capabilities 001-008 - complete
    - Capability 008A.1 - Governance Consolidation - In Progress
    - Capability 008A.2 - Delivery Hardening - Not started
    - Capability 008A.3 - Editorial Integrity Hardening - Not started
    - Capability 009 - Article Engine and Publication Package - Todo

    ## Active engineering hardening increment

    Capability 008A.1 establishes Governance Authority through ADR-011,
    validates the agent operating contract, makes Agent Memory explicitly
    advisory, aligns contributor guidance, repairs ADR-002 reference integrity
    without inventing history, and reconciles assigned current-status records.

    Architecture Baseline 2026.08.01v06 remains current. No new architecture
    baseline is created for Governance Consolidation.

    ## Program sequence

    Capability 008A.1 must complete before Capability 008A.2 begins.
    Capability 008A.2 must complete before Capability 008A.3 begins.
    Capability 009 begins only after the complete Capability 008A program.
    """
)


GENERATED_FILES = {
    "docs/architecture/adr/ADR-011-governance-authority.md": ADR_011,
    "tests/test_capability008a1_governance.py": GOVERNANCE_TESTS,
}


FULL_FILES = {
    "CONTRIBUTING.md": CONTRIBUTING,
    "docs/architecture/adr/README.md": ADR_INDEX,
}


MARKER_BLOCKS = {
    "AGENTS.md": ("CAPABILITY_008A1_GOVERNANCE_AUTHORITY", AGENTS_BLOCK),
    "AGENT_MEMORY.md": ("CAPABILITY_008A1_MEMORY_GOVERNANCE", MEMORY_BLOCK),
    "ROADMAP.md": ("CAPABILITY_008A1_ROADMAP", ROADMAP_BLOCK),
    "docs/VERSION_ONE_SCORECARD.md": (
        "CAPABILITY_008A1_SCORECARD",
        SCORECARD_BLOCK,
    ),
    "docs/product/Current_Product_Focus.md": (
        "CAPABILITY_008A1_CURRENT_FOCUS",
        CURRENT_FOCUS_BLOCK,
    ),
    "docs/product/Decision_Log.md": (
        "CAPABILITY_008A1_DECISION_LOG",
        DECISION_LOG_BLOCK,
    ),
    "docs/product/Release_v1.0.md": (
        "CAPABILITY_008A1_RELEASE_STATUS",
        RELEASE_BLOCK,
    ),
}


BASELINE_PATH = (
    "docs/architecture/baselines/Architecture_Baseline_2026.08.01v01.md"
)
CAPABILITY006_BOOTSTRAP = "scripts/bootstrap_capability006_editorial_integrity.py"
CAPABILITY006A_BOOTSTRAP = (
    "scripts/bootstrap_capability006a_constitutional_freeze.py"
)


EXPECTED_PATHS = {
    SCRIPT_PATH,
    *GENERATED_FILES,
    *FULL_FILES,
    *MARKER_BLOCKS,
    BASELINE_PATH,
    CAPABILITY006_BOOTSTRAP,
    CAPABILITY006A_BOOTSTRAP,
}


class CapabilityError(RuntimeError):
    """Raised when Capability 008A.1 cannot proceed safely."""


def run(
    command: list[str],
    *,
    cwd: Path,
    capture: bool = False,
) -> subprocess.CompletedProcess[str]:
    print("$", " ".join(command))
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=capture,
        check=True,
    )


def output(command: list[str], *, cwd: Path) -> str:
    return run(command, cwd=cwd, capture=True).stdout.strip()


def json_output(command: list[str], *, cwd: Path) -> Any:
    raw = output(command, cwd=cwd)
    if not raw:
        return None
    return json.loads(raw)


def repository_root() -> Path:
    root = Path(
        output(["git", "rev-parse", "--show-toplevel"], cwd=Path.cwd())
    ).resolve()
    if root.name != EXPECTED_REPOSITORY:
        raise CapabilityError(
            f"Expected repository {EXPECTED_REPOSITORY}, found {root.name}."
        )
    remote = output(["git", "remote", "get-url", "origin"], cwd=root)
    if EXPECTED_REMOTE_FRAGMENT not in remote:
        raise CapabilityError("Origin does not match the expected repository.")
    branch = output(["git", "branch", "--show-current"], cwd=root)
    if branch != EXPECTED_BRANCH:
        raise CapabilityError(f"Expected branch {EXPECTED_BRANCH}, found {branch}.")
    return root


def verify_script_integrity(root: Path) -> None:
    content = (root / SCRIPT_PATH).read_text(encoding="utf-8")
    if SCRIPT_SENTINEL not in content:
        raise CapabilityError("Bootstrap sentinel is missing.")
    print("Bootstrap integrity check passed.")


def working_tree_lines(root: Path) -> list[str]:
    status = run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=root,
        capture=True,
    ).stdout
    return [line for line in status.splitlines() if line.strip()]


def verify_expected_working_tree(root: Path) -> None:
    unexpected: list[str] = []
    for line in working_tree_lines(root):
        relative = line[3:]
        if " -> " in relative:
            relative = relative.split(" -> ", 1)[1]
        if relative not in EXPECTED_PATHS:
            unexpected.append(line)
    if unexpected:
        raise CapabilityError(
            "Unexpected working-tree changes:\n" + "\n".join(unexpected)
        )
    print("Working tree contains only expected Capability 008A.1 paths.")


def managed_block(name: str, content: str) -> str:
    return f"<!-- {name}_START -->\n\n{content.rstrip()}\n\n<!-- {name}_END -->"


def upsert(path: Path, name: str, content: str) -> None:
    original = path.read_text(encoding="utf-8")
    start = f"<!-- {name}_START -->"
    end = f"<!-- {name}_END -->"
    if (start in original) != (end in original):
        raise CapabilityError(f"Incomplete marker pair in {path}.")
    block = managed_block(name, content)
    if start in original:
        before, remainder = original.split(start, 1)
        _, after = remainder.split(end, 1)
        updated = before.rstrip() + "\n\n" + block
        if after.strip():
            updated += "\n\n" + after.strip()
    else:
        updated = original.rstrip() + "\n\n" + block
    path.write_text(updated.rstrip() + "\n", encoding="utf-8")


def replace_once(path: Path, old: str, new: str) -> None:
    content = path.read_text(encoding="utf-8")
    if new in content:
        return
    count = content.count(old)
    if count != 1:
        raise CapabilityError(
            f"Expected one replacement target in {path}; found {count}."
        )
    path.write_text(content.replace(old, new, 1), encoding="utf-8")


def replace_version_after_heading(
    path: Path,
    heading: str,
    old_version: str,
    new_version: str,
) -> None:
    content = path.read_text(encoding="utf-8")
    pattern = re.compile(
        rf"({re.escape(heading)}\s+```text\s+){re.escape(old_version)}(\s+```)",
        re.MULTILINE,
    )
    if re.search(
        rf"{re.escape(heading)}\s+```text\s+{re.escape(new_version)}\s+```",
        content,
        re.MULTILINE,
    ):
        return
    updated, count = pattern.subn(rf"\g<1>{new_version}\g<2>", content, count=1)
    if count != 1:
        raise CapabilityError(f"Could not update {heading} in {path}.")
    path.write_text(updated, encoding="utf-8")


def apply_reference_and_status_repairs(root: Path) -> None:
    baseline_old = "- ADR-002 - Adaptive Editorial Context"
    baseline_new = (
        "- Adaptive Editorial Context architecture - "
        "`docs/architecture/Editorial_Context_Model.md`"
    )
    for relative in (BASELINE_PATH, CAPABILITY006_BOOTSTRAP):
        replace_once(root / relative, baseline_old, baseline_new)

    for relative in (
        "docs/product/Release_v1.0.md",
        CAPABILITY006_BOOTSTRAP,
    ):
        replace_version_after_heading(
            root / relative,
            "Architecture baseline:",
            "2026.08.01v01",
            "2026.08.01v06",
        )

    replace_version_after_heading(
        root / "docs/product/Decision_Log.md",
        "## Active Architecture Baseline",
        "2026.08.01v01",
        "2026.08.01v06",
    )
    replace_version_after_heading(
        root / CAPABILITY006_BOOTSTRAP,
        "## Active Architecture Baseline",
        "{ARCHITECTURE_BASELINE_VERSION}",
        "2026.08.01v06",
    )

    scorecard_rows = {
        "| Editorial Workspace | Planned | Capability 007 |":
            "| Editorial Workspace | Complete | Capability 007 runtime |",
        "| Editorial Intake | Planned | Capability 007 |":
            "| Editorial Intake | Complete | Capability 007 runtime |",
        "| Source Assessment | Planned | Capability 007 |":
            "| Source Assessment | Complete | Capability 007 runtime |",
        "| Evidence Validation | Planned | Capability 008 |":
            "| Evidence Validation | Complete | Capability 008 runtime |",
        "| LMHS Editorial Risk | Planned | Capability 008 |":
            "| LMHS Editorial Risk | Complete | Capability 008 runtime |",
        "| Editorial Confidence Translation | Planned | Capability 008 |":
            "| Editorial Confidence Translation | Complete | Capability 008 runtime |",
    }
    for relative in (
        "docs/VERSION_ONE_SCORECARD.md",
        CAPABILITY006A_BOOTSTRAP,
    ):
        for old, new in scorecard_rows.items():
            replace_once(root / relative, old, new)

    replace_once(
        root / "AGENT_MEMORY.md",
        "The Author strongly prefers one verified step at a time.",
        "Nilesh prefers one verified step at a time.",
    )


def write_repository_changes(root: Path) -> None:
    for relative, content in GENERATED_FILES.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"Wrote {relative}")
    for relative, content in FULL_FILES.items():
        (root / relative).write_text(content, encoding="utf-8")
        print(f"Wrote {relative}")
    for relative, (name, content) in MARKER_BLOCKS.items():
        upsert(root / relative, name, content)
        print(f"Updated {relative}")
    apply_reference_and_status_repairs(root)
    print("Applied baseline, scorecard, and generator repairs.")


def validate_governance(root: Path) -> None:
    required = set(GENERATED_FILES) | set(FULL_FILES) | set(MARKER_BLOCKS)
    required |= {BASELINE_PATH, CAPABILITY006_BOOTSTRAP, CAPABILITY006A_BOOTSTRAP}
    missing = [relative for relative in sorted(required) if not (root / relative).is_file()]
    if missing:
        raise CapabilityError("Missing required files:\n" + "\n".join(missing))

    agents = (root / "AGENTS.md").read_text(encoding="utf-8")
    if len(re.findall(r"^```", agents, re.MULTILINE)) % 2:
        raise CapabilityError("AGENTS.md contains unbalanced Markdown fences.")

    checks = {
        "AGENTS.md": (
            "Governance Document Responsibilities",
            "Dirty-Tree Protection",
            "Approval Boundaries",
            "Stopping Conditions",
        ),
        "AGENT_MEMORY.md": ("advisory", "append dated lessons"),
        "CONTRIBUTING.md": (
            "staging changes with `git add`",
            "Never repair only a generated artifact",
            "The Standard delegated delivery profile",
            "## Change Consolidation",
        ),
        "docs/architecture/adr/ADR-011-governance-authority.md": (
            "Governance Authority",
            "No new architecture baseline",
            "ADR-002 is not recreated retroactively",
        ),
        "ROADMAP.md": (
            "Capability 008A.1 - Governance Consolidation - In Progress",
            "Capability 009 - Not started",
        ),
    }
    for relative, phrases in checks.items():
        content = (root / relative).read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in content:
                raise CapabilityError(f"Missing '{phrase}' in {relative}.")

    if (root / "docs/architecture/adr/ADR-002.md").exists():
        raise CapabilityError("ADR-002 must not be invented.")
    print("Capability 008A.1 governance validation passed.")


def run_repository_validation(root: Path) -> None:
    run(
        [sys.executable, "-m", "compileall", "-q", "studio", "scripts", "tests"],
        cwd=root,
    )
    run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=root,
    )
    run([sys.executable, "studio.py", "validate"], cwd=root)
    run(["git", "diff", "--check"], cwd=root)
    print("Complete repository validation passed.")


def preview() -> None:
    print("Capability 008A.1 Governance Consolidation preview\n")
    print("File budget: 15 files (approved range: 10-15)\n")
    print("New generated files:")
    for relative in GENERATED_FILES:
        print(f"  - {relative}")
    print("\nManaged or regenerated files:")
    for relative in sorted(EXPECTED_PATHS - {SCRIPT_PATH, *GENERATED_FILES}):
        print(f"  - {relative}")
    print("\nDecisions:")
    for decision in (
        "Adopt ADR-011 - Governance Authority",
        "Keep AGENT_MEMORY.md advisory and chronological",
        "Align contributor governance and approval boundaries",
        "Repair ADR-002 reference integrity without inventing history",
        "Keep Architecture Baseline 2026.08.01v06 current",
        "Reconcile only the status records assigned to Capability 008A.1",
        "Keep Capability 008A.2, 008A.3, and 009 not started",
    ):
        print(f"  - {decision}")
    print("\nPreview mode changes nothing.")


def project_payload(root: Path) -> dict[str, Any]:
    payload = json_output(
        [
            "gh", "project", "view", str(PROJECT_NUMBER), "--owner", OWNER,
            "--format", "json",
        ],
        cwd=root,
    )
    return payload if isinstance(payload, dict) else {}


def issue_list(root: Path) -> list[dict[str, Any]]:
    payload = json_output(
        [
            "gh", "issue", "list", "--repo", REPOSITORY, "--state", "all",
            "--limit", "300", "--json", "number,title,url,state",
        ],
        cwd=root,
    )
    return payload if isinstance(payload, list) else []


def exact_issues(root: Path, title: str) -> list[dict[str, Any]]:
    return [issue for issue in issue_list(root) if issue.get("title") == title]


def ensure_issue(root: Path) -> dict[str, Any]:
    matches = exact_issues(root, ISSUE_TITLE)
    if len(matches) > 1:
        raise CapabilityError(f"Duplicate issues exist for {ISSUE_TITLE}.")
    if matches:
        issue = matches[0]
        if issue.get("state") == "CLOSED":
            run(
                ["gh", "issue", "reopen", str(issue["number"]), "--repo", REPOSITORY],
                cwd=root,
            )
        return issue

    run(
        [
            "gh", "issue", "create", "--repo", REPOSITORY,
            "--title", ISSUE_TITLE, "--body", ISSUE_BODY,
        ],
        cwd=root,
    )
    for attempt in range(1, 6):
        matches = exact_issues(root, ISSUE_TITLE)
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1:
            raise CapabilityError(f"Duplicate issues exist for {ISSUE_TITLE}.")
        print(f"Issue not visible yet ({attempt}/5); waiting...")
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
    if not isinstance(payload, dict):
        return []
    items = payload.get("items", [])
    return items if isinstance(items, list) else []


def project_item_for_url(root: Path, url: str) -> dict[str, Any] | None:
    for item in project_items(root):
        content = item.get("content") or {}
        if content.get("url") == url:
            return item
    return None


def ensure_project_item(root: Path, url: str) -> dict[str, Any]:
    existing = project_item_for_url(root, url)
    if existing is not None:
        return existing
    run(
        [
            "gh", "project", "item-add", str(PROJECT_NUMBER), "--owner", OWNER,
            "--url", url,
        ],
        cwd=root,
    )
    for attempt in range(1, 11):
        item = project_item_for_url(root, url)
        if item is not None:
            return item
        print(f"Project item not visible yet ({attempt}/10); waiting...")
        time.sleep(2)
    raise CapabilityError("Project item did not become visible.")


def set_status(root: Path, item_id: str, status: str) -> None:
    run(
        [
            "gh", "project", "item-edit", "--id", item_id,
            "--project-id", PROJECT_ID, "--field-id", STATUS_FIELD_ID,
            "--single-select-option-id", STATUS_OPTIONS[status],
        ],
        cwd=root,
    )


def preserve_existing_status(root: Path, title: str, status: str) -> None:
    matches = exact_issues(root, title)
    if len(matches) > 1:
        raise CapabilityError(f"Duplicate issues exist for {title}.")
    if not matches:
        print(f"No issue exists for {title}; preserving it as not started.")
        return
    item = ensure_project_item(root, matches[0]["url"])
    set_status(root, item["id"], status)
    print(f"Preserved {title} as {status}.")


def verify_planning(root: Path, issue: dict[str, Any]) -> None:
    matches = exact_issues(root, ISSUE_TITLE)
    if len(matches) != 1 or matches[0].get("state") != "OPEN":
        raise CapabilityError("Capability 008A.1 issue state is not uniquely Open.")
    item = project_item_for_url(root, issue["url"])
    if item is None or item.get("status") != "In Progress":
        raise CapabilityError("Capability 008A.1 Project item is not In Progress.")
    for title in (CAPABILITY_008A2_TITLE, CAPABILITY_008A3_TITLE):
        for candidate in exact_issues(root, title):
            candidate_item = project_item_for_url(root, candidate["url"])
            if candidate_item is not None and candidate_item.get("status") != "Todo":
                raise CapabilityError(f"{title} is not preserved as Todo.")
    capability009 = exact_issues(root, CAPABILITY_009_TITLE)
    if len(capability009) != 1:
        raise CapabilityError("Capability 009 issue could not be resolved uniquely.")
    capability009_item = project_item_for_url(root, capability009[0]["url"])
    if capability009_item is None or capability009_item.get("status") != "Todo":
        raise CapabilityError("Capability 009 must remain Todo.")
    readme = project_payload(root).get("readme", "")
    if "Capability 008A.1 - Governance Consolidation - In Progress" not in readme:
        raise CapabilityError("Project summary does not record 008A.1 In Progress.")
    print("GitHub planning verification passed.")


def sync_project(root: Path) -> None:
    validate_governance(root)
    run_repository_validation(root)
    run(["gh", "auth", "status"], cwd=root)
    project = project_payload(root)
    if project.get("id") != PROJECT_ID:
        raise CapabilityError("GitHub Project identity does not match Project #1.")

    issue = ensure_issue(root)
    item = ensure_project_item(root, issue["url"])
    set_status(root, item["id"], "In Progress")
    preserve_existing_status(root, CAPABILITY_008A2_TITLE, "Todo")
    preserve_existing_status(root, CAPABILITY_008A3_TITLE, "Todo")
    preserve_existing_status(root, CAPABILITY_009_TITLE, "Todo")

    run(
        [
            "gh", "project", "edit", str(PROJECT_NUMBER), "--owner", OWNER,
            "--readme", PROJECT_README,
        ],
        cwd=root,
    )
    verify_planning(root, issue)
    print(f"Capability 008A.1 planning synchronized using issue #{issue['number']}.")


def show_status(root: Path) -> None:
    run(["git", "status", "--short"], cwd=root)
    run(["git", "diff", "--stat"], cwd=root)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--apply", action="store_true")
    modes.add_argument("--sync-project", action="store_true")
    args = parser.parse_args()

    try:
        root = repository_root()
        verify_script_integrity(root)
        verify_expected_working_tree(root)

        if args.sync_project:
            sync_project(root)
        elif args.apply:
            write_repository_changes(root)
            validate_governance(root)
            run_repository_validation(root)
            show_status(root)
        else:
            preview()
        return 0
    except (CapabilityError, subprocess.CalledProcessError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


# CAPABILITY_008A1_GOVERNANCE_BOOTSTRAP_COMPLETE


if __name__ == "__main__":
    raise SystemExit(main())
