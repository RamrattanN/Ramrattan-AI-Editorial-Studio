# Active Mission Template

## Purpose

A copy-ready statement of the third bootstrap layer defined in
`AI_Conversation_Bootstrap.md`: this conversation's mission. Fill in the
placeholders below to state what this conversation is for, instead of
letting it be inferred or rediscovered turn by turn.

Pair this with a filled `Project_Context_Template.md`. That template
supplies facts; this template supplies intent.

This is a lightweight framing for any conversation - documentation,
research, review, or implementation. When the mission is a full
engineering delivery requiring commit, push, or merge authority, escalate
to `docs/engineering/AI_Engineering_Work_Order_Template.md`, the
authoritative, complete Engineering Work Order structure governed by
`docs/engineering/AI_Engineering_Standard.md`. This template does not
replace it.

## Template

```text
Current Mission: [one sentence: what this conversation exists to accomplish]

Success Criteria:
- [condition that must be true for the mission to be complete]
- [...]

Expected Deliverable: [the artifact type: a document, a merged PR, a report, a decision]

Required Outputs:
- [specific output the AI must produce]
- [...]

Stop Conditions:
- [condition under which the AI must stop and report rather than continue]
- [...]
```

## Notes

- State Stop Conditions explicitly even when they seem obvious; an
  unstated stop condition is discovered mid-work, which costs more than
  stating it up front.
- A mission without stated Success Criteria cannot be verified complete;
  do not leave this field generic ("done") when a specific, checkable
  condition is available.
