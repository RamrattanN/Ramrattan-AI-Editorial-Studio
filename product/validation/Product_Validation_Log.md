# Product Validation Log

This log is the authoritative repository record of observed product
behaviour during real-world use.

It records evidence, not ideas. Entries are never hypothetical
improvements, brainstorming, speculative features, implementation
notes, or engineering process. Each entry follows one path:

Observation -> Evidence -> Analysis -> Decision -> Status

Every entry ends with an explicit decision. `docs/product/Decision_Log.md`
records the resulting product decisions once acted upon; this log records
the observation that motivated them.

## Index

| ID | Date | Scenario | Status |
|---|---|---|---|
| [PV-001](#pv-001) | 2026-08-05 | First-draft LinkedIn article generation, compared against the original Article & Post Generator | Validated |
| [PV-002](#pv-002) | 2026-08-05 | Transition from approved article to Hero Visual preparation | Validated |
| [PV-003](#pv-003) | 2026-08-05 | Source material in a language different from the intended publication language | Validated |
| [PV-004](#pv-004) | 2026-08-05 | Editorial Audit requested on a generated first draft | Validated |
| [PV-005](#pv-005) | 2026-08-05 | Editorial house style during LinkedIn article generation | Validated |
| [PV-006](#pv-006) | 2026-08-05 | Conversational continuation after a completed response | Validated |
| [PV-007](#pv-007) | 2026-08-05 | In-conversation choice presentation and interaction | Validated |
| [PV-008](#pv-008) | 2026-08-08 | Sources missing from publication package | Validated |
| [PV-009](#pv-009) | 2026-08-08 | Hashtags omitted from publication package | Validated |
| [PV-010](#pv-010) | 2026-08-08 | Publication completeness not checked before Hero Visual | Validated |
| [PV-011](#pv-011) | 2026-08-08 | URL intake became a questionnaire | Validated - RC6 failed |
| [PV-012](#pv-012) | 2026-08-08 | Editorial angle selection was artificially single-select | Validated - RC6 failed |
| [PV-013](#pv-013) | 2026-08-08 | End-to-end experience less polished than the original GPT | Validated - RC6 failed |
| [PV-014](#pv-014) | 2026-08-08 | Hero Visual delivery failed the visible-output contract | Validated - RC6 failed |
| [PV-015](#pv-015) | 2026-08-08 | Workflow remained over-procedural through final delivery | Validated - RC6 failed end-to-end |
| [PV-016](#pv-016) | 2026-08-08 | URL starter produced redundant intake choices | Validated and implemented |
| [PV-017](#pv-017) | 2026-08-08 | Consolidated Editorial Direction materially improved UX | Validated and implemented |
| [PV-018](#pv-018) | 2026-08-08 | Numeric workflow vocabulary should be consistent | Validated and implemented |
| [PV-019](#pv-019) | 2026-08-08 | Hashtag quantity was insufficient | Validated and implemented |
| [PV-020](#pv-020) | 2026-08-08 | Publication tail order needs to match copy/paste workflow | Validated and implemented |
| [PV-021](#pv-021) | 2026-08-08 | Output completeness must include order, not only presence | Validated and implemented |
| [PV-022](#pv-022) | 2026-08-09 | Editorial Plan can be mistaken for final output | Validated and approved for Recovery RC3 |
| [PV-023](#pv-023) | 2026-08-09 | Hero Visual personalization lacks an obvious fast path | Validated and approved for Recovery RC3 |
| [PV-024](#pv-024) | 2026-08-09 | Workflow needs a definitive completion state | Validated and approved for Recovery RC3 |
| [PV-025](#pv-025) | 2026-08-09 | Hero Visual dimensions did not meet LinkedIn requirement | Validated and approved for Recovery RC3 |
| [PV-026](#pv-026) | 2026-08-09 | Hero Visual rendered but workflow halted | Validated and approved for Recovery RC4 |
| [PV-027](#pv-027) | 2026-08-09 | Post-image continuation is not reliable in Custom GPT | Validated, approved, and locked for the private GPT baseline |
| [PV-028](#pv-028) | 2026-08-10 | Post-publication Reader Engagement extends Editorial Project value | Validated real-use discovery - candidate requirement for web-product discovery |
| [PV-029](#pv-029) | 2026-08-11 | Web Editorial Direction quality compared against the locked GPT baseline | Validated real-use discovery - investigation pending |

---

## PV-001

| Field | Detail |
|---|---|
| Date | 2026-08-05 |
| Validation Session | Volkswagen Emergency Assist validation session |
| Scenario | First-draft LinkedIn article generation, compared against the original Article & Post Generator |
| Observation | First-draft article quality is materially weaker than the original Article & Post Generator. |
| Evidence | Volkswagen Emergency Assist validation session. |
| Analysis | Editorial reasoning is strong. First-draft generation does not yet match the specialist generator. |
| Decision | Preserve the Editorial Studio. Improve the embedded article-generation capability. |
| Status | Validated |

---

## PV-002

| Field | Detail |
|---|---|
| Date | 2026-08-05 |
| Validation Session | Volkswagen Emergency Assist validation session |
| Scenario | Transition from approved article to Hero Visual preparation |
| Observation | The Hero Visual transition was unclear. |
| Evidence | Author explicitly requested the Hero Visual because the Studio did not naturally continue the conversation. |
| Analysis | The Studio lost ownership of the conversational transition. |
| Decision | The Studio should own every transition until the publication package is complete. |
| Status | Validated |

---

## PV-003

| Field | Detail |
|---|---|
| Date | 2026-08-05 |
| Validation Session | Volkswagen Emergency Assist validation session |
| Scenario | Source material in a language different from the intended publication language |
| Observation | The source language differed from the desired publication language. |
| Evidence | German LinkedIn source. Author manually requested US English. |
| Analysis | Publication language should become an explicit editorial decision when source and publication languages differ. |
| Decision | Automatically detect source language. Confirm publication language whenever they differ. |
| Status | Validated |

---

## PV-004

| Field | Detail |
|---|---|
| Date | 2026-08-05 |
| Validation Session | Volkswagen Emergency Assist validation session |
| Scenario | Editorial Audit requested on a generated first draft |
| Observation | The Editorial Audit quality exceeded the quality of the first draft. |
| Evidence | Author's detailed critique of the generated article. |
| Analysis | The editorial reasoning engine is stronger than the drafting engine. |
| Decision | Reuse the editorial reasoning process to improve first-draft quality. |
| Status | Validated |

---

## PV-005

| Field | Detail |
|---|---|
| Date | 2026-08-05 |
| Validation Session | Private GPT Validation Session 2 |
| Scenario | Editorial house style during LinkedIn article generation |
| Observation | The GPT used long punctuation marks and single sentence spacing even though the Repository Author's ChatGPT preferences prohibit em dashes, en dashes, and long dashes, and require two spaces after a full stop and one space after a comma. |
| Evidence | Generated LinkedIn article from the Volkswagen Emergency Assist source. |
| Analysis | Custom GPT behavior must be self-contained. Account-level preferences cannot be assumed to govern the GPT deployment. |
| Decision | Make the private deployment's editorial house style explicit in the GPT Instructions and validate it directly. |
| Status | Validated and approved for RC5 |

---

## PV-006

| Field | Detail |
|---|---|
| Date | 2026-08-05 |
| Validation Session | Private GPT Validation Session 2 |
| Scenario | Conversational continuation after a completed response |
| Observation | The GPT completed a response but did not clearly state or execute the next step, leaving the Author uncertain how to continue. |
| Evidence | The Author had to identify that the session had stopped and ask what to do next. |
| Analysis | "Own the Transition" was present but insufficiently operational. A chat response necessarily ends, but the product must never end a non-terminal response without either performing the next safe action or requesting one precise Author decision. |
| Decision | Require every non-terminal response to execute the next non-decision step in the same response or finish with one explicit, low-effort next action. |
| Status | Validated and approved for RC5 |

---

## PV-007

| Field | Detail |
|---|---|
| Date | 2026-08-05 |
| Validation Session | Private GPT Validation Session 2 |
| Scenario | In-conversation choice presentation and interaction |
| Observation | Choices appeared as numbered text rather than clickable buttons. |
| Evidence | The Author had to type a number manually. |
| Analysis | The OpenAI Custom GPT surface provides opening-screen conversation starters but does not expose a supported builder control for custom in-conversation buttons. This is a deployment-platform constraint, not a content-generation defect. |
| Decision | Do not promise clickable in-conversation buttons. Present short, standalone numbered choices designed for replies such as "1" or "1, 3". Preserve true clickable controls as a future web-product UX requirement. |
| Status | Validated platform constraint and approved mitigation |

---

## PV-008

| Field | Detail |
|---|---|
| Date | 2026-08-08 |
| Validation Session | Private GPT Validation Session 3 (NINJIO / FBI IC3 source) |
| Scenario | Sources missing from publication package |
| Observation | The GPT retrieved, verified, and cited sources during reasoning, but those sources were not preserved in the approval output or final publication package. |
| Evidence | The draft and fact-checking relied on NINJIO and FBI IC3 evidence, but the final package omitted source references. |
| Analysis | Evidence continuity is breaking between research and delivery. A source set gathered during validation must survive into publication output. |
| Decision | Preserve the verified source set across the session and include a Sources section in the publication package whenever factual claims were grounded in external sources. |
| Status | Validated and approved for RC6 |

---

## PV-009

| Field | Detail |
|---|---|
| Date | 2026-08-08 |
| Validation Session | Private GPT Validation Session 3 (NINJIO / FBI IC3 source) |
| Scenario | Hashtags omitted from publication package |
| Observation | No hashtags were generated in the approval phase or final output. |
| Evidence | The final LinkedIn package omitted hashtags entirely. |
| Analysis | The deployment instructions treated hashtags as optional "if they exist," allowing a standard LinkedIn publication element to disappear without an Author decision. |
| Decision | Generate a concise LinkedIn hashtag set by default unless the Author explicitly opts out. |
| Status | Validated and approved for RC6 |

---

## PV-010

| Field | Detail |
|---|---|
| Date | 2026-08-08 |
| Validation Session | Private GPT Validation Session 3 (NINJIO / FBI IC3 source) |
| Scenario | Publication completeness not checked before Hero Visual |
| Observation | The workflow approached Hero Visual preparation despite missing textual publication-package elements. |
| Evidence | Sources and hashtags were absent before the transition toward Hero Visual generation. |
| Analysis | Publication preparation needs a deterministic completeness check before visual generation begins. |
| Decision | Before Hero Visual preparation, verify the required publication-text components are present and surface any missing component for completion. |
| Status | Validated and approved for RC6 |

---

## PV-011

| Field | Detail |
|---|---|
| Date | 2026-08-08 |
| Validation Session | Private GPT Validation Session 4 (RC6 end-to-end) |
| Scenario | URL intake became a questionnaire |
| Observation | After the Author selected URL transformation and pasted a URL, the GPT analyzed it, then separately asked for angle, outcome, and audience as three distinct typed-numeric-response questions - re-requesting the URL in the process - instead of inferring these and proceeding. |
| Evidence | Observed sequence: select URL transformation -> paste URL -> GPT analyzes -> three substantially duplicate choices presented -> Author selects -> GPT separately asks for angle -> Author selects -> GPT separately asks for outcome -> Author selects -> GPT asks for the URL again -> GPT continues requiring typed numeric responses. |
| Analysis | The intake violates Infer Before Asking and creates unnecessary Author labor; it re-requests input already supplied. |
| Decision | Consolidate intake into research plus one recommended Editorial Direction with exactly one Author decision; never re-request already-supplied input. |
| Status | Validated - RC6 failed |

---

## PV-012

| Field | Detail |
|---|---|
| Date | 2026-08-08 |
| Validation Session | Private GPT Validation Session 4 (RC6 end-to-end) |
| Scenario | Editorial angle selection was artificially single-select |
| Observation | Angle selection forced the Author to pick exactly one option, when the desired behavior is a recommended primary angle plus up to two optional supporting lenses. |
| Evidence | The angle question was presented as a single-select choice among substantially duplicate options. |
| Analysis | A single-select angle model understates the editorial nuance a strong piece can carry and forces artificial either/or framing. |
| Decision | Permit up to three complementary angles - one primary, zero to two supporting lenses - with the Studio recommending the minimum needed. |
| Status | Validated - RC6 failed |

---

## PV-013

| Field | Detail |
|---|---|
| Date | 2026-08-08 |
| Validation Session | Private GPT Validation Session 4 (RC6 end-to-end) |
| Scenario | End-to-end experience less polished than the original GPT |
| Observation | The complete RC6 experience remained substantially less polished than the original four-hour Article & Post Generator, for the same kind of input. |
| Evidence | Direct comparison during the validation session against the original GPT's immediacy, low cognitive burden, and concise editorial structure. |
| Analysis | Version 1.1 capability accumulation increased procedural overhead faster than it increased Author-perceived value; sunk implementation effort had been preserved past the point it earned its complexity. |
| Decision | Treat the original Article & Post Generator as the minimum UX and drafting-quality baseline; rebuild the Instructions from that baseline outward rather than continuing to append rules. |
| Status | Validated - RC6 failed |

---

## PV-014

| Field | Detail |
|---|---|
| Date | 2026-08-08 |
| Validation Session | Private GPT Validation Session 4 (RC6 end-to-end) |
| Scenario | Hero Visual delivery failed the visible-output contract |
| Observation | At the end of the workflow, the Author received text or path-like output indicating where a file existed rather than an immediately useful, visible Hero Visual. |
| Evidence | The Author could not meaningfully access the result from the output produced. |
| Analysis | A filename, path, or claim of successful generation is not a deliverable in a chat surface; only a visibly rendered image satisfies the Hero Visual contract. |
| Decision | Successful Hero Visual generation means the image is visibly rendered in the conversation; a path, filename, or success claim is never sufficient. On failure, offer Retry, Revise visual direction, or Skip. |
| Status | Validated - RC6 failed |

---

## PV-015

| Field | Detail |
|---|---|
| Date | 2026-08-08 |
| Validation Session | Private GPT Validation Session 4 (RC6 end-to-end) |
| Scenario | Workflow remained over-procedural through final delivery |
| Observation | Beyond the specific intake, angle, and Hero Visual defects, the workflow as a whole remained procedural and effortful all the way through final delivery. |
| Evidence | Cumulative Author labor across PV-011 through PV-014, observed within one continuous validation session. |
| Analysis | Individually fixable defects were compounding into a systemically over-procedural experience; incremental patching of RC6 would not resolve this, only a rebuild from the original GPT's proven simplicity would. |
| Decision | The Custom GPT deployment has failed end-to-end product validation. This conclusion applies to the Custom GPT deployment experience only, not to the underlying Version 1.1 repository engineering. Recover the deployment as GPT Recovery RC1, rewritten from the original Article & Post Generator baseline outward. |
| Status | Validated - RC6 failed end-to-end |

---

## PV-016

| Field | Detail |
|---|---|
| Date | 2026-08-08 |
| Validation Session | Recovery RC1 live validation session (GPT Builder) |
| Scenario | URL starter produced redundant intake choices |
| Observation | After the Author selected the URL conversation starter, the GPT asked what URL it should use and presented redundant options (paste the URL, upload the source, another paste-URL interaction) even though the Author had already selected the URL workflow. |
| Evidence | The conversation starter had already established intent; the follow-up menu added cognitive effort without adding information. |
| Analysis | Presenting intake choices the starter already resolved violates the consolidated-intake intent of Recovery RC1. |
| Decision | When the URL conversation starter is selected and no URL has yet been supplied, respond only "Paste the URL here to get started." - no alternative input methods offered at that moment. A subsequent live test produced exactly that response, after which the Author pasted the URL and the GPT proceeded directly into research and a consolidated Editorial Direction. |
| Status | Validated and implemented |

---

## PV-017

| Field | Detail |
|---|---|
| Date | 2026-08-08 |
| Validation Session | Recovery RC1 live validation session (GPT Builder) - https://thehackernews.com/2026/08/new-css-attacks-can-break-webmail.html |
| Scenario | Consolidated Editorial Direction materially improved UX |
| Observation | After the URL was supplied, the GPT retrieved and researched the source, verified important claims, inferred audience and objective, used US English, recommended one primary angle plus two supporting lenses, and presented one consolidated editorial thesis - without separate angle/outcome/audience questionnaires and without requesting the URL again. |
| Evidence | Direct observation of the full intake-to-direction sequence for the URL above. |
| Analysis | This was materially closer to the intended low-friction experience and to the original four-hour GPT baseline. |
| Decision | Preserve consolidated Editorial Direction as the normal URL-intake behavior. |
| Status | Validated and implemented |

---

## PV-018

| Field | Detail |
|---|---|
| Date | 2026-08-08 |
| Validation Session | Recovery RC1 live validation session (GPT Builder) |
| Scenario | Numeric workflow vocabulary should be consistent |
| Observation | Mixed interaction terms across Editorial Direction, Editorial Plan, article approval, and Hero Visual (Proceed, Approve, Adjust, Audit, and various numeric selections) created unnecessary inconsistency. |
| Evidence | Direct comparison of the decision prompts presented at each approval boundary during the session. |
| Analysis | A single, stable decision vocabulary reduces cognitive load at every approval boundary. |
| Decision | Use "1. Approve / 2. Reject" as the standard decision vocabulary at every approval boundary, with "3. Editorial Audit" added only at article approval. Accept either the number or the corresponding word; meaning stays stable everywhere (1 = Approve, 2 = Reject). Reject does not discard previously approved upstream work. |
| Status | Validated and implemented |

---

## PV-019

| Field | Detail |
|---|---|
| Date | 2026-08-08 |
| Validation Session | Recovery RC1 live validation session (GPT Builder) |
| Scenario | Hashtag quantity was insufficient |
| Observation | The GPT generated five hashtags in the live article-generation test. |
| Evidence | Direct count of hashtags in the generated publication package. |
| Analysis | Five hashtags under-served the LinkedIn publication package the Repository Author expects by default. |
| Decision | Generate exactly 10 relevant LinkedIn hashtags by default unless the Author explicitly opts out, using a deliberate mix of approximately 2-3 broad, 4-5 topic-specific, and 2-3 niche hashtags - no duplicates, no irrelevant trending tags, no keyword stuffing. |
| Status | Validated and implemented |

---

## PV-020

| Field | Detail |
|---|---|
| Date | 2026-08-08 |
| Validation Session | Recovery RC1 live validation session (GPT Builder) |
| Scenario | Publication tail order needs to match copy/paste workflow |
| Observation | The final publication elements were not ordered optimally for the Author's LinkedIn copy/paste workflow. |
| Evidence | Direct review of the final publication package's element order during the session. |
| Analysis | A predictable, fixed publication sequence reduces manual reordering before the Author posts. |
| Decision | The final four text blocks must always appear in this order: Call to Action, Sources, Hashtags, LinkedIn Description - LinkedIn Description always last. |
| Status | Validated and implemented |

---

## PV-021

| Field | Detail |
|---|---|
| Date | 2026-08-08 |
| Validation Session | Recovery RC1 live validation session (GPT Builder) |
| Scenario | Output completeness must include order, not only presence |
| Observation | Prior completeness checks verified whether elements existed but did not guarantee their final order. |
| Evidence | Direct comparison of package contents against the approved order from PV-020. |
| Analysis | Presence-only verification is insufficient once a fixed publication order is required. |
| Decision | Before presenting a draft or final publication package, verify both required component presence and required component order; correct any missing or misplaced element before presenting it to the Author. |
| Status | Validated and implemented |

---

## PV-022

| Field | Detail |
|---|---|
| Date | 2026-08-09 |
| Validation Session | Successful Recovery RC2 end-to-end validation |
| Scenario | Editorial Plan can be mistaken for final output |
| Observation | The Editorial Plan is now useful and concise, but a first-time Author may not understand that it is a pre-draft review rather than the final article. |
| Evidence | Direct observation during a successful Recovery RC2 end-to-end session. |
| Analysis | The workflow should make the purpose of this approval boundary obvious without creating another explanation-heavy phase. |
| Decision | Present the section as "Editorial Plan - Review Before Drafting" with the line "This is the proposed structure for your article, not the final article. Approve it to move to the full draft." immediately underneath. Retain 1. Approve / 2. Reject. |
| Status | Validated and approved for Recovery RC3 |

---

## PV-023

| Field | Detail |
|---|---|
| Date | 2026-08-09 |
| Validation Session | Successful Recovery RC2 end-to-end validation |
| Scenario | Hero Visual personalization lacks an obvious fast path |
| Observation | Hero Visual preparation asks for optional personalization inputs but does not make the quickest default path sufficiently obvious. |
| Evidence | Direct observation during a successful Recovery RC2 end-to-end session. |
| Analysis | "Skip personalization" can sound as though the Author is foregoing the Hero Visual rather than selecting the Studio's default visual treatment. |
| Decision | After article approval, present "1. Continue with the Studio Theme - no additional assets needed" alongside the option to personalize with any combination of headshot, logo, website URL, or explicit palette. The Studio Theme path still generates the Hero Visual; it does not skip visual generation. |
| Status | Validated and approved for Recovery RC3 |

---

## PV-024

| Field | Detail |
|---|---|
| Date | 2026-08-09 |
| Validation Session | Successful Recovery RC2 end-to-end validation |
| Scenario | Workflow needs a definitive completion state |
| Observation | The workflow reaches the Hero Visual and final package successfully, but the Author needs an unmistakable signal that the complete process is finished. |
| Evidence | Direct observation during a successful Recovery RC2 end-to-end session. |
| Analysis | A polished product should terminate deliberately rather than merely stop producing content. |
| Decision | After the complete final publication package, end with "Publication Package Complete / Your article and Hero Visual are ready for publication. / Thank you for using Ramrattan AI Editorial Studio." with no follow-up question, choice, or menu. |
| Status | Validated and approved for Recovery RC3 |

---

## PV-025

| Field | Detail |
|---|---|
| Date | 2026-08-09 |
| Validation Session | Recovery RC2 validation after transferring the generated Hero Visual into LinkedIn's cover-image workflow |
| Scenario | Hero Visual dimensions did not meet LinkedIn requirement |
| Observation | The Hero Visual was visibly generated and usable in conversation, but it was not in the explicitly required LinkedIn format of 720 x 425 pixels. |
| Evidence | The Author transferred the Hero Visual into LinkedIn and observed that the image did not fit the required 720 x 425 presentation correctly. |
| Analysis | Visible image delivery alone is insufficient; the Hero Visual publication contract includes both visible usable delivery and the correct intended LinkedIn canvas and composition. A visual that requires manual reformatting or cropping is not fully publication-ready. |
| Decision | The LinkedIn Hero Visual target for this GPT deployment is 720 x 425 pixels, landscape orientation, 144:85 aspect ratio, composed specifically for that final canvas. If the image-generation surface cannot directly return an exact 720 x 425 pixel file: preserve the 144:85 intended composition, state the limitation truthfully, do not claim exact pixel compliance, do not treat a path or filename as a solution, and do not claim the package is fully publication-ready without disclosing the remaining sizing limitation. |
| Status | Validated and approved for Recovery RC3 |

---

## PV-026

| Field | Detail |
|---|---|
| Date | 2026-08-09 |
| Validation Session | Recovery RC3 end-to-end validation |
| Scenario | Hero Visual rendered but workflow halted |
| Observation | Direct URL intake, consolidated Editorial Direction, the "Editorial Plan - Review Before Drafting" clarity, article generation, exactly 10 hashtags, correct publication-tail ordering, automatic transition into Hero Visual preparation, the Studio Theme fast path, and visible Hero Visual rendering all worked as intended. Immediately after visibly rendering the Hero Visual, the GPT stopped and did not present 1. Approve / 2. Reject. |
| Evidence | The Author could not naturally advance into final-package delivery, and the required "Publication Package Complete" terminal message was never reached, because the approval boundary after the Hero Visual was never presented. |
| Analysis | The completion-message requirement itself was not disproven; the workflow failed one transition earlier. Hero Visual rendering and Hero Visual approval presentation must be treated as one atomic conversational interaction - a visible image by itself is not the end of the Hero Visual stage. |
| Decision | Immediately after a Hero Visual is visibly rendered, the GPT must present 1. Approve / 2. Reject in the same response - never terminate a response on the generated Hero Visual alone. 1 / Approve advances directly to final-package delivery. 2 / Reject remains local to Hero Visual preparation, preserves the approved article, and asks only what should change about the visual. |
| Status | Validated and approved for Recovery RC4 |

---

## PV-027

| Field | Detail |
|---|---|
| Date | 2026-08-09 |
| Validation Session | Repeated end-to-end Recovery validation through successful Hero Visual generation |
| Scenario | Post-image continuation is not reliable in Custom GPT |
| Observation | Multiple configurations explicitly instructed the GPT to continue after the Hero Visual rendered, including Recovery RC4's atomic 1. Approve / 2. Reject requirement immediately after rendering. Live validation repeatedly showed that successful image generation could end the assistant interaction regardless. A subsequent test that moved all required publication text and completion messaging before image generation produced a materially better experience and was approved by the Repository Author. |
| Evidence | Positive evidence from the final validation session: direct URL intake remained effective; consolidated Editorial Direction remained effective; the GPT handled an unexpected mid-workflow change well; Editorial Plan clarity remained effective; article generation remained materially improved; source continuity remained effective; 10 hashtags remained effective; publication-tail ordering remained effective; the Hero Visual visibly rendered; the overall experience was materially better than earlier recovery builds. |
| Analysis | The product should not depend on a Custom GPT behavior that repeated live validation has shown to be unreliable. Image generation should be treated as the final production action in the private Custom GPT deployment, with the graceful completion message occurring immediately before image generation rather than after it. |
| Decision | For the private Custom GPT: (1) deliver the complete approved publication text before Hero Visual generation; (2) present Hero Visual as the explicit final step; (3) obtain any required visual-direction approval before generation; (4) display the graceful completion/sign-off before invoking image generation; (5) generate and visibly render the Hero Visual; (6) treat the visible Hero Visual as the terminal artifact; (7) never depend on another assistant turn after successful image generation. |
| Status | Validated, approved, and locked for the private GPT baseline |

---

## PV-028

| Field | Detail |
|---|---|
| Date | 2026-08-10 |
| Validation Session | Real editorial use of the locked private GPT (GPT Recovery RC5) |
| Scenario | Post-publication Reader Engagement extends Editorial Project value |
| Observation | The Author created an article using Ramrattan AI Editorial Studio and kept the original conversation available after publication. The Author subsequently received reader replies/comments and supplied those responses back into the original article conversation. Because the conversation still contained the article's editorial context, the Studio could help the Author understand and interpret the reader response in relation to the article's thesis, supporting arguments, evidence, intended meaning, and professional context, and could help the Author consider an appropriate and meaningful response. |
| Evidence | Direct real-use observation: the Studio remained useful after publication because the original conversation retained the article's in-session editorial context; this was not a new, context-free AI conversation. |
| Analysis | Post-publication discussion is part of the Author's editorial lifecycle. Reader comments may contain agreement, disagreement, questions, challenges, misunderstandings, additional evidence, alternative perspectives, requests for clarification, or ideas for future articles. Because the Studio already understands the originating article and its evidence context, it may provide higher-value analysis than a fresh, context-free AI conversation - particularly when the Author wants to understand a reader's point before deciding whether or how to respond. The observed behavior depends on the original conversation remaining available with its in-session context; this must not be misrepresented as persistent cross-session product memory. |
| Decision | Record Reader Engagement as a candidate future web-product capability, extending the Editorial Project lifecycle to Create -> Publish -> Engage. A future web Editorial Project should remain available after publication and may enter a Reader Engagement state. This is a product discovery, not authorization to modify the locked private GPT, implement LinkedIn integration, implement automatic replies, or change canonical Author Ownership rules. |
| Status | Validated real-use discovery. Not yet implemented as a formal new GPT capability. Candidate requirement for web-product discovery. |

---

## PV-029

| Field | Detail |
|---|---|
| Date | 2026-08-11 |
| Validation Session | Web Walking Skeleton 01 literal hosted browser acceptance (Render, https://studio.ramrattan.com) |
| Scenario | Web Editorial Direction quality compared against the locked GPT baseline |
| Observation | The hosted Web Editorial Direction successfully completed the technical workflow but produced materially weaker editorial framing than the accepted locked GPT baseline during direct Repository Author comparison. |
| Evidence | Real hosted browser acceptance against https://studio.ramrattan.com (2026-08-11): a real public source URL was submitted, retrieved, and processed; a real, non-mocked, server-side OpenAI Editorial Direction request executed through the application's own path; the resulting Editorial Direction was schema-valid, persisted, and displayed, and native Approve/Reject functioned correctly.  The Repository Author's direct comparison against the GPT Recovery RC5 - Locked Private GPT Baseline found the web output materially weaker editorially for comparable source material. |
| Analysis | Publication-quality editorial intelligence for the Web Product is not yet proven, even though the technical foundation (retrieval, OpenAI integration, schema validation, persistence, and Approve/Reject) is proven.  The specific cause of the gap is not yet established; candidate factors include model selection, prompt/instruction quality, context construction, source processing, and schema constraints, none of which is prejudged by this entry. |
| Decision | Investigate the quality gap before deepening the generation pipeline.  Tracked as BACKLOG.md BL-001 (quality parity with the locked GPT baseline) and BL-002 (model-selection evaluation); no model, prompt, or implementation change is adopted by this entry. |
| Status | Validated real-use discovery.  Investigation pending under BACKLOG.md BL-001 and BL-002.  Not yet resolved. |
