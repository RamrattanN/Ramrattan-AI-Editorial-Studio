# ADR-007 - Implement Editorial Workspace Intake Runtime

## Status

Accepted

## Date

2026-08-01

## Context

The Constitutional Freeze defines the complete Author, Editor, and
Reader relationship, but the repository still requires an
executable beginning to the Canonical Editorial Session.

The Author must be able to provide natural material without
navigating a technical intake wizard.

Version 1.0 must also support optional logo and headshot assets
without weakening:

- brand-neutral defaults,
- stateless operation,
- Author ownership,
- privacy,
- or project resumption.

## Decision

Implement the Editorial Workspace as the Author-facing environment.

Implement Editorial Intake as the first capability within that
Workspace.

Capability 007 implements:

1. Understanding your input
2. Assessing your sources

## Canonical Vocabulary

Adopt:

- Editorial Workspace - complete Author-facing environment
- Editorial Intake - first capability within the Workspace
- Identity Asset - optional Author-supplied logo or headshot

## Identity Assets

Identity assets:

- remain optional,
- require rights confirmation,
- do not replace brand-neutral defaults,
- do not require Product-managed storage,
- and do not block resume when absent.

## Source Assessment Boundary

Capability 007 provides initial source assessment.

It must not imply full evidence verification.

## Consequences

### Positive

- Creates the first runnable Canonical Editorial Session behaviour
- Reduces Author classification effort
- Establishes consistent Workspace language
- Supports future Hero Visual personalisation
- Preserves stateless product architecture
- Creates a testable boundary before evidence validation

### Costs

- Requires conservative source-quality language
- Requires host-platform capability awareness
- Requires identity-asset rights confirmation
- Requires later integration with evidence validation

## Alternatives Rejected

### Require the Author to Select an Input Type

Rejected because the Editor should infer before asking.

### Store Identity Assets Automatically

Rejected because Version 1.0 is stateless by default.

### Treat Source Assessment as Verification

Rejected because source identity and apparent quality do not prove
factual accuracy.
