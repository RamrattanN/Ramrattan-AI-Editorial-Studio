# Delivery Operating Model

**Status:** Active
**Classification:** Process definition (Informative - operational, not
constitutional)

## Purpose

Establish a lean delivery operating model - daily sprints, daily
closeout, a maintained backlog and Kanban, weekly demos, weekly
retrospectives, and Lessons Learned integration - that accelerates
product delivery rather than creating project-management overhead.

This document defines the *process*. [`BACKLOG.md`](../../BACKLOG.md)
at the repository root is the *data* this process operates on - the
single canonical view of current backlog items, priority, and Kanban
state. Read `BACKLOG.md`'s "Authority and Scope" section for the
complete ownership table across all planning documents.

This document does not define repository governance, delivery
mechanics, or approval boundaries. Where it appears to conflict with
`AGENTS.md`, `docs/engineering/Capability_Delivery_Workflow.md`,
`docs/engineering/AI_Engineering_Standard.md`, or
`docs/engineering/AI_Collaboration_Standard.md`, those documents
control; the conflict is reported rather than silently resolved, per
`AGENTS.md`'s Instruction Authority order.

## Three Distinct Decisions

Keep these distinct. Conflating them is the most common source of
uncontrolled scope growth:

| Stage | Question | Owner |
|---|---|---|
| **Product Discovery** | What work might be valuable? | Anyone - real use, review, an agent, the Repository Author |
| **Backlog Prioritization** | Should this be built, and when? | Repository Author, recorded in `BACKLOG.md` |
| **Sprint Commitment** | What is actually being delivered right now? | Whoever starts the Daily Sprint, from `BACKLOG.md` |

A new idea discovered mid-sprint does **not** automatically become
current sprint scope. Apply this default rule:

| Discovery type | Effect on the active sprint |
|---|---|
| **Critical blocker** | May enter the active sprint immediately, only when necessary to complete the committed outcome. |
| **Required dependency** | May enter only when explicitly recognized as necessary for the committed outcome. |
| **Improvement / quality opportunity** | Backlog by default. |
| **Unrelated opportunity** | Backlog or Parking Lot. |

Do not silently expand sprint scope. If a discovery doesn't clearly fit
the first two rows, it goes to `BACKLOG.md`, not into today's work.

## Daily Sprint

A Daily Sprint is a **one-day execution commitment**, not a traditional
multi-week Scrum sprint.

**Fields** (only these - no others):

- Sprint Date / ID
- Outcome
- Must Complete
- Stretch
- Acceptance Criteria
- Dependencies
- Risks
- Explicit Non-Goals
- Owner / execution agent
- Review agent (where appropriate)
- Status

**Daily Start:**

