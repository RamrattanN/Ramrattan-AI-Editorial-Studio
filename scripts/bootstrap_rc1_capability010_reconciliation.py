#!/usr/bin/env python3
"""Reconcile RC1 documentation after delivered Capability 010."""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
import textwrap
from pathlib import Path


EXPECTED_REPOSITORY = "Ramrattan-AI-Editorial-Studio"
EXPECTED_BRANCH = "docs/rc1-capability-010-reconciliation"
SCRIPT_PATH = "scripts/bootstrap_rc1_capability010_reconciliation.py"
CAPABILITY010_OWNER = "scripts/bootstrap_capability010_hero_visual_system.py"
RC1_OWNER = "scripts/bootstrap_rc1_checkpoint_authorization_hardening.py"
SCORECARD_OWNER = "scripts/bootstrap_capability006a_constitutional_freeze.py"
CHECKPOINT_PATH = "docs/product/checkpoints/RC1_Checkpoint_2026.08.02v02.md"
TEST_PATH = "tests/test_rc1_checkpoint.py"
SENTINEL = "RC1_CAPABILITY010_RECONCILIATION_COMPLETE"
MARK_HASH = "b2cd1c22239b7176b43578892b0c37ac502ca5ab696b7c083a0b397bfe285727"
LOCKUP_HASH = "ae56f16f3e4b3a2bfbf5cefbf6ee807482cd8814e30b7496a917b9eae3a5ba72"
ARTICLE_ENGINE_HASH = "653db77e8881aa6532906fa1b17a8c771152cfe14ef1266383daba423d596868"
PUBLICATION_PACKAGE_HASH = "1e6cc91dda667f9b87eee248f563771f2cb99f0954346f3aef6f0e0bcb62d64b"


class BootstrapError(RuntimeError):
    """Raised when reconciliation cannot continue safely."""


def clean(value: str) -> str:
    return textwrap.dedent(value).strip() + "\n"


CAPABILITY010_FILES = {
    "docs/architecture/adr/ADR-016-hero-visual-system.md": clean('''
        # ADR-016 - Hero Visual System

        ## Status

        Accepted. Delivered by Capability 010 in PR #46.

        ## Date

        2026-08-02

        ## Decision Level

        D4 - Architecture

        ## Context

        Capability 009 produces an approved Hero Visual prompt but intentionally does
        not render an image. Version 1 requires a 720 × 425 Hero Visual while repository
        validation must remain deterministic, offline, and independent of any external
        generation service.

        ## Decision

        Adopt one provider-independent Hero Visual System. The core validates requests,
        applies explicit policy constraints, invokes a selected provider, validates the
        returned artifact and provenance, and exposes distinct success and failure
        states.

        Require a 720 × 425 PNG output contract for Version 1. Include an offline
        deterministic provider for tests and demonstrations. Treat every provider
        response as untrusted until core validation passes.

        Integrate with the Publication Package only by attaching one existing result
        whose prompt matches the approved Capability 009 prompt. Do not silently invoke
        a provider, regenerate approved content, or claim Portable Project completion.

        ## Constitutional Impact

        The decision implements Understanding Before Generation, Evidence Before
        Assertion, Trust Above All, Professional Judgement, Author ownership, and
        approved-component preservation. It changes no frozen constitutional principle
        or canonical term.

        ## Alternatives Considered

        ### Require one external image provider

        Rejected because validation would depend on network access, credentials, and
        provider availability, and provider behavior could leak into the core contract.

        ### Trust provider metadata without validating the artifact

        Rejected because dimensions, format, content availability, and provenance must
        be verified rather than asserted.

        ### Generate the visual during Publication Package assembly

        Rejected because it would silently couple package construction to generation
        and make focused revision and failure recovery unsafe.

        ### Implement Portable Project or UI behavior simultaneously

        Rejected because those are later or separate product surfaces and would expand
        Capability 010 beyond its approved boundary.

        ## Consequences

        The repository can deterministically demonstrate and validate Hero Visual
        generation without an external service. Future providers may implement the
        same boundary without changing Publication Package semantics. Version 1 remains
        incomplete until Capability 011 and end-to-end release-readiness work complete.

        ## Architecture Baseline

        Recorded by Architecture Baseline `2026.08.02v12`.
    '''),
    "docs/architecture/baselines/Architecture_Baseline_2026.08.02v12.md": clean('''
        # Architecture Baseline - 2026.08.02v12

        ## Status

        Current delivered architecture baseline. Capability 010 was delivered by PR
        #46.

        ## Baseline ID

        `2026.08.02v12`

        ## Supersedes

        `2026.08.02v11`

        ## Reason for Revision

        Add the provider-independent Hero Visual System and the narrow Publication
        Package attachment boundary required for a validated 720 × 425 visual.

        ## Runtime Architecture

        - `studio/hero_visual.py` owns request validation, policy constraints, provider
          selection, artifact validation, provenance, and explicit outcome states.
        - `HeroVisualProvider` is the stable provider-neutral generation boundary.
        - `DeterministicHeroVisualProvider` supplies an offline, repeatable PNG artifact
          for tests, demos, and repository validation.
        - `studio/publication_package.py` attaches one existing result without invoking
          generation or modifying textual package content.

        ## Trust and Failure Model

        Provider output is untrusted until the core verifies format, dimensions,
        artifact presence, PNG header, and provenance. Malformed requests, unsupported
        providers, generation failures, validation failures, and policy blocks remain
        distinct and cannot be presented as ready.

        ## Explicit Exclusions

        No Portable Editorial Project, project resume or export, workspace,
        collaboration, orchestration, UI, publishing automation, release packaging,
        B002, or Version 2 architecture is introduced.

        ## Architecture Decision

        ADR-016 records the durable decision.
    '''),
}


