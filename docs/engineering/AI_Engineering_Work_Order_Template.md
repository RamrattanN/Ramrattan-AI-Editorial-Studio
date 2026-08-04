# AI Engineering Work Order Template

## Status

Proposed - pending delivery.

## Purpose

This is the copy-ready template for an Engineering Work Order, as defined
by `docs/engineering/AI_Engineering_Standard.md`. It is a reusable
repository template, not explanatory prose. Copy the template below,
replace every placeholder, delete any field genuinely not applicable, and
issue the completed work order.

This template is subordinate to `AGENTS.md` and
`docs/engineering/Capability_Delivery_Workflow.md`. Where it appears to
permit something those documents restrict, the governing document
controls.

## How to Use This Template

1. Copy the canonical template in full.
2. Replace every `[...]` placeholder with exact, verified content. Do not
   leave a placeholder unresolved in an issued work order.
3. Delete a numbered field only when it is genuinely not applicable to the
   task; do not delete a field because its answer is inconvenient.
4. Apply the short guidance for the closest matching task type in
   Appendix A.
5. Issue the completed work order as, or alongside, the appropriate
   rendering defined in the Standard's Terminal Instruction Standard
   (Terminal Paste, Script File, Claude Work Order, Codex Work Order,
   Copilot Instruction, or Repository Document Content). Label the
   rendering explicitly.

Do not maintain a second, competing full template for a specific task
type. Use this one template, adjusted per Appendix A.

## Canonical Template

```text
# Engineering Work Order

## 1. Work Order Title
[One concise, specific title. Not "fix bug" - name the exact concern.]

## 2. Role
[Functional role for this task: Lead Product Architect and Engineering
Work Order Designer / Lead Documentation and Architecture Review Engineer
/ Lead Implementation Engineer / IDE Implementation Companion / other,
explicitly named. Note if this differs from the participant's default
role per the AI Engineering Standard.]

## 3. Authority and Approval Profile
[Exactly one of: Start / Publish / Complete / Conservative. State the
exact scope this profile is authorized for in this task - do not rely on
the profile name alone. If Conservative, state that approval is required
at each protected mutation boundary individually.]

## 4. Objective
[What this task accomplishes, and why. One paragraph.]

## 5. Verified Repository State
[State only what has been directly verified before this work order was
issued, distinguished from what is merely expected:
- current branch:
- working-tree cleanliness:
- local/remote synchronization:
- recent history (last few commits):
- relevant existing branches, PRs, or issues:
- any pre-existing, user-owned or Repository-Author-owned change present
  and how it must be treated:
Mark anything not directly verified as "expected, not verified" rather
than presenting it as confirmed.]

## 6. Governing Inputs
[The exact governing documents, ADRs, and prior artifacts this task must
read and treat as authoritative. List specific paths, not general
categories.]

## 7. Repository Author Decisions
[Decisions the Repository Author has already made that this task must
apply without re-litigating. If none, state "None beyond standing
governance."]

## 8. Exact Scope
[The exact paths, systems, or concerns in scope. List specific file paths
where the task is documentation or narrowly bounded implementation. Do not
describe scope only in prose if an exact path list is possible.]

## 9. Explicit Non-Goals
[What this task does not do, stated explicitly, including adjacent work
that might seem natural to absorb but is out of scope.]

## 10. Constraints and Protected Areas
[Protected files, hash-pinned artifacts, frozen documents, generated-file
ownership, or other bounded limits that apply. Name the owning bootstrap
or generator for any generated artifact in scope, or state that ownership
was checked and none applies.]

## 11. Required Deliverables
[What must exist when the task is done. Exact file paths for
documentation or code; exact behavior for implementation.]

## 12. Implementation or Documentation Requirements
[Task-specific requirements: required structure, required content,
required behavior, style constraints. See Appendix A for task-type
guidance.]

## 13. Validation Requirements
[Exact commands required and the evidence expected from each. For this
repository, the baseline suite is:

python3 -m compileall -q studio scripts tests
python3 -m unittest discover -s tests -v
python3 studio.py validate
git diff --check

Add task-specific validation - deterministic-regeneration checks,
documentation cross-reference checks, fence-balance checks - as required
by the task. State that validation evidence must be produced against the
exact final state delivered, not reused from an earlier state.]

## 14. Repository Actions Authorized
[Exactly which mutations are authorized for this task: staging / commit /
push / pull-request creation or reuse / marking ready for review / merge /
branch deletion / issue mutation / Project mutation / tag or release
creation / dependency installation / external publication. State "none of
the above; read-only" if applicable.]

## 15. Repository Actions Prohibited
[Explicitly list what remains out of scope even if it would be a natural
next step, to prevent silent scope expansion. State this even when it
overlaps with Section 16 of the AI Engineering Standard, so the work order
itself is self-contained.]

## 16. Failure and Stop Conditions
[What constitutes a fail-closed condition for this task (UNAVAILABLE,
AMBIGUOUS, mismatched state, conflicting branch, failing validation,
required decision outside authority) and the required response: stop and
report, do not infer, do not proceed. If this task involves polling
external state (CI, a remote, a pull request), state the bounded timeout
or check interval and what to report if the timeout is reached without
resolution.]

## 17. Required Final Report
[The exact structure the completion report must follow. Number the
required items. At minimum: what changed, validation results, repository
state, assumptions and discrepancies, and the next approval boundary.]

## 18. Next Approval Boundary
[State explicitly what happens after this task completes, and what
requires a new, separate authorization. Do not imply that this
authorization extends beyond its stated profile.]
```

## Appendix A - Task-Type Guidance

Use the canonical template above for every task. Apply this short guidance
for the closest matching type; do not create a separate full template per
type.

### Documentation / Architecture Work

- Section 12: state exact required document structure, required sections,
  and status field value.
- Section 13: add cross-reference resolution, fence balance, and
  terminology-consistency checks alongside the baseline suite.
- Section 10: confirm whether the target document is bootstrap-owned
  before editing; if ownership evidence requires another file to change,
  stop and report before expanding scope.

### Runtime Implementation

- Section 12: state exact function, module, or behavior boundaries, and
  which existing modules must be called rather than modified.
- Section 13: require the full validation suite plus any new or updated
  tests, and require that hash-pinned or otherwise protected files remain
  unmodified unless the work order explicitly authorizes changing them.
- Section 16: state explicitly that a discovered need to change approved
  product or architecture behavior is a stop condition, per the
  specification-preservation rule, not an implementation judgment call.

### Read-Only Review

- Section 14 and 15: state "read-only; no mutation authorized" explicitly.
- Section 17: require the report to distinguish findings from
  recommendations, and repository evidence from inference.
- Omit Section 16's timeout guidance unless the review itself depends on
  polling external state.

### GitHub-Only Transition

- Section 8: name the exact issue, pull request, Project item, or release
  artifact affected, by number or identifier, not by description alone.
- Section 16: require `FOUND` / `NOT_FOUND` / `UNAVAILABLE` / `AMBIGUOUS`
  discovery results before any mutation, per the AI Engineering Standard's
  Failure and Recovery section.
- Section 14: name the exact GitHub mutation authorized; GitHub mutation
  authorizations are never implied by an adjacent code change.

### Terminal Paste

- Every command must be safe to paste directly into an interactive shell.
- Do not include a shebang line or assume script-file execute permissions.
- Precede a mutating command with the read-only pre-flight command that
  verifies the assumed state, so the paste is self-verifying.

### Script File

- State the intended filename, location, and execution method explicitly.
- State whether the script is temporary (to be deleted after use) or a
  durable repository artifact, and if durable, state its owning location
  and who maintains it going forward.