1. Synchronize `develop` with `origin/develop`.
2. Review the previous Daily Closeout (in `BACKLOG.md`'s "Latest
   Closeout" section).
3. Review current blockers/dependencies.
4. Review `BACKLOG.md` (the canonical backlog/Kanban).
5. Select **one** primary sprint outcome.
6. Confirm acceptance criteria.
7. Move only the authorized work item(s) into `In Progress` on the
   Kanban board (respecting the WIP limit below).
8. Begin execution.

Do not create hour-by-hour planning. Do not schedule every task in
advance. Record the day's sprint by overwriting `BACKLOG.md`'s "Current
Sprint" section - do not create a new file per day.

## Daily Closeout

A short closeout, taking minutes, not a report-writing exercise.

**Fields:**

- Committed outcome
- Completed
- Not completed
- Blockers
- Defects discovered
- Product discoveries
- Lessons learned
- Backlog changes
- Kanban changes
- Repository / deployment state
- Recommended starting point for tomorrow

**Classify every discovery before closeout** as exactly one of:

- Defect
- Blocker
- Backlog item
- Lesson learned
- Product-validation evidence
- No action

Do not promote every observation into a permanent rule. Most
discoveries are defects or backlog items (see BL-001 in `BACKLOG.md`
for a live example: a real quality observation, recorded as backlog
evidence, explicitly *not* auto-promoted into a Product Validation Log
entry or a process rule). A discovery earns "Lesson learned" status only
when it has genuinely reusable value beyond this one instance (see
"Lessons Learned Integration" below).

Record the closeout by overwriting `BACKLOG.md`'s "Latest Closeout"
section - one current record, not an accumulating file per day. Git
history already preserves every prior day's record if it's ever needed
again.

## Kanban

**Flow:**

```text
Backlog -> Ready -> In Progress -> Review / Validation -> Done
```

A `Blocked` state may be added later only if it materially improves
visibility without adding unnecessary complexity - not by default.

**WIP limits:**

- `In Progress`: maximum **1** primary product delivery.
- `Review / Validation`: maximum **2** items.

The purpose of the limit is to finish work before starting more work.

**Agent pattern:**

- **Claude** - primary implementation / documentation delivery.
- **Codex** - targeted independent review where risk, architecture,
  security, persistence, workflow state, or an explicit acceptance
  concern warrants it.

Claude and Codex should not normally implement the same scope in
parallel. Do not automatically duplicate every Claude delivery with a
full Codex review - reserve Codex review for the specific risk
categories above, not as a blanket second pass.

## Prioritization

```text
P0            Active blocker / immediate operational risk.
P1            Critical path / next high-value work.
P2            Important but not immediate.
P3            Later candidate.
Parking Lot   Discovery or idea not yet ready for commitment.
```

Consider, when prioritizing: Author value, critical-path dependency,
quality risk, rework risk, evidence, effort/complexity, and operational
deadlines. No weighted scoring model - use judgment against these
factors, recorded in the backlog item's evidence.

Do not default a previously-named "next" capability to P1 merely because
it was named next. Explicitly weigh whether a quality or foundation risk
should be resolved first (see `BACKLOG.md` BL-001 through BL-003 for a
live example of this reasoning applied).

Do not decide the next Daily Sprint as part of prioritization work -
that is a separate, explicit "Tomorrow's Sprint Readiness" step, done at
the next Daily Start, not during backlog maintenance.

## Weekly Demo

**Purpose:** demonstrate working product from the Author's perspective.
Prefer working product over slides - do not create a slide-deck
requirement. Documentation-only demonstration is acceptable only when
the week's increment is genuinely non-executable.

**Structure:**

1. Outcome targeted.
2. Live product journey.
3. Newly working behavior.
4. Acceptance/evidence passed.
5. Known gaps.
6. Decisions required.

Cadence: weekly. The specific day/time is a Repository Author choice,
not assumed here - record it in `HANDOFF.md` once selected.

## Weekly Retrospective

**Structure:**

- Continue
- Stop
- Start
- Biggest delivery friction
- Biggest acceleration
- Rework/defects caused by process
- Lessons worth promoting
- Maximum **1-2** operating changes for the following week

The retrospective must improve delivery, not generate ceremony. Limiting
operating changes to 1-2 per week is deliberate - it prevents the
process itself from becoming unstable.

## Lessons Learned Integration

`docs/learning/` is the existing, established home for durable, reusable
lessons - see `AI_Developer_Bootstrap_Lessons.md` and
`AI_Developer_Bootstrap_Checklist.md` in that directory (not duplicated
here; reference them directly).

A lesson is promoted to `docs/learning/` - typically at Daily Closeout
or the Weekly Retrospective - only when it distinguishes:

- **Observation** - what was seen.
- **Impact** - what it affected.
- **Cause** - why it happened.
- **Reusable Lesson** - what generalizes beyond this one instance.
- **Future Rule / Checklist Change** - the concrete, durable change that
  results.

Most discoveries do not clear this bar. A minor defect stays a defect,
tracked in `BACKLOG.md`, not a permanent process rule.

## Document Synchronization Cadence

| Artifact | Updates |
|---|---|
| `BACKLOG.md` (canonical backlog/Kanban) | Whenever operational state materially changes. |
| Daily Sprint | Created/confirmed at Daily Start; overwrites `BACKLOG.md`'s "Current Sprint" section. |
| Daily Closeout | Once, at end of day; overwrites `BACKLOG.md`'s "Latest Closeout" section. |
| `ROADMAP.md` | When milestones, strategic sequence, or material priorities change. Not on every trivial action. |
| `HANDOFF.md` | At meaningful stopping points, deployment/environment transitions, or machine/session handoff. Not a duplicate of `BACKLOG.md`'s daily detail. |
| `docs/learning/` (Lessons Learned) | When a reusable lesson is promoted - normally at closeout or retrospective. |
| `product/validation/Product_Validation_Log.md` | Only when real product evidence meets the existing governance criteria in that document. |
| `product/validation/Product_Decisions.md` | Only when evidence is promoted into an explicit, Repository-Author-approved product decision. |
| GitHub Wiki | At meaningful product milestones, releases, major accepted capability changes, or material architecture/deployment changes. Not on every PR. |

Do not churn `ROADMAP.md` or `HANDOFF.md` after trivial actions. If an
update to one of them would only restate what `BACKLOG.md` already
says, it's the wrong document for that update.

The GitHub Wiki is human-facing orientation and synthesis only. It is
never canonical for backlog, Kanban, roadmap, product decisions,
acceptance criteria, or architecture specification - those remain owned
by the documents in the table above and in `BACKLOG.md`'s "Authority and
Scope" section. Synchronize the Wiki at the cadence in the table; do not
update it after every PR, and do not let it accumulate detail that
duplicates a faster-moving canonical source.

## Non-Goals

This model does not:

- replace the Capability Delivery Workflow, approval profiles, or any
  approval boundary defined in `AGENTS.md`;
- introduce story-point estimation, hour-level scheduling, or a
  weighted-scoring prioritization model;
- require a slide deck for the weekly demo;
- create a new file per Daily Sprint or Daily Closeout - both live as
  the current, overwritten sections of `BACKLOG.md`;
- promote every observation into a permanent rule; or
- decide, by itself, what the next Daily Sprint's committed outcome is -
  that is a separate, explicit step taken at the next Daily Start.
