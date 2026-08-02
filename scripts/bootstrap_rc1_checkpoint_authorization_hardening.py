#!/usr/bin/env python3
"""Bootstrap the RC1 checkpoint and delegated authorization hardening.

Preview is non-mutating. Apply updates only the declared governance,
delivery, checkpoint, generator, and current-status paths, then runs the
complete repository validation suite.
"""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
import textwrap
from pathlib import Path


EXPECTED_REPOSITORY = "Ramrattan-AI-Editorial-Studio"
EXPECTED_BRANCH = "feature/rc1-checkpoint-authorization-hardening"
SCRIPT_PATH = "scripts/bootstrap_rc1_checkpoint_authorization_hardening.py"
SENTINEL = "RC1_CHECKPOINT_AUTHORIZATION_HARDENING_COMPLETE"

MARK_HASH = "b2cd1c22239b7176b43578892b0c37ac502ca5ab696b7c083a0b397bfe285727"
LOCKUP_HASH = "ae56f16f3e4b3a2bfbf5cefbf6ee807482cd8814e30b7496a917b9eae3a5ba72"
ARTICLE_ENGINE_HASH = "653db77e8881aa6532906fa1b17a8c771152cfe14ef1266383daba423d596868"
PUBLICATION_PACKAGE_HASH = "ba3e4bf6e0d92ff088279e8a6a8bf5e74b33845ca8056bd82cf4e1c1eb136500"


class BootstrapError(RuntimeError):
    """Raised when safe deterministic application cannot continue."""


def clean(value: str) -> str:
    return textwrap.dedent(value).strip() + "\n"


def replace_once(content: str, old: str, new: str, *, label: str) -> str:
    """Apply one idempotent exact replacement."""
    if new in content:
        return content
    if content.count(old) != 1:
        raise BootstrapError(f"Expected one {label}; found {content.count(old)}.")
    return content.replace(old, new, 1)


def replace_section(content: str, start: str, end: str, new: str, *, label: str) -> str:
    """Replace one section bounded by stable definitions."""
    if new in content:
        return content
    if content.count(start) != 1 or content.count(end) != 1:
        raise BootstrapError(f"Cannot locate unique {label} boundaries.")
    prefix, rest = content.split(start, 1)
    _, suffix = rest.split(end, 1)
    return prefix + new + end + suffix