CAPABILITY010_MANAGED = {
    "ROADMAP.md": ("CAPABILITY_010_ROADMAP", clean('''
        ## Capability 010 - Hero Visual System

        Status: **Complete**

        Approved scope:

        - [x] Provider-independent Hero Visual boundary
        - [x] Validated 720 × 425 PNG contract
        - [x] Deterministic offline validation provider
        - [x] Explicit generation, validation, provider, request, and policy states
        - [x] Narrow Publication Package attachment boundary
        - [x] Approved prompt and textual-content preservation

        Capability 010 was delivered by PR #46; issue #16 is closed. Capability 011 is
        Next, Todo, and unstarted. B002 remains Todo, Low Priority, Post-RC1, and
        non-blocking. Architecture Baseline `2026.08.02v12` is current.

        No Portable Project, workspace, collaboration, orchestration, UI, publishing
        automation, release packaging, or Version 2 behavior is included.
    ''')),
    "docs/VERSION_ONE_SCORECARD.md": ("CAPABILITY_010_SCORECARD", clean('''
        ## Capability 010 Progress

        | Area | Status | Evidence |
        |---|---|---|
        | Capability 009 | Complete | Article Engine and textual Publication Package |
        | Capability 010 | Complete | PR #46 and closed issue #16 |
        | Hero Visual provider boundary | Complete | `studio/hero_visual.py` |
        | 720 × 425 output validation | Complete | Behavioral tests |
        | Deterministic offline provider | Complete | Repeatability tests |
        | Explicit failure states | Complete | Generation and validation tests |
        | Publication Package integration | Complete | Pending/ready/failed/blocked tests |
        | ADR-016 | Accepted | Hero Visual System decision |
        | Capability 011 | Next, Todo, and unstarted | Issue #17 |
        | B002 | Todo, Low Priority, Post-RC1, non-blocking | Issue #41 |
        | Current delivered baseline | Complete | `2026.08.02v12` |

        Version 1 remains incomplete until Capability 011 and end-to-end release
        readiness are delivered.
    ''')),
    "docs/product/Current_Product_Focus.md": ("CAPABILITY_010_CURRENT_FOCUS", clean('''
        ## Capability 010 Delivered State

        Capability 010 delivered the provider-independent Hero Visual System for the
        existing Capability 009 Publication Package. It consumes the approved prompt,
        preserves visual intent, validates a 720 × 425 PNG and its provenance, and
        returns explicit safe failure states when generation cannot be trusted.

        The Publication Package integration attaches one existing result without
        regenerating approved article content. PR #46 is merged, issue #16 is closed,
        ADR-016 is Accepted, and baseline `2026.08.02v12` is current. Capability 011 is
        Next, Todo, and unstarted. B002 remains deferred, Low Priority, Post-RC1, and
        non-blocking.

        No Portable Project, workspace, collaboration, orchestration, UI, publishing
        automation, release packaging, or Version 2 behavior is part of this focus.
    ''')),
    "docs/product/Release_v1.0.md": ("CAPABILITY_010_RELEASE_STATUS", clean('''
        ## Capability 010 Release Contribution

        Capability 010 is Complete and delivers the provider-independent 720 × 425 Hero
        Visual System, deterministic validation provider, explicit failure states, and
        the narrow Publication Package attachment boundary.

        PR #46 is merged, issue #16 is closed, ADR-016 is Accepted, and Architecture
        Baseline `2026.08.02v12` is current.

        Version 1 remains incomplete. Capability 011 Portable Editorial Project resume
        and export and issue #18 end-to-end release-readiness evidence remain
        outstanding. B002 remains non-blocking Post-RC1 work.
    ''')),
}


