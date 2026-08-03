# Publication Package Contract

## Status

Active Version 1.0 product contract.

## Purpose

The Publication Package Contract defines the complete article
output delivered by Ramrattan AI Editorial Studio.

## Default Package Components

Every complete Version 1.0 publication package contains:

1. Hero Visual prompt
2. Hero Visual - 720 × 425
3. Headline
4. Hook
5. Insight 1
6. Insight 2 when editorially useful
7. Practical Takeaway
8. Call to Action
9. Source and attribution
10. Hashtags
11. LinkedIn Description
12. Portable Editorial Project

## Article-First Scope

The package supports professional articles.

Carousel output is not part of Version 1.0.

## Presentation

The Studio presents:

- the Hero Visual,
- followed by text with clear headings,
- followed by the Editorial Risk result,
- followed by next actions.

## Internal Consistency

The package should maintain alignment between:

- thesis,
- headline,
- hook,
- insights,
- practical takeaway,
- CTA,
- Hero Visual,
- source attribution,
- hashtags,
- and LinkedIn Description.

## Independent Revision

Components may be reviewed and revised independently.

A change does not automatically regenerate the complete package.

## Export Fast Path

The first completion action is:

> Export the publication package

The standard export should include:

- article Markdown,
- Hero Visual,
- Portable Editorial Project,
- and selected supporting metadata.

An optional ZIP package may bundle the selected files.

## Copy and Download

The Product may support:

- Copy Article
- Download Article
- Copy Hero Visual
- Download Hero Visual
- Download Portable Editorial Project
- Export ZIP

The Author chooses where downloaded files are stored.

The Product does not require storage paths.

## Completion Statement

A suitable completion message is:

> Your publication package is ready.

The Product should then present the export fast path and the
secondary actions.

<!-- CAPABILITY_009_PUBLICATION_PACKAGE_CONTRACT_START -->

## Capability 009 Implementation Boundary

Capability 009 implements the Article Engine and the textual
Publication Package: Hero Visual prompt, headline, hook, one or two
insights, practical takeaway, CTA, source and attribution, hashtags,
LinkedIn Description, article Markdown, Editorial Confidence, and
LMHS Editorial Risk.

A rendered Hero Visual remains Capability 010. Portable Editorial
Project serialization remains Capability 011. The Capability 009
runtime records both as deferred and must not report the complete
Version 1.0 package while they are absent.

<!-- CAPABILITY_009_PUBLICATION_PACKAGE_CONTRACT_END -->

<!-- CAPABILITY_010_PUBLICATION_PACKAGE_CONTRACT_START -->

## Capability 010 Hero Visual Boundary

The Hero Visual System consumes the approved Hero Visual prompt and returns a
validated 720 × 425 PNG or an explicit generation, validation, provider,
request, or policy failure.

The Publication Package begins with a pending Hero Visual state and may attach
one existing result whose prompt matches the approved package prompt. Attachment
does not invoke generation, modify textual components, or silently replace an
already attached result. Ready, failed, and blocked states remain distinct.

Portable Editorial Project serialization, resume, and export remain Capability
011. The complete Version 1.0 package remains incomplete until that capability
and release-readiness evidence are delivered.

<!-- CAPABILITY_010_PUBLICATION_PACKAGE_CONTRACT_END -->
