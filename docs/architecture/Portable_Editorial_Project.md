# Portable Editorial Project Specification

## Status

Active architecture baseline for Capability 5.

## Purpose

A Portable Editorial Project allows an Author to resume an article
project later without requiring the Studio to host or retain the
Author's work.

It preserves a small amount of high-value context in a
human-readable Markdown file.

## Core Principle

> The Studio's memory belongs to the Author.

Every project should be:

- portable,
- resumable,
- human-readable,
- versioned,
- private by default,
- and under the Author's control.

## Product Boundary

The Studio creates downloadable or copyable outputs.

The Author may:

- download the article,
- copy the article text,
- download the Hero Visual,
- copy the Hero Visual,
- download the Portable Editorial Project,
- or download an optional ZIP package.

The Author chooses where those outputs are stored.

The Product does not require:

- a local path,
- a Dropbox path,
- a OneDrive path,
- a Google Drive path,
- or any other storage location.

The Product must not burden the Author with reporting file paths.

## Why Saving Matters

At the appropriate point, the Studio should explain the value of
saving the Portable Editorial Project.

Example:

> Save your Editorial Project
>
> This small file preserves the context behind your article,
> including its thesis, sources, Author perspective, important
> evidence, editorial decisions, publication information, and next
> actions.
>
> Saving it allows the Studio to resume your work later without
> asking you to reconstruct the project from memory.
>
> Store it wherever you keep important work. The Studio does not
> need to retain a copy.

Saving should be encouraged without becoming a mandatory or
laborious step.

## Start Experience

The opening experience should support:

- Start a New Editorial Project
- Resume an Existing Editorial Project

Resume should accept a compatible Portable Editorial Project file.

The Studio should validate the file before restoring context.

## File Naming Standard

The project Markdown filename follows:

```text
Ramrattan-Editorial-Project_<Article-Slug>_YYYY.MM.DDvNN.md
```

Example:

```text
Ramrattan-Editorial-Project_AI-Governance-Beyond-Compliance_2026.08.01v01.md
```

## Version Control Method

The version identifier follows:

```text
YYYY.MM.DDvNN
```

Where:

- `YYYY` is the four-digit year,
- `MM` is the two-digit month,
- `DD` is the two-digit day,
- `vNN` is the sequential version for that date.

Examples:

```text
2026.08.01v01
2026.08.01v02
2026.08.01v03
2026.08.07v01
```

The daily sequence begins at `v01`.

Existing versions are not silently overwritten.

## Filename Length

Generated filenames must never exceed 255 characters.

The product must preserve:

- the fixed product prefix,
- the version suffix,
- and the file extension.

The article slug is shortened when required.

When shortening could create ambiguity or collision, the filename
receives a short collision-resistant identifier.

Example:

```text
Ramrattan-Editorial-Project_How-Enterprise-AI-Governance-Changes-Decision-Making-8F3A2C_2026.08.01v01.md
```

The Product may warn when a destination rejects a generated file.

It must not require the Author to disclose the destination path.

## Slug Rules

The article slug should:

- remain human-readable,
- use letters, numbers, and hyphens,
- replace whitespace with hyphens,
- remove unsafe characters,
- collapse repeated hyphens,
- remove leading and trailing hyphens,
- and preserve meaningful words where practical.

## Permanent Identity

Every project contains a permanent machine-readable Project ID.

Example:

```yaml
project_id: REP-7F3A91C2
project_slug: AI-Governance-Beyond-Compliance
document_version: 2026.08.01v01
previous_version:
```

The permanent Project ID is not derived solely from the title or
filename.

## Portable Project Contents

The Markdown file should preserve enough context to resume the work
without carrying unnecessary bulk.

Suggested structure:

```yaml
studio:
  product: Ramrattan AI Editorial Studio
  schema_version: 1
  created_with_version:
  capability_level:

project:
  project_id:
  title:
  slug:
  document_version:
  previous_version:
  created_at:
  updated_at:
  status:

author:
  intent:
  perspective:
  audience:
  tone:
  constraints:

editorial:
  thesis:
  current_angle:
  key_decisions:
  open_questions:
  next_actions:

article:
  title:
  suggested_file_name:
  approved:
  word_count:
  article_summary:
  article_text_included:

hero_visual:
  suggested_file_name:
  dimensions: 720x425
  visual_thesis:
  hero_copy:
  generation_prompt:
  approved:
  image_included:

publication:
  status:
  linkedin_url:
  facebook_url:
  published_at:

sources:
  - source_id:
    source_type:
    url:
    title:
    source_author:
    publisher:
    publication_date:
    accessed_at:
    paywalled:
    source_quality:
    verification_status:
    durable_summary:
    key_claims:
    statistics_used:
    author_reaction:
    editorial_role:
    retained_excerpt:
    full_source_retained: false
    reverification_may_be_required:

integrity:
  attribution_complete:
  claims_supported:
  uncertainty_disclosed:
  originality_reviewed:
  privacy_reviewed:
  safety_reviewed:
  blockers:

history:
  - version:
    date:
    summary:
```

