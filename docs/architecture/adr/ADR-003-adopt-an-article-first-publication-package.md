# ADR-003 - Adopt an Article-First Publication Package

## Status

Accepted

## Date

2026-08-01

## Decision Level

D5 - Product philosophy and scope

## Context

Earlier product definitions included both articles and carousels.

The expanded scope risked turning the Studio into a general-purpose
content-production system before it had become exceptional at its
primary job.

The intended product outcome is a professional article supported by
a purpose-built 720 × 425 LinkedIn Hero Visual.

## Decision

The current product scope will focus on professional articles.

Each completed work will be represented as an article publication
package containing:

- Hero Visual - 720 × 425
- Headline
- Publication-ready article
- Source attribution
- Supporting publication copy
- Publication metadata

Carousels are removed from the active roadmap.

Historical carousel concepts may remain in the workflow prototype
for traceability until that prototype is replaced by the adaptive
Editorial Context architecture.

## Time-to-Value

When sufficient starting material exists, the Studio should aim to
produce the first publication-ready article package within
approximately 10 minutes.

## Input Quality

The Studio will not generate generic filler from insufficient
material.

It will explain the limitation, identify what is missing, provide a
stronger example, and recommend one next action.

## Hero Visual

The Hero Visual is part of the article rather than an independent
publishing format.

Its purpose is to communicate the article's thesis visually.

## Consequences

### Positive

- Clearer product identity
- Smaller and more coherent scope
- Stronger article-specific data model
- Better alignment between article and visual
- Easier quality measurement
- Reduced implementation complexity
- Faster path to a differentiated product

### Costs and Risks

- Carousel capability is deferred
- Historical prototype code requires clear labelling
- Future formats require explicit product decisions
- LinkedIn-specific Hero Visual requirements remain part of the
  initial publication package

## Outcome

Accepted as the active product scope and architectural direction.
