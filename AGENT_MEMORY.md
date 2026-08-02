# Agent Memory

This document captures engineering experience gained while working on the
Ramrattan AI Editorial Studio.

Unlike AGENTS.md, this file is expected to evolve over time.

---

# Collaboration Lessons

## One verified step

Nilesh prefers one verified step at a time.

Do not provide multiple future commands unless explicitly requested.

After each verified step:

- inspect repository state
- determine the next safe transition
- recommend only that transition

---

## Repository first

Conversation history can become stale.

Before suggesting actions:

- inspect repository state
- inspect git state
- inspect workflow state

Continue from the verified state rather than restarting a workflow.

---

## Avoid repeated work

Never ask the Author to repeat work that has already been completed.

Examples:

- rerunning successful validation
- recreating an existing Pull Request
- restaging committed files
- repeating GitHub synchronization

Always acknowledge completed work and continue.

---

# Repository Conventions

## Capability delivery

The repository uses:

scripts/capability_delivery.py

as the canonical state machine.

Use it to determine the next workflow state instead of reconstructing the workflow manually.

---

## Bootstrap architecture

Generated runtime files must remain synchronized with their bootstrap generators.

Repairs must be applied to:

- runtime implementation
- bootstrap generator

Then regenerate and validate.

---

## Validation

Validation is expected before recommending Commit.

Repository validation consists of:

- compileall
- unittest
- studio.py validate

If any stage fails:

repair before continuing.

---

# GitHub Workflow

GitHub Project state should remain synchronized with repository progress.

Typical sequence:

Feature work

↓

Validation

↓

Project synchronization

↓

Commit

↓

Push

↓

Pull Request

↓

CI

↓

Merge

↓

Return to develop

↓

Project completion

---

# Engineering Preferences

Prefer:

- deterministic generation
- repository inspection
- reproducible workflows
- constitutional governance
- explicit workflow state
- small safe transitions

Avoid:

- assumptions
- speculative instructions
- duplicated effort
- hidden workflow state

---

# Lessons Learned

## Capability 008

Related source material should preserve Editorial Intent.

When runtime behavior changes, update bootstrap generation immediately to prevent regeneration from undoing fixes.

Repository state should always take precedence over conversation history.

The Author values minimizing copy-and-paste overhead and prefers the agent to carry the workflow context.

---

# Future Entries

Append new lessons rather than rewriting history.

Date each significant lesson.

Keep observations concise and actionable.

<!-- CAPABILITY_008A1_MEMORY_GOVERNANCE_START -->

# Authority and Lifecycle

`AGENT_MEMORY.md` is advisory. It records engineering experience but never
overrides the Constitution, Canonical Vocabulary, accepted ADRs, the
current architecture baseline, the Capability Delivery Workflow,
`AGENTS.md`, or `CONTRIBUTING.md`.

This file must not define current repository status or silently create
normative policy.

Maintain it chronologically:

- append dated lessons rather than rewriting history;
- annotate a correction when an earlier lesson is no longer reliable;
- promote a normative lesson into its authoritative governance document;
- keep repository and GitHub state in their designated current-status
  records; and
- keep entries concise, evidence-based, and actionable.

<!-- CAPABILITY_008A1_MEMORY_GOVERNANCE_END -->
