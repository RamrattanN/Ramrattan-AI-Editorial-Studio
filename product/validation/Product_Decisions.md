# Product Decisions Register

## Status

Active

## Purpose

This document records product decisions that have been promoted from the
Product Validation Log.

The Validation Log captures observations.

This register captures accepted product decisions.

Only validated observations explicitly approved by the Repository Author
may be entered here.

Each decision should reference the originating Product Validation entry.

## Baseline Status

**GPT Recovery RC5 - Locked Private GPT Baseline**

Locked: 2026-08-09, following DEC-026 and PV-027.

The recovery is considered successful. `deployment/openai_gpt/GPT_Configuration_v2_RC1.md`
at "GPT Recovery RC5" is the reference private-GPT implementation.

"Locked" means change-controlled by evidence, not immutable forever:

- further changes to the private GPT require new real-use validation
  evidence, entered through the Product Validation Log first;
- speculative polishing is not sufficient reason to modify the baseline;
- the private GPT should now be used for real editorial work;
- new observations return through the Product Validation Log, and
  approved changes return through this register, in that order; and
- the web-product track remains separate and may implement richer
  native UI behavior (for example, a post-image completion screen) that
  the Custom GPT deployment cannot rely on.

## Decision Template

| Field | Value |
|---|---|
| Decision ID | |
| Validation Reference | |
| Date Approved | |
| Decision | |
| Reason | |
| Affected Product Areas | |
| Implementation Status | |
| Repository References | |

## Promoted Decisions

