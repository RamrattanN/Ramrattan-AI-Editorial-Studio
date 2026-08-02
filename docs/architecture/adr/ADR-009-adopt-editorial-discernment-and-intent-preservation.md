# ADR-009 - Adopt Editorial Discernment and Intent Preservation

## Status

Accepted

## Date

2026-08-01

## Context

Editorial Intake can recognise material, but the Studio also needs to
determine what each new contribution means.

Without Editorial Discernment, unrelated sources or publication
objectives could be merged into incoherent work that undermines the
Author's credibility and Reader trust.

## Decision

Adopt the Editorial Discernment Engine internally and Editorial
Guidance as the Author-facing experience.

Implement:

- one Editorial Intent per Editorial Session,
- Intent Alignment,
- Editorial Coherence Guard,
- No Silent Scope Expansion,
- one-question clarification,
- approved-component protection,
- Workspace lifecycle,
- and Editorial Never Events.

## Workspace Lifecycle

Workspace State is distinct from Stage State.

Distinguish Cancelled from Aborted. Cancellation is deliberate Author termination.

Abortion is exceptional or interrupted termination.

Both preserve the project record unless the Author explicitly
deletes it.

## Editorial Authority

The Author retains final publication authority.

The Editor must explain material trust or coherence concerns before
accepting a risky change.

## Consequences

### Positive

- Protects one coherent publication objective
- Prevents silent source blending
- Preserves approved work
- Makes pause, resume, cancel, and abort explicit
- Creates testable Editorial Guidance
- Improves Reader trust

### Costs

- Requires conservative ambiguity handling
- Requires session state management
- Requires intent metadata
- Requires future model-assisted classification to remain governed by
  deterministic constitutional rules

## Alternatives Rejected

### Merge Everything Supplied

Rejected because availability does not imply editorial coherence.

### Block Every Scope Change

Rejected because the Author retains authority.

### Ask Multiple Clarifying Questions

Rejected because the Editor should infer before asking and minimise
Author effort.