def harden_helper(content: str) -> str:
    """Add invocation-scoped authorization outcomes to the canonical helper."""
    content = replace_once(
        content,
        '    REMOTE_VERIFICATION_FAILED = "remote_verification_failed"\n',
        '    SCOPE_CONFLICT = "scope_conflict"\n'
        '    REMOTE_VERIFICATION_FAILED = "remote_verification_failed"\n',
        label="scope-conflict delivery state",
    )
    content = replace_once(
        content,
        '''class ProfileBoundary(str, Enum):
    """Next delegated approval boundary implied by verified workflow state."""

    START = "start"
    PUBLISH = "publish"
    COMPLETE = "complete"
    STOP = "stop"
''',
        '''class ProfileBoundary(str, Enum):
    """Next delegated approval boundary implied by verified workflow state."""

    START = "start"
    PUBLISH = "publish"
    COMPLETE = "complete"
    STOP = "stop"


class AuthorizationStatus(str, Enum):
    """Invocation-scoped authorization outcome for the observed action."""

    ALREADY_SATISFIED = "authorization already satisfied"
    NEW_PROFILE_REQUIRED = "new profile authorization required"
    CONSERVATIVE_APPROVAL_REQUIRED = "conservative mutation approval required"
    BLOCKED_FAIL_CLOSED = "blocked by fail-closed condition"
''',
        label="authorization status enum",
    )
    content = replace_once(
        content,
        '''    explanation: str = ""
    read_only: bool = False

    @property
    def next_profile_boundary(self) -> ProfileBoundary:
''',
        '''    explanation: str = ""
    read_only: bool = False
    blocked_by_fail_closed: bool = False

    def authorization_status(
        self,
        approval_profile: ApprovalProfile,
    ) -> AuthorizationStatus:
        """Classify current-task authority without persisting conversation state."""
        if self.blocked_by_fail_closed:
            return AuthorizationStatus.BLOCKED_FAIL_CLOSED
        if self.read_only:
            return AuthorizationStatus.ALREADY_SATISFIED
        if approval_profile is ApprovalProfile.CONSERVATIVE:
            if self.command:
                return AuthorizationStatus.CONSERVATIVE_APPROVAL_REQUIRED
            return AuthorizationStatus.ALREADY_SATISFIED
        if profile_authorizes(approval_profile, self.next_profile_boundary):
            return AuthorizationStatus.ALREADY_SATISFIED
        return AuthorizationStatus.NEW_PROFILE_REQUIRED

    @property
    def next_profile_boundary(self) -> ProfileBoundary:
''',
        label="authorization status classifier",
    )
    content = replace_once(
        content,
        '''def blocked(state: DeliveryState, summary: str, explanation: str = "") -> DeliveryRecommendation:
    """Create a recommendation with no mutating command."""
    return DeliveryRecommendation(state=state, summary=summary, explanation=explanation)
''',
        '''def blocked(state: DeliveryState, summary: str, explanation: str = "") -> DeliveryRecommendation:
    """Create a fail-closed recommendation with no mutating command."""
    return DeliveryRecommendation(
        state=state,
        summary=summary,
        explanation=explanation,
        blocked_by_fail_closed=True,
    )
''',
        label="fail-closed recommendation factory",
    )
    content = replace_once(
        content,
        '''    return blocked(
        DeliveryState.COMPLETE,
        f"Pull request #{pr.number} is merged and repository cleanup is complete.",
    )
''',
        '''    return DeliveryRecommendation(
        state=DeliveryState.COMPLETE,
        summary=f"Pull request #{pr.number} is merged and repository cleanup is complete.",
    )
''',
        label="complete status report",
    )
    content = replace_once(
        content,
        '''        return blocked(
            DeliveryState.READY_FOR_WORK,
            "The feature branch is ready for capability implementation.",
        )
''',
        '''        return DeliveryRecommendation(
            state=DeliveryState.READY_FOR_WORK,
            summary="The feature branch is ready for capability implementation.",
        )
''',
        label="ready-for-work status report",
    )
    content = replace_once(
        content,
        '''            read_only=True,
        )

    if pr.mergeability is MergeabilityState.CONFLICTING:
''',
        '''            read_only=True,
            blocked_by_fail_closed=True,
        )

    if pr.mergeability is MergeabilityState.CONFLICTING:
''',
        label="CI fail-closed marker",
    )
    content = replace_once(
        content,
        '''def recommend(*, feature_branch: str, commit_message: str, pr_title: str) -> DeliveryRecommendation:
    """Return the next safe capability-delivery action."""
    repo = snapshot(feature_branch=feature_branch)
''',
        '''def recommend(
    *,
    feature_branch: str,
    commit_message: str,
    pr_title: str,
    scope_conflict: str = "",
) -> DeliveryRecommendation:
    """Return the next safe capability-delivery action."""
    if scope_conflict.strip():
        return blocked(
            DeliveryState.SCOPE_CONFLICT,
            "Product or capability scope requires a human decision.",
            scope_conflict.strip(),
        )
    repo = snapshot(feature_branch=feature_branch)
''',
        label="scope conflict input",
    )
    renderer = '''def print_recommendation(
    recommendation: DeliveryRecommendation,
    *,
    approval_profile: ApprovalProfile = ApprovalProfile.CONSERVATIVE,
) -> None:
    """Render workflow and invocation-scoped authorization evidence."""
    authorization = recommendation.authorization_status(approval_profile)
    already_satisfied = authorization is AuthorizationStatus.ALREADY_SATISFIED
    new_profile_required = authorization is AuthorizationStatus.NEW_PROFILE_REQUIRED
    fail_closed = authorization is AuthorizationStatus.BLOCKED_FAIL_CLOSED

    print()
    print(f"State: {recommendation.state.value}")
    print(f"Next profile boundary: {recommendation.next_profile_boundary.value}")
    print(f"Active approval profile: {approval_profile.value}")
    print(f"Authorization status: {authorization.value}")
    print(f"Current action covered: {'yes' if already_satisfied else 'no'}")
    print(f"New profile authorization required: {'yes' if new_profile_required else 'no'}")
    print(f"Fail-closed blocked: {'yes' if fail_closed else 'no'}")
    print()
    print(recommendation.summary)
    if recommendation.explanation:
        print()
        print(recommendation.explanation)
    if recommendation.command:
        print()
        if fail_closed:
            print(
                "Execution: blocked by fail-closed condition; only the displayed "
                "read-only diagnostic may run."
            )
        elif authorization is AuthorizationStatus.ALREADY_SATISFIED:
            print(
                "Authorization: authorization already satisfied by the active "
                "current-task profile; verify prerequisites and continue."
            )
        elif authorization is AuthorizationStatus.NEW_PROFILE_REQUIRED:
            print("Authorization: new profile authorization required. Stop.")
        else:
            print(
                "Authorization: Conservative mode requires explicit approval for "
                "this mutation."
            )
        print()
        print("Next command:")
        print()
        print(recommendation.command)


'''
    content = replace_section(
        content,
        "def print_recommendation(\n",
        "def parse_args() -> argparse.Namespace:\n",
        renderer,
        label="recommendation renderer",
    )
    content = replace_once(
        content,
        '''def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
''',
        '''def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse invocation-scoped arguments; authorization is never persisted."""
''',
        label="invocation-scoped argument parser",
    )
    content = replace_once(
        content,
        '''    parser.add_argument(
        "--approval-profile",
''',
        '''    parser.add_argument(
        "--scope-conflict",
        default="",
        help="Current-task scope conflict that must fail closed.",
    )
    parser.add_argument(
        "--approval-profile",
''',
        label="scope conflict CLI option",
    )
    content = replace_once(
        content,
        "    return parser.parse_args()\n",
        "    return parser.parse_args(argv)\n",
        label="argument parse invocation",
    )
    content = replace_once(
        content,
        '''            pr_title=args.pr_title,
        )
''',
        '''            pr_title=args.pr_title,
            scope_conflict=args.scope_conflict,
        )
''',
        label="scope conflict recommendation input",
    )
    return content


