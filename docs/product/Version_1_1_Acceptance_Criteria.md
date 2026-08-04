# Version 1.1 Acceptance Criteria

## Status

Proposed - pending delivery. Revised per Architecture Review Board findings
dated 2026-08-03, and further revised to finalize criteria for the Editorial
Audit Gate and Resume Existing Project decisions. No criterion in this
document is contingent.

## Purpose

This document translates
`docs/product/Version_1_1_Author_Experience_Baseline.md` and
`docs/architecture/Version_1_1_State_Machine.md` into atomic, testable
criteria suitable for direct implementation by an engineer or a coding agent.

## How to Read This Document

Each criterion has a unique identifier, a single MUST or MUST NOT statement,
and, where useful, a reference to the state or artifact it governs. A
criterion is atomic: it tests exactly one behaviour. A criterion is testable:
it can be verified by inspection, automated test, or direct observation
without further interpretation. Criteria are grouped by the session stage or
concern they govern, in the order defined by the Author Journey.

Every criterion in this document is subordinate to
`docs/architecture/adr/ADR-018-author-ownership-and-publication-studio.md`
and to the Guiding Principles recorded in the Baseline. Where an
implementation choice would satisfy a criterion here while violating a
Guiding Principle, the Guiding Principle governs and the criterion must be
corrected.

## Entry Path

**AC-ENTRY-1.** The Studio MUST present exactly two choices at Entry Path:
Start New Publication and Resume Existing Project.

**AC-ENTRY-2.** Selecting Start New Publication MUST transition to
Configuration Load.

**AC-ENTRY-3.** Selecting Resume Existing Project MUST transition to Resume
Validation.

**AC-ENTRY-4.** Resume Validation MUST validate the supplied Portable
Editorial Project using the existing Version 1.0 validation, deserialization,
`EditorialSession.resume()`, and Temporal Integrity review behaviour,
unmodified by this document.

**AC-ENTRY-5.** If Resume Validation succeeds, the session MUST transition
directly to Publication Studio with the project's approved content restored,
bypassing Configuration Load, Workflow Selection, Editorial Source, Branding,
Editorial Discovery, Editorial Plan, and Generation.

**AC-ENTRY-6.** If Resume Validation fails, the Studio MUST explain that the
project cannot be resumed and MUST transition back to Entry Path. It MUST NOT
proceed into Start New Publication automatically.

**AC-ENTRY-7.** Resume Validation MUST NOT read, apply, or be influenced by a
Ramrattan AI Configuration. Configuration Load MUST NOT be reachable from the
Resume Existing Project path.

**AC-ENTRY-8.** Configuration Load MUST NOT be reachable from any state other
than Entry Path's Start New Publication choice.

## Studio Configuration

**AC-CONFIG-1.** The Studio MUST offer the Author the option to load a
configuration file when Configuration Load is reached, on the Start New
Publication path only.

**AC-CONFIG-2.** The Studio MUST accept a configuration file whose filename
matches the pattern `Ramrattan-AI-Configuration-[YYYY.MM.DDvNN].json`.

**AC-CONFIG-3.** The Studio MUST reject, with an explicit and specific
message, a configuration file that does not match the supported filename
pattern or supported content structure.

**AC-CONFIG-4.** Loading a configuration file MUST restore publication
preferences for the current session only.

**AC-CONFIG-5.** Loading a configuration file MUST NOT restore editorial
content, evidence, source material, or Portable Editorial Project state.

**AC-CONFIG-6.** The Studio MUST NOT reject a configuration file solely
because of its age.

**AC-CONFIG-7.** The Studio MUST NOT persist a loaded configuration file, or
any of its contents, beyond the session in which it was loaded.

**AC-CONFIG-8.** Skipping Configuration Load MUST proceed directly to
Workflow Selection using Studio defaults, with no error or warning state.

**AC-CONFIG-9.** At Session Completion, the Studio MUST present the prompt
offering to generate a Ramrattan AI Configuration from the current session.

**AC-CONFIG-10.** If the Author accepts the Session Completion prompt, the
Studio MUST generate a configuration file matching the supported filename
pattern.

**AC-CONFIG-11.** If the Author declines the Session Completion prompt, the
session MUST proceed to Complete without generating a configuration file and
without an error state.

**AC-CONFIG-12.** The Studio MUST NOT retain a copy of a generated
configuration file after it has been delivered to the Author.

**AC-CONFIG-13.** A Ramrattan AI Configuration MUST NOT contain editorial
content, evidence, source material, or Portable Editorial Project data.

