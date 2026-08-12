# Backlog and Kanban

**Status:** Active
**Authority:** Canonical operational source for backlog items, priority,
Kanban state, and current sprint status.

## Authority and Scope

This file is the **single canonical view of current backlog and delivery
state**. It does not compete with, and should not be duplicated by,
other governing documents:

| Document | Owns |
|---|---|
| **This file** | Backlog items, priority, Kanban state, current sprint status |
| `ROADMAP.md` | Milestones, strategic sequence, material priority changes |
| `HANDOFF.md` | Meaningful stopping state, environment/deployment context, session handoff |
| `docs/learning/` | Durable, reusable engineering lessons |
| `product/validation/Product_Validation_Log.md` / `Product_Decisions.md` | Product evidence and promoted product decisions |
| `docs/engineering/Delivery_Operating_Model.md` | The process this file is operated under (cadence, ceremonies, rules) |

Read [`docs/engineering/Delivery_Operating_Model.md`](docs/engineering/Delivery_Operating_Model.md)
for the full definition of the daily sprint, daily closeout, Kanban
flow, WIP limits, prioritization model, weekly demo, weekly
retrospective, and document synchronization cadence this file operates
under. This file is the *data*; that document is the *process*.

Update this file whenever operational state materially changes -
backlog items added/reprioritized, Kanban state changes, or a sprint is
committed/closed. Do not let a second, parallel list of priorities
accumulate elsewhere (in particular, `HANDOFF.md`'s "Current Priorities"
now points here rather than maintaining its own detailed list).

## Kanban Board

```text
Backlog -> Ready -> In Progress -> Review / Validation -> Done
```

**WIP limits:** In Progress: max 1 primary product delivery. Review /
Validation: max 2 items. The purpose is to finish work before starting
more work.