AUTHORIZATION_WORKFLOW = clean('''
## Authorization Continuity Within a Profile

An explicitly authorized Start, Publish, or Complete profile remains satisfied
through every documented transition in that same phase. The Implementation
Agent must not request that profile again merely because it reports status,
reruns the helper, or advances to another state inside the authorized phase.

Authorization ends when the profile reaches its stopping boundary, a genuine
fail-closed condition occurs, verified prerequisites materially change, scope
materially changes, authority is revoked or changed, or the current task or
conversation no longer supplies the authorization context. A later profile
always requires new explicit authorization.

The helper receives the active profile per invocation. It never stores approval
as permanent repository authority and never infers it from prior sessions,
historical commits, earlier capabilities, or old chats.

Helper output distinguishes:

- `authorization already satisfied` for an action or status inside the active
  current-task profile;
- `new profile authorization required` at a later profile boundary; and
- `blocked by fail-closed condition` when state is unsafe, unavailable,
  ambiguous, mismatched, pending, failed, or otherwise blocking.

A status report is not an approval request. A transition inside an already
authorized profile is not a new approval boundary. Conservative delivery
remains available and requires explicit approval for each protected mutation.
''')


def harden_workflow(content: str) -> str:
    return upsert_text(content, "RC1_AUTHORIZATION_CONTINUITY", AUTHORIZATION_WORKFLOW)


def reconcile_release_baseline(content: str) -> str:
    """Reconcile the current Release Identity without rewriting history."""
    return replace_once(
        content,
        "Architecture baseline:\n\n```text\n2026.08.01v06\n```",
        "Architecture baseline:\n\n```text\n2026.08.02v10\n```",
        label="current Release Identity architecture baseline",
    )


def harden_tests(content: str) -> str:
    """Replace superseded prose assertions with authorization semantics."""
    replacements = (
        (
            'self.assertIn("conditionally covered", self.render(result, delivery.ApprovalProfile.START))',
            'self.assertEqual(\n'
            '            result.authorization_status(delivery.ApprovalProfile.START),\n'
            '            delivery.AuthorizationStatus.ALREADY_SATISFIED,\n'
            '        )',
            "Start authorization assertion",
        ),
        (
            'self.assertIn("does not authorize this transition. Stop.", self.render(result, delivery.ApprovalProfile.START))',
            'self.assertEqual(\n'
            '            result.authorization_status(delivery.ApprovalProfile.START),\n'
            '            delivery.AuthorizationStatus.NEW_PROFILE_REQUIRED,\n'
            '        )',
            "Publish boundary assertion",
        ),
        (
            'self.assertIn("does not authorize this transition. Stop.", self.render(result, delivery.ApprovalProfile.PUBLISH))',
            'self.assertEqual(\n'
            '            result.authorization_status(delivery.ApprovalProfile.PUBLISH),\n'
            '            delivery.AuthorizationStatus.NEW_PROFILE_REQUIRED,\n'
            '        )',
            "Complete boundary assertion",
        ),
        (
            'self.assertIn("explicit approval is required", self.render(result, delivery.ApprovalProfile.CONSERVATIVE))',
            'self.assertEqual(\n'
            '            result.authorization_status(delivery.ApprovalProfile.CONSERVATIVE),\n'
            '            delivery.AuthorizationStatus.CONSERVATIVE_APPROVAL_REQUIRED,\n'
            '        )',
            "Conservative assertion",
        ),
        (
            'self.assertIn("read-only observation; no separate approval required", self.render(result, delivery.ApprovalProfile.CONSERVATIVE))',
            'self.assertEqual(\n'
            '            result.authorization_status(delivery.ApprovalProfile.CONSERVATIVE),\n'
            '            delivery.AuthorizationStatus.BLOCKED_FAIL_CLOSED,\n'
            '        )\n'
            '        self.assertIn("read-only diagnostic may run", self.render(result, delivery.ApprovalProfile.CONSERVATIVE))',
            "read-only pending-CI assertion",
        ),
    )
    for old, new, label in replacements:
        content = replace_once(content, old, new, label=label)
    return content


