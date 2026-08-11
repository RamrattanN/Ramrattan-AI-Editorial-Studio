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
| BL-002 through BL-010, BL-012 through BL-015 | BL-011 | BL-001 | *(none)* | *(see completed capabilities in ROADMAP.md - this board tracks forward-looking work, not delivery history)* |

## Current Sprint

| Field | Value |
|---|---|
| Sprint Date / ID | DS-01, 2026-08-11 |
| Outcome | Determine why the Web Product's Editorial Direction is materially weaker editorially than the locked GPT baseline (PV-029), and produce an evidence-backed recommendation for the Web Product's Editorial Direction configuration. |
| Must Complete | Baseline reconstruction (locked GPT and current Web path); difference analysis; a controlled evaluation; a bounded finding on primary cause (prompt, model, context, source processing, schema, or a combination); a model/configuration recommendation with quality/cost rationale; a finding on whether Editorial Direction quality is now sufficiently understood to permit Web Walking Skeleton 02. |
| Stretch | A narrow, reversible, prompt-only production change, authorized only if evidence clearly isolates a prompt-only cause requiring no model, schema, persistence, source-processing, or architecture change. |
| Acceptance Criteria | The sprint's five governing questions are each answered with a bounded, evidence-based conclusion, not "more investigation is required"; a durable evidence artifact exists; the Repository Author has a concise comparison to review before any implementation decision. |
| Dependencies | BL-002 (model-selection evaluation), resolved as supporting investigation under this sprint; does not independently enter In Progress. |
| Risks | Real OpenAI evaluation cost; editorial-quality judgment remains the Repository Author's, not the agent's; rework risk if Web Walking Skeleton 02 is deemed ready prematurely. |
| Explicit Non-Goals | Web Walking Skeleton 02, Editorial Plan, Draft, Hero Visual, LinkedIn publishing, Reader Engagement, locked GPT or GPT Knowledge changes, SMTP, Render/DNS changes, `main` promotion, tagging, BL-011, BL-016, Codex audible-notification troubleshooting, Wiki expansion. |
| Owner / Execution Agent | Claude |
| Review Agent | Codex, scope determined by findings (see final report) |
| Status | In Progress - baseline reconstruction, difference analysis, evaluation design, and model research are complete; the sprint's Must Complete bar requires *executed* controlled comparisons, which have not run (Section 5 of the evidence artifact - no `OPENAI_API_KEY` in this environment).  Not Review / Validation: an unexecuted evidence package is not yet the completed evidence the Delivery Operating Model's Review / Validation column presumes.  See `docs/product/version2/Editorial_Direction_Quality_Investigation.md` and the pending execution-boundary decision recorded there. |

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
| Evidence / Source | Repository Author, real hosted browser acceptance (2026-08-11): the Web Editorial Direction was technically functional (real OpenAI call, schema-valid, persisted, Approve/Reject working) but materially weaker editorially than the locked GPT baseline.  Formalized as `product/validation/Product_Validation_Log.md` PV-029 (observational evidence only, no cause prejudged). |
| Priority | P1 |
| Kanban State | In Progress (DS-01) |
| Dependencies | Closely coupled to BL-002 (model selection); recommend resolving before deepening the generation pipeline (BL-003). |
| Acceptance Summary | DS-01 (2026-08-11) executed two bounded 4-call evaluation matrices on materially different sources (cybersecurity, then NASA/AI-policy; combined measured cost $0.042630; see `docs/product/version2/Editorial_Direction_Quality_Investigation.md` Sections 13-14).  Both passes showed the same D > C > B > A quality pattern; the model effect (A -> C) repeated strongly, the prompt effect (A -> B) repeated but with variable magnitude, D remained strongest in both, and extraction noise did not visibly degrade either result.  No material contradiction was found between passes.  **Not yet reviewed by the Repository Author.**  Not treated as proof; no winner has been declared. |
| Notes | Primary WIP=1 item for DS-01; BL-002 is resolved alongside it as supporting investigation and does not separately enter In Progress, per the Delivery Operating Model's WIP=1 rule.  Remains In Progress, not Review / Validation, until the Repository Author has reviewed both executed comparisons (Sections 13-14 of the evidence artifact), per explicit instruction. |

### BL-002 - Model-selection quality/cost evaluation for Editorial Direction

| Field | Value |
|---|---|
| Outcome | A deliberate, evidence-based decision on which OpenAI model to use for Editorial Direction (and future Editorial Plan/Draft), balancing quality against cost. |
| Evidence / Source | `docs/product/version2/Web_Product_Foundation_v1.md` Section 5 explicitly deferred "model-selection policy beyond 'use a capable general-purpose model.'" `gpt-4o-mini` was used for foundation verification as an implementation detail, never accepted as a product quality decision. |
| Priority | P1 |
| Kanban State | Backlog (resolved as DS-01 supporting investigation; not moved independently) |
| Dependencies | Informs BL-001; resolved together in DS-01. |
| Acceptance Summary | DS-01 (2026-08-11) produced an interim candidate, not yet a decision: `gpt-5.6-terra`, OpenAI's current "balance of intelligence and cost" tier, grounded in authoritative OpenAI pricing/model documentation, with an estimated per-request cost comparison against `gpt-4o-mini`, `gpt-5.6-luna`, `gpt-5.6-sol`, and `gpt-4o`.  **Not empirically confirmed** - no live comparison has been executed (no `OPENAI_API_KEY` in this environment) and the Repository Author has not reviewed or accepted it.  See `docs/product/version2/Editorial_Direction_Quality_Investigation.md` Section 6 and Section 9. |
| Notes | Supporting investigation for BL-001, not a second primary In Progress item.  Resolved within the same sprint as BL-001 without independently entering the In Progress column, per the Delivery Operating Model's WIP=1 rule. |

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
