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

`2026.08.02v13`

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

Current validation baseline:

- Compileall PASS
- Repository Validation PASS
- 324 Tests PASS

---

# Current Focus

## Active Objective

**Manual Version 1 Release**

Issue #18 and Version 1 RC1 Release Readiness are Complete. The remaining
release actions require explicit Repository Author approval:

- Repository Author release approval
- `develop`-to-`main` release promotion
- Creation of tag `v1.0.0`
- GitHub Release publication
- Release-note publication
- External announcement, if approved
- Post-release verification

No release action or additional feature work should begin unless explicitly
approved by the Repository Author.

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

1. Repository Author release approval.
2. Promote `develop` to `main` for the Version 1 release.
3. Create tag `v1.0.0` and publish the GitHub Release and release notes.
4. Publish an external announcement, if approved, and verify the release.
5. Post-RC1 Improvements.
6. B002 Brand Refinement.
7. Version 1.1 Planning.

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

`2026.08.02v13`

Capabilities

**001–011 Complete**

Current Objective

**Manual Version 1 Release**

Deferred

**B002**

Validation

- Compileall PASS
- Repository Validation PASS
- 324 Tests PASS

Repository

- `develop`
- Clean
- Synchronized

---

# Document Information

Version

**1.0**

Last Updated

**2026-08-03**

Current Phase

**Manual Version 1 Release**
