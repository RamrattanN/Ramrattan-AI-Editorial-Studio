# ADR-019 - Studio Configuration and Author-Controlled Continuity

## Status

Accepted. Approved as part of the Version 1.1 product design in
`docs/product/Version_1_1_Author_Experience_Baseline.md`, and further revised
to record the Repository Author's resolution of the Resume Existing Project
placement decision. Version 1.1 is delivered against this decision: V11-01
through V11-10 (Issues #70-#79) are complete on `develop`, including Studio
Configuration (V11-01, Issue #70) and Resume Existing Project integration
(V11-07, Issue #76, PR #89) this ADR governs.

## Date

2026-08-03

## Decision Level

D4 - Architecture

## Context

Version 1.0 solved editorial continuity with the Portable Editorial Project:
a durable, Author-owned Markdown record of approved article content, Hero
Visual reference, and package state, restored through Resume Existing
Project. It deliberately carries no publication *preferences* — Workflow
choice, Branding treatment — because those are not editorial content and did
not exist as separate concepts before Version 1.1.

Version 1.1 introduces Workflow Selection and Branding as explicit, repeated
per-session decisions. An Author who publishes regularly will make the same
choice in most sessions. Asking that Author to restate an unchanged
preference every session is a needless burden that Progressive Disclosure and
Author-Controlled Continuity both argue against. At the same time, the
Studio's statelessness is non-negotiable: nothing about this continuity may
depend on the Studio remembering anything.

The Architecture Review Board's review of the Version 1.1 baseline identified
that this mechanism — Studio Configuration — was specified only in narrative
terms ("publication preferences") with no defined content, and had no ADR of
its own despite meeting the repository's stated bar for one: it introduces a
new artifact format and a new persistence-adjacent guarantee (never stored,
session-scoped restoration).

## Decision

Adopt Studio Configuration as a minimal, versioned, Author-held file distinct
from, and never merged with, the Portable Editorial Project.

### Content boundary

A Ramrattan AI Configuration carries exactly two fields:

- the preferred Workflow mode (Guided or Express); and
- the Branding preference last used, recorded as a reference to the type of
  branding material previously supplied, or an explicit record that the
  Studio Theme was used.

It carries nothing else. It does not embed branding asset files, editorial
content, evidence, or Portable Editorial Project state. This boundary is
drawn directly from what the Version 1.1 Author Journey itself collects as a
preference; it is not drawn from, and does not partially implement, the
broader candidate preference schema (audience, tone, region, CTA style,
hashtag strategy, and others) described as a Version 2 candidate in
`docs/product/version2/Capability_012_Portable_Author_Context.md`.

### File format and naming

Configuration files use:

```text
Ramrattan-AI-Configuration-[YYYY.MM.DDvNN].json
```

matching the versioning convention established for the Portable Editorial
Project in ADR-004 and ADR-017. Configuration files do not expire because of
age; validity is determined by schema compatibility, not elapsed time.

### Serialization Format

This ADR standardizes JSON as the Ramrattan AI Configuration's
serialization format. It does not define concrete field names, the
implementation-level schema, parser implementation, or future format
extensions; the implementation owns the concrete JSON schema, and this
architecture owns only the decision to serialize as JSON at all.

JSON was selected over Markdown for deterministic, unambiguous parsing;
explicit field names and value types; straightforward schema validation;
reliable automated testing; and portability across future interaction
surfaces, consistent with this repository's software-engineering
discipline for AI-assisted products (ADR-000). Markdown configuration
input is not supported in Version 1.1.

### Load and generate mechanics

Configuration Load is offered once, only on the Start New Publication path
from Welcome's Entry Path choice, and is optional. Loading restores the two
fields above for the current session only; the Studio never retains a copy.
At Session Completion, the Studio offers to generate a new configuration from
the current session's Workflow mode and Branding preference; declining
produces no file and no error state, and the Studio again retains no copy.

### Relationship to Resume Existing Project

Studio Configuration and Resume Existing Project are distinct, non-competing
continuity mechanisms with different responsibilities: Configuration restores
preference, Resume restores content. The Repository Author has resolved how
they are sequenced: Resume Existing Project is a separate entry path from
Welcome, a sibling to Start New Publication, not an option offered alongside
Configuration Load. Configuration Load exists only on the Start New
Publication path; the Resume Existing Project path never presents it and
never reads a Configuration file.

This means a resumed Portable Editorial Project's Workflow mode or Branding
treatment is never silently altered by a Configuration file the Author
happens to also hold — the two artifacts cannot collide, because the paths
that consult them never overlap in the same session. An Author who wants
different Workflow or Branding behaviour while resuming sets it within the
resumed session directly; Configuration is structurally out of reach on that
path, not merely unconsulted by convention. This is recorded as the
authoritative sequencing decision in
`docs/product/Version_1_1_Author_Experience_Baseline.md`'s Entry Path and
Relationship to Resume Existing Project sections and in
`docs/architecture/Version_1_1_State_Machine.md`.

## Alternatives Considered

### Fold preferences into the Portable Editorial Project

Rejected. The Portable Editorial Project's responsibility is unfinished
editorial work; a preferences field would be read on every resume regardless
of whether the Author wanted preference continuity or content continuity on
that occasion, and would force the two artifacts' lifespans together. This
violates Every Artifact Has One Responsibility as directly as merging
Publication Content and Editorial Review would.

### Implement the full Capability 012 candidate schema now

Rejected. That schema is broader (audience, tone, region, CTA style, hashtag
strategy) than anything the Version 1.1 Author Journey collects, and its
delivery mechanism (a signed token, potentially delivered through a platform
entry point) raises security and trust questions explicitly deferred to
Version 2 review. Implementing a subset of that schema now, ahead of that
review, would pre-empt decisions that review is responsible for making.

### Store branding asset bytes inside the configuration file

Rejected. Embedding logos or headshots would make the configuration file
carry Author-identifying material with different privacy sensitivity than a
preference record, duplicate asset ownership already established by Identity
Asset handling in Version 1.0, and enlarge a file explicitly designed to stay
thin. Recording only the branding preference, and asking the Author to
resupply material, keeps the file's privacy profile uniform and low.

### Hosted or server-managed preference storage

Rejected outright. Directly conflicts with Stateless by Design; not seriously
considered as an alternative.

## Consequences

### Positive

- The Configuration's content is fully enumerable and independently
  testable: exactly two fields, no ambiguity about what else might be
  present.
- The boundary against Capability 012's broader schema is explicit, removing
  any risk that Version 1.1 quietly pre-implements unapproved Version 2
  scope.
- Keeping Configuration separate from the Portable Editorial Project
  preserves both artifacts' single responsibility and allows either to be
  loaded, generated, or omitted independently of the other.

### Costs and Risks

- A two-field schema is deliberately conservative; an Author who wants
  broader preference continuity (audience, tone, and so on) has no path to
  it within Version 1.1. This is accepted scope discipline, not an oversight.
- Because branding asset bytes are never embedded, restoring a full branding
  treatment still requires the Author to resupply the actual material each
  session; Configuration only removes the need to re-decide whether to.
- Because Configuration Load and Resume Existing Project are mutually
  exclusive per session, an Author who wants both a resumed project and a
  specific saved Workflow or Branding preference cannot get the latter from a
  Configuration file on that occasion; they set it directly within the
  resumed session instead. This is the accepted cost of keeping the two
  artifacts structurally non-overlapping rather than a defect.

## Rationale

This decision applies Every Artifact Has One Responsibility and
Author-Controlled Continuity together: continuity is real and valuable, but
only the thinnest slice of it — preference, not substance, and never asset
bytes — is worth carrying as a separate file. A wider schema would either
duplicate what the Portable Editorial Project already owns or anticipate a
Version 2 decision that has not been made. Progressive Disclosure is served
by removing repeated preference questions across sessions; Stateless by
Design is preserved because the Studio still remembers nothing — the Author
does.

## Future Implications

Any future expansion of Studio Configuration's content boundary toward the
Capability 012 candidate schema supersedes this ADR's content boundary
decision and requires its own review, on the same terms Capability 012's own
Candidate Acceptance Boundary already specifies. Any future integration
between Studio Configuration and the Portable Author Context token mechanism
requires a decision this ADR explicitly declines to make now.

Any future decision to make Configuration and a resumed Portable Editorial
Project available together in the same session — for example, applying a
saved Workflow or Branding preference automatically on resume — reverses the
non-overlap decision recorded above and requires its own review, since it
reintroduces exactly the collision risk that decision was written to avoid.
