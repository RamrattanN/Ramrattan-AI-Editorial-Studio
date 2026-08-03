# Current Product Focus

## Status

Active product direction as of 2026-08-01.

## Product Definition

Ramrattan AI Editorial Studio is an adaptive editorial operating
system for developing publication-ready professional articles and
their supporting 720 × 425 Hero Visuals.

## Primary Outcome

The primary outcome is an article publication package containing:

- Hero Visual - 720 × 425
- Headline
- Publication-ready article
- Source attribution
- Practical takeaway
- Call to action
- Hashtags
- LinkedIn description
- Relevant publication metadata

## Time-to-Value Target

When sufficient material is available, the Studio should aim to
produce the first publication-ready package within approximately
10 minutes of the Author's original specification.

This is a product target, not permission to sacrifice editorial
quality.

## Sufficient Starting Material

A starting point is sufficient when it provides enough information
to establish at least:

- a meaningful topic,
- a plausible Author intent,
- and a path to defensible evidence or experience.

Examples include:

- A reputable URL
- Copied source material
- A headline plus Author perspective
- A news recollection that can be researched
- A professional observation with relevant detail
- Notes or a draft containing a discernible argument
- Multiple partial inputs that become sufficient together

## Insufficient Starting Material

Material is insufficient when it cannot support a distinctive,
defensible article without inventing facts, intent, or expertise.

The Studio should not produce generic filler.

It should respond with:

1. A concise explanation of the limitation.
2. The specific information that is missing.
3. An example of an improved starting point.
4. One clear next action.

## Active Capabilities

1. Adaptive Editorial Context
2. Article Engine
3. Hero Visual
4. Author Library
5. Editorial Intelligence
6. Evidence and Research
7. Platform Services

## Current Scope

Included:

- Professional articles
- LinkedIn-oriented publication packages
- 720 × 425 Hero Visuals
- Adaptive Author input
- Evidence and attribution
- Revision and context preservation
- Local-first Author Library planning

Excluded from current scope:

- Carousels
- Social-media threads
- Video scripts
- Podcast scripts
- General marketing-content suites
- Cloud collaboration
- Multi-tenant storage
- Automatic direct publishing

## Relationship Between Context and Library

The Editorial Context is the active workspace.

The Author Library stores paused or completed work so it can be
recalled, reviewed, resumed, revised, exported, archived, restored,
or deleted.

Author work is private by default.

The Library supports the creation process. It does not replace it.

<!-- CAPABILITY_005_CURRENT_FOCUS_START -->

## Capability 5 - Current Architecture Direction

The Adaptive Editorial Context is the system kernel.

The Studio continuously interprets Author contributions and updates
a shared representation of:

- intent,
- sources,
- durable source context,
- evidence,
- Author perspective,
- thesis,
- article state,
- Hero Visual state,
- integrity,
- readiness,
- and revision history.

The Studio is stateless by default.

Project continuity is provided through Portable Editorial Projects
owned and stored by the Author.

The Product does not request or rely on storage paths.

Each project may be exported as a small Markdown file using:

```text
Ramrattan-Editorial-Project_<Article-Slug>_YYYY.MM.DDvNN.md
```

Generated filenames must not exceed 255 characters.

The opening experience supports:

- Start a New Editorial Project
- Resume an Existing Editorial Project

The Author may download or copy:

- the article,
- the Hero Visual,
- the Portable Editorial Project,
- or an optional ZIP package.

The project preserves enough source context to remain useful when
URLs expire or paywalled material becomes inaccessible.

Editorial Integrity is a first-class component.

<!-- CAPABILITY_005_CURRENT_FOCUS_END -->

<!-- CAPABILITY_006_CURRENT_FOCUS_START -->

## Capability 006 and Version 1.0 Focus

The current product priority is implementing the complete Version
1.0 Author journey.

The active foundations are:

- Editorial Integrity Pipeline
- Adaptive Editorial Context
- Article Engine
- Hero Visual System
- Publication Package Contract
- Portable Editorial Projects
- Resume Existing Project
- Export Publication Package

Version 1.0 is article-first.

Carousels, hosted storage, team collaboration, direct publishing,
and analytics remain outside the Version 1.0 scope.

<!-- CAPABILITY_006_CURRENT_FOCUS_END -->

<!-- CAPABILITY_006A_CURRENT_FOCUS_START -->

## Constitutional Freeze

Version 0.9 establishes the constitutional foundation for Version
1.0 implementation.

The current governing documents define:

- trust-first product design,
- the Author, Editor, and Reader relationship,
- Editorial Confidence,
- component-based collaboration,
- Reader Experience Principles,
- Editorial Language Framework,
- Editorial Fingerprint,
- and the Canonical Editorial Session.

After this freeze, Capabilities 007-011 focus on implementation.

<!-- CAPABILITY_006A_CURRENT_FOCUS_END -->

<!-- CAPABILITY_007_CURRENT_FOCUS_START -->

## Capability 007 Active Focus

The current implementation focus is the beginning of the Canonical
Editorial Session:

- Editorial Workspace welcome experience
- Natural Editorial Intake
- Understanding your input
- Assessing your sources
- Optional identity assets
- Rights confirmation
- Brand-neutral defaults
- Resume without missing assets

Full evidence verification remains Capability 008.

<!-- CAPABILITY_007_CURRENT_FOCUS_END -->

<!-- CAPABILITY_008_CURRENT_FOCUS_START -->

## Capability 008 Active Focus

The current Product focus is Editorial Discernment:

