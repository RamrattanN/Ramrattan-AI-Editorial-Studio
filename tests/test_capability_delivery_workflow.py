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