CHECKPOINT = clean('''
# RC1 Checkpoint - 2026.08.02

## Checkpoint Basis

- Verified commit: `b2ffc31b6f7fc366d8e8c3b181a4df93ad0a26bc`
- Checkpoint date: 2026-08-02
- Current delivered architecture baseline: `2026.08.02v10`
- Tests at checkpoint: 256 passed

## Repository Health

At checkpoint start, `develop` was active, the working tree was clean, local
`develop` matched `origin/develop` with zero divergence, compileall passed, all
256 tests passed, repository validation passed for `v3.0.0-rc1`, and
`git diff --check` passed.

## Product and Roadmap State

Capabilities 001-009, the Capability 008A Engineering Hardening Program, and
Initiative B001 are complete. Capability 010 is next, Todo, and unstarted.
Capability 011 is Todo and unstarted. B002 remains Todo, Low Priority,
Post-RC1, and non-blocking.

Version 1 is not release-ready. Current blockers are the Capability 010 Hero
Visual System, Capability 011 Portable Project resume/export work, and the
Version 1 end-to-end demonstration and release-readiness evidence tracked by
issue #18.

## Architecture Integrity

ADR-015 is indexed and agrees with the delivered Capability 009 scope: Article
Engine and textual Publication Package only. Baseline v10 is the sole current
delivered baseline at this checkpoint. Broader workspace, Adaptive Context,
collaboration, orchestration, Hero Visual generation, and Portable Project
runtime remain deferred.

## Brand Adoption

The root README references
`assets/brand/logo/exports/editorial-compass-lockup-1200.png`, and that path
exists. Both Repository Author-supplied raster masters exist and match their
approved hashes. No rejected, candidate, review, preview, SVG-source, or
superseded artwork is present in the operational brand tree.

This checkpoint validates paths, inventory, dimensions, and hashes. It does
not claim a new subjective visual review.

## GitHub Planning Alignment

Live GitHub evidence showed Capability 009 and B001 Done; Capability 010,
Capability 011, and B002 Todo; and no duplicate issue or Project item for this
checkpoint increment. Issue #44 and its one Project item are In Progress.

## Known Limitations

- A rendered 720 x 425 Hero Visual is not yet implemented.
- Portable Project serialization, resume, and export are not yet implemented.
- Complete end-to-end RC1 demonstration and release evidence remain pending.
- This checkpoint does not perform subjective brand rendering review.

## Readiness Conclusion

**Engineering readiness:** the merged repository through Capability 009 is
healthy, reproducible, synchronized, and fully validated at this checkpoint.

**Complete RC1 readiness:** not achieved. RC1 remains blocked until the stated
Capability 010, Capability 011, and end-to-end release-readiness evidence are
complete and validated.

No completion percentage is asserted because the repository defines no
reproducible percentage calculation.
''')


BASELINE_V11 = clean('''
# Architecture Baseline - 2026.08.02v11

## Status

Proposed during RC1 Checkpoint and Delegated Authorization Hardening. Becomes
current only when this increment is delivered.

## Baseline ID

`2026.08.02v11`

## Supersedes

`2026.08.02v10`

## Reason for Revision

Extend the executable Capability Delivery helper with invocation-scoped
authorization outcomes that prevent duplicate profile requests without
weakening fail-closed delivery behavior.

## Engineering Architecture

The existing `scripts/capability_delivery.py` remains the sole delivery state
observer and recommender. It reports workflow state, next profile boundary,
active profile, authorization outcome, action coverage, new-profile need, and
fail-closed blocking independently.

Start, Publish, and Complete authorization is supplied per current-task helper
invocation and remains valid only through that profile. No approval is stored
as durable repository state. Conservative per-mutation approval remains
available.

## Product Runtime Impact

None. Article Engine, Publication Package, editorial runtime, Hero Visual,
Portable Project, and approved brand behavior are unchanged.

## Governance Decision

ADR-014, as amended by this increment, owns delegated authorization continuity.
''')


