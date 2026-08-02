# ADR-015 - Article Engine and Publication Package

## Status

Accepted

## Date

2026-08-02

## Decision Level

D4 - Architecture

## Context

Capabilities 007 and 008 can interpret input, preserve Editorial Intent,
validate evidence, and determine Editorial Risk, but the repository has
no executable Article Engine or textual Publication Package assembly.
Earlier planning also assigned broader integrated product surfaces to
Capability 009, conflicting with issue #15, ROADMAP, and the Version 1
Scorecard.

## Decision

Capability 009 implements only the Article Engine and Publication
Package. The Article Engine uses a provider-independent draft boundary,
preserves approved Editorial Intent and insights, requires attribution
for used evidence, and fails closed when Editorial Risk is High or
Severe.

The Publication Package validates the Capability 009 textual components
and carries the existing Editorial Confidence and LMHS Editorial Risk.
It explicitly records rendered Hero Visual and Portable Editorial
Project outputs as deferred and does not claim the full Version 1.0
package is complete.

## Explicit Deferrals

Integrated Editorial Workspace, Adaptive Editorial Context runtime,
Component Collaboration, a stable Author-facing orchestration API, and
final integrated Editorial Confidence presentation are not independent
Capability 009 scope. Rendered Hero Visual generation remains Capability
010. Portable Editorial Project behavior remains Capability 011.

## Constitutional Impact

This decision implements Author ownership, Understanding Before
Generation, Evidence Before Assertion, Confidence Before Publication,
Professional Judgement, and approved-work protection. It changes no
frozen constitutional principle or canonical term.

## Alternatives Considered

### Implement the broader integrated workflow

Rejected because it combines several product surfaces, creates new
Author-facing behavior, and absorbs later capability scope.

### Generate before Editorial Integrity completes

Rejected because unsupported claims could become polished publication
content before evidence and risk gates run.

### Couple runtime to one model provider

Rejected because editorial invariants must remain deterministic and
provider-independent.

## Consequences

Capability 009 produces an evidence-aligned textual article package
ready for later Hero Visual work. The complete Version 1.0 package
remains intentionally incomplete until Capabilities 010 and 011.

## Architecture Baseline

Recorded by Architecture Baseline `2026.08.02v10`.
