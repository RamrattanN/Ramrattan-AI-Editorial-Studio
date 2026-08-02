# Article Engine and Publication Package

## Status

Capability 009 executable architecture.

## Responsibilities

The Article Engine consumes explicit Author-owned editorial inputs and
the completed Evidence Validation report. It preserves the approved
Editorial Intent, refuses High or Severe Editorial Risk, requires
attribution for evidence used, and delegates language construction
through a provider-independent interface.

The Publication Package builder assembles and validates the textual
package: Hero Visual prompt, headline, hook, one or two insights,
practical takeaway, CTA, source and attribution, hashtags, LinkedIn
Description, article Markdown, and the existing Editorial Confidence
and Editorial Risk result.

## Boundaries

Capability 009 does not add an Integrated Editorial Workspace,
Adaptive Editorial Context runtime, Component Collaboration, stable
Author-facing orchestration API, or final integrated Editorial
Confidence presentation.

A rendered Hero Visual remains Capability 010. Portable Editorial
Project serialization and export remain Capability 011. The runtime
represents both as deferred and never reports the complete Version 1.0
package while they are absent.

## Provider Independence

`ArticleDraftProvider` is the only article-language provider boundary.
The repository includes a deterministic provider that structures
approved Author material without network access or source imitation.
Future providers must obey the same intent, evidence, attribution, and
publication-gate validations.

## Dependencies

Capability 009 depends only on the existing Evidence Validation report
and canonical editorial vocabulary. It introduces no persistence,
ingestion, UI, Hero Visual generation, Portable Project, collaboration,
or orchestration dependency.
