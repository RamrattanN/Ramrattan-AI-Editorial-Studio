# ADR-010 - Implement Evidence Validation and Editorial Risk

## Status

Accepted

## Date

2026-08-01

## Context

Capability 008 separated Editorial Discernment from Evidence Validation.
The repository needed an executable, provider-independent way to preserve
claim meaning, corroboration, conflicts, and time validity without
claiming certainty unsupported by the evidence.

## Decision

Adopt explicit Claim, EvidenceRecord, ClaimAssessment, and
EvidenceValidationReport models. Corroboration counts independent source
groups. Internal LMHS Editorial Risk is derived from material evidence
findings and translated into Editorial Confidence as the primary
Author-facing conclusion.

Verified requires two credible independent supporting groups and no
credible contradiction. High and Severe risk block a publication
recommendation. Percentages are prohibited.

## Constitutional Impact

No constitutional principle changes. This decision implements Evidence
Before Assertion, Confidence Before Publication, transparent uncertainty,
and the frozen Canonical Vocabulary.

## Consequences

The core remains deterministic and testable. External research providers
can be added later, but they must return attributable records. The model is
intentionally conservative and may request corroboration rather than
manufacture confidence.