AUTH_TESTS = clean(r'''
from __future__ import annotations

import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = str(ROOT / "scripts")
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

import capability_delivery as delivery


class DelegatedAuthorizationContinuityTests(unittest.TestCase):
    def render(self, result, profile):
        stream = io.StringIO()
        with redirect_stdout(stream):
            delivery.print_recommendation(result, approval_profile=profile)
        return stream.getvalue()

    def recommendation(self, state, *, command="command", blocked=False, read_only=False):
        return delivery.DeliveryRecommendation(
            state=state,
            summary="state",
            command=command,
            blocked_by_fail_closed=blocked,
            read_only=read_only,
        )

    def test_start_is_not_requested_again_during_internal_start_state(self):
        result = self.recommendation(delivery.DeliveryState.READY_TO_STAGE)
        self.assertEqual(result.authorization_status(delivery.ApprovalProfile.START), delivery.AuthorizationStatus.ALREADY_SATISFIED)

    def test_start_status_report_is_not_an_approval_request(self):
        result = self.recommendation(delivery.DeliveryState.READY_FOR_WORK, command=None)
        output = self.render(result, delivery.ApprovalProfile.START)
        self.assertIn("authorization already satisfied", output)
        self.assertIn("New profile authorization required: no", output)

    def test_publish_is_not_requested_again_after_supply(self):
        result = self.recommendation(delivery.DeliveryState.READY_TO_COMMIT)
        self.assertEqual(result.authorization_status(delivery.ApprovalProfile.PUBLISH), delivery.AuthorizationStatus.ALREADY_SATISFIED)

    def test_capability009_duplicate_publish_request_is_prevented(self):
        result = self.recommendation(delivery.DeliveryState.READY_TO_COMMIT, command="git commit -m capability009")
        output = self.render(result, delivery.ApprovalProfile.PUBLISH)
        self.assertIn("authorization already satisfied", output)
        self.assertNotIn("new profile authorization required. Stop", output)

    def test_complete_is_not_requested_again_during_cleanup(self):
        for state in (delivery.DeliveryState.READY_TO_MERGE, delivery.DeliveryState.POST_MERGE_CLEANUP, delivery.DeliveryState.COMPLETE):
            with self.subTest(state=state):
                result = self.recommendation(state, command=None if state is delivery.DeliveryState.COMPLETE else "cleanup")
                self.assertEqual(result.authorization_status(delivery.ApprovalProfile.COMPLETE), delivery.AuthorizationStatus.ALREADY_SATISFIED)

    def test_new_profile_still_requires_authorization(self):
        result = self.recommendation(delivery.DeliveryState.READY_TO_COMMIT)
        self.assertEqual(result.authorization_status(delivery.ApprovalProfile.START), delivery.AuthorizationStatus.NEW_PROFILE_REQUIRED)

    def test_scope_conflict_blocks(self):
        result = delivery.blocked(delivery.DeliveryState.SCOPE_CONFLICT, "conflict")
        self.assertEqual(result.authorization_status(delivery.ApprovalProfile.START), delivery.AuthorizationStatus.BLOCKED_FAIL_CLOSED)

    def test_dirty_tree_mismatch_blocks(self):
        result = delivery.blocked(delivery.DeliveryState.DEVELOP_DIRTY, "dirty")
        self.assertEqual(result.authorization_status(delivery.ApprovalProfile.START), delivery.AuthorizationStatus.BLOCKED_FAIL_CLOSED)

    def test_remote_or_github_unavailability_blocks(self):
        for state in (delivery.DeliveryState.REMOTE_VERIFICATION_FAILED, delivery.DeliveryState.PR_DISCOVERY_UNAVAILABLE):
            with self.subTest(state=state):
                self.assertEqual(delivery.blocked(state, "unavailable").authorization_status(delivery.ApprovalProfile.PUBLISH), delivery.AuthorizationStatus.BLOCKED_FAIL_CLOSED)

    def test_commit_and_pr_head_mismatch_block(self):
        for state in (delivery.DeliveryState.FEATURE_OUT_OF_SYNC, delivery.DeliveryState.REMOTE_VERIFICATION_FAILED):
            with self.subTest(state=state):
                self.assertEqual(delivery.blocked(state, "mismatch").authorization_status(delivery.ApprovalProfile.PUBLISH), delivery.AuthorizationStatus.BLOCKED_FAIL_CLOSED)

    def test_ci_failure_or_unavailability_blocks(self):
        for state in (delivery.DeliveryState.PR_CHECKS_FAILED, delivery.DeliveryState.PR_CHECKS_UNAVAILABLE):
            with self.subTest(state=state):
                result = self.recommendation(state, blocked=True, read_only=True)
                self.assertEqual(result.authorization_status(delivery.ApprovalProfile.PUBLISH), delivery.AuthorizationStatus.BLOCKED_FAIL_CLOSED)

    def test_prior_invocation_authorization_is_not_persisted(self):
        publish = delivery.parse_args(["--branch", "b", "--commit-message", "c", "--pr-title", "p", "--approval-profile", "publish"])
        later = delivery.parse_args(["--branch", "b", "--commit-message", "c", "--pr-title", "p"])
        self.assertEqual(publish.approval_profile, "publish")
        self.assertEqual(later.approval_profile, "conservative")

    def test_conservative_mode_retains_per_mutation_approval(self):
        result = self.recommendation(delivery.DeliveryState.READY_TO_COMMIT)
        self.assertEqual(result.authorization_status(delivery.ApprovalProfile.CONSERVATIVE), delivery.AuthorizationStatus.CONSERVATIVE_APPROVAL_REQUIRED)

    def test_helper_distinguishes_all_authorization_outcomes(self):
        outcomes = {
            self.recommendation(delivery.DeliveryState.READY_TO_STAGE).authorization_status(delivery.ApprovalProfile.START),
            self.recommendation(delivery.DeliveryState.READY_TO_COMMIT).authorization_status(delivery.ApprovalProfile.START),
            self.recommendation(delivery.DeliveryState.PR_CHECKS_FAILED, blocked=True).authorization_status(delivery.ApprovalProfile.PUBLISH),
        }
        self.assertEqual(outcomes, {delivery.AuthorizationStatus.ALREADY_SATISFIED, delivery.AuthorizationStatus.NEW_PROFILE_REQUIRED, delivery.AuthorizationStatus.BLOCKED_FAIL_CLOSED})

    def test_owning_bootstraps_match_live_delivery_artifacts(self):
        import bootstrap_capability008a2_delivery_hardening as hardened
        import bootstrap_capability_delivery_workflow as original

        live_helper = (ROOT / "scripts/capability_delivery.py").read_text(encoding="utf-8")
        live_workflow = (ROOT / "docs/engineering/Capability_Delivery_Workflow.md").read_text(encoding="utf-8")
        live_tests = (ROOT / "tests/test_capability_delivery_workflow.py").read_text(encoding="utf-8")
        for owner in (original, hardened):
            self.assertEqual(owner.CAPABILITY_DELIVERY_HELPER, live_helper)
            self.assertEqual(owner.CAPABILITY_DELIVERY_WORKFLOW, live_workflow)
            self.assertEqual(owner.WORKFLOW_TESTS, live_tests)


if __name__ == "__main__":
    unittest.main()
''')


