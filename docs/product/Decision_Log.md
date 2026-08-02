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
2026.08.01v06
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

<!-- CAPABILITY_008_DECISION_LOG_START -->

## Capability 008 Decisions

| Date | Level | Decision | Rationale |
|---|---:|---|---|
| 2026-08-01 | D4 | Adopt one Editorial Intent per Editorial Session | A publication must remain coherent and traceable. |
| 2026-08-01 | D4 | Adopt Editorial Discernment Engine internally | The Studio must interpret what new contributions mean. |
| 2026-08-01 | D4 | Use Editorial Guidance with Authors | Internal engine language should not dominate the Author experience. |
| 2026-08-01 | D4 | Adopt No Silent Scope Expansion | Material scope changes require Author awareness. |
| 2026-08-01 | D4 | Adopt Editorial Never Events | Unacceptable trust failures require explicit guardrails. |
| 2026-08-01 | D4 | Separate Workspace State from Stage State | Session lifecycle and work progress are different concerns. |
| 2026-08-01 | D4 | Distinguish Cancelled from Aborted | Deliberate Author cancellation differs from exceptional termination. |
| 2026-08-01 | D4 | Preserve aborted work | Interruption must not destroy provenance, approvals, or project history. |
| 2026-08-01 | D4 | Ask one clarification question | Minimise Author effort while avoiding unsafe assumptions. |
| 2026-08-01 | D4 | Create Architecture Baseline 2026.08.01v05 | Editorial Discernment becomes part of the Version 1.0 runtime baseline. |

<!-- CAPABILITY_008_DECISION_LOG_END -->

<!-- CAPABILITY_008A1_DECISION_LOG_START -->

## Capability 008A.1 Governance Decisions

| Date | Level | Decision | Rationale |
|---|---:|---|---|
| 2026-08-02 | D4 | Adopt explicit Governance Authority | Each governance concept requires one authoritative owner and deterministic precedence. |
| 2026-08-02 | D4 | Keep `AGENT_MEMORY.md` advisory | Chronological experience must not silently become policy or current status. |
| 2026-08-02 | D4 | Assign current-status responsibilities | Roadmap, scorecard, release definition, and architecture records answer different status questions. |
| 2026-08-02 | D4 | Do not recreate ADR-002 | No ADR-002 artifact exists in repository history; the broken reference is repaired to surviving architecture evidence. |
| 2026-08-02 | D4 | Retain Architecture Baseline 2026.08.01v06 | Governance clarification does not change executable architecture. |

ADR-011 records the durable governance decision.

<!-- CAPABILITY_008A1_DECISION_LOG_END -->

<!-- CAPABILITY_008A2_DECISION_LOG_START -->

## Capability 008A.2 Delivery Hardening Decisions

| Date | Level | Decision | Rationale |
|---|---:|---|---|
| 2026-08-02 | D4 | Fail closed on unavailable or ambiguous delivery evidence | Missing evidence cannot justify a protected transition. |
| 2026-08-02 | D4 | Observe remote heads directly | Cached remote-tracking references do not prove freshness. |
| 2026-08-02 | D4 | Model draft, review, mergeability, and checks independently | PRs #30, #31, and #33 exposed optimistic state collapse. |
| 2026-08-02 | D4 | Treat zero checks as unavailable | Repository policy requires canonical CI validation. |
| 2026-08-02 | D4 | Recover post-merge cleanup one step at a time | Merge success does not prove cleanup completed. |
| 2026-08-02 | D4 | Create Architecture Baseline 2026.08.01v07 | Delivery observation and recovery are durable engineering architecture. |

<!-- CAPABILITY_008A2_DECISION_LOG_END -->

<!-- CAPABILITY_009_DECISION_LOG_START -->

## Capability 009 Decisions

| Date | Level | Decision | Rationale |
|---|---:|---|---|
| 2026-08-02 | D4 | Limit Capability 009 to Article Engine and Publication Package | Issue #15, ROADMAP, scorecard, and Project planning define one coherent capability. |
| 2026-08-02 | D4 | Require a provider-independent draft boundary | Editorial invariants must not depend on one generation provider. |
| 2026-08-02 | D4 | Apply Evidence Validation before generation | High and Severe risk must not become polished publication content. |
| 2026-08-02 | D4 | Represent Capability 010 and 011 outputs as deferred | Partial product state must not be presented as the complete Version 1.0 package. |

ADR-015 and Architecture Baseline `2026.08.02v10` record the durable
architecture.

<!-- CAPABILITY_009_DECISION_LOG_END -->

<!-- CAPABILITY_010_DECISION_LOG_START -->

## Capability 010 Decisions

| Date | Level | Decision | Rationale |
|---|---:|---|---|
| 2026-08-02 | D4 | Adopt a provider-independent Hero Visual boundary | Visual-generation providers must not define the stable product contract. |
| 2026-08-02 | D4 | Validate every provider artifact in the core | Provider claims cannot substitute for verified dimensions, format, bytes, and provenance. |
| 2026-08-02 | D4 | Include an offline deterministic provider | Tests, demos, bootstrap recovery, and repository validation must not require network access. |
| 2026-08-02 | D4 | Attach results without implicit generation | Approved prompts and textual package components must not be silently regenerated. |

ADR-016 and proposed Architecture Baseline `2026.08.02v12` record the durable
architecture.

<!-- CAPABILITY_010_DECISION_LOG_END -->
