# ADR-012 - Delivery Hardening

## Status

Accepted

## Date

2026-08-02

## Decision Level

D4 - Architecture

## Context

The original Capability Delivery helper could turn failed GitHub discovery
into apparent absence, treat an empty check rollup as success, ignore draft
state, select the first of multiple pull requests, and recommend merge without
complete review or mergeability evidence.

PRs #30, #31, and #33 confirmed the draft-state defect: the helper reported
`ready_to_merge` while GitHub still reported each pull request as a draft.
Remote freshness and incomplete post-merge cleanup were also not represented
as first-class evidence.

These are trust failures. A delivery recommendation must not be more certain
than the evidence used to produce it.

## Decision

Adopt a fail-closed delivery observation model.

### Discovery Results

External discovery returns one of:

- `FOUND` - exactly one complete matching artifact was verified;
- `NOT_FOUND` - a successful query confirmed zero matches;
- `UNAVAILABLE` - authentication, network, API, parsing, or required evidence
  failed; or
- `AMBIGUOUS` - more than one matching artifact was verified.

`UNAVAILABLE` and `AMBIGUOUS` block advancement. Failure is never interpreted
as absence.

### Remote Freshness

Remote-dependent recommendations require direct observation of
`origin/develop` and the feature branch. Cached remote-tracking references are
insufficient freshness evidence.

A command failure, malformed reference response, or missing remote base branch
blocks the workflow.

### Pull-Request Evidence

The helper models:

- zero, one, or multiple branch-matching pull requests;
- open, closed, and merged state;
- draft and ready-for-review state;
- review required, changes requested, and approved state;
- clean, conflicting, blocked, unknown, and unavailable mergeability;
- pull-request head identity; and
- check availability and outcomes.

A draft pull request is never ready to merge. The remote feature head must
match the pull-request head before PR recommendations advance.

### CI Evidence

An empty or missing check rollup is unavailable unless repository policy
independently proves no checks are required. This repository requires CI, so
zero checks block merge.

Check outcomes are normalized as unavailable, pending, failed, cancelled,
timed out, action required, or successful. Only successful checks can satisfy
the CI gate.

### Recovery

Merged state is observed independently from branch cleanup. The helper
recommends one recovery step at a time when checkout, local branch deletion,
remote branch deletion, baseline synchronization, or merge ancestry remains
incomplete. The helper never repeats a confirmed merge.

### Approval Boundaries

Read-only observation, validation, and CI monitoring may continue
automatically inside an authorized phase. Protected mutations retain explicit
Nilesh approval boundaries. The helper may recommend them but does not execute
them.

## CI Contract

```bash
python3 -m compileall -q studio scripts tests
python3 -m unittest discover -s tests -v
python3 studio.py validate
```

## Alternatives Considered

Optimistic defaults, open-only discovery, zero-check success, and automatic
protected mutations were rejected because each weakens verified evidence or
explicit approval.

## Consequences

Delivery recommendations cannot silently overstate external evidence, and
partial cleanup is resumable. Delivery may pause more often when evidence is
incomplete, and GitHub response-shape changes require parser maintenance.

## Architecture Baseline

Recorded by Architecture Baseline `2026.08.01v07`.
