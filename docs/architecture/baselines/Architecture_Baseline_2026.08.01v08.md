# Architecture Baseline - 2026.08.01v08

## Status

Current editorial integrity baseline when Capability 008A.3 is delivered.

## Baseline ID

`2026.08.01v08`

## Supersedes

`2026.08.01v07`

## Reason for Revision

Implement Capability 008A.3 - Editorial Integrity Hardening under ADR-013.

## Evidence Architecture

Verified Fact is an earned ClaimAssessment classification. A caller cannot
select it as an initial Claim classification. Only a Source Assertion with at
least two genuinely distinct, credible supporting sources and no credible
contradiction may earn it.

Author Experience and Opinion require durable attribution. Reasonable
Inference, Forecast, and Unresolved Uncertainty preserve their semantic
classification even when independently supported.

Corroboration is deduplicated by normalized source identity before independent
groups are counted. Credible contradictions are preserved conservatively.

## Editorial Risk Architecture

Material contradictions are Severe. Low risk contains no actionable finding.
High and Severe risk set an explicit publication block. Author-facing Editorial
Confidence preserves that block rather than softening it into apparent
readiness.

## Stage Architecture

`studio.editorial_guidance` is the canonical owner of EditorialStage,
StageState, stage order, Author-facing stage names, and permitted transitions.
Editorial Intake and Editorial Discernment share that exact runtime class.

Completed stages form an ordered prefix, only one stage may be in progress,
later stages cannot start early, and completed stages cannot reopen.
Workspace State remains distinct and is not changed by a stage transition.

## Generated Ownership

`scripts/bootstrap_capability008a3_editorial_integrity_hardening.py` owns the
hardened runtime, focused tests, ADR, baseline, and current-status sections.
The Capability 007 Intake, Capability 008 Discernment, and Capability 008
Evidence bootstraps delegate their affected templates to the 008A.3 canonical
templates.

## Constitutional Impact

No frozen constitutional rule changes. This baseline makes evidence certainty,
publication blocking, Editorial Confidence, and stage behavior more faithful
to the existing Constitution and Canonical Vocabulary.

## Deferred Scope

Article Engine, Publication Package, Component Collaboration, Hero Visual,
Portable Project, real ingestion, UI, release packaging, performance work, and
Version 2 generator consolidation remain unchanged.
