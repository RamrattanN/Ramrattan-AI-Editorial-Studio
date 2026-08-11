# Editorial Direction Quality Investigation

**Status:** DS-01 Complete and closed - approved by the Repository Author 2026-08-11 as `product/validation/Product_Decisions.md` DEC-030 (Section 15), implemented and merged as PR #130 (commit `afb07eb`), and hosted-verified by the Repository Author through the real Web Product path (Section 16).  BL-001 is Done.
**Classification:** Evidence and recommendation artifact (Informative - not a Product Decision)
**Backlog:** BL-001 (primary), BL-002 (supporting)
**Evidence base:** PV-029

## 1. Question

PV-029 recorded that the hosted Web Editorial Direction completed its technical workflow successfully but was judged materially weaker editorially than the locked private GPT baseline (`GPT Recovery RC5`) during direct Repository Author comparison.  PV-029 deliberately did not diagnose a cause.  This document answers DS-01's five governing questions:

1. What materially causes the observed quality gap?
2. Is the gap prompt-related, model-related, context-construction-related, source-processing-related, schema-related, or a combination?
3. Which model/configuration should the Web Product use?
4. What quality/cost tradeoff does that recommendation imply?
5. Is Editorial Direction quality now sufficiently understood to permit Web Walking Skeleton 02 to proceed?

## 2. Baseline

### 2.A Locked GPT baseline (read-only reference, not modified)

Reconstructed from `deployment/openai_gpt/GPT_Configuration_v2_RC1.md` (GPT Recovery RC5, locked):

- **Persona and quality bar.**  The Instructions open with "You are the Editor inside Ramrattan AI Editorial Studio... Work like a skilled editor - concise, accurate, useful, and low-friction."  This framing governs every stage, including Editorial Direction.
- **Editorial Direction behavior.**  "For a URL or source, retrieve it, verify important claims, and infer audience, objective, publication language, and editorial angle... Recommend one primary angle plus up to two supporting lenses only when useful."
- **Retrieval and verification tooling.**  Web Search capability is **ON** - the model can browse and cross-reference, not just read one pre-fetched snapshot.  The Instructions explicitly require verifying important claims, which presumes this tool access.
- **Recommended model.**  Section 9: "the platform's current general-purpose flagship conversational model... rather than a pure reasoning-optimized model," reasoned specifically because the workload is "long-form editorial writing plus moderate evidence reasoning and web browsing."
- **House Style.**  US English, no em/en dashes, one space after commas, two spaces after sentence periods - the same convention this repository now applies to its own documentation (`AGENTS.md`, "Prose Convention").

### 2.B Current Web path (traced from source, 2026-08-11)

Traced directly from `web/server/src/openai/editorialDirection.ts`, `client.ts`, `schema.ts`, and `source/retrieve.ts` (code is authoritative; `web/README.md` was not relied on for behavior):

- **Model.**  `getConfiguredModel()` in `client.ts` returns `process.env.OPENAI_MODEL ?? "gpt-4o-mini"` - `gpt-4o-mini` is the default, and no `OPENAI_MODEL` override has been adopted as a product decision (`Web_Product_Foundation_v1.md` Section 5 explicitly deferred model-selection policy).
- **API and tooling.**  `client.chat.completions.create(...)` with `response_format: { type: "json_schema", ... }` (Structured Outputs, strict mode).  No tool calling, no web-browsing tool - the model sees only the `sourceText` string already extracted server-side.  It cannot browse, search, or verify anything beyond what is in that one string.
- **System prompt.**  A single paragraph instructing the model to infer audience/objective/angle, recommend one primary angle plus up to two lenses, default to US English, and "respond with the requested JSON object only."  It does **not** instruct the model to verify claims, does not establish an editor persona or quality bar, and does not mention analytical depth, distinctiveness, or a target audience's practical needs.
- **Source retrieval.**  `retrieveSource()`: a single `fetch()` (10s timeout, 2MB cap), `html-to-text` conversion stripping `script`/`style`/`nav`/`footer`/`img`, then `.slice(0, 12_000)` (`MAX_SUMMARY_CHARS`).  No readability/main-content extraction beyond tag-based stripping; no retry, no JavaScript rendering.
- **Schema.**  `source_understanding` (max 2000 chars), `audience` (max 300), `objective` (max 300), `publication_language` (max 60), `primary_angle` (max 500), `supporting_lenses` (0-2 items, each max 500), `editorial_thesis` (max 1000).  Enforced twice: OpenAI's strict `json_schema` mode, then a `zod` schema (`schema.ts`) before persistence.
- **Retry.**  One bounded retry (`MAX_ATTEMPTS = 2`) on schema-validation failure only - not on quality grounds.
- **Persistence.**  `ProjectRepository.createEditorialDirection` persists the seven fields as-is (no transformation) and advances `EditorialProject.stage`.

