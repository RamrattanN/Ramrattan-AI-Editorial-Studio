# ADR-002 - Adopt an Adaptive Editorial Context

## Status

Accepted

## Date

2026-08-01

## Decision Level

D4 - Architecture

## Context

The initial workflow prototype models editorial creation as a
sequence of ordered stages.

That model does not fully represent how Authors develop ideas,
introduce new sources, reverse approvals, or change direction.

## Decision

The target architecture will use an evolving Editorial Context
rather than a mandatory linear state machine.

The context will represent:

- editorial components,
- statuses,
- provenance,
- dependencies,
- revisions,
- and recoverable history.

## Existing Prototype

The current `studio.workflow` package remains an engineering
prototype and reference implementation.

It does not define the final product interaction model.

## Consequences

### Positive

- Supports non-linear creativity.
- Preserves continuity across revisions.
- Treats perspective and evidence independently.
- Allows partial regeneration.
- Supports future session persistence.
- Reduces forced questions.

### Costs and Risks

- Dependency tracking becomes more sophisticated.
- Context interpretation requires confidence and provenance.
- Testing must cover revision events, not only stages.
- Existing workflow code will eventually require migration.

## Outcome

Accepted as the target architecture.
