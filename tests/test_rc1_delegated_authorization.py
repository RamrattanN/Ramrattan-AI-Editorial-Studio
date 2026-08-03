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