RC1_MANAGED = {
    "ROADMAP.md": ("RC1_CHECKPOINT_CURRENT_STATUS", clean('''
        ## RC1 Checkpoint - Current Status

        - Capability 009 - Complete
        - Capability 010 - Complete (PR #46; issue #16 closed)
        - Initiative B001 - Complete
        - RC1 Documentation Reconciliation after Capability 010 - In Progress
        - Capability 011 - Next, Todo, and unstarted
        - B002 - Todo, Low Priority, Post-RC1, and non-blocking
        - Current delivered architecture baseline - `2026.08.02v12`

        Version 1 is not release-ready. Capability 011 and the end-to-end
        release-readiness evidence in issue #18 remain outstanding. Earlier capability
        status sections are historical delivery records; this section is authoritative
        for the current checkpoint increment.
    ''')),
    "docs/VERSION_ONE_SCORECARD.md": ("RC1_CHECKPOINT_CURRENT_STATUS", clean('''
        ## RC1 Checkpoint - Current Status

        | Area | Status | Evidence |
        |---|---|---|
        | Capability 009 | Complete | PR #43 and ADR-015 |
        | Initiative B001 | Complete | PR #42 and approved master hashes |
        | Capability 010 | Complete | PR #46, closed issue #16, and ADR-016 |
        | Capability 011 | Next, Todo, and unstarted | Issue #17 |
        | B002 | Todo, Low Priority, Post-RC1, non-blocking | Issue #41 |
        | Current delivered baseline | Complete | `2026.08.02v12` |
        | Complete RC1 readiness | Blocked | Capability 011 and issue #18 |

        The Article Engine, Publication Package, and Hero Visual System are delivered.
        Version 1 is not release-ready until the Portable Project and end-to-end
        release-readiness evidence are complete.
    ''')),
    "docs/product/Current_Product_Focus.md": ("RC1_CHECKPOINT_CURRENT_STATUS", clean('''
        ## RC1 Checkpoint - Current Product Status

        Capability 009 is complete.

        Capability 010 is complete. The Article Engine, Publication Package, and Hero
        Visual System are delivered under ADR-015, ADR-016, and baseline
        `2026.08.02v12`.

        Capability 011 is Next, Todo, and unstarted. B002 remains deferred, Low
        Priority, Post-RC1, and non-blocking. Version 1 is not release-ready until the
        Portable Project and end-to-end release-readiness work in issue #18 is complete.
    ''')),
    "docs/product/Release_v1.0.md": ("RC1_CHECKPOINT_CURRENT_STATUS", clean('''
        ## RC1 Checkpoint - Current Release Status

        - Capability 009 - Complete
        - Capability 010 - Complete (PR #46; issue #16 closed)
        - Capability 011 - Next, Todo, and unstarted
        - B001 - Complete
        - B002 - Todo, Low Priority, Post-RC1, and non-blocking
        - Current delivered architecture baseline - `2026.08.02v12`

        Version 1 is not release-ready. The Portable Editorial Project resume/export
        path and end-to-end release-readiness evidence in issue #18 remain outstanding.
    ''')),
    "docs/START_HERE.md": ("RC1_CHECKPOINT_DISCOVERY", clean('''
        ## RC1 Checkpoint

        The current evidence-based engineering and release checkpoint is:

        - `product/checkpoints/RC1_Checkpoint_2026.08.02v02.md`

        The prior checkpoint remains historical evidence:

        - `product/checkpoints/RC1_Checkpoint_2026.08.02.md`

        The current checkpoint distinguishes validated engineering readiness from
        complete RC1 readiness after Capability 010 delivery.
    ''')),
}


