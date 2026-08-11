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
| BL-001 through BL-010, BL-012 through BL-015 | BL-011 | *(none)* | *(none)* | *(see completed capabilities in ROADMAP.md - this board tracks forward-looking work, not delivery history)* |

## Current Sprint

**No active Daily Sprint.** The next Daily Sprint is selected from this
backlog at the start of the next session, per
`docs/engineering/Delivery_Operating_Model.md`'s Daily Start sequence.
This delivery explicitly does not select it - see "Tomorrow's Sprint
Readiness" as the next authorized task.

## Latest Closeout

**Not applicable yet** - no Daily Sprint has run under this operating
model. The first Daily Closeout will be recorded here after the first
Daily Sprint.

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
| Kanban State | Ready - fully defined, blocked only on Repository Author decision, no further engineering scoping needed |
| Dependencies | None technical - pure decision. Independent of the Web Product Track (BL-001 through BL-010). |
| Acceptance Summary | Decision recorded; if approved, promotion/tag/release executed per the existing release process. |

### BL-001 - Editorial Direction quality parity with the locked GPT baseline

| Field | Value |
|---|---|
| Outcome | Web Editorial Direction output is at least as strong, editorially, as the locked private GPT's (`GPT Recovery RC5`) output for comparable source material. |
| Evidence / Source | Repository Author, real hosted browser acceptance (2026-08-11): the Web Editorial Direction was technically functional (real OpenAI call, schema-valid, persisted, Approve/Reject working) but materially weaker editorially than the locked GPT baseline. **Not yet formalized as a Product Validation Log entry** - this backlog item is the interim record; promoting it to a formal `PV-029` entry is a reasonable next step for the Repository Author to authorize separately, not done in this delivery. |
| Priority | P1 |
| Kanban State | Backlog |
| Dependencies | Closely coupled to BL-002 (model selection); recommend resolving before deepening the generation pipeline (BL-003). |
| Acceptance Summary | Not yet defined - requires a product decision on target quality bar, comparison method, and whether the gap is prompt-only or model-selection-related. |

### BL-002 - Model-selection quality/cost evaluation for Editorial Direction

| Field | Value |
|---|---|
| Outcome | A deliberate, evidence-based decision on which OpenAI model to use for Editorial Direction (and future Editorial Plan/Draft), balancing quality against cost. |
| Evidence / Source | `docs/product/version2/Web_Product_Foundation_v1.md` Section 5 explicitly deferred "model-selection policy beyond 'use a capable general-purpose model.'" `gpt-4o-mini` was used for foundation verification as an implementation detail, never accepted as a product quality decision. |
| Priority | P1 |
| Kanban State | Backlog |
| Dependencies | Informs BL-001; may be resolved together. |
| Acceptance Summary | Not yet defined - candidate output: a short model comparison and recommendation, reviewed by the Repository Author. |

### BL-003 - Web Walking Skeleton 02 - Editorial Plan + Draft

| Field | Value |
|---|---|
| Outcome | `Approved Editorial Direction -> Editorial Plan -> native Approve/Reject -> Draft generation -> persistent article workspace`, per `ROADMAP.md`'s Version 2 Checkpoint. |
| Evidence / Source | `ROADMAP.md`, "Version 2 Checkpoint" - "Next Vertical Slice (Not Started)." |
| Priority | P2 - deliberately **not** auto-elevated to P1 merely because it was previously named "next." Building a deeper generation workflow on top of unproven editorial quality (BL-001) carries real rework risk. |
| Kanban State | Backlog |
| Dependencies | Should weigh BL-001/BL-002 resolution first. |
| Acceptance Summary | Not yet written - no Engineering Delivery Order exists for this slice. |
| Notes | Not started. Not authorized by this delivery. |

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
| Notes | Reconsideration triggers may include: a major release; multiple implemented Version 2 capabilities; material architecture expansion; a meaningful stakeholder/onboarding need; the Home page becoming difficult to navigate; or a subject gaining enough stable orientation value to justify a maintained Wiki page. Acceptance principle for any additional page: it must have a clear human-navigation/orientation purpose, identify or link to authoritative repository sources, avoid becoming an operational source of truth, and avoid duplicating fast-changing backlog/Kanban state. Not moved to Ready or In Progress by this delivery. |

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
