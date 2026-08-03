# Architecture Baseline - 2026.08.02v10

## Status

Current Capability 009 product-runtime baseline when delivered.

## Baseline ID

`2026.08.02v10`

## Supersedes

`2026.08.01v09`

## Reason for Revision

Implement the Article Engine and textual Publication Package under
ADR-015 without absorbing Capability 010, Capability 011, or broader
integration work.

## Runtime Architecture

`studio.article_engine` owns approved article inputs, the provider
boundary, evidence-attribution validation, Editorial Intent preservation,
and High/Severe publication blocking.

`studio.publication_package` owns the validated textual package and
explicit later-capability placeholders. Package readiness distinguishes
Ready for Hero Visual from Review before Hero Visual and never claims
Version 1.0 completion while deferred outputs are absent.

## Integrity Boundary

The runtime consumes the existing `EvidenceValidationReport`. It does
not perform ingestion, research, claim classification, corroboration, or
risk reassessment. A provider cannot override the report, invent claim
identifiers, change approved intent, or omit attribution for evidence
used.

## Deferred Architecture

Integrated Editorial Workspace, Adaptive Editorial Context runtime,
Component Collaboration, stable Author-facing orchestration API, and
final integrated Editorial Confidence presentation remain deferred.
Rendered Hero Visual behavior remains Capability 010. Portable Editorial
Project behavior remains Capability 011.

## Generated Ownership

`scripts/bootstrap_capability009_article_engine_publication_package.py`
owns the Capability 009 runtime, tests, ADR, baseline, demo, architecture
contract, and managed documentation sections.

## Constitutional Impact

No frozen principle or canonical vocabulary changes. The implementation
applies existing Author ownership, evidence, attribution, risk, and
approved-work protections.
