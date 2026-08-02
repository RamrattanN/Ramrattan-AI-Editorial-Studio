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

<!-- CAPABILITY_006_DECISION_LOG_START -->

## Capability 006 Decisions

| Date | Level | Decision | Rationale |
|---|---:|---|---|
| 2026-08-01 | D5 | Define Version 1.0 explicitly | Future backlog decisions require a stable release boundary. |
| 2026-08-01 | D4 | Adopt the Editorial Integrity Pipeline | The Studio must assess sources and evidence before publication recommendation. |
| 2026-08-01 | D3 | Display five visible processing stages | The Author should understand and appreciate the work being performed. |
| 2026-08-01 | D3 | Adopt LMHS Editorial Risk | Low, Moderate, High, and Severe communicate risk without false precision. |
| 2026-08-01 | D4 | Prohibit knowing dissemination of materially false information | Truthfulness and Author reputation are non-negotiable. |
| 2026-08-01 | D3 | Use proportionate challenge, rebuild, redirection, and refusal | Refusal is reserved for scenarios where responsible recovery is not possible. |
| 2026-08-01 | D3 | Offer three curated alternatives | Three options reduce blank-page effort without overwhelming the Author. |
| 2026-08-01 | D3 | Place recommendation after all options | Editorial advice should not bias evaluation before the Author sees the alternatives. |
| 2026-08-01 | D3 | Always allow an Author-provided option | The Studio reduces effort without reducing control. |
| 2026-08-01 | D3 | Use intelligent dependency management | Requested components change first; related updates require Author approval. |
| 2026-08-01 | D3 | Place Export first at completion | Export is the Author's primary fast path after successful generation. |
| 2026-08-01 | D3 | Support host-compatible audio and video intake | The Product should meet the Author where their ideas naturally exist. |
| 2026-08-01 | D3 | Use host context only when reliably available | Personalization is optional and must never become a correctness dependency. |
| 2026-08-01 | D4 | Version architecture baselines using VCM | Architecture history should follow the established YYYY.MM.DDvNN convention. |

## Active Architecture Baseline

```text
2026.08.01v01
```

## Capability 006 Learning

Editorial Integrity is not a hidden back-end check.

It is a visible Author experience that demonstrates how the Product
protects factual quality, publication readiness, and professional
reputation.

<!-- CAPABILITY_006_DECISION_LOG_END -->

<!-- CAPABILITY_006A_DECISION_LOG_START -->

## Capability 006A Decisions

| Date | Level | Decision | Rationale |
|---|---:|---|---|
| 2026-08-01 | D5 | Adopt the Constitutional Layer | Enduring principles require a governing layer above Product and Architecture. |
| 2026-08-01 | D5 | Freeze the Constitution for Version 1.0 | Implementation should test the design before further foundational change. |
| 2026-08-01 | D4 | Adopt the Human Collaboration Model | Author, Editor, and Reader have distinct responsibilities. |
| 2026-08-01 | D4 | Adopt Editorial Confidence as Author-facing | The Author needs a positive publication-readiness outcome while internal risk remains visible when useful. |
| 2026-08-01 | D4 | Retain LMHS Editorial Risk internally | Risk remains necessary for editorial judgement and governance. |
| 2026-08-01 | D4 | Adopt Reader Experience Principles | Publications should create Reader value rather than superficial engagement. |
| 2026-08-01 | D4 | Adopt component-based collaboration | Any publication component may be revised independently. |
| 2026-08-01 | D4 | Require approval before dependent regeneration | Approved work must not be silently replaced. |
| 2026-08-01 | D4 | Adopt the Editorial Language Framework | Recurring language should remain consistent in purpose but varied in wording. |
| 2026-08-01 | D4 | Adopt the Editorial Fingerprint | The Editor is defined by professional behaviour rather than repeated phrases. |
| 2026-08-01 | D4 | Adopt the Canonical Editorial Session | Version 1.0 requires an end-to-end behavioural acceptance demonstration. |
| 2026-08-01 | D4 | Adopt Constitutional Impact Review | Significant changes must assess impact on governing documents. |
| 2026-08-01 | D3 | Adopt the motto | Trust earned. Confidence shared. Conversations inspired. |
| 2026-08-01 | D4 | Create Architecture Baseline 2026.08.01v02 | The same-day VCM revision records the Constitutional Freeze. |

<!-- CAPABILITY_006A_DECISION_LOG_END -->

<!-- CAPABILITY_007_DECISION_LOG_START -->

## Capability 007 Decisions

| Date | Level | Decision | Rationale |
|---|---:|---|---|
| 2026-08-01 | D4 | Adopt Canonical Vocabulary | One concept should have one active name. |
| 2026-08-01 | D4 | Establish Editorial Workspace | The Author needs one coherent environment across the Canonical Editorial Session. |
| 2026-08-01 | D4 | Define Editorial Intake as the first Workspace capability | Intake is a capability, not the complete experience. |
| 2026-08-01 | D3 | Infer input type before asking | The Author should not manage technical classification. |
| 2026-08-01 | D4 | Support optional logo and headshot assets | Authors may personalise Hero Visuals without changing the default path. |
| 2026-08-01 | D4 | Require identity-asset rights confirmation | The Studio should not use assets without Author authority. |
| 2026-08-01 | D4 | Preserve brand-neutral as the default | Identity assets are enhancements, not requirements. |
| 2026-08-01 | D4 | Permit resume without original identity assets | Portable projects must not depend on separately stored binary assets. |
| 2026-08-01 | D4 | Create Architecture Baseline 2026.08.01v03 | Version 1.0 runtime implementation begins. |

<!-- CAPABILITY_007_DECISION_LOG_END -->

<!-- CAPABILITY_DELIVERY_DECISION_LOG_START -->

## Capability Delivery Workflow Decisions

| Date | Level | Decision | Rationale |
|---|---:|---|---|
| 2026-08-01 | D4 | Adopt a repeatable Capability Delivery Workflow | Previously solved procedural problems recurred. |
| 2026-08-01 | D4 | Require exact paste-ready commands | Unresolved placeholders caused avoidable shell errors. |
| 2026-08-01 | D4 | Detect existing branches before creation | Existing branches should be resumed, not recreated. |
| 2026-08-01 | D4 | Require partial-apply recovery | Validation failures must not force repository reset. |
| 2026-08-01 | D4 | Reuse existing GitHub issues and pull requests | Duplicate planning artifacts reduce trust. |
| 2026-08-01 | D4 | Retry delayed Project item propagation | GitHub Project items may not appear immediately. |
| 2026-08-01 | D4 | Require CI before merge | Local success does not replace repository checks. |
| 2026-08-01 | D4 | Require return-to-develop verification | A capability is incomplete while repository state remains ambiguous. |
| 2026-08-01 | D4 | Create Architecture Baseline 2026.08.01v04 | The engineering delivery process is now part of the architecture baseline. |

<!-- CAPABILITY_DELIVERY_DECISION_LOG_END -->
