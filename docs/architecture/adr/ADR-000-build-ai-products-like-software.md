# ADR-000 - Build AI Products Like Software

## Status

Accepted

## Date

2026-08-01

## Context

Many AI projects begin as isolated prompts and gradually become difficult to understand, test, maintain, and improve.

Prompt changes may be undocumented. Workflows may rely on hidden assumptions. Earlier behavior may be difficult to restore.

## Decision

Ramrattan AI Editorial Studio will use established software engineering practices, including:

- Version control
- Semantic versioning
- Documentation
- Architecture Decision Records
- Reviewable branches
- Release candidates
- Regression testing
- Changelogs
- Rollback paths
- Explicit acceptance criteria

Prompt engineering is treated as one component of the product rather than the entire product.

## Alternatives Considered

### Maintain one continuously edited prompt

Rejected because it provides weak traceability and makes rollback difficult.

### Maintain dated prompt copies only

Rejected because it preserves history without addressing testing, architecture, workflow, or release quality.

### Build a fully automated application immediately

Deferred because it would add premature complexity before the editorial workflow is validated.

## Consequences

### Positive

- Decisions remain understandable
- Releases remain traceable
- Prompt drift can be identified
- Changes can be reviewed and reversed
- Contributors have clearer standards

### Costs

- Documentation requires time
- Releases require discipline
- Some changes move more slowly

## Outcome

Accepted as the founding architectural principle.