- interpret each new Author contribution,
- preserve one coherent Editorial Intent,
- accept related supporting material,
- detect separate publication objectives,
- prevent silent scope expansion,
- protect approved work,
- and manage the Editorial Session lifecycle.

Evidence-validation depth remains part of Capability 008's next
implementation increment.

<!-- CAPABILITY_008_CURRENT_FOCUS_END -->

<!-- CAPABILITY_008A1_CURRENT_FOCUS_START -->

## Current Implementation Status - Capability 008A.1

- Capability 008 - Complete
- Capability 008A.1 - Governance Consolidation - In Progress
- Capability 008A.2 - Delivery Hardening - Not started
- Capability 008A.3 - Editorial Integrity Hardening - Not started
- Capability 009 - Not started

The active engineering focus is Governance Consolidation. Product runtime
remains at the completed Capability 008 baseline while governance
authority, current status, and historical reference integrity are hardened.

Earlier capability focus sections are delivery records. This section owns
the current implementation status until the next increment updates it.

<!-- CAPABILITY_008A1_CURRENT_FOCUS_END -->

<!-- CAPABILITY_008A2_CURRENT_FOCUS_START -->

## Current Implementation Status - Capability 008A.2

- Capability 008 - Complete
- Capability 008A.1 - Governance Consolidation - Complete
- Capability 008A.2 - Delivery Hardening - In Progress
- Capability 008A.3 - Editorial Integrity Hardening - Todo
- Capability 009 - Todo

The active engineering focus is fail-closed capability delivery under
ADR-012. Product runtime remains at Capability 008. Evidence Validation,
StageState, and publication behavior do not change in this increment.

Architecture Baseline `2026.08.01v07` records the hardened delivery
architecture. Earlier focus sections remain delivery history.

<!-- CAPABILITY_008A2_CURRENT_FOCUS_END -->

<!-- CAPABILITY_008A3_CURRENT_FOCUS_START -->

## Current Engineering Hardening Increment - Capability 008A.3

Capability 008A.1 Governance Consolidation and Capability 008A.2 Delivery
Hardening are complete. Capability 008A.3 Editorial Integrity Hardening is in
progress. Capability 009 remains Todo and has not started.

This increment corrects evidence certainty, source independence,
contradiction-to-risk behavior, publication blocking, Author-facing Editorial
Confidence translation, and canonical StageState ownership. It does not add an
Article Engine, Publication Package, Component Collaboration, Hero Visual,
Portable Project, real ingestion, UI, or release behavior.

ADR-013 records the durable decision. Architecture Baseline
`2026.08.01v08` becomes current when Capability 008A.3 is delivered; baseline
`2026.08.01v07` remains the merged baseline during implementation.

<!-- CAPABILITY_008A3_CURRENT_FOCUS_END -->

<!-- CAPABILITY_009_CURRENT_FOCUS_START -->

## Capability 009 Scope Clarification

Capability 009 is the active product capability and implements only
the Article Engine and textual Publication Package.

The Article Engine consumes explicit Author-owned inputs and completed
Editorial Integrity results. The package includes the article and its
required textual publication components while preserving Editorial
Confidence and publication blocking.

Integrated Editorial Workspace, Adaptive Editorial Context runtime,
Component Collaboration, stable Author-facing orchestration API, and
final integrated Editorial Confidence presentation remain deferred.
Rendered Hero Visual remains Capability 010. Portable Editorial Project
behavior remains Capability 011.

<!-- CAPABILITY_009_CURRENT_FOCUS_END -->

<!-- RC1_CHECKPOINT_CURRENT_STATUS_START -->

## RC1 Checkpoint - Current Product Status

Capability 009 is complete.

Capability 010 is complete. The Article Engine, Publication Package, and Hero
Visual System are delivered under ADR-015, ADR-016, and baseline
`2026.08.02v12`.

Capability 011 is active and In Progress under issue #17. B002 remains
deferred, Low Priority, Post-RC1, and non-blocking. Version 1 is not
release-ready until the Portable Project and end-to-end release-readiness work
in issue #18 is complete.

<!-- RC1_CHECKPOINT_CURRENT_STATUS_END -->

<!-- CAPABILITY_010_CURRENT_FOCUS_START -->

## Capability 010 Delivered State

Capability 010 delivered the provider-independent Hero Visual System for the
existing Capability 009 Publication Package. It consumes the approved prompt,
preserves visual intent, validates a 720 × 425 PNG and its provenance, and
returns explicit safe failure states when generation cannot be trusted.

The Publication Package integration attaches one existing result without
regenerating approved article content. PR #46 is merged, issue #16 is closed,
ADR-016 is Accepted, and baseline `2026.08.02v12` is current. Capability 011 is
Next, Todo, and unstarted. B002 remains deferred, Low Priority, Post-RC1, and
non-blocking.

No Portable Project, workspace, collaboration, orchestration, UI, publishing
automation, release packaging, or Version 2 behavior is part of this focus.

<!-- CAPABILITY_010_CURRENT_FOCUS_END -->

<!-- CAPABILITY_011_CURRENT_FOCUS_START -->

## Capability 011 Active State

Capability 011 implements the narrow RC1 Portable Editorial Project using only
state supplied by the current Article Engine, Hero Visual, Publication Package,
and Editorial Session runtimes. ADR-017 and proposed baseline
`2026.08.02v13` govern the implementation.

The richer legacy schema remains documentation of future product direction;
unsupported Author profiles, Adaptive Editorial Context, rich sources,
publication history, collaboration, workspace, orchestration, UI, and Version
2 state are not fabricated. Issue #18 and B002 remain unchanged.

<!-- CAPABILITY_011_CURRENT_FOCUS_END -->