CHECKPOINT_TESTS = clean(r'''
from __future__ import annotations

import hashlib
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RC1CheckpointTests(unittest.TestCase):
    def text(self, relative):
        return (ROOT / relative).read_text(encoding="utf-8")

    def digest(self, relative):
        return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()

    def test_checkpoint_records_reproducible_evidence_and_blockers(self):
        checkpoint = self.text("docs/product/checkpoints/RC1_Checkpoint_2026.08.02.md")
        for phrase in ("b2ffc31b6f7fc366d8e8c3b181a4df93ad0a26bc", "2026.08.02v10", "256 passed", "Engineering readiness", "Complete RC1 readiness", "not achieved", "Capability 010", "Capability 011", "issue #18"):
            self.assertIn(phrase, checkpoint)
        self.assertNotRegex(checkpoint, r"\b\d{1,3}%")

    def test_brand_adoption_is_path_and_hash_verified(self):
        readme = self.text("README.md")
        match = re.search(r'<img src="([^"]+)"', readme)
        self.assertIsNotNone(match)
        self.assertTrue((ROOT / match.group(1)).is_file())
        self.assertEqual(self.digest("assets/brand/logo/master/editorial-compass-mark-master.png"), "b2cd1c22239b7176b43578892b0c37ac502ca5ab696b7c083a0b397bfe285727")
        self.assertEqual(self.digest("assets/brand/logo/master/editorial-compass-lockup-master.png"), "ae56f16f3e4b3a2bfbf5cefbf6ee807482cd8814e30b7496a917b9eae3a5ba72")
        self.assertFalse((ROOT / "assets/brand/review").exists())
        self.assertFalse((ROOT / "assets/brand/logo/source").exists())

    def test_editorial_runtime_is_unchanged(self):
        self.assertEqual(self.digest("studio/article_engine.py"), "653db77e8881aa6532906fa1b17a8c771152cfe14ef1266383daba423d596868")
        self.assertEqual(self.digest("studio/publication_package.py"), "ba3e4bf6e0d92ff088279e8a6a8bf5e74b33845ca8056bd82cf4e1c1eb136500")

    def test_current_status_records_are_reconciled(self):
        for relative in ("ROADMAP.md", "docs/VERSION_ONE_SCORECARD.md", "docs/product/Current_Product_Focus.md", "docs/product/Release_v1.0.md"):
            content = self.text(relative)
            self.assertIn("RC1_CHECKPOINT_CURRENT_STATUS", content)
            self.assertIn("Capability 009", content)
            self.assertIn("Complete", content)
            self.assertIn("Capability 010", content)
            self.assertIn("unstarted", content)
            self.assertIn("2026.08.02v10", content)
        release = self.text("docs/product/Release_v1.0.md")
        self.assertIn("Architecture baseline:\n\n```text\n2026.08.02v10\n```", release)

    def test_adr015_is_indexed_and_baseline_v11_is_proposed(self):
        self.assertIn("ADR-015", self.text("docs/architecture/adr/README.md"))
        baseline = self.text("docs/architecture/baselines/Architecture_Baseline_2026.08.02v11.md")
        self.assertIn("Proposed", baseline)
        self.assertIn("2026.08.02v10", baseline)

    def test_direct_adr_and_baseline_markdown_links_resolve(self):
        for directory in (ROOT / "docs/architecture/adr", ROOT / "docs/architecture/baselines"):
            for path in directory.glob("*.md"):
                for target in re.findall(r"\[[^]]+\]\(([^)#]+\.md)\)", path.read_text(encoding="utf-8")):
                    self.assertTrue((path.parent / target).resolve().is_file(), f"Broken link: {path} -> {target}")


if __name__ == "__main__":
    unittest.main()
''')