CHECKPOINT = clean('''
    # RC1 Checkpoint - 2026.08.02v02

    ## Checkpoint Basis

    - Verified pre-increment commit: `5f20cee82bad322976a0b5d3bed655f10a72d503`
    - Checkpoint date: 2026-08-02
    - Current delivered architecture baseline: `2026.08.02v12`
    - Tests before this reconciliation: 299 passed

    ## Repository Health

    At checkpoint start, `develop` was active and clean, local `develop` matched
    `origin/develop`, compileall passed, all 299 tests passed, repository validation
    passed for `v3.0.0-rc1`, and `git diff --check` passed.

    ## Product and Roadmap State

    Capabilities 001-010, the Capability 008A Engineering Hardening Program, and
    Initiative B001 are complete. Capability 010 was delivered by merged PR #46;
    issue #16 is closed and its Project item is Done. Capability 011 is Next, Todo,
    and unstarted. B002 remains Todo, Low Priority, Post-RC1, and non-blocking.

    Version 1 is not release-ready. Capability 011 Portable Project resume/export
    and the end-to-end release-readiness work tracked by open issue #18 remain
    outstanding.

    ## Architecture Integrity

    ADR-016 is Accepted and records the delivered Hero Visual System. Architecture
    Baseline `2026.08.02v12` is the current delivered baseline. No Capability 011,
    Portable Project, UI, release packaging, B002, or Version 2 behavior is included.

    ## Brand Adoption

    The root README uses the approved lockup export. The approved mark and lockup
    masters remain present at their canonical paths and retain their approved
    SHA-256 hashes. This checkpoint does not claim a new subjective visual review.

    ## GitHub Planning Alignment

    Live GitHub evidence showed Capability 010 Done, Capability 011 Todo, issue #18
    open and Todo, and B002 Todo. Issue #48 and its single Project item track this
    reconciliation and are In Progress. No duplicate reconciliation item exists.

    ## Current RC1 Blockers

    - Capability 011 Portable Project serialization, resume, and export.
    - Issue #18 end-to-end demonstration and release-readiness evidence.

    ## Known Limitations

    - Portable Project serialization, resume, and export are not yet implemented.
    - Complete end-to-end RC1 demonstration and release evidence remain pending.
    - This checkpoint validates repository evidence, not subjective visual quality.

    ## Readiness Conclusion

    **Engineering readiness:** the merged repository through Capability 010 is
    healthy, reproducible, synchronized, and fully validated at this checkpoint.

    **Complete RC1 readiness:** not achieved. Version 1 is not release-ready until
    Capability 011 and issue #18 are complete and validated.

    No completion percentage is asserted because the repository defines no
    reproducible percentage calculation.
''')


