# Capability 013 - Reader Engagement

**Status:** Version 2 Candidate  
**Classification:** Product Discovery  
**Architecture:** Extends the Editorial Project lifecycle beyond publication  
**Governance Status:** Informative - Not Yet Approved for Implementation

## Vision

The useful lifecycle of an Editorial Project may not end at publication.
Real-use evidence shows that an Author returning to a completed
Editorial Project with reader replies or comments can be helped to
understand, contextualize, and respond to that discussion - because the
Studio already holds the article's editorial context.

## Discovery Evidence

This capability originates from real editorial use of the locked
private GPT (`GPT Recovery RC5 - Locked Private GPT Baseline`), recorded
in `product/validation/Product_Validation_Log.md` as PV-028 and promoted
in `product/validation/Product_Decisions.md` as DEC-027.

An Author created an article using Ramrattan AI Editorial Studio and
kept the original conversation available after publication. The Author
later received reader replies and supplied them back into that same
conversation. Because the conversation still held the article's
editorial context, the Studio could help the Author understand what the
reader was communicating, relate it back to the article's thesis and
evidence, and consider how to respond - value a fresh, context-free
conversation could not have provided.

This observed behavior depends on the original conversation remaining
available with its in-session context. It is not persistent cross-session
product memory, and this document does not treat it as such.

## Problem Statement

Version 1 and the current private GPT treat article generation and
delivery as the practical end of an editorial engagement. Real use shows
that publication is frequently followed by reader discussion the Author
still wants editorial help with, and that help is more valuable when it
is grounded in the article's actual thesis and evidence rather than
reconstructed from scratch in a new conversation.

## Candidate Lifecycle

The discovery motivates extending the Editorial Project lifecycle:

```text
Create -> Publish -> Engage
```

Documented here as one instance of the broader conceptual product
lifecycle this capability contributes to:

```text
Research -> Create -> Review -> Publish -> Engage -> Learn -> Next Article
```

This is a conceptual lifecycle for web-product discovery. The locked
private GPT is not required, and is not being asked, to implement every
state.

## Reader Engagement Concept

Reader Engagement extends the Editorial Project after publication around
four candidate jobs to be done.

### 1. Understand

Help the Author understand what a reader is actually communicating.
Possible interpretation categories include agreement, disagreement, a
question, a challenge, a misunderstanding, a clarification request,
additional evidence, an alternative perspective, professional
experience, or a potential new editorial idea. The product should
distinguish interpretation from verified fact rather than assume reader
intent with certainty.

### 2. Contextualize

Relate the reader's comment back to the article's thesis, specific
claims, evidence used, editorial framing, and the Author's intended
meaning. Identify when a reader introduces a new factual claim that may
require verification.

### 3. Response Strategy

Help the Author decide what kind of response, if any, is appropriate.
Candidate strategies include: acknowledge, clarify, respectfully
disagree, add evidence, ask a follow-up question, recognize an
alternative perspective, invite further discussion, or do not respond.
The Author remains the decision-maker.

### 4. Learn

Reader Engagement may provide editorial intelligence for future work.
Candidate signals include arguments that generate substantive
discussion, claims repeatedly challenged, recurring audience questions,
recurring misunderstandings, themes that resonate, useful
counterarguments, new evidence, and future article ideas. This document
records Learn as future product potential only; no analytics capability
is authorized or implemented by this delivery.

## Author Ownership Boundary

Reader Engagement must preserve Author Ownership. This discovery does
not authorize automatic public responses. Within the boundary this
capability contemplates, the Studio may:

- analyze a reader comment;
- explain likely interpretations;
- relate it to the article;
- identify factual questions it raises; and
- suggest response strategies.

Whether the Studio should generate complete response text for the
Author to review is an explicit, open future product decision boundary
and is **not** decided by this discovery. It is recorded here rather
than silently resolved in either direction.

`DEC-013` (the canonical Author Ownership prohibition on the Studio
rewriting, regenerating, or improving approved Publication Content, even
on explicit request) remains unresolved and is unchanged by this
document. Any future decision about Studio-generated response text must
be evaluated against `ADR-018` and the Version 1.1 Author Experience
Baseline, not assumed compatible with them by default.

## Future Web-Product State Extension

The likely web-product Editorial Project state model:

