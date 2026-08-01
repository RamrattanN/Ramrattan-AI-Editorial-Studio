# Product Decision Log

This log records significant product decisions.

Technical architecture decisions remain documented separately as
Architecture Decision Records.

## Product Foundation Decisions

| Date | Level | Decision | Rationale |
|---|---:|---|---|
| 2026-08-01 | D5 | Treat the Studio as an adaptive editorial partner | The product should help Authors develop ideas rather than merely generate content. |
| 2026-08-01 | D5 | Replace URL-first positioning | A URL is one possible input, not the product's organizing concept. |
| 2026-08-01 | D5 | Replace rigid workflow thinking with an editorial conversation | Creative work loops, branches, and changes direction. |
| 2026-08-01 | D4 | Introduce an evolving Editorial Context | The product requires continuity across non-linear revisions. |
| 2026-08-01 | D3 | Treat Author perspective as a first-class input | Thought leadership depends on interpretation, not source summary alone. |
| 2026-08-01 | D3 | Infer intent before presenting intake options | Premature categorization creates unnecessary friction. |
| 2026-08-01 | D3 | Preserve reversibility after approval | Authors must remain able to change direction mid-flight. |
| 2026-08-01 | D2 | Use options only at genuine decision points | Options should accelerate the conversation rather than control it. |
| 2026-08-01 | D2 | Use the term Author rather than user | The terminology reinforces ownership and the Studio's supporting role. |

## Decision Levels

- **D1 - Cosmetic:** Wording, formatting, or naming.
- **D2 - Interaction:** Changes how an Author works with the Studio.
- **D3 - Capability:** Adds or changes a major product ability.
- **D4 - Architecture:** Changes the structural product model.
- **D5 - Philosophy:** Changes what the product fundamentally is.

## Article-First Alignment Decisions

| Date | Level | Decision | Rationale |
|---|---:|---|---|
| 2026-08-01 | D5 | Adopt professional articles as the active publishing scope | Focus increases product clarity and reduces premature multi-format complexity. |
| 2026-08-01 | D4 | Treat the 720 × 425 Hero Visual as part of the article publication package | The visual communicates the article thesis and is not an unrelated output. |
| 2026-08-01 | D3 | Establish approximately 10 minutes as the target for the first publication-ready package | Time to useful output is a primary product measure when sufficient material exists. |
| 2026-08-01 | D3 | Reject insufficient starting material constructively | The Studio should not disguise weak foundations with generic prose. |
| 2026-08-01 | D3 | Adopt Author Library as the name for durable work storage | The capability preserves and recalls an Author's evolving body of work. |
| 2026-08-01 | D2 | Retain infographic as an accepted conversational synonym for Hero Visual | Familiar language should not create friction, while architecture uses one stable term. |

<!-- CAPABILITY_005_DECISION_LOG_START -->

## Capability 5 Decisions

| Date | Level | Decision | Rationale |
|---|---:|---|---|
| 2026-08-01 | D5 | Make the Adaptive Editorial Context the system kernel | Every capability requires one shared and revisable representation of the Author's evolving work. |
| 2026-08-01 | D4 | Adopt Portable Editorial Projects | Small Author-owned files provide continuity without hosted-storage complexity. |
| 2026-08-01 | D4 | Make the Studio stateless by default | The Author retains custody while the product avoids unnecessary account, storage, privacy, and tenancy scope. |
| 2026-08-01 | D3 | Do not require external file paths | Storage location is the Author's concern and is not required for project resumption. |
| 2026-08-01 | D3 | Add Start New and Resume Existing as opening actions | Resumption must be a first-class experience rather than an afterthought. |
| 2026-08-01 | D3 | Adopt VCM format YYYY.MM.DDvNN | The established method gives human-readable daily version management. |
| 2026-08-01 | D3 | Limit generated filenames to 255 characters | The safer legacy-compatible maximum protects portability. |
| 2026-08-01 | D3 | Preserve durable source context | URLs may expire, move, or change and cannot be the only retained source information. |
| 2026-08-01 | D3 | Preserve paywalled excerpts selectively | The project should retain editorial value without automatically archiving complete paywalled works. |
| 2026-08-01 | D3 | Explain the future value of the project file to the Author | The Author must understand that saving context reduces future repetition. |
| 2026-08-01 | D4 | Make Editorial Integrity a first-class context component | Responsible publication requires more than generic platform safety. |
| 2026-08-01 | D2 | Require a Capability Demo in the Definition of Done | Product progress must be demonstrable to stakeholders and future contributors. |

## Capability 5 Learning

A hosted Author Library is not required to provide high-value
continuity.

The Product also does not need to know where the Author saves
downloaded files.

A few kilobytes of well-structured, Author-owned context can
preserve enough knowledge to resume an article project.

The durable value of a source is its evidence, metadata,
interpretation, and editorial significance, not merely its URL.

<!-- CAPABILITY_005_DECISION_LOG_END -->
