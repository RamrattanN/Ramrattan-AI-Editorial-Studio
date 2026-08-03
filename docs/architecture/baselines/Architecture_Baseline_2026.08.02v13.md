# Architecture Baseline - 2026.08.02v13

## Status

Proposed during Capability 011. Becomes current only when Capability 011 is
delivered.

## Baseline ID

`2026.08.02v13`

## Supersedes

`2026.08.02v12`

## Reason for Revision

Add the narrow RC1 Portable Editorial Project serialization, validated resume,
download, and deterministic optional ZIP boundary.

## Runtime Architecture

- `studio/portable_editorial_project.py` owns schema validation, Markdown
  serialization, VCM filenames, explicit load/resume states, downloads, and
  deterministic ZIP construction.
- `InputKind.PORTABLE_EDITORIAL_PROJECT` remains the intake classification.
- `EditorialSession.resume()` remains the lifecycle transition and is invoked
  only after project validation.
- Temporal Integrity review is mandatory on resume; older saved dates are
  explicitly stale.
- `studio/publication_package.py` attaches one validated project without
  changing approved article or Hero Visual results.

## Trust and Failure Model

Schema version 1 accepts only current runtime state. Malformed Markdown/JSON,
unsupported versions or fields, invalid values, stale projects, missing visual
downloads, unresolved blockers, filename exhaustion, and invalid session
transitions remain explicit and fail closed where continuation is unsafe.

## Explicit Exclusions

No Adaptive Editorial Context, Integrated Editorial Workspace, collaboration,
orchestration API, UI, hosted storage, publishing automation, release
packaging, rich legacy source/history/publication fields, or Version 2 behavior
is introduced.

## Architecture Decision

ADR-017 records the durable decision.