CHECKPOINT_TESTS = (Path(__file__).resolve().parents[1] / TEST_PATH).read_text(
    encoding="utf-8"
)


def run(command: list[str], root: Path, *, capture: bool = False) -> str:
    result = subprocess.run(
        command, cwd=root, text=True, capture_output=capture, check=False
    )
    if result.returncode:
        detail = (result.stderr or result.stdout or "command failed").strip()
        raise BootstrapError(f"{' '.join(command)}: {detail}")
    return result.stdout if capture else ""


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
    return {
        line[3:].split(" -> ")[-1].strip('"')
        for line in output.splitlines()
        if line
    }


def allowed_paths() -> set[str]:
    return {
        SCRIPT_PATH,
        CAPABILITY010_OWNER,
        RC1_OWNER,
        SCORECARD_OWNER,
        CHECKPOINT_PATH,
        TEST_PATH,
        "README.md",
        *CAPABILITY010_FILES,
        *CAPABILITY010_MANAGED,
        *RC1_MANAGED,
    }


def verify_context(root: Path) -> None:
    branch = run(["git", "branch", "--show-current"], root, capture=True).strip()
    if branch != EXPECTED_BRANCH:
        raise BootstrapError(f"Expected {EXPECTED_BRANCH}; found {branch}.")
    unexpected = changed_paths(root) - allowed_paths()
    if unexpected:
        raise BootstrapError(
            "Unexpected working-tree paths: " + ", ".join(sorted(unexpected))
        )


def managed_text(original: str, marker: str, body: str) -> str:
    start = f"<!-- {marker}_START -->"
    end = f"<!-- {marker}_END -->"
    if original.count(start) != 1 or original.count(end) != 1:
        raise BootstrapError(f"Managed marker is missing or ambiguous: {marker}")
    prefix, rest = original.split(start, 1)
    _, suffix = rest.split(end, 1)
    block = f"{start}\n\n{body.rstrip()}\n\n{end}"
    return prefix.rstrip() + "\n\n" + block + suffix


def reconcile_readme(content: str) -> str:
    replacements = {
        "[PRD v1.1](docs/product/PRD_v1.1.md)":
            "[PRD v1.3](docs/product/PRD_v1.3.md)",
        "[Product Constitution](docs/product/Constitution.md)":
            "[Product Constitution](docs/constitution/Constitution.md)",
        "[Adaptive Editorial Model](docs/product/Adaptive_Editorial_Model.md)":
            "[Adaptive Editorial Context Model](docs/architecture/Editorial_Context_Model.md)",
        "[Author Journey](docs/product/Author_Journey.md)":
            "[Author Journey](docs/constitution/Author_Journey.md)",
    }
    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new, 1)
        elif new not in content:
            raise BootstrapError(f"README reconciliation anchor missing: {old}")
    return content


def reconcile_runtime_summary(content: str) -> str:
    replacements = {
        "| Article Engine | Planned | Capability 009 |":
            "| Article Engine | Complete | Capability 009 runtime |",
        "| Publication Package | Planned | Capability 009 |":
            "| Publication Package | Complete | Capabilities 009-010 runtime |",
        "| Hero Visual System | Planned | Capability 010 |":
            "| Hero Visual System | Complete | Capability 010 runtime |",
        "| Component Collaboration | Planned | Capabilities 009-010 |":
            "| Component Collaboration | Not separately delivered | Deferred product surface |",
    }
    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new, 1)
        elif new not in content:
            raise BootstrapError(f"Scorecard summary anchor missing: {old}")
    return content


def reconcile_release_baseline(content: str) -> str:
    old = "Architecture baseline:\n\n```text\n2026.08.02v11\n```"
    new = "Architecture baseline:\n\n```text\n2026.08.02v12\n```"
    if old in content:
        return content.replace(old, new, 1)
    if new not in content:
        raise BootstrapError("Release baseline reconciliation anchor missing.")
    return content


