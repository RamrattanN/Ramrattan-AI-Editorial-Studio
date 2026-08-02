# CLAUDE.md

Version: 1.0
Status: Active
Last Updated: 2026-08-02
Maintainer: Repository Author

# Ramrattan AI Editorial Studio

This repository is engineered around a repository-first workflow.

The repository is the authoritative source of truth.

Do not rely on prior conversations, assumptions, or historical context when repository evidence is available.

---

# Purpose

This document is a lightweight adapter for Claude Code.

It explains how Claude Code should operate within this repository.

Repository governance is defined by **AGENTS.md**.

Treat **AGENTS.md** as the authoritative engineering constitution.

This document must never duplicate, replace, or supersede repository governance.

---

# First Actions

Before proposing changes or modifying the repository, read these files in the following order:

1. AGENTS.md
2. CONTRIBUTING.md
3. docs/engineering/Capability_Delivery_Workflow.md
4. ROADMAP.md
5. docs/product/Current_Product_Focus.md
6. docs/product/PRD_v1.3.md
7. docs/architecture/Definition_of_Done.md
8. Current Architecture Baseline (latest version only)
9. Current ADR Index
10. Relevant capability documentation for the requested task

If repository documents appear to conflict, stop and report the discrepancy instead of making assumptions.

---

# Repository-First Principle

Always derive understanding from the repository before asking for clarification.

Prefer verified repository evidence over inference.

Avoid asking questions already answered by repository documentation.

Do not reconstruct repository state from conversation history.

---

# Working Model

Treat the repository as the permanent memory.

Treat conversations as temporary working context.

Whenever repository evidence and conversation differ, repository evidence takes precedence.

---

# Delivery Workflow

This repository uses delegated delivery governance.

Implementation follows four profiles:

- Start
- Publish
- Complete
- Conservative

Read **AGENTS.md** for the complete workflow.

Do not invent additional approval boundaries.

Do not skip existing approval boundaries.

---

# Authorization

Treat workflow authorization as conversation-scoped.

Never assume authorization from:

- previous chats
- previous sessions
- previous capabilities
- previous commits
- previous pull requests

Once a workflow profile has been explicitly authorized for the current delivery, continue until:

- the documented stopping boundary;
- a genuine fail-closed condition;
- or explicit Repository Author revocation.

Do not request duplicate authorization for an already authorized profile.

---

# Fail-Closed Behaviour

Stop immediately whenever:

- repository state differs from verified prerequisites;
- scope materially changes;
- repository evidence conflicts;
- GitHub state is inconsistent;
- CI fails;
- mergeability is blocked;
- a required human decision is reached.

Always explain the exact reason for stopping.

---

# Scope Discipline

Implement only the approved capability.

Do not absorb adjacent roadmap work.

Keep implementations coherent.

Prefer one well-designed implementation over multiple fragmented passes when modifying the same area of the repository.

Avoid speculative refactoring.

Avoid unrelated cleanup.

---

# Repository Standards

Preserve deterministic generation.

Keep generators and generated artifacts synchronized.

Do not install dependencies unless explicitly approved.

Do not rewrite completed capabilities.

Do not modify approved brand masters.

Keep documentation synchronized with implementation.

---

# Validation

Before publication, perform the repository validation defined by AGENTS.md.

Never bypass validation.

Never weaken tests to obtain a passing result.

Prefer fixing the implementation rather than changing validation expectations.

---

# Brand

The approved brand masters are immutable repository assets.

Do not recreate them.

Do not reinterpret them.

Do not regenerate them.

Use the canonical assets already stored in the repository.

---

# Reporting

Keep reports concise and evidence-based.

State:

- what changed;
- what was verified;
- what remains deferred;
- why execution stopped (if applicable);
- the exact next approval boundary.

Avoid unnecessary narrative.

---

# Working Style

Prefer:

- repository evidence;
- deterministic behavior;
- one coherent implementation;
- synchronized artifacts;
- concise reporting;
- engineering discipline.

Avoid:

- duplicate work;
- unnecessary repository churn;
- speculative design;
- repeated approval requests;
- rewriting unrelated documentation.

---

# Beginning Every Session

1. Read the repository.
2. Summarize the verified repository state.
3. Identify the active capability or task.
4. Confirm the current workflow profile.
5. Begin work.

Never infer repository state from conversation history alone.

Always prefer repository evidence.