# Web Product Foundation v1

**Status:** Version 2 Candidate
**Classification:** Lean Foundation Spike
**Architecture:** Application-owned workflow state; AI performs bounded editorial tasks
**Governance Status:** Informative - Not Yet Approved for Full Implementation

## 1. Objective

Define the minimum technical foundation required to begin building the
browser-based Ramrattan AI Editorial Studio web product, so the next
Engineering Delivery can build one real, end-to-end vertical slice
without another architecture discussion:

```text
Sign In -> Create Editorial Project -> Paste URL -> Research /
Editorial Direction -> real Approve / Reject controls
```

This is a foundation spike, not an architecture program. It makes only
the decisions needed to start implementation. It does not authorize
building the full product, and it does not modify the locked private
GPT (`GPT Recovery RC5 - Locked Private GPT Baseline`,
`deployment/openai_gpt/GPT_Configuration_v2_RC1.md`) - that artifact
remains a validated behavioral reference, not the web product's
implementation architecture.

**Governing principle:** the web application owns workflow state -
current stage, available actions, Approve/Reject controls, navigation,
persistence, project ownership, and completion. The model performs
bounded editorial tasks inside that state. The Custom GPT's
prompt-driven state machine is not recreated in the browser.

## 2. Existing Baseline / Reuse

The repository contains a complete, tested, provider-independent Python
**domain model** of the Editorial Studio (`studio/`, 484 passing tests)
but **no web application code**: no frontend, no HTTP server, no
database, no OpenAI SDK usage, and no external dependencies anywhere in
`studio/` or `scripts/` (stdlib-only, confirmed by import inspection).
The web product is greenfield at the infrastructure layer; it is not
greenfield at the product-logic layer.

| Component | Classification | Notes |
|---|---|---|
| `studio/editorial_guidance.py` (`EditorialStage`, `StageState`) | Adapt | Existing five-stage enum (Understanding Input, Assessing Sources, Verifying Evidence, Reviewing Editorial Risks, Creating Publication Package) is a reasonable starting point for the backend workflow-state model, not a literal reuse - the web product's first slice only needs Source -> Editorial Direction. |
| `studio/editorial_intake.py` (`InputKind`) | Adapt | Canonical intake classification (URL, pasted text, document, etc.) is directly relevant to the `Source` entity and intake validation. |
| `studio/evidence_validation.py` (`EditorialRisk`, `EditorialConfidence`) | Reuse as-is (concept) | LMHS risk scale and confidence vocabulary are canonical product terms; port the enums, not necessarily the full pipeline, into the first slice. |
| `studio/article_engine.py`, `studio/publication_package.py` | Retire / do not use in slice 1 | Deterministic, provider-independent Article Engine and package assembly are valuable references for later article-generation work but are out of scope for the walking skeleton (see Section 9, Section 10). |
| `studio/hero_visual.py` (`HeroVisualProvider` Protocol, `HERO_VISUAL_WIDTH/HEIGHT = 720/425`) | Adapt | The `Protocol`-based provider abstraction and the existing 720 x 425 dimension constants and PNG validation are the right pattern for the future Hero Visual pipeline (Section 8) - swap the deterministic provider for a real OpenAI image provider behind the same interface. |
| `studio/portable_editorial_project.py` (`REP-[A-F0-9]{8}` project ID, JSON schema) | Adapt | Already defines a project identifier scheme and a versioned, human-readable JSON schema for editorial state. The web product's persistent `EditorialProject` should reuse this ID shape and schema-versioning discipline rather than inventing a new one. |
| `studio/workflow/` (`EditorialState`, `choices.py`) | Retire / do not use | This is the Version 1 CLI/demo workflow's own state shape (Carousel slides, hero copy direction, etc.) and predates the Version 1.1 Author Journey. Superseded by `editorial_guidance.py` and the Portable Editorial Project schema; do not extend it. |
| `deployment/openai_gpt/GPT_Configuration_v2_RC1.md` | Unrelated (do not touch) | Validated behavioral reference for editorial tone, sequencing, and UX lessons (Approve/Reject vocabulary, no re-asking supplied input, atomic transitions). Locked; not modified by this document. |
| `docs/architecture/Version_1_1_State_Machine.md`, `Version_1_1_Author_Experience_Baseline.md` | Reuse as-is (behavioral spec) | The canonical Author Journey (Welcome -> Editorial Source -> Branding -> Editorial Discovery -> Editorial Plan -> Generation -> Publication Studio) is the target full product; the walking skeleton implements its first two-and-a-half stages only. |
| `docs/product/version2/Capability_013_Reader_Engagement.md` | Reuse as-is (constraint) | Establishes that publication must not terminate the Editorial Project, and that comment ingestion is unresolved and LinkedIn-dependent. Section 6 and Section 10 of this document carry that constraint forward. |
| Bootstrap/delivery tooling (`scripts/`, `AGENTS.md`, `docs/engineering/*`) | Reuse as-is | Governance, validation, and delivery discipline apply unchanged to web-product engineering; no new process is introduced. |

