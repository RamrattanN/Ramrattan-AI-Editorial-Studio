# Version 1.1 Design Rationale

## Status

Proposed - pending delivery. Revised per Architecture Review Board findings
dated 2026-08-03, and further revised to record the resolution of the
Editorial Audit Gate and Resume Existing Project decisions. Informative, not
normative — this document carries no obligations of its own regardless of
status elsewhere in this set.

## Purpose

This document is not an Architecture Decision Record. It carries no
obligations of its own. Its purpose is to preserve the reasoning behind the
Version 1.1 Author Experience for contributors who were not present for the
design conversation — including, eventually, every future contributor.
Where `docs/architecture/adr/ADR-018-author-ownership-and-publication-studio.md`
records what was decided, this document records why it made sense to decide
it that way.

## The Question Version 1.0 Left Open

Version 1.0 answered a hard question well: can an editorial studio built on
AI generation produce something an Author can trust enough to publish? The
Editorial Integrity Pipeline, Evidence Validation, LMHS Editorial Risk, and
the Article Engine's evidence-gated generation all answer yes, with evidence
to show for it.

But Version 1.0 left a second question mostly unaddressed: once a publication
exists, whose words are they? Component Collaboration — reviewing and
improving one Publication Package component while preserving unaffected work
— was a careful, well-scoped answer to a narrower problem: how do we let an
Author ask for changes without breaking things that were already approved.
It never had to answer the harder question, because Version 1.0's scope
stopped short of a workspace where that question became unavoidable.

Version 1.1 is that workspace. Publication Studio exists because the Studio
now sits with the Author for the entire remainder of the session, not just
for one generation and one export. A workspace that persists has to answer
the authorship question explicitly, because every additional interaction
inside it either reinforces or erodes the Author's claim to the words on the
screen.

## Why Discovery and Plan Are Two Gates, Not One

Editorial Source, Branding, Editorial Discovery, and Editorial Plan could
have been collapsed into a single intake-and-approve step: gather everything,
show everything, approve everything, generate. Version 1.1 deliberately keeps
Editorial Discovery and Editorial Plan as two separate gates instead, and the
separation is not incidental.

Editorial Discovery asks the Author to confirm what the Studio understood.
Editorial Plan asks the Author to approve what the Studio intends to write.
These are different questions, answered from different evidence, at
different points of certainty. An Author who agrees with the Studio's
understanding of their intent, audience, and platform has not yet seen — and
should not yet be asked to approve — a specific Headline, Hook, and Call to
Action built on that understanding. Merging the two gates would force the
Author to approve a structure before confirming the foundation it stands on,
or to reconfirm the foundation redundantly alongside a structure they are
really being asked to judge.

This is Progressive Disclosure and One Decision Per Step applied at the
point in the Journey where they are easiest to skip past for the sake of
fewer screens. Two gates cost the Author two decisions instead of one. They
buy something Trust Before Convenience treats as worth that cost: an Author
who approves Editorial Plan is approving a plan built on ground they already
inspected, not ground they are inspecting for the first time at the same
moment they are asked to approve what is built on it.

The same discipline governs why Editorial Source and Branding remain
distinct inputs even where Express Workflow lets them share a screen — see
Why Branding Never Touches Editorial Source, and the Express Workflow
combination rule described in the Baseline. Combining a screen's
presentation is a navigation choice. Combining two decisions into one
approval is a governance choice, and this baseline only ever makes the
former.

## Why Generate Once, Not Generate Better

The instinctive answer to "how do we help the Author improve a draft" is to
let them ask for another one. Version 1.1 deliberately does not do this
inside Publication Studio, and the reasoning is worth preserving even though
it will feel restrictive on first read.

Every offer to regenerate is also, quietly, an offer to keep authorship
ambiguous. An Author who can always ask the Studio to try again has less
reason to fully inhabit any single draft — there is always a version that
might be better, produced by someone other than themselves. Removing the
option does not remove the Studio's editorial judgement from the session; it
removes the Studio's pen from the page. The Editorial Review panel keeps the
judgement. The Publication Editor keeps the pen, and gives it entirely to the
Author.

This is Trust Before Convenience applied at the point where it is hardest to
apply: the moment right after generation, when it would be genuinely
convenient to offer one more pass. Version 1.1 chooses not to, because the
trust an Author places in their own final publication depends on knowing no
one else might still touch it.

## Why Two Panes, Not One

Publication Studio's Hero Visual pane and Publication Editor pane are
visually separate for the same reason they are architecturally separate: the
Hero Visual System and the Article Engine were already independent
generation pipelines in Version 1.0, each with its own evidence and
provenance requirements. Version 1.1 does not merge them into one surface,
because doing so would blur two different kinds of Author ownership — visual
and verbal — into one, at exactly the moment the product is trying to make
ownership clearer, not less clear.

