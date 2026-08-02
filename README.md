# Ramrattan AI Editorial Studio

> **Engineering AI-assisted thought leadership with the discipline
> of software development.**

Ramrattan AI Editorial Studio is an adaptive editorial operating
system that helps Authors transform evolving ideas, evidence,
expertise, and perspective into publication-ready professional
articles.

**The Studio adapts to the Author's creative process - never the
other way around.**

## Current Product Focus

The current product creates one complete article publication
package:

- A publication-ready professional article
- A 720 × 425 Hero Visual
- A strong headline
- A clear opening hook
- Evidence-supported insights
- A practical takeaway
- Source attribution
- A pointed call to action
- Relevant hashtags
- A concise LinkedIn description

The Hero Visual may also be described informally as an infographic.
In the product architecture, **Hero Visual** is the standard term.

## Author Starting Points

Authors may begin naturally with:

- one or more URLs,
- copied source material,
- a headline,
- a topic,
- something seen in the news,
- a personal observation,
- a developed perspective,
- rough notes,
- an incomplete idea,
- a previous draft,
- or any useful combination.

The Studio interprets what is happening before imposing structure.

## Product Promise

When the Author provides sufficient material, the Studio should aim
to produce a publication-ready first draft and Hero Visual within
approximately 10 minutes.

Speed does not override quality, originality, evidence, or Author
control.

## Insufficient Starting Material

The Studio must not manufacture confidence from a weak foundation.

When the starting material cannot support a distinctive,
defensible article, the Studio should:

1. Explain specifically why the material is insufficient.
2. Identify what is missing.
3. Show an example of a stronger starting point.
4. Offer the smallest useful next action.

A constructive response is better than generating generic or
unsupported content.

## Core Product Capabilities

```text
Ramrattan AI Editorial Studio
├── Adaptive Editorial Context
├── Article Engine
│   ├── Headline
│   ├── Hero Visual - 720 × 425
│   ├── Article
│   ├── Source Attribution
│   └── Publication Package
├── Author Library
├── Editorial Intelligence
├── Evidence and Research
└── Platform Services
```

## Adaptive Editorial Context

The Editorial Context is the active workspace while an article is
being developed.

It may contain:

- Author intent
- Source material
- Author perspective
- Research
- Evidence
- Candidate angles
- Current thesis
- Constraints
- Article structure
- Hero Visual concepts
- Draft assets
- Decisions
- Revisions
- Publication readiness

The Author may change direction at any time. The Studio preserves
useful work and updates only affected components where practical.

## Author Library

The Author Library stores paused and completed editorial work.

It should eventually support:

- Save
- Recall
- Review
- Resume
- Revise
- Duplicate
- Archive
- Restore
- Export
- Delete

Author work is private by default.

## Current Scope Boundary

The present product is focused on professional articles and their
Hero Visuals.

Carousels and other publishing formats are not part of the active
product scope.

Historical workflow code may still contain earlier carousel
concepts. Those remain only for traceability until the adaptive
architecture replaces the prototype.

## Product Documentation

Begin here:

1. [Current Product Focus](docs/product/Current_Product_Focus.md)
2. [PRD v1.1](docs/product/PRD_v1.1.md)
3. [Product Constitution](docs/product/Constitution.md)
4. [Product Principles](docs/product/Product_Principles.md)
5. [Studio Contract](docs/product/Studio_Contract.md)
6. [Adaptive Editorial Model](docs/product/Adaptive_Editorial_Model.md)
7. [Author Journey](docs/product/Author_Journey.md)
8. [Product Glossary](docs/product/Glossary.md)
9. [Product Decision Log](docs/product/Decision_Log.md)

PRD v1.0 remains available as a historical product baseline.

## Architecture Status

The existing `studio.workflow` package is a historical linear
workflow prototype.

The target architecture is an adaptive Editorial Context shared by
the Article Engine, Hero Visual capability, Author Library,
Evidence Engine, and Editorial Intelligence.

## Validation

```bash
python3 -m compileall -q studio tests
python3 -m unittest discover -s tests -v
python3 studio.py validate
```

## License

This project is licensed under the MIT License.

---

**The Author owns the idea. The Studio helps make it publishable.**

<!-- CAPABILITY_005_README_START -->

## Capability 5 - Adaptive Editorial Context

The Adaptive Editorial Context is the working memory of the Studio.

It interprets natural Author contributions and preserves:

