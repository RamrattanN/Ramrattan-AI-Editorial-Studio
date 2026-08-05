# AI Conversation Bootstrap

## Status

Proposed - pending delivery.

## Purpose

Every AI conversation begins with no memory of any other conversation.
This document defines the universal philosophy and model for starting
one productively, regardless of which AI model is used or which
Ramrattan product the conversation concerns.

It does not restate `docs/engineering/AI_Collaboration_Standard.md` or
`docs/engineering/AI_Engineering_Standard.md`. It explains how a
conversation should draw on them at the moment it begins.

## Universal Bootstrap Philosophy

The repository is the source of truth. A conversation is not.

A new conversation carries no reliable memory of prior sessions,
decisions, or repository state. Whatever a conversation "remembers" is,
at best, a claim to verify against the repository, never a substitute
for verifying it.

Bootstrapping a conversation well means supplying exactly the context
required to begin safely and productively - no more, no less. Too little
context produces repeated questions and rediscovery work. Too much
context wastes tokens restating what a governing document already says
durably.

## Conversation Initialization Model

Every conversation draws on three layers of context, which change at
different rates and must not be conflated:

1. **Stable governance** - rarely changes. `AGENTS.md`,
   `docs/engineering/AI_Collaboration_Standard.md`,
   `docs/engineering/AI_Engineering_Standard.md`, and any model-specific
   adapter document (for example `CLAUDE.md`). These are read in full,
   not summarized from memory, because they define durable rules rather
   than current facts.
2. **Current repository state** - changes with every delivery.
   `HANDOFF.md`, plus directly verified branch, working-tree, and
   synchronization state. This layer is never assumed current from a
   prior conversation; it is re-verified at the start of every session.
3. **This conversation's mission** - changes with every request. What
   the Repository Author wants accomplished right now, captured using
   `Project_Context_Template.md` and `Active_Mission_Template.md` in
   this directory.

Bootstrapping a conversation is the act of establishing all three layers
before repository mutation begins: governance by reading it, repository
state by verifying it, and mission by stating it explicitly or inferring
it from the request.

## Required Conversation Expectations

Once bootstrapped, a conversation proceeds under
`docs/engineering/AI_Collaboration_Standard.md` Sections 3 and 4: the AI
owns navigation through the work and states position, rationale, and any
required Repository Author action at each meaningful transition; once
work is authorized, it proceeds without artificial pauses or
re-narration of what is about to happen.

## Repository-First Principles

Verified repository and external-system state governs over conversation
history whenever the two disagree, per
`docs/engineering/AI_Engineering_Standard.md` Section 5. Bootstrapping a
conversation is the first, not the only, moment this applies: state
verified at the start of a session can change during it, and later
actions must verify what they depend on rather than trust the
bootstrap's original snapshot indefinitely.

## Momentum Expectations

A conversation that has been bootstrapped with a clear mission does not
need to re-establish momentum at every turn. Continue executing
authorized work directly; reserve pauses for a genuine stop condition,
per `docs/engineering/AI_Collaboration_Standard.md` Section 4.

## Truthful Capability Boundaries

A bootstrapped conversation states its capability boundaries once,
plainly, rather than allowing them to be assumed. It does not continue
after the active response ends, does not initiate contact independently,
and does not monitor systems in the background without an authorized
automation. The complete list of boundaries is authoritative in
`docs/engineering/AI_Collaboration_Standard.md` Section 13; this
document does not restate it, only reminds a bootstrapping conversation
to apply it from the first message.