Keeping them side by side, rather than sequential, also reflects how an
Author actually works: the Hero Visual and the text inform each other
continuously while editing, not once in sequence. A layout that matches that
reality is not a cosmetic choice; it is the same Progressive Disclosure
principle applied to spatial layout instead of sequence.

## Why Editorial Review Is Never Copied

The instinct to merge Editorial Review into the Publication Editor usually
comes from a good place: the Author might want the Sources or the Session
Summary handy while editing. Version 1.1 keeps them close, in a collapsible
panel, but never inside the copyable surface, because the two kinds of text
serve fundamentally different audiences.

Publication Content is written for the Reader. Editorial Review is written
for the Author, about the Studio's own confidence in what it produced. A
Reader has no use for an internal risk assessment, and an Author who
accidentally copies one into a LinkedIn post has had their trust in the
Studio's boundaries broken in a small but real way. The single Copy LinkedIn
Publication action exists precisely so this mistake is structurally
impossible rather than merely unlikely.

## Why Branding Never Touches Editorial Source

This boundary is easy to underestimate, because it is easy to imagine cases
where inferring branding from source material would feel helpful — a source
article's clean, minimal visual style might genuinely suit an Author's brand.
Version 1.1 rejects the inference anyway, because the alternative asks the
Studio to make a judgement it has no standing to make: what an Author's own
professional identity should look like, based on material the Author
supplied for an entirely different reason.

Editorial Source material is chosen for what it says. Branding material is
chosen for what it represents. An Author who supplies a competitor's article
as source material has not, by that act, expressed any preference about
their own visual identity. Treating the two as related, even loosely, would
quietly expand what the Studio infers beyond what the Author actually
approved — the same failure mode Component Collaboration was designed to
avoid at the component level, now avoided at the input level instead.

## Why Editorial Audit Exists at All

Removing every rewrite action from Publication Studio raises a fair
question: if the Studio can no longer help by rewriting, how does it help at
all once editing begins? Editorial Audit is the answer, and its shape is
deliberate.

Free editing is a form of convenience, and Trust Before Convenience does not
mean convenience is forbidden — it means convenience must never come before
trust. Editorial Audit is what keeps the two properly ordered once the
Author has full editing freedom: it gives the Studio a way to keep verifying,
without ever regaining a way to keep writing. The Author can edit anything,
including in ways that quietly undercut the evidence the publication was
built on. Editorial Audit's job is to say so, honestly and without
correction, whenever asked.

This is also why Editorial Audit is repeatable rather than one-shot, and why
its required use is narrowly scoped to Copy LinkedIn Publication rather than
to Session Completion generally. A mandatory audit gating Session
Completion would reintroduce a Studio gatekeeper between the Author and
their own mandatory artifacts — the Publication Package and Portable
Editorial Project — over a requirement that only the LinkedIn-specific copy
action actually needs. Requiring the analysis to have run and been shown
before that one action, while leaving Session Completion itself ungated, is
what keeps the Studio's role advisory everywhere except the single point
where its silence would otherwise let an unanalysed publication leave the
session. See The Editorial Audit Gate in Editorial Audit for the resolved
mechanics.

## Why Editorial Drift Is Measured, Not Judged

Editorial Drift could easily have been designed as a warning system —
flagging edits as risky, discouraged, or requiring justification. Version
1.1 does not do this. Editorial Drift reports how far the Author's edits have
moved the publication from the approved Editorial Plan and the evidence
confirmed at Editorial Discovery, and stops there. It does not ask the Author
to defend a change, and it never blocks Session Completion, editing, or the
Author's mandatory artifacts.

This restraint matters because Author Edits Freely is not a qualified
principle, even where the Editorial Audit Gate now requires the analysis to
have run. An Editorial Audit that punished drift, even mildly — refusing to
enable Copy LinkedIn Publication under High or Severe risk, for instance —
would make editing conditionally free rather than actually free. The gate
requires disclosure, not a favourable result; a High or Severe finding
withholds a positive recommendation and explains why, but the Author can
still copy what they wrote. Measuring drift honestly, disclosing it
unconditionally, and leaving every judgement about what to do with that
measurement to the Author, is what keeps Audit Before Publishing compatible
with Author Edits Freely rather than in tension with it.

## Why Three Artifacts, Not One

It would be simpler to produce a single session file containing everything:
preferences, project state, and the finished publication together. Version
1.1 deliberately does not do this, because the three things an Author might
want from a session — publish this now, resume this later, start faster next
time — are genuinely different requests with different lifespans and
different sensitivity.

