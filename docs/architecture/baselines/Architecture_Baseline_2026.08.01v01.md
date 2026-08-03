# Architecture Baseline - 2026.08.01v01

## Status

Active Version 1.0 architecture baseline.

## Baseline Version

```text
2026.08.01v01
```

## Purpose

This document records the coherent architecture supporting the
target Version 1.0 release.

It is a checkpoint, not a substitute for detailed architecture
documents or ADRs.

## Capabilities Included

- Repository Foundation
- Editorial Workflow Prototype - historical
- Adaptive Product Foundation
- Article-First Alignment
- Adaptive Editorial Context
- Portable Editorial Projects
- Editorial Integrity Pipeline
- Editorial Judgment Framework
- Editorial Collaboration Model
- Publication Package Contract
- Version 1.0 Product Release Definition

## Major Decisions

- The Product is article-first.
- The Hero Visual is 720 × 425.
- The Adaptive Editorial Context is the system kernel.
- The Studio is stateless by default.
- Portable Editorial Projects preserve continuity.
- The Product does not require external storage paths.
- Editorial Integrity precedes publication recommendation.
- LMHS communicates Editorial Risk.
- The Studio challenges unsupported assumptions constructively.
- Export is the completion fast path.
- Carousel generation is excluded from Version 1.0.

## Related ADRs

- ADR-001 - Historical workflow decision
- Adaptive Editorial Context architecture - `docs/architecture/Editorial_Context_Model.md`
- ADR-003 - Article-First Publication Package
- ADR-004 - Portable Editorial Projects
- ADR-005 - Editorial Integrity Pipeline

## Supersedes

This baseline supersedes earlier informal architecture summaries.

Earlier ADRs and product records remain available for historical
traceability.

## Compatibility

Future architecture changes must:

- preserve Portable Editorial Project compatibility where practical,
- provide schema migration when required,
- preserve Author ownership,
- and identify any breaking Version 1.0 contract change explicitly.
