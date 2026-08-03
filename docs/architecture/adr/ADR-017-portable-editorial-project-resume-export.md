# ADR-017 - Portable Editorial Project Resume and Export

## Status

Proposed during Capability 011. Accept when Capability 011 is delivered.

## Context

The legacy Portable Editorial Project specification describes a rich future
record containing Author profiles, Adaptive Editorial Context, source archives,
publication history, and editorial decision history. The current RC1 runtime
does not reliably supply those values. Serializing placeholders would create
false memory and weaken trust.

Capability 011 must provide Author-owned continuity using the existing Article
Engine, Hero Visual, Publication Package, Editorial Session, Editorial Intake,
and Temporal Integrity seams without introducing deferred subsystems.

## Decision

Adopt a versioned, human-readable Markdown format with one deterministic JSON
data block. Schema version 1 contains only:

- product/schema identity and deterministic project identity;
- safe slug, saved date, daily sequential `YYYY.MM.DDvNN` document version,
  and optional previous version;
- approved article Markdown;
- approved Hero Visual prompt, attachment status, and validated hash when
  available; and
- current package confidence, risk, readiness, findings, and blockers.

Deserialization is strict. Malformed, unsupported, invalid, stale, and blocked
states remain explicit. Unknown legacy fields are rejected rather than
silently ignored or fabricated. Resume validates first, invokes
`EditorialSession.resume()`, and requires Temporal Integrity review.

Downloads are offline byte artifacts. Optional ZIP output uses stable ordering,
timestamps, permissions, and compression settings. Filename creation preserves
the fixed prefix, version suffix, extension, 255-character limit, and daily
collision sequence.

`PublicationPackage.portable_editorial_project` is the sole package attachment
change. Existing Article and Hero Visual content is preserved.

## Alternatives Rejected

- Implementing the full legacy schema: current runtime cannot truthfully supply
  it.
- Adding Adaptive Editorial Context or a workspace/orchestration layer: outside
  RC1 and Capability 011.
- Permissive parsing: unknown state could be mistaken for trusted state.
- Hosted storage: conflicts with Author-owned portable continuity.

## Consequences

RC1 projects are intentionally small and honest about their limits. Rich
context, migration beyond schema version 1, collaboration, UI, publication
automation, and Version 2 behavior remain deferred. Architecture Baseline
`2026.08.02v13` records the executable boundary.
