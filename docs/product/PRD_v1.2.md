# Product Requirements Document - Version 1.2

## Product

Ramrattan AI Editorial Studio

## Status

Active Capability 5 product baseline.

## Supersedes

PRD v1.1 as the active product definition.

Earlier PRDs remain preserved as historical product records.

## North Star

> Ramrattan AI Editorial Studio is an adaptive editorial operating
> system that helps Authors transform evolving ideas, evidence,
> expertise, and perspective into publication-ready professional
> articles.

> The Studio adapts to the Author's creative process - never the
> other way around.

## Primary Product Outcome

The Studio produces a publication-ready article package containing:

- Hero Visual - 720 × 425
- Headline
- Publication-ready article
- Source attribution
- Practical takeaway
- Call to action
- Hashtags
- LinkedIn description
- Publication metadata
- Portable Editorial Project

## Time-to-Value

When sufficient starting material exists, the Studio should aim to
produce the first publication-ready package within approximately
10 minutes.

The Author experience must not become laborious or questionnaire
driven.

## Adaptive Editorial Context

The Adaptive Editorial Context is the system kernel.

It must:

- exist before the first draft,
- support first-pass generation,
- support focused revision,
- preserve version history,
- support changes of direction,
- assess readiness,
- track Editorial Integrity,
- preserve durable source context,
- and serialize into a Portable Editorial Project.

## Natural Author Input

The Author may begin or continue with:

- URLs,
- pasted material,
- paywalled excerpts,
- headlines,
- observations,
- news recollections,
- perspectives,
- notes,
- drafts,
- corrections,
- publication links,
- or compatible Portable Editorial Projects.

The Author is not required to classify the contribution.

## Progressive Clarification

The Studio should infer before asking.

It should ask one focused question only when ambiguity materially
blocks:

- accuracy,
- distinctiveness,
- ethical publication,
- or the Author's intended direction.

## Portable Editorial Projects

The Studio is stateless by default.

The Author may export a small, human-readable project file that
preserves enough context to resume the work later.

The Author chooses where the project is stored.

The Product must not require or depend on the storage path.

## Resume Existing Project

Resume Existing Project is a first-class opening action.

The Studio must:

- validate the project file,
- identify the project and version,
- restore compatible context,
- explain missing optional assets,
- summarize the last known state,
- identify unresolved integrity issues,
- and continue without unnecessary re-entry.

## File Naming and VCM

Project files use:

```text
Ramrattan-Editorial-Project_<Article-Slug>_YYYY.MM.DDvNN.md
```

The VCM identifier uses:

```text
YYYY.MM.DDvNN
```

Requirements:

- maximum filename length of 255 characters,
- no silent overwrite,
- daily sequencing from `v01`,
- preserved version suffix,
- readable slug,
- and collision protection when truncation is required.

## Download and Copy Options

The Product should support appropriate combinations of:

- Download Portable Editorial Project
- Download Article
- Copy Article
- Download Hero Visual
- Copy Hero Visual
- Export ZIP

The Studio should explain the future value of saving the Portable
Editorial Project.

## Durable Source Context

The Project must remain understandable when a source URL:

- expires,
- moves,
- changes,
- becomes inaccessible,
- or becomes paywalled.

It should preserve:

- citation metadata,
- concise source summary,
- key claims,
- statistics used,
- Author interpretation,
- editorial role,
- verification status,
- and limited essential excerpts.

## Paywalled Material

When an Author supplies copied material from a paywalled source,
the Studio should preserve enough editorial context to resume the
project later.

It should not automatically retain the complete source.

It should clearly record:

- that the complete source was not retained,
- that future access may be limited,
- and that reverification may be needed.

## Publication URLs

LinkedIn, Facebook, or other public URLs may be stored as optional
metadata.

They are not required for resumption.

The Project must remain useful when the URL was never supplied or
later becomes unavailable.

## Reuse

A resumed project may support:

- article revision,
- Hero Visual revision,
- publication-link updates,
- follow-up articles,
- project duplication,
- evidence review,
- or continuation of unfinished work.

Reuse must not silently carry unsupported or outdated claims into
new work.

## Editorial Integrity

Editorial Integrity is a first-class component.

The Studio must assess:

- harmful intent,
- source quality,
- attribution,
- evidence support,
- uncertainty,
- originality,
- privacy,
- professional conduct,
- and publication blockers.

## Source Quality

Disreputable or weak sources must not silently become the factual
foundation of an article.

The Studio should explain source-quality concerns and help the
Author find stronger support where appropriate.

## Harmful Requests

The Studio should not assist with article projects intended to:

- cause harm,
- facilitate illegality,
- deceive,
- harass,
- defame through unsupported allegations,
- reveal private information improperly,
- impersonate,
- defraud,
- or deliberately spread false information.

## Author Ownership

The Author owns:

- the project,
- the ideas,
- the article,
- the Hero Visual,
- the project file,
- and the publication decision.

## Non-Goals

The current product does not require:

- hosted Author storage,
- user accounts,
- cloud synchronization,
- reported file paths,
- collaboration workspaces,
- a multi-tenant database,
- carousel generation,
- or automatic direct publishing.

## Success Measures

- Time to first publication-ready package
- Author confidence to publish
- Low-friction interaction
- Perspective preservation
- Evidence quality
- Originality
- Editorial Integrity
- Successful focused revision
- Successful project export
- Successful project resumption
- Resilience to expired URLs
- Responsible handling of paywalled excerpts
- Author-controlled storage
