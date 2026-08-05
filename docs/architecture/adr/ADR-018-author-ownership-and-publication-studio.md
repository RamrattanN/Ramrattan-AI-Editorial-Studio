# ADR-018 - Author Ownership and Publication Studio

## Status

Accepted. Revised per Architecture Review Board findings dated 2026-08-03,
and further revised to record the Repository Author's resolution of the
Editorial Audit Gate decision on the same date. Version 1.1 is delivered
against this decision: V11-01 through V11-10 (Issues #70-#79) are complete
on `develop`, including the Editorial Audit and Copy LinkedIn Publication
gate this ADR governs (V11-06, Issue #75, PR #88). The Constitutional
Impact Review this ADR's Governance Question Resolved section requires is
recorded in `docs/product/Decision_Log.md`.

## Date

2026-08-03

## Decision Level

D4 - Architecture

## Context

Version 1.0 established the Editorial Integrity Pipeline, the Article Engine,
the Hero Visual System, and the Portable Editorial Project. Together they
prove that the Studio can carry an Author from natural starting material to a
complete, evidence-checked publication package.

Version 1.0's Canonical Vocabulary also defines Component Collaboration: "the
process of reviewing and improving one Publication Package component while
preserving unaffected work." In practice, this model keeps the Studio in the
authorship loop after generation — the Author requests an improvement, and the
Studio regenerates the affected component. This is safe with respect to
unaffected work, but it does not resolve a more fundamental question: once a
publication exists, whose words are they?

Version 1.1 approaches the end of a session differently. It introduces
Publication Studio, a workspace that opens immediately after a single
Generation and remains open for the rest of the session. The product decision
approved for Version 1.1 is that, inside Publication Studio, the Studio stops
writing and the Author starts editing. This decision needs to be recorded
because it changes a boundary that Version 1.0 left open, and because it
affects the shape of the Publication Editor, the Editorial Review panel, and
the Branding intake, all of which must express the same boundary consistently.

## Decision

Adopt Author Ownership as the governing rule for everything that happens after
Generation, and design Publication Studio to enforce it structurally rather
than by convention alone.

Four linked rules implement this decision:

### 1. Generate Once; the Author edits, the Studio does not

Generation produces the complete publication in a single generative act.
After Generation, the Studio never offers to regenerate, rewrite, improve,
shorten, or expand any part of the publication. The Publication Editor
contains no such controls. The only Studio-provided action inside the
Publication Editor is **Copy LinkedIn Publication**, which copies exactly
what the Author currently sees — nothing the Studio has not shown, and
nothing the Author has not already had the opportunity to change.

This retires Component Collaboration as an Author-facing mechanism for
Version 1.1. The underlying principle Component Collaboration protected —
preserving unaffected work — is now guaranteed structurally, because nothing
is ever regenerated at all. There is no unaffected work to preserve, because
there is no regeneration that could affect it.

### 2. Editorial Review is separate from Publication Content

The Studio's own editorial judgement — Editorial Confidence, Editorial Risk,
Sources, Suggested Mentions, Branding Summary, and Session Summary — remains
visible throughout Publication Studio, but it lives in a distinct, preferably
collapsible Editorial Review panel. It is never copied into the publication
and never rendered inside the Publication Editor. The Studio's judgement
remains available to inform the Author. It is never positioned where it could
be mistaken for the Author's own words.

### 3. Branding is independent of Editorial Source

The Studio must never infer branding from Editorial Source material, and must
never allow Editorial Source content to influence a Branding decision the
Author has not made. If the Author supplies no branding material, the Studio
uses its professional Studio Theme. This is a narrower expression of the same
underlying principle as rules 1 and 2: material the Author did not
specifically approve for a purpose must never silently determine that
purpose. Evidence approved for writing about a topic must never become the
basis for a brand decision the Author never made.

The resolved output of the Branding stage is referred to internally as
**Publication Identity**. This is an architectural term, used in this ADR,
the state model, and acceptance criteria to name the data Generation
consumes. It is not Author-facing language; the Author-facing term remains
"Branding," or "Your Branding" in direct address. The two terms name the
same decision at two different layers and must not be treated as separate
concepts.

### 4. A completed Editorial Audit gates Copy LinkedIn Publication, not editing itself

Copy LinkedIn Publication is enabled only after an Editorial Audit has run
against the currently displayed publication with no edits since. Any further
edit disables it again until a new Editorial Audit reflects that edit. This
rule gates one specific action, not the Author's ability to edit, reach
Session Completion, or produce the Publication Package and Portable
Editorial Project by other means.

The gate is procedural, not evaluative: it requires the analysis to have run
and been disclosed, not that the analysis be favourable. A High or Severe
Editorial Risk result withholds a positive Publication Readiness
recommendation and explains the risk; it does not disable Copy LinkedIn
Publication, trigger a rewrite, or trigger regeneration. This preserves rules
1 through 3 exactly — the Studio still never writes to Publication Content
after Generation, under any audit outcome — while closing the gap those three
rules left open: an Author could previously copy a publication the Studio had
never analysed in its edited form. See Governance Question Resolved below for
the reasoning this closes.

## Alternatives Considered

### Continue Component Collaboration into Version 1.1

Rejected. Component Collaboration still positions the Studio as a co-writer
after generation: the Author asks, the Studio regenerates. Even with
unaffected-work preservation, this leaves an open question about whose words
appear in the final publication. Version 1.1's approved design resolves that
question rather than refining the mechanism that avoided asking it.

### Offer optional AI-assisted rewrite actions inside Publication Studio

Rejected. Offering a rewrite, shorten, or expand action as one option among
many still reintroduces Studio-authored text into an Author-owned surface.
The presence of the option, even if unused, changes what the Publication
Editor is: no longer a space that is unambiguously the Author's, but a space
the Studio might still write into. Trust Before Convenience requires removing
the option entirely, not making it optional.

### Merge Editorial Review into the Publication Editor

Rejected. Placing Editorial Confidence, Editorial Risk, Sources, and Session
Summary inside the same surface as Headline, Hook, Article, and CTA creates a
serious risk that editorial commentary is copied into a publication by
accident, particularly given the Publication Editor's single Copy LinkedIn
Publication action. A separate panel makes the boundary physically visible
rather than merely documented.

### Allow the Studio to infer Branding from Editorial Source

Rejected. Editorial Source material is evidence about what is being written.
Using it to infer a brand identity would let unrelated material — a
competitor's article, a third party's photography, a source publication's
visual style — silently shape how an Author's own publication looks. Branding
must remain a decision the Author makes on its own terms, informed only by
material the Author has specifically supplied for that purpose.

### Leave Editorial Audit optional and non-blocking indefinitely

Rejected. This was the behaviour originally approved and reviewed as Option A
in an earlier revision of this ADR: Author Ownership understood to mean the
Author also inherits responsibility for any risk introduced after Generation,
with no gate at all. It was rejected because it left Version 1.0's
publication-risk guarantee — no positive recommendation for High or Severe
risk — with no enforcement point whatsoever once Author Edits Freely applied,
relying entirely on the Author's own initiative to request an audit that had
no consequence if skipped.

### Gate Session Completion, or block Copy LinkedIn Publication outright, on audit content

Rejected. Gating Session Completion (an earlier candidate, Option B) would
have blocked the Author from producing the Publication Package and Portable
Editorial Project — mandatory artifacts unrelated to the LinkedIn-specific
copy action — over an audit requirement that only that one action needs.
Disabling Copy LinkedIn Publication based on what an audit found, rather than
on whether an audit had run, would have reintroduced the Studio as a
publication gatekeeper deciding content acceptability, which Author Ownership
exists to prevent. Gating the specific action, on the audit having occurred
and been disclosed rather than on its result, is the narrowest rule that
still closes the enforcement gap.

## Consequences

### Positive

- The Publication Editor becomes unambiguous: everything in it is the
  Author's, because nothing else ever touches it after Generation.
- Component Collaboration's safety property — preserving unaffected work — is
  achieved structurally rather than procedurally, removing an entire class of
  partial-regeneration defects.
- Editorial Review can be designed, tested, and audited as a strictly
  read-only surface, since it is never a source for copied publication
  content.
- Branding and Editorial Source can be validated independently, with a single
  clear test for cross-contamination in either direction.
- The single Generate Once boundary gives Editorial Audit an unambiguous
  reference point: drift is always measured against one approved plan and one
  generation, never against a shifting target.
- Version 1.0's publication-risk guarantee now has an enforcement point that
  survives Author Edits Freely: no publication reaches Copy LinkedIn
  Publication without the Studio having analysed and disclosed its final,
  edited form.

### Costs and Risks

- An Author who wants the Studio's help improving a specific sentence after
  Generation must do so by hand. The only alternative is starting an entirely
  new session from Welcome, with a new Editorial Plan and a new Generation;
  there is no path back to Editorial Plan from within the same Publication
  Studio session, and no partial-regeneration path inside it. A blocked or
  failed Generation attempt is the one exception: it returns to Editorial
  Plan within the same session precisely because it never produced a
  publication and never entered Publication Studio. See Editorial Plan in
  `docs/product/Version_1_1_Author_Experience_Baseline.md`.
- Editorial Audit must be precise about what "drift" means, since it is the
  only mechanism left that connects Author edits back to the evidence
  established during Editorial Discovery. An imprecise Editorial Drift
  assessment would leave a real gap that Component Collaboration used to
  narrow procedurally.
- Any future product decision to reintroduce AI-assisted editing inside
  Publication Studio would reverse this ADR and requires the same level of
  review that produced it, not an incremental exception.

## Governance Question Resolved

An earlier revision of this ADR raised, and deliberately did not resolve, a
question about whether Version 1.0's requirement to "prevent High or Severe
risk from receiving a publication recommendation" remained enforced once
Author Edits Freely was adopted: in Version 1.0, that guarantee was enforced
structurally by `PublicationPackageBuilder` refusing to assemble a package
under High or Severe risk, and Version 1.1 did not originally extend any
equivalent enforcement to edits made after Generation.

The Repository Author has resolved this question by selecting rule 4 above:
a completed Editorial Audit, run against the current edited content, is
required before Copy LinkedIn Publication is enabled. This is neither of the
two options this ADR previously described unmodified. It carries Option A's
respect for Author Ownership — no risk level ever disables editing, blocks
the copy action outright, or triggers a rewrite — and Option B's insistence
that the Studio's analysis cannot simply be skipped, but narrows the gate to
the one action that produces Reader-facing publication content, rather than
to Session Completion, which also governs the mandatory Publication Package
and Portable Editorial Project artifacts unrelated to this concern.

Version 1.0's guarantee is preserved in spirit and extended into the edit
phase: the Studio still never issues a positive publication-readiness
recommendation under High or Severe risk. What changes is the enforcement
mechanism — disclosure and a withheld recommendation, not a hard block —
because Author Ownership means the Author, not the Studio, holds final
authority over the copy action once informed. Recording this resolution
formally in the Version 1.0 Decision Log, and completing the Constitutional
Impact Review this kind of change ordinarily warrants under
`docs/architecture/Definition_of_Done.md`, remains normal pre-delivery
governance housekeeping for whichever capability delivers this ADR — the
same step every prior capability in this repository has completed at
delivery time, not a gap specific to this decision.

## Rationale

This decision follows directly from Trust Before Convenience and The Author
Owns the Message, the first two Guiding Principles recorded in
`docs/product/Version_1_1_Author_Experience_Baseline.md`. A workspace that can
still rewrite the Author's words, even helpfully and even on request, asks the
Author to trust that every future rewrite will be as faithful as the first
Generation was. Removing that capability entirely removes the need for that
trust. The Author does not have to wonder whether a sentence was written by
the Studio or edited back by the Author; after Generate Once, every word in
the Publication Editor is the Author's by construction.

Separating Editorial Review from Publication Content and separating Branding
from Editorial Source are the same rationale applied at smaller scale: in
each case, material approved for one purpose must not be permitted to shape a
different purpose without the Author's specific, separate approval. This is
the architecture of Every Artifact Has One Responsibility extended from
session artifacts to session surfaces.

## Future Implications

Any Version 2 capability that reintroduces Studio-generated text after
Generation — including but not limited to a future assisted-editing feature —
supersedes this ADR and requires its own architecture review, its own
Constitutional Impact Review where applicable, and an explicit decision to
depart from Author Ownership as defined here.

The Portable Author Context described in
`docs/product/version2/Capability_012_Portable_Author_Context.md` does not
touch this decision. It concerns preference continuity between sessions, not
authorship inside a session, and remains a separate, unapproved candidate.
Studio Configuration, which does concern preference continuity, is governed
by its own decision record,
`docs/architecture/adr/ADR-019-studio-configuration-and-author-controlled-continuity.md`,
not by this ADR.

Any future change to the Editorial Audit Gate — removing it, tightening it
into a content-based block, or extending it to Session Completion — reverses
part of rule 4 above and requires the same level of review that produced it.

Future publishing integrations must continue to treat the Publication Package
produced by Publication Studio as final Author-owned content at the point of
export. No future capability may reopen or modify Publication Content on the
Author's behalf without repeating the review this ADR represents.
