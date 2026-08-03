# ADR-004 - Adopt Portable Editorial Projects

## Status

Accepted

## Date

2026-08-01

## Decision Level

D4 - Architecture

## Context

The product requires Authors to resume, review, revise, duplicate,
or continue article projects later.

A hosted Author Library would introduce:

- accounts,
- authentication,
- storage costs,
- synchronization,
- backups,
- privacy obligations,
- retention policies,
- and multi-tenant architecture.

The Product also should not require the Author to disclose where
downloaded files are stored.

## Decision

The Studio will be stateless by default.

The initial continuity mechanism will be a Portable Editorial
Project owned and stored by the Author.

The project will use a small, human-readable Markdown file that
preserves enough Adaptive Editorial Context to resume work later.

The Studio will not rely on:

- local paths,
- Dropbox paths,
- OneDrive paths,
- Google Drive paths,
- or another reported storage location.

## File Naming

Portable project files use:

```text
Ramrattan-Editorial-Project_<Article-Slug>_YYYY.MM.DDvNN.md
```

Generated filenames must not exceed 255 characters.

The VCM identifier uses:

```text
YYYY.MM.DDvNN
```

## Export

The Author may:

- download the project Markdown file,
- download or copy the article,
- download or copy the Hero Visual,
- or export an optional ZIP package.

## Source Durability

URLs are preserved as provenance but are not treated as durable
memory.

The project should preserve:

- citation metadata,
- source summary,
- key claims,
- statistics used,
- Author reaction,
- editorial role,
- verification information,
- and limited necessary excerpts.

## Paywalled Material

When an Author supplies paywalled material, the project should
preserve the editorial substance required for resumption without
automatically retaining the complete source.

## Resume

Resume Existing Project becomes a first-class opening experience.

## Privacy

The Author decides where project files and generated outputs are
stored.

The Studio does not require custody of the Author's work.

## Alternatives Considered

### Hosted Author Library

Deferred because it introduces significant infrastructure,
security, privacy, and commercial scope.

### Local Database

Deferred because a database creates unnecessary coupling and is
less portable than an Author-owned project file.

### File-Path Tracking

Rejected because storage paths:

- burden the Author,
- become stale,
- reveal unnecessary information,
- and are not required for project resumption.

### Save Only the Finished Article

Rejected because the finished article does not preserve enough
editorial context to support high-quality resumption.

## Consequences

### Positive

- Author ownership
- Privacy by default
- Low storage burden
- Human readability
- Easy backup
- Easy transfer
- No required account system
- No required hosted database
- No path-management burden
- Lower operating cost
- Reduced compliance scope

### Costs and Risks

- The Author may lose the file
- Separately downloaded assets may be unavailable later
- Search across many projects is not initially provided
- Schema migration must be supported
- Project files must be validated before resumption
- Some expired sources may require reverification

## Future Options

A future optional index may catalog Portable Editorial Projects
without replacing Author ownership.

Hosted synchronization requires a new explicit architecture,
security, privacy, and commercial decision.
