# Web Walking Skeleton 02 Scope - Editorial Plan + Draft

**Status:** Scoped - approved slice definition and acceptance contract; implementation not authorized.
**Classification:** Product scope and acceptance-contract artifact (Informative - not a Product Decision).
**Backlog:** BL-003.
**Evidence base:** `ROADMAP.md` "Version 2 Checkpoint" (Next Vertical Slice); `docs/product/version2/Web_Product_Foundation_v1.md` Sections 6, 9-10; `docs/architecture/Version_1_1_State_Machine.md` (Editorial Plan, Generation); `docs/product/Version_1_1_Author_Experience_Baseline.md` (Editorial Plan); `studio/article_engine.py` (`ArticleDraft`).

## 1. Objective and User-Visible Outcome

An Author who has an approved Editorial Direction can advance the same Editorial Project through a proposed Editorial Plan (Headline, Hook, Key Insights, Practical Takeaway, Call to Action) to a generated Draft article, entirely through the real Web Product - persisted, refresh-safe, and Author-scoped, matching the reliability already proven by Web Walking Skeleton 01 for Editorial Direction.

This is the same `Approved Editorial Direction -> Editorial Plan -> Approve/Reject -> Draft generation -> persistent article workspace` outcome named in `ROADMAP.md`, now given an exact, testable boundary.

## 2. Starting Project State

An authenticated Author's `EditorialProject` at `stage = 'editorial_plan'` (already reachable today - `Approve` on an `EditorialDirection` advances to this stage per DEC-029/migration `002_add_editorial_plan_stage.sql`), with no `EditorialPlan` or `Article` row yet.

## 3. Ending Project State

The same `EditorialProject` at a new terminal stage for this slice - `stage = 'draft'` - with exactly one approved `EditorialPlan` row and exactly one `Article` (Draft) row, both persisted and retrievable through `GET /:id`.

## 4. Editorial Plan Capability (Minimum)

- **Fields**, per `Web_Product_Foundation_v1.md` Section 6's already-sketched `EditorialPlan` shape: `headline`, `hook`, `key_insights` (jsonb array), `practical_takeaway`, `cta_direction`.
- **Generation trigger**: proposed automatically as part of the same request that approves the `EditorialDirection` - the existing `POST /:id/direction/approve` endpoint is extended to synchronously generate and persist the initial `EditorialPlan` proposal in the same transaction as the stage advance. This mirrors the existing precedent already established by `POST /:id/source` (source retrieval and Editorial Direction generation happen synchronously in one request) rather than introducing a new asynchronous or two-step pattern. See Section 11 for the one point this needs explicit confirmation on.
- **Author decision**: exactly two outcomes, per the State Machine (not the three-outcome `proposed | approved | rejected` pattern `EditorialDirection` uses):
  - **Approve** - advances the project to `stage = 'draft'` and triggers Draft generation (Section 5).
  - **Request revision** - regenerates a new plan proposal and the project remains at `stage = 'editorial_plan'`. This is a real behavioral difference from `EditorialDirection`'s Reject (which is terminal and stage-local, never regenerates) - see Section 11.
- **No independent Approve/Reject exists for the Draft itself** in this slice - `ROADMAP.md`'s wording places `Approve/Reject` between Editorial Plan and Draft generation, not after it, matching the State Machine's Generation stage being automatic, not an Author decision point.

## 5. Draft Capability (Minimum)

A new `Article` entity, deliberately narrower than the full `studio/article_engine.ArticleDraft` it is modeled on, to keep this the smallest coherent slice:

