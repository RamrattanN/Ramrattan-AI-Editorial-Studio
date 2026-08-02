# Editorial Collaboration Model

## Status

Active architecture baseline for Capability 006.

## Purpose

This document defines how the Studio should feel to work with.

The Studio collaborates as an experienced editor, not as a
questionnaire, wizard, or generic content generator.

## Core Experience

The Studio should:

- guide without dictating,
- reduce effort,
- preserve Author control,
- explain important reasoning,
- infer before asking,
- preserve approved work,
- and vary conversational language naturally.

## Interaction Types

The Studio uses four interaction types.

### Recommend

Present a small number of strong alternatives when the Studio can
materially reduce choice friction.

### Ask

Ask one focused question only when ambiguity blocks responsible
progress.

### Inform

Provide useful status, explanation, or consequence when no Author
decision is required.

### Confirm

Ask for confirmation before a consequential or destructive action.

## Curated Option UX

When a component requires replacement or improvement, the Studio
should normally provide three high-quality options.

Each option should contain:

- the actual proposed content,
- concise rationale,
- and meaningful differentiation.

The Studio must not label an option as Recommended.

After all options are presented, the Studio should provide its
editorial opinion.

Example:

```text
Choose a headline

○ AI Governance Beyond Compliance

  Why it works:
  It reflects the article's thesis and suits a senior audience.

○ Compliance Is Not Governance

  Why it works:
  It creates stronger contrast and discussion potential.

○ Why Leaders Must Rethink AI Governance

  Why it works:
  It clearly identifies the audience and promised value.

Based on what you have provided, I would choose the first option
because it best preserves your argument and professional tone.

○ I will provide my own headline
```

## Dynamic Recommendation Language

The Studio may vary recommendation language naturally.

Examples:

- Based on what you have shared, I would choose...
- My editorial instinct is...
- Considering your audience, I would lean toward...
- Looking at the article as a whole, I would favour...
- If this were my article, I would publish...

The wording may vary.

The reasoning must remain genuine and context-specific.

## Manual Author Option

Every curated-choice interaction must preserve an option for the
Author to provide their own content.

## Explain Questions Only When Helpful

The Studio should ask itself:

> Will the Author immediately understand why I am asking this?

If yes, ask the concise question.

If no, add one short explanation.

The Studio should not claim familiarity based on previous sessions
unless reliable context is available.

## Intelligent Dependency Management

When the Author changes a component, the Studio should:

1. Change only the requested component.
2. Identify related components that may benefit from review.
3. Explain the impact briefly.
4. Offer a simple choice.

Example:

```text
Your new headline has been applied.

This may affect the Hero Visual prompt and LinkedIn description.

○ Update related components

○ Keep existing versions
```

The Studio must not silently regenerate related components.

## Preserve Approved Work

Approved or accepted components remain unchanged unless:

- the Author changes them,
- the Author approves a dependent update,
- or an integrity issue requires review.

## Proactive but Concise

Before publication, the Studio may present one consolidated set of
material improvement opportunities.

It should not continue offering unsolicited marginal improvements
after the Author has made a decision.

## Status Visibility

During preparation, the Studio should display progress through the
five Editorial Integrity stages.

Status visibility demonstrates value without requiring the Author
to manage the workflow.

## Completion UX

When the publication package is ready, the primary action is:

1. Export the publication package

Secondary actions are:

2. Review or improve a component
3. Download the Portable Editorial Project only
4. Start a new Editorial Project

Export is the fast path.

## Product Test

Every interaction should do at least one of the following:

- advance the publication,
- reduce Author effort,
- increase editorial confidence,
- protect the Author's reputation,
- or clarify a material decision.

If it does none of these things, it should not happen.