| Backlog | Ready | In Progress (0/1) | Review / Validation (0/2) | Done |
|---|---|---|---|---|
| BL-004 through BL-010, BL-012 through BL-015 | *(none)* | BL-003 | *(none)* | *(see completed capabilities in ROADMAP.md - this board tracks forward-looking work, not delivery history; BL-002 completed 2026-08-11, see DEC-030; BL-001 completed 2026-08-11, see DEC-030 and PR #130 hosted acceptance; BL-011 completed 2026-08-11, see `v1.1.0` GitHub Release and PR #133)* |

## Current Sprint

| Field | Value |
|---|---|
| Sprint Date / ID | DS-03, 2026-08-11 |
| Outcome | Define the smallest coherent and testable scope for BL-003 - Web Walking Skeleton 02: Editorial Plan + Draft - and prepare it for a later engineering delivery, without beginning implementation. |
| Must Complete | User-visible outcome; exact starting/ending project state; minimum Editorial Plan and Draft capability; persistence/refresh requirements; deferred scope; dependencies already satisfied; any genuine unresolved Repository Author decision; literal, testable Acceptance Criteria; a prepared (not executed) Engineering Work Order. |
| Stretch | None - a scoping sprint; implementation is explicitly out of scope. |
| Acceptance Criteria | A durable scope document exists with all Must-Complete elements; BL-003 is implementation-ready pending the Repository Author's resolution of the two flagged decisions. |
| Dependencies | BL-001/BL-002 (Done, DEC-030) - previously the reason BL-003 was not auto-elevated; now resolved. |
| Risks | None from scoping itself (no implementation, no OpenAI calls); rework risk if implementation began without the Repository Author confirming Section 11's two decisions first - avoided by not implementing. |
| Explicit Non-Goals | Editorial Plan or Draft implementation, any OpenAI call, redesigning Walking Skeleton 01, reopening DS-01/DEC-030, Render changes, BL-005, BL-016, another backlog item. |
| Owner / Execution Agent | Claude |
| Review Agent | None required for this scoping pass - no architecture, security, persistence, or workflow-state risk category applies to a documentation-only scope; the prepared Engineering Work Order itself designates Codex/independent review at the point it is actually executed. |
| Status | Scoping complete - see `docs/product/version2/Web_Walking_Skeleton_02_Scope.md`. Awaiting Repository Author resolution of Section 11's two decisions before an implementation delivery can be authorized. |

## Latest Closeout

**DS-01 - Editorial Direction Quality Investigation vs. Locked GPT Baseline (2026-08-11)**

| Field | Value |
|---|---|
| Committed Outcome | Determine why the Web Product's Editorial Direction was materially weaker editorially than the locked GPT baseline (PV-029), and produce an evidence-backed recommendation for the Web Product's Editorial Direction configuration. |
| Completed | Baseline reconstruction, difference analysis, and a two-pass controlled evaluation (Sections 9, 13-14 of `docs/product/version2/Editorial_Direction_Quality_Investigation.md`); Repository Author approval of `gpt-5.6-terra` and the Variant D instructions as `product/validation/Product_Decisions.md` DEC-030; the bounded implementation delivery DEC-030 authorized, merged as PR #130 (commit `afb07eb`); and post-merge hosted acceptance through `https://studio.ramrattan.com` covering health, authentication, project creation, real public-URL submission, Editorial Direction generation, runtime model evidence, schema rendering, persistence/rehydration, Reject durability, Approve advancement, and authentication protection. |
| Not Completed | Nothing outstanding within DS-01's scope. |
| Blockers | None outstanding.  Two transient local-environment blockers were hit and resolved during implementation verification: a stale local `OPENAI_MODEL=gpt-4o-mini` override in `web/server/.env` masked the new default on the first two verification attempts, and the Repository Author's first hosted-acceptance attempt hit an HTTP 403 during source retrieval on an unrelated URL, resolved by using the same NASA source already verified reachable in DS-01's second evaluation pass. |
| Defects Discovered | One test-only defect: the new `editorialDirection.model.test.ts` mocked the `openai` package with an arrow function passed to `mockImplementation`, which cannot be used as a constructor (`new OpenAI(...)` in `client.ts`).  Fixed to a regular function before the delivery's test suite was reported green; no production code was affected. |
| Product Discoveries | None beyond PV-029 (already recorded) and DEC-030 (already recorded). |
| Lessons Learned | None promoted to `docs/learning/` - the mock-constructor and stale-local-env issues were mechanical, not reusable beyond this instance. |
| Backlog Changes | BL-001 moved Review / Validation -> Done.  BL-002 remains Done (unchanged, resolved earlier in DS-01). |
| Kanban Changes | Review / Validation column returns to empty (0/2).  Done column note updated to record BL-001's completion alongside BL-002's. |
| Repository / Deployment State | `develop` synchronized with `origin/develop` at commit `afb07eb` (PR #130 merged).  Render redeployed the merged commit; hosted runtime `[openai-usage]` evidence confirmed `gpt-5.6-terra` is live, not `gpt-4o-mini`. |
| Recommended Starting Point for Tomorrow | No sprint is currently committed.  The next Daily Start should review `BACKLOG.md`'s Backlog/Ready columns (BL-011 release decision; BL-005 time-bound Render database decision) for the next primary WIP=1 item.  Web Walking Skeleton 02 (BL-003) remains a candidate but is not pre-selected. |

## Priority Model

- **P0** - Active blocker / immediate operational risk.
- **P1** - Critical path / next high-value work.
- **P2** - Important but not immediate.
- **P3** - Later candidate.
- **Parking Lot** - Discovery or idea not yet ready for commitment.

Full model and the scope-change rule (what may enter an active sprint
versus what goes to the backlog) are defined in
`docs/engineering/Delivery_Operating_Model.md`.

## Backlog Items

### BL-011 - Manual Version 1.0 / Version 1.1 release decision

| Field | Value |
|---|---|
| Outcome | Repository Author decision on `develop`-to-`main` promotion, release tag(s), GitHub Release publication, release notes, and external announcement for Version 1.0 and/or Version 1.1. |
| Evidence / Source | `HANDOFF.md` "Current Focus" #1; Issue #18 and the Version 1.1 Engineering Epic (Issue #69) are both functionally complete but not promoted to `main`. |
| Priority | P1 |
| Kanban State | Done - `v1.0.0` was already released (2026-08-03); the Repository Author authorized a pinned Version 1.1 promotion from the verified completion boundary (commit `a00111d`, PR #92) to `main` via PR #133 (merged 2026-08-11), deliberately excluding subsequent Version 2 Web Product work. Tagged `v1.1.0` and published as a GitHub Release ("Ramrattan AI Editorial Studio v1.1.0 - Author Experience"). Issue #69 closed. |
| Dependencies | None technical - pure decision. Independent of the Web Product Track (BL-001 through BL-010). |
| Acceptance Summary | Met. Decision recorded and executed: `v1.1.0` promoted, tagged, and released per the existing release process. External announcement was not part of this decision's scope and remains a separate, not-yet-requested action. |

### BL-001 - Editorial Direction quality parity with the locked GPT baseline

| Field | Value |
|---|---|
| Outcome | Web Editorial Direction output is at least as strong, editorially, as the locked private GPT's (`GPT Recovery RC5`) output for comparable source material. |
| Evidence / Source | Repository Author, real hosted browser acceptance (2026-08-11): the Web Editorial Direction was technically functional (real OpenAI call, schema-valid, persisted, Approve/Reject working) but materially weaker editorially than the locked GPT baseline.  Formalized as `product/validation/Product_Validation_Log.md` PV-029 (observational evidence only, no cause prejudged). |
| Priority | P1 |
| Kanban State | Done (DEC-030 implementation delivered via PR #130, commit `afb07eb`; post-merge hosted acceptance passed 2026-08-11) |
| Dependencies | Closely coupled to BL-002 (model selection, resolved by DEC-030); resolved together. |
| Acceptance Summary | DS-01 (2026-08-11) executed two bounded 4-call evaluation matrices on materially different sources (cybersecurity, then NASA/AI-policy; combined measured cost $0.042630; see `docs/product/version2/Editorial_Direction_Quality_Investigation.md` Sections 13-14).  Both passes showed the same D > C > B > A quality pattern; the model effect (A -> C) repeated strongly, the prompt effect (A -> B) repeated but with variable magnitude, D remained strongest in both, and extraction noise did not visibly degrade either result.  The Repository Author reviewed both passes and approved adopting `gpt-5.6-terra` and the Variant D instructions as the target configuration, recorded as `product/validation/Product_Decisions.md` DEC-030.  The bounded implementation delivery DEC-030 authorized was completed on `feature/editorial-direction-gpt-5-6-terra` (typecheck, lint, 41/41 tests including new DEC-030 regression coverage, build, and full repository validation all passing) and merged to `develop` as PR #130 (commit `afb07eb`), including the matching `render.yaml` `OPENAI_MODEL` update.  Post-merge, the Repository Author completed literal hosted acceptance through `https://studio.ramrattan.com`: hosted health, magic-link authentication, project creation, real public-URL submission, Editorial Direction generation, fresh Render `[openai-usage]` runtime evidence confirming `gpt-5.6-terra` (not `gpt-4o-mini`), unchanged schema rendering, browser-refresh persistence/rehydration, durable Reject with feedback surviving refresh, Approve advancing the workflow, and confirmed authentication protection after sign-out.  BL-001's Outcome (editorial parity with the locked GPT baseline) is achieved to the standard this delivery was scoped to prove: the approved configuration is live in the hosted Web Product and verified end-to-end through the real application path. |
| Notes | Primary WIP=1 item for DS-01.  BL-002 completed (Done) alongside it, never having independently entered In Progress, per the Delivery Operating Model's WIP=1 rule.  DS-01 is closed; see BACKLOG.md's "Latest Closeout" section for the full record. |

### BL-002 - Model-selection quality/cost evaluation for Editorial Direction

| Field | Value |
|---|---|
| Outcome | A deliberate, evidence-based decision on which OpenAI model to use for Editorial Direction (and future Editorial Plan/Draft), balancing quality against cost. |
| Evidence / Source | `docs/product/version2/Web_Product_Foundation_v1.md` Section 5 explicitly deferred "model-selection policy beyond 'use a capable general-purpose model.'" `gpt-4o-mini` was used for foundation verification as an implementation detail, never accepted as a product quality decision. |
| Priority | P1 |
| Kanban State | Done (DEC-030, approved 2026-08-11) |
| Dependencies | Informed BL-001; resolved together in DS-01. |
| Acceptance Summary | Met.  DS-01 (2026-08-11) produced an evidence-based model recommendation - `gpt-5.6-terra`, OpenAI's current "balance of intelligence and cost" tier - grounded in authoritative OpenAI pricing/model documentation and confirmed by two controlled evaluation passes on materially different sources.  The Repository Author reviewed and approved it as `product/validation/Product_Decisions.md` DEC-030.  This backlog item's Outcome (a deliberate, evidence-based model decision) is fully achieved; the resulting implementation is tracked separately, not as further BL-002 work. |
| Notes | Supporting investigation for BL-001, never a second primary In Progress item, per the Delivery Operating Model's WIP=1 rule.  Completed without independently entering In Progress. |

### BL-003 - Web Walking Skeleton 02 - Editorial Plan + Draft

| Field | Value |
|---|---|
| Outcome | `Approved Editorial Direction -> Editorial Plan -> native Approve/Reject -> Draft generation -> persistent article workspace`, per `ROADMAP.md`'s Version 2 Checkpoint. |
| Evidence / Source | `ROADMAP.md`, "Version 2 Checkpoint" - "Next Vertical Slice (Not Started)." |
| Priority | P2 - deliberately **not** auto-elevated to P1 merely because it was previously named "next." Building a deeper generation workflow on top of unproven editorial quality (BL-001) carries real rework risk. |
| Kanban State | In Progress (scoping sprint) - BL-001/BL-002 are now Done, resolving the prior dependency; a bounded scoping delivery defined the slice without implementing it. |
| Dependencies | BL-001/BL-002 resolution (Done, see DEC-030). Two Repository Author decisions remain open before implementation: see `docs/product/version2/Web_Walking_Skeleton_02_Scope.md` Section 11. |
| Acceptance Summary | Scope defined, not yet implemented. `docs/product/version2/Web_Walking_Skeleton_02_Scope.md` defines the exact starting/ending project state, the minimum Editorial Plan and Draft capability, persistence/refresh requirements, eight literal Acceptance Criteria, and a prepared (not executed) Engineering Work Order per `docs/engineering/AI_Engineering_Work_Order_Template.md`. |
| Notes | Scoping only - no implementation performed. Two decisions require explicit Repository Author confirmation before an implementation delivery can be authorized (synchronous generation trigger; Editorial Plan revision semantics) - see the scope document Section 11. |

### BL-004 - Real outbound email / SMTP for the production Author experience

| Field | Value |
|---|---|
| Outcome | Real magic-link email delivery (`SmtpEmailProvider`, e.g. Resend) for the production Author experience, replacing the console/Render-Logs mechanism used for hosted development. |
| Evidence / Source | `web/README.md` hosted-deployment section; `Web_Product_Foundation_v1.md` Section 13 external-dependency plan item 6. |
| Priority | P3 - console magic links remain acceptable for current hosted development. |
| Kanban State | Backlog |
| Dependencies | Requires a Repository Author decision on SMTP provider - Resend is the recorded candidate, not yet selected. |
| Acceptance Summary | A real email is received and clicked through, in place of Render Logs tab retrieval. |

### BL-005 - Render PostgreSQL free-tier lifecycle decision

| Field | Value |
|---|---|
| Outcome | Explicit Repository Author decision on whether/when to upgrade the free Render PostgreSQL database before it expires. |
| Evidence / Source | `web/README.md`: "the free PostgreSQL database expires 30 days after creation (14-day grace period before deletion)." The database was created as part of the Render Blueprint applied via PR #116 (merged 2026-08-11). |
| Priority | **P0** - time-bound operational risk; data loss if not decided before the window closes. |
| Kanban State | Backlog |
| Dependencies | Repository Author decision: upgrade to the paid `basic-256mb` plan, or accept eventual data loss/recreation. |
| Acceptance Summary | Explicit decision recorded; if upgrading, executed before expiry. |
| Notes | Confirm the exact creation timestamp in the Render dashboard for a precise deadline; treat conservatively as within 30 days of 2026-08-11. |

### BL-006 - Render web-service cold-start / tier decision

| Field | Value |
|---|---|
| Outcome | Explicit decision on whether the free web service's ~15-minute idle spin-down (brief cold-start delay on the next request) remains acceptable, or warrants upgrading to the paid `starter` plan. |
| Evidence / Source | `web/README.md` free-tier note. |
| Priority | P3 - acceptable during development unless it becomes disruptive. |
| Kanban State | Backlog |
| Dependencies | None. |
| Acceptance Summary | Not applicable - monitor; revisit only if disruptive. |

### BL-007 - Web Hero Visual capability

| Field | Value |
|---|---|
| Outcome | Web-product Hero Visual generation preserving the established 720 x 425, 144:85 output contract. |
| Evidence / Source | `Web_Product_Foundation_v1.md` Section 8; `ROADMAP.md` "Later Web Slices." |
| Priority | P3 |
| Kanban State | Backlog |
| Dependencies | Sequenced after Web Walking Skeleton 02 (BL-003) - an article must exist before a Hero Visual attaches to one. |
| Acceptance Summary | Not yet written. |

### BL-008 - LinkedIn publishing (Author-authorized)

| Field | Value |
|---|---|
| Outcome | Author-authorized publishing to LinkedIn using the Author's own OAuth-granted credentials (`w_member_social` scope), per the confirmed feasibility finding. |
| Evidence / Source | `Web_Product_Foundation_v1.md` Section 7 (feasible now via self-serve OAuth, no special LinkedIn approval required); `ROADMAP.md` "Later Web Slices." |
| Priority | P3 |
| Kanban State | Backlog |
| Dependencies | Sequenced after Hero Visual (BL-007) and publication package assembly. |
| Acceptance Summary | Not yet written. |
| Notes | The Author's LinkedIn password is never collected or stored - OAuth only, per the Studio's constitutional constraint. |

### BL-009 - Reader Engagement (manual-input path)

| Field | Value |
|---|---|
| Outcome | Published Editorial Projects may enter a Reader Engagement state; Author-supplied comment/reply content is used to help the Author understand and respond, per Capability 013 / DEC-027. |
| Evidence / Source | `product/validation/Product_Validation_Log.md` PV-028; `product/validation/Product_Decisions.md` DEC-027; `docs/product/version2/Capability_013_Reader_Engagement.md`. |
| Priority | P3 |
| Kanban State | Backlog |
| Dependencies | Sequenced after a Published Editorial Project state exists (LinkedIn publishing, BL-008, or another publication path). |
| Acceptance Summary | Not yet written. |
| Notes | **Manual Author-input path only.** LinkedIn's Comments API (`r_member_social`) remains closed to new access requests - do not design around automated comment ingestion; re-verify LinkedIn's current documentation before any future attempt. |

### BL-010 - Production readiness / security hardening review

| Field | Value |
|---|---|
| Outcome | A formal review of production-readiness gaps once main-branch promotion/release is decided. No compliance program, threat model, or penetration-test plan is currently authorized. |
| Evidence / Source | `Web_Product_Foundation_v1.md` Section 11. |
| Priority | P3 - no known urgent gap; SSRF protection, Author isolation, and secret handling are already verified for the hosted-dev deployment. |
| Kanban State | Backlog |
| Dependencies | BL-004 (SMTP), BL-005/BL-006 (Render tier decisions), and BL-011 (Version 1/1.1 release decision). Umbrella item - does not duplicate their individual tracking. |
| Acceptance Summary | Not yet written. |

### BL-016 - Dependency Supply-Chain Security Visibility

| Field | Value |
|---|---|
| Outcome | Verify and maintain GitHub dependency supply-chain visibility without remediating packages, including Dependency Graph coverage, Dependabot vulnerability alerts, and a documented follow-up policy for security updates and version-update automation. |
| Evidence / Source | GitHub repository dependency state, security visibility configuration, and current alert findings. |
| Priority | P2 |
| Kanban State | Backlog |
| Dependencies | None technical; depends on repository owner review of security visibility and vulnerability findings. |
| Acceptance Summary | GitHub dependency graph and Dependabot alerts are verified, security-update automation is intentionally left unchanged, and a follow-up remediation priority policy is recorded in the backlog. |

### BL-012 - B002 - Brand Identity Refinement

| Field | Value |
|---|---|
| Outcome | Refine the approved RC1 brand identity assets per any accumulated real-use feedback. |
| Evidence / Source | `ROADMAP.md` Initiative B001/B002; GitHub issue #41. |
| Priority | P3 - explicitly Low Priority, Post-RC1, non-blocking throughout `ROADMAP.md`. |
| Kanban State | Backlog |
| Dependencies | None. |
| Acceptance Summary | Not yet written. |

### BL-013 - Capability 012 - Portable Author Context

| Field | Value |
|---|---|
| Outcome | Reduce repetitive editorial setup via portable, Author-controlled context, while preserving the Studio's stateless architecture. |
| Evidence / Source | `docs/product/version2/Capability_012_Portable_Author_Context.md` - "Version 2 Candidate... Not Yet Approved for Implementation." |
| Priority | P3 |
| Kanban State | Backlog |
| Dependencies | None identified. |
| Acceptance Summary | Not yet written. |

### BL-014 - Author editing workspace / DEC-013 resolution

| Field | Value |
|---|---|
| Outcome | Resolve the long-standing open discrepancy on whether and how the Editor may assist with editing already-approved Publication Content, through a native editing surface. |
| Evidence / Source | DEC-013 in `product/validation/Product_Decisions.md` ("Explicitly authorized editing - NOT adopted; discrepancy recorded"), repeatedly referenced as "remains unresolved" across DEC-017, DEC-025, DEC-026, and DEC-029. |
| Priority | P3 |
| Kanban State | Backlog |
| Dependencies | Architectural/governance decision; likely intersects with the Web Walking Skeleton progression once a Draft/article surface exists (BL-003). |
| Acceptance Summary | Not yet written. |
| Notes | Long-standing and deliberately unresolved - do not resolve unilaterally. |

### BL-015 - Wiki Evolution - Human-Facing Project Knowledge

| Field | Value |
|---|---|
| Outcome | Evolve the GitHub Wiki beyond its minimal Home/Sidebar only when project complexity creates a demonstrated navigation, onboarding, stakeholder, release, or knowledge-orientation need. |
| Evidence / Source | GitHub Wiki Discovery found the Wiki had never been initialized and that a single Home page is currently sufficient - additional pages would largely duplicate authoritative repository sources (`BACKLOG.md`, `ROADMAP.md`, `HANDOFF.md`, `docs/product/version2/Web_Product_Foundation_v1.md`, etc.). |
| Priority | P3 |
| Kanban State | Backlog |
| Dependencies | None. |
| Acceptance Summary | Not yet written. |
| Notes | Reconsideration triggers may include: a major release; multiple implemented Version 2 capabilities; material architecture expansion; a meaningful stakeholder/onboarding need; the Home page becoming difficult to navigate; or a subject gaining enough stable orientation value to justify a maintained Wiki page.  Acceptance principle for any additional page: it must have a clear human-navigation/orientation purpose, identify or link to authoritative repository sources, avoid becoming an operational source of truth, and avoid duplicating fast-changing backlog/Kanban state.  Not moved to Ready or In Progress by this delivery. |

## GitHub Project and Issues - Known State, Not Canonical

GitHub Project #1 ("Ramrattan AI Editorial Studio") and several open
GitHub issues (`Sprint 3B`/`3C`, "Build the LinkedIn Visual System",
"Build the Evidence and Research Engine", "Future - Secure Cloud Author
Repository", "Future - Host Platform Preference", "Future - Commercial
Packaging") exist from an earlier planning generation. The Project was
actively maintained through the end of the Version 1.1 Engineering Epic
but contains **no items at all** for the entire Version 2 / Web Product
Track (GPT recovery, Reader Engagement discovery, Web Product
Foundation, Web Walking Skeleton 01, or the Render deployment) - it has
not been kept current since Version 1.1 completed, and its `Status`
field is the generic three-state default (`Todo`/`In Progress`/`Done`),
not the five-state flow this file uses.

This file is authoritative going forward. Reconciling or reviving the
GitHub Project as canonical instead is a possible future decision, not
made here - doing so would require substantial GitHub-side reconciliation
work outside this delivery's scope.