| ID | Validation Reference | Decision |
|---|---|---|
| [DEC-001](#dec-001) | PV-005 | Private GPT house style |
| [DEC-002](#dec-002) | PV-006 | No unexplained conversational halts |
| [DEC-003](#dec-003) | PV-007 | Platform-aware choice interaction |
| [DEC-004](#dec-004) | PV-008 | Evidence continuity into final delivery |
| [DEC-005](#dec-005) | PV-009 | Hashtags by default |
| [DEC-006](#dec-006) | PV-010 | Pre-Hero-Visual completeness gate |
| [DEC-007](#dec-007) | PV-013 | Original GPT is the deployment quality baseline |
| [DEC-008](#dec-008) | PV-011 | Consolidated URL intake |
| [DEC-009](#dec-009) | PV-011 | Never request supplied input again |
| [DEC-010](#dec-010) | PV-012 | Multi-angle framing |
| [DEC-011](#dec-011) | PV-014 | Visible Hero Visual contract |
| [DEC-012](#dec-012) | PV-015 | Complete publication package |
| [DEC-013](#dec-013) | Governance review (ADR-018, Author Experience Baseline) | Explicitly authorized editing - NOT adopted; discrepancy recorded |
| [DEC-014](#dec-014) | PV-016 | URL conversation-starter behavior |
| [DEC-015](#dec-015) | PV-017 | Consolidated Editorial Direction (reaffirmed) |
| [DEC-016](#dec-016) | PV-018 | Approval vocabulary |
| [DEC-017](#dec-017) | PV-018 | Stage-local rejection |
| [DEC-018](#dec-018) | PV-019 | Hashtag standard - exactly 10 by default |
| [DEC-019](#dec-019) | PV-020 | Publication-tail order |
| [DEC-020](#dec-020) | PV-021 | Presence-and-order verification |
| [DEC-021](#dec-021) | PV-022 | Editorial Plan labeling |
| [DEC-022](#dec-022) | PV-023 | Hero Visual Studio Theme fast path |
| [DEC-023](#dec-023) | PV-024 | Terminal completion state |
| [DEC-024](#dec-024) | PV-025 | Hero Visual dimensions and composition |
| [DEC-025](#dec-025) | PV-026 | Atomic Hero Visual approval transition |
| [DEC-026](#dec-026) | PV-027 | Custom GPT terminal Hero Visual model |
| [DEC-027](#dec-027) | PV-028 | Published Editorial Projects may continue into Reader Engagement |
| [DEC-028](#dec-028) | Web Product Foundation discovery spike | Web Product Foundation v1 adopted |
| [DEC-029](#dec-029) | Independent Codex implementation review | Web approval-boundary decisions are durable project state |

---

## DEC-001

| Field | Value |
|---|---|
| Decision ID | DEC-001 |
| Validation Reference | PV-005 |
| Date Approved | 2026-08-05 |
| Decision | For the current private GPT deployment, all Author-facing editorial prose and publication output must: never use em dash U+2014; never use en dash U+2013; never use any long dash as punctuation; use the ASCII hyphen only, formatted with one space on each side (" - "); use two literal spaces after a sentence-ending full stop; use one literal space after a comma. Exceptions: do not alter URLs, decimal numbers, abbreviations, initials, Markdown syntax, list numbering, filenames, or code. |
| Reason | The Custom GPT does not reliably inherit the Repository Author's account-level preferences. |
| Affected Product Areas | OpenAI Custom GPT deployment only. |
| Implementation Status | RC5. |
| Repository References | `deployment/openai_gpt/GPT_Configuration_v2_RC1.md` |

---

## DEC-002

| Field | Value |
|---|---|
| Decision ID | DEC-002 |
| Validation Reference | PV-006 |
| Date Approved | 2026-08-05 |
| Decision | Every non-terminal GPT response must do one of the following: (1) perform the next safe step in the same response when no Author decision is required; or (2) end with one clearly labeled next action requiring a concise Author response. The GPT must never end a non-terminal response with descriptive content alone. |
| Reason | The Author must always know what happens next. |
| Affected Product Areas | OpenAI Custom GPT conversational flow. |
| Implementation Status | RC5. |
| Repository References | `deployment/openai_gpt/GPT_Configuration_v2_RC1.md` |

---

## DEC-003

| Field | Value |
|---|---|
| Decision ID | DEC-003 |
| Validation Reference | PV-007 |
| Date Approved | 2026-08-05 |
| Decision | For the Custom GPT deployment, choices must be presented as concise, standalone numbered text options. The GPT must: state the recommended option first; keep labels brief; specify "Choose one" or "Choose up to three"; accept replies such as "1" or "1, 3"; include "Other" when appropriate; never describe the options as clickable buttons. True clickable workflow controls remain a web-deployment UX requirement and are not simulated or promised in the Custom GPT. |
| Reason | The current Custom GPT interface does not provide a supported configuration mechanism for custom in-conversation buttons. |
| Affected Product Areas | OpenAI Custom GPT deployment and future web-deployment requirements. |
| Implementation Status | RC5 mitigation; native web control deferred to the web track. |
| Repository References | `deployment/openai_gpt/GPT_Configuration_v2_RC1.md` |

---

## DEC-004

| Field | Value |
|---|---|
| Decision ID | DEC-004 |
| Validation Reference | PV-008 |
| Date Approved | 2026-08-08 |
| Decision | When the GPT uses external evidence to support factual claims, the verified source set must persist through planning, drafting, approval, and final delivery. Final publication output must include a Sources section. Each source should include, where available: source or publisher name; title or a concise identifying label; direct URL. Internal sourcing commentary or audit notes must not appear in the publication package. |
| Reason | Evidence continuity was breaking between research and delivery; a source set gathered during validation must survive into publication output. |
| Affected Product Areas | OpenAI Custom GPT publication workflow. |
| Implementation Status | RC6. |
| Repository References | `deployment/openai_gpt/GPT_Configuration_v2_RC1.md` |

---

## DEC-005

| Field | Value |
|---|---|
| Decision ID | DEC-005 |
| Validation Reference | PV-009 |
| Date Approved | 2026-08-08 |
| Decision | For LinkedIn article output, generate a concise, relevant hashtag set by default unless the Author explicitly requests none. Target 3 to 6 hashtags, preferring relevance and specificity over volume; do not keyword-stuff. |
| Reason | Treating hashtags as optional "if they exist" allowed a standard LinkedIn publication element to disappear without an Author decision. |
| Affected Product Areas | OpenAI Custom GPT final publication package. |
| Implementation Status | RC6. |
| Repository References | `deployment/openai_gpt/GPT_Configuration_v2_RC1.md` |

---

## DEC-006

| Field | Value |
|---|---|
| Decision ID | DEC-006 |
| Validation Reference | PV-010 |
| Date Approved | 2026-08-08 |
| Decision | Before beginning Hero Visual preparation, confirm that the publication text package contains: Headline; Hook; Article body; Call to Action; Hashtags, unless explicitly opted out; LinkedIn Description; Sources, whenever external evidence was used. If any required component is missing, complete or resolve it before moving to Hero Visual preparation. |
| Reason | Publication preparation needs a deterministic completeness check before visual generation begins. |
| Affected Product Areas | OpenAI Custom GPT publication workflow. |
| Implementation Status | RC6. |
| Repository References | `deployment/openai_gpt/GPT_Configuration_v2_RC1.md` |

---

## DEC-007

| Field | Value |
|---|---|
| Decision ID | DEC-007 |
| Validation Reference | PV-013 |
| Date Approved | 2026-08-08 |
| Decision | The original Article & Post Generator becomes the minimum UX and drafting-quality baseline for the Custom GPT deployment. New capability must build on that baseline - immediate usefulness, low cognitive burden, concise editorial structure, strong output orientation, little process overhead - rather than replace its proven strengths. |
| Reason | RC6 accumulated procedural overhead across four validation cycles that made it less useful than the original prototype it succeeded; sunk implementation effort is not a product requirement. |
| Affected Product Areas | OpenAI Custom GPT deployment scope and drafting-quality standard. |
| Implementation Status | GPT Recovery RC1. |
| Repository References | `deployment/openai_gpt/GPT_Configuration_v2_RC1.md` |

---

## DEC-008

| Field | Value |
|---|---|
| Decision ID | DEC-008 |
| Validation Reference | PV-011 |
| Date Approved | 2026-08-08 |
| Decision | For an accessible URL with sufficient evidence, normal intake requires no more than one Author decision between URL submission and presentation of the Editorial Direction. The GPT retrieves and reads the URL, verifies important claims, infers likely audience and objective, infers publication language, recommends the strongest primary angle and up to two supporting lenses, presents this as one consolidated Editorial Direction, and requests one confirmation or change decision. Angle, outcome, audience, and personalization are not interviewed separately when they can reasonably be inferred. |
| Reason | Separate angle, outcome, and audience questionnaires violated Infer Before Asking and created unnecessary Author labor with substantially duplicate choices. |
| Affected Product Areas | OpenAI Custom GPT intake and Editorial Direction flow. |
| Implementation Status | GPT Recovery RC1. |
| Repository References | `deployment/openai_gpt/GPT_Configuration_v2_RC1.md` |

---

## DEC-009

| Field | Value |
|---|---|
| Decision ID | DEC-009 |
| Validation Reference | PV-011 |
| Date Approved | 2026-08-08 |
| Decision | Once a URL, document, draft, idea, brand asset, or preference has been successfully supplied and remains available in the current conversation, never ask the Author to supply it again. Only request replacement input if retrieval failed or the original input is unavailable. |
| Reason | RC6 re-requested the URL mid-workflow after it had already been supplied and analyzed. |
| Affected Product Areas | OpenAI Custom GPT conversational flow. |
| Implementation Status | GPT Recovery RC1. |
| Repository References | `deployment/openai_gpt/GPT_Configuration_v2_RC1.md` |

---

## DEC-010

| Field | Value |
|---|---|
| Decision ID | DEC-010 |
| Validation Reference | PV-012 |
| Date Approved | 2026-08-08 |
| Decision | Permit up to three complementary editorial angles: one primary angle, plus zero to two supporting lenses. The Studio recommends the minimum number needed; one is preferred when one is sufficient. Three is a maximum, not a target. |
| Reason | A forced single-select angle choice understated the editorial nuance a strong piece can carry. |
| Affected Product Areas | OpenAI Custom GPT Editorial Direction flow. |
| Implementation Status | GPT Recovery RC1. |
| Repository References | `deployment/openai_gpt/GPT_Configuration_v2_RC1.md` |

---

## DEC-011

| Field | Value |
|---|---|
| Decision ID | DEC-011 |
| Validation Reference | PV-014 |
| Date Approved | 2026-08-08 |
| Decision | For the Custom GPT deployment, successful Hero Visual generation means the image is visibly rendered in the conversation. A filename is not successful delivery. A filesystem path is not successful delivery. A sandbox path is not successful delivery. A text statement claiming generation succeeded is not successful delivery. A visual-generation prompt alone is not successful delivery. If image generation fails or cannot visibly return an image, say so plainly and offer Retry, Revise visual direction, or Skip Hero Visual. Internal filesystem or path implementation is never exposed to the Author as the deliverable. |
| Reason | The Author reached the end of the RC6 workflow but received path-like text output instead of a usable, visible Hero Visual, and could not meaningfully access the result. |
| Affected Product Areas | OpenAI Custom GPT Hero Visual delivery. |
| Implementation Status | GPT Recovery RC1. |
| Repository References | `deployment/openai_gpt/GPT_Configuration_v2_RC1.md` |

---

## DEC-012

| Field | Value |
|---|---|
| Decision ID | DEC-012 |
| Validation Reference | PV-015 |
| Date Approved | 2026-08-08 |
| Decision | The final package must be directly useful to the Author, with applicable elements limited to: visible Hero Visual, Headline, Hook, Article, CTA, Hashtags, LinkedIn Description, and Sources. No implementation artifact is exposed. After a visible Hero Visual is generated, the GPT delivers the complete package and reaches an obvious terminal state without asking "what next?" |
| Reason | The workflow remained over-procedural all the way through final delivery, compounding the intake, angle, and Hero Visual defects into a systemically less-polished experience than the original GPT. |
| Affected Product Areas | OpenAI Custom GPT final delivery. |
| Implementation Status | GPT Recovery RC1. |
| Repository References | `deployment/openai_gpt/GPT_Configuration_v2_RC1.md` |

---

## DEC-013

| Field | Value |
|---|---|
| Decision ID | DEC-013 |
| Validation Reference | Governance review (ADR-018, Version 1.1 Author Experience Baseline) |
| Date Approved | 2026-08-08 |
| Decision | Reviewed the GPT's Author Ownership rule against the canonical Version 1.1 documents to determine whether it could be simplified to permit the Editor to perform an explicitly Author-requested edit. Both ADR-018 (Rule 1 and Costs and Risks) and the Author Experience Baseline (Non-Goals and Success Criteria) prohibit AI-assisted rewriting, regeneration, or improvement of Publication Content after Generation under any circumstance, including an explicit Author request - "an Author who wants the Studio's help improving a specific sentence after Generation must do so by hand." This rule is NOT loosened in GPT Recovery RC1; the strict "never rewrite, regenerate, improve, shorten, or expand it yourself, under any circumstance, even on request" wording is retained. |
| Reason | AGENTS.md Instruction Authority places accepted ADRs and the current architecture baseline above delivery-scoped product decisions; this delivery is not authorized to override them. A separate, unresolved discrepancy is recorded: the Custom GPT is a single-surface chat with no separate Author-editing UI, so any Author-directed change to displayed text is necessarily produced by the model - a tension with ADR-018's literal "even on request" prohibition that predates this recovery (present since RC1) and is not resolved by this delivery. |
| Affected Product Areas | OpenAI Custom GPT deployment; potentially Version 1.1 architecture if the Repository Author elects to formally address the chat-surface tension. |
| Implementation Status | GPT Recovery RC1 - rule retained unchanged; no override applied; discrepancy open. |
| Repository References | `deployment/openai_gpt/GPT_Configuration_v2_RC1.md`; `docs/architecture/adr/ADR-018-author-ownership-and-publication-studio.md`; `docs/product/Version_1_1_Author_Experience_Baseline.md` |

---

## DEC-014

| Field | Value |
|---|---|
| Decision ID | DEC-014 |
| Validation Reference | PV-016 |
| Date Approved | 2026-08-08 |
| Decision | When the Author selects the URL conversation starter and has not yet supplied a URL, the GPT responds only "Paste the URL here to get started." - no redundant intake menu, no alternative input methods offered at that moment. Once the URL is supplied, retrieve it and continue. |
| Reason | The URL starter already established the Author's intent; a follow-up menu re-asking how to supply a URL added cognitive effort without adding information. |
| Affected Product Areas | OpenAI Custom GPT conversation-starter response and intake flow. |
| Implementation Status | GPT Recovery RC2. |
| Repository References | `deployment/openai_gpt/GPT_Configuration_v2_RC1.md` |

---

## DEC-015

| Field | Value |
|---|---|
| Decision ID | DEC-015 |
| Validation Reference | PV-017 |
| Date Approved | 2026-08-08 |
| Decision | For a normal accessible URL, research and inference occur before one consolidated Editorial Direction is presented. The GPT does not separately interview for angle, objective, audience, personalization, or language when these can reasonably be inferred. This reaffirms DEC-008 and DEC-009 (Recovery RC1), now confirmed by direct live-session evidence rather than by design intent alone. |
| Reason | A live test against a real URL showed this behavior working as intended and materially closer to the original GPT's low-friction experience; no change to the underlying behavior is needed. |
| Affected Product Areas | OpenAI Custom GPT Editorial Direction flow. |
| Implementation Status | GPT Recovery RC2 - preserved unchanged from Recovery RC1. |
| Repository References | `deployment/openai_gpt/GPT_Configuration_v2_RC1.md` |

---

## DEC-016

| Field | Value |
|---|---|
| Decision ID | DEC-016 |
| Validation Reference | PV-018 |
| Date Approved | 2026-08-08 |
| Decision | At every approval boundary, use "1. Approve / 2. Reject" as the standard decision vocabulary. At article approval only, add "3. Editorial Audit". Accept either the number or the corresponding word; the meaning of 1 and 2 stays stable everywhere (1 = Approve, 2 = Reject). |
| Reason | Mixed interaction terms (Proceed, Approve, Adjust, Audit, and various numeric selections) across the workflow created unnecessary inconsistency. |
| Affected Product Areas | OpenAI Custom GPT decision prompts at every approval boundary. |
| Implementation Status | GPT Recovery RC2. |
| Repository References | `deployment/openai_gpt/GPT_Configuration_v2_RC1.md` |

---

## DEC-017

| Field | Value |
|---|---|
| Decision ID | DEC-017 |
| Validation Reference | PV-018 |
| Date Approved | 2026-08-08 |
| Decision | Reject preserves approved upstream work, remains at the current relevant stage, asks only what the Author wants changed, does not restart the workflow, does not discard verified evidence, and does not silently regenerate unrelated work. At the article stage, Reject asks what the Author wants changed and does not regenerate the article. This decision does not override the canonical post-generation Author Ownership prohibition; DEC-013 remains unresolved, and Reject at the article stage remains compatible with the canonical rule that the Editor cannot rewrite approved Publication Content. |
| Reason | A single, predictable rejection model - local to the stage, non-destructive to prior approvals - reduces friction without reopening the DEC-013 discrepancy. |
| Affected Product Areas | OpenAI Custom GPT decision handling at every approval boundary. |
| Implementation Status | GPT Recovery RC2. |
| Repository References | `deployment/openai_gpt/GPT_Configuration_v2_RC1.md`; DEC-013 |

---

## DEC-018

| Field | Value |
|---|---|
| Decision ID | DEC-018 |
| Validation Reference | PV-019 |
| Date Approved | 2026-08-08 |
| Decision | Generate exactly 10 relevant LinkedIn hashtags by default unless the Author explicitly opts out, using a deliberate mix of approximately 2 to 3 broad, 4 to 5 topic-specific, and 2 to 3 niche hashtags. No duplicates, no irrelevant trending tags, no keyword stuffing. This supersedes DEC-005's 3-to-6 default. |
| Reason | A live test produced only five hashtags; the Repository Author determined the publication package should contain ten hashtags by default. |
| Affected Product Areas | OpenAI Custom GPT final publication package. |
| Implementation Status | GPT Recovery RC2. |
| Repository References | `deployment/openai_gpt/GPT_Configuration_v2_RC1.md` |

---

## DEC-019

| Field | Value |
|---|---|
| Decision ID | DEC-019 |
| Validation Reference | PV-020 |
| Date Approved | 2026-08-08 |
| Decision | The final four text blocks must always appear in this exact order: Call to Action, Sources, Hashtags, LinkedIn Description. LinkedIn Description is always the final text block. |
| Reason | A predictable publication sequence reduces manual reordering in the Author's LinkedIn copy/paste workflow. |
| Affected Product Areas | OpenAI Custom GPT final publication package. |
| Implementation Status | GPT Recovery RC2. |
| Repository References | `deployment/openai_gpt/GPT_Configuration_v2_RC1.md` |

---

## DEC-020

| Field | Value |
|---|---|
| Decision ID | DEC-020 |
| Validation Reference | PV-021 |
| Date Approved | 2026-08-08 |
| Decision | Before presenting a draft or final publication package, verify both required-component presence and required-component order (per DEC-019). If an element is missing or misplaced, correct the package before presenting it to the Author. |
| Reason | Prior completeness checks verified presence only and did not guarantee the fixed order DEC-019 now requires. |
| Affected Product Areas | OpenAI Custom GPT draft and final package presentation. |
| Implementation Status | GPT Recovery RC2. |
| Repository References | `deployment/openai_gpt/GPT_Configuration_v2_RC1.md` |

---

## DEC-021

| Field | Value |
|---|---|
| Decision ID | DEC-021 |
| Validation Reference | PV-022 |
| Date Approved | 2026-08-09 |
| Decision | Present the Editorial Plan as "Editorial Plan - Review Before Drafting" and immediately state "This is the proposed structure for your article, not the final article. Approve it to move to the full draft." This is explanatory UX, not a new workflow stage; 1. Approve / 2. Reject are retained unchanged. |
| Reason | A first-time Author may not understand the Editorial Plan is a pre-draft review rather than the final article. |
| Affected Product Areas | OpenAI Custom GPT Editorial Plan presentation. |
| Implementation Status | GPT Recovery RC3. |
| Repository References | `deployment/openai_gpt/GPT_Configuration_v2_RC1.md` |

---

## DEC-022

| Field | Value |
|---|---|
| Decision ID | DEC-022 |
| Validation Reference | PV-023 |
| Date Approved | 2026-08-09 |
| Decision | At Hero Visual preparation, present "1. Continue with the Studio Theme - no additional assets needed" alongside the option to instead provide any combination of headshot, logo, website URL, or explicit color palette. Selecting 1 must generate a Hero Visual; it must never be interpreted as skipping Hero Visual generation. |
| Reason | "Skip personalization" could sound as though the Author is foregoing the Hero Visual rather than selecting the Studio's default visual treatment. |
| Affected Product Areas | OpenAI Custom GPT Hero Visual preparation. |
| Implementation Status | GPT Recovery RC3. |
| Repository References | `deployment/openai_gpt/GPT_Configuration_v2_RC1.md` |

---

## DEC-023

| Field | Value |
|---|---|
| Decision ID | DEC-023 |
| Validation Reference | PV-024 |
| Date Approved | 2026-08-09 |
| Decision | After final package delivery, display "Publication Package Complete / Your article and Hero Visual are ready for publication. / Thank you for using Ramrattan AI Editorial Studio." with no further prompt. If the Author explicitly skipped Hero Visual generation after a failure, or if exact 720 x 425 sizing remains unresolved, adapt the completion statement truthfully so it does not claim full publication readiness. |
| Reason | The Author needs an unmistakable signal that the complete process is finished; a polished product terminates deliberately rather than merely stopping. |
| Affected Product Areas | OpenAI Custom GPT final delivery. |
| Implementation Status | GPT Recovery RC3. |
| Repository References | `deployment/openai_gpt/GPT_Configuration_v2_RC1.md` |

---

## DEC-024

| Field | Value |
|---|---|
| Decision ID | DEC-024 |
| Validation Reference | PV-025 |
| Date Approved | 2026-08-09 |
| Decision | Every LinkedIn Hero Visual should target 720 x 425 pixels, landscape orientation, 144:85 aspect ratio, with composition designed for that intended final canvas; critical text, face, logo, and focal elements remain within safe margins, and the Editor never relies on LinkedIn to repair bad composition. The Editor does not claim exact pixel compliance unless the platform actually provides it; if exact 720 x 425 output is not technically supported, the limitation is disclosed truthfully. The future web product must guarantee final 720 x 425 output before download or publication preparation. |
| Reason | The generated Hero Visual was visibly usable in conversation but did not fit LinkedIn's required 720 x 425 presentation; visible delivery alone is insufficient without the correct intended canvas and composition. |
| Affected Product Areas | OpenAI Custom GPT Hero Visual generation; future web-product Hero Visual export requirement. |
| Implementation Status | GPT Recovery RC3 (GPT deployment); web-product guarantee deferred to that track. |
| Repository References | `deployment/openai_gpt/GPT_Configuration_v2_RC1.md` |

---

## DEC-025

| Field | Value |
|---|---|
| Decision ID | DEC-025 |
| Validation Reference | PV-026 |
| Date Approved | 2026-08-09 |
| Decision | Hero Visual rendering and Hero Visual approval form one atomic workflow transition. After the visible Hero Visual is rendered, the GPT immediately presents 1. Approve / 2. Reject in the same interaction - it never ends a response with the image alone. 1 = Approve: accept the visible Hero Visual, advance automatically, deliver the complete final publication package, display the terminal completion state, and do not ask for another approval. 2 = Reject: preserve the approved article and all approved upstream work, remain in Hero Visual preparation, ask only what should change about the visual, and regenerate only the Hero Visual after receiving revised direction - again presenting 1. Approve / 2. Reject immediately once the new visual renders. This decision does not change canonical Author Ownership rules for Publication Content. |
| Reason | RC3 validation showed the Hero Visual rendering visibly but the workflow halting immediately afterward without presenting the required approval decision, so the Author could never reach final-package delivery or the terminal completion state. |
| Affected Product Areas | OpenAI Custom GPT Hero Visual approval and final-package transition. |
| Implementation Status | GPT Recovery RC4. Superseded by DEC-026 for the private GPT deployment - repeated live validation showed the atomic post-image approval this decision required was not reliably reachable in the Custom GPT surface. |
| Repository References | `deployment/openai_gpt/GPT_Configuration_v2_RC1.md` |

---

## DEC-026

| Field | Value |
|---|---|
| Decision ID | DEC-026 |
| Validation Reference | PV-027 |
| Date Approved | 2026-08-09 |
| Decision | Custom GPT terminal Hero Visual model. For the private OpenAI Custom GPT deployment, successful Hero Visual generation is the final production action. Required sequence: Approved Article -> Complete Approved Publication Text Package -> Hero Visual - Final Step -> Visual Direction Approval when required -> Graceful Completion / Thank You -> Image Generation -> Visible Hero Visual -> END. No behavior after successful image generation is required for the Custom GPT deployment. Studio Theme path: selecting Studio Theme approves that visual direction; do not introduce an unnecessary second visual-direction approval; present final sign-off; invoke image generation; the visible image is terminal. Personalized path: collect only personalization information not already supplied; summarize visual direction; obtain 1. Approve / 2. Reject before generation; after approval, present final sign-off; invoke image generation; the visible image is terminal. The completion/sign-off communicates substantially: "Everything else is complete. Once your Hero Visual appears, your Ramrattan AI Editorial Studio session is finished. Thank you for using Ramrattan AI Editorial Studio." The product must never promise or depend on a post-image assistant message. This decision applies specifically to the private Custom GPT deployment; future web-product UX may provide a post-image completion screen because the web application controls its own interface. This decision supersedes DEC-025's post-image 1. Approve / 2. Reject requirement and Recovery RC3/RC4's post-image final-package delivery and completion message for the private GPT; it does not change canonical Author Ownership rules for Publication Content, and DEC-013 remains unresolved. |
| Reason | Repeated live end-to-end validation showed that successful Hero Visual generation could terminate the assistant interaction even when the Instructions explicitly required an atomic post-image approval step (DEC-025). Moving all required publication text, the final-step explanation, and the completion/sign-off before image generation produced a materially better, Repository-Author-approved experience that does not depend on unreliable post-image continuation. |
| Affected Product Areas | OpenAI Custom GPT Hero Visual sequencing and final delivery. |
| Implementation Status | GPT Recovery RC5 - Locked Private GPT Baseline. |
| Repository References | `deployment/openai_gpt/GPT_Configuration_v2_RC1.md` |

---

## DEC-027

| Field | Value |
|---|---|
| Decision ID | DEC-027 |
| Validation Reference | PV-028 |
| Date Approved | 2026-08-10 |
| Decision | Published Editorial Projects may continue into Reader Engagement. Publication does not necessarily terminate an Editorial Project. For future web-product design, a published project may enter a Reader Engagement state, extending the candidate lifecycle to Create -> Publish -> Engage. Reader Engagement should preserve enough project context to support post-publication analysis, subject to future privacy, retention, and Author-control decisions. At minimum, future discovery should evaluate preserving: the approved article; the approved editorial thesis/direction; verified evidence/source context; publication metadata; Author-approved project context; and reader comments/replies associated with that article. Purpose: enable the Studio to help the Author understand and respond thoughtfully to post-publication discussion without reconstructing the article's context from scratch. See `docs/product/version2/Capability_013_Reader_Engagement.md` for the full candidate concept, including the Author Ownership boundary on response-text generation (not decided by this discovery) and the LinkedIn integration feasibility boundary (not approved or implemented by this discovery). |
| Reason | Real editorial use of the locked private GPT (PV-028) showed that retained article context let the Studio meaningfully help the Author interpret and consider a response to reader comments - value that a fresh, context-free conversation could not provide. |
| Affected Product Areas | Future web-product Editorial Project lifecycle and architecture discovery. |
| Implementation Status | Approved as a web-product discovery requirement. NOT approved for implementation. NOT a change to the locked private GPT baseline (`deployment/openai_gpt/GPT_Configuration_v2_RC1.md`, GPT Recovery RC5, unchanged). |
| Repository References | `docs/product/version2/Capability_013_Reader_Engagement.md` |

---

## DEC-028

| Field | Value |
|---|---|
| Decision ID | DEC-028 |
| Validation Reference | Web Product Foundation discovery spike (`docs/product/version2/Web_Product_Foundation_v1.md`) |
| Date Approved | 2026-08-10 |
| Decision | Adopt Web Product Foundation v1 as the minimum technical foundation for the first browser-based Ramrattan AI Editorial Studio vertical slice. Key foundation decisions: (1) a thin conventional stack - TypeScript/Node.js backend, React frontend, PostgreSQL, managed container/PaaS deployment with separated development and production environments; (2) email magic link Author authentication, server-verified, no password stored - explicitly NOT a "sign in with ChatGPT and use my subscription" model, because no such officially supported third-party delegation capability currently exists; (3) all OpenAI calls are server-side only, billed under the application's own OpenAI API account (never the Author's ChatGPT subscription), using separate development/production API projects with independent spend limits; (4) a minimal relational data model (Author, EditorialProject, Source, EditorialDirection, EditorialPlan) that extends without a blocking migration to Article, Evidence, HeroVisual, Publication, and ReaderEngagement, and that represents publication as a state transition rather than project termination, per DEC-027/Capability 013; (5) the web application owns final Hero Visual image processing and guarantees the exact 720 x 425, 144:85 deliverable deterministically, with the AI model generating source artwork only; (6) LinkedIn publish-on-behalf-of-member (`w_member_social`) and image upload are confirmed feasible now via self-serve OAuth, while comment retrieval/reply (`r_member_social`) is confirmed closed to new access requests as of this spike - Reader Engagement automation remains blocked until that changes. The full foundation, including sourced current-documentation citations, is recorded in `docs/product/version2/Web_Product_Foundation_v1.md`. |
| Reason | The web product needed a minimum, evidence-based technical foundation - verified against current official OpenAI and LinkedIn documentation rather than assumption - so the next Engineering Delivery (Web Walking Skeleton 01) can begin implementation without a further architecture discussion, consistent with Baseline Before Better and the lean-foundation-spike scope authorized for this delivery. |
| Affected Product Areas | Future web-product architecture, authentication, OpenAI integration, data model, Hero Visual pipeline, and LinkedIn integration planning. |
| Implementation Status | Foundation adopted; NOT an authorization to implement the full web product. Only "Web Walking Skeleton 01," as scoped in `docs/product/version2/Web_Product_Foundation_v1.md` Section 9, is build-ready for the next Engineering Delivery. Does not change the locked private GPT baseline (`deployment/openai_gpt/GPT_Configuration_v2_RC1.md`, GPT Recovery RC5, unchanged) or DEC-013. |
| Repository References | `docs/product/version2/Web_Product_Foundation_v1.md` |

---

## DEC-029

| Field | Value |
|---|---|
| Decision ID | DEC-029 |
| Validation Reference | Independent Codex implementation review of Web Walking Skeleton 01 (Reject-persistence discrepancy) |
| Date Approved | 2026-08-11 |
| Decision | Web approval-boundary decisions are durable project state. Both Approve and Reject persist to the database as an explicit product decision, not an implementation detail. Approve persists the Author's decision, persists decision metadata, and advances the workflow to the next stage. Reject persists the Author's decision, persists Author feedback when supplied, persists decision metadata, and remains at the current workflow stage; it preserves the originating Source, the project, and any already-approved upstream work, and it does not restart the project or require already-supplied information to be re-entered. "Reject remains local to the stage" means **stage-local** - the workflow neither advances nor restarts - and explicitly does **not** mean client-local, ephemeral, or non-persistent. A browser refresh, sign-out/sign-in, device change, or later return to the project must not erase the fact that the Author rejected the current artifact. This decision generalizes DEC-017's stage-local rejection principle from the stateless private Custom GPT surface (where "stage-local" and "non-persistent" were indistinguishable because the GPT has no database) to the persistent web product, where the two are no longer the same thing and must be stated explicitly. |
| Reason | Independent review of Web Walking Skeleton 01 found that the implemented Reject endpoint persists rejected status, Author feedback, and decision time, while `docs/product/version2/Web_Product_Foundation_v1.md` Section 9's acceptance criteria and required-journey diagram stated persistence explicitly for Approve only, creating the appearance of a contract violation. The Repository Author reviewed the finding and confirmed the implementation was correct: persistent Editorial Projects are intended to retain Author decisions durably, which is one of their advantages over the stateless Custom GPT surface. The documentation, not the implementation, was stale and is corrected by this decision. |
| Affected Product Areas | Web product Editorial Direction approval boundary (Web Walking Skeleton 01) and every future web-product approval boundary (Editorial Plan, Draft, Hero Visual, and later stages) that persists Author decisions to the database. |
| Implementation Status | Reject was already conformant at time of decision - no application code change required for Reject. `web/server/src/projects/repository.ts`'s `rejectDirection` already persisted `status`, `reject_feedback`, and `decided_at`, and left `EditorialProject.stage` unchanged. Acceptance-criteria wording in `docs/product/version2/Web_Product_Foundation_v1.md` Section 9 corrected to match; automated test coverage in `web/server/tests/projects.test.ts` extended to assert the decision timestamp and stage non-advancement explicitly. **Update, 2026-08-11:** a follow-up Codex review found Approve was not fully conformant - it persisted `EditorialDirection.status` and `decided_at` but did not advance `EditorialProject.stage`. Fixed: `approveDirection` now advances the project to the `editorial_plan` stage in the same transaction as the direction update (migration `002_add_editorial_plan_stage.sql`); test coverage extended accordingly. Does not change the locked private GPT baseline or DEC-017, which remains the authoritative decision for the Custom GPT surface. |
| Repository References | `docs/product/version2/Web_Product_Foundation_v1.md`; `web/server/src/projects/repository.ts`; `web/server/src/db/migrations/002_add_editorial_plan_stage.sql`; `web/server/tests/projects.test.ts`; DEC-017 |