**AC-CONFIG-14.** A Ramrattan AI Configuration MUST contain exactly two
fields: the preferred Workflow mode, and the Branding preference last used.
It MUST NOT contain any field beyond these two, including any field from the
candidate preference schema described in
`docs/product/version2/Capability_012_Portable_Author_Context.md`.

**AC-CONFIG-15.** A Ramrattan AI Configuration MUST NOT embed branding asset
files (logo, headshot, or other supplied material). It records the type of
branding preference only.

**AC-CONFIG-16.** Loading a configuration MUST pre-select the Workflow
Selection choice without bypassing the Workflow Selection state; the Author
MUST be able to change the pre-selected value.

**AC-CONFIG-17.** Loading a configuration MUST show the carried Branding
preference for confirmation, change, or clearing at the Branding state; it
MUST NOT be applied without being shown.

## Workflow Selection

**AC-WORKFLOW-1.** The Studio MUST offer exactly two workflow modes at
Workflow Selection: Guided Workflow and Express Workflow.

**AC-WORKFLOW-2.** The selected workflow mode MUST NOT change which states
are visited or which approvals are required, as defined in
`docs/architecture/Version_1_1_State_Machine.md`.

**AC-WORKFLOW-3.** Under Express Workflow, Editorial Source and Branding MUST
be presented on one combined screen. No other pair of states MAY be combined
in either workflow mode; Editorial Discovery and Editorial Plan MUST each
remain their own screen under both Guided and Express Workflow.

**AC-WORKFLOW-4.** Under Express Workflow, the Studio MUST NOT bypass the
Editorial Discovery approval or the Editorial Plan approval.

**AC-WORKFLOW-5.** Under Express Workflow, the Studio MUST NOT infer Branding
from Editorial Source, even when both are presented on a combined screen.

**AC-WORKFLOW-6.** If a Ramrattan AI Configuration was loaded, the combined
Editorial Source/Branding screen under Express Workflow MUST show the carried
Branding preference for confirmation; it MUST NOT apply that preference
without displaying it.

## Editorial Source

**AC-SRC-1.** The Studio MUST accept Editorial Source material in at least
the following forms: URL, article, document, research material, topic, or
notes.

**AC-SRC-2.** From supplied Editorial Source material, the Studio MUST infer
editorial intent, audience, platform, and desired outcome.

**AC-SRC-3.** Inferred editorial intent, audience, platform, and desired
outcome MUST be presented to the Author for confirmation before Generation
occurs.

**AC-SRC-4.** The Studio MUST NOT begin Generation using an inference that
has not been confirmed at Editorial Discovery.

## Branding

**AC-BRD-1.** The Studio MUST ask whether the publication should reflect
personal or business branding.

**AC-BRD-2.** The Studio MUST accept branding material in at least the
following forms: website, logo, professional headshot, brand colours, brand
guide, presentation, previous Hero Visual, or other visual references.

**AC-BRD-3.** The Studio MUST NOT derive a branding decision from Editorial
Source material under any circumstance.

**AC-BRD-4.** If no branding material is supplied, the Studio MUST use its
professional Studio Theme.

**AC-BRD-5.** The Branding state MUST NOT accept Editorial Source content as
an input parameter.

## Editorial Discovery

**AC-DISC-1.** The Studio MUST present the confirmed editorial intent,
audience, platform, desired outcome, and Branding decision together, as a
single reviewable understanding.

**AC-DISC-2.** The Author MUST be able to approve the presented
understanding, request Editorial Source refinement, or request Branding
refinement.

**AC-DISC-3.** Requesting Editorial Source refinement MUST return the session
to the Editorial Source state without discarding previously supplied Branding
material.

**AC-DISC-4.** Requesting Branding refinement MUST return the session to the
Branding state without discarding previously supplied or inferred Editorial
Source material.

**AC-DISC-5.** The Studio MUST NOT propose an Editorial Plan until Editorial
Discovery has been approved.

## Editorial Plan

**AC-PLAN-1.** The proposed Editorial Plan MUST include a Headline, a Hook,
Key Insights, a Practical Takeaway, and a Call to Action.

**AC-PLAN-2.** The Author MUST be able to approve the plan or request
revision.

**AC-PLAN-3.** Requesting revision MUST keep the session in the Editorial
Plan state and MUST NOT trigger Generation.

**AC-PLAN-4.** The Studio MUST NOT begin Generation without an approved
Editorial Plan.

## Generation

**AC-GEN-1.** Publication Studio MUST be entered at most once per session.

