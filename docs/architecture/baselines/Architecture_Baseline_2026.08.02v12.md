# Architecture Baseline - 2026.08.02v12

## Status

Current delivered architecture baseline. Capability 010 was delivered by PR
#46.

## Baseline ID

`2026.08.02v12`

## Supersedes

`2026.08.02v11`

## Reason for Revision

Add the provider-independent Hero Visual System and the narrow Publication
Package attachment boundary required for a validated 720 × 425 visual.

## Runtime Architecture

- `studio/hero_visual.py` owns request validation, policy constraints, provider
  selection, artifact validation, provenance, and explicit outcome states.
- `HeroVisualProvider` is the stable provider-neutral generation boundary.
- `DeterministicHeroVisualProvider` supplies an offline, repeatable PNG artifact
  for tests, demos, and repository validation.
- `studio/publication_package.py` attaches one existing result without invoking
  generation or modifying textual package content.

## Trust and Failure Model

Provider output is untrusted until the core verifies format, dimensions,
artifact presence, PNG header, and provenance. Malformed requests, unsupported
providers, generation failures, validation failures, and policy blocks remain
distinct and cannot be presented as ready.

## Explicit Exclusions

No Portable Editorial Project, project resume or export, workspace,
collaboration, orchestration, UI, publishing automation, release packaging,
B002, or Version 2 architecture is introduced.

## Architecture Decision

ADR-016 records the durable decision.
