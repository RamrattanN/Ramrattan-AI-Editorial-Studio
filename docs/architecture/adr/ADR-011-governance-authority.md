# ADR-011 - Governance Authority

## Status

Accepted

## Date

2026-08-02

## Decision Level

D4 - Architecture

## Context

The repository contains constitutional, architectural, engineering,
contributor, memory, planning, and release documents. Several documents
repeated similar rules without defining which document owned each concept
or how conflicts and status drift should be resolved.

Capability 008A.1 must consolidate governance without changing product
runtime behavior or inventing historical records.

## Decision

Adopt an explicit governance authority model with one authoritative owner
for every concept.

Nilesh's current request defines maximum task scope and authorization.
Within that scope, repository authority is applied in this order:

1. Verified repository and external-system state for factual questions
2. Constitution
3. Canonical Vocabulary
4. Current architecture baseline and accepted ADRs
5. Capability Delivery Workflow
6. `AGENTS.md`
7. `CONTRIBUTING.md`
8. `AGENT_MEMORY.md`
9. Conversation history

More restrictive safety and approval requirements always apply.

## Authoritative Responsibilities

| Artifact | Authoritative responsibility |
|---|---|
| Constitution | Enduring product principles and human responsibilities |
| Canonical Vocabulary | Active product and editorial terminology |
| Accepted ADRs | Durable architectural and governance decisions |
| Current architecture baseline | Coherent implemented architecture at a point in time |
| Capability Delivery Workflow | Canonical delivery lifecycle and recovery procedure |
| `AGENTS.md` | Operational contract for repository agents |
| `CONTRIBUTING.md` | Contributor-facing translation of repository governance |
| `AGENT_MEMORY.md` | Advisory, chronological engineering experience |
| `ROADMAP.md` | Current capability sequence and program status |
| Version 1.0 Scorecard | Release-readiness evidence by required area |
| Version 1.0 Release Definition | Product promise and release boundary |

A document may summarize another authority but must link to it rather than
create a competing rule.

## Lifecycle

- The capability that changes a governed fact updates its authoritative
  artifact and affected summaries in the same increment.
- Historical capability sections remain delivery records and must not be
  interpreted as current status when a later authoritative status section
  exists.
- `AGENT_MEMORY.md` is append-oriented and advisory. Normative lessons must
  be promoted into the appropriate governing document before enforcement.
- Changes to governance authority require an ADR, focused contract tests,
  generator synchronization, complete validation, and deliberate review.
- Frozen constitutional or canonical vocabulary changes require explicit
  authorization beyond ordinary governance maintenance.

## Approval Boundaries

Governance consolidation does not weaken approval boundaries. Staging,
commit, push, pull-request mutations, merge, branch deletion, issue
mutations, Project mutations, publication, and destructive operations
remain protected unless Nilesh explicitly authorizes them.

## ADR-002 Reference Integrity

Repository history contains no ADR-002 file or Git object. The surviving
reference in Architecture Baseline v01 is therefore repaired to point to
`docs/architecture/Editorial_Context_Model.md`, the historical architecture
artifact that actually exists. ADR-002 is not recreated retroactively.

## Architecture Baseline

No new architecture baseline is created for Capability 008A.1. This ADR
clarifies governance authority without changing executable system
architecture. Architecture Baseline `2026.08.01v06` remains current.

## Alternatives Considered

### Treat every governance document as equally authoritative

Rejected because duplicated rules can conflict without a deterministic
resolution path.

### Make `AGENT_MEMORY.md` normative

Rejected because chronological experience should not silently change
repository policy.

### Recreate ADR-002 from its broken reference

Rejected because no historical ADR content exists and reconstruction would
invent repository history.

### Create a new architecture baseline

Rejected because governance clarification does not change runtime
architecture.

## Consequences

### Positive

- Conflicts resolve deterministically.
- Every governance concept has one authoritative owner.
- Advisory memory cannot silently become policy.
- Current status is separated from historical delivery records.
- Broken historical references are repaired honestly.

### Costs

- Capabilities must update affected authorities and summaries together.
- Governance contract tests add maintenance obligations.
- Contributors must distinguish current status from historical records.
