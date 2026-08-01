> **Historical prototype notice**
>
> This package represents the earlier linear workflow experiment.
> It is retained for engineering traceability and test coverage.
>
> It is not the current product architecture.
>
> The active product is article-first and uses an adaptive Editorial
> Context. Earlier carousel concepts in this prototype are not part
> of the current product scope.
# Editorial Workflow System

## Purpose

The workflow system coordinates the complete editorial journey
without embedding generation logic in one monolithic prompt.

The central principle is:

> The workflow controls the AI, not the other way around.

## Responsibilities

The package is responsible for:

- Representing editorial session state
- Defining selectable user choices
- Enforcing valid workflow transitions
- Preserving approved work
- Resetting only affected downstream work
- Supporting backward navigation
- Supporting future save-and-resume behavior

It is not responsible for:

- Fetching source pages
- Generating editorial copy
- Generating images
- Publishing to LinkedIn
- Rendering interface components

Those capabilities will be supplied by separate engines.

## Package Structure

```text
studio/workflow/
├── __init__.py
├── choices.py
├── state.py
└── workflow.py
```

## Workflow Stages

```text
START
  ↓
SOURCE_ANALYZED
  ↓
CONTENT_TYPE_SELECTED
  ↓
VISUAL_STYLE_SELECTED
  ↓
HERO_COPY_SELECTED
  ↓
GRAPHIC_GENERATED
  ↓
GRAPHIC_APPROVED
  ↓
WRITTEN_CONTENT_GENERATED
  ↓
FINAL_REVIEW
  ↓
COMPLETE
```

## State Preservation

Moving backward does not immediately delete approved work.

Changing an earlier decision clears only the assets that depend
on that decision.

Examples:

- Changing a color palette does not rewrite the article.
- Changing the visual style clears hero copy and visual assets.
- Changing the content type clears visual and written assets.
- Restarting clears the complete session.

## Example

```python
from studio.workflow import (
    ContentType,
    EditorialWorkflow,
    HeroCopyDirection,
    VisualStyle,
)

workflow = EditorialWorkflow()

workflow.analyze_source(
    source_url="https://example.com/article",
    strongest_insight="Remote work changes occupancy economics.",
    supporting_statistic="$200 per month",
    provocative_claim=(
        "Utility models were not designed for remote work."
    ),
)

workflow.choose_content_type(ContentType.ARTICLE)

workflow.choose_visual_style(
    VisualStyle.EXECUTIVE_EDITORIAL
)

workflow.choose_hero_copy(
    direction=HeroCopyDirection.RECOMMENDED,
    headline=(
        "Remote Work Is Reshaping Rental Economics"
    ),
    supporting_text=(
        "Higher daytime occupancy is changing utility costs."
    ),
)
```

## Why This Matters

A structured workflow makes prompt behavior testable,
comprehensible, and replaceable.

The AI model may change. The product journey should remain stable.
