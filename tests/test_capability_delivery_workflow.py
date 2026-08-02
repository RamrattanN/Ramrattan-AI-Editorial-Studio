"""High-risk behavioral tests for the Capability Delivery Workflow."""

from __future__ import annotations

import importlib.util
import io
import json
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "capability_delivery.py"
SPEC = importlib.util.spec_from_file_location("capability_delivery", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
delivery = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = delivery
SPEC.loader.exec_module(delivery)


def remote(
    *,
    state=delivery.RemoteState.FRESH,
    feature_head: str | None = "feature",
    reason: str = "",
):
    return delivery.RemoteSnapshot(
        state=state,
        base_head="base" if state is delivery.RemoteState.FRESH else "",
        feature_head=feature_head,
        reason=reason,
    )


def snapshot(
    *,
    branch: str = "feature/test",
    clean: bool = True,
    head: str | None = None,
    base_head: str = "base",
    remote_snapshot=None,
    ahead: int = 0,
    behind: int = 0,
    feature_exists: bool = True,
    upstream: str | None = "origin/feature/test",
):
    if remote_snapshot is None:
        remote_snapshot = remote()
    if head is None:
        head = "base" if branch == "develop" else "feature"
    return delivery.RepositorySnapshot(
        root=ROOT,
        branch=branch,
        status_lines=() if clean else (" M README.md",),
        head=head,
        base_head=base_head,
        upstream=upstream,
        ahead=ahead,
        behind=behind,
        feature_branch_exists=feature_exists,
        remote=remote_snapshot,
    )


def pull_request(
    *,
    number: int = 42,
    state: str = "OPEN",
    review=delivery.ReviewState.APPROVED,
    mergeability=delivery.MergeabilityState.CLEAN,
    checks=delivery.CheckState.SUCCESSFUL,
    head_oid: str = "feature",
):
    return delivery.PullRequestSnapshot(
        number=number,
        url=f"https://example.test/pull/{number}",
        state=state,
        head_oid=head_oid,
        review=review,
        mergeability=mergeability,
        checks=checks,
    )


def discovery(pr=None, *, state=None, reason: str = ""):
    if state is None:
        state = (
            delivery.ObservationState.FOUND
            if pr is not None
            else delivery.ObservationState.NOT_FOUND
        )
    return delivery.PullRequestDiscovery(
        state=state,
        matches=(pr,) if pr is not None else (),
        reason=reason,
    )


def recommendation(repo, pr_discovery):
    with patch.object(delivery, "snapshot", return_value=repo), patch.object(
        delivery,
        "discover_pull_requests",
        return_value=pr_discovery,
    ):
        return delivery.recommend(
            feature_branch="feature/test",
            commit_message="chore: test delivery",
            pr_title="Test delivery",
        )


def check_run(*, status: str = "COMPLETED", conclusion: str = "SUCCESS"):
    return {"status": status, "conclusion": conclusion}


def gh_item(
    *,
    number: int = 42,
    is_draft: bool = False,
    state: str = "OPEN",
    review_decision: str = "APPROVED",
    mergeable: str = "MERGEABLE",
    merge_state: str = "CLEAN",
    checks=None,
):
    return {
        "number": number,
        "url": f"https://example.test/pull/{number}",
        "state": state,
        "isDraft": is_draft,
        "reviewDecision": review_decision,
        "mergeable": mergeable,
        "mergeStateStatus": merge_state,
        "statusCheckRollup": checks if checks is not None else [check_run()],
        "headRefOid": "feature",
    }


class RemoteObservationTests(unittest.TestCase):
    def test_remote_verification_failure_fails_closed(self) -> None:
        result = recommendation(
            snapshot(
                remote_snapshot=remote(
                    state=delivery.RemoteState.UNAVAILABLE,
                    feature_head=None,
                    reason="network unavailable",
                )
            ),
            discovery(),
        )
        self.assertEqual(result.state, delivery.DeliveryState.REMOTE_VERIFICATION_FAILED)
        self.assertIsNone(result.command)

    def test_remote_response_requires_base_branch(self) -> None:
        command_result = delivery.CommandResult(("git",), 0, "", "")
        with patch.object(delivery, "run", return_value=command_result):
            observed = delivery.observe_remote(ROOT, "feature/test")
        self.assertEqual(observed.state, delivery.RemoteState.UNAVAILABLE)

    def test_remote_malformed_response_is_unavailable(self) -> None:
        command_result = delivery.CommandResult(("git",), 0, "malformed", "")
        with patch.object(delivery, "run", return_value=command_result):
            observed = delivery.observe_remote(ROOT, "feature/test")
        self.assertEqual(observed.state, delivery.RemoteState.UNAVAILABLE)

    def test_remote_freshness_uses_direct_heads(self) -> None:
        payload = "a" * 40 + "\trefs/heads/develop\n" + "b" * 40 + "\trefs/heads/feature/test"
        command_result = delivery.CommandResult(("git",), 0, payload, "")
        with patch.object(delivery, "run", return_value=command_result):
            observed = delivery.observe_remote(ROOT, "feature/test")
        self.assertEqual(observed.state, delivery.RemoteState.FRESH)
        self.assertEqual(observed.feature_head, "b" * 40)


class PullRequestDiscoveryTests(unittest.TestCase):
    def observe(self, result):
        with patch.object(delivery, "run", return_value=result):
            return delivery.discover_pull_requests(ROOT, feature_branch="feature/test")

    def test_auth_or_api_failure_is_unavailable_not_absent(self) -> None:
        observed = self.observe(
            delivery.CommandResult(("gh",), 1, "", "authentication failed")
        )
        self.assertEqual(observed.state, delivery.ObservationState.UNAVAILABLE)

    def test_malformed_json_is_unavailable(self) -> None:
        observed = self.observe(delivery.CommandResult(("gh",), 0, "{", ""))
        self.assertEqual(observed.state, delivery.ObservationState.UNAVAILABLE)

    def test_malformed_response_shape_is_unavailable(self) -> None:
        observed = self.observe(
            delivery.CommandResult(("gh",), 0, json.dumps({"number": 1}), "")
        )
        self.assertEqual(observed.state, delivery.ObservationState.UNAVAILABLE)

    def test_zero_matches_is_confirmed_not_found(self) -> None:
        observed = self.observe(delivery.CommandResult(("gh",), 0, "[]", ""))
        self.assertEqual(observed.state, delivery.ObservationState.NOT_FOUND)

    def test_one_match_is_found(self) -> None:
        observed = self.observe(
            delivery.CommandResult(("gh",), 0, json.dumps([gh_item()]), "")
        )
        self.assertEqual(observed.state, delivery.ObservationState.FOUND)
        self.assertEqual(observed.match.number, 42)

    def test_multiple_matches_are_ambiguous(self) -> None:
        observed = self.observe(
            delivery.CommandResult(
                ("gh",),
                0,
                json.dumps([gh_item(number=30), gh_item(number=31)]),
                "",
            )
        )
        self.assertEqual(observed.state, delivery.ObservationState.AMBIGUOUS)
        self.assertIn("#30", observed.reason)
        self.assertIn("#31", observed.reason)

    def test_missing_required_field_is_unavailable(self) -> None:
        item = gh_item()
        del item["isDraft"]
        observed = self.observe(
            delivery.CommandResult(("gh",), 0, json.dumps([item]), "")
        )
        self.assertEqual(observed.state, delivery.ObservationState.UNAVAILABLE)


class DraftRegressionTests(unittest.TestCase):
    def assert_draft_blocks_merge(self, number: int) -> None:
        result = recommendation(
            snapshot(),
            discovery(
                pull_request(number=number, review=delivery.ReviewState.DRAFT)
            ),
        )
        self.assertEqual(result.state, delivery.DeliveryState.PR_DRAFT)
        self.assertEqual(result.command, f"gh pr ready {number}")
        self.assertNotIn("merge", result.command)

    def test_pr30_draft_state_regression(self) -> None:
        self.assert_draft_blocks_merge(30)

    def test_pr31_draft_state_regression(self) -> None:
        self.assert_draft_blocks_merge(31)

    def test_pr33_draft_state_regression(self) -> None:
        self.assert_draft_blocks_merge(33)

    def test_discovery_failure_never_recommends_new_pr(self) -> None:
        result = recommendation(
            snapshot(),
            discovery(
                state=delivery.ObservationState.UNAVAILABLE,
                reason="GitHub API failed",
            ),
        )
        self.assertEqual(result.state, delivery.DeliveryState.PR_DISCOVERY_UNAVAILABLE)
        self.assertIsNone(result.command)


class ReviewAndMergeabilityTests(unittest.TestCase):
    def test_ready_for_review_but_blocked_is_explicit(self) -> None:
        result = recommendation(
            snapshot(),
            discovery(
                pull_request(
                    review=delivery.ReviewState.READY_FOR_REVIEW,
                    mergeability=delivery.MergeabilityState.BLOCKED,
                )
            ),
        )
        self.assertEqual(result.state, delivery.DeliveryState.PR_READY_FOR_REVIEW)

    def test_review_required_blocks(self) -> None:
        result = recommendation(
            snapshot(),
            discovery(pull_request(review=delivery.ReviewState.REVIEW_REQUIRED)),
        )
        self.assertEqual(result.state, delivery.DeliveryState.PR_REVIEW_REQUIRED)

    def test_changes_requested_blocks(self) -> None:
        result = recommendation(
            snapshot(),
            discovery(pull_request(review=delivery.ReviewState.CHANGES_REQUESTED)),
        )
        self.assertEqual(result.state, delivery.DeliveryState.PR_CHANGES_REQUESTED)

    def test_merge_conflict_blocks(self) -> None:
        result = recommendation(
            snapshot(),
            discovery(
                pull_request(mergeability=delivery.MergeabilityState.CONFLICTING)
            ),
        )
        self.assertEqual(result.state, delivery.DeliveryState.PR_MERGE_CONFLICT)

    def test_unknown_mergeability_blocks(self) -> None:
        result = recommendation(
            snapshot(),
            discovery(pull_request(mergeability=delivery.MergeabilityState.UNKNOWN)),
        )
        self.assertEqual(result.state, delivery.DeliveryState.PR_MERGEABILITY_UNKNOWN)

    def test_blocked_mergeability_blocks(self) -> None:
        result = recommendation(
            snapshot(),
            discovery(pull_request(mergeability=delivery.MergeabilityState.BLOCKED)),
        )
        self.assertEqual(result.state, delivery.DeliveryState.PR_MERGE_BLOCKED)


class CheckStateTests(unittest.TestCase):
    def assert_check_state(self, check_state, expected_delivery_state) -> None:
        result = recommendation(
            snapshot(),
            discovery(pull_request(checks=check_state)),
        )
        self.assertEqual(result.state, expected_delivery_state)
        self.assertNotIn("merge", result.command or "")

    def test_zero_checks_are_unavailable(self) -> None:
        self.assertEqual(delivery.classify_checks([]), delivery.CheckState.UNAVAILABLE)

    def test_unavailable_checks_block(self) -> None:
        self.assert_check_state(
            delivery.CheckState.UNAVAILABLE,
            delivery.DeliveryState.PR_CHECKS_UNAVAILABLE,
        )

    def test_pending_checks_use_read_only_watch(self) -> None:
        result = recommendation(
            snapshot(),
            discovery(pull_request(checks=delivery.CheckState.PENDING)),
        )
        self.assertEqual(result.state, delivery.DeliveryState.PR_CHECKS_PENDING)
        self.assertEqual(result.command, "gh pr checks 42 --watch")

    def test_failed_checks_block(self) -> None:
        self.assert_check_state(
            delivery.CheckState.FAILED,
            delivery.DeliveryState.PR_CHECKS_FAILED,
        )

    def test_cancelled_checks_block(self) -> None:
        self.assert_check_state(
            delivery.CheckState.CANCELLED,
            delivery.DeliveryState.PR_CHECKS_CANCELLED,
        )

    def test_timed_out_checks_block(self) -> None:
        self.assert_check_state(
            delivery.CheckState.TIMED_OUT,
            delivery.DeliveryState.PR_CHECKS_TIMED_OUT,
        )

    def test_action_required_checks_block(self) -> None:
        self.assert_check_state(
            delivery.CheckState.ACTION_REQUIRED,
            delivery.DeliveryState.PR_CHECKS_ACTION_REQUIRED,
        )

    def test_successful_checks_and_clean_pr_can_merge(self) -> None:
        result = recommendation(snapshot(), discovery(pull_request()))
        self.assertEqual(result.state, delivery.DeliveryState.READY_TO_MERGE)
        self.assertEqual(result.command, "gh pr merge 42 --merge --delete-branch")


class LocalWorkflowTests(unittest.TestCase):
    def test_clean_develop_creates_branch(self) -> None:
        result = recommendation(
            snapshot(
                branch="develop",
                feature_exists=False,
                remote_snapshot=remote(feature_head=None),
                upstream="origin/develop",
            ),
            discovery(),
        )
        self.assertEqual(result.command, "git switch -c feature/test")

    def test_dirty_develop_blocks_branch_creation(self) -> None:
        result = recommendation(
            snapshot(
                branch="develop",
                clean=False,
                remote_snapshot=remote(feature_head=None),
            ),
            discovery(),
        )
        self.assertEqual(result.state, delivery.DeliveryState.DEVELOP_DIRTY)

    def test_outdated_develop_uses_ff_only(self) -> None:
        result = recommendation(
            snapshot(
                branch="develop",
                base_head="old-base",
                remote_snapshot=remote(feature_head=None),
            ),
            discovery(),
        )
        self.assertEqual(result.command, "git pull --ff-only origin develop")

    def test_new_feature_branch_is_ready_for_work_not_push(self) -> None:
        result = recommendation(
            snapshot(
                head="base",
                remote_snapshot=remote(feature_head=None),
                upstream=None,
            ),
            discovery(),
        )
        self.assertEqual(result.state, delivery.DeliveryState.READY_FOR_WORK)
        self.assertIsNone(result.command)

    def test_unpublished_committed_feature_pushes(self) -> None:
        result = recommendation(
            snapshot(
                head="feature",
                remote_snapshot=remote(feature_head=None),
                upstream=None,
            ),
            discovery(),
        )
        self.assertEqual(result.state, delivery.DeliveryState.READY_TO_PUSH)

    def test_published_branch_without_pr_creates_pr(self) -> None:
        result = recommendation(snapshot(), discovery())
        self.assertEqual(result.state, delivery.DeliveryState.READY_FOR_PR)
        self.assertIn("--head feature/test", result.command or "")

    def test_feature_behind_remote_fails_closed(self) -> None:
        result = recommendation(snapshot(behind=1), discovery())
        self.assertEqual(result.state, delivery.DeliveryState.FEATURE_OUT_OF_SYNC)

    def test_multiple_pr_recommendation_fails_closed(self) -> None:
        result = recommendation(
            snapshot(),
            delivery.PullRequestDiscovery(
                state=delivery.ObservationState.AMBIGUOUS,
                matches=(pull_request(number=30), pull_request(number=31)),
                reason="multiple",
            ),
        )
        self.assertEqual(result.state, delivery.DeliveryState.PR_DISCOVERY_AMBIGUOUS)


class PostMergeRecoveryTests(unittest.TestCase):
    def merged(self, repo):
        with patch.object(delivery, "snapshot", return_value=repo), patch.object(
            delivery,
            "discover_pull_requests",
            return_value=discovery(pull_request(state="MERGED")),
        ), patch.object(delivery, "is_ancestor", return_value=True):
            return delivery.recommend(
                feature_branch="feature/test",
                commit_message="chore: test",
                pr_title="Test",
            )

    def test_merged_pr_on_feature_returns_to_develop(self) -> None:
        result = self.merged(snapshot())
        self.assertEqual(result.state, delivery.DeliveryState.POST_MERGE_CLEANUP)
        self.assertEqual(result.command, "git switch develop")

    def test_merged_pr_deletes_remaining_local_branch(self) -> None:
        result = self.merged(
            snapshot(
                branch="develop",
                feature_exists=True,
                remote_snapshot=remote(feature_head=None),
            )
        )
        self.assertEqual(result.command, "git branch -d feature/test")

    def test_merged_pr_deletes_remaining_remote_branch(self) -> None:
        result = self.merged(
            snapshot(branch="develop", feature_exists=False)
        )
        self.assertEqual(result.command, "git push origin --delete feature/test")

    def test_merged_pr_is_complete_after_cleanup(self) -> None:
        result = self.merged(
            snapshot(
                branch="develop",
                feature_exists=False,
                remote_snapshot=remote(feature_head=None),
            )
        )
        self.assertEqual(result.state, delivery.DeliveryState.COMPLETE)

    def test_merged_pr_with_unverified_ancestry_fails_closed(self) -> None:
        with patch.object(delivery, "is_ancestor", return_value=None):
            result = delivery.post_merge_recommendation(
                snapshot(), pull_request(state="MERGED"), "feature/test"
            )
        self.assertEqual(result.state, delivery.DeliveryState.UNKNOWN)


class DelegatedApprovalProfileTests(unittest.TestCase):
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


class DocumentationContractTests(unittest.TestCase):
    def test_documentation_exists(self) -> None:
        self.assertTrue((ROOT / "docs/engineering/Capability_Delivery_Workflow.md").is_file())

    def test_workflow_requires_partial_apply_recovery(self) -> None:
        content = (ROOT / "docs/engineering/Capability_Delivery_Workflow.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Partial-Apply Recovery", content)
        self.assertIn("--untracked-files=all", content)

    def test_workflow_requires_return_to_develop(self) -> None:
        content = (ROOT / "docs/engineering/Capability_Delivery_Workflow.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Return to Baseline", content)
        self.assertIn("branch is `develop`", content)


    def test_workflow_defines_profiles_and_consolidation_contract(self) -> None:
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
        self.assertIn("Product Runtime Impact\n\nNone", baseline)

    def test_owning_delivery_bootstraps_expose_refined_templates(self) -> None:
        scripts = str(ROOT / "scripts")
        if scripts not in sys.path:
            sys.path.insert(0, scripts)
        import bootstrap_capability008a2_delivery_hardening as hardened
        import bootstrap_capability_delivery_workflow as original

        self.assertEqual(hardened.CAPABILITY_DELIVERY_HELPER, original.CAPABILITY_DELIVERY_HELPER)
        self.assertIn("class ApprovalProfile", hardened.CAPABILITY_DELIVERY_HELPER)
        self.assertIn("Delegated Approval Profiles", hardened.CAPABILITY_DELIVERY_WORKFLOW)

if __name__ == "__main__":
    unittest.main()