## 3. Foundation Decisions - Web Stack

**Decision:** Thin, conventional stack - a TypeScript/Node.js backend
(e.g. a minimal REST API), a server-rendered or lightly hydrated React
frontend, PostgreSQL for persistence, deployed to a managed
container/PaaS platform (e.g. Fly.io, Render, or Railway) with separate
`development` and `production` environments and environment-scoped
secrets.

**Why:** Nothing in the repository constrains frontend/backend
technology (`studio/` is a pure-Python domain model with no web
framework). A conventional, boring stack minimizes new tooling risk for
a one-slice walking skeleton and keeps the team's attention on proving
the state-ownership principle (Section 1), not on stack novelty. A
managed relational database gives the walking skeleton real persistence
with minimal operational burden; Postgres specifically because the data
model (Section 6) is relational and will need constrained enums, foreign
keys, and JSON columns for portable-schema fields.

**What is deferred:** exact frontend framework/component library choice
beyond "React," exact managed-hosting vendor, CI/CD pipeline detail,
infrastructure-as-code, autoscaling, and multi-region deployment. These
are ordinary implementation decisions for the next delivery, not
foundation decisions requiring Repository Author review.

## 4. Authentication Decision

**Current official-documentation finding (OpenAI, retrieved
2026-08-10):** There is no officially documented, generally available
"sign in with ChatGPT and use my ChatGPT Plus/Pro subscription"
capability for independent third-party web applications. Public
reporting (OpenAI Developer Community, TechCrunch) describes a "Sign in
with ChatGPT" identity feature (name, email, profile picture) that was
piloted with one-time incentive API credits for early adopters through
OpenAI's own Codex CLI specifically - not ongoing subscription
delegation to arbitrary third-party apps. The dedicated documentation
URL for this feature
(`developers.openai.com/api/docs/guides/sign-in-with-chatgpt`) returned
HTTP 404 at time of retrieval. A direct 2023-2026 community feature
request asking OpenAI to let users "use their own message
credits/limits instead of the developer's API" remains an open request
with no confirmed official resolution. **This must be stated plainly:
the web product cannot consume an Author's ChatGPT Plus/Pro subscription
in place of its own OpenAI API billing.**

**Decision:** Email magic link for MVP Author authentication, issued and
verified entirely server-side, with a short-lived signed session cookie.
No password is collected or stored.

**Why:** The mission requires one recommendation, not a menu. Magic
link avoids password storage/rotation risk entirely, requires no
third-party OAuth app review to ship the walking skeleton, and is
sufficient to prove real, persistent, Author-scoped project ownership -
the actual requirement of the walking skeleton (Section 9). Google or
Microsoft OIDC sign-in is a reasonable near-future addition once there
is a real domain and consent-screen review, but is not required to prove
the foundation.

