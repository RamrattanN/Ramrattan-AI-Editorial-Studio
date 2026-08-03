# Capability 008 Demo - Editorial Discernment

## Objective

Demonstrate a Guided Editorial Session that protects editorial
coherence while preserving Author authority.

## Scenario 1 - Related Source

Current topic:

```text
AI governance in financial services
```

New material:

```text
A bank regulator's AI governance guidance
```

Expected:

- Alignment is Aligned or Related
- Current session continues
- No new session recommended

## Scenario 2 - Separate Publication

Current topic:

```text
AI governance in financial services
```

New material:

```text
Leadership lessons from cricket
```

Expected:

- Separate Intent detected
- Current session preserved
- New Editorial Session recommended
- No silent merging

## Scenario 3 - Component Revision

Author says:

```text
I do not like this CTA.
```

Expected:

- CTA is the affected component
- Other approved components remain protected
- No unrelated regeneration

## Scenario 4 - Ambiguous Rejection

Author says:

```text
I do not like this.
```

Expected:

- One concise clarification question
- No speculative question chain

## Scenario 5 - Abort

Author says:

```text
Abort this session.
```

Expected:

- Workspace State becomes Aborted
- Approvals remain preserved
- Provenance remains preserved
- Resume remains possible

## Scenario 6 - Scope Expansion

New material is related but changes the article from one product to
an industry-wide comparison.

Expected:

- Diverging classification
- Scope expansion made explicit
- Author chooses broaden, preserve, or new session

## Completion

Capability 008 passes when the Studio protects coherence without
taking publication authority away from the Author.
