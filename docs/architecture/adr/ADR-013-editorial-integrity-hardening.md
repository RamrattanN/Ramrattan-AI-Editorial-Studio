# ADR-013 - Editorial Integrity Hardening

## Status

Accepted

## Date

2026-08-02

## Decision Level

D4 - Architecture

## Context

Capability 008 established deterministic Evidence Validation and Editorial
Risk, but callers could construct a claim already labelled Verified Fact,
duplicate source identifiers could manufacture apparent independence, and
non-factual claim types could appear verified merely through corroboration.

The runtime also contained two incompatible StageState enums and repeated
stage names without one owner. Those differences could make intake,
discernment, and Author-facing progress disagree.

## Decision

Adopt strict editorial-integrity and canonical-stage contracts.

### Evidence Classification

- Verified Fact is an earned assessment result, never an initial caller choice.
- Only a Source Assertion can become Verified Fact after sufficient evidence.
- Author Experience and Opinion retain explicit, durable attribution.
- Reasonable Inference, Forecast, and Unresolved Uncertainty retain their
  classification even when independent evidence supports them.
- Evidence support never silently changes the semantic meaning of a claim.

### Corroboration Independence

Evidence is deduplicated by normalized source identity before independent
groups are counted. Repeating one source identifier under different groups
cannot manufacture corroboration. When duplicated records disagree, a
credible contradiction takes precedence over support.

### Contradiction and LMHS Editorial Risk

- A material credible contradiction produces Severe Editorial Risk.
- A non-material contradiction remains actionable and cannot produce Low risk.
- Low risk contains no actionable finding.
- High and Severe risk block publication recommendation.
- Moderate risk may proceed only with its identified review actions.

### Author-Facing Editorial Confidence

Editorial Confidence remains the primary Author-facing conclusion. High and
Severe translations explicitly disclose that publication is blocked; the
translation must never make a blocking internal risk appear publication-ready.
Final integrated presentation remains deferred to Capability 009.

### Canonical StageState

`studio.editorial_guidance` owns:

- the five ordered EditorialStage values;
- their canonical Author-facing names;
- the shared StageState lifecycle;
- permitted state transitions; and
- ordered-stage validation.

Editorial Intake and Editorial Discernment import and re-export this one model.
Compatibility aliases for earlier `PENDING` and `ACTIVE` names resolve to the
canonical `NOT_STARTED` and `IN_PROGRESS` members; active runtime behavior uses
only canonical names.

Workspace State remains the persistent Editorial Workspace lifecycle.
StageState remains transient progress for one Editorial Integrity stage. A
stage transition does not silently change Workspace State.

## Constitutional Impact

This decision implements Evidence Before Assertion, Confidence Before
Publication, Professional Judgement, Language Shapes Behaviour, and trust
before convenience. It does not change the frozen Constitution or Canonical
Vocabulary.

## Alternatives Considered

### Permit callers to declare Verified Fact

Rejected because certainty must be earned from evidence rather than asserted.

### Count only independent-group labels

Rejected because duplicate source identities could be assigned different
labels and falsely appear independent.

### Keep separate intake and discernment StageState enums

Rejected because identical concepts with different members create drift and
make cross-component state unreliable.

### Hide publication blocking behind generic confidence language

Rejected because Author-facing translation must preserve material risk.

## Consequences

Evidence assessments are more conservative and explicit. Existing callers
must provide attribution for Author Experience and Opinion and may no longer
construct Verified Fact directly. Stage transitions reject invalid order and
terminal-state reopening. Compatibility aliases reduce migration risk without
creating a second state model.

## Architecture Baseline

Recorded by Architecture Baseline `2026.08.01v08`.
