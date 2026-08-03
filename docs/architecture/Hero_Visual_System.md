# Hero Visual System

## Status

Capability 010 executable architecture.

## Responsibility

The Hero Visual System consumes the approved Hero Visual prompt from the
Capability 009 Publication Package and returns either a validated 720 × 425
PNG artifact or one explicit failure state. It preserves the prompt and visual
intent and never reports success when generation or validation fails.

## Provider Boundary

`HeroVisualProvider` is the stable provider-neutral interface. Providers return
untrusted artifact bytes, dimensions, format, and provenance. The core system
validates every response independently before it can become `ready`.

The repository includes `DeterministicHeroVisualProvider` for tests, demos,
offline validation, and repeatable generation. It uses only the Python standard
library and requires no network access.

## Output Contract

A ready Hero Visual requires:

- width `720`;
- height `425`;
- PNG format;
- a non-empty PNG artifact whose header dimensions match the contract;
- provider name and version provenance;
- `ready` generation status; and
- `passed` validation status.

The runtime distinguishes ready, generation failed, validation failed,
unsupported provider, malformed request, and policy/editorial blocking.

## Publication Package Boundary

The Publication Package begins with a pending Hero Visual state. It may attach
one existing `HeroVisualResult` whose prompt matches the approved package
prompt. Attachment never invokes a provider, regenerates textual content, or
changes an approved article. Ready, failed, and blocked states remain distinct.

## Policy and Brand Neutrality

Brand-neutral generation is the default. Logo, recognizable-face, or text
overlay requests are blocked unless the request contract explicitly permits
the relevant category. Logo use additionally requires explicit approved brand
context. The B001 brand masters are neither inputs nor outputs of this system.

## Explicit Boundaries

Capability 010 introduces no Portable Editorial Project, project resume or
export, workspace, collaboration, orchestration, UI, publication automation,
release packaging, or Version 2 behavior.
