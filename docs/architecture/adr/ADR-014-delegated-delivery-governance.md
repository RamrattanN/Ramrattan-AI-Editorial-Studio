# ADR-014 - Delegated Delivery Governance

## Status

Accepted

## Date

2026-08-02

## Decision Level

D4 - Architecture and Governance

## Context

The Capability Delivery Workflow protected consequential transitions, but its
default interaction pattern required roughly seven or eight separate approval
exchanges during routine delivery. The repository had already demonstrated
that a bounded publication phase could safely combine commit, push, pull-request
creation, CI monitoring, and ready-for-review transition when every prerequisite
was checked before advancing.

Repository guidance also lacked an explicit rule for combining already approved
pending changes to the same file or tightly coupled concern. That omission could
produce artificial change fragmentation without improving authority, recovery,
or review safety.

## Decision

Adopt a Standard delegated delivery model with three independently authorized
profiles:

- **Start** covers planning synchronization to `In Progress`, branch creation
  or resumption, implementation, generation, repair, validation, diff review,
  and staging of the exact reviewed scope. It stops before publication.
- **Publish** covers commit of the approved staged diff, commit verification,
  push, pull-request creation or reuse, read-only CI monitoring, and marking the
  pull request ready only when all required conditions pass. It stops before
  merge.
- **Complete** covers merge, branch cleanup, return to clean synchronized
  `develop`, completion planning synchronization, issue closure, and the
  Capability Delivery Receipt.

Retain a **Conservative** profile for exceptional high-risk work. Conservative
delivery requires approval at each protected mutation boundary.

Every profile authorization must come from the current task or conversation.
It is conditional on verified scope, targets, and prerequisites. One profile
never authorizes a later profile. Unknown, unavailable, mismatched, or failed
state stops execution immediately. Read-only CI monitoring remains autonomous.

The delivery helper remains an observer and recommender. It reports the
workflow state, next profile boundary, active approval profile, and whether the
recommended command is covered, requires specific Conservative approval, or
must stop because the active profile does not match.

When two or more approved pending changes affect the same file or tightly
coupled concern, consolidate them only when scope, risk profile, and delivery
timing agree. Separate changes for materially different scope, different risk
or approval authority, safer rollback or recovery, conflicting delivery timing,
or an explicit repository constraint. Consolidation never expands authority.

## Alternatives Considered

- **Keep per-mutation approval for all work.** Rejected as the only default
  because it adds routine interaction cost after scope and conditions are
  already explicit. It remains available as Conservative delivery.
- **Authorize the entire lifecycle at Start.** Rejected because publication and
  merge are consequential boundaries that require fresh, independently verified
  state.
- **Automatically consolidate all nearby changes.** Rejected because scope,
  authority, rollback, and timing can differ even when files overlap.

## Consequences

Routine capability delivery can use three meaningful approval interactions
without weakening fail-closed verification or role-based human authority.
Helper output makes profile mismatch explicit. Governance documentation,
contributor guidance, executable behavior, tests, and owning generators must
remain synchronized.

## Architecture Baseline

Recorded by Architecture Baseline `2026.08.01v09`.

<!-- RC1_AUTHORIZATION_CONTINUITY_START -->

## Authorization Continuity Amendment

An explicitly authorized Standard profile remains valid through all verified
states assigned to that phase. Repeated status reporting and helper invocations
inside the phase do not require duplicate authorization. The helper now reports
authorization already satisfied, new profile authorization required, or blocked
by fail-closed condition as distinct outcomes.

Authorization remains current-task context only. It expires at the profile
boundary or on material mismatch, scope change, revocation, fail-closed state,
or loss of current conversational authority. It is never persisted or inferred
from repository history. Conservative per-mutation approval remains unchanged.

Architecture Baseline `2026.08.02v11` records the executable helper change when
this increment is delivered.

<!-- RC1_AUTHORIZATION_CONTINUITY_END -->
