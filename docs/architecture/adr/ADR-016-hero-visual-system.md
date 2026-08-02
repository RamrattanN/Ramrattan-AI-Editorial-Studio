# ADR-016 - Hero Visual System

## Status

Proposed during Capability 010. Becomes Accepted when the capability is
delivered.

## Date

2026-08-02

## Decision Level

D4 - Architecture

## Context

Capability 009 produces an approved Hero Visual prompt but intentionally does
not render an image. Version 1 requires a 720 × 425 Hero Visual while repository
validation must remain deterministic, offline, and independent of any external
generation service.

## Decision

Adopt one provider-independent Hero Visual System. The core validates requests,
applies explicit policy constraints, invokes a selected provider, validates the
returned artifact and provenance, and exposes distinct success and failure
states.

Require a 720 × 425 PNG output contract for Version 1. Include an offline
deterministic provider for tests and demonstrations. Treat every provider
response as untrusted until core validation passes.

Integrate with the Publication Package only by attaching one existing result
whose prompt matches the approved Capability 009 prompt. Do not silently invoke
a provider, regenerate approved content, or claim Portable Project completion.

## Constitutional Impact

The decision implements Understanding Before Generation, Evidence Before
Assertion, Trust Above All, Professional Judgement, Author ownership, and
approved-component preservation. It changes no frozen constitutional principle
or canonical term.

## Alternatives Considered

### Require one external image provider

Rejected because validation would depend on network access, credentials, and
provider availability, and provider behavior could leak into the core contract.

### Trust provider metadata without validating the artifact

Rejected because dimensions, format, content availability, and provenance must
be verified rather than asserted.

### Generate the visual during Publication Package assembly

Rejected because it would silently couple package construction to generation
and make focused revision and failure recovery unsafe.

### Implement Portable Project or UI behavior simultaneously

Rejected because those are later or separate product surfaces and would expand
Capability 010 beyond its approved boundary.

## Consequences

The repository can deterministically demonstrate and validate Hero Visual
generation without an external service. Future providers may implement the
same boundary without changing Publication Package semantics. Version 1 remains
incomplete until Capability 011 and end-to-end release-readiness work complete.

## Architecture Baseline

Recorded by Architecture Baseline `2026.08.02v12`.
