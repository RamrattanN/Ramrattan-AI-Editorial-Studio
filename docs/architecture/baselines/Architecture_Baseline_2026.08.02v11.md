# Architecture Baseline - 2026.08.02v11

## Status

Proposed during RC1 Checkpoint and Delegated Authorization Hardening. Becomes
current only when this increment is delivered.

## Baseline ID

`2026.08.02v11`

## Supersedes

`2026.08.02v10`

## Reason for Revision

Extend the executable Capability Delivery helper with invocation-scoped
authorization outcomes that prevent duplicate profile requests without
weakening fail-closed delivery behavior.

## Engineering Architecture

The existing `scripts/capability_delivery.py` remains the sole delivery state
observer and recommender. It reports workflow state, next profile boundary,
active profile, authorization outcome, action coverage, new-profile need, and
fail-closed blocking independently.

Start, Publish, and Complete authorization is supplied per current-task helper
invocation and remains valid only through that profile. No approval is stored
as durable repository state. Conservative per-mutation approval remains
available.

## Product Runtime Impact

None. Article Engine, Publication Package, editorial runtime, Hero Visual,
Portable Project, and approved brand behavior are unchanged.

## Governance Decision

ADR-014, as amended by this increment, owns delegated authorization continuity.
