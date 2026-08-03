# Changelog

<!-- CAPABILITY_011_CHANGELOG_START -->

### Added - Capability 011 (In Progress)

- Narrow RC1 Portable Editorial Project schema and Markdown round trip
- Versioned Configuration Management filenames with bounded safe slugs
- Validated resume with mandatory Temporal Integrity review
- Article, Hero Visual, project, and deterministic optional ZIP downloads
- Narrow Publication Package project attachment
- ADR-017 and proposed Architecture Baseline 2026.08.02v13

<!-- CAPABILITY_011_CHANGELOG_END -->

All notable changes to Ramrattan AI Editorial Studio are documented here.

## [Unreleased]

### Added - PR-004 Article-First Product Alignment

- Current Product Focus document
- Product Requirements Document v1.1
- Article-first publication-package definition
- Hero Visual terminology and 720 × 425 specification
- Ten-minute time-to-value target
- Constructive insufficient-input behaviour
- Author Library terminology
- ADR-003 - Adopt an Article-First Publication Package
- Article-first alignment tests

### Changed - PR-004 Article-First Product Alignment

- Narrowed the active product scope to professional articles
- Removed carousels from the active product roadmap
- Defined the Hero Visual as part of the article publication package
- Reframed the Author Library as supporting paused and completed work
- Clarified that the existing linear workflow is a historical prototype
- Established Author confidence to publish as the primary usefulness measure


### Added - Sprint 2 Editorial Workflow System

- Explicit editorial workflow state machine
- Serializable editorial session state
- Centralized selectable user choices
- Back and restart navigation
- Dependency-aware downstream resets
- Hero-copy validation
- Unit tests for workflow behavior
- ADR-001 - The Workflow Is the Product


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

<!-- CAPABILITY_005_CHANGELOG_START -->

### Added - Capability 5 Architecture Baseline

- Adaptive Editorial Context Model
- Portable Editorial Project Specification
- Editorial Integrity Charter
- Capability Definition of Done
- Capability 5 Demo
- PRD v1.2
- ADR-004 - Adopt Portable Editorial Projects
- VCM project filename standard
- 255-character filename maximum
- Resume Existing Project experience
- Download and copy output model
- Durable source context
- Expired URL resilience
- Paywalled excerpt handling
- Optional project ZIP concept
- Capability architecture tests

### Changed - Capability 5 Architecture Baseline

- Replaced the hosted Author Library direction with Author-owned
  Portable Editorial Projects
- Established the Studio as stateless by default
- Removed external file-path dependency
- Made publication URLs optional metadata
- Required preservation of source meaning beyond the URL
- Defined selective retention for paywalled material
- Made Editorial Integrity a first-class context component
- Established Capability Demos as part of completion

<!-- CAPABILITY_005_CHANGELOG_END -->

<!-- CAPABILITY_006_CHANGELOG_START -->

### Added - Capability 006

- Editorial Integrity Pipeline
- Editorial Judgment Framework
- Editorial Collaboration Model
- Publication Package Contract
- Editorial Philosophy
- Product Vision
- Version 1.0 Product Release Definition
- PRD v1.3
- ADR-005
- LMHS Editorial Risk
- Five visible processing stages
- Progressive Recovery
- Temporal Integrity
- Curated three-option interaction contract
- Intelligent dependency management
- Export-first completion UX
- Architecture Baseline 2026.08.01v01
- Capability 006 demo
- Capability 006 validation tests

### Changed - Capability 006

- Defined Version 1.0 scope and exclusions
- Made fact and evidence review mandatory before publication
  recommendation
- Added host-compatible document, audio, and video intake
- Made Export the primary completion action
- Required Author approval before related component regeneration
- Required concise, consolidated editorial observations
- Added VCM versioning for architecture baselines

<!-- CAPABILITY_006_CHANGELOG_END -->

<!-- CAPABILITY_006A_CHANGELOG_START -->

## Version 0.9 - Constitutional Freeze

### Added

- Constitutional documentation layer
- START_HERE repository entry point
- Constitution 2026.08.01v01
- Product Philosophy
- Human Collaboration Model
- Author Journey
- Editor Journey
- Editor Charter
- Reader Experience Principles
- Editorial Behaviour Standard
- Editorial Language Framework
- Editorial Fingerprint
- Canonical Editorial Session
- Constitutional Decision Register
- ADR-006
- Architecture Baseline 2026.08.01v02
- Version 1.0 Scorecard
- Constitutional validation tests