**What is deferred:** social/OIDC sign-in providers, "Sign in with
ChatGPT" (revisit if and when OpenAI documents general-purpose
subscription or identity delegation for third-party apps), multi-factor
authentication, account recovery flows beyond re-requesting a magic
link, and org/team membership.

## 5. OpenAI Execution Decision

**Current official-documentation finding (OpenAI, retrieved
2026-08-10):** Official guidance (`developers.openai.com/api/docs/guides/production-best-practices`,
`help.openai.com` "Best Practices for API Key Safety") states that API
keys must be routed through the developer's own backend and kept out of
browser/client code entirely; exposing a key client-side lets any user
make requests - and incur cost - on the application's account. The same
guidance recommends separate API "projects" for staging and production
with independent rate/spend limits, environment-variable or
secret-manager storage (never hardcoded/committed), enabled usage
tracking, and configurable spend alerts and hard spend limits.

**Decision:** All OpenAI calls happen server-side only, under the
application's own OpenAI API account (never the Author's ChatGPT
subscription, per Section 4), using separate OpenAI "projects" for
development and production with independent spend limits and alerts.
The API key is read from the platform's secret-management mechanism at
runtime and is never present in frontend code, browser network
responses, or version control.

**Why:** Directly required by official OpenAI guidance and by this
document's own security minimum (Section 11). Project-scoped
development/production separation lets the walking skeleton exercise a
real OpenAI request without risking uncontrolled spend against a shared
key.

**What is deferred:** production per-Author usage metering and billing
model, prompt-cost optimization, model-selection policy beyond "use a
capable general-purpose model for Editorial Direction," retry/backoff
policy detail, and whether web-search-grounding for source verification
uses OpenAI's own web-enabled tool calling or a separate fetch step -
resolve this as an implementation detail in the walking skeleton, not
here. Image generation (Hero Visual) is explicitly out of scope for
slice 1 (Section 9); its execution model is addressed only at the
pipeline-ownership level in Section 8.

## 6. Minimal Data Model

Relational, minimal, and intentionally incomplete. Every entity below
is required for the walking skeleton or is a near-term, low-risk
extension point; no field is spent modeling capabilities this document
defers.

```text
Author
  id (uuid, pk)
  email (unique)
  created_at

EditorialProject
  id (text, pk)                 -- reuse the REP-[A-F0-9]{8} shape
                                    from studio/portable_editorial_project.py
  author_id (fk -> Author)
  state (enum: draft_intake | direction_pending |
               direction_approved)   -- slice-1 states only; see Section 9
  created_at
  updated_at

Source
  id (uuid, pk)
  editorial_project_id (fk -> EditorialProject)
  kind (enum: url | pasted_text | document)   -- subset of studio InputKind
  raw_reference (text)           -- the URL or a pointer to stored text
  retrieved_summary (text, nullable)
  created_at

EditorialDirection
  id (uuid, pk)
  editorial_project_id (fk -> EditorialProject, 1:1 for slice 1)
  primary_angle (text)
  supporting_lenses (jsonb, 0-2 items)
  audience (text, nullable)
  publication_language (text, default 'en-US')
  status (enum: proposed | approved | rejected)
  decided_at (nullable)

EditorialPlan
  id (uuid, pk)
  editorial_project_id (fk -> EditorialProject)
  headline, hook, key_insights (jsonb), practical_takeaway, cta_direction
  status (enum: proposed | approved | rejected)
```