**AC-GEN-2.** Generation MUST use only the approved Editorial Plan, the
confirmed Editorial Discovery understanding, and the Branding decision as
inputs.

**AC-GEN-3.** After Generation completes, the session MUST transition
directly to Publication Studio.

**AC-GEN-4.** No state reachable from Publication Studio MAY transition back
to the Generation state within the same session.

**AC-GEN-5.** If Generation is blocked because the approved plan would
produce High or Severe Editorial Risk, the session MUST transition to
Editorial Plan with an explicit explanation, and MUST NOT enter Publication
Studio.

**AC-GEN-6.** If Generation fails for a reason unrelated to Editorial Risk,
the session MUST transition to Editorial Plan with an explicit explanation
distinguishing the failure from a risk block, and MUST NOT enter Publication
Studio.

**AC-GEN-7.** A blocked or failed Generation attempt MUST NOT count toward
the once-per-session limit in AC-GEN-1; only a completed Generation that
enters Publication Studio does.

## Publication Studio Structure

**AC-PSTUDIO-1.** Publication Studio MUST present two workspaces: a left
workspace for the Hero Visual and a right workspace for the Publication
Editor.

**AC-PSTUDIO-2.** The left workspace MUST display the generated Hero Visual
and MUST offer copy, save, and download actions.

**AC-PSTUDIO-3.** Publication Studio MUST present the Editorial Review panel
as a distinct element from the Publication Editor, preferably collapsible.

## Publication Editor

**AC-EDITOR-1.** The Publication Editor MUST be fully editable by the Author,
including Headline, Hook, Body, CTA, Hashtags, Formatting, Mentions, and
Links.

**AC-EDITOR-2.** The Publication Editor MUST NOT contain a rewrite,
regenerate, improve, shorten, or expand action, or any control with
equivalent effect.

**AC-EDITOR-3.** The Studio MUST NOT modify Publication Editor content except
as a direct result of an explicit Author edit.

**AC-EDITOR-4.** The Publication Editor MUST provide exactly one Studio
action: Copy LinkedIn Publication.

**AC-EDITOR-5.** The Copy LinkedIn Publication action MUST copy only the
Author's current Publication Content, exactly as displayed, with no Editorial
Review content included.

**AC-EDITOR-6.** Copy LinkedIn Publication MUST be disabled unless the Copy
LinkedIn Publication gate defined in Editorial Audit is matched.

## Publication Content

**AC-CONTENT-1.** The Publication Editor MUST display only Publication
Content: Headline, Hook, Article, CTA, Hashtags when present, and LinkedIn
Description when present.

**AC-CONTENT-2.** If Hashtags are absent, the Publication Editor MUST omit
the Hashtags section entirely rather than display an empty-state message.

**AC-CONTENT-3.** If a LinkedIn Description is absent, the Publication Editor
MUST omit that section entirely rather than display an empty-state message.

**AC-CONTENT-4.** The Publication Editor MUST NOT render any placeholder text
of the form "No Sources," "No Mentions," "No Hashtags," or an equivalent
empty-state message for any optional section.

## Editorial Review

**AC-REVIEW-1.** The Editorial Review panel MUST include Editorial
Confidence, Editorial Risk, Sources, Suggested Mentions, Branding Summary,
and Session Summary.

**AC-REVIEW-2.** Editorial Review content MUST NOT be included in the Copy
LinkedIn Publication action or in any other export of Publication Content.

**AC-REVIEW-3.** Editorial Confidence and Editorial Risk within Editorial
Review MUST reflect the result of the most recent Generation or, if one has
been requested, the most recent Editorial Audit. They MUST NOT be
recalculated continuously as the Author edits.

**AC-REVIEW-4.** Editorial Review MUST visibly indicate that its Editorial
Confidence and Editorial Risk values may not reflect edits made since the
last computation (for example, by timestamping the assessment or labelling
it "as of last audit"). It MUST NOT imply continuous freshness it does not
have.

## Editorial Audit

**AC-AUDIT-1.** The Author MUST be able to request an Editorial Audit at any
point while in the Author Editing state.

**AC-AUDIT-2.** An Editorial Audit MUST produce an LMHS Assessment, an
Editorial Drift assessment, and an updated Editorial Confidence.

**AC-AUDIT-3.** An Editorial Audit MUST NOT modify Publication Content.

**AC-AUDIT-4.** After an Editorial Audit completes, the session MUST return
to the Author Editing state automatically.

**AC-AUDIT-5.** The Author MUST be able to request more than one Editorial
Audit within a single session, with intervening edits between requests.