**Included** (the article's own content, generated once from the approved plan):
- `headline`, `hook`, `key_insights`, `practical_takeaway`, `cta` (carried forward from the approved `EditorialPlan`)
- `article_markdown` - the generated article body
- `source_attributions` - grounding back to the project's `Source`, consistent with `Evidence Before Generation`

**Explicitly excluded from this slice** (see Section 9): `hashtags`, `linkedin_description` (LinkedIn-publication-specific formatting; belongs with the deferred LinkedIn slices), `hero_visual_prompt` and any Hero Visual artifact (its own deferred slice), and the full LMHS Editorial Risk / Evidence Validation blocking machinery (`used_claim_identifiers` and the "High or Severe Editorial Risk block" outcome) - see Section 11.

- **Generation trigger**: automatic, synchronous, immediately on Editorial Plan approval (`Generate Once`) - one request produces both the stage advance and the persisted `Article` row, mirroring the same synchronous-generation precedent as Section 4.
- **Outcomes**: **complete** (persists the `Article`, advances to `stage = 'draft'`) or **technical failure** (does not persist an `Article`, project remains at `stage = 'editorial_plan'` with an explanation, mirroring `EditorialDirection`'s existing bounded-retry-then-fail pattern in `web/server/src/openai/editorialDirection.ts`). The risk-based "block" outcome is out of scope per Section 9/11.

## 6. Persistence and Refresh/Rehydration

Both `EditorialPlan` and `Article` must persist through the existing repository/migration pattern (`web/server/src/db/migrations/`, `web/server/src/projects/repository.ts`) and rehydrate through the existing `ProjectView` aggregation (`GET /:id`) on refresh or a fresh sign-in, exactly as `EditorialDirection` already does. No new persistence mechanism is introduced.

## 7. Stage-Gate Behavior

- Editorial Plan: Approve / Request Revision, as defined in Section 4 - this is the one Approve/Reject-equivalent decision point in this slice.
- Draft: no independent Author gate in this slice (Section 4's last point).
- Existing `EditorialDirection` Approve/Reject behavior is unchanged and must not regress.

## 8. Authentication and Author Isolation

Inherited as-is from Web Walking Skeleton 01: session-based auth, `authorId` scoping on every repository call, no new authentication surface. Not re-verified in depth by this slice unless a regression is found - already proven by Walking Skeleton 01 and DS-01/BL-001's hosted acceptance.

## 9. Explicitly Deferred

Per `ROADMAP.md`'s "Later Web Slices" and this document's own narrowing above:

- Editorial Audit
- Author editing workspace (DEC-013 resolution)
- Hero Visual generation
- Full Publication Package assembly (hashtags, LinkedIn description, source-attribution formatting beyond the Draft's own grounding)
- LinkedIn OAuth and Author-approved LinkedIn publishing
- Published Editorial Project state
- Reader Engagement
- LMHS Editorial Risk / Evidence Validation blocking (Generation's "High or Severe Editorial Risk" block outcome) - this slice implements only the technical-failure outcome, not the risk-block outcome

## 10. Dependencies Already Satisfied

- `stage = 'editorial_plan'` is already a valid, reachable `EditorialProject` stage (migration `002_add_editorial_plan_stage.sql`).
- The `EditorialPlan` entity shape was already sketched, not built, in `Web_Product_Foundation_v1.md` Section 6, specifically to let this next delivery add it without a migration touching already-shipped tables.
- The synchronous generate-on-request pattern, bounded-retry OpenAI integration, Structured Outputs/zod validation, and malformed-output-never-persisted contract all already exist (`web/server/src/openai/`) and are reused, not redesigned.
- Editorial quality/model configuration is governed by DEC-030 (`gpt-5.6-terra`, Variant D-equivalent instruction quality bar) - this slice must follow the same instruction-quality discipline for its own prompts, not introduce a separate, unreviewed prompting approach.

## 11. Unresolved Repository Author Decisions

Two points genuinely require confirmation before implementation, not invented here:

1. **Synchronous vs. explicit-trigger generation.** Section 4/5 recommends synchronous generation (Plan on Direction-approve; Draft on Plan-approve), matching the existing `POST /:id/source` precedent. An explicit separate "generate" endpoint per stage is the alternative. Recommendation: synchronous, for consistency; needs confirmation, not assumed.
2. **Editorial Plan revision semantics.** Section 4 notes Editorial Plan's "Request revision" regenerates a new proposal, unlike `EditorialDirection`'s terminal Reject. Confirm whether `EditorialPlan.status` should reuse the same `proposed | approved | rejected` enum with `rejected` behaviorally meaning "regenerate," or use a distinct status vocabulary to avoid conflating two different behaviors under the same word Walking Skeleton 01 already uses for something else.

Both are product/architecture judgment calls, not technical blockers - each is answerable in one Repository Author decision before implementation begins.

## 12. Acceptance Criteria

Verifiable through the real Web Product, following the same real-application-path standard DEC-030/BL-001 used:

1. Starting from an authenticated, persisted `EditorialProject` at `stage = 'editorial_plan'`.
2. An `EditorialPlan` proposal (Headline, Hook, Key Insights, Practical Takeaway, Call to Action) is generated and rendered through the real application path - not mocked.
3. `EditorialPlan` data persists and rehydrates correctly after a browser refresh.
4. Approving the plan advances the project to `stage = 'draft'`; requesting revision regenerates a new proposal and the project remains at `stage = 'editorial_plan'`.
5. On plan approval, a real `Article` (Draft) is generated and rendered through the real application path.
6. `Article` data persists and rehydrates correctly after a browser refresh.
7. Existing authentication and Author isolation remain intact (no cross-Author access to another Author's Plan/Draft).
8. Existing, already-verified Walking Skeleton 01 behavior (Source intake, Editorial Direction generation, Approve/Reject) is not regressed.

## 13. Engineering Work Order (Prepared, Not Executed)

Prepared per `docs/engineering/AI_Engineering_Work_Order_Template.md`'s canonical template, for a future authorized delivery. **Not executed by this document.**

```text
# Engineering Work Order

## 1. Work Order Title
Web Walking Skeleton 02 - Editorial Plan + Draft Implementation

## 2. Role
Lead Implementation Engineer, per the AI Engineering Standard.

## 3. Authority and Approval Profile
Start, scoped to: branch creation/resumption, implementation, testing,
validation, complete diff review, and staging of the exact reviewed
scope. Publish (commit/push/PR) requires separate, explicit
authorization at that boundary, per AGENTS.md.

## 4. Objective
Implement the Editorial Plan and Draft slice defined in
docs/product/version2/Web_Walking_Skeleton_02_Scope.md Sections 1-12,
so an Author can advance an approved Editorial Direction through a
proposed Editorial Plan to a generated Draft, entirely through the
real Web Product, persisted and refresh-safe.

## 5. Verified Repository State
[To be re-verified at the start of that delivery - do not reuse this
document's verification as current. At minimum confirm: current
branch is develop; local develop matches origin/develop; no primary
Kanban item is In Progress other than BL-003; this scope document and
its two Repository Author decisions (Section 11) are still current.]

## 6. Governing Inputs
- docs/product/version2/Web_Walking_Skeleton_02_Scope.md (this document)
- docs/product/version2/Web_Product_Foundation_v1.md (Sections 6, 9-10)
- docs/architecture/Version_1_1_State_Machine.md (Editorial Plan, Generation)
- docs/product/Version_1_1_Author_Experience_Baseline.md (Editorial Plan)
- studio/article_engine.py (ArticleDraft - field-shape reference only)
- product/validation/Product_Decisions.md DEC-030 (instruction-quality bar)
- web/server/src/openai/editorialDirection.ts, client.ts (pattern to extend, not redesign)
- web/server/src/projects/routes.ts, repository.ts (REST/persistence pattern to extend)
- web/server/src/db/migrations/ (migration sequence to extend)

## 7. Repository Author Decisions
Section 11's two decisions (synchronous generation; Editorial Plan
revision semantics) must be resolved before this work order is
executed - they are not resolved by this scope document.

## 8. Exact Scope
- New migration: web/server/src/db/migrations/003_add_editorial_plan_and_article.sql
- web/server/src/types.ts (extend ProjectStage, add EditorialPlan/Article types)
- web/server/src/projects/repository.ts (persistence for EditorialPlan, Article)
- web/server/src/projects/routes.ts (extend direction/approve; add plan approve/revise)
- web/server/src/openai/ (new editorialPlan.ts, articleDraft.ts generation modules,
  following the existing editorialDirection.ts pattern - System prompt quality
  bar per DEC-030)
- web/server/tests/ (regression coverage for the above, following existing test patterns)
- web/client/src/components/ (new EditorialPlanCard.tsx, ArticleDraftCard.tsx,
  following EditorialDirectionCard.tsx's pattern)
- web/client/src/pages/Project.tsx (render the new stages)

## 9. Explicit Non-Goals
Everything in this scope document's Section 9 (Editorial Audit, Author
editing workspace, Hero Visual, Publication Package assembly, LinkedIn
OAuth/publishing, Published state, Reader Engagement, LMHS risk
blocking). Also: no change to Editorial Direction behavior beyond the
one extension named in Section 8; no Render/infrastructure change; no
new authentication surface.

## 10. Constraints and Protected Areas
Existing editorial_projects, sources, editorial_directions tables and
their current columns are additive-only (new migration, no destructive
change). DEC-030's approved model/instruction-quality bar governs any
new OpenAI prompt. The locked GPT and GPT Knowledge are unchanged.

## 11. Required Deliverables
Migration 003; extended types/repository/routes; two new OpenAI
generation modules; client components rendering both new stages;
passing regression tests; this scope document's twelve Acceptance
Criteria demonstrated through the real application path (local, then
one bounded hosted verification, mirroring DEC-030's delivery
standard).

## 12. Implementation or Documentation Requirements
Follow existing code patterns exactly (synchronous generation,
Structured Outputs + zod validation, malformed-output-never-persisted,
bounded retry) rather than introducing new architectural patterns.
Reuse the existing ProjectView aggregation pattern for rehydration.

## 13. Validation Requirements
npm run typecheck / lint / test / build (web/), against the exact
final diff. Python baseline (compileall, unittest, studio.py validate,
git diff --check) if any file under repository root is touched.
Acceptance Criteria 1-8 (Section 12 of the scope document) verified
through the real application path.

## 14. Repository Actions Authorized
[Set at the time this work order is actually issued - not
pre-authorized by this scope document.]

## 15. Repository Actions Prohibited
Merge to main, tag/release creation, Render modification, and
everything in Section 9 of this scope document.

## 16. Failure and Stop Conditions
Any ambiguity about Section 11's two decisions, any conflict with
DEC-030's instruction-quality bar, or any required schema change
beyond the additive migration in Section 8: stop and report, do not
infer.

## 17. Required Final Report
What changed (exact files), validation results (all four suites),
Acceptance Criteria 1-8 status individually, real application-path
verification evidence, and the next approval boundary.

## 18. Next Approval Boundary
Implementation and local verification only, under Start. Publish
(stage/commit/push/PR) requires separate explicit authorization, per
AGENTS.md, exactly as DEC-030's implementation delivery was gated.
```