`EditorialPlan` is included in the schema now (per the mission's list)
but is not written to by the walking skeleton, which stops at
`EditorialDirection` approval (Section 9). Its presence lets the very
next delivery add the plan step without a schema migration that touches
already-shipped tables.

**Extension path (not built now, not blocked by this shape):**

- `Article` - belongs to `EditorialProject`, one approved draft, mirrors
  `studio/article_engine.ArticleDraft` fields.
- `Evidence` / `Source` extension - `Source` already supports multiple
  rows per project; evidence/citation detail can be added as columns or
  a child table without changing the shape above.
- `HeroVisual` - belongs to `EditorialProject`, stores the provider
  result reference and validated final dimensions (Section 8), mirrors
  `studio/hero_visual.HeroVisualResult`.
- `Publication` - belongs to `EditorialProject`, records publication
  metadata (destination, published_at, external reference). Its
  existence is what lets `EditorialProject.state` reach a "published"
  value **without deleting or archiving the project row** - required by
  Capability 013.
- `ReaderEngagement` - belongs to `EditorialProject` (not to
  `Publication`), so engagement can exist whenever a project has been
  published, consistent with Capability 013's Create -> Publish ->
  Engage lifecycle. Not created by this document.

**Reader Engagement is not blocked by this model:** publication is
represented as a state value and a related `Publication` row, not as
project deletion, archival, or termination. `EditorialProject` remains
the single durable anchor an Author returns to after publication,
exactly as Capability 013 requires.

## 7. LinkedIn Feasibility

Current official-documentation findings (Microsoft Learn / LinkedIn
official developer documentation, retrieved 2026-08-10:
`learn.microsoft.com/en-us/linkedin/shared/authentication/getting-access`,
`.../shared/authentication/authentication`,
`.../marketing/community-management/shares/images-api`,
`.../marketing/community-management/shares/comments-api`):

| Capability | Status | Detail |
|---|---|---|
| OAuth model | Feasible now | OAuth 2.0; 3-legged (member authorization code flow) for acting on a member's behalf, 2-legged (client credentials) for application-only access. |
| Publish on behalf of a member | **Feasible now** | `w_member_social` scope ("Share on LinkedIn" product) is an **Open Permission** - self-service via the Developer Portal, no special LinkedIn approval required. Explicitly documented as "Post, comment and like posts on behalf of an authenticated member." |
| Image upload for a post | **Feasible now** | Images API `initializeUpload` action works under the same self-serve `w_member_social` permission - no additional product/approval needed. |
| Comment retrieval / reply (Reader Engagement) | **Approval-dependent, currently closed** | `r_member_social` (Social Actions / Comments API - read/write comments on shares) is explicitly documented as a closed permission: "access requests are not being accepted at this time due to resource constraints." This directly blocks automated Reader Engagement comment ingestion for the foreseeable future; Capability 013's manual, Author-supplied comment path remains the only viable near-term approach. |
| Marketing / Advertising, Sales Navigator (SNAP), Talent APIs | Approval-dependent | Manual partner approval; independent research (non-primary sources) reports typical timelines of 4 weeks (fast) to 3-4 months (average), occasionally 6+ months; SNAP is reported as not accepting new partner applications as of 2026. Not required for the walking skeleton or for publish-on-behalf-of-member. |

**Product principle (unchanged, restated):** the Author's LinkedIn
password is never collected or stored. Every future LinkedIn
integration uses OAuth 2.0 member authorization and explicit Author
consent, matching the pattern already established for OpenAI secret
handling (Section 5, Section 11).

**Conclusion for this delivery:** publishing an approved article and
Hero Visual to LinkedIn on the Author's behalf is technically feasible
without special approval, and is a reasonable near-future delivery.
Reading or ingesting reader comments programmatically is not currently
available and should not be designed against until LinkedIn's Comments
API access reopens or an alternative is confirmed; this is recorded as
`Unknown/requires later spike` and must not be assumed in any Reader
Engagement implementation plan.

## 8. Hero Visual Pipeline

**Decision:** The AI image model generates source artwork only. The web
application owns all final image processing and is solely responsible
for guaranteeing the final deliverable: 720 x 425 pixels, landscape,
144:85 aspect ratio. This mirrors `studio/hero_visual.py`'s existing
`HeroVisualProvider` Protocol and its `HERO_VISUAL_WIDTH`/`HERO_VISUAL_HEIGHT`
constants and validation function - the same pattern, with a real
provider behind the interface instead of the deterministic one.

**Thinnest implementation path:** request source artwork from the image
model at or above the target resolution and aspect ratio; deterministically
crop/resize server-side to exactly 720 x 425 (a fixed, testable image
operation, not a model responsibility); validate the resulting file's
exact dimensions and format before it is ever shown to the Author or
attached to a `Publication`; if the model cannot produce usable source
artwork, fail closed with the same three choices already validated in
the locked GPT (Retry / Revise direction / Skip) rather than silently
serving an incorrectly sized image.

**Why:** Real use of the locked GPT (PV-025, DEC-024) proved that
disclosure and best-effort composition are not sufficient once an exact
LinkedIn dimension is promised - the web product removes that gap
entirely by owning the deterministic step the chat-only GPT surface
could not perform.

**What is deferred:** actual OpenAI image-generation model selection and
prompt design, image-storage/CDN choice, and the full Hero Visual UI.
None of this is required to prove the foundation.

## 9. First Walking Skeleton

**WEB WALKING SKELETON 01** - the exact, sharply bounded scope for the
next Engineering Delivery.

Required journey:

```text
Sign In -> Create Editorial Project -> Paste URL ->
application retrieves/processes the source -> real OpenAI call returns
consolidated Editorial Direction -> browser presents real Approve /
Reject controls -> the Author's decision persists as durable project
state (Approve advances the workflow; Reject remains stage-local)
```

**Acceptance criteria:**

- an Author can open the development site in a browser;
- an Author can authenticate (Section 4: email magic link);
- an Author can create an `EditorialProject`;
- the project receives a persistent `REP-`-shaped ID (Section 6);
- an Author can paste a URL as the project's `Source`;
- the application stores the `Source` reference;
- the backend makes one real, server-side OpenAI request (Section 5) -
  no mock/fake AI path is an acceptable final acceptance condition;
- the request returns a consolidated `EditorialDirection` (one primary
  angle, zero to two supporting lenses, no separate
  angle/outcome/audience questionnaire - carrying forward the validated
  GPT UX lesson, per Section 12's Web UX Principles);
- the browser presents real native **Approve** and **Reject** buttons -
  no typed numeric commands, no magic words;
- both Approve and Reject are durable project-state decisions, per
  DEC-029: Approve persists `EditorialDirection.status`, persists
  decision metadata, and advances `EditorialProject.state`; Reject
  persists `EditorialDirection.status`, persists Author feedback when
  supplied, persists decision metadata, and remains at the current
  workflow stage (**stage-local**, not client-local, ephemeral, or
  non-persistent) while preserving the `Source` and the project;
- a page refresh does not lose project state, for either an approved or
  a rejected Editorial Direction (real persistence, not client-only
  state);
- a project is visible only to its owning Author (`author_id` scoping
  enforced server-side);
- the application is deployable to a development environment (Section
  3).

**Explicitly not built in this slice** (unless already a trivial
extension of code the slice already needs): Editorial Plan, article
drafting, Editorial Audit, Hero Visual, LinkedIn publication, Reader
Engagement. The goal is to prove the foundation, not the full journey.

## Web UX Principles (carried forward from the locked GPT)

- real Approve / Reject buttons, not typed numbers or magic words;
- multi-select controls where the product needs them (e.g. future
  supporting-lens adjustment);
- never re-request information already supplied in the current project;
- the current state and the next action are always visually clear;
- project context persists across page loads because the application
  owns it - not because a conversation happens to still be open.

## 10. Deferred Scope

Explicitly out of scope for this document and for the walking skeleton
it authorizes:

- full article-generation flow and Editorial Audit implementation;
- Hero Visual generation UI and the final 720 x 425 pipeline
  implementation (Section 8 defines the approach only);
- LinkedIn publishing implementation (Section 7 establishes feasibility
  only);
- Reader Engagement implementation, automatic LinkedIn comment
  ingestion, and response publishing;
- subscriptions/billing, usage plans, teams/organizations, analytics,
  scheduling, mobile application, and public production launch.

These may follow once the walking skeleton proves the foundation.

## 11. Risks / External Dependencies / Security Minimum

**External dependencies:**

- OpenAI API availability, pricing, and rate limits (application-billed,
  per Section 5);
- LinkedIn's Comments API access remaining closed indefinitely (Section
  7) - Reader Engagement automation has no committed timeline;
- LinkedIn's self-serve `w_member_social`/Images API scope or approval
  model changing without notice - re-verify official documentation
  immediately before implementing LinkedIn publishing, not from this
  document's 2026-08-10 snapshot.

**Security minimum for this delivery:**

- OpenAI secrets remain server-side only (Section 5);
- OAuth tokens (LinkedIn, future providers) remain server-side only;
- no LinkedIn password, and no ChatGPT password, is ever collected or
  stored;
- project access is scoped to the authenticated, owning Author
  (Section 9 acceptance criterion);
- production secrets are never committed to the repository;
- development and production environments, and their secrets, are
  separated (Section 3, Section 5);
- sensitive tokens are stored using the deployment platform's supported
  secret mechanism (e.g. platform-managed environment secrets), not
  plaintext configuration files.

No compliance program, threat model, or penetration-test plan is
authorized or required by this document.

## 12. Next Engineering Delivery

**WEB WALKING SKELETON 01**, as fully specified in Section 9, is
build-ready. The next Engineering Delivery may begin implementation
directly against Section 3 (stack), Section 4 (authentication), Section
5 (OpenAI execution), Section 6 (data model), and Section 9 (acceptance
criteria) without another architecture discussion. Section 7 and Section
8 govern LinkedIn publishing and the Hero Visual pipeline respectively
and apply only once those capabilities are explicitly authorized in a
future delivery, not as part of Walking Skeleton 01.

## 13. Walking Skeleton 01 - Implementation Status

Recorded as of 2026-08-10, after PR #111 (merged commit `08cb986`)
delivered `web/client` and `web/server` against Section 9's acceptance
criteria. This section reports outcome only; it does not reopen or
restate the foundation decisions above.

**DECIDED and IMPLEMENTED:** the Section 3 stack (React 18 + Vite,
Express 4/TypeScript, PostgreSQL, npm workspaces); the Section 4
authentication decision (single-use SHA-256-hashed magic-link token,
15-minute TTL, Postgres-backed sessions, pluggable `EmailProvider` with
`ConsoleEmailProvider` for development and `SmtpEmailProvider`/nodemailer
for production-compatible delivery); the Section 5 OpenAI execution
decision (server-side only, `openai` SDK, Structured Outputs against a
strict JSON schema, zod validation, bounded retry, no client-side key
exposure); the Section 6 data model's `Author`, `EditorialProject`
(`REP-XXXXXXXX` IDs), `Source`, and `EditorialDirection` entities
(`EditorialPlan` remains schema-only, not written to); Section 9's SSRF
protections (scheme allowlist, DNS/IP-range blocking, timeout, source-size
cap) and Author-scoping enforcement.

**VERIFIED:** web automated tests, `npm install`, typecheck, lint,
production build, `npm audit` (0 vulnerabilities); existing Python
validation remains green (484 tests, `studio.py validate`, `git diff
--check`); real-stack HTTP/API-level behavior against a real PostgreSQL,
Express, and Vite dev server - magic-link flow, project creation and
rehydration, public-URL retrieval, SSRF/invalid-URL rejection,
cross-Author isolation, sign-out revocation.

**VERIFIED (2026-08-10, real-OpenAI-foundation verification):**

- **Real OpenAI Editorial Direction generation** - `OPENAI_API_KEY` was
  configured locally by the Repository Author directly into the existing
  gitignored `web/server/.env` mechanism (never pasted into or handled by
  an AI participant). Two real, non-mocked, end-to-end requests were
  executed through the actual application path (`POST
  /api/projects/:id/source`) against real public URLs (RFC 2119, RFC
  8174): real server-side source retrieval, a real `gpt-4o-mini` chat
  completion using Structured Outputs, strict JSON-schema validation, and
  persistence of the resulting `EditorialDirection` - `source_understanding`,
  `audience`, `objective`, `publication_language`, `primary_angle`, zero
  and two `supporting_lenses` (both cases exercised), and
  `editorial_thesis` were all present, schema-valid, and accurately
  reflected the real retrieved source text. Both were approved through the
  real Approve path, persisted, and confirmed present after a simulated
  refresh (re-`GET` of the project). The configured model
  (`gpt-4o-mini`) was confirmed available to the configured key via
  `models.retrieve` before use; no model substitution was required.
- Non-secret OpenAI usage metadata (model, request id, prompt/completion/
  total token counts, timestamp) is now logged server-side on every
  completed request, for future cost-per-Editorial-Project measurement.
  No prompt or source text is logged.
- Missing- and invalid-API-key error handling verified safely: an unset
  key produces the exact application guard error before any network call;
  an invalid key is rejected by the OpenAI API with `401` before any
  usage is billed. Neither path exposes the key or internal detail to the
  browser.

**RECONCILED (2026-08-11, DEC-029):** an independent Codex review of Web
Walking Skeleton 01 found that this section's acceptance criteria and
required-journey diagram stated persistence explicitly for Approve only,
while the implemented Reject endpoint already persisted rejected status,
Author feedback, and decision time. The Repository Author confirmed the
implementation, not the acceptance criteria, was correct: both Approve
and Reject are durable project-state decisions (DEC-029). Section 9 above
is corrected to state this explicitly. No application code changed;
`web/server/tests/projects.test.ts` was extended to assert the decision
timestamp and stage non-advancement that the implementation already
provided.

**FIXED (2026-08-11, DEC-029):** a follow-up Codex review of the same PR
found that, unlike Reject, Approve did not yet advance
`EditorialProject.stage` - it persisted only `EditorialDirection.status`
and `decided_at`. `web/server/src/projects/repository.ts`'s
`approveDirection` now updates both the Editorial Direction and the
project's stage (to the already-named `editorial_plan` stage) in one
transaction, so an Editorial Direction can never be left approved without
the project advancing. Migration `002_add_editorial_plan_stage.sql` adds
`editorial_plan` to the project stage constraint. Editorial Plan
generation itself remains out of scope.

**VERIFIED (2026-08-11, Render hosted development deployment and literal
browser acceptance):** Web Walking Skeleton 01 is deployed to Render -
one free-tier PostgreSQL database and one free-tier Node web service
(`ramrattan-studio`), the Express server also serving the built React
SPA from the same origin (`docs`/`web/README.md`'s "Hosted development
deployment (Render)" section has the full topology). Hosted URLs:
`https://ramrattan-studio.onrender.com` (Render-native) and the custom
domain `https://studio.ramrattan.com` (DNS via Hostinger, TLS
provisioned automatically by Render after verification). The Repository
Author performed literal browser acceptance directly (this environment
has no browser-automation tool), against both URLs, and confirmed:

- sign-in via email magic link, `EMAIL_PROVIDER=console` (the link is
  read from Render's authenticated Logs tab, not emailed - see "Hosted
  authentication" below);
- Editorial Project creation with a persistent `REP-`-shaped id;
- a real public article URL submitted, retrieved, and processed;
- a real, non-mocked OpenAI Editorial Direction generated and displayed;
- native Approve/Reject controls; Approve persisted and advanced the
  project to the `editorial_plan` stage;
- state survived a page refresh;
- sign-out revoked access, and a **second, independent sign-in** (a
  fresh magic link, a new session) recovered the **same** project at its
  persisted `editorial_plan` stage - proving persistence is real
  database state, not session- or client-local;
- on the custom domain specifically: a magic link requested from
  `https://studio.ramrattan.com` correctly resolved to
  `https://studio.ramrattan.com/auth/callback?...` (not the Render-native
  hostname), confirming `CLIENT_ORIGIN` is wired correctly end to end.

No token, credential, or magic-link value is recorded here or anywhere
in the repository; the evidence above is the outcome, not the secret.

**Hosted authentication.** `EMAIL_PROVIDER=console` remains the hosted
development mechanism: the magic link is written to the service's
stdout, visible only to the Repository Author via Render's authenticated
Logs tab. Real outbound email delivery (SMTP) remains not yet configured
and was not required for the acceptance above; `SmtpEmailProvider`
already exists and is production-capable if needed later.

**DEFERRED** (unchanged from Section 9 and Section 10): Editorial Plan,
article drafting, Editorial Audit, Hero Visual, LinkedIn publishing, Reader
Engagement, and all billing/org/analytics scope.

**External-dependency plan status:** ~~(1) configure `OPENAI_API_KEY`~~ -
done; ~~(2) execute and verify a real OpenAI Editorial Direction
request~~ - done; ~~(3) validate in a real browser~~ - done; ~~(4)
configure a development deployment~~ - done (Render); ~~(5) obtain a
hosted development URL~~ - done (`studio.ramrattan.com`); (6) continue
`ConsoleEmailProvider` for development and defer real outbound SMTP
delivery until it is genuinely required - **Resend via SMTP** remains a
candidate production provider, not yet implemented or selected.

Full status detail and sequencing are also recorded in `ROADMAP.md`
("Version 2 Checkpoint" section), which is authoritative for current
program status; this section exists so the foundation document is not
read as still purely prospective.

## Non-Goals

This document does not:

- modify or unlock `GPT Recovery RC5 - Locked Private GPT Baseline`;
- authorize LinkedIn integration, automatic replies, or Reader
  Engagement implementation;
- authorize production authentication or production OpenAI integration
  code (Section 9's walking skeleton is the first real implementation,
  authorized separately by the next Engineering Delivery, not by this
  document);
- define commercial pricing, billing, or usage-plan design;
- create a compliance program, a multi-year roadmap, or a service
  decomposition beyond the single application server described in
  Section 3.

## Open Questions

- Exact frontend component approach (Section 3) - resolved at
  implementation time.
- Whether server-side web-search grounding for source verification uses
  OpenAI's own tool-calling or an independent fetch step (Section 5) -
  resolved at implementation time.
- LinkedIn Comments API reopening timeline (Section 7) - unknown;
  monitor official documentation before any Reader Engagement
  implementation attempt.
- Whether `EditorialProject.state` should be a single enum column or a
  richer state/substate pair as more stages are added after Walking
  Skeleton 01 - revisit once Editorial Plan is implemented.

## Sources Consulted (retrieved 2026-08-10)

- OpenAI, "Production best practices,"
  `developers.openai.com/api/docs/guides/production-best-practices`
- OpenAI Help Center, "Best Practices for API Key Safety,"
  `help.openai.com/en/articles/5112595-best-practices-for-api-key-safety`
- OpenAI Developer Community, "'Login With ChatGPT' | Allow users to use
  their own Plus subscription in 3rd party apps,"
  `community.openai.com/t/login-with-chatgpt-allow-users-to-use-their-own-plus-subscription-in-3rd-party-apps/1378506`
  (feature request; no confirmed official resolution)
- `developers.openai.com/api/docs/guides/sign-in-with-chatgpt` (returned
  HTTP 404 at time of retrieval)
- Microsoft Learn / LinkedIn, "Getting Access to LinkedIn APIs,"
  `learn.microsoft.com/en-us/linkedin/shared/authentication/getting-access`
- Microsoft Learn / LinkedIn, "Authenticating with OAuth 2.0 Overview,"
  `learn.microsoft.com/en-us/linkedin/shared/authentication/authentication`
- Microsoft Learn / LinkedIn, "Images API,"
  `learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/images-api`
- Microsoft Learn / LinkedIn, "Comments API,"
  `learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/comments-api`
