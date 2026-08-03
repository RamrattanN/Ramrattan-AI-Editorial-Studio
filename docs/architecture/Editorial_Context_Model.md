# Adaptive Editorial Context Model

## Status

Active architecture baseline for Capability 5.

## Purpose

The Adaptive Editorial Context is the working memory of Ramrattan
AI Editorial Studio.

It represents what the Studio currently understands about one
Author-led article project.

It exists:

- before the first article draft,
- during first-pass generation,
- during review and refinement,
- during Hero Visual development,
- before publication,
- after publication,
- and when a saved project is resumed later.

## Core Principle

> The Studio continuously interprets Author contributions, updates
> a shared Editorial Context, and determines the most useful next
> editorial action.

The Author does not need to select a rigid workflow mode.

## Author Experience

The Context must reduce cognitive load.

It must not become a questionnaire, wizard, or laborious intake
form.

The Studio should:

1. infer before asking,
2. preserve creative momentum,
3. ask only focused questions,
4. retain useful context,
5. preserve unaffected approved work,
6. explain significant recommendations,
7. remain reversible,
8. and aim for a publication-ready first pass quickly.

## Natural Contributions

The Author may contribute:

- a URL,
- copied source material,
- a headline,
- a topic,
- something remembered from the news,
- a personal observation,
- professional experience,
- a perspective,
- a correction,
- a draft,
- a revision request,
- a publication URL,
- or a previously saved Portable Editorial Project.

The Author does not need to label the contribution.

## Context Components

```text
Adaptive Editorial Context
├── Project Identity
├── Author Intent
├── Inputs
├── Sources
├── Durable Source Context
├── Evidence
├── Author Perspective
├── Editorial Thesis
├── Candidate Angles
├── Constraints
├── Open Questions
├── Article State
├── Hero Visual State
├── Decisions
├── Editorial Integrity
├── Readiness
├── Revision History
└── Publication Information
```

## Project Identity

Project Identity answers:

- What body of work is this?
- What permanent identifier belongs to it?
- What human-readable title describes it?
- Which project version is current?
- When was it created?
- When was it last updated?

Project Identity remains stable when:

- the article headline changes,
- the article slug changes,
- the thesis changes,
- or the saved project filename changes.

A duplicated project receives a new Project ID while optionally
preserving a reference to its parent project.

## Author Intent

Author Intent is the Studio's current interpretation of what the
Author is trying to accomplish.

Intent may be:

- explicit,
- inferred,
- revised,
- uncertain,
- or superseded.

Intent is not a compulsory field the Author must complete.

## Inputs

Inputs preserve what the Author supplied.

Examples:

- URLs
- Pasted excerpts
- Headlines
- Topics
- News recollections
- Observations
- Perspectives
- Notes
- Drafts
- Corrections
- Constraints
- Publication links
- Resume-project documents

Inputs should retain:

- their original form where appropriate,
- their contribution type,
- their timestamp,
- and their relationship to the project.

## Sources

Sources identify where information originated.

A source may include:

- URL,
- title,
- source author,
- publisher,
- publication date,
- access date,
- source type,
- paywall status,
- source-quality assessment,
- verification status,
- and relevance to the article.

A URL is useful provenance.

A URL is not durable memory.

## Durable Source Context

Referenced URLs may:

- expire,
- move,
- change,
- become unavailable,
- become paywalled,
- or display materially different content later.

The Context must therefore preserve the editorial value of a
source, not merely its address.

Durable Source Context may include:

- citation metadata,
- a concise source summary,
- key claims,
- important statistics,
- relevant dates,
- the Author's reaction,
- the source's role in the article,
- the evidence actually used,
- verification notes,
- and a limited essential excerpt where appropriate.

The purpose is continuity.

The purpose is not to create an unauthorized archive of the full
source.

## Paywalled and Author-Supplied Material

An Author may paste material that:

- came from a paywalled publication,
- cannot be revisited later,
- is visible only through the Author's subscription,
- or may disappear after the current interaction.

The Context should preserve enough information to understand the
editorial significance later.

It should normally retain:

- known citation metadata,
- a concise source summary,
- the specific claims used,
- relevant statistics,
- the Author's interpretation,
- how the material affected the thesis,
- and only the minimum necessary excerpt.

It should not automatically retain the complete paywalled article.

It should record when:

- the complete source was not retained,
- future independent verification may be limited,
- or reverification may be needed before republication.

## Evidence

Evidence is information used to support, qualify, or challenge a
claim.

Evidence may include:

- verified facts,
- statistics,
- research findings,
- official statements,
- professional experience,
- quotations,
- examples,
- and documented observations.

Evidence must distinguish:

- verified fact,
- source assertion,
- Author experience,
- reasonable inference,
- and unresolved uncertainty.

## Author Perspective

Author Perspective records what the Author:

- believes,
- observes,
- questions,
- agrees with,
- rejects,
- or has learned through experience.

Perspective is a first-class component.

It must never be silently replaced with generic AI opinion.

