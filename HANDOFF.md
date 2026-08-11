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

**1. Manual Version 1 and Version 1.1 Release Decisions**

Issue #18 and Version 1 RC1 Release Readiness are Complete. Version 1.1
(V11-01 through V11-10, Issue #69 Epic) is also now Complete on `develop`.
Neither version has been promoted to `main`; both remaining release
decisions require explicit Repository Author approval:

- Repository Author release approval, for Version 1.0, Version 1.1, or both
- `develop`-to-`main` release promotion
- Creation of the applicable release tag(s)
- GitHub Release publication
- Release-note publication
- External announcement, if approved
- Post-release verification

No release action or additional feature work should begin unless explicitly
approved by the Repository Author.

**2. Web Product - Development Deployment and Browser Acceptance**

Web Walking Skeleton 01 (PR #111) is implemented; real OpenAI Editorial
Direction generation is now verified (2026-08-10) - `OPENAI_API_KEY` is
configured locally, and two real end-to-end Editorial Direction requests
have been executed, approved, and persisted through the actual
application path. Remaining sequence: validate in a real browser;
configure a development deployment (Render recommended, not yet
configured); obtain a hosted development URL. See `ROADMAP.md` ("Version 2
Checkpoint") and `docs/product/version2/Web_Product_Foundation_v1.md`
(Section 13) for full detail. Web Walking Skeleton 02 (Editorial Plan +
Draft) is the next vertical slice and has not started.

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

1. Repository Author release approval for Version 1.0, Version 1.1, or both.
2. Promote `develop` to `main` for the approved release(s).
3. Create the applicable release tag(s) and publish the GitHub Release and release notes.
4. Publish an external announcement, if approved, and verify the release.
5. Post-RC1 Improvements.
6. B002 Brand Refinement.
7. ~~Configure `OPENAI_API_KEY` and verify real OpenAI Editorial Direction
   generation for Web Walking Skeleton 01~~ - done (2026-08-10).
8. Configure a development deployment (Render recommended) and obtain a
   hosted development URL; validate in a real browser.
9. Web Walking Skeleton 02 - Editorial Plan + Draft (not started).

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
5. Review the active GitHub issue.
6. Identify the active delivery profile.
7. Begin only the approved engineering objective.

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
Product Foundation v1 adopted; Web Walking Skeleton 01 implemented; real
OpenAI Editorial Direction foundation verified**

Current Objective

**(1) Manual Version 1 and Version 1.1 Release Decisions; (2) Web Product -
Development Deployment and Browser Acceptance**

Deferred

**B002**

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

**2026-08-10**

Current Phase

**(1) Manual Version 1 and Version 1.1 Release Decisions; (2) Web Product -
Development Deployment and Browser Acceptance**