A Publication Package is finished and meant to leave the Studio entirely. A
Portable Editorial Project is unfinished-work continuity, carrying evidence
and editorial state that the Author may not want attached to every future
session. A Ramrattan AI Configuration is neither; it is the thinnest possible
slice of the session — preference, not substance — chosen specifically so an
Author can share or reuse it without exposing any editorial content at all.
Collapsing these into one artifact would eventually force a compromise on at
least one of those three lifespans. Keeping them separate costs nothing an
Author actually wants, and preserves Every Artifact Has One Responsibility
exactly.

This is the fourth place this document has invoked Every Artifact Has One
Responsibility — after the three session artifacts here, it has already
governed why Editorial Review stays out of the Publication Editor and why
Branding stays out of Editorial Source. That repetition is deliberate rather
than a single phrase doing loose duty for four unrelated boundaries. Each
application asks the same question at a different scale — does this thing
carry exactly one responsibility, or has a second one been allowed to attach
to it — and Version 1.1's boundaries are best understood as one principle
applied consistently at the artifact scale, the surface scale, and the input
scale, not as four independent rules that happen to agree.

## Why Guided and Express Are One Machine

It was tempting, early in this design, to treat Express Workflow as a
lighter, faster alternative product path — fewer checks, fewer screens,
built for the Author who already knows what they want. Version 1.1 rejects
that framing entirely. Express Workflow changes how many screens an Author
sees. It changes nothing about what the Studio is allowed to assume without
asking.

Maintaining two workflows as two views of one state machine, rather than two
machines, is what makes that guarantee possible to keep over time. A second
machine invites a second set of assumptions, and eventually a second set of
mistakes — a shortcut taken in the name of speed that quietly reintroduces
an inference the Guided Workflow would never have allowed. One machine, two
presentations, is a discipline as much as an architecture choice.

## What Remains Deliberately Unresolved

Version 1.1 does not attempt to solve preference portability beyond a single
downloadable file, and does not integrate with the Portable Author Context
described as a Version 2 candidate in
`docs/product/version2/Capability_012_Portable_Author_Context.md`. That
restraint is intentional. A token-based, platform-integrated preference
system raises security, signing, and trust questions that deserve their own
review, on their own timeline, with their own evidence. Bundling that
ambition into Version 1.1 would have meant either rushing those questions or
quietly deferring them without saying so. Version 1.1 chooses to say so
instead.

The same discipline applies to publishing automation. Publication Studio
produces a Publication Package an Author can copy and export; it does not
send anything anywhere. Every future capability that would change that must
justify itself against Author Ownership from first principles, not inherit
permission from proximity to a workspace that already handles publication
content.

## Why Two Questions Were Left Open, and How They Were Resolved

An earlier revision of this baseline deliberately left two questions
unanswered: whether Editorial Audit must run at least once before Copy
LinkedIn Publication, and how Resume Existing Project fits into this
Journey. Both were documented precisely, neither was decided, and that
restraint was itself worth explaining at the time — the reasoning is
preserved here because it explains why the resolution, once it came, took
the shape it did.

Both questions shared a shape: each had more than one answer fully
consistent with everything else this document argues for. Requiring an
audit and not requiring one were both defensible readings of Audit Before
Publishing — one treating it as a floor, the other as a standing offer the
Author is trusted to accept or decline. Placing Resume alongside
Configuration Load and placing it as a separate fast path into Publication
Studio were both defensible readings of Author-Controlled Continuity.
Choosing between them was not a documentation task; it was a product
judgment about how much the Studio should still insist on, and how much it
should simply trust, once free editing exists. The alternative — silently
picking the answer that happened to already be written down — was available
and was rejected, because a specification that hides its own unresolved
judgment calls behind confident prose is worse than one that names them.

The Repository Author has since resolved both. Editorial Audit is now
required — but the requirement was narrowed to the one action that produces
Reader-facing output, Copy LinkedIn Publication, rather than broadened to
Session Completion. This is the answer that best honours both readings that
were on the table: the Studio insists on its analysis having occurred, the
way a floor would, but only where the Author is about to act on
Reader-facing content, preserving the Author's trust everywhere else. Resume
Existing Project became a distinct entry path rather than an option folded
into Configuration Load, precisely because folding it in would have made two
mechanisms with different responsibilities — preference and content —
collide at the one moment they most needed to stay apart. Structural
separation, not configuration, is what Author-Controlled Continuity turned
out to require once the choice was actually made. See The Editorial Audit
Gate in Editorial Audit and Relationship to Resume Existing Project in
Studio Configuration for the resolved specifications.

Trust Before Convenience applied to how this document treated its own
readers while the questions were open, and applies equally now: the
resolution is recorded here in full, not silently absorbed into prose that
gives no sign a judgment call was ever made.

## Closing

The Studio's motto has not changed: trust earned, confidence shared,
conversations inspired. Version 1.1 is best understood as that motto applied
to the moment right after generation — the moment a product is most tempted
to keep helping, and the moment an Author most needs to be left alone with
work that is genuinely, unambiguously their own.