```text
Drafting -> Approved -> Published -> Reader Engagement
```

Publication becomes a state transition, not necessarily project
termination. A future published-project screen may conceptually contain:

- the published article;
- the Hero Visual;
- the publication date;
- a LinkedIn publication reference;
- source/evidence context;
- a Reader Engagement workspace;
- reader comments/replies;
- Studio interpretation;
- response-strategy assistance; and
- future-article signals.

These are discovery concepts, not implementation authorization.

## LinkedIn Integration Boundary

Reader Engagement is more valuable if reader comments and replies can be
associated with a published article. Future discovery should investigate
whether LinkedIn's supported APIs and permissions can enable:

- publication metadata capture;
- comment retrieval;
- comment/reply association with a published article; and
- Author-authorized reply publishing.

This document does not claim any of the above is currently available,
approved, or technically verified. LinkedIn API feasibility requires a
dedicated current-platform technical investigation before any of it is
treated as a design input. No credentials, OAuth scopes, API endpoints,
or technical architecture are specified here beyond what is already
established elsewhere in this repository.

The governing product principle: the Studio must never collect or store
the Author's LinkedIn password. Any future LinkedIn integration must use
supported authorization mechanisms and explicit Author consent.

## Web-Product Persistence Implication

The locked private GPT benefits from article context only while the
originating conversation remains available - it does not persist
anything between sessions. A future web product may intentionally
persist Editorial Project context to make Reader Engagement durable
across sessions. Candidate persisted context includes:

- approved publication content;
- approved editorial direction;
- verified evidence references;
- publication metadata; and
- associated reader engagement.

Retention rules, deletion, privacy, consent, security, data portability,
and Author control must be explicitly designed before any of this is
implemented. This document does not treat persistence as automatically
authorized by this discovery.

## Relationship to Other Capabilities

Capability 011 introduced the Portable Editorial Project as the durable
editorial continuity record. Capability 012 (`Capability_012_Portable_Author_Context.md`)
extends portability to editorial preferences. Reader Engagement extends
the same underlying "project" concept forward in time, past publication,
rather than introducing a new artifact type. Any future design should
evaluate whether Reader Engagement context is a natural extension of the
Portable Editorial Project or a distinct artifact, consistent with Every
Artifact Has One Responsibility.

## Non-Goals

This capability does not introduce, and this document does not
authorize:

- a change to the locked private GPT baseline (`GPT Recovery RC5 -
  Locked Private GPT Baseline`) or its Instructions;
- a new GPT Recovery release;
- LinkedIn integration of any kind;
- automatic reply generation or automatic publishing;
- a resolved answer to whether the Studio may draft response text;
- a change to canonical Author Ownership rules or to `DEC-013`;
- a persistence or retention model; or
- Version 2 implementation authorization.

## Open Questions

Before implementation, Version 2 architecture must determine:

- whether the Studio may draft candidate response text, or only analyze
  and advise;
- how reader comments are supplied to the Studio (manual paste, platform
  integration, or both);
- whether Reader Engagement requires a dedicated artifact or extends the
  Portable Editorial Project;
- what LinkedIn API feasibility investigation concludes;
- retention, deletion, and consent design for any persisted engagement
  context;
- how Editorial Integrity Pipeline evidence standards apply to claims a
  reader introduces; and
- how Learn-category signals, if ever implemented, would be surfaced
  without becoming hidden behavioural tracking.

## Candidate Acceptance Boundary

Capability 013 should not be considered ready for implementation until:

- the Version 2 product boundary is approved;
- the Author Ownership boundary on response-text generation is
  explicitly resolved;
- LinkedIn API feasibility is verified by dedicated technical
  investigation;
- a retention, privacy, and Author-control model is designed for any
  persisted Reader Engagement context; and
- an ADR defines ownership and failure behaviour, consistent with how
  Capability 011 and Capability 012 are governed.

## GPT Baseline Status

`GPT Recovery RC5 - Locked Private GPT Baseline` remains unchanged. This
Reader Engagement discovery does not unlock or supersede the locked
baseline. It is evidence of additional product value observed in real
use, not evidence of a defect requiring immediate GPT modification.
Future real-use evidence may justify reconsideration through the normal
process: Product Validation Log, then Product Decision, then authorized
implementation.
