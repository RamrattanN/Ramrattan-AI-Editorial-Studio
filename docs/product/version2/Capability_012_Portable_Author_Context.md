# Capability 012 - Portable Author Context

**Status:** Version 2 Candidate  
**Classification:** Product Enhancement  
**Architecture:** Stateless and Author-Controlled  
**Governance Status:** Informative - Not Yet Approved for Implementation

## Vision

Reduce repetitive editorial setup while preserving the Studio's stateless
architecture and the principle that the Author owns the message.

Rather than maintaining server-side user profiles, the Editorial Studio may
support portable, Author-controlled context that can move between sessions.

## Problem Statement

Version 1 begins every editorial engagement as a new interaction.

This protects privacy and architectural simplicity, but returning Authors may
need to answer the same preference questions repeatedly.

Examples include:

- preferred audience
- geographic focus
- editorial tone
- preferred content format
- CTA style
- Hero Visual style
- hashtag strategy
- evidence expectations
- preferred publication destination

These preferences may remain stable across multiple sessions.

## Objectives

The capability should:

- remain stateless
- require no application-specific login
- require no user database
- require no server-side profile storage
- remain portable
- remain transparent
- remain Author-controlled
- require confirmation before applying defaults
- reduce repeated questions during later sessions

## Proposed Solution

Introduce a Portable Author Context.

A Portable Author Context is a compact, versioned token representing approved
editorial defaults.

The token may be supplied when a session begins, including through a trusted
URL.

The Studio interprets the token, presents the resulting preferences to the
Author, and applies them only after confirmation.

The Studio stores no persistent Author profile.

## Illustrative URL

```text
https://chatgpt.com/g/<editorial-studio>?ctx=<portable-author-context>
```

The exact URL and integration mechanism remain subject to platform capability,
security review, and Version 2 architecture.

## Candidate Context Fields

A Portable Author Context may contain:

- preferred audience
- preferred region
- preferred tone
- preferred publication format
- preferred CTA style
- preferred Hero Visual style
- preferred hashtag strategy
- editorial evidence threshold
- preferred publication platform
- optional supported feature flags

## Excluded Data

A Portable Author Context must not contain:

- passwords
- authentication credentials
- billing information
- private keys
- unpublished editorial work
- unnecessary personal information
- hidden behavioural tracking data

A first name may be used only when supplied or otherwise made available through
a verified platform capability. The design must not assume that the signed-in
platform identity is always available to the Studio.

## Session Workflow

1. The Author opens a trusted context link.
2. The Studio validates and interprets the token.
3. The Studio displays the interpreted preferences.
4. The Author confirms or changes the preferences.
5. The editorial workflow begins.
6. The Publication Package is produced.
7. The session-specific context is discarded.

## Example Author Experience

The Studio may present:

> Your usual editorial defaults are:
>
> - Audience: Managers and Practitioners
> - Region: Global
> - Format: LinkedIn Article
> - Tone: Professional
> - CTA: Binary
> - Hero Visual: Photorealistic Editorial
>
> Continue with these defaults?

The Author may accept, reject, or modify any value.

## Privacy Principles

- The Studio stores no Author profile.
- The Author owns the context.
- The context travels with the Author.
- No persistent identity database is required.
- No hidden personalization is permitted.
- Context must be visible and confirmable before use.

## Security Requirements

The Portable Author Context should:

- be versioned
- be compact
- detect tampering
- support schema evolution
- reject malformed or unsupported versions
- avoid readable sensitive URL parameters
- fail closed when integrity cannot be verified

Signing, encryption, expiry, and replay protection require architectural review
before implementation.

## Architectural Benefits

This approach:

- preserves stateless architecture
- avoids application account management
- avoids server-side profile storage
- reduces repeated questioning
- supports repeat-session efficiency
- supports multiple editorial contexts
- aligns with the Portable Editorial Project philosophy
- preserves explicit Author approval

## Multiple Contexts

An Author may maintain more than one context, such as:

- Executive Leadership
- Board Advisory
- Technical Practitioner
- AI Governance
- Internal Communications
- Global Editorial
- LinkedIn Article
- LinkedIn Carousel

Each context represents a different starting configuration rather than a stored
identity.

## Relationship to Version 1

Capability 011 introduced the Portable Editorial Project.

Capability 012 extends the same portability principle to approved editorial
preferences.

Together, they support an architecture in which both project state and
editorial defaults travel with the Author rather than being retained by the
platform.

## Relationship to Publishing Integrations

Portable Author Context may later supply default publication destinations or
format preferences to a Publish to Platform capability.

It does not itself publish content.

Every publishing action remains subject to explicit Author review and approval.

## Non-Goals

This capability does not introduce:

- application-managed user accounts
- server-side Author profiles
- cloud preference storage
- behavioural tracking
- invisible memory
- automatic publishing
- automatic editorial approval
- Version 2 implementation authorization

## Open Questions

Before implementation, Version 2 architecture must determine:

- supported token encoding
- signing approach
- whether encryption is required
- token expiry behaviour
- schema-version migration
- URL-length limits
- supported ChatGPT or platform entry mechanisms
- token regeneration and revocation
- treatment of copied or shared links
- interaction with Portable Editorial Projects
- interaction with Publish to Platform adapters

## Candidate Acceptance Boundary

Capability 012 should not be considered ready for implementation until:

- the Version 2 product boundary is approved
- the token threat model is documented
- the platform entry mechanism is verified
- privacy and security constraints are accepted
- an ADR defines ownership and failure behaviour
- deterministic validation coverage is designed
