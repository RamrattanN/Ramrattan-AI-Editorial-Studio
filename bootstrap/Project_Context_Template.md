# Project Context Template

## Purpose

A copy-ready snapshot of the second bootstrap layer defined in
`AI_Conversation_Bootstrap.md`: current repository state. Fill in the
placeholders below at the start of a conversation and provide the result
to the AI, instead of re-explaining this context in prose.

Derive values from `HANDOFF.md` and directly verified repository or
GitHub state - never from memory of a prior conversation.

This template is product-independent. The same structure applies to any
Ramrattan product or repository; only the values change.

## Template

```text
Repository: [name and URL]
Product: [product name and one-line description]
Current Phase: [e.g., "Version 1.1 delivered on develop, release decision pending"]
Current Branch: [branch name, verified via `git branch --show-current`]
Current Objective: [the standing objective this conversation serves, if any]
Current Constraints: [protected files, frozen documents, out-of-scope areas]
Deployment Target: [e.g., GitHub develop/main, a private OpenAI Custom GPT, production]
```

## Notes

- Leave a field explicitly marked `None` rather than deleting it; an
  omitted field is ambiguous, a field marked `None` is a verified
  answer.
- This template supplies facts. It does not supply a mission; pair it
  with `Active_Mission_Template.md`.
- Re-verify this snapshot at the start of each new conversation. Do not
  carry a prior conversation's filled template forward unverified.
