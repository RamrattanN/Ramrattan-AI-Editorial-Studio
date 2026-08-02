# Capability 008 Demo - Evidence Validation and Editorial Risk

## Problem

The Studio could assess sources and protect Editorial Intent, but could not
yet distinguish an assertion from a verified fact, compare independent
support, expose stale evidence, or produce an executable publication gate.

## What Changed

The Studio now classifies claims, corroborates attributable evidence,
preserves contradictions, checks Temporal Integrity, assigns internal LMHS
Editorial Risk, and translates it into Author-facing Editorial Confidence.

## Example

```text
Material factual claim
          |
          v
two independent credible sources? -- no --> strengthen or qualify
          |
         yes
          v
current and uncontradicted? -------- no --> revalidate or rebuild
          |
         yes
          v
Low Editorial Risk -> Ready for publication
```

Repeated copies of one wire report count as one source group. A credible
contradiction remains visible and prevents a false Verified result.

## Author Benefit

The Author receives a concise readiness conclusion and a specific next
action. Internal mechanics remain available as supporting detail without
replacing Editorial Confidence.

## Acceptance Evidence

Behavioural tests cover claim classification, independent corroboration,
contradiction, time-sensitive evidence, every LMHS level, publication
gating, and the absence of percentage-based false precision.

## Learning

Corroboration is a provenance relationship, not a source count. Recording
independence explicitly prevents repeated reporting from manufacturing
confidence.

## Next

Capability 009 can consume the validated report when building the Article
Engine and Publication Package.
