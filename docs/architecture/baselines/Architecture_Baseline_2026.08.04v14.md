# Architecture Baseline - 2026.08.04v14

## Status

Current delivered architecture baseline. Delivered by V11-10 (Issue #79),
closing the Version 1.1 Engineering Epic (Issue #69).

## Baseline ID

`2026.08.04v14`

## Supersedes

`2026.08.02v13`

## Reason for Revision

Record the delivered Version 1.1 Author Journey: the complete session flow
from Welcome through Complete, assembled from the ten implementation slices
V11-01 through V11-10 (Issues #70-#79, PRs #81-#91), governed by
`docs/product/Version_1_1_Author_Experience_Baseline.md`,
`docs/architecture/Version_1_1_State_Machine.md`, ADR-018, and ADR-019.

## Runtime Architecture

- `studio/author_journey.py` owns the single Author Journey orchestrator:
  Welcome, Entry Path, Studio Configuration Load, Workflow Selection,
  Editorial Source, Branding, Editorial Discovery, Editorial Plan,
  Generation, Publication Studio, Editorial Audit, Session Completion, and
  Complete. It wraps the existing Version 1.0 `EditorialSession` without
  changing that runtime, and calls `article_engine.py`, `hero_visual.py`,
  `evidence_validation.py`, `publication_package.py`, and
  `portable_editorial_project.py` as-is.
- `studio/publication_studio.py` owns the two-workspace Publication Studio,
  the Author-editable Publication Editor, Publication Content boundary,
  Editorial Review panel, and the Copy LinkedIn Publication gate
  (`CopyGateState.MATCHED` / `UNMATCHED`).
- `studio/editorial_audit.py` owns the on-demand, analysis-only Editorial
  Audit: LMHS Assessment (re-invoking the existing, unmodified
  `evidence_validation.validate_evidence()`), Editorial Drift measured
  against the fixed Generate-Once baseline, and Editorial Confidence. It
  never writes to Publication Content.
- `studio/session_completion.py` owns the Session Completion state's
  Configuration-generation prompt and assembly of the three Session
  Artifacts (Publication Package, Portable Editorial Project, and the
  optional Ramrattan AI Configuration) from the Author's live edited
  content, not the immediate post-Generation state.
- The Ramrattan AI Configuration artifact is a two-field, JSON-only,
  session-scoped preference file
  (`Ramrattan-AI-Configuration-[YYYY.MM.DDvNN].json`), distinct from and
  never merged with the Portable Editorial Project, per ADR-019.
- Resume Existing Project reuses the existing, unmodified
  `portable_editorial_project.resume_project()` mechanism as a distinct
  Entry Path branch entering Publication Studio directly, bypassing
  Configuration Load, Workflow Selection, intake, and Generation entirely.
- `Editorial Confidence` is the sole canonical Author-facing
  publication-readiness field; an Editorial Audit recomputes it in
  addition to Generation. No separate "Publication Readiness" field
  exists (see `docs/constitution/Canonical_Vocabulary.md`, Version 1.1
  Vocabulary).

## Trust and Failure Model

Generate Once remains structural: Publication Studio is entered at most
once per session, from exactly a completed Generation or a validated
Resume, and no transition re-enters Generation or Resume Validation.
Author Ownership remains structural: no rewrite, regenerate, improve,
shorten, or expand action exists anywhere in Publication Studio, under any
Editorial Audit outcome, including High or Severe. The Copy LinkedIn
Publication gate is session-owned state, not a UI convention: any Author
edit sets it unmatched; only a completed Editorial Audit sets it matched;
a High or Severe result withholds a positive Editorial Confidence and
explains the risk without disabling the action, rewriting content, or
auto-publishing. The Studio remains stateless: every session artifact is a
file delivered to the Author, and the Studio retains nothing once Complete
is reached.

## Explicit Exclusions

No Publish to Platform, Portable Author Context, user accounts, hosted
storage, persistent Author identity, multi-user collaboration, or other
Version 2 behavior is introduced. `studio/article_engine.py`,
`assets/brand/` masters, and the legacy `studio/workflow/` module remain
unmodified and protected. No release action - `main` promotion, tagging,
or GitHub Release publication - is authorized by this baseline.

## Architecture Decision

ADR-018 and ADR-019 record the durable decisions, both Accepted against
this delivery.