### Changed

- Adopted Editorial Confidence as the primary Author-facing outcome
- Retained LMHS Editorial Risk as the internal assessment
- Generalized revision to all Publication Package components
- Required permission before dependent-component regeneration
- Established naturally varied CTA and conversation invitation
  language
- Established Constitutional Impact Review
- Froze foundational philosophy for Version 1.0 implementation

### Motto

> Trust earned. Confidence shared. Conversations inspired.

<!-- CAPABILITY_006A_CHANGELOG_END -->

<!-- CAPABILITY_007_CHANGELOG_START -->

## Capability 007 - Editorial Workspace Runtime

### Added

- Canonical Vocabulary
- Editorial Workspace runtime
- Editorial Intake runtime
- Natural input recognition
- Initial source assessment
- Stage 1 - Understanding your input
- Stage 2 - Assessing your sources
- Optional logo identity asset
- Optional headshot identity asset
- Identity-asset rights confirmation
- Resume guidance for missing identity assets
- ADR-007
- Architecture Baseline 2026.08.01v03
- Runtime tests
- Capability 007 demo

### Changed

- Established Editorial Workspace as the complete Author-facing
  environment
- Established Editorial Intake as the first Workspace capability
- Preserved brand-neutral Hero Visual creation as the default
- Clarified that source assessment does not equal evidence
  verification
- Added canonical vocabulary governance

<!-- CAPABILITY_007_CHANGELOG_END -->

<!-- CAPABILITY_DELIVERY_CHANGELOG_START -->

## Engineering - Capability Delivery Workflow

### Added

- Capability Delivery Workflow documentation
- State-aware capability delivery helper
- Existing-branch detection
- Exact command resolution
- Pull-request discovery
- CI-state inspection
- Resolved merge command generation
- Return-to-`develop` completion standard
- Capability delivery tests
- ADR-008
- Architecture Baseline 2026.08.01v04
- Capability delivery demo

### Changed

- Capability completion now requires a clean, current `develop`
  baseline after merge
- Known values must replace command placeholders
- Bootstrap recovery must permit expected partial-apply changes
- GitHub issue and Project synchronization must be idempotent
- CI must pass before merge

<!-- CAPABILITY_DELIVERY_CHANGELOG_END -->

<!-- CAPABILITY_008_CHANGELOG_START -->

## Capability 008 - Editorial Discernment and Evidence Validation

### Added

- Editorial Discernment Engine and Editorial Guidance
- Editorial Intent, Intent Alignment, and Editorial Coherence Guard
- Workspace and Stage lifecycle
- approved-component protection and one-question clarification
- Claim Classification and Evidence Validation runtime
- Independent corroboration and contradiction handling
- Temporal Integrity review
- LMHS Editorial Risk and Editorial Confidence translation
- Architecture Baseline 2026.08.01v06 and ADR-010
- Behavioural and documentation tests

### Changed

- Separate publication objectives are no longer silently merged
- Workspace State and Stage State are distinct
- Aborted sessions preserve work, provenance, and approvals
- High and Severe Editorial Risk now block publication recommendation

<!-- CAPABILITY_008_CHANGELOG_END -->

<!-- CAPABILITY_009_CHANGELOG_START -->

### Added - Capability 009

- Provider-independent Article Engine
- Evidence and attribution validation before generation
- Editorial Intent preservation
- High and Severe publication blocking
- Textual Publication Package assembly
- Explicit Capability 010 and Capability 011 deferrals
- ADR-015 and Architecture Baseline 2026.08.02v10
- Capability 009 behavioral, documentation, and demo coverage

<!-- CAPABILITY_009_CHANGELOG_END -->

<!-- CAPABILITY_010_CHANGELOG_START -->

### Added - Capability 010

- Provider-independent Hero Visual System
- Validated 720 × 425 PNG output contract
- Offline deterministic Hero Visual provider
- Explicit generation, validation, provider, request, and policy states
- Narrow Publication Package Hero Visual attachment boundary
- Approved prompt and textual-component preservation
- ADR-016 and proposed Architecture Baseline 2026.08.02v12
- Capability 010 behavioral, documentation, and demo coverage

<!-- CAPABILITY_010_CHANGELOG_END -->
