# ADR-008 - Adopt the Capability Delivery Workflow

## Status

Accepted

## Date

2026-08-01

## Context

Repeated capability delivery exposed recurring procedural failure
modes:

- attempting to create an existing branch,
- bootstraps rejecting their own partial-apply changes,
- exact-language validation failures requiring repeated repairs,
- GitHub Project propagation delays,
- unresolved pull-request placeholders,
- terminal output accidentally pasted into the shell,
- duplicated manual reasoning,
- and inconsistent return-to-baseline verification.

These failures were individually resolved, but the resolutions were
not consistently carried forward.

## Decision

Adopt a state-aware, repeatable Capability Delivery Workflow.

The workflow governs:

- baseline verification,
- branch creation or resumption,
- bootstrap preview,
- safe application,
- partial-apply recovery,
- local validation,
- GitHub synchronization,
- staging,
- commit,
- push,
- pull-request creation,
- CI checking,
- merge,
- branch cleanup,
- return to `develop`,
- and capability closure.

## Tooling

Add:

- `docs/engineering/Capability_Delivery_Workflow.md`
- `scripts/capability_delivery.py`
- `tests/test_capability_delivery_workflow.py`

## Command Standard

Guidance must provide exact, paste-ready commands.

When a value is known, placeholders are prohibited.

## State Model

The helper determines the next safe action from repository and
GitHub evidence.

It does not blindly execute the complete lifecycle.

## Safety Boundary

The helper may inspect and recommend.

Mutating commands require explicit Author invocation.

## Consequences

### Positive

- Reduces repeated procedural mistakes
- Makes recovery predictable
- Makes capability completion auditable
- Prevents premature merge
- Prevents ambiguous branch state
- Preserves clean repository history
- Improves command quality
- Carries lessons forward automatically

### Costs

- Adds engineering process documentation
- Adds workflow-maintenance responsibility
- Requires future bootstraps to comply
- May stop work when repository state is ambiguous

## Alternatives Rejected

### Continue with Manual Memory

Rejected because previously solved problems recurred.

### Fully Automatic Release Script

Rejected because branch, commit, push, pull-request, and merge
actions should remain explicit and reviewable.

### Document the Process Without Tooling

Rejected because documentation alone does not detect actual
repository state.
