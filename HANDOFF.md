# HANDOFF.md

# Repository Continuity & AI Handoff

---

## Purpose

This document provides the minimum operational context required for an AI assistant or the Repository Author to resume productive work after a new session or loss of conversational context.

It is **not** a governance document.

Repository governance is defined in **AGENTS.md**.

This document exists to:

- Preserve engineering continuity
- Reduce AI onboarding time
- Minimise token consumption
- Prevent repeated discovery work

---

# Repository Status

**Repository**

Ramrattan AI Editorial Studio

**Branch**

`develop`

**Architecture Baseline**

`2026.08.04v14`

**Repository State**

- Working tree clean
- `develop` synchronized with `origin/develop`
- Deterministic bootstraps operational
- Repository validation expected to pass

---

# Current Delivery Status

## Completed

### Brand

- B001 - Brand Identity

### Capabilities

- Capability 001
- Capability 002
- Capability 003
- Capability 004
- Capability 005
- Capability 006
- Capability 007
- Capability 008
- Capability 009 - Article Engine
- Capability 010 - Hero Visual System
- Capability 011 - Portable Editorial Project

### Engineering

- Delegated Delivery Workflow
- RC1 Documentation Reconciliation
- Issue #18 - Version 1 End-to-End Demo and RC1 Release Readiness
- Version 1 RC1 Release Readiness
- Claude Code Integration

### Version 1.1

