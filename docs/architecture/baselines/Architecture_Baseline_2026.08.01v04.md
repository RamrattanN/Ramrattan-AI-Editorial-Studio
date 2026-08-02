# Architecture Baseline - 2026.08.01v04

## Status

Current engineering delivery baseline.

## Baseline ID

```text
2026.08.01v04
```

## Baseline Family

```text
2026.08.01
```

## Supersedes

```text
2026.08.01v03
```

## Reason for Revision

Establish the Capability Delivery Workflow as the repeatable
engineering process for all subsequent capabilities.

## Additions

This baseline adds:

- state-aware delivery guidance,
- exact command resolution,
- branch-existence detection,
- partial-apply recovery requirements,
- complete Git porcelain handling,
- duplicate issue prevention,
- Project propagation retries,
- pull-request discovery,
- CI gating,
- merge cleanup,
- and return-to-`develop` verification.

## Engineering Rule

A capability is not complete when code is committed.

It is complete when:

- the pull request is merged,
- the feature branch is removed,
- `develop` is current,
- the working tree is clean,
- repository validation passes,
- and GitHub planning agrees.

## Workflow Authority

`docs/engineering/Capability_Delivery_Workflow.md` is the active
engineering delivery standard.

## Constitutional Impact

This baseline does not change the Product Constitution.

It operationalizes the existing principles of:

- trust,
- consistency,
- transparency,
- stewardship,
- and deliberate refinement.
