#!/usr/bin/env python3
"""
Populate and update the Ramrattan AI Editorial Studio GitHub Project.

Preview:
    python3 scripts/update_kanban_sprint3.py

Apply:
    python3 scripts/update_kanban_sprint3.py --apply
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


OWNER = "RamrattanN"
REPOSITORY = "Ramrattan-AI-Editorial-Studio"
REPO_SLUG = f"{OWNER}/{REPOSITORY}"

PROJECT_NUMBER = 1
PROJECT_ID = "PVT_kwHOAuXHyM4BfHW9"

STATUS_FIELD_ID = "PVTSSF_lAHOAuXHyM4BfHW9zhZclQY"

STATUS_OPTIONS = {
    "Todo": "f75ad846",
    "In Progress": "47fc9ee4",
    "Done": "98236657",
}

PROJECT_DESCRIPTION = (
    "Product roadmap for Ramrattan AI Editorial Studio - "
    "an adaptive editorial partner that follows the Author's "
    "creative process."
)

PROJECT_README = """# Ramrattan AI Editorial Studio

This project tracks the development of an adaptive editorial partner
that helps Authors transform evolving ideas, evidence, expertise, and
perspective into publication-ready thought leadership.

## Current position

- Sprint 1 - Repository Foundation: complete
- Sprint 2 - Editorial Workflow Prototype: complete
- Sprint 2.5 - Adaptive Product Foundation: complete or in review
- Sprint 3 - Adaptive Editorial Intelligence: next

## Sprint 3 sequence

1. Adaptive Editorial Context
2. Local Author Repository
3. Intent and Revision Intelligence
4. Evidence and Research
5. Visual System

## Product principle

The Studio adapts to the Author's creative process - never the other
way around.
"""


@dataclass(frozen=True)
class PlannedIssue:
    title: str
    body: str
    status: str = "Todo"


ISSUES = (
    PlannedIssue(
        title="Sprint 3A - Build the Adaptive Editorial Context",
        body="""## Capability

Adaptive Editorial Context

## Objective

Replace the final reliance on a linear workflow with a durable,
component-based Editorial Context.

## Scope

- Model Author intent
- Model sources and provenance
- Model Author perspectives
- Model candidate and selected editorial angles
- Model constraints and unresolved questions
- Model generated assets and approvals
- Model revision events
- Preserve recoverable history

## Product alignment

- Infer before asking
- Preserve context
- Everything is revisable
- Follow the Author

## Acceptance criteria

- Context can begin from any natural Author contribution
- Components can be independently revised
- Provenance is retained
- Existing workflow tests remain passing
- New adaptive-context tests pass
""",
    ),
    PlannedIssue(
        title="Sprint 3B - Implement the Local Author Repository",
        body="""## Capability

Author Repository

## Objective

Allow Authors to save, recall, review, archive, restore, export, and
delete previous editorial work.

## Present scope

- Local-first persistence
- Repository interface independent of storage technology
- Save Editorial Context
- Load work by stable ID
- List prior work
- Archive and restore work
- Delete work explicitly
- Export a publication package
- Preserve revision history and provenance

## Initial storage

Use a local implementation such as SQLite or structured JSON behind a
clean repository interface.

## Deferred scope

- Cloud accounts
- Cross-device synchronization
- Team collaboration
- Shared workspaces
- Billing and quotas
- Multi-tenant storage

## Privacy principle

Author work remains private by default.
""",
    ),
    PlannedIssue(
        title="Sprint 3C - Add Intent and Revision Intelligence",
        body="""## Capability

Editorial discernment and revision intelligence

## Objective

Interpret what each new Author contribution means without requiring
the Author to select a mode.

## Examples

A contribution may:

- introduce evidence,
- add or revise perspective,
- correct context,
- approve or reject an asset,
- request research,
- change the central angle,
- change output format,
- or return to earlier work.

## Acceptance criteria

- Intent is inferred from context where practical
- Clarification is requested only when ambiguity blocks progress
- Affected components are identified
- Unaffected approved work is preserved
- Revision events are recorded
""",
    ),
    PlannedIssue(
        title="Build the Evidence and Research Engine",
        body="""## Capability

Evidence and research

## Objective

Gather, verify, qualify, and attribute evidence that strengthens or
respectfully challenges the Author's perspective.

## Requirements

- Support URLs and topic-led research
- Support current-news verification
- Maintain provenance
- Separate fact, inference, and Author perspective
- Flag uncertainty and thin sources
- Avoid replacing the Author's position with generic AI opinion
""",
    ),
    PlannedIssue(
        title="Build the LinkedIn Visual System",
        body="""## Capability

Visual communication

## Objective

Generate visual concepts and 720 × 425 LinkedIn hero assets from the
Editorial Context.

## Initial directions

- Executive Editorial
- Magazine Cover
- Data Story

## Requirements

- Visuals follow the editorial angle
- Copy remains editable
- No hard-coded test topics
- Brand-neutral output
- No logos, watermarks, or recognizable faces by default
- Preserve the visual when unrelated written content changes
""",
    ),
    PlannedIssue(
        title="Future - Secure Cloud Author Repository",
        body="""## Future capability

Secure cloud persistence for Author work.

## Deferred until the local repository is validated

Potential future scope:

- Authentication
- Encryption and key management
- Cross-device synchronization
- Organization workspaces
- Collaboration and sharing
- Retention policies
- Privacy controls
- Export and account deletion
- Storage quotas and billing

