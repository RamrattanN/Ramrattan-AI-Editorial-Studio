#!/usr/bin/env python3
"""Deterministically apply the delegated workflow-governance refinement."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


EXPECTED_BRANCH = "feature/workflow-governance-refinement"
SCRIPT_PATH = "scripts/bootstrap_workflow_governance_refinement.py"


class BootstrapError(RuntimeError):
    """Raised when deterministic refinement cannot proceed safely."""


def replace_once(content: str, old: str, new: str, *, label: str) -> str:
    """Replace one required fragment and fail on stale or ambiguous input."""
    if content.count(old) != 1:
        raise BootstrapError(f"Expected one {label} fragment, found {content.count(old)}.")
    return content.replace(old, new, 1)


def refine_helper(content: str) -> str:
    """Add approval-profile observation to the fail-closed helper."""
    content = replace_once(
        content,
        '    UNKNOWN = "unknown"\n\n\n@dataclass(frozen=True)\nclass CommandResult:',
        '''    UNKNOWN = "unknown"


class ApprovalProfile(str, Enum):
    """Explicitly authorized delivery profile for the current task."""

    START = "start"
    PUBLISH = "publish"
    COMPLETE = "complete"
    CONSERVATIVE = "conservative"


class ProfileBoundary(str, Enum):
    """Next delegated approval boundary implied by verified workflow state."""

    START = "start"
    PUBLISH = "publish"
    COMPLETE = "complete"
    STOP = "stop"


@dataclass(frozen=True)
class CommandResult:''',
        label="approval profile insertion",
    )
    content = replace_once(
        content,
        '''    command: str | None = None
    explanation: str = ""


def run''',
        '''    command: str | None = None
    explanation: str = ""
    read_only: bool = False

    @property
    def next_profile_boundary(self) -> ProfileBoundary:
        """Return the next delegated boundary without weakening blocked states."""
        if self.state in {
            DeliveryState.DEVELOP_DIRTY,
            DeliveryState.DEVELOP_BEHIND,
            DeliveryState.READY_FOR_BRANCH,
            DeliveryState.READY_FOR_WORK,
            DeliveryState.FEATURE_OUT_OF_SYNC,
            DeliveryState.READY_TO_STAGE,
        }:
            return ProfileBoundary.START
        if self.state in {
            DeliveryState.READY_TO_COMMIT,
            DeliveryState.READY_TO_PUSH,
            DeliveryState.READY_FOR_PR,
            DeliveryState.PR_DISCOVERY_UNAVAILABLE,
            DeliveryState.PR_DISCOVERY_AMBIGUOUS,
            DeliveryState.PR_CLOSED,
            DeliveryState.PR_DRAFT,
            DeliveryState.PR_READY_FOR_REVIEW,
            DeliveryState.PR_REVIEW_REQUIRED,
            DeliveryState.PR_CHANGES_REQUESTED,
            DeliveryState.PR_CHECKS_UNAVAILABLE,
            DeliveryState.PR_CHECKS_PENDING,
            DeliveryState.PR_CHECKS_FAILED,
            DeliveryState.PR_CHECKS_CANCELLED,
            DeliveryState.PR_CHECKS_TIMED_OUT,
            DeliveryState.PR_CHECKS_ACTION_REQUIRED,
            DeliveryState.PR_MERGE_CONFLICT,
            DeliveryState.PR_MERGE_BLOCKED,
            DeliveryState.PR_MERGEABILITY_UNKNOWN,
        }:
            return ProfileBoundary.PUBLISH
        if self.state in {
            DeliveryState.READY_TO_MERGE,
            DeliveryState.POST_MERGE_CLEANUP,
            DeliveryState.COMPLETE,
        }:
            return ProfileBoundary.COMPLETE
        return ProfileBoundary.STOP


def run''',
        label="recommendation profile property",
    )
    replacements = {
        "Branch deletion requires explicit Nilesh approval.":
            "Branch deletion requires Complete authorization.",
        "Marking a pull request ready requires explicit Nilesh approval.":
            "Marking a pull request ready requires Publish authorization.",
        "Merge and branch deletion require explicit Nilesh approval.":
            "Merge and branch deletion require Complete authorization.",
        "Staging requires explicit Nilesh approval and staged review.":
            "Staging requires Start authorization and exact staged-scope review.",
        "Creating a pull request requires explicit Nilesh approval.":
            "Creating a pull request requires Publish authorization.",
    }
    for old, new in replacements.items():
        if old not in content:
            raise BootstrapError(f"Missing helper authority phrase: {old}")
        content = content.replace(old, new)
    content = replace_once(
        content,
        '''                else "Do not merge until successful checks are confirmed."
            ),
        )''',
        '''                else "Do not merge until successful checks are confirmed."
            ),
            read_only=True,
        )''',
        label="read-only CI marker",
    )
    content = replace_once(
        content,
        '''def print_recommendation(recommendation: DeliveryRecommendation) -> None:
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
''',
        '''def profile_authorizes(
    approval_profile: ApprovalProfile,
    boundary: ProfileBoundary,
) -> bool:
    """Return whether a delegated profile covers the reported boundary."""
    return boundary is not ProfileBoundary.STOP and approval_profile.value == boundary.value


def print_recommendation(
    recommendation: DeliveryRecommendation,
    *,
    approval_profile: ApprovalProfile = ApprovalProfile.CONSERVATIVE,
) -> None:
    """Render one recommendation."""
    print()
    print(f"State: {recommendation.state.value}")
    print(f"Next profile boundary: {recommendation.next_profile_boundary.value}")
    print(f"Active approval profile: {approval_profile.value}")
    print()
    print(recommendation.summary)
    if recommendation.explanation:
        print()
        print(recommendation.explanation)
    if recommendation.command:
        if recommendation.read_only:
            print()
            print("Authorization: read-only observation; no separate approval required.")
        elif approval_profile is ApprovalProfile.CONSERVATIVE:
            print()
            print("Authorization: explicit approval is required for this mutation.")
        elif not profile_authorizes(
            approval_profile, recommendation.next_profile_boundary
        ):
            print()
            print("Authorization: current profile does not authorize this transition. Stop.")
        else:
            print()
            print(
                "Authorization: conditionally covered by the active profile; "
                "verify every prerequisite before execution."
            )
        print()
        print("Next command:")
        print()
        print(recommendation.command)
''',
        label="recommendation renderer",
    )
    content = replace_once(
        content,
        '    parser.add_argument("--pr-title", required=True, help="Resolved pull-request title.")\n',
        '''    parser.add_argument("--pr-title", required=True, help="Resolved pull-request title.")
    parser.add_argument(
        "--approval-profile",
        choices=[profile.value for profile in ApprovalProfile],
        default=ApprovalProfile.CONSERVATIVE.value,
        help="Explicitly authorized profile for this invocation (default: conservative).",
    )
''',
        label="profile argument",
    )
    content = replace_once(
        content,
        "        print_recommendation(recommendation)\n",
        '''        print_recommendation(
            recommendation,
            approval_profile=ApprovalProfile(args.approval_profile),
        )
''',
        label="profile rendering call",
    )
    return content


def refine_tests(content: str) -> str:
    """Add behavioral and documentation contracts for delegated profiles."""
    content = replace_once(content, "import importlib.util\n", "import importlib.util\nimport io\n", label="io import")
    content = replace_once(
        content,
        "import unittest\nfrom pathlib import Path\n",
        "import unittest\nfrom contextlib import redirect_stdout\nfrom pathlib import Path\n",
        label="redirect import",
    )
    test_block = '''class DelegatedApprovalProfileTests(unittest.TestCase):
    def render(self, result, profile):
        stream = io.StringIO()
        with redirect_stdout(stream):
            delivery.print_recommendation(result, approval_profile=profile)
        return stream.getvalue()

    def test_start_boundary_covers_exact_staging_transition(self) -> None:
        result = delivery.DeliveryRecommendation(
            state=delivery.DeliveryState.READY_TO_STAGE,
            summary="Review and stage.",
            command="git add AGENTS.md",
        )
        self.assertEqual(result.next_profile_boundary, delivery.ProfileBoundary.START)
        self.assertIn("conditionally covered", self.render(result, delivery.ApprovalProfile.START))

    def test_publish_boundary_does_not_accept_start_authorization(self) -> None:
        result = delivery.DeliveryRecommendation(
            state=delivery.DeliveryState.READY_TO_COMMIT,
            summary="Commit reviewed scope.",
            command="git commit -m test",
        )
        self.assertEqual(result.next_profile_boundary, delivery.ProfileBoundary.PUBLISH)
        self.assertIn("does not authorize this transition. Stop.", self.render(result, delivery.ApprovalProfile.START))

    def test_complete_boundary_is_distinct_from_publish(self) -> None:
        result = delivery.DeliveryRecommendation(
            state=delivery.DeliveryState.READY_TO_MERGE,
            summary="Ready.",
            command="gh pr merge 42 --merge --delete-branch",
        )
        self.assertEqual(result.next_profile_boundary, delivery.ProfileBoundary.COMPLETE)
        self.assertIn("does not authorize this transition. Stop.", self.render(result, delivery.ApprovalProfile.PUBLISH))

    def test_conservative_requires_specific_mutation_approval(self) -> None:
        result = delivery.DeliveryRecommendation(
            state=delivery.DeliveryState.READY_FOR_PR,
            summary="Create PR.",
            command="gh pr create",
        )
        self.assertIn("explicit approval is required", self.render(result, delivery.ApprovalProfile.CONSERVATIVE))

    def test_read_only_ci_monitoring_needs_no_separate_approval(self) -> None:
        result = recommendation(
            snapshot(),
            discovery(pull_request(review=delivery.ReviewState.READY_FOR_REVIEW, checks=delivery.CheckState.PENDING)),
        )
        self.assertTrue(result.read_only)
        self.assertIn("read-only observation; no separate approval required", self.render(result, delivery.ApprovalProfile.CONSERVATIVE))

    def test_unknown_state_reports_stop_boundary(self) -> None:
        result = delivery.DeliveryRecommendation(state=delivery.DeliveryState.UNKNOWN, summary="Unknown.")
        self.assertEqual(result.next_profile_boundary, delivery.ProfileBoundary.STOP)


'''
    content = replace_once(
        content,
        "class DocumentationContractTests(unittest.TestCase):\n",
        test_block + "class DocumentationContractTests(unittest.TestCase):\n",
        label="profile test block",
    )
    doc_test = '''    def test_workflow_defines_profiles_and_consolidation_contract(self) -> None:
        workflow = (ROOT / "docs/engineering/Capability_Delivery_Workflow.md").read_text(
            encoding="utf-8"
        )
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        for phrase in (
            "### Start Profile",
            "### Publish Profile",
            "### Complete Profile",
            "### Conservative Profile",
            "### Change Consolidation",
        ):
            self.assertIn(phrase, workflow)
        self.assertIn("## Delegated Approval Profiles", agents)
        self.assertIn("## Change Consolidation", agents)
        self.assertIn("Approval for one", workflow)
        self.assertIn("profile never authorizes a later profile", workflow)

    def test_role_authority_and_architecture_records_are_synchronized(self) -> None:
        governed = (
            "AGENTS.md",
            "CONTRIBUTING.md",
            "docs/engineering/Capability_Delivery_Workflow.md",
            "scripts/capability_delivery.py",
            "docs/architecture/adr/ADR-011-governance-authority.md",
            "docs/architecture/adr/ADR-012-delivery-hardening.md",
        )
        for relative in governed:
            self.assertNotIn("Nilesh", (ROOT / relative).read_text(encoding="utf-8"))
        adr = (ROOT / "docs/architecture/adr/ADR-014-delegated-delivery-governance.md").read_text(encoding="utf-8")
        baseline = (ROOT / "docs/architecture/baselines/Architecture_Baseline_2026.08.01v09.md").read_text(encoding="utf-8")
        self.assertIn("ADR-014 - Delegated Delivery Governance", adr)
        self.assertIn("2026.08.01v09", baseline)
        self.assertIn("Product Runtime Impact\\n\\nNone", baseline)

    def test_owning_delivery_bootstraps_expose_refined_templates(self) -> None:
        scripts = str(ROOT / "scripts")
        if scripts not in sys.path:
            sys.path.insert(0, scripts)
        import bootstrap_capability008a2_delivery_hardening as hardened
        import bootstrap_capability_delivery_workflow as original

        self.assertEqual(hardened.CAPABILITY_DELIVERY_HELPER, original.CAPABILITY_DELIVERY_HELPER)
        self.assertIn("class ApprovalProfile", hardened.CAPABILITY_DELIVERY_HELPER)
        self.assertIn("Delegated Approval Profiles", hardened.CAPABILITY_DELIVERY_WORKFLOW)

'''
    content = replace_once(
        content,
        '\n\nif __name__ == "__main__":\n',
        "\n\n" + doc_test + 'if __name__ == "__main__":\n',
        label="documentation profile test",
    )
    return content


def refine_workflow(content: str) -> str:
    """Return the current authoritative workflow documentation."""
    content = replace_once(
        content,
        '''### One Transition at a Time

Provide one safe next action after verifying the previous action.

Do not issue a long sequence that assumes every intermediate step
will succeed.''',
        '''### Verified Transitions Within an Authorized Profile

Provide one safe next action after verifying the previous action. A delegated
profile may authorize a conditional sequence, but every prerequisite must be
verified before the next transition.

Stop immediately when any state is unknown, unavailable, mismatched, or failed.
Do not issue or execute a sequence that assumes intermediate success.''',
        label="verified transition principle",
    )
    content = replace_once(
        content,
        '''Staging, commit, push, pull-request mutation, merge, branch deletion, issue
mutation, and Project mutation retain explicit Nilesh approval boundaries.
Recommendations must identify that boundary and must never execute the
protected command automatically.

### Finish Where We Started''',
        '''Staging, commit, push, pull-request mutation, merge, branch deletion, issue
mutation, and Project mutation require explicit role-based authority through
the applicable delegated profile or the Conservative profile. Recommendations
must identify both workflow state and the next profile boundary and must never
execute a protected command automatically.

### Change Consolidation

Before editing, inspect whether other approved pending changes affect the same
files or tightly coupled concern. Consolidate them into one coherent change set
when scope, risk profile, and delivery timing agree. Do not split work merely
to demonstrate incremental progress.

Separate changes only for materially different scope, different risk or
approval authority, safer rollback or recovery, conflicting delivery timing,
or an explicit repository constraint. Consolidation never expands authority.

## Delegated Approval Profiles

The Standard delivery profile consists of three separately authorized phases.
Authority must come from the current task or conversation. Approval for one
profile never authorizes a later profile.

### Start Profile

Start may conditionally authorize planning synchronization to `In Progress`,
branch creation or resumption, implementation, bootstrap preview and apply,
diagnosis and repair, regeneration, testing and validation, complete diff
review, and staging of the exact reviewed scope. Stop before publication unless
Publish was explicitly included.

### Publish Profile

Publish may conditionally authorize commit of the approved staged diff, commit
hash verification, push, pull-request creation or reuse, automatic read-only CI
monitoring, and marking the pull request ready for review when all required
conditions pass. Stop before merge.

### Complete Profile

Complete may conditionally authorize merge, local and remote branch cleanup,
return to clean synchronized `develop`, completion planning synchronization,
Project item `Done`, Project summary update, issue closure, and the Capability
Delivery Receipt. Stop immediately if any verification condition fails.

### Conservative Profile

Use Conservative delivery for exceptional high-risk work or when a delegated
profile was not explicitly authorized. Approval is then required at each Git or
GitHub mutation boundary.

No Git or GitHub mutation may occur outside the explicitly authorized profile.
Automatic CI monitoring is read-only and does not require separate approval.

### Finish Where We Started''',
        label="profiles and consolidation",
    )
    content = content.replace(
        '''An existing draft pull request must be reported as draft. It is never ready to
merge, even when its checks are green. Marking it ready requires explicit
Nilesh approval.''',
        '''An existing draft pull request must be reported as draft. It is never ready to
merge, even when its checks are green. Marking it ready requires Publish
authorization or explicit Conservative approval.''',
    )
    content = content.replace(
        "When every condition passes and Nilesh explicitly approves merge:",
        "When every condition passes and Complete authorization or explicit\nConservative merge approval is present:",
    )
    if "Nilesh" in content:
        raise BootstrapError("Person-specific workflow authority remains.")
    return content


def repository_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        text=True,
        capture_output=True,
        check=True,
    )
    return Path(result.stdout.strip()).resolve()


def templates() -> dict[str, str]:
    """Load refined canonical templates after the base generator is available."""
    from bootstrap_capability008a2_delivery_hardening import (
        CAPABILITY_DELIVERY_HELPER,
        CAPABILITY_DELIVERY_WORKFLOW,
        WORKFLOW_TESTS,
    )

    return {
        "scripts/capability_delivery.py": CAPABILITY_DELIVERY_HELPER,
        "docs/engineering/Capability_Delivery_Workflow.md": CAPABILITY_DELIVERY_WORKFLOW,
        "tests/test_capability_delivery_workflow.py": WORKFLOW_TESTS,
    }


def verify(root: Path) -> None:
    branch = subprocess.run(
        ["git", "branch", "--show-current"], cwd=root, text=True, capture_output=True, check=True
    ).stdout.strip()
    if branch != EXPECTED_BRANCH:
        raise BootstrapError(f"Expected {EXPECTED_BRANCH}, found {branch}.")
    allowed = set(templates()) | {
        SCRIPT_PATH,
        "AGENTS.md",
        "CONTRIBUTING.md",
        "scripts/bootstrap_capability008a1_governance_consolidation.py",
        "scripts/bootstrap_capability008a2_delivery_hardening.py",
        "scripts/bootstrap_capability_delivery_workflow.py",
        "tests/test_capability008a1_governance.py",
        "docs/architecture/adr/ADR-011-governance-authority.md",
        "docs/architecture/adr/ADR-012-delivery-hardening.md",
        "docs/architecture/adr/ADR-014-delegated-delivery-governance.md",
        "docs/architecture/adr/README.md",
        "docs/architecture/baselines/Architecture_Baseline_2026.08.01v09.md",
    }
    status = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=root, text=True, capture_output=True, check=True
    ).stdout.splitlines()
    unexpected = [line for line in status if line[3:].strip() not in allowed]
    if unexpected:
        raise BootstrapError("Unexpected working-tree changes:\n" + "\n".join(unexpected))


def apply(root: Path) -> None:
    for relative, content in templates().items():
        path = root / relative
        path.write_text(content, encoding="utf-8")
        print(f"Wrote {relative}")


def validate(root: Path) -> None:
    for relative, expected in templates().items():
        if (root / relative).read_text(encoding="utf-8") != expected:
            raise BootstrapError(f"Generated artifact differs: {relative}")
    subprocess.run([sys.executable, "-m", "compileall", "-q", "studio", "scripts", "tests"], cwd=root, check=True)
    subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=root, check=True)
    subprocess.run([sys.executable, "studio.py", "validate"], cwd=root, check=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        root = repository_root()
        verify(root)
        print("Workflow-governance refinement:")
        for relative in templates():
            print(f"  - {relative}")
        if args.apply:
            apply(root)
            validate(root)
        else:
            print("Preview mode changes nothing.")
        return 0
    except (BootstrapError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