## Editorial Thesis

The Editorial Thesis is the central proposition the article
develops and supports.

It is not necessarily the headline.

The thesis may evolve when:

- new evidence appears,
- the Author changes position,
- a weak claim is removed,
- or a stronger editorial angle emerges.

## Candidate Angles

The Context may retain several possible editorial directions.

One angle may be current while others remain:

- proposed,
- rejected,
- superseded,
- or reserved for future use.

Rejected ideas may remain valuable because they explain the
evolution of the article.

## Constraints

Constraints may include:

- intended audience,
- tone,
- word count,
- LinkedIn article requirements,
- privacy requirements,
- subjects to avoid,
- timing,
- source restrictions,
- brand rules,
- or professional sensitivities.

## Open Questions

Open Questions represent unresolved matters that could affect:

- quality,
- accuracy,
- integrity,
- or editorial direction.

The Studio should ask the Author only when an unresolved question
materially blocks useful progress.

## Article State

Article State may contain:

- working title,
- headline,
- hook,
- structure,
- first draft,
- revised drafts,
- approved article,
- supporting publication copy,
- and publication status.

Article State is versioned.

Earlier meaningful versions should remain recoverable where
practical.

## Hero Visual State

Hero Visual State may contain:

- visual thesis,
- visual direction,
- Hero Visual copy,
- image-generation prompt,
- dimensions,
- suggested filename,
- approval status,
- and version.

The required Hero Visual size is 720 × 425.

The Author may copy or save the Hero Visual wherever they choose.

The Product does not require the Author to report its storage
location.

The conversational term infographic may be accepted, while
Hero Visual remains the architectural term.

## Decisions

Decisions record meaningful Author or Studio choices.

Examples:

- thesis approved,
- source rejected,
- headline selected,
- visual direction changed,
- article approved,
- publication channel selected,
- or project duplicated.

Decisions must remain understandable and revisable.

## Editorial Integrity

Editorial Integrity records whether the project currently satisfies
professional, evidentiary, ethical, and safety expectations.

It includes:

- source quality,
- attribution completeness,
- claim support,
- uncertainty disclosure,
- originality,
- privacy,
- professional conduct,
- safety concerns,
- and publication blockers.

## Readiness

Readiness is multidimensional.

The Studio may independently assess:

- intent readiness,
- source readiness,
- evidence readiness,
- perspective readiness,
- thesis readiness,
- article readiness,
- Hero Visual readiness,
- integrity readiness,
- and publication readiness.

Readiness should guide behaviour without exposing a rigid workflow
to the Author.

## Revision History

Revision History records meaningful editorial events.

Examples:

- perspective added,
- thesis changed,
- source removed,
- evidence challenged,
- article revised,
- Hero Visual replaced,
- publication URL recorded,
- or project resumed.

Revision History should not record every keystroke.

## Publication Information

Publication Information may include:

- publication channel,
- publication date,
- public URL,
- publication status,
- post-publication observations,
- and follow-up opportunities.

Public URLs are optional.

A project must remain useful when:

- no publication URL was supplied,
- the URL later expires,
- the post is removed,
- or the platform changes its URL structure.

LinkedIn is the initial article channel.

Facebook or another channel may be recorded when the Author
chooses to reference or republish the article elsewhere.

## Component Versioning

Editorial components support:

- a permanent component identifier,
- one current version,
- earlier versions,
- status,
- provenance,
- dependency information,
- and timestamps.

A component may be:

- missing,
- observed,
- inferred,
- proposed,
- approved,
- revised,
- superseded,
- rejected,
- archived,
- or removed.

## Dependency Intelligence

Dependencies do not create a fixed workflow.

They identify which work may require review after a change.

Examples:

- A changed palette should not rewrite the article.
- A changed Hero Visual should not alter verified evidence.
- A changed headline may require a revised hook.
- A changed thesis may affect the article and Hero Visual.
- A new source may strengthen evidence without changing the thesis.
- A changed publication URL should not alter editorial content.

## First-Pass and Refinement Behaviour

The Context supports both:

1. development before the first article package, and
2. refinement after the first article package.

The Author is not required to choose between these modes.

The Studio interprets the contribution and updates the appropriate
components.

## Time-to-Value

When sufficient starting material exists, the Studio should aim to
produce the first publication-ready article package within
approximately 10 minutes.

The Context must support rapid understanding without imposing a
laborious intake process.

## Insufficient Starting Material

When the material cannot support a distinctive, defensible article,
the Studio should not generate generic filler.

It should:

1. explain why the material is insufficient,
2. identify what is missing,
3. provide an example of a stronger starting point,
4. and recommend one useful next action.

## Relationship to Portable Editorial Projects

The Adaptive Editorial Context is the live in-session
representation of the work.

A Portable Editorial Project is the Author-owned, human-readable
export of the context needed to resume work later.

The Studio is stateless by default.

The Author controls the exported files and chooses where to save
them.

The Product does not depend on external file paths.