- V11-01 - Author Journey Foundation (Issue #70, PR #81)
- V11-02 - Editorial Source and Branding Intake (Issue #71, PR #82)
- V11-03 - Editorial Discovery and Editorial Plan Gates (Issue #72, PR #83)
- V11-04 - Generation Orchestration and Blocked/Failed Handling (Issue #73, PR #84)
- V11-05 - Publication Studio Workspace (Issue #74, PR #85)
- V11-06 - Editorial Audit and the Copy LinkedIn Publication Gate (Issue #75, PR #88)
- V11-07 - Resume Existing Project Integration (Issue #76, PR #89)
- V11-08 - Session Completion, Configuration Generation, and Session Artifacts (Issue #77, PR #90)
- V11-09 - End-to-End Author Acceptance Evidence (Issue #78, PR #91)
- V11-10 - Documentation and Status Reconciliation (Issue #79)

ADR-018 and ADR-019 are Accepted. Version 1.1 Epic completion does not
authorize release; see Current Focus below.

Current validation baseline:

- Compileall PASS
- Repository Validation PASS
- 484 Tests PASS

### Version 2 (Web Product Track)

- Private GPT recovery locked as **GPT Recovery RC5 - Locked Private GPT
  Baseline** (PR #108, DEC-026); change-controlled by real-use evidence.
- Reader Engagement discovery recorded (PV-028, DEC-027, PR #109);
  future web-product scope only, not implemented.
- Web Product Foundation v1 adopted (DEC-028, PR #110).
- Web Walking Skeleton 01 implemented (PR #111, merged commit `08cb986`):
  `web/client` and `web/server`, email magic-link auth, persistent
  `EditorialProject`/`Source`/`EditorialDirection`, server-side OpenAI
  integration, native Approve/Reject.

`ROADMAP.md` ("Version 2 Checkpoint" section) is authoritative for current
Version 2 status, including what remains not yet verified.

---

# Current Focus

## Active Objective

Two independent objectives are active in parallel; neither blocks the
other.

**1. Manual Version 1 and Version 1.1 Release Decisions - Resolved**

Issue #18 and Version 1 RC1 Release Readiness are Complete and released
(`v1.0.0`, GitHub Release published 2026-08-03). Version 1.1 (V11-01
through V11-10, Issue #69 Epic, closed) is also Complete and released:
the Repository Author authorized a pinned promotion from the verified
Version 1.1 completion boundary (commit `a00111d`, PR #92) to `main`
via PR #133 (merged 2026-08-11), intentionally excluding subsequent
Version 2 Web Product work. Tagged `v1.1.0` and published as a GitHub
Release ("Ramrattan AI Editorial Studio v1.1.0 - Author Experience",
2026-08-11). `BACKLOG.md` BL-011 is Done. No external announcement has
been published yet - that remains a separate, not-yet-requested action.

**2. Web Product - Foundation Complete (Hosted, Browser-Accepted)**

Web Walking Skeleton 01 is implemented, real OpenAI Editorial Direction
generation is verified, and the application is now deployed to Render at
both `https://ramrattan-studio.onrender.com` and the custom domain
`https://studio.ramrattan.com` (Hostinger DNS, TLS via Render). The
Repository Author completed literal browser acceptance against both
URLs, including sign-in, project creation, real OpenAI Editorial
Direction, Approve advancing to `editorial_plan`, refresh persistence,
sign-out, and a second independent sign-in recovering the same project.
The foundation objective sequence is complete; no further action is
pending on it. See `ROADMAP.md` ("Version 2 Checkpoint") and
`docs/product/version2/Web_Product_Foundation_v1.md` (Section 13) for
full detail. Web Walking Skeleton 02 (Editorial Plan + Draft) is the next
candidate vertical slice and has not been authorized or started - see
`BACKLOG.md` for its current priority relative to the Editorial
Direction quality observation below.

Real hosted acceptance also surfaced a material product observation,
now formalized as `product/validation/Product_Validation_Log.md`
PV-029: Editorial Direction output was technically functional but
materially weaker editorially than the locked GPT baseline.  PV-029
records the observation only and does not prejudge a model, prompt, or
implementation cause.  This is tracked as `BACKLOG.md` BL-001 (the
proposed primary sprint item) and BL-002 (supporting model-selection
investigation, not a second primary WIP item); no fix has been
authorized or implemented, and neither item is In Progress.

No Daily Sprint is currently active, and nothing is in the In Progress
Kanban column.  DS-01 - Editorial Direction Quality Investigation vs.
Locked GPT Baseline - is recommended (see `BACKLOG.md`) but has not
been authorized.  The next working session begins with Daily Start,
Repository Author approval of one sprint outcome, and only then moving
the approved primary item to In Progress.

---

# Deferred Work

## B002

Brand Identity Refinement

Status

- Todo
- Low Priority
- Post-RC1
- Non-blocking

---

# AI Responsibilities

## ChatGPT

Primary responsibilities

- Architecture
- Product thinking
- Planning
- Prompt engineering
- Design review
- Engineering strategy
- Risk analysis

---

## Codex

Primary responsibilities

- Runtime implementation
- Repository mutation
- Bootstraps
- Validation
- Git
- GitHub
- Pull Requests
- Delivery workflow

---

## Claude Code

Primary responsibilities

- Independent architecture review
- Pull request review
- Implementation critique
- Release-readiness audits
- Evidence-based verification

Claude complements implementation rather than replacing Codex.

---

# Repository Principles

Always follow **AGENTS.md**.

Core principles

- Repository-first engineering
- Deterministic generation
- Fail closed
- Small reviewable changes
- Provider-independent architecture
- Evidence over assumption

Generated sections must only be modified through their owning bootstrap.

---

# Working Style

Preferred engineering approach

- Keep prompts concise.
- Avoid repeating governance already defined in AGENTS.md.
- Validate proportionally to the size and risk of the change.
- Use targeted repository inspection.
- Avoid repository-wide inventories unless required.
- Reserve full validation for stabilised implementations.
- Use ChatGPT for architecture and planning.
- Use Codex for implementation.
- Use Claude Code for independent review.

---

# AI Efficiency

AI usage should always be proportional to the value created.

Guidelines

- Small change → small prompt.
- Large change → comprehensive prompt.
- Reuse repository knowledge.
- Do not restate established facts.
- Do not perform duplicate analysis.
- Do not spend tokens proving facts already established.
- Every repository mutation should create meaningful value.

---

# Current Priorities

**`BACKLOG.md` (repository root) is now the canonical source for
backlog items, priority, and Kanban state - operated under
`docs/engineering/Delivery_Operating_Model.md`.** This section no longer
duplicates that detail; it is retained only as a short cross-cutting
summary so a session can orient without opening `BACKLOG.md` first.

One track remains active; the other is resolved:

1. **Manual Version 1.0 / Version 1.1 release decision - Done.** `v1.0.0`
   and `v1.1.0` are both promoted to `main`, tagged, and published as
   GitHub Releases. `BACKLOG.md` BL-011 is Done. External announcement,
   if wanted, remains a separate, not-yet-requested action.
2. **Web Product Track** - Web Walking Skeleton 01's foundation is
   complete and hosted-browser-accepted. The next candidate slice (Web
   Walking Skeleton 02) is deliberately not assumed to be the next
   priority - see `BACKLOG.md` BL-001 through BL-003 for the current,
   evidence-based ordering (Editorial Direction quality parity with the
   locked GPT baseline is currently ranked ahead of deepening the
   generation workflow).

B002 Brand Refinement and every other still-open item are tracked in
`BACKLOG.md`, not enumerated here.

---

# Established Decisions

## AI

- ChatGPT is the architectural advisor.
- Codex is the implementation agent.
- Claude Code is the independent reviewer.
- Gemini has been intentionally removed.

## Architecture

- Provider-independent runtime
- Deterministic bootstraps
- Publication Package architecture
- Hero Visual architecture
- Portable Editorial Project architecture

## Delivery

Delivery Profiles

- Start
- Publish
- Complete

Governed by **AGENTS.md**.

---

# Things Not To Do

Unless explicitly approved

- Redesign completed capabilities.
- Introduce Version 2 functionality into RC1.
- Expand scope.
- Duplicate documentation.
- Create duplicate GitHub issues.
- Replace deterministic generators.
- Modify approved brand masters.
- Repeat completed validation without cause.

---

# Session Startup Checklist

Every AI session should

1. Read `HANDOFF.md`.
2. Read `AGENTS.md`.
3. Read `CLAUDE.md` (Claude Code only).
4. Verify:
   - Current branch
   - Clean working tree
   - Synchronisation with origin
5. Review `BACKLOG.md` (canonical backlog/Kanban) and its "Current
   Sprint" / "Latest Closeout" sections.
6. Review the active GitHub issue.
7. Identify the active delivery profile.
8. Begin only the approved engineering objective.

---

# Session Log

Recent engineering milestones

- B001 Brand Identity completed.
- Capability 009 delivered (Article Engine).
- Capability 010 delivered (Hero Visual System).
- Capability 011 delivered (Portable Editorial Project Resume & Export).
- RC1 Documentation Reconciliation completed.
- Claude Code adopted as the independent engineering reviewer.
- Architecture Baseline advanced to `2026.08.02v13`.
- Issue #18 and Version 1 RC1 Release Readiness completed.
- Version 1.1 Engineering Epic (Issue #69) delivered: V11-01 through V11-10
  (Issues #70-#79, PRs #81-#91) complete on `develop`.
- ADR-018 and ADR-019 transitioned to Accepted.
- Architecture Baseline advanced to `2026.08.04v14`.
- Private GPT recovered and locked as GPT Recovery RC5 - Locked Private GPT
  Baseline (PR #108, DEC-026).
- Reader Engagement discovered through real GPT use and recorded as future
  web-product scope (PV-028, DEC-027, PR #109).
- Web Product Foundation v1 adopted for the Version 2 web product (DEC-028,
  PR #110).
- Web Walking Skeleton 01 implemented: React/Vite client, Express/TypeScript
  server, PostgreSQL persistence, email magic-link auth, server-side OpenAI
  integration (PR #111, merged commit `08cb986`).
- Real OpenAI Editorial Direction foundation verified (2026-08-10):
  `OPENAI_API_KEY` configured locally; two real, non-mocked Editorial
  Direction requests executed end-to-end, approved, and persisted through
  the actual application path; non-secret usage-metadata logging added.
  Browser click-through, hosted development URL, and production email
  delivery remain not yet verified/available.
- Durable Reject contract reconciled (DEC-029, 2026-08-11): independent
  Codex review found Section 9's acceptance criteria stated persistence
  for Approve only, while Reject already persisted correctly. Repository
  Author confirmed both are durable, stage-local decisions; documentation
  corrected, no application code changed.
- Approve stage-advancement gap fixed (DEC-029, 2026-08-11): a follow-up
  Codex review found Approve did not advance `EditorialProject.stage`.
  `approveDirection` now advances the project to `editorial_plan` in the
  same transaction as the direction update.
- Render development deployment complete and literal browser acceptance
  passed (2026-08-11): deployed via `render.yaml` to
  `https://ramrattan-studio.onrender.com` and the custom domain
  `https://studio.ramrattan.com` (Hostinger DNS, Render-provisioned TLS).
  Two follow-on fixes delivered: the build's `npm install` was silently
  skipping `devDependencies` under `NODE_ENV=production` (fixed with
  `npm ci --include=dev`), and the magic-link `CLIENT_ORIGIN` still
  pointed at the Render-native hostname after the custom domain went
  live (fixed, with regression coverage). The Repository Author
  completed full browser acceptance against both URLs, including a
  second independent sign-in recovering the same persisted project.
  Web Walking Skeleton 01's foundation is now fully verified end to end.
- AI developer bootstrap lessons captured (2026-08-11):
  `docs/learning/AI_Developer_Bootstrap_Lessons.md` and its companion
  `AI_Developer_Bootstrap_Checklist.md` record the reusable engineering
  lessons from this delivery - most importantly, that AI-agent
  permission optimization (Claude Code and Codex) is a project-bootstrap
  requirement, not a late-stage convenience - so a future project starts
  with low-friction routine work and deliberately gated
  destructive/privileged/secret/merge/production actions from day one.
- Lean delivery operating model established (2026-08-11): `BACKLOG.md`
  (repository root) is now the single canonical source for backlog
  items, priority, and Kanban state, operated under
  `docs/engineering/Delivery_Operating_Model.md` (daily sprint, daily
  closeout, Kanban with WIP limits, prioritization, weekly demo, weekly
  retrospective, and document synchronization cadence). Reconciled 14
  backlog items from authoritative repository state, including the
  Editorial Direction quality observation (BL-001/BL-002) and the
  Render free-tier PostgreSQL lifecycle deadline (BL-005, P0). GitHub
  Project #1 was inspected and found stale since Version 1.1 completion
  (no Web Product Track items); not used as canonical. No product
  implementation began.
- Minimal GitHub Wiki initialized and current (2026-08-11): Home and
  `_Sidebar` orient a human reader and link to authoritative repository
  sources on `develop`; the repository remains authoritative, and Wiki
  synchronization now has an explicit cadence rule in
  `docs/engineering/Delivery_Operating_Model.md`.  A repository prose
  convention (no em/en dashes, one space after a comma, two spaces
  after a sentence period, with explicit technical exceptions) is now
  established in `AGENTS.md` for Claude, Codex, and future
  collaborators.  Sprint Preflight Governance completed ahead of DS-01
  (2026-08-11): PV-029 records the Editorial Direction quality
  observation as evidence only; `BACKLOG.md` BL-001 is clarified as
  the primary WIP=1 sprint item with BL-002 as supporting work; BL-005
  (Render PostgreSQL lifecycle) and BL-011 (Version 1.0/1.1 release
  decision) were reviewed and remain unresolved Repository Author
  decisions, with no invented deadline and no release action taken.
  No product implementation began.
- DS-01 closed and BL-001 delivered (2026-08-11): the DEC-030
  implementation (`gpt-5.6-terra`, Variant D instructions) merged as
  PR #130 and hosted-verified through the real Web Product path; DS-01
  closeout merged as PR #131. BL-001 and BL-002 are Done.
- Version 1.1 promoted and released (2026-08-11): the Repository Author
  authorized BL-011's release decision. A pinned promotion from the
  verified Version 1.1 completion boundary (commit `a00111d`, PR #92)
  to `main` merged as PR #133, deliberately excluding subsequent
  Version 2 Web Product work (Web Walking Skeleton 01, DS-01, DEC-030,
  BL-001 closeout), which remain on `develop` only. Tagged `v1.1.0` and
  published as a GitHub Release. Issue #69 (Version 1.1 Engineering
  Epic) closed - all ten V11-01 through V11-10 sub-issues were already
  closed. BL-011 is Done.

---

# Engineering Philosophy

This repository values

- Correctness over speed.
- Determinism over convenience.
- Small, reviewable increments.
- Repository truth over conversational memory.
- Evidence over assumption.
- Automation that remains understandable.
- Engineering discipline over unnecessary complexity.

---

# Current Snapshot

Architecture Baseline

`2026.08.04v14`

Capabilities

**001–011 Complete**

Version 1.1

**V11-01–V11-10 Complete**

Version 2 (Web Product Track)

**GPT Recovery RC5 locked; Reader Engagement discovery recorded; Web
Product Foundation v1 adopted; Web Walking Skeleton 01 implemented and
hosted on Render (`https://studio.ramrattan.com`); foundation fully
verified including real OpenAI, real Approve/Reject persistence, and
literal browser acceptance**

Current Objective

**See `BACKLOG.md` (canonical). Summary: (1) Manual Version 1 and
Version 1.1 Release Decisions (BL-011); (2) Web Product Track - a lean
daily-sprint operating model is now active; next Daily Sprint selects
from `BACKLOG.md`, not decided here.**

Deferred

**See `BACKLOG.md` for the full backlog, including B002 (BL-012)**

Validation

- Compileall PASS
- Repository Validation PASS
- 484 Tests PASS

Repository

- `develop`
- Clean
- Synchronized

---

# Document Information

Version

**1.1**

Last Updated

**2026-08-11**

Current Phase

**(1) Version 1.0 and Version 1.1 released (`v1.0.0`, `v1.1.0`); (2) Web
Product - foundation complete, lean delivery operating model active - see
`BACKLOG.md` for current backlog/Kanban state**
