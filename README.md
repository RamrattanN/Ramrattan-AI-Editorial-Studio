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
