# V11-01 Author Journey Foundation

## Status

Implementation contract for GitHub Issue #70.

## Runtime ownership

`studio/author_journey.py` owns the repository-side early-session contract
for Welcome, Entry Path, Configuration Load, Workflow Selection, and the
downstream routing seams established by V11-01. It wraps, but does not replace
or modify, the Version 1.0 `EditorialSession` runtime.

## Acceptance mapping

- Entry Path routing: AC-ENTRY-1, AC-ENTRY-2, AC-ENTRY-3, AC-ENTRY-8.
- JSON Configuration validation and session-scoped restoration:
  AC-CONFIG-1 through AC-CONFIG-8 and AC-CONFIG-13 through AC-CONFIG-16.
- Workflow mode selection over one state machine: AC-WORKFLOW-1 and
  AC-WORKFLOW-2.
- Structural absence of cancellation, cleanup, save, and artifact generation:
  AC-LEAVE-1 through AC-LEAVE-3.

The authoritative behavior remains in the governing Version 1.1 product and
architecture documents. This file records implementation ownership and test
traceability only.

## Deferred seams

`Resume Validation` is a routing target only; V11-07 owns its integration.
`Editorial Source` is a routing target only; V11-02 owns its behavior. V11-01
does not implement either target, any later Author Journey state, or any
standalone interface.
