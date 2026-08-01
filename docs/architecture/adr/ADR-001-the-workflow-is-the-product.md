# ADR-001 - The Workflow Is the Product

## Status

Accepted

## Date

2026-08-01

## Context

The original Article & Post Generator used one instruction set
to analyze sources, develop editorial positioning, propose visual
treatments, and generate final LinkedIn content.

As the product evolved, this approach created several risks:

- Workflow behavior could be hidden inside prompt language.
- Moving backward could lose approved decisions.
- User choices could be represented inconsistently.
- Visual and editorial logic could become tightly coupled.
- Replacing the underlying model could require redesigning the
  complete experience.

## Decision

Ramrattan AI Editorial Studio will treat the guided workflow as
the stable product layer.

AI models, prompts, visual generators, and publishing adapters
will operate as replaceable capabilities coordinated by that
workflow.

The workflow will explicitly represent:

- Editorial session state
- User choices
- Valid transitions
- Review checkpoints
- Backward navigation
- Downstream dependency resets
- Final approval

## Alternatives Considered

### One Monolithic Prompt

Rejected because behavior would remain difficult to test,
extend, and restore.

### Generate Everything in One Step

Rejected because it provides speed but weak editorial control.

### Build a Full Web Application Immediately

Deferred because the workflow must be validated before investing
in a complete interface.

## Consequences

### Positive

- The workflow can be tested independently.
- AI providers can be replaced.
- User state can eventually be persisted.
- Navigation becomes predictable.
- Visual and written engines remain modular.
- Product behavior is easier to document.

### Costs and Risks

- More explicit code is required.
- State dependencies must be maintained carefully.
- Workflow versioning becomes a product responsibility.
- Mock implementations are needed before all engines exist.

## Outcome

Accepted as the core architectural principle for Sprint 2.
