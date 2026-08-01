#!/usr/bin/env python3
"""
Repair, validate, and publish PR-003A - Product Foundation.

Safe run:
    python3 scripts/complete_pr003a_product_foundation.py

Publish:
    python3 scripts/complete_pr003a_product_foundation.py --publish

This script is designed for the current PR-003A working branch after the
product-foundation documents have already been generated.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import textwrap
from pathlib import Path


REPOSITORY_NAME = "Ramrattan-AI-Editorial-Studio"
REMOTE_FRAGMENT = "RamrattanN/Ramrattan-AI-Editorial-Studio"

BASE_BRANCH = "develop"
FEATURE_BRANCH = "feature/product-foundation"

COMMIT_MESSAGE = "docs: establish the adaptive product foundation"
PR_TITLE = "PR-003A: Establish the adaptive product foundation"


def clean(value: str) -> str:
    """Normalize embedded text and ensure one trailing newline."""
    return textwrap.dedent(value).strip() + "\n"


CORRECTED_TEST_FILE = clean(
    '''
    """Tests for the product-foundation documentation."""

    from __future__ import annotations

    import unittest
    from pathlib import Path


    ROOT = Path(__file__).resolve().parents[1]
    PRODUCT = ROOT / "docs" / "product"

    REQUIRED_FILES = (
        "PRD_v1.0.md",
        "Constitution.md",
        "Product_Principles.md",
        "Studio_Contract.md",
        "Adaptive_Editorial_Model.md",
        "Author_Journey.md",
        "Things_We_Will_Not_Do.md",
        "Glossary.md",
        "Decision_Log.md",
        "Editorial_Intelligence_Manifesto.md",
    )


    def normalized_text(path: Path) -> str:
        """
        Read Markdown and normalize whitespace.

        This prevents harmless Markdown line wrapping from causing
        false test failures.
        """
        content = path.read_text(encoding="utf-8")
        return " ".join(content.split())


    class ProductFoundationTests(unittest.TestCase):
        def test_required_documents_exist(self) -> None:
            for filename in REQUIRED_FILES:
                with self.subTest(filename=filename):
                    self.assertTrue(
                        (PRODUCT / filename).is_file(),
                        msg=f"Missing product document: {filename}",
                    )

        def test_prd_is_not_url_first(self) -> None:
            content = normalized_text(PRODUCT / "PRD_v1.0.md")

            self.assertIn("adaptive editorial partner", content)
            self.assertIn("headline", content)
            self.assertIn("perspective", content)
            self.assertIn("Editorial Context", content)

        def test_constitution_preserves_reversibility(self) -> None:
            content = normalized_text(PRODUCT / "Constitution.md")

            self.assertIn("Everything Is Revisable", content)
            self.assertIn("Infer Before Asking", content)
            self.assertIn("Preserve Context", content)

        def test_adaptive_model_marks_linear_workflow_as_prototype(
            self,
        ) -> None:
            content = normalized_text(
                PRODUCT / "Adaptive_Editorial_Model.md"
            )

            self.assertIn(
                "not the final product interaction model",
                content,
            )

        def test_glossary_defines_author_and_context(self) -> None:
            content = normalized_text(PRODUCT / "Glossary.md")

            self.assertIn("## Author", content)
            self.assertIn("## Editorial Context", content)

        def test_readme_uses_adaptive_positioning(self) -> None:
            content = normalized_text(ROOT / "README.md")

            self.assertIn("adaptive editorial partner", content)
            self.assertIn("Authors May Begin With", content)
            self.assertIn(
                "The Studio interprets what is happening",
                content,
            )

        def test_adr_records_target_architecture(self) -> None:
            adr = (
                ROOT
                / "docs"
                / "architecture"
                / "adr"
                / "ADR-002-adopt-an-adaptive-editorial-context.md"
            )
            content = normalized_text(adr)

            self.assertIn(
                "evolving Editorial Context",
                content,
            )
            self.assertIn(
                "does not define the final product interaction model",
                content,
            )


    if __name__ == "__main__":
        unittest.main()
    '''
)


REQUIRED_PRODUCT_FILES = (
    "docs/product/PRD_v1.0.md",
    "docs/product/Constitution.md",
    "docs/product/Product_Principles.md",
    "docs/product/Studio_Contract.md",
    "docs/product/Adaptive_Editorial_Model.md",
    "docs/product/Author_Journey.md",
    "docs/product/Things_We_Will_Not_Do.md",
    "docs/product/Glossary.md",
    "docs/product/Decision_Log.md",
    "docs/product/Editorial_Intelligence_Manifesto.md",
    "docs/architecture/adr/ADR-002-adopt-an-adaptive-editorial-context.md",
    "README.md",
    "CHANGELOG.md",
    "ROADMAP.md",
    "docs/Project_Charter.md",
)


class CompletionError(RuntimeError):
    """Raised when PR-003A cannot be completed safely."""


def run(
    command: list[str],
    *,
    cwd: Path,
    capture: bool = False,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    """Run a command after displaying it."""
    print("$", " ".join(command))

    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=capture,
        check=check,
    )


def output(command: list[str], *, cwd: Path) -> str:
    """Run a command and return stripped standard output."""
    return run(
        command,
        cwd=cwd,
        capture=True,
    ).stdout.strip()


def repository_root() -> Path:
    """Locate and validate the expected Git repository."""
    try:
        root = Path(
            output(
                ["git", "rev-parse", "--show-toplevel"],
                cwd=Path.cwd(),
            )
        ).resolve()
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise CompletionError(
            "Run this script from inside the cloned repository."
        ) from exc

    if root.name != REPOSITORY_NAME:
        raise CompletionError(
            f"Expected repository '{REPOSITORY_NAME}', "
            f"found '{root.name}'."
        )

    remote = output(
        ["git", "remote", "get-url", "origin"],
        cwd=root,
    )

    if REMOTE_FRAGMENT not in remote:
        raise CompletionError(
            "The origin remote does not match the expected repository."
        )

    return root


def current_branch(root: Path) -> str:
    """Return the current Git branch."""
    return output(
        ["git", "branch", "--show-current"],
        cwd=root,
    )


def require_feature_branch(root: Path) -> None:
    """Ensure PR-003A is being completed on the correct branch."""
    branch = current_branch(root)

    if branch != FEATURE_BRANCH:
        raise CompletionError(
            f"Expected branch '{FEATURE_BRANCH}', "
            f"but the current branch is '{branch}'."
        )


def repair_test(root: Path) -> None:
    """Replace the fragile test with a whitespace-safe test."""
    destination = root / "tests" / "test_product_foundation.py"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        CORRECTED_TEST_FILE,
        encoding="utf-8",
    )

    print("Repaired tests/test_product_foundation.py")


def validate_required_files(root: Path) -> None:
    """Confirm that all PR-003A product artifacts exist."""
    missing = [
        relative
        for relative in REQUIRED_PRODUCT_FILES
        if not (root / relative).is_file()
    ]

    if missing:
        details = "\n".join(
            f"  - {relative}" for relative in missing
        )
        raise CompletionError(
            "PR-003A is missing required artifacts:\n"
            f"{details}"
        )

    print("All required PR-003A artifacts are present.")


def validate_product_language(root: Path) -> None:
    """Confirm the repository reflects the corrected product vision."""
    checks: dict[str, tuple[str, ...]] = {
        "README.md": (
            "adaptive editorial partner",
            "Authors May Begin With",
            "The Studio interprets what is happening",
        ),
        "docs/product/PRD_v1.0.md": (
            "adaptive editorial partner",
            "Editorial Context",
            "perspective",
            "headline",
        ),
        "docs/product/Constitution.md": (
            "Infer Before Asking",
            "Everything Is Revisable",
            "Preserve Context",
        ),
        "docs/product/Adaptive_Editorial_Model.md": (
            "not the final product",
            "interaction model",
        ),
        "docs/architecture/adr/"
        "ADR-002-adopt-an-adaptive-editorial-context.md": (
            "evolving Editorial Context",
            "does not define the final product interaction model",
        ),
    }

    for relative, required_phrases in checks.items():
        path = root / relative
        content = " ".join(
            path.read_text(encoding="utf-8").split()
        )

        for phrase in required_phrases:
            if phrase not in content:
                raise CompletionError(
                    f"Expected phrase '{phrase}' in {relative}."
                )

    print("Product-positioning validation passed.")


def run_validation(root: Path) -> None:
    """Compile the package and execute all tests."""
    run(
        [
            sys.executable,
            "-m",
            "compileall",
            "-q",
            "studio",
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

    print("PR-003A validation passed.")


def pull_request_body() -> str:
    """Return the PR-003A pull-request description."""
    return clean(
        """
        ## Summary

        Establishes the adaptive product foundation for Ramrattan AI
        Editorial Studio.

        ## Problem

        Earlier product language and architecture implied that Authors
        would follow a fixed, URL-led sequence.

        That model did not reflect how Authors naturally begin with
        URLs, headlines, observations, news references, perspectives,
        notes, drafts, or combinations of these inputs.

        It also did not adequately support Authors changing direction
        during the creative process.

        ## Changes

        - Adds Product Requirements Document v1.0
        - Adds the Product Constitution
        - Adds Product Principles
        - Adds the Studio Contract
        - Adds the Adaptive Editorial Model
        - Adds the Author Journey
        - Adds explicit product constraints
        - Adds the Product Glossary
        - Adds the Product Decision Log
        - Adds the Editorial Intelligence Manifesto
        - Adds ADR-002 - Adopt an Adaptive Editorial Context
        - Updates the README
        - Updates the Project Charter
        - Updates the roadmap and changelog
        - Adds product-foundation validation tests

        ## Product Alignment

        **Capability improved:**  
        Product definition and adaptive editorial intelligence.

        **Product Principles reinforced:**  
        Follow the Author, Infer Before Asking, Preserve Momentum,
        Everything Is Revisable, and Preserve Context.

        **Constitution Articles supported:**  
        Articles I through X.

        **Author benefit:**  
        Authors may begin naturally, add or revise perspective, change
        direction, and retain useful earlier work.

        **Future compatibility:**  
        Establishes the requirements for the adaptive Editorial Context
        architecture.

        ## Validation

        ```bash
        python3 -m compileall -q studio tests
        python3 -m unittest discover -s tests -v
        python3 studio.py validate
        ```

        ## Risk

        The repository still contains a linear workflow prototype.

        This PR documents that the prototype is not the final product
        interaction model.

        ## Rollback

        Close the pull request without merging, or revert the PR-003A
        commit after merge.
        """
    )


def publish(root: Path) -> None:
    """Stage, commit, push, and create PR-003A."""
    run(["gh", "auth", "status"], cwd=root)
    run(["git", "add", "."], cwd=root)

    staged = output(
        ["git", "diff", "--cached", "--name-only"],
        cwd=root,
    )

    if not staged:
        print("No staged changes are available to publish.")
        return

    run(
        [
            "git",
            "commit",
            "-m",
            COMMIT_MESSAGE,
        ],
        cwd=root,
    )

    run(
        [
            "git",
            "push",
            "--set-upstream",
            "origin",
            FEATURE_BRANCH,
        ],
        cwd=root,
    )

    existing = subprocess.run(
        [
            "gh",
            "pr",
            "view",
            FEATURE_BRANCH,
            "--json",
            "url",
            "--jq",
            ".url",
        ],
        cwd=root,
        text=True,
        capture_output=True,
    )

    if existing.returncode == 0 and existing.stdout.strip():
        print(
            "Pull request already exists: "
            f"{existing.stdout.strip()}"
        )
        return

    run(
        [
            "gh",
            "pr",
            "create",
            "--base",
            BASE_BRANCH,
            "--head",
            FEATURE_BRANCH,
            "--title",
            PR_TITLE,
            "--body",
            pull_request_body(),
        ],
        cwd=root,
    )


def parse_args() -> argparse.Namespace:
    """Parse command-line options."""
    parser = argparse.ArgumentParser(
        description=(
            "Repair, validate, and publish the PR-003A "
            "product foundation."
        )
    )

    parser.add_argument(
        "--publish",
        action="store_true",
        help=(
            "Commit, push, and open PR-003A after validation."
        ),
    )

    return parser.parse_args()


def main() -> int:
    """Run the PR-003A completion process."""
    args = parse_args()

    try:
        root = repository_root()

        print(f"Repository: {root}")
        print(f"Branch: {current_branch(root)}")

        require_feature_branch(root)
        repair_test(root)
        validate_required_files(root)
        validate_product_language(root)
        run_validation(root)

        print("\nGit status:")
        run(
            ["git", "status", "--short"],
            cwd=root,
        )

        print("\nChange summary:")
        run(
            ["git", "diff", "--stat"],
            cwd=root,
        )

        if args.publish:
            publish(root)
        else:
            print()
            print("PR-003A has been repaired and validated.")
            print("Nothing has been committed or pushed.")
            print()
            print("Publish with:")
            print(
                "  python3 "
                "scripts/complete_pr003a_product_foundation.py "
                "--publish"
            )

        return 0

    except CompletionError as exc:
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
        print(
            f"\nUNEXPECTED ERROR: {exc}",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())