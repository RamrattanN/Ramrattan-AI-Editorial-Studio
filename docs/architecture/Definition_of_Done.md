# Capability Definition of Done

## Purpose

A capability is complete only when the product, architecture,
implementation, validation, documentation, demonstration, and
planning artifacts agree.

Completion is not defined solely by merged code.

## 1. Product Alignment

The capability must state:

- the problem it solves,
- the Author benefit,
- the product principle it reinforces,
- the current scope,
- and explicit non-goals.

The PRD is updated when product behaviour changes.

The Product Decision Log is updated when a meaningful product
decision is made.

## 2. Author Experience

The capability must avoid unnecessary Author burden.

It should confirm:

- progressive clarification,
- no avoidable questionnaire,
- no unnecessary file-path collection,
- no unnecessary account requirement,
- clear explanation of important outputs,
- and a low-friction route to the primary outcome.

## 3. Architecture

An Architecture Decision Record is required when the capability:

- changes the system model,
- introduces a major dependency,
- changes persistence,
- changes privacy or security assumptions,
- or materially affects future implementation.

Architecture documents must explain:

- responsibilities,
- boundaries,
- dependencies,
- alternatives,
- consequences,
- and migration considerations.

## 4. Implementation

Production code must be:

- understandable,
- modular,
- typed where practical,
- provider-independent where appropriate,
- and free from hard-coded demonstration topics.

Temporary repair code must not be merged unless it has a durable
repository purpose.

## 5. Validation

The capability must pass:

```bash
python3 -m compileall -q studio tests
python3 -m unittest discover -s tests -v
python3 studio.py validate
```

Tests should validate behaviour rather than fragile line wrapping
or formatting accidents.

## 6. Documentation

Required documentation is updated before merge.

This may include:

- README
- Current Product Focus
- PRD
- Product Principles
- Studio Contract
- Glossary
- Architecture documents
- ADRs
- Roadmap
- Changelog
- Decision Log

## 7. Capability Demo

Every completed capability must include a demo document.

The demo must answer:

1. What problem existed?
2. What changed?
3. Why does it matter?
4. What can the product now do?
5. Which acceptance criteria passed?
6. What was learned?
7. What comes next?

The demo should include at least one clear example or diagram.

## 8. Project Planning

The GitHub Project must reflect:

- completed work,
- current work,
- next work,
- and explicitly deferred work.

Completed pull requests should be marked Done.

Active capability work should be marked In Progress.

## 9. Repository Hygiene

Before commit:

```bash
git add -A
git diff --cached --name-status
```

Review must confirm:

- correct paths,
- no double-nested directories,
- no accidental private files,
- no credentials,
- no temporary repair artifacts,
- and no unrelated changes.

## 10. Pull Request

The pull request must explain:

- summary,
- problem,
- changes,
- product alignment,
- Author benefit,
- validation,
- risks,
- and rollback.

Automated checks must pass before merge.

## 11. Merge and Cleanup

After merge:

- synchronize `develop`,
- delete local and remote feature branches,
- prune stale references,
- confirm the working tree is clean,
- and confirm the Kanban board is current.

## 12. Learning

Every capability should record:

> What did we learn that changed our understanding of the product?

A capability is not complete until this question has been answered.

<!-- CAPABILITY_006_DEFINITION_OF_DONE_START -->

## Capability 006 Completion Additions

Before a Version 1.0 capability is Done, confirm:

- Editorial Integrity implications are documented.
- LMHS Editorial Risk behaviour is tested where applicable.
- The capability does not knowingly disseminate false information.
- Author-facing interactions are concise.
- Related components are not silently regenerated.
- Export remains the completion fast path.
- Version 1.0 scope is not expanded accidentally.
- The Capability Demo is current.
- The GitHub Project and backlog are current.

<!-- CAPABILITY_006_DEFINITION_OF_DONE_END -->
