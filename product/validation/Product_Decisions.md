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
