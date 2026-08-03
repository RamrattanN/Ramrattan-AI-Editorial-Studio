# Evidence Validation Runtime

## Status

Active runtime architecture for the Capability 008 continuation.

## Purpose

Evidence Validation determines whether material claims are supported. It
follows Editorial Discernment and implements stages 3 and 4 of the
Editorial Integrity Pipeline.

## Responsibilities

The runtime:

- classifies claims without presenting assertions as verified facts;
- records attributable support, contradiction, and context;
- counts independent source groups rather than repeated reporting;
- exposes missing, weak, conflicting, undated, and outdated evidence;
- assigns internal LMHS Editorial Risk;
- translates that assessment into Author-facing Editorial Confidence; and
- provides a proportionate recommended action.

## Verification Boundary

A source identifier is not proof. Two records derived from the same
reporting origin are one independent source group. A claim is Verified
only when at least two credible independent groups support it and no
credible contradiction is recorded.

Provider or network research remains outside this deterministic core.
Integrations must supply attributable evidence records and must never
fabricate a source, citation, date, quotation, or verification result.

## Temporal Integrity

Time-sensitive claims record whether supporting evidence is Current,
Review Required, Outdated, or Undated. The one-year default is a
conservative implementation threshold, not a universal truth claim;
callers may later supply domain-specific policy without weakening the
requirement to revalidate before publication.

## Publication Gate

Low and Moderate risk may support a publication recommendation. High and
Severe risk do not. Severe risk requires a defensible alternative rather
than silent continuation.