MANAGED = {
    "AGENTS.md": ("RC1_AUTHORIZATION_CONTINUITY", clean('''
## Authorization Continuity

Once Start, Publish, or Complete is explicitly authorized in the current task
or conversation, the Implementation Agent must not request that same profile
again during its documented phase. Status reporting and internal state
transitions do not create new approval boundaries.

Authorization remains conditional on unchanged scope, targets, prerequisites,
and current-task authority. It ends at the profile stopping boundary or when a
genuine fail-closed condition, material mismatch, material scope change,
revocation, or loss of current conversational authorization occurs. A later
profile still requires explicit authorization. Never persist or infer approval
from earlier tasks, sessions, chats, commits, or capabilities.
''')),
    "CONTRIBUTING.md": ("RC1_AUTHORIZATION_CONTINUITY", clean('''
## Authorization Continuity

Within the current task, an authorized delegated profile covers every verified
transition assigned to that phase. Do not request the same profile again after
a status report or internal state transition. Stop at the next profile boundary
or on a genuine fail-closed condition. Authorization is invocation-scoped and
must not be inferred from prior sessions or repository history.
''')),
    "docs/architecture/adr/ADR-014-delegated-delivery-governance.md": ("RC1_AUTHORIZATION_CONTINUITY", clean('''
## Authorization Continuity Amendment

An explicitly authorized Standard profile remains valid through all verified
states assigned to that phase. Repeated status reporting and helper invocations
inside the phase do not require duplicate authorization. The helper now reports
authorization already satisfied, new profile authorization required, or blocked
by fail-closed condition as distinct outcomes.

Authorization remains current-task context only. It expires at the profile
boundary or on material mismatch, scope change, revocation, fail-closed state,
or loss of current conversational authority. It is never persisted or inferred
from repository history. Conservative per-mutation approval remains unchanged.

Architecture Baseline `2026.08.02v11` records the executable helper change when
this increment is delivered.
''')),
    "ROADMAP.md": ("RC1_CHECKPOINT_CURRENT_STATUS", clean('''
## RC1 Checkpoint - Current Status

- Capability 009 - Complete
- Initiative B001 - Complete
- RC1 Checkpoint and Delegated Authorization Hardening - In Progress
- Capability 010 - Next, Todo, and unstarted
- Capability 011 - Todo and unstarted
- B002 - Todo, Low Priority, Post-RC1, and non-blocking
- Current delivered architecture baseline - `2026.08.02v10`

Version 1 is not release-ready. Capability 010, Capability 011, and the
end-to-end release-readiness evidence remain outstanding. Earlier capability
status sections are historical delivery records; this section is authoritative
for the current checkpoint increment.
''')),
    "docs/VERSION_ONE_SCORECARD.md": ("RC1_CHECKPOINT_CURRENT_STATUS", clean('''
## RC1 Checkpoint - Current Status

| Area | Status | Evidence |
|---|---|---|
| Capability 009 | Complete | PR #43 and ADR-015 |
| Initiative B001 | Complete | PR #42 and approved master hashes |
| Capability 010 | Todo and unstarted | Issue #16 |
| Capability 011 | Todo and unstarted | Issue #17 |
| B002 | Todo, Low Priority, Post-RC1, non-blocking | Issue #41 |
| Current delivered baseline | Complete | `2026.08.02v10` |
| Complete RC1 readiness | Blocked | Capabilities 010, 011, and issue #18 |

The Article Engine and textual Publication Package are delivered. Version 1 is
not release-ready until the remaining Hero Visual, Portable Project, and
end-to-end evidence is complete.
''')),
    "docs/product/Current_Product_Focus.md": ("RC1_CHECKPOINT_CURRENT_STATUS", clean('''
## RC1 Checkpoint - Current Product Status

Capability 009 is complete. The Article Engine and textual Publication Package
are delivered under ADR-015 and baseline `2026.08.02v10`.

Capability 010 is next, Todo, and unstarted. Capability 011 is Todo and
unstarted. B002 remains deferred, Low Priority, Post-RC1, and non-blocking.
Version 1 is not release-ready until the remaining Hero Visual, Portable
Project, and end-to-end release-readiness work is complete.
''')),
    "docs/product/Release_v1.0.md": ("RC1_CHECKPOINT_CURRENT_STATUS", clean('''
## RC1 Checkpoint - Current Release Status

- Capability 009 - Complete
- Capability 010 - Next, Todo, and unstarted
- Capability 011 - Todo and unstarted
- B001 - Complete
- B002 - Todo, Low Priority, Post-RC1, and non-blocking
- Current delivered architecture baseline - `2026.08.02v10`

Version 1 is not release-ready. The 720 x 425 Hero Visual, Portable Editorial
Project resume/export path, and end-to-end release-readiness evidence remain
outstanding.
''')),
    "docs/START_HERE.md": ("RC1_CHECKPOINT_DISCOVERY", clean('''
## RC1 Checkpoint

The current evidence-based engineering and release checkpoint is:

- `product/checkpoints/RC1_Checkpoint_2026.08.02.md`

It distinguishes validated engineering readiness from complete RC1 readiness.
''')),
}


NEW_FILES = {
    "docs/product/checkpoints/RC1_Checkpoint_2026.08.02.md": CHECKPOINT,
    "docs/architecture/baselines/Architecture_Baseline_2026.08.02v11.md": BASELINE_V11,
    "tests/test_rc1_delegated_authorization.py": AUTH_TESTS,
    "tests/test_rc1_checkpoint.py": CHECKPOINT_TESTS,
}


OWNER_IMPORT = clean('''
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
''')


OWNER_FILES = (
    "scripts/bootstrap_capability_delivery_workflow.py",
    "scripts/bootstrap_capability008a2_delivery_hardening.py",
)


def upsert_text(content: str, marker: str, body: str) -> str:
    start = f"<!-- {marker}_START -->"
    end = f"<!-- {marker}_END -->"
    block = f"{start}\n\n{body.rstrip()}\n\n{end}"
    if start in content and end in content:
        prefix, rest = content.split(start, 1)
        _, suffix = rest.split(end, 1)
        return prefix.rstrip() + "\n\n" + block + suffix
    return content.rstrip() + "\n\n" + block + "\n"