The final format may use structured front matter plus readable
Markdown sections.

## Article Content

The project file may contain:

- the complete current article,
- a concise article summary,
- or a reference to an accompanying article file within the ZIP.

The Author may also copy the article directly from the Product.

Resumption must remain possible when the separately downloaded
article file is missing.

## Hero Visual Context

The Markdown project cannot be expected to contain the complete
binary Hero Visual unless it is part of an optional ZIP package.

It should preserve enough context to understand or recreate it:

- visual thesis,
- Hero Visual copy,
- dimensions,
- generation prompt,
- visual direction,
- approval status,
- and suggested filename.

The Author may download or copy the Hero Visual independently.

The Product does not need to know where the Author saved it.

## Durable Source Context

URLs may expire or change.

The project file must therefore preserve enough source context to
understand the evidence later.

For each material source, preserve where available:

- citation metadata,
- concise durable summary,
- key claims,
- statistics used,
- the Author's interpretation,
- editorial role,
- access date,
- verification state,
- and limited essential excerpts.

A resumed project should remain understandable when a URL:

- expires,
- becomes unavailable,
- moves behind a paywall,
- changes content,
- or redirects elsewhere.

## Paywalled Material

Authors may paste material from a paywalled source.

The Studio should preserve:

- known citation metadata,
- a concise summary,
- the claims used,
- important statistics,
- the Author's response,
- and only the minimum necessary excerpt.

The Studio should not automatically place the complete paywalled
article into the project file.

The project should record when:

- the full source was not retained,
- future independent access may be limited,
- or reverification may be needed before future publication.

## Optional Publication Links

The project may record:

- LinkedIn article URL,
- Facebook post URL,
- company website URL,
- or another public publication URL.

Publication URLs are optional.

The project must remain useful when a URL:

- was never supplied,
- later expires,
- changes,
- or becomes inaccessible.

## Optional Export Package

The Studio may offer:

- Save Project File
- Download Article
- Download Hero Visual
- Copy Article
- Copy Hero Visual
- Export ZIP

Example ZIP contents:

```text
AI-Governance-Beyond-Compliance/
├── Ramrattan-Editorial-Project_AI-Governance-Beyond-Compliance_2026.08.01v01.md
├── Ramrattan-Article_AI-Governance-Beyond-Compliance_2026.08.01v01.md
└── Ramrattan-Hero-Visual_AI-Governance-Beyond-Compliance_2026.08.01v01.png
```

The Author may choose to download only the small project file.

## Resume Behaviour

When a compatible project file is supplied, the Studio should:

1. validate the schema,
2. identify the project and version,
3. summarize the restored context,
4. identify any missing optional assets,
5. identify unresolved integrity blockers,
6. explain the most recent known state,
7. and continue without unnecessary re-entry.

Example:

> Welcome back.
>
> The latest saved project is
> `AI Governance Beyond Compliance`, version
> `2026.08.01v03`.
>
> The article was marked as published on LinkedIn.
>
> A publication URL was not preserved.
>
> The Hero Visual context is available and can be revised or
> regenerated.
>
> The last open action was to consider a follow-up article about
> operational accountability.

## Missing Optional Assets

A missing article file or Hero Visual file must not corrupt the
Portable Editorial Project.

The Studio should:

- explain which optional asset was not supplied,
- preserve the remaining editorial context,
- use included article text where available,
- regenerate the Hero Visual when appropriate,
- or continue without the asset.

## Privacy

The project is private by default.

The Author chooses:

- whether to download it,
- where to store it,
- whether to share it,
- whether supporting files are included,
- and whether it is deleted.

## Storage Responsibility

The Studio is stateless by default.

The initial product does not require:

- user accounts,
- hosted document storage,
- cloud synchronization,
- reported file paths,
- multi-tenant databases,
- or custody of Author files.

Future hosted storage requires a separate explicit product,
security, privacy, and commercial decision.

## Reuse

The Author may resume a project to:

- revise the article,
- update the Hero Visual,
- add a publication URL,
- create a follow-up article,
- duplicate the project,
- review earlier evidence,
- or continue an unfinished idea.

Reuse should reduce effort without silently carrying outdated,
weak, or unsupported claims into new work.
