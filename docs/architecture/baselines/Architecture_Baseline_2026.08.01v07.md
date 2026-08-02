# Architecture Baseline - 2026.08.01v07

## Status

Current engineering delivery baseline.

## Baseline ID

`2026.08.01v07`

## Supersedes

`2026.08.01v06`

## Reason for Revision

Implement Capability 008A.2 - Delivery Hardening under ADR-012.

## Architecture

The Capability Delivery helper is a fail-closed observer and recommender.
Its evidence model contains direct remote freshness; explicit `FOUND`,
`NOT_FOUND`, `UNAVAILABLE`, and `AMBIGUOUS` discovery; normalized draft,
review, mergeability, and check state; verified PR/head agreement;
deterministic post-merge recovery; and explicit approval boundaries.

Remote, GitHub, parsing, or required-field failure blocks advancement.
Missing or empty checks do not count as successful CI.

## CI Contract

```bash
python3 -m compileall -q studio scripts tests
python3 -m unittest discover -s tests -v
python3 studio.py validate
```

## Generated Ownership

`scripts/bootstrap_capability008a2_delivery_hardening.py` owns the hardened
delivery artifacts. The original Capability Delivery bootstrap delegates its
helper, workflow, and test templates to the 008A.2 canonical templates.

## Constitutional Impact

No frozen constitutional rule changes. This baseline strengthens Engineering
Stewardship and trust before convenience by refusing to convert unavailable
evidence into a safe transition.

## Product Runtime Impact

None. Evidence Validation, StageState, editorial runtime, Article Engine,
Publication Package, Hero Visual, and Portable Project behavior are unchanged.
