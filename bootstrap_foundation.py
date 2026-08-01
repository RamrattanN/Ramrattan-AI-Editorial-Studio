#!/usr/bin/env python3
"""
Bootstrap Sprint 1 for Ramrattan AI Editorial Studio.

Safe default behavior:
- Confirms the repository identity
- Backs up current uncommitted files
- Creates or repairs the foundation files
- Validates the result
- Does not commit or push unless --publish is supplied
"""

from __future__ import annotations

import argparse
import datetime as dt
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path

EXPECTED_REPOSITORY = "Ramrattan-AI-Editorial-Studio"
EXPECTED_REMOTE_FRAGMENT = "RamrattanN/Ramrattan-AI-Editorial-Studio"
FEATURE_BRANCH = "feature/repository-foundation"
BASE_BRANCH = "develop"
VERSION = "3.0.0-rc1"


def clean(text: str) -> str:
    """Remove code indentation and ensure one trailing newline."""
    return textwrap.dedent(text).strip() + "\n"


FILES: dict[str, str] = {
    "VERSION": clean(
        """
        3.0.0-rc1
        """
    ),
    "README.md": clean(
        """
        # Ramrattan AI Editorial Studio

        > **Engineering AI-assisted thought leadership with the discipline of software development.**

        [![Status](https://img.shields.io/badge/status-v3.0.0--rc1-blue)](VERSION)
        [![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
        [![Stage](https://img.shields.io/badge/stage-foundation-orange)](ROADMAP.md)

        Ramrattan AI Editorial Studio is an open-source framework for turning a single source URL into premium, visual-first LinkedIn thought leadership.

        The project treats AI editorial workflows as maintainable products rather than isolated prompts.

        ## Why This Project Exists

        AI can produce content quickly. Producing content that is original, evidence-based, visually coherent, reviewable, and repeatable is a more demanding problem.

        This project addresses that gap through:

        - Versioned prompt architecture
        - Guided editorial workflows
        - Visual-first content design
        - Explicit review checkpoints
        - Architecture Decision Records
        - Regression testing
        - Reversible releases
        - Documented editorial standards

        ## Current Scope

        The first production module focuses on LinkedIn:

        - Short LinkedIn articles
        - Seven-slide LinkedIn carousels
        - 720 × 425 hero infographics
        - Executive Editorial visual direction
        - Magazine Cover visual direction
        - Data Story visual direction
        - Guided option-based selection
        - Editable visual and written content
        - Source attribution and originality controls

        ## Core Workflow

        ```text
        Source URL
            ↓
        Source Analysis
            ↓
        Strongest Defensible Insight
            ↓
        Content Type
            ↓
        Visual Direction
            ↓
        Hero Copy Selection
            ↓
        720 × 425 Infographic
            ↓
        Graphic Review
            ↓
        Written Content
            ↓
        Final Review
        ```

        ## Product Principles

        ### Visual-First

        The hero graphic establishes the editorial narrative. The written content reinforces it.

        ### Guided

        The system presents concise options instead of requiring unnecessary free-form input.

        ### Original

        Reference material may inform sentiment or context, but output must use a distinct argument, structure, and language.

        ### Evidence-Based

        Every final piece includes at least one meaningful number and identifies relevant assumptions.

        ### Maintainable

        Prompts, decisions, releases, and tests are versioned and documented.

        ### Reversible

        Each significant change has a rollback path.

        ## Repository Structure

        ```text
        .
        ├── .github/                  GitHub templates and automation
        ├── assets/                   Visual and branding assets
        ├── docs/                     Architecture and project documentation
        │   ├── architecture/adr/     Architecture Decision Records
        │   ├── Handoff/              Historical and transition records
        │   └── learning/             Educational material
        ├── examples/                 Curated examples
        ├── prompts/                  Versioned GPT instructions
        ├── releases/                 Release snapshots
        ├── scripts/                  Maintenance and release utilities
        ├── templates/                Reusable project templates
        ├── tests/                    Regression and acceptance tests
        ├── CHANGELOG.md
        ├── CONTRIBUTING.md
        ├── ROADMAP.md
        ├── VERSION
        └── studio.py
        ```

        ## Current Release

        **Version:** `v3.0.0-rc1`

        **Stage:** Sprint 1 - The Foundation

        This release candidate establishes the repository structure, governance model, versioning strategy, and initial command-line interface.

        ## Documentation

        Start with:

        1. [Project Charter](docs/Project_Charter.md)
        2. [Architecture Decision Records](docs/architecture/adr/README.md)
        3. [Roadmap](ROADMAP.md)
        4. [Contributing Guide](CONTRIBUTING.md)
        5. [Changelog](CHANGELOG.md)

        ## Command-Line Interface

        ```bash
        python3 studio.py status
        python3 studio.py structure
        python3 studio.py validate
        python3 studio.py version
        ```

        ## Contributing

        Contributions, issue reports, documentation improvements, and design discussions are welcome.

        Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

        ## License

        This project is licensed under the MIT License. See [LICENSE](LICENSE).

        ---

        **Ramrattan AI Editorial Studio**

        Clarity over cleverness. Quality over speed. Documented decisions over hidden assumptions.
        """
    ),
    "CHANGELOG.md": clean(
        """
        # Changelog

        All notable changes to Ramrattan AI Editorial Studio are documented here.

        ## [Unreleased]

        ### Planned

        - Versioned GPT prompt architecture
        - Guided content workflow
        - Visual design standards
        - Regression tests
        - Example content packages

        ## [3.0.0-rc1] - 2026-08-01

        ### Added

        - Repository foundation
        - Project charter
        - Flagship README
        - Product motto and principles
        - Semantic version file
        - Initial roadmap
        - Contribution guide
        - Code of conduct
        - Architecture Decision Record framework
        - ADR-000 - Build AI Products Like Software
        - Initial `studio.py` command-line scaffold
        - GitHub issue templates
        - Pull request template
        - Release checklist
        - Preservation of the original README

        ### Changed

        - Reframed the project from a single prompt into a maintainable AI editorial product
        - Established `develop` as the integration branch
        - Established feature branches for reviewable changes

        ### Known Limitations

        - Final GPT instructions are not yet included
        - Visual-generation rules are not yet implemented
        - Full regression tests are not yet implemented
        - GitHub Project board is not yet configured
        """
    ),
    "ROADMAP.md": clean(
        """
        # Roadmap

        ## Current Target

        `v3.0.0-rc1`

        ## Now - Foundation

        - [x] Public repository
        - [x] MIT license
        - [x] Python `.gitignore`
        - [x] Repository scaffold
        - [x] Project charter
        - [x] Changelog
        - [x] Version file
        - [x] Initial CLI scaffold
        - [x] GitHub templates
        - [ ] Architecture documentation
        - [ ] Workflow documentation
        - [ ] Versioning guide
        - [ ] Release process
        - [ ] Full handoff document
        - [ ] Kanban project board

        ## Next - Guided Editorial Studio

        Target: `v3.0.0`

        - [ ] Preserve the original V1 prompt
        - [ ] Document the V2 visual-first prompt
        - [ ] Implement the V3 guided prompt
        - [ ] Add visual style selection
        - [ ] Add hero-copy review
        - [ ] Add infographic review
        - [ ] Add backward navigation
        - [ ] Add state-preservation rules
        - [ ] Add final content review
        - [ ] Add source and originality safeguards

        ## Later - Visual Intelligence

        Target: `v3.1.0`

        - [ ] Executive Editorial visual specification
        - [ ] Magazine Cover visual specification
        - [ ] Data Story visual specification
        - [ ] Palette selection
        - [ ] Safe-area guidance
        - [ ] Text-legibility validation
        - [ ] Visual regeneration controls

        ## Future - Content Studio

        Target: `v4.0.0`

        - [ ] Newsletter output
        - [ ] Blog output
        - [ ] Executive briefing output
        - [ ] Presentation output
        - [ ] Speaker notes
        - [ ] Multi-platform content adaptation
        - [ ] Brand voice profiles
        - [ ] Knowledge-vault integration

        ## Success Measures

        The project should improve:

        - Editorial quality
        - Visual coherence
        - Originality
        - Ease of use
        - Maintainability
        - Reproducibility
        - Release confidence
        """
    ),
    "CONTRIBUTING.md": clean(
        """
        # Contributing

        Thank you for contributing to Ramrattan AI Editorial Studio.

        ## Guiding Principle

        Every enhancement must make the product more maintainable, more intuitive, or more valuable.

        ## Development Model

        - `main` contains stable releases.
        - `develop` contains integrated work for the next release.
        - Feature branches contain focused changes.

        Recommended branch names:

        ```text
        feature/short-description
        docs/short-description
        fix/short-description
        test/short-description
        ```

        ## Commit Messages

        Use concise conventional prefixes:

        ```text
        feat: add a new capability
        docs: improve documentation
        fix: correct a defect
        test: add or improve tests
        refactor: improve internal structure
        release: prepare or publish a release
        ```

        ## Pull Requests

        A pull request should:

        - Solve one coherent problem
        - Explain why the change is needed
        - Describe the implementation
        - Include validation notes
        - Mention related issues
        - Preserve approved behavior unless explicitly replacing it

        ## Significant Decisions

        Create an Architecture Decision Record when a change:

        - Alters the product workflow
        - Alters the prompt architecture
        - Alters the visual system
        - Alters release or versioning policy
        - Creates a lasting constraint
        - Rejects a credible alternative

        ## Editorial Standards

        Contributions should preserve:

        - Originality
        - Evidence-based claims
        - Clear source attribution
        - Jargon-light language
        - Visual and written alignment
        - Brand-neutral output
        - Space - hyphen - space
        - No en dashes or em dashes in generated editorial copy

        ## Code of Conduct

        Participation is governed by [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
        """
    ),
    "CODE_OF_CONDUCT.md": clean(
        """
        # Code of Conduct

        ## Our Standard

        Ramrattan AI Editorial Studio is committed to a respectful, constructive, and welcoming environment.

        Expected behavior includes:

        - Communicating professionally
        - Giving actionable feedback
        - Respecting differing experience levels
        - Critiquing ideas rather than people
        - Attributing contributions
        - Disclosing uncertainty
        - Correcting errors openly

        Unacceptable behavior includes:

        - Harassment
        - Personal attacks
        - Discrimination
        - Plagiarism
        - Deliberate misrepresentation
        - Publishing private information without permission
        - Disruptive or bad-faith participation

        ## Enforcement

        Project maintainers may edit, reject, or remove contributions that conflict with these standards.

        Concerns should be raised privately with the repository owner through an appropriate GitHub channel.
        """
    ),
    "docs/Project_Charter.md": clean(
        """
        # Project Charter

        ## Project

        Ramrattan AI Editorial Studio

        ## Version

        `v3.0.0-rc1`

        ## Motto

        > Engineering AI-assisted thought leadership with the discipline of software development.

        ## Vision

        Build a maintainable, transparent, and professional AI-powered editorial studio for executive thought leadership.

        ## Mission

        Transform a single source into publication-ready thought leadership with minimal user effort while maintaining originality, evidence quality, editorial coherence, and visual excellence.

        ## Initial Scope

        The first module creates:

        - LinkedIn articles
        - Seven-slide LinkedIn carousels
        - 720 × 425 LinkedIn hero infographics
        - Supporting headlines and descriptions
        - Practical takeaways
        - Discussion-oriented calls to action
        - Source attribution
        - Structured hashtags

        ## Core Principles

        - Visual-first
        - Guided
        - Evidence-based
        - Original
        - Transparent
        - Maintainable
        - Reversible

        ## Primary Audience

        - Managers
        - Executives
        - Industry practitioners
        - Consultants
        - Real estate professionals
        - Business-to-business content creators

        ## Current Non-Goals

        The initial release will not:

        - Publish directly to LinkedIn
        - Replace human editorial judgment
        - Guarantee interface-level clickable buttons
        - Reproduce another organization's visual identity
        - Store private user credentials
        - Train on private content without explicit direction

        ## Sprint 1 Definition of Done

        Sprint 1 is complete when:

        - Repository structure is established
        - Project charter is published
        - Changelog and roadmap exist
        - ADR framework exists
        - Versioning is explicit
        - Initial CLI validates the structure
        - GitHub contribution templates exist
        - PR-001 is reviewed and merged into `develop`
        """
    ),
    "docs/architecture/adr/README.md": clean(
        """
        # Architecture Decision Records

        Architecture Decision Records - ADRs - capture significant product and engineering decisions.

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

        ## Current Records

        - [ADR-000 - Build AI Products Like Software](ADR-000-build-ai-products-like-software.md)
        """
    ),
    "docs/architecture/adr/ADR-000-build-ai-products-like-software.md": clean(
        """
        # ADR-000 - Build AI Products Like Software

        ## Status

        Accepted

        ## Date

        2026-08-01

        ## Context

        Many AI projects begin as isolated prompts and gradually become difficult to understand, test, maintain, and improve.

        Prompt changes may be undocumented. Workflows may rely on hidden assumptions. Earlier behavior may be difficult to restore.

        ## Decision

        Ramrattan AI Editorial Studio will use established software engineering practices, including:

        - Version control
        - Semantic versioning
        - Documentation
        - Architecture Decision Records
        - Reviewable branches
        - Release candidates
        - Regression testing
        - Changelogs
        - Rollback paths
        - Explicit acceptance criteria

        Prompt engineering is treated as one component of the product rather than the entire product.

        ## Alternatives Considered

        ### Maintain one continuously edited prompt

        Rejected because it provides weak traceability and makes rollback difficult.

        ### Maintain dated prompt copies only

        Rejected because it preserves history without addressing testing, architecture, workflow, or release quality.

        ### Build a fully automated application immediately

        Deferred because it would add premature complexity before the editorial workflow is validated.

        ## Consequences

        ### Positive

        - Decisions remain understandable
        - Releases remain traceable
        - Prompt drift can be identified
        - Changes can be reviewed and reversed
        - Contributors have clearer standards

        ### Costs

        - Documentation requires time
        - Releases require discipline
        - Some changes move more slowly

        ## Outcome

        Accepted as the founding architectural principle.
        """
    ),
    "templates/ADR.md": clean(
        """
        # ADR-XXX - Decision Title

        ## Status

        Proposed

        ## Date

        YYYY-MM-DD

        ## Context

        Describe the problem, constraints, and forces affecting the decision.

        ## Decision

        Describe the selected approach.

        ## Alternatives Considered

        ### Alternative 1

        Explain why it was not selected.

        ## Consequences

        ### Positive

        - Benefit

        ### Costs and Risks

        - Cost or risk

        ## Outcome

        State the final result.
        """
    ),
    "docs/Release_Checklist.md": clean(
        """
        # Release Checklist

        ## Preparation

        - [ ] Version selected
        - [ ] Release scope agreed
        - [ ] Acceptance criteria met
        - [ ] Changelog updated
        - [ ] Documentation updated
        - [ ] ADRs accepted where required
        - [ ] Known limitations documented

        ## Validation

        - [ ] `python3 studio.py validate` passes
        - [ ] Prompt files reviewed
        - [ ] Examples reviewed
        - [ ] Regression tests pass
        - [ ] No secrets or private data are present

        ## Git

        - [ ] Feature branches merged into `develop`
        - [ ] Release candidate reviewed
        - [ ] `develop` merged into `main`
        - [ ] Version tag created
        - [ ] Release notes published

        ## Post-Release

        - [ ] Repository release verified
        - [ ] Roadmap updated
        - [ ] Follow-up issues created
        - [ ] Rollback target confirmed
        """
    ),
    ".github/PULL_REQUEST_TEMPLATE.md": clean(
        """
        # Summary

        Describe the change.

        ## Problem

        What problem does this solve?

        ## Rationale

        Why is this approach appropriate?

        ## Changes

        - Change

        ## Validation

        - [ ] Documentation reviewed
        - [ ] Project validation completed
        - [ ] No credentials or private data included
        - [ ] Changelog updated where appropriate

        ## Architecture Decision

        - [ ] No ADR required
        - [ ] ADR added or updated

        ## Related Issues

        Closes #

        ## Rollback

        Describe how this change can be reversed.
        """
    ),
    ".github/ISSUE_TEMPLATE/feature_request.yml": clean(
        """
        name: Feature request
        description: Propose an improvement to the editorial studio
        title: "[Feature]: "
        labels:
          - enhancement
        body:
          - type: textarea
            id: problem
            attributes:
              label: Problem
              description: What problem should this feature solve?
            validations:
              required: true

          - type: textarea
            id: proposal
            attributes:
              label: Proposed solution
              description: Describe the desired behavior.
            validations:
              required: true

          - type: textarea
            id: value
            attributes:
              label: Product value
              description: How does this make the product more maintainable, intuitive, or valuable?
            validations:
              required: true

          - type: textarea
            id: acceptance
            attributes:
              label: Acceptance criteria
            validations:
              required: true
        """
    ),
    ".github/ISSUE_TEMPLATE/bug_report.yml": clean(
        """
        name: Bug report
        description: Report incorrect or inconsistent behavior
        title: "[Bug]: "
        labels:
          - bug
        body:
          - type: input
            id: version
            attributes:
              label: Version
              placeholder: v3.0.0-rc1
            validations:
              required: true

          - type: textarea
            id: current
            attributes:
              label: Current behavior
            validations:
              required: true

          - type: textarea
            id: expected
            attributes:
              label: Expected behavior
            validations:
              required: true

          - type: textarea
            id: steps
            attributes:
              label: Reproduction steps
            validations:
              required: true
        """
    ),
    ".github/workflows/validate.yml": clean(
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

              - name: Validate project structure
                run: python3 studio.py validate
        """
    ),
    "studio.py": clean(
        '''
        #!/usr/bin/env python3
        """Project utilities for Ramrattan AI Editorial Studio."""

        from __future__ import annotations

        import argparse
        import sys
        from pathlib import Path

        ROOT = Path(__file__).resolve().parent
        VERSION_FILE = ROOT / "VERSION"

        REQUIRED_PATHS = (
            "README.md",
            "CHANGELOG.md",
            "ROADMAP.md",
            "CONTRIBUTING.md",
            "CODE_OF_CONDUCT.md",
            "VERSION",
            "docs",
            "prompts",
            "examples",
            "releases",
            "tests",
            "templates",
            ".github",
        )


        def version() -> str:
            try:
                return VERSION_FILE.read_text(encoding="utf-8").strip()
            except OSError:
                return "unknown"


        def show_status(_: argparse.Namespace) -> int:
            print("Ramrattan AI Editorial Studio")
            print(f"Version: {version()}")
            print("Sprint: Sprint 1 - The Foundation")
            print("Status: Release candidate")
            return 0


        def show_version(_: argparse.Namespace) -> int:
            print(version())
            return 0


        def show_structure(_: argparse.Namespace) -> int:
            for relative in REQUIRED_PATHS:
                marker = "✓" if (ROOT / relative).exists() else "✗"
                print(f"{marker} {relative}")
            return 0


        def validate(_: argparse.Namespace) -> int:
            missing = [
                relative
                for relative in REQUIRED_PATHS
                if not (ROOT / relative).exists()
            ]

            if missing:
                print("Validation failed:", file=sys.stderr)
                for relative in missing:
                    print(f"  - Missing: {relative}", file=sys.stderr)
                return 1

            if version() in {"", "unknown"}:
                print("Validation failed: VERSION is unreadable.", file=sys.stderr)
                return 1

            print(f"Validation passed for v{version()}.")
            return 0


        def parser() -> argparse.ArgumentParser:
            result = argparse.ArgumentParser(
                description="Ramrattan AI Editorial Studio utilities."
            )
            commands = result.add_subparsers(dest="command", required=True)

            definitions = {
                "status": ("Display project status.", show_status),
                "version": ("Display project version.", show_version),
                "structure": ("Display required paths.", show_structure),
                "validate": ("Validate the repository.", validate),
            }

            for name, (help_text, handler) in definitions.items():
                command = commands.add_parser(name, help=help_text)
                command.set_defaults(handler=handler)

            return result


        def main() -> int:
            args = parser().parse_args()
            return int(args.handler(args))


        if __name__ == "__main__":
            raise SystemExit(main())
        '''
    ),
}


DIRECTORIES = (
    ".github/ISSUE_TEMPLATE",
    ".github/workflows",
    "assets",
    "docs/architecture/adr",
    "docs/Handoff",
    "docs/learning",
    "examples",
    "prompts",
    "releases",
    "scripts",
    "templates",
    "tests",
)

PLACEHOLDERS = (
    "assets/.gitkeep",
    "docs/learning/.gitkeep",
    "examples/.gitkeep",
    "prompts/.gitkeep",
    "releases/.gitkeep",
    "scripts/.gitkeep",
    "tests/.gitkeep",
)


class BootstrapError(RuntimeError):
    """Raised when the bootstrap cannot proceed safely."""


def run(
    command: list[str],
    *,
    cwd: Path,
    check: bool = True,
    capture: bool = False,
) -> subprocess.CompletedProcess[str]:
    """Run a command with readable output."""
    print("$", " ".join(command))
    return subprocess.run(
        command,
        cwd=cwd,
        check=check,
        text=True,
        capture_output=capture,
    )


def output(command: list[str], *, cwd: Path) -> str:
    """Run a command and return stripped stdout."""
    result = run(command, cwd=cwd, capture=True)
    return result.stdout.strip()


def repository_root() -> Path:
    """Find and validate the current Git repository."""
    try:
        root_text = output(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=Path.cwd(),
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        raise BootstrapError(
            "Run this script from inside the cloned Git repository."
        ) from exc

    root = Path(root_text).resolve()

    if root.name != EXPECTED_REPOSITORY:
        raise BootstrapError(
            f"Expected repository '{EXPECTED_REPOSITORY}', found '{root.name}'."
        )

    remote = output(["git", "remote", "get-url", "origin"], cwd=root)

    if EXPECTED_REMOTE_FRAGMENT not in remote:
        raise BootstrapError(
            "The origin remote does not match the expected GitHub repository."
        )

    return root


def current_branch(root: Path) -> str:
    return output(["git", "branch", "--show-current"], cwd=root)


def backup_working_tree(root: Path) -> Path | None:
    """Back up changed and untracked files outside the repository."""
    status = output(["git", "status", "--porcelain"], cwd=root)

    if not status:
        print("Working tree is clean. No backup is required.")
        return None

    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_root = (
        Path.home()
        / "Ramrattan_AI_Editorial_Studio_Backups"
        / timestamp
    )
    backup_root.mkdir(parents=True, exist_ok=False)

    paths: set[str] = set()

    for line in status.splitlines():
        raw_path = line[3:]

        if " -> " in raw_path:
            raw_path = raw_path.split(" -> ", 1)[1]

        paths.add(raw_path)

    for relative in sorted(paths):
        source = root / relative

        if not source.exists():
            continue

        destination = backup_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)

        if source.is_dir():
            shutil.copytree(source, destination, dirs_exist_ok=True)
        else:
            shutil.copy2(source, destination)

    print(f"Backup created: {backup_root}")
    return backup_root


def preserve_original_readme(root: Path) -> None:
    """Preserve the original README from main if not already archived."""
    destination = (
        root
        / "docs"
        / "Handoff"
        / "README_original_V1.0.0_2026-08-01.md"
    )

    if destination.exists():
        return

    destination.parent.mkdir(parents=True, exist_ok=True)

    try:
        original = output(
            ["git", "show", "main:README.md"],
            cwd=root,
        )
    except subprocess.CalledProcessError:
        original = "# Original README\n"

    destination.write_text(original + "\n", encoding="utf-8")


def create_foundation(root: Path) -> None:
    """Create and repair the Sprint 1 foundation."""
    for directory in DIRECTORIES:
        (root / directory).mkdir(parents=True, exist_ok=True)

    preserve_original_readme(root)

    for relative, content in FILES.items():
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")
        print(f"Wrote {relative}")

    for relative in PLACEHOLDERS:
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.touch(exist_ok=True)

    studio = root / "studio.py"
    studio.chmod(studio.stat().st_mode | 0o111)


def validate_foundation(root: Path) -> None:
    """Validate required foundation files and commands."""
    required = list(FILES) + list(PLACEHOLDERS)

    missing = [
        relative
        for relative in required
        if not (root / relative).exists()
    ]

    if missing:
        formatted = "\n".join(f"  - {item}" for item in missing)
        raise BootstrapError(
            f"Foundation validation failed. Missing:\n{formatted}"
        )

    for relative, expected in FILES.items():
        actual = (root / relative).read_text(encoding="utf-8")

        if actual != expected:
            raise BootstrapError(
                f"Content validation failed for {relative}."
            )

    run([sys.executable, "studio.py", "status"], cwd=root)
    run([sys.executable, "studio.py", "structure"], cwd=root)
    run([sys.executable, "studio.py", "validate"], cwd=root)

    print("Foundation validation passed.")


def publish(root: Path) -> None:
    """Commit, push, and create the pull request."""
    branch = current_branch(root)

    if branch != FEATURE_BRANCH:
        raise BootstrapError(
            f"Publishing requires branch '{FEATURE_BRANCH}', "
            f"but the current branch is '{branch}'."
        )

    run(["gh", "auth", "status"], cwd=root)
    run(["git", "add", "."], cwd=root)

    staged = output(["git", "diff", "--cached", "--name-only"], cwd=root)

    if not staged:
        print("There are no staged changes to commit.")
        return

    run(
        [
            "git",
            "commit",
            "-m",
            "feat: establish the foundation for "
            "Ramrattan AI Editorial Studio",
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
        print(f"Pull request already exists: {existing.stdout.strip()}")
        return

    body = clean(
        """
        ## Summary

        Establishes the initial engineering and documentation foundation
        for Ramrattan AI Editorial Studio.

        ## Changes

        - Adds the flagship README
        - Adds the project charter
        - Adds the changelog and roadmap
        - Adds semantic version tracking
        - Adds ADR-000 and the ADR framework
        - Adds the initial `studio.py` CLI
        - Adds GitHub issue and pull request templates
        - Adds repository validation through GitHub Actions
        - Preserves the original README

        ## Validation

        - `python3 studio.py status`
        - `python3 studio.py structure`
        - `python3 studio.py validate`

        ## Rollback

        Close the pull request without merging, or revert the foundation
        commit after merge.
        """
    )

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
            "PR-001: Establish the repository foundation",
            "--body",
            body,
        ],
        cwd=root,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the Sprint 1 repository foundation."
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Commit, push, and open the pull request after validation.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        root = repository_root()
        branch = current_branch(root)

        print(f"Repository: {root}")
        print(f"Branch: {branch}")

        if branch != FEATURE_BRANCH:
            raise BootstrapError(
                f"Switch to '{FEATURE_BRANCH}' before running the script."
            )

        backup_working_tree(root)
        create_foundation(root)
        validate_foundation(root)

        print("\nGit status:")
        run(["git", "status", "--short"], cwd=root)

        print("\nChange summary:")
        run(["git", "diff", "--stat"], cwd=root)

        if args.publish:
            publish(root)
        else:
            print(
                "\nFoundation created and validated, but not published."
            )
            print(
                "Review the files in VS Code, then run:\n"
                "  python3 bootstrap_foundation.py --publish"
            )

        return 0

    except BootstrapError as exc:
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