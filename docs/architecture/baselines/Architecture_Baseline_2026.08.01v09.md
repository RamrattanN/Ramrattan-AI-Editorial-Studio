# Architecture Baseline - 2026.08.01v09

## Status

Current workflow-governance baseline.

## Baseline ID

`2026.08.01v09`

## Supersedes

`2026.08.01v08`

## Reason for Revision

Implement delegated delivery profiles and coherent change consolidation under
ADR-014 without changing editorial product behavior.

## Delivery Architecture

The Capability Delivery helper remains a fail-closed observer and recommender.
In addition to its verified workflow state, it reports the next profile boundary
and the active approval profile.

The Standard delegated workflow has three independently authorized profiles:
Start, Publish, and Complete. Conservative delivery retains approval at every
protected mutation boundary. Conditional bundles verify every prerequisite
before advancing, and unknown, unavailable, mismatched, or failed evidence
stops execution.

Automatic CI monitoring is read-only. The helper never performs a protected
Git or GitHub mutation.

## Governance Architecture

Approved pending changes to the same file or tightly coupled concern are
consolidated only when scope, risk profile, and delivery timing agree.
Materially different scope, authority, rollback needs, timing, or repository
constraints require separate delivery.

Role-based authority from ADR-011 remains unchanged. Authorization must come
from the current task or conversation, a Repository Maintainer remains limited
to explicitly delegated authority, and the Repository Author retains final
authority over product direction, governance changes, and material scope.

## Generated Ownership

`scripts/bootstrap_capability008a2_delivery_hardening.py` owns the hardened base
templates. `scripts/bootstrap_workflow_governance_refinement.py` owns the
delegated-profile and consolidation delta and produces the current delivery
helper, workflow documentation, and workflow tests. The original Capability
Delivery bootstrap delegates to the refined hardened templates. The Capability
008A.1 bootstrap owns `CONTRIBUTING.md` and remains synchronized with its
role-based translation.

## Product Runtime Impact

None. Evidence Validation, StageState, Article Engine, Publication Package,
Hero Visual, Portable Project, and all editorial product behavior are unchanged.