**AC-AUDIT-6.** Editorial Drift MUST be assessed against the approved
Editorial Plan and the evidence confirmed at Editorial Discovery, not against
an arbitrary or undefined baseline.

**AC-AUDIT-7.** Reaching Session Completion MUST NOT require that an
Editorial Audit has been requested. The Editorial Audit Gate defined below
governs Copy LinkedIn Publication only, not Session Completion, the
Publication Package, or the Portable Editorial Project.

### The Editorial Audit Gate

**AC-AUDIT-8.** Author Editing MUST track whether the most recent Editorial
Audit result matches the currently displayed Publication Content, in exactly
two states: matched or unmatched.

**AC-AUDIT-9.** On every entry into Author Editing — from Generation, from
Resume Validation, or from Editorial Audit — the gate MUST start or remain
unmatched until a completed Editorial Audit sets it to matched, except that
returning from a completed Editorial Audit MUST set it to matched for the
content just audited.

**AC-AUDIT-10.** Any Author edit made after the gate is matched MUST set it
back to unmatched.

**AC-AUDIT-11.** Copy LinkedIn Publication MUST be enabled if and only if the
gate is matched. See AC-EDITOR-6.

**AC-AUDIT-12.** A High or Severe LMHS Assessment MUST NOT set the gate to
unmatched, disable Copy LinkedIn Publication, trigger a rewrite, trigger
regeneration, or otherwise alter Publication Content. It MUST cause
Editorial Confidence to withhold a positive recommendation and explain the
risk.

**AC-AUDIT-13.** The Studio MUST NOT auto-publish or transmit content to
LinkedIn or any other platform under any Editorial Audit outcome, including
High or Severe.

## Leaving a Session Before Complete

**AC-LEAVE-1.** The Studio MUST NOT require a distinct cancel, abort, or
restart action to leave a session before Complete; ending the interaction at
any state MUST be sufficient.

**AC-LEAVE-2.** If a session ends before Complete, the Studio MUST NOT
produce any Session Artifact.

**AC-LEAVE-3.** Leaving a session before Complete MUST NOT require any
different handling before Generation than after it; no additional cleanup
state exists for either case.

## Session Completion and Artifacts

**AC-COMPLETE-1.** At Complete, the Studio MUST have produced a Publication
Package and a Portable Editorial Project.

**AC-COMPLETE-2.** The Publication Package produced at Complete MUST reflect
the Author's edited Publication Content, not the content as it existed
immediately after Generation, if the Author made edits.

**AC-COMPLETE-3.** The Studio MUST NOT retain a copy of the Publication
Package, the Portable Editorial Project, or the Ramrattan AI Configuration
after Complete is reached.

**AC-COMPLETE-4.** A Ramrattan AI Configuration MUST NOT be required to
produce a Publication Package or a Portable Editorial Project.

**AC-COMPLETE-5.** The three session artifacts (Publication Package, Portable
Editorial Project, Ramrattan AI Configuration) MUST remain independently
producible; the absence of one MUST NOT block the production of another.

## Cross-Cutting Prohibitions

These criteria apply across every state in the Author Journey and are
restated here for direct testability.

**AC-XCUT-1.** The Studio MUST NOT store any Author data, file, or preference
on the Studio's behalf beyond the lifetime of a single session.

**AC-XCUT-2.** The Studio MUST NOT require a user account, login, or any form
of persistent identity to complete a session.

**AC-XCUT-3.** The Studio MUST NOT offer any AI-assisted rewrite,
regeneration, or content-improvement action anywhere within Publication
Studio.

**AC-XCUT-4.** The Studio MUST NOT infer Branding from Editorial Source
content, or Editorial Source interpretation from Branding content, at any
state in the Author Journey.

**AC-XCUT-5.** The Studio MUST NOT publish or transmit Publication Content to
any external platform on the Author's behalf.

## Cross-References

- `docs/product/Version_1_1_Author_Experience_Baseline.md` — the narrative
  specification each criterion is derived from, including the Entry Path and
  Editorial Audit Gate decisions.
- `docs/architecture/Version_1_1_State_Machine.md` — the state model each
  criterion tests against.
- `docs/architecture/adr/ADR-018-author-ownership-and-publication-studio.md`
  — the architectural decision governing AC-EDITOR-6 and AC-AUDIT-7 through
  AC-AUDIT-13.
- `docs/architecture/adr/ADR-019-studio-configuration-and-author-controlled-continuity.md`
  — the architectural decision governing AC-CONFIG-14 through AC-CONFIG-17
  and AC-ENTRY-7 through AC-ENTRY-8.