## 3. Difference Analysis

| Dimension | Locked GPT | Current Web | Classification |
|---|---|---|---|
| Model capability | Current flagship conversational model (explicit recommendation) | `gpt-4o-mini` (small/cheap tier, explicitly deferred as "an implementation detail, never accepted as a product quality decision") | **Likely quality-relevant** |
| Instruction completeness / persona | Full "skilled editor" framing, applies to every stage | Narrow, mechanical, schema-filling instructions only | **Likely quality-relevant** |
| Verification requirement | Explicit: "verify important claims" | Absent entirely | **Likely quality-relevant** |
| Retrieval / verification tooling | Real web-search/browsing tool (Web Search: ON) | None - one static pre-fetched text snapshot only | **Likely quality-relevant** (context/source-processing) |
| Analytical depth / distinctiveness bar | Implied by editor persona; explicit at Draft stage ("specific evidence, no padding") | Not present at the Direction stage | **Possibly quality-relevant** |
| Source extraction quality | N/A (model's own browsing) | Basic tag-stripped `html-to-text`, no main-content/readability extraction | **Possibly quality-relevant** |
| Source length bound | N/A (model's own browsing, can revisit) | Hard cut at 12,000 characters | **Possibly quality-relevant** (mainly for long sources) |
| Schema field-length limits | N/A (free-form chat) | `source_understanding` <= 2000, `editorial_thesis` <= 1000, etc. | **Unlikely quality-relevant** - generous for a consolidated direction |
| Retry policy | N/A | Schema-validation retry only, not quality-based | **Implementation-only / not editorially relevant** |
| Persistence / transformation | N/A | Fields persisted as-is, no post-processing | **Implementation-only / not editorially relevant** |
| House style (dash/spacing) | Explicit, enforced by instruction | Not addressed in the Direction task's system prompt | **Unlikely quality-relevant** to substance; cosmetic |

No assumption was made that the model alone explains the gap merely because it differs, or that the prompt alone explains it merely because the locked GPT's instructions are longer - both are supported independently above: the model difference is evidenced by the explicit Section 9 recommendation the Web Product has not adopted, and the prompt difference is evidenced by concrete missing instructions (verification, persona, depth), not merely length.

## 4. Evaluation Design

### 4.A Rubric (1-5 per dimension; Repository Author judgment is authoritative, agent scoring is supporting evidence only)

1. Source fidelity - does it accurately reflect the source, including material uncertainty?
2. Strength of central editorial thesis
3. Specificity (vs. generic restatement)
4. Analytical depth
5. Usefulness to a manager/practitioner audience
6. Identification of the non-obvious implication
7. Practical direction
8. Absence of generic filler
9. Appropriate confidence/qualification
10. Structural completeness (all seven fields genuinely useful, not filler)
11. Editorial distinctiveness

### 4.B Evaluation matrix

Four variants, holding one variable constant per comparison, using the same source material throughout:

| Variant | Model | Prompt | Context / Schema | Isolates |
|---|---|---|---|---|
| A | `gpt-4o-mini` (current default) | Current production prompt | Current (unchanged) | Reproduces current production baseline |
| B | `gpt-4o-mini` | Improved, baseline-aligned prompt (adds editor persona, claim-uncertainty handling, distinctiveness bar - no browsing tool assumed) | Current (unchanged) | Prompt effect |
| C | `gpt-5.6-terra` (candidate) | Current production prompt | Current (unchanged) | Model effect |
| D | `gpt-5.6-terra` | Improved prompt | Current (unchanged) | Combined effect / best achievable configuration |

The "improved" prompt is implemented in the evaluation harness (Section 5) as `IMPROVED_SYSTEM_PROMPT` and is a candidate for review, not an adopted change.

### 4.C Source material

The original 2026-08-11 hosted-acceptance source URL is not recorded in `ROADMAP.md`, `HANDOFF.md`, or PV-029 - only the Repository Author's qualitative judgment is recorded, not the specific source or generated output.  Per this sprint's instruction not to invent unrecoverable evidence, the original comparison cannot be reproduced verbatim.  A representative substitute is recommended instead: the same URL already used and recorded for the locked GPT's own PV-017 validation (`https://thehackernews.com/2026/08/new-css-attacks-can-break-webmail.html`), which keeps the evaluation within the same source category (technical/professional article suitable for LinkedIn thought leadership) already precedented in this repository's own validation history.

## 5. Evaluation Harness (built, not yet executed)

`web/server/eval/editorial-direction-eval.mjs` - a standalone, dependency-free script (Node's built-in `fetch` only; no `npm install` required) that replicates the exact production request shape (model, both prompt variants, JSON schema, Structured Outputs).  It fails closed with a clear error and makes no network call when `OPENAI_API_KEY` is unset - verified directly in this session (see Section 8).

**Not executed in this session:** this sandboxed environment has no `OPENAI_API_KEY` in its process environment and no `web/server` npm dependencies installed (`node_modules` is empty and gitignored).  Real evaluation calls were authorized for this sprint but require an environment with a configured key.  The harness is ready to run as-is, by the Repository Author or a future Claude session with `OPENAI_API_KEY` configured, following the usage instructions in the script's header comment.

## 6. Usage / Cost Comparison

**Measured usage:** none - no evaluation calls were executed in this session (Section 5).

**Estimated cost**, from reference pricing captured 2026-08-11 (`developers.openai.com/api/docs/pricing`; verify before relying on it, pricing changes independently of this document) and a representative 3,000-input / 400-output-token Editorial Direction request (approximate size for a 12,000-character source and a seven-field structured response):

| Model | Input $/1M | Output $/1M | Est. cost per request | Positioning (OpenAI's own guidance) |
|---|---|---|---|---|
| `gpt-4o-mini` (current default) | $0.15 | $0.60 | ~$0.0007 | Small/cheap tier, superseded generation |
| `gpt-5.6-luna` | $0.20 | $1.20 | ~$0.0011 | "Efficient, high-volume workloads" |
| `gpt-5.6-terra` (recommended candidate) | $2.00 | $12.00 | ~$0.0108 | "A balance of intelligence and cost" |
| `gpt-5.6-sol` | $5.00 | $30.00 | ~$0.0270 | "Complex production workflows... frontier capability" |
| `gpt-4o` (for reference) | $2.50 | $10.00 | ~$0.0115 | Prior-generation flagship |

At current, pre-scale Editorial Project volumes, the absolute cost difference between `gpt-4o-mini` and `gpt-5.6-terra` is small in dollar terms (roughly one cent per request) even though it is a roughly 15x per-token cost increase - the quality question, not the absolute cost, should govern this decision at this product stage.

Sources: [OpenAI API pricing](https://developers.openai.com/api/docs/pricing), [OpenAI model guidance](https://developers.openai.com/api/docs/guides/latest-model), [OpenAI Structured Outputs guide](https://developers.openai.com/api/docs/guides/structured-outputs).

## 7. Findings

Ranked by strength of evidence, not assumption:

1. **Prompt/instruction completeness (primary suspect).**  The current system prompt omits verification, editor-quality framing, and any distinctiveness/depth bar - not merely "shorter" than the locked GPT's, but missing specific, evidenced instructions the locked GPT relies on.  This is a zero-marginal-cost factor and the most concretely evidenced difference.
2. **Model capability (significant contributing factor).**  `gpt-4o-mini` was adopted as an implementation detail during Web Walking Skeleton 01, never evaluated as a quality decision, and directly contradicts the locked GPT's own explicit flagship-model recommendation for this exact kind of task (long-form editorial writing, moderate evidence reasoning).
3. **Missing verification/browsing capability (significant, but architecturally distinct).**  The locked GPT can search and cross-reference; the Web path sees one static, already-truncated text snapshot.  This plausibly explains weaker "verify important claims" behavior specifically, but adding real-time browsing is a larger architectural change than a prompt or model swap and is not recommended as part of this sprint's immediate next step.
4. **Source extraction and truncation (possible, secondary).**  Reasonable for most single-article sources; more likely to matter for unusually long sources.  Not the primary explanation for a "materially weaker" result on ordinary source material.
5. **Schema constraints (unlikely primary cause).**  Field-length limits are generous for a consolidated direction; strict-mode Structured Outputs is standard practice and shared by every current-generation model considered here.

## 8. Limitations

- No live model comparison was executed in this session - `OPENAI_API_KEY` is not available in this environment, and `web/server`'s npm dependencies are not installed here.  Findings above are based on code- and documentation-level evidence, not empirical output comparison.
- The original 2026-08-11 acceptance source/output could not be recovered (Section 4.C); a representative substitute source is recommended instead.
- Harness safety was verified (fails closed, no network call, no secret exposure without a key - Section 5), but its actual generation behavior across the four variants has not been observed.
- Cost estimates use a representative token-count assumption, not measured usage; actual costs will vary by source length and output verbosity.

## 9. Recommendation (Provisional - Not Yet Proven)

**Everything below is a hypothesis grounded in code- and documentation-level evidence, not a proven conclusion.**  Section 8's limitations apply directly: no controlled comparison has been executed.  This section states what the evidence currently points to and what would need to happen to treat it as confirmed - it does not itself establish Category E as the root cause or authorize adopting `gpt-5.6-terra`.

**Provisional category: E - combination (prompt + model, with an architecturally larger factor noted but not recommended for immediate action).**  This classification should be treated as the leading hypothesis to test, not a settled finding.

- **Model/configuration:** adopt `gpt-5.6-terra` as the Editorial Direction model, pending empirical confirmation via the evaluation matrix (Section 4.B) run through the harness (Section 5).  It is OpenAI's own current "balance of intelligence and cost" tier, directly answering BL-002, and aligns with the locked GPT's flagship-not-reasoning-optimized principle applied to the current model lineup.
- **Prompt:** adopt the `IMPROVED_SYSTEM_PROMPT` candidate in the harness (or a Repository-Author-refined version of it) after review - it closes the concretely identified gaps (verification framing, editor persona, distinctiveness bar) without requiring browsing-tool access the Web path does not have.
- **Not recommended for this sprint:** adding real-time web-search/verification tooling.  It is a plausible contributing factor but a materially larger architecture change; revisit only if the prompt+model change (once empirically tested) does not close the gap sufficiently.
- **Quality/cost tradeoff:** the model change is a real per-token cost increase (roughly 13x versus `gpt-4o-mini`) but a small absolute cost at current volumes (Section 6); the prompt change is free.  Neither implies a schema, persistence, or architecture change - both are configuration/prompt-level changes to the existing `chat.completions.create` call.
- **Web Walking Skeleton 02 readiness (Question 5):** **not yet.**  The causal hypothesis is now well-evidenced and specific, but not empirically confirmed - proceeding to deepen the generation pipeline (BL-003) before running the designed evaluation would still carry the rework risk `BACKLOG.md` already flags.  Running Section 4.B's matrix through the harness is a small, fast next step relative to that risk.

This recommendation requires a model swap, which is a production change - per this sprint's implementation-authorization boundary, no code change is made here.  The optional narrow prompt-only stretch was considered and **not attempted**: the evidence supports prompt **and** model together, not a prompt-only fix in isolation, and Section 8's limitations mean condition 1 of the stretch ("evidence clearly identifies a prompt/instruction-only improvement") is not confidently met without the empirical comparison this session could not run.

## 10. Remaining Repository Author Decisions

1. Whether to run the evaluation harness (Section 5) - in an environment with `OPENAI_API_KEY` configured and `web/server` dependencies installed via the repository's normal `npm ci` process - and review the resulting four-variant comparison before any implementation decision.
2. Whether to authorize the `gpt-5.6-terra` model change and the `IMPROVED_SYSTEM_PROMPT` (or a refined version) for implementation, once the comparison is reviewed.
3. Whether BL-003 (Web Walking Skeleton 02) should remain sequenced after this resolution, per `BACKLOG.md`'s existing dependency note.

## 11. Recommended Codex Review Scope

Not started automatically.  If the Repository Author authorizes the model/prompt change for implementation, recommend a narrow Codex review scoped specifically to: (a) confirming the change is genuinely prompt/configuration-only with no schema, persistence, or Approve/Reject workflow drift, and (b) independently reproducing at least one of the four evaluation variants to confirm the reported comparison is genuine and reproducible - matching the risk categories (persistence, workflow state, evidence verification) the Delivery Operating Model reserves Codex review for, not a blanket second pass.

## 12. Execution Boundary - Safe Path to Run the Evaluation (Approved and Executed)

Recorded 2026-08-11, before any evaluation call was made, in response to the Repository Author's request to determine the safest way to execute Section 4.B's matrix without exposing or copying the Render-hosted `OPENAI_API_KEY`.  The Repository Author approved this path (with a hard bound of 4 calls, variants A/B/C/D only) and confirmed `OPENAI_API_KEY` was already present in `web/server/.env`.  It was never inspected, printed, echoed, or copied - the harness's `loadLocalEnvIfPresent()` loads it via Node's built-in `process.loadEnvFile()`, the same mechanism production's own `dotenv.config()` call would use, and never logs the value.  Execution is recorded in Section 13.

**Why Render's key cannot be used directly here.**  `render.yaml` sets `OPENAI_API_KEY` with `sync: false` - by design, its value exists only inside the Render dashboard and the running Render service's environment, never in any tracked file, and is not retrievable by an agent working in this local repository checkout.  This is correct, established behavior (see `docs/learning/AI_Developer_Bootstrap_Lessons.md` Section 6) and was not worked around.

**Recommended path: a fresh local key, entered directly by the Repository Author.**  This repeats the exact pattern already used successfully for the original OpenAI foundation verification (`Web_Product_Foundation_v1.md` Section 13): the Repository Author enters an `OPENAI_API_KEY` (the same key or a distinct one, their choice) directly into a local, gitignored location - `web/server/.env`, verified ignored first via `git check-ignore -v web/server/.env`, or simply exported in the shell for a single command - never pasted into chat, never handled by an AI participant.  The harness (`web/server/eval/editorial-direction-eval.mjs`) then reads it from `process.env`, exactly as production code does, and never logs it.

**Dependency installation - not required for the harness.**  The harness was deliberately built dependency-free (Node's built-in `fetch` only); it imports nothing from `web/server/node_modules`.  Running it requires no `npm install` or `npm ci` at all.  Dependency installation would only become relevant if the Repository Author instead wanted to exercise the real production TypeScript path (e.g., via `npm run dev` or an integration test) for an even more faithful reproduction - that would require `npm ci` (or `npm ci --include=dev` if typecheck/build is also needed) run from `web/` (the npm-workspaces root; `web/package-lock.json` is committed, so this installs already-locked versions, not new ones - the same command `render.yaml`'s own build already runs).  `AGENTS.md`'s Approval Boundaries list "installing dependencies" unconditionally, with no exception for locked/existing versions, so this would still require explicit Repository Author approval before being run, even though it is low-risk and already precedented.  It is not needed for the recommended harness path.

**Render as an alternative - possible but not recommended.**  Render's Shell feature (dashboard-only, browser-based) would let a script run inside the live service's environment, using `OPENAI_API_KEY` in place without ever displaying it - technically avoiding exposure.  Not recommended as the primary path: it requires the Repository Author to manually operate the Render dashboard and paste the harness script in (no reduction in their effort), mixes investigation traffic with the production service's runtime context, and is harder to iterate on than a local run.  The local-key path above achieves the same secrecy guarantee with less friction.

**Expected OpenAI calls and approximate cost.**  Section 4.B's matrix is four variants (A, B, C, D), one call each for an initial pass: 4 calls total.  Using Section 6's estimated per-request costs, the most expensive pairing (`gpt-5.6-terra`, variants C and D) is approximately $0.0108 each, and the cheapest (`gpt-4o-mini`, variants A and B) approximately $0.0007 each - **approximately $0.023 total for one pass**, well under five cents.  If results are ambiguous and the Repository Author wants multiple repetitions per variant for reliability (e.g., three reps, twelve calls), the total remains under $0.10.  No broad benchmarking or multi-model sweep is proposed.

**Recommendation summary:** the Repository Author provisions a fresh local `OPENAI_API_KEY` (Section 12, "Recommended path"); no dependency installation is required for the harness; four OpenAI calls (~$0.02) are expected for one pass of the evaluation matrix; Render's key remains untouched and unexposed throughout.  No call has been made; this is a proposal awaiting explicit approval.

## 13. Executed Comparison Results (2026-08-11) - Awaiting Repository Author Review

**Not a conclusion.**  This section reports what the four approved calls produced.  The Repository Author has not yet reviewed it; no winner is declared here, and Category E (Section 9) remains provisional until that review happens.

**Source:** the same URL used for the Section 5 fidelity test (Section 4.C), 9,768 extracted characters, reused unchanged across all four variants so the disclosed boilerplate (Section 5 fidelity notes) affects every variant equally rather than biasing the prompt-effect or model-effect comparison.

**Usage, latency, and cost (all measured, not estimated):**

| Variant | Model | Prompt | Tokens (prompt/completion/total) | Latency | Actual cost |
|---|---|---|---|---|---|
| A | `gpt-4o-mini` | current | 2428 / 223 / 2651 | 4804ms | $0.000498 |
| B | `gpt-4o-mini` | improved | 2629 / 287 / 2916 | 3519ms | $0.000567 |
| C | `gpt-5.6-terra` | current | 2426 / 325 / 2751 | 5765ms | $0.008752 |
| D | `gpt-5.6-terra` | improved | 2627 / 466 / 3093 | 7354ms | $0.010846 |

**Total measured cost for the 4-call pass: $0.020663** - within the approved bound and closely matching Section 12's $0.023 estimate.  All four calls returned schema-valid, parseable output on the first attempt; no retries were needed.

**Generated output** (each variant's full `editorial_thesis` and `primary_angle`, the two fields most directly reflecting editorial judgment; full JSON for all seven fields per variant is in the local, uncommitted results file the harness wrote, per its header note not to commit raw evaluation output):

- **A** (`gpt-4o-mini` / current): *Primary angle:* "Emerging CSS vulnerabilities pose serious threats to webmail security, highlighting the need for robust defensive practices." *Thesis:* "As webmail continues to be a key conduit for sensitive information, understanding and mitigating emerging CSS attack vectors is crucial for maintaining user security and trust."
- **B** (`gpt-4o-mini` / improved): *Primary angle:* "Webmail security is critically compromised by new CSS vulnerabilities, requiring urgent action from service providers to implement more robust isolation and security controls to thwart sophisticated credential theft and data exfiltration efforts." *Thesis:* "Cybersecurity managers should prioritize understanding and addressing the latest CSS vulnerabilities in webmail platforms, as these represent an evolving threat landscape that endangers user data and corporate security."
- **C** (`gpt-5.6-terra` / current): *Primary angle:* "The webmail trust-boundary failure: why allowing email content to interact with the surrounding application UI creates identity-security risk." *Thesis:* "Webmail security cannot be reduced to phishing filters: when untrusted email HTML and CSS can influence trusted interface behavior, browsers and AI integrations can turn message rendering into a route to credential, token, and privacy compromise."
- **D** (`gpt-5.6-terra` / improved): *Primary angle:* "Email rendering is no longer a self-contained phishing surface... permitted markup and browser/application parsing differences can let untrusted message content cross into trusted webmail UI and AI-connected workflows, turning defensive conveniences... into credential and token-exfiltration paths." *Thesis:* "The webmail threat model must shift from treating malicious email as a content-filtering problem to treating it as untrusted code containment: if message HTML/CSS can influence trusted interface elements, browser behavior, or connected AI workflows, sanitization alone is not a dependable security boundary."

**Agent rubric assessment (supporting evidence only, per Section 4.A - the Repository Author's judgment is authoritative, not this scoring).**  Approximate 1-5 averages across the 11 rubric dimensions: A ~2.5, B ~3.3, C ~3.9, D ~4.5.  The pattern was monotonic (D > C > B > A) on nearly every individual dimension, not just the average, which is itself notable.

**Qualitative observations, offered as evidence, not as a declared winner:**

- A (current prompt/current model) produced the most generic framing of the four - a plausible but unremarkable summary, closest to what PV-029 originally described as "materially weaker."
- B (improved prompt/current model) added concrete specifics (named platforms, message-boundary escaping, disguised UI elements) absent from A, without any model change - direct evidence of a real, non-zero prompt effect.
- C (current prompt/stronger model) reframed the story around a "trust-boundary failure" and named the source research (PortSwigger, Black Hat USA 2026) despite using the *same weaker prompt as A* - direct evidence of a real, non-zero model effect independent of the prompt.
- D (improved prompt/stronger model) was the only variant to explicitly hedge on unverified claims ("Claims and vendor-fix status are reported by the article and underlying researchers, not independently verified here") - directly traceable to the improved prompt's verification/uncertainty instruction, and only appearing when paired with the stronger model.

This pattern is consistent with, and provides the first empirical support for, Section 9's provisional Category E finding (prompt and model both contribute, in different and complementary ways) - but it is one source, one pass, no repetitions, and Repository Author review has not happened.  It should not yet be treated as proof.

**Not done:** no winner declared, no production change made, BL-001 remains In Progress (not Review / Validation) pending this review, per the Repository Author's explicit condition.

## 14. Second Pass - Cross-Source Generalization Check (2026-08-11) - Awaiting Repository Author Review

**Not a conclusion.**  A second, independently authorized bounded pass (4 more calls, variants A/B/C/D, no repetitions) was run against a materially different source to test whether Section 13's pattern generalizes or was an artifact of one source.  Same extraction method, same matrix, same rubric, no manual trimming, exactly as instructed.  The Repository Author has not yet reviewed this section either; Category E remains provisional.

**Source:** `https://www.nasa.gov/news-release/nasa-joins-genesis-mission-to-accelerate-ai-driven-discovery/` (NASA science/AI-policy, versus Section 13's cybersecurity source - a materially different topic and domain).  Extraction produced 11,527 characters, of which approximately the first 1,258 lines were navigation-menu noise (NASA.gov's mega-menu is not wrapped in semantic `<nav>` tags any more than Section 13's source's chrome was) - proportionally *more* noise than Section 13's source, making this an incidental stress test of the noise question below.  The real article content was fully present, unmodified, and untrimmed within the 12,000-character cap.

**Usage, latency, and cost (all measured):**

| Variant | Model | Prompt | Tokens (prompt/completion/total) | Latency | Actual cost |
|---|---|---|---|---|---|
| A | `gpt-4o-mini` | current | 2950 / 240 / 3190 | 3278ms | $0.000586 |
| B | `gpt-4o-mini` | improved | 3151 / 244 / 3395 | 2518ms | $0.000619 |
| C | `gpt-5.6-terra` | current | 2948 / 313 / 3261 | 5707ms | $0.009652 |
| D | `gpt-5.6-terra` | improved | 3149 / 401 / 3550 | 6875ms | $0.011110 |

**Total measured cost for this pass: $0.021967** (combined with Section 13: $0.04263 across both passes).  All four calls returned schema-valid output on the first attempt; no retries needed.

**Generated output** (`primary_angle` and `editorial_thesis` per variant; full seven-field JSON is in the local, uncommitted results file):

- **A** (`gpt-4o-mini` / current): *Primary angle:* "The role of artificial intelligence in enhancing scientific discovery and accelerating innovations in space and related fields through the Genesis Mission." *Thesis:* "NASA's involvement in the Genesis Mission signifies a transformative step in employing artificial intelligence to not only speed up scientific discoveries but also to redefine how humanity explores and understands the universe."
- **B** (`gpt-4o-mini` / improved): *Primary angle:* "The Genesis Mission represents a significant integration of AI into government-funded scientific research, positioning NASA to transform its vast data reserves into actionable knowledge..." *Thesis:* "Harnessing AI through the Genesis Mission will not only streamline NASA's research processes but also unlock previously inaccessible scientific insights, solidifying the United States' position as a leader in space and technology innovation." (`supporting_lenses` was empty for this variant - the improved prompt's "do not pad the list" instruction produced zero rather than the one-or-two seen elsewhere.)
- **C** (`gpt-5.6-terra` / current): *Primary angle:* "From data archive to discovery engine: how NASA plans to use AI to extract more value from 150+ petabytes of mission data while accelerating the design and operational readiness of integrated space systems." *Thesis:* "NASA's participation in the Genesis Mission shows that AI's highest-value role in science may be turning decades of complex, underused mission data and engineering expertise into faster, more connected discovery and mission readiness."
- **D** (`gpt-5.6-terra` / improved): *Primary angle:* "From archive to advantage: NASA's AI opportunity is to unlock returns from existing public investments by connecting vast historical data with mission engineering - not merely to automate research." *Thesis:* "NASA's Genesis Mission signals that the strategic value of AI in science is not simply faster analysis: it is the ability to turn decades of fragmented, under-examined mission data and engineering knowledge into a continuously reusable discovery and mission-readiness asset, provided AI is integrated with domain expertise and operational systems." *Source understanding* explicitly noted: "the release... provides no implementation plan, governance details, technical benchmarks, funding information, or evidence that these outcomes have yet been achieved" - an even more explicit instance of the improved prompt's verification/uncertainty instruction than Section 13's D variant produced.

**Agent rubric assessment (supporting evidence only).**  Approximate 1-5 averages: A ~2.7, B ~3.0, C ~3.9, D ~4.6 - the same ordering as Section 13 (D > C > B > A).

### Answering the four generalization questions

- **Does A -> B demonstrate a repeatable prompt effect?**  Directionally yes, but weaker here than in Section 13.  B added audience specificity ("managers and practitioners") and a marginally sharper thesis, but the jump from A was less pronounced than Section 13's, and `supporting_lenses` came back empty rather than populated.  The prompt effect appears real but source-dependent in magnitude, not a fixed, uniform improvement.
- **Does A -> C demonstrate a repeatable model effect?**  Yes, and strongly.  In both passes, C reframed the story with a distinct, specific angle ("data archive to discovery engine" here; "trust-boundary failure" in Section 13) using the *identical, weaker prompt as A* - the cleanest repeated evidence in this investigation, since prompt is held constant and only the model changes.
- **Does D remain strongest overall?**  Yes in both passes, by the same rubric and the same qualitative markers (most distinctive framing, most explicit epistemic hedging, most actionable for the stated audience).
- **Does source-extraction noise materially change the result?**  No evidence that it did, in either pass.  This source had proportionally more raw navigation noise than Section 13's, yet all four variants correctly identified and summarized the real article content with no visible contamination from the surrounding menu text.  This is reassuring but based on only two sources - it should not be read as a general guarantee that extraction noise never matters.

### Assessment: no material contradiction found

Per the Repository Author's stop condition, the two passes were compared for material contradiction before writing this section.  None was found: the core pattern (model effect strong and repeatable; prompt effect real but variable in magnitude; D strongest in both; noise not clearly harmful in either case) held across two materially different sources.  No further calls were made or are proposed.  This strengthens, but does not prove, Section 9's provisional Category E hypothesis - two sources, one pass each, is still a small evidence base.

**Not done:** no winner declared, no production change made, BL-001 remains In Progress, per the Repository Author's explicit condition.

## 15. Repository Author Decision (DEC-030) - Final Conclusion

**Approved 2026-08-11.**  The Repository Author reviewed Sections 13-14 and judged the two-source evidence sufficient for a product decision: the same D > C > B > A ordering on materially different sources, a repeatable model effect (A -> C) holding the prompt constant, a repeatable-but-variable prompt effect (A -> B), and no material contradiction between passes.

**Decision:** adopt `gpt-5.6-terra` as the Editorial Direction model and the Variant D "improved" instructions as the Editorial Direction system prompt, replacing `gpt-4o-mini` and the current production prompt respectively.  Schema, persistence, source retrieval/processing, and Approve/Reject behavior are explicitly unchanged.  Recorded formally as `product/validation/Product_Decisions.md` DEC-030.

This closes Section 9's "provisional" status for the purpose of authorizing implementation - Category E (prompt + model combination) is the accepted basis for the approved configuration.  Sections 9, 13, and 14 above are left as written; they are the evidentiary record the decision was based on, not superseded text.

**Not authorized by this decision:** the implementation itself.  DEC-030's Implementation Status field is the authoritative scope boundary for that separate, bounded delivery - model selection and Editorial Direction instructions only, with schema, persisted shape, source-processing, workflow state, Approve/Reject, authentication, Render, the locked GPT, and GPT Knowledge all explicitly out of scope, plus required regression tests and one bounded real verification through the actual Web Product path before that delivery can be considered complete.

## 16. Implementation and Post-Merge Hosted Acceptance (2026-08-11) - Closure

**Implementation.** The bounded delivery DEC-030 authorized was completed on `feature/editorial-direction-gpt-5-6-terra`: `getConfiguredModel()` defaults to `gpt-5.6-terra` (`OPENAI_MODEL` remains a supported override), the Editorial Direction system prompt was replaced with the approved Variant D instructions verbatim, and `render.yaml`'s `OPENAI_MODEL` value was updated to match.  Schema, persistence, source retrieval/processing, Approve/Reject behavior, and authentication were unchanged, per DEC-030's scope boundary.  New regression coverage (`web/server/tests/editorialDirection.model.test.ts`) guards the model default and override, the exact prompt text, the unchanged schema, and unchanged user/source message construction.  Full verification passed: typecheck, lint, 41/41 tests, build, and repository validation (`compileall`, 484 Python unittests, `studio.py validate`).  One bounded real application-path call (not mocked) confirmed the deployed request shape end-to-end before merge.  Merged to `develop` as PR #130, commit `afb07eb`.

**Post-merge hosted acceptance.** The Repository Author completed literal hosted acceptance through `https://studio.ramrattan.com` against the merged commit:

- Hosted health - `/api/health` returned `{"status":"ok"}`.
- Authentication - normal magic-link sign-in succeeded; the authenticated application loaded correctly.
- Editorial Project creation - a new hosted project (`REP-97BE2BC6`) was created successfully.
- Real public-URL submission - the same NASA source used in Section 14's second evaluation pass (`https://www.nasa.gov/news-release/nasa-joins-genesis-mission-to-accelerate-ai-driven-discovery/`) was accepted and processed, after an unrelated first URL returned an HTTP 403 during source retrieval (a source-retrieval-target issue, not a DEC-030 model or implementation defect; source-processing code was not changed).
- Editorial Direction generation - succeeded through the real hosted application path.
- Runtime model evidence - fresh Render `[openai-usage]` log entries showed `model: 'gpt-5.6-terra'`, confirming the deployed Render environment is using the DEC-030-approved model, not a stale `gpt-4o-mini` override.
- Schema/rendering - the hosted Editorial Direction rendered all seven unchanged fields: `source_understanding`, `audience`, `objective`, `publication_language`, `primary_angle`, `supporting_lenses`, `editorial_thesis`.
- Persistence/rehydration - a browser refresh preserved and rehydrated the generated Editorial Direction.
- Reject behavior - Reject exposed the expected feedback workflow; feedback was submitted, the project showed "Changes requested", and the feedback remained present after a browser refresh.
- Approve behavior - an existing Editorial Direction project (`REP-82C8BD41`) was used for the normal approval path; approval succeeded, the project displayed "Approved", and the UI confirmed advancement to the Editorial Plan stage.
- Authentication protection - after sign-out, protected application content was no longer available and the application returned to the sign-in / magic-link request screen.

**Conclusion.** All required hosted acceptance criteria passed.  BL-001's Outcome is achieved to the standard this delivery was scoped to prove.  DS-01 is closed; see `BACKLOG.md`'s "Latest Closeout" section for the operating-model record.