This issue is intentionally future scope and should not block Sprint 3.
""",
    ),
)


class BoardError(RuntimeError):
    """Raised when the Kanban update cannot proceed safely."""


def run(
    command: list[str],
    *,
    capture: bool = False,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    print("$", " ".join(command))

    return subprocess.run(
        command,
        text=True,
        capture_output=capture,
        check=check,
    )


def output(command: list[str]) -> str:
    return run(command, capture=True).stdout.strip()


def json_output(command: list[str]) -> Any:
    raw = output(command)
    return json.loads(raw) if raw else {}


def validate_environment() -> None:
    run(["gh", "auth", "status"])

    root = Path(
        output(["git", "rev-parse", "--show-toplevel"])
    ).resolve()

    if root.name != REPOSITORY:
        raise BoardError(
            f"Expected repository '{REPOSITORY}', found '{root.name}'."
        )

    project = json_output(
        [
            "gh",
            "project",
            "view",
            str(PROJECT_NUMBER),
            "--owner",
            OWNER,
            "--format",
            "json",
        ]
    )

    if project.get("id") != PROJECT_ID:
        raise BoardError(
            "The GitHub Project ID does not match Project #1."
        )


def existing_project_items() -> dict[str, str]:
    payload = json_output(
        [
            "gh",
            "project",
            "item-list",
            str(PROJECT_NUMBER),
            "--owner",
            OWNER,
            "--limit",
            "200",
            "--format",
            "json",
        ]
    )

    result: dict[str, str] = {}

    for item in payload.get("items", []):
        item_id = item.get("id")
        content = item.get("content") or {}
        url = content.get("url")

        if item_id and url:
            result[url] = item_id

    return result


def add_url_to_project(
    url: str,
    existing: dict[str, str],
) -> str:
    if url in existing:
        print(f"Already on project: {url}")
        return existing[url]

    payload = json_output(
        [
            "gh",
            "project",
            "item-add",
            str(PROJECT_NUMBER),
            "--owner",
            OWNER,
            "--url",
            url,
            "--format",
            "json",
        ]
    )

    item_id = payload.get("id")

    if not item_id:
        raise BoardError(
            f"GitHub did not return a project item ID for {url}."
        )

    existing[url] = item_id
    return item_id


def set_status(item_id: str, status: str) -> None:
    option_id = STATUS_OPTIONS[status]

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
            option_id,
        ]
    )


def pull_request_status(number: int) -> tuple[str, str]:
    payload = json_output(
        [
            "gh",
            "pr",
            "view",
            str(number),
            "--repo",
            REPO_SLUG,
            "--json",
            "url,state,mergedAt",
        ]
    )

    url = payload["url"]

    if payload.get("mergedAt"):
        return url, "Done"

    if payload.get("state") == "OPEN":
        return url, "In Progress"

    return url, "Done"


def existing_issues() -> dict[str, str]:
    payload = json_output(
        [
            "gh",
            "issue",
            "list",
            "--repo",
            REPO_SLUG,
            "--state",
            "all",
            "--limit",
            "200",
            "--json",
            "title,url",
        ]
    )

    return {
        item["title"]: item["url"]
        for item in payload
    }


def ensure_issue(
    planned: PlannedIssue,
    known: dict[str, str],
) -> str:
    if planned.title in known:
        print(f"Existing issue: {planned.title}")
        return known[planned.title]

    url = output(
        [
            "gh",
            "issue",
            "create",
            "--repo",
            REPO_SLUG,
            "--title",
            planned.title,
            "--body",
            planned.body,
        ]
    )

    known[planned.title] = url
    return url


def preview() -> None:
    print("\nPlanned project update:\n")
    print("Pull requests:")
    print("  - PR #1 - automatic status")
    print("  - PR #2 - automatic status")
    print("  - PR #3 - automatic status")

    print("\nIssues:")
    for planned in ISSUES:
        print(f"  - [{planned.status}] {planned.title}")

    print("\nNothing has been changed.")
    print("Apply with:")
    print("  python3 scripts/update_kanban_sprint3.py --apply")


def apply_update() -> None:
    validate_environment()

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
        ]
    )

    project_items = existing_project_items()

    for number in (1, 2, 3):
        url, status = pull_request_status(number)
        item_id = add_url_to_project(url, project_items)
        set_status(item_id, status)
        print(f"PR #{number}: {status}")

    known_issues = existing_issues()

    for planned in ISSUES:
        url = ensure_issue(planned, known_issues)
        item_id = add_url_to_project(url, project_items)
        set_status(item_id, planned.status)
        print(f"{planned.title}: {planned.status}")

    print("\nProject update complete.")
    print("\nCurrent items:")

    run(
        [
            "gh",
            "project",
            "item-list",
            str(PROJECT_NUMBER),
            "--owner",
            OWNER,
            "--limit",
            "200",
        ]
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Update the Sprint 3 GitHub Project board."
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Create issues and update Project #1.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        if args.apply:
            apply_update()
        else:
            preview()

        return 0

    except BoardError as exc:
        print(f"\nERROR: {exc}", file=sys.stderr)
        return 1

    except subprocess.CalledProcessError as exc:
        print(
            f"\nERROR: Command failed with exit code "
            f"{exc.returncode}.",
            file=sys.stderr,
        )
        return exc.returncode

    except Exception as exc:
        print(f"\nUNEXPECTED ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())