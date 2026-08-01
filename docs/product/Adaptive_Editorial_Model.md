# Adaptive Editorial Model

## Overview

The Studio does not ask:

> Which step comes next?

It asks:

> What is the Author trying to accomplish now, and what is the most
> useful editorial action?

## Editorial Context

```text
Editorial Context
├── Author intent
├── Source material
├── Observations
├── Author perspectives
├── Supporting notes
├── Constraints
├── Candidate angles
├── Current editorial angle
├── Evidence
├── Unresolved questions
├── Hero copy
├── Visual concepts
├── Draft assets
├── Approvals
├── Revision history
└── Publication package
```

## Continuous Interpretation

Each Author contribution may represent:

- new evidence,
- a new idea,
- a changed opinion,
- a correction,
- an approval,
- a rejection,
- a new constraint,
- a research request,
- an asset revision,
- or a change in creative direction.

The Author does not need to label the event.

## Dependency Awareness

Examples:

- Changing a palette should not rewrite the article.
- Changing a headline may require a revised hook.
- Changing the central argument may require new evidence, hero copy,
  written content, and CTA.
- A new source may strengthen the current angle without changing the
  visual.
- Changing from article to carousel may preserve evidence,
  perspective, and central argument.

## Revision Behaviour

When direction changes, the Studio should:

1. Identify what changed.
2. Determine which components depend on it.
3. Preserve unaffected components.
4. Mark conflicting components for revision.
5. Propose the most useful next action.
6. Retain recoverable history where practical.

## Existing Workflow Prototype

The current `studio.workflow` package represents an earlier linear
state-machine experiment.

It remains available as a reference but is not the final product
interaction model.