def expected_content(root: Path) -> dict[str, str]:
    expected = dict(CAPABILITY010_FILES)
    for mapping in (CAPABILITY010_MANAGED, RC1_MANAGED):
        for relative, (marker, body) in mapping.items():
            original = expected.get(
                relative, (root / relative).read_text(encoding="utf-8")
            )
            expected[relative] = managed_text(original, marker, body)
    expected["README.md"] = reconcile_readme(
        (root / "README.md").read_text(encoding="utf-8")
    )
    expected["docs/VERSION_ONE_SCORECARD.md"] = reconcile_runtime_summary(
        expected["docs/VERSION_ONE_SCORECARD.md"]
    )
    expected["docs/product/Release_v1.0.md"] = reconcile_release_baseline(
        expected["docs/product/Release_v1.0.md"]
    )
    expected[CHECKPOINT_PATH] = CHECKPOINT
    expected[TEST_PATH] = CHECKPOINT_TESTS
    return expected


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_owner_sync(root: Path) -> None:
    marker = "RC1_CAPABILITY010_RECONCILIATION_OWNER_SYNC_START"
    for relative in (CAPABILITY010_OWNER, RC1_OWNER):
        if marker not in (root / relative).read_text(encoding="utf-8"):
            raise BootstrapError(f"Owning bootstrap is not synchronized: {relative}")
    owner = (root / SCORECARD_OWNER).read_text(encoding="utf-8")
    for row in (
        "| Article Engine | Complete | Capability 009 runtime |",
        "| Publication Package | Complete | Capabilities 009-010 runtime |",
        "| Hero Visual System | Complete | Capability 010 runtime |",
    ):
        if row not in owner:
            raise BootstrapError("Scorecard owner retains stale runtime summary.")


def validate_generated(root: Path) -> None:
    for relative, expected in expected_content(root).items():
        path = root / relative
        if not path.is_file() or path.read_text(encoding="utf-8") != expected:
            raise BootstrapError(f"Generated content differs: {relative}")
    verify_owner_sync(root)
    protected = {
        "assets/brand/logo/master/editorial-compass-mark-master.png": MARK_HASH,
        "assets/brand/logo/master/editorial-compass-lockup-master.png": LOCKUP_HASH,
        "studio/article_engine.py": ARTICLE_ENGINE_HASH,
        "studio/publication_package.py": PUBLICATION_PACKAGE_HASH,
    }
    for relative, expected in protected.items():
        if digest(root / relative) != expected:
            raise BootstrapError(f"Protected artifact changed: {relative}")


def apply(root: Path) -> None:
    script_hash = digest(root / SCRIPT_PATH)
    for relative, content in expected_content(root).items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    if digest(root / SCRIPT_PATH) != script_hash:
        raise BootstrapError("Bootstrap modified itself during apply.")


def validate_repository(root: Path) -> None:
    run([sys.executable, "-m", "compileall", "-q", "studio", "scripts", "tests"], root)
    run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], root)
    run([sys.executable, "studio.py", "validate"], root)
    run(["git", "diff", "--check"], root)


def preview(root: Path) -> None:
    print("RC1 Capability 010 documentation reconciliation preview.")
    print("No files will be changed.\n")
    print("Expected paths:")
    for relative in sorted(allowed_paths()):
        print(f"- {relative}")
    print("\nDecisions:")
    print("- Capability 010, ADR-016, and baseline v12 are delivered/current")
    print("- Capability 011 remains Next, Todo, and unstarted")
    print("- issue #18 and B002 remain unchanged")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    root = repository_root()
    verify_context(root)
    if not args.apply:
        preview(root)
        return 0
    apply(root)
    verify_context(root)
    validate_generated(root)
    validate_repository(root)
    print(SENTINEL)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BootstrapError as exc:
        print(f"RC1 reconciliation bootstrap stopped: {exc}", file=sys.stderr)
        raise SystemExit(1)
