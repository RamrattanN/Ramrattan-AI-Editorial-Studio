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

<!-- CAPABILITY_006A_DEFINITION_OF_DONE_START -->

## Constitutional Impact Review

Before a significant capability is Done, answer:

- Does this alter the Constitution?
- Does this alter the Human Collaboration Model?
- Does this alter the Editor Charter?
- Does this alter Reader Experience Principles?
- Does this alter the Canonical Editorial Session?
- Does this alter Editorial Confidence behaviour?
- Does this alter approved component preservation?
- Does this alter CTA or editorial language behaviour?

If yes:

- document the reason,
- update constitutional documents first,
- update the Decision Log,
- create or amend an ADR,
- update complementary documents,
- update validation,
- and obtain deliberate review.

Version 1.0 implementation should not expand foundational philosophy
without implementation evidence.

<!-- CAPABILITY_006A_DEFINITION_OF_DONE_END -->

<!-- CAPABILITY_007_DEFINITION_OF_DONE_START -->

## Capability 007 Completion Additions

Before Capability 007 is Done, confirm:

- Editorial Workspace terminology is canonical.
- Editorial Intake is not presented as the complete Workspace.
- Supported inputs are described honestly.
- Stage 1 and Stage 2 are executable.
- Stages 3 through 5 remain pending.
- Source assessment does not claim verification.
- Identity assets remain optional.
- Rights confirmation is enforced.
- Brand-neutral remains the default.
- Missing identity assets do not block resume.
- Runtime and documentation tests pass.

<!-- CAPABILITY_007_DEFINITION_OF_DONE_END -->

<!-- CAPABILITY_DELIVERY_DEFINITION_OF_DONE_START -->

## Delivery Workflow Completion

A capability is not Done until:

- local validation passes;
- GitHub planning is synchronized;
- all intended files are staged;
- the capability commit exists;
- the feature branch is pushed;
- the pull request exists;
- CI passes;
- the pull request is merged;
- the local feature branch is deleted;
- the remote feature branch is deleted;
- the repository is on `develop`;
- local `develop` matches `origin/develop`;
- the working tree is clean;
- and the merge commit is visible.

Use `docs/engineering/Capability_Delivery_Workflow.md` as the
governing procedure.

<!-- CAPABILITY_DELIVERY_DEFINITION_OF_DONE_END -->

<!-- CAPABILITY_008_DEFINITION_OF_DONE_START -->

## Capability 008 Completion Additions

Confirm:

- one Editorial Intent is maintained per session;
- related material may continue;
- separate publication objectives recommend a new session;
- no silent scope expansion occurs;
- ambiguous intent produces one concise clarification question;
- approved components remain protected;
- Workspace State and Stage State remain distinct;
- abort preserves work and provenance;
- Author-facing language uses Editorial Guidance;
- runtime tests pass;
- documentation tests pass;
- and repository validation passes.

<!-- CAPABILITY_008_DEFINITION_OF_DONE_END -->

<!-- CAPABILITY_009_DEFINITION_OF_DONE_START -->

## Capability 009 Completion Additions

Confirm:

- Article generation preserves approved Editorial Intent;
- evidence used by the article has explicit attribution;
- High and Severe Editorial Risk block article and package creation;
- the provider boundary cannot bypass deterministic integrity checks;
- every Capability 009 textual component is validated;
- rendered Hero Visual and Portable Editorial Project outputs remain
  explicitly deferred;
- no new Author-facing workflow, collaboration feature, orchestration
  API, persistence model, or later-capability behavior is introduced;
- the Capability 009 demo is current; and
- complete repository validation passes.

<!-- CAPABILITY_009_DEFINITION_OF_DONE_END -->

<!-- CAPABILITY_010_DEFINITION_OF_DONE_START -->

## Capability 010 Completion Additions

Confirm:

- the approved Capability 009 Hero Visual prompt is preserved;
- provider-specific behavior remains behind `HeroVisualProvider`;
- ready output is a validated 720 × 425 PNG with provenance;
- deterministic generation is offline and repeatable;
- malformed, unsupported, failed, invalid, and blocked states remain distinct;
- no failed or unvalidated artifact is reported ready;
- Publication Package attachment does not regenerate or change textual content;
- already attached results are protected from silent replacement;
- approved brand masters remain unchanged and are not Hero Visual inputs;
- no Portable Project, workspace, collaboration, orchestration, UI, publishing
  automation, release packaging, or Version 2 behavior is introduced;
- the Capability 010 demo is current; and
- complete repository validation passes.

<!-- CAPABILITY_010_DEFINITION_OF_DONE_END -->