def harden_owner(content: str) -> str:
    marker = "# RC1_CHECKPOINT_AUTHORIZATION_HARDENING_OWNER_SYNC_START"
    if marker in content:
        start = content.index(marker)
        prefix = content[:start]
        if not prefix.endswith(("FULL_", "NEW_")):
            return content
        end_marker = "# RC1_CHECKPOINT_AUTHORIZATION_HARDENING_OWNER_SYNC_END"
        end = content.index(end_marker, start) + len(end_marker)
        suffix = content[end:]
        if prefix.endswith(("FULL_", "NEW_")):
            content = prefix + suffix.lstrip()
        else:
            content = prefix.rstrip() + "\n\n" + suffix.lstrip()
    anchors = ("\nNEW_FILES = {\n", "\nFULL_FILES = {\n", "\nFILES = {\n")
    anchor = next((candidate for candidate in anchors if candidate in content), None)
    if anchor is None:
        raise BootstrapError("Owning bootstrap insertion anchor is missing.")
    return content.replace(anchor, "\n" + OWNER_IMPORT + anchor, 1)


def run(command: list[str], root: Path, *, capture: bool = False) -> str:
    result = subprocess.run(command, cwd=root, text=True, capture_output=capture, check=False)
    if result.returncode:
        detail = result.stderr or result.stdout or "command failed"
        raise BootstrapError(f"{' '.join(command)}: {detail.strip()}")
    return result.stdout if capture else ""


def repository_root() -> Path:
    root = Path(__file__).resolve().parents[1]
    if root.name != EXPECTED_REPOSITORY or not (root / ".git").exists():
        raise BootstrapError("Run from the expected repository.")
    return root


def changed_paths(root: Path) -> set[str]:
    output = run(["git", "status", "--porcelain", "--untracked-files=all"], root, capture=True)
    return {line[3:].split(" -> ")[-1].strip('"') for line in output.splitlines() if line}


def allowed_paths() -> set[str]:
    return {
        SCRIPT_PATH,
        "scripts/capability_delivery.py",
        "docs/engineering/Capability_Delivery_Workflow.md",
        "tests/test_capability_delivery_workflow.py",
        *OWNER_FILES,
        *NEW_FILES,
        *MANAGED,
    }


def verify_context(root: Path) -> None:
    branch = run(["git", "branch", "--show-current"], root, capture=True).strip()
    if branch != EXPECTED_BRANCH:
        raise BootstrapError(f"Expected {EXPECTED_BRANCH}; found {branch}.")
    unexpected = changed_paths(root) - allowed_paths()
    if unexpected:
        raise BootstrapError("Unexpected working-tree paths: " + ", ".join(sorted(unexpected)))


def expected_content(root: Path) -> dict[str, str]:
    expected = {
        "scripts/capability_delivery.py": harden_helper((root / "scripts/capability_delivery.py").read_text(encoding="utf-8")),
        "docs/engineering/Capability_Delivery_Workflow.md": harden_workflow((root / "docs/engineering/Capability_Delivery_Workflow.md").read_text(encoding="utf-8")),
        "tests/test_capability_delivery_workflow.py": harden_tests((root / "tests/test_capability_delivery_workflow.py").read_text(encoding="utf-8")),
    }
    for relative in OWNER_FILES:
        expected[relative] = harden_owner((root / relative).read_text(encoding="utf-8"))
    for relative, (marker, body) in MANAGED.items():
        content = (root / relative).read_text(encoding="utf-8")
        if relative == "docs/product/Release_v1.0.md":
            content = reconcile_release_baseline(content)
        expected[relative] = upsert_text(content, marker, body)
    expected.update(NEW_FILES)
    return expected


def apply(root: Path) -> None:
    before = hashlib.sha256((root / SCRIPT_PATH).read_bytes()).hexdigest()
    for relative, content in expected_content(root).items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    after = hashlib.sha256((root / SCRIPT_PATH).read_bytes()).hexdigest()
    if before != after:
        raise BootstrapError("Bootstrap modified itself during apply.")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_generated(root: Path) -> None:
    for relative, content in expected_content(root).items():
        if (root / relative).read_text(encoding="utf-8") != content:
            raise BootstrapError(f"Generated content differs: {relative}")
    if digest(root / "assets/brand/logo/master/editorial-compass-mark-master.png") != MARK_HASH:
        raise BootstrapError("Approved brand mark changed.")
    if digest(root / "assets/brand/logo/master/editorial-compass-lockup-master.png") != LOCKUP_HASH:
        raise BootstrapError("Approved brand lockup changed.")
    if digest(root / "studio/article_engine.py") != ARTICLE_ENGINE_HASH:
        raise BootstrapError("Article Engine changed outside scope.")
    if digest(root / "studio/publication_package.py") != PUBLICATION_PACKAGE_HASH:
        raise BootstrapError("Publication Package changed outside scope.")


def validate_repository(root: Path) -> None:
    run([sys.executable, "-m", "compileall", "-q", "studio", "scripts", "tests"], root)
    run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], root)
    run([sys.executable, "studio.py", "validate"], root)
    run(["git", "diff", "--check"], root)


def preview(root: Path) -> None:
    print("RC1 checkpoint and delegated authorization hardening preview.")
    print("No files will be changed.\n")
    for relative in sorted(allowed_paths()):
        print(f"- {relative}")


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
        print(f"RC1 bootstrap stopped: {exc}", file=sys.stderr)
        raise SystemExit(1)
