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
