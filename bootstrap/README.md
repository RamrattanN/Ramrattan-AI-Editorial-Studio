# Conversation Bootstrap Framework

## Purpose

Every AI conversation - with ChatGPT, Claude, Codex, or a future
collaborator - begins with no memory of any other conversation. Without a
standard way to start one, each session either re-derives context from
scratch (slow, token-expensive) or proceeds on unverified assumptions
(error-prone).

This framework standardizes how a conversation begins: what is durable
and should be read, what is current and should be verified, and what is
specific to this conversation and should be stated. It exists to reduce
repeated context, repeated prompting, repeated explanation, unnecessary
token consumption, human error, and conversation startup friction, per
`docs/engineering/AI_Collaboration_Standard.md`.

The repository remains the sole source of truth. This framework
organizes how a conversation reaches that truth quickly; it does not
replace it.

## Architecture

The framework separates stable context from changing context into three
files, plus this README:

| File | Layer | Changes |
|---|---|---|
| `AI_Conversation_Bootstrap.md` | Universal bootstrap philosophy and model | Rarely |
| `Project_Context_Template.md` | Current repository and product state | Every delivery |
| `Active_Mission_Template.md` | This conversation's mission | Every conversation |

`AI_Conversation_Bootstrap.md` is read, not filled in: it defines the
philosophy and the three-layer initialization model every conversation
follows. `Project_Context_Template.md` and `Active_Mission_Template.md`
are copy-ready templates: filled in with current values and provided to
the AI at the start of a conversation, rather than re-explained in prose.

This structure mirrors the existing repository convention of separating
durable engineering principles
(`docs/engineering/AI_Engineering_Standard.md`) from the per-delivery
work order built from them
(`docs/engineering/AI_Engineering_Work_Order_Template.md`), applied one
level earlier - to the conversation itself, before any specific work
order exists.

## How to Use

1. Read `AI_Conversation_Bootstrap.md` once, or confirm it is already
   understood; it changes rarely.
2. Fill in `Project_Context_Template.md` from `HANDOFF.md` and directly
   verified repository or GitHub state.
3. Fill in `Active_Mission_Template.md` with this conversation's mission,
   success criteria, expected deliverable, required outputs, and stop
   conditions.
4. Provide the filled templates to the AI at the start of the
   conversation, alongside (or in place of re-explaining) the standing
   governance documents.
5. If the mission becomes a formal engineering delivery, escalate to
   `docs/engineering/AI_Engineering_Work_Order_Template.md` for the
   complete Engineering Work Order structure; the Active Mission
   Template is a lightweight starting frame, not a substitute for it.

## Relationship to Other Governing Documents

- **`docs/engineering/AI_Collaboration_Standard.md`** governs the
  working relationship between the Repository Author and AI
  collaborators throughout a conversation - navigation, momentum,
  complete artifacts, and truthful capability boundaries. This framework
  operationalizes the moment a conversation begins; it does not restate
  or alter that Standard's requirements.
- **`docs/engineering/AI_Engineering_Standard.md`** governs how AI
  participants perform repository engineering work once a delivery is
  underway - work orders, approval profiles, validation, and reporting.
  This framework hands off to it once a conversation's mission is a
  formal engineering delivery; it does not redefine delivery mechanics
  or approval boundaries.

Where this framework and either Standard appear to conflict, the
conflict is reported rather than silently resolved, per `AGENTS.md`'s
Instruction Authority order. No content in this framework overrides
either Standard.
