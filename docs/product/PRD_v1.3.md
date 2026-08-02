# Product Requirements Document - Version 1.3

## Product

Ramrattan AI Editorial Studio

## Status

Active Version 1.0 product baseline.

## Supersedes

PRD v1.2 as the active product definition.

Earlier PRDs remain preserved as historical records.

## Product Definition

Ramrattan AI Editorial Studio is an adaptive editorial operating
system that helps professional Authors turn evolving ideas,
sources, evidence, experience, and perspective into responsible,
publication-ready articles and 720 × 425 Hero Visuals.

## Version 1.0 Primary Outcome

A complete publication package containing:

- Hero Visual prompt
- Hero Visual - 720 × 425
- Headline
- Hook
- Insight 1
- Insight 2 when useful
- Practical Takeaway
- CTA
- Source and attribution
- Hashtags
- LinkedIn Description
- Portable Editorial Project

## Input Experience

The Author may begin with any compatible host-platform input,
including:

- URL
- Text
- Notes
- Draft
- Document
- Audio
- Video
- Portable Editorial Project

The Author should not need to choose a technical intake mode.

## Editorial Integrity

The Editorial Integrity Pipeline must run before publication
recommendation.

It must:

- assess source quality,
- verify material claims,
- distinguish fact from opinion,
- identify outdated information,
- assess originality and attribution,
- identify harmful or deceptive requests,
- and assign LMHS Editorial Risk.

## LMHS Editorial Risk

Risk levels are:

- Low
- Moderate
- High
- Severe

Percentages are not used.

## False Information

The Studio must not knowingly disseminate materially false,
fabricated, deceptive, or dangerously misleading information.

## Author Challenge

When evidence does not support the Author's assumption, the Studio
should explain the evidence and offer a more defensible direction.

## Options and Recommendations

When appropriate, the Studio should present three strong options.

Each option includes concise rationale.

The Studio's recommendation appears after all options and is based
on the Author's material, thesis, audience, and objective.

Every option set includes a way for the Author to provide their own
answer.

## Interaction Style

The Studio should:

- infer before asking,
- ask only focused questions,
- explain questions only when the reason is not obvious,
- remain proactively helpful but concise,
- avoid endless recommendation loops,
- and never pretend to remember unavailable information.

## Host Context

The Studio may use reliable host-platform context when available,
including a preferred name or writing preference.

The Product must remain correct when host context is unavailable.

## Intelligent Dependency Management

A requested change updates only the requested component.

The Studio may identify related components and ask whether the
Author wants them updated.

It must not silently regenerate them.

## Publication Completion

The Studio presents:

- the Hero Visual,
- the complete structured text,
- the Editorial Risk result,
- and the completion actions.

The first completion action is:

> Export the publication package

Secondary actions are:

- Review or improve a component
- Download the Portable Editorial Project only
- Start a new Editorial Project

## Portable Projects

Portable Editorial Projects preserve context required for future
resumption.

They use:

```text
Ramrattan-Editorial-Project_<Article-Slug>_YYYY.MM.DDvNN.md
```

Generated filenames must not exceed 255 characters.

## Temporal Integrity

Resumed projects should be reviewed for time-sensitive evidence
before republication.

## Version 1.0 Exclusions

Version 1.0 excludes:

- Carousels
- Hosted Author Library
- Hosted accounts
- Cloud synchronization
- Team workspaces
- Direct automatic publishing
- Analytics dashboards
- Persistent Product-managed Author profiles
- Multi-tenant storage
- Subscription implementation

## Success Measures

- Time to first publication package
- Low Author effort
- LMHS assessment quality
- Fact-verification quality
- Author confidence to publish
- Preservation of Author perspective
- Focused revision success
- Export success
- Project resume success
- Hero Visual compliance
- Publication-package completeness

<!-- CAPABILITY_006A_PRD_START -->

## Constitutional Authority

Version 1.0 implementation shall conform to:

- the Constitution,
- Human Collaboration Model,
- Author Journey,
- Editor Journey,
- Editor Charter,
- Reader Experience Principles,
- Editorial Behaviour Standard,
- Editorial Language Framework,
- Editorial Fingerprint,
- and Canonical Editorial Session.

Editorial Confidence is the primary Author-facing readiness
conclusion.

LMHS Editorial Risk remains the internal assessment model.

<!-- CAPABILITY_006A_PRD_END -->

<!-- CAPABILITY_007_PRD_START -->

## Capability 007 Runtime Requirements

Version 1.0 shall provide an Editorial Workspace that:

- explains supported input formats,
- recognises natural Author input,
- completes Understanding your input,
- completes Assessing your sources,
- keeps later stages visible but pending,
- and does not falsely imply evidence verification.

## Optional Hero Visual Identity Assets

The Author may optionally provide:

- logo,
- headshot,
- or both.

Requirements:

- brand-neutral remains the default,
- rights confirmation is required,
- headshot recognisability should be preserved,
- assets remain Author-controlled,
- no storage path is required,
- and resume remains possible without the original asset.

<!-- CAPABILITY_007_PRD_END -->

<!-- CAPABILITY_008_PRD_START -->

## Capability 008 Requirements

The Product shall:

- maintain one Editorial Intent per Editorial Session;
- classify new material as Aligned, Related, Diverging, Separate
  Intent, or Ambiguous;
- recommend a new Editorial Session for separate publication
  objectives;
- never silently merge unrelated sources;
- never silently expand scope;
- ask one concise clarification question when ambiguity blocks safe
  progress;
- preserve approved Publication Package components;
- distinguish Workspace State from Stage State;
- support pause, resume, cancel, abort, complete, and archive;
- preserve work and provenance after abort;
- and present Editorial Guidance rather than internal engine language
  to the Author.

<!-- CAPABILITY_008_PRD_END -->