- intent,
- sources,
- durable source context,
- evidence,
- perspective,
- thesis,
- article state,
- Hero Visual state,
- integrity,
- readiness,
- and meaningful revision history.

The Author does not need to select a workflow mode.

## Portable Editorial Projects

The Studio is stateless by default.

Authors can save a small project file containing the context needed
to resume later.

Project files use:

```text
Ramrattan-Editorial-Project_<Article-Slug>_YYYY.MM.DDvNN.md
```

Filenames never exceed 255 characters.

Authors may:

- download or copy the article,
- download or copy the Hero Visual,
- download the Portable Editorial Project,
- or export an optional ZIP.

The Author chooses where files are stored.

The Product does not request or depend on storage paths.

## Durable Source Context

URLs may expire, change, or become inaccessible.

The project preserves:

- citation metadata,
- concise source summaries,
- key claims,
- statistics used,
- Author interpretation,
- verification notes,
- and editorial significance.

Paywalled material is preserved selectively.

The complete source is not automatically archived.

## Resume Existing Project

A future opening experience will support:

- Start a New Editorial Project
- Resume an Existing Editorial Project

Resume validates and restores the saved context without requiring
the Author to reconstruct previous work.

## Editorial Integrity

The Studio evaluates:

- source quality,
- evidence support,
- attribution,
- uncertainty,
- originality,
- privacy,
- safety,
- professional conduct,
- and publication blockers.

<!-- CAPABILITY_005_README_END -->

<!-- CAPABILITY_006_README_START -->

## Capability 006 - Editorial Integrity

Every publication project passes through five visible stages:

1. Understanding your input
2. Assessing your sources
3. Verifying the evidence
4. Reviewing editorial risks
5. Creating your publication package

Editorial Risk uses:

- Low
- Moderate
- High
- Severe

The Studio does not knowingly disseminate materially false,
fabricated, deceptive, or dangerously misleading information.

## Version 1.0 Target

Version 1.0 delivers:

- article-first editorial intake,
- fact and evidence validation,
- Adaptive Editorial Context,
- 720 × 425 Hero Visual,
- complete Publication Package,
- focused component revision,
- Portable Editorial Projects,
- Resume Existing Project,
- and export-first completion.

Carousel generation is not part of Version 1.0.

See:

- `docs/product/Product_Vision.md`
- `docs/product/Release_v1.0.md`
- `docs/product/PRD_v1.3.md`
- `docs/architecture/Editorial_Integrity_Pipeline.md`
- `docs/architecture/Publication_Package_Contract.md`

<!-- CAPABILITY_006_README_END -->

<!-- CAPABILITY_006A_README_START -->

## Constitutional Layer

Version 0.9 establishes a Constitutional Layer above Product,
Architecture, Implementation, and Tests.

Begin with:

- `docs/START_HERE.md`
- `docs/constitution/Constitution.md`
- `docs/constitution/Human_Collaboration_Model.md`
- `docs/constitution/Canonical_Editorial_Session.md`

The governing relationship is:

- Author - owns intent and publication authority
- Editor - provides editorial judgement
- Reader - receives work whose trust must be earned

Editorial Risk remains an internal LMHS assessment.

Editorial Confidence is the primary Author-facing outcome.

Motto:

> Trust earned. Confidence shared. Conversations inspired.

<!-- CAPABILITY_006A_README_END -->

<!-- CAPABILITY_007_README_START -->

## Capability 007 - Editorial Workspace Runtime

Capability 007 begins Version 1.0 runtime implementation.

The Editorial Workspace now supports:

- natural input recognition,
- Stage 1 - Understanding your input,
- Stage 2 - Assessing your sources,
- optional logo and headshot identity assets,
- rights confirmation,
- and brand-neutral Hero Visual defaults.

Editorial Workspace is the complete Author-facing environment.

Editorial Intake is the first capability within that Workspace.

Canonical terminology is defined in:

- `docs/constitution/Canonical_Vocabulary.md`

<!-- CAPABILITY_007_README_END -->

<!-- CAPABILITY_DELIVERY_README_START -->

## Capability Delivery

Repository capabilities use a state-aware, repeatable delivery
workflow.

Read:

- `docs/engineering/Capability_Delivery_Workflow.md`

Inspect the next safe action with:

```bash
python3 scripts/capability_delivery.py \
  --branch "feature/example" \
  --commit-message "feat: implement example" \
  --pr-title "Example: Implement capability"
```

The helper resolves branch and pull-request state before suggesting
the next command.

<!-- CAPABILITY_DELIVERY_README_END -->
