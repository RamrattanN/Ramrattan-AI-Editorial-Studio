# AI Engineering Standard

## Status

Proposed - pending delivery.

## 1. Purpose

This standard defines how AI participants perform repository engineering
work safely, consistently, and durably, under Repository Author authority,
repository governance, verified repository state, and explicit approval
boundaries. It governs how work is delegated, executed, verified, and
reported.

It does not define product behavior, system architecture, or governance in
its own right. It does not replace the documents it is subordinate to (see
Section 3). It exists so that engineering delegation to an AI participant
is as disciplined, reviewable, and recoverable as delegation to a human
contributor.

## 2. Scope

This standard applies to any AI-assisted engineering work performed against
this repository, regardless of which AI tool performs it, the size of the
task, or whether the task is documentation, implementation, review, or
delivery mechanics.

It governs the discipline of delegation and execution. It does not govern
the content of any specific capability, product decision, or release.

This standard is model-agnostic. It does not depend on, name as
authoritative, or presume the continued existence of any specific model
version or vendor. It is not a vendor comparison, a model ranking, a
prompt-writing tutorial, or a record of one engineering conversation. It is
durable repository documentation, revised deliberately like any other
governing document, and is written to remain applicable across future
releases and, where the receiving project adopts equivalent governance,
future repositories.

Where this standard uses "Author," in the context of product or editorial
material, it refers to the editorial end-user role defined in
`docs/constitution/Canonical_Vocabulary.md`, never to the Repository
Author. The two must not be confused; see Section 8.

## 3. Governing Authorities

This standard is subordinate to, and does not restate, the following, in
the authority order established by accepted governance:

1. verified repository and external-system state, for factual questions;
2. `docs/constitution/Constitution.md`;
3. `docs/constitution/Canonical_Vocabulary.md`;
4. accepted Architecture Decision Records and the current architecture
   baseline;
5. `docs/engineering/Capability_Delivery_Workflow.md`;
6. `AGENTS.md`;
7. `CONTRIBUTING.md`; and
8. `AGENT_MEMORY.md`, which is advisory only.

Where this standard appears to describe a rule already stated in one of
these documents, that document controls; this standard cross-references it
rather than duplicating it. Where this standard and a higher-authority
document conflict, the higher-authority document prevails, and the conflict
is reported rather than silently resolved.

This standard does not create a competing approval profile, authorization
tier, or governance hierarchy. It operationalizes the hierarchy already
established by the documents above.

## 4. Core Principles

- **Trust before convenience.** Engineering speed never overrides evidence,
  verification, or Repository Author control.
- **The Repository Author retains final authority.** Product direction,
  governance, and consequential architecture and product decisions may be
  delegated for specific work; final accountability is never transferred.
- **The repository is the source of truth for repository state.**
  Conversation history is not, and becomes unreliable as soon as
  repository state changes underneath it.
- **Verified evidence takes precedence over assumption.** An assumption
  may inform judgment. It may never by itself justify a repository
  mutation.
- **AI participants operate only within explicit authority.** No
  participant infers standing authorization from a prior session, a prior
  task, or its own typical functional role.
- **Specification and architecture must not evolve silently during
  implementation.** A change to approved product behavior, architecture,
  artifact boundaries, or governance requires the same review that
  produced the original decision. See Section 12.
- **Implementation stops when a product, constitutional, governance, or
  architectural decision is required.** The work order that surfaces such
  a decision reports it; it does not resolve it unilaterally.
- **User-owned and Repository-Author-owned repository work is preserved.**
  It is never discarded, overwritten, staged, committed, or relocated
  without explicit authorization scoped to that exact work.
- **Destructive recovery is never inferred.** It requires explicit
  authorization for the exact operation and the exact target.
- **One coherent work order is preferred over a chain of small patches**
  when the problem is already sufficiently understood. Patch chains
  increase the risk of losing context, contradicting an earlier patch, and
  requiring a human to reconcile fragments the participant should have
  reconciled itself.
- **A work order should be holistic, internally consistent, and
  self-verifying**, not a fragment requiring the Repository Author to
  supply missing context turn by turn.
- **Repository mutation requires the governing approval profile for the
  mutation attempted.** An earlier, differently scoped authorization does
  not extend to a new mutation.
- **Validation evidence must match the exact state being delivered.**
  Validation performed against an earlier commit, working tree, or
  generated output does not carry forward automatically; a merge,
  rebase, regeneration, or code change invalidates it.
- **Participants distinguish verified, inferred, and assumed
  information**, and label each accordingly in reporting.
- **An assumption may support a recommendation. It may not support a
  repository mutation.**
- **Completed evidence is not requested again without a material
  reason.** Re-verification is proportional to the likelihood that
  relevant state has changed.
- **External-state inspection failure is not proof of absence.** When a
  remote, GitHub, or CI system cannot be inspected, that state is reported
  as unavailable, never treated as confirmation that the inspected
  artifact does not exist.
- **One active work order should normally close before another begins**,
  unless parallel execution is explicitly authorized. See Section 17.
- **Parallel work must have disjoint scope, or a deliberate consolidation
  decision.** Overlap without one of these creates review and recovery
  risk that outweighs any speed gained.
- **Work orders are engineering contracts, not casual prompts.** They are
  written, reviewable, and durable, not improvised turn by turn.
- **A model-specific rendering of a work order is a presentation of that
  work order.** A Claude instruction, a Codex instruction, or a terminal
  script derived from a work order is not itself the canonical authority
  for the task; the work order is. See Section 9.
- **Baseline Before Better.** When an implementation, product, workflow,
  UX, prompt, API, document, or other engineering artifact already
  exists, engineering begins by establishing that implementation as the
  baseline. Review the existing implementation before proposing
  improvements: understand what already works, what users value, what
  should remain, what should evolve, and what should be removed.
  Redesign is never assumed to be improvement, and existing functionality
  is never recreated before its current behavior is understood.
  Engineering improvements build on validated evidence about the
  existing artifact, not on an unreviewed assumption that it should
  change.

## 5. Repository-First Engineering

Before any recommendation or mutation, inspect verified repository state:
current branch, working-tree cleanliness, local and remote synchronization,
recent history, and the state of any relevant external system (a GitHub
issue, pull request, or CI run). Continue from that verified state.

Conversation history may describe an intended, expected, or previously
true state. It is not evidence of current state. Where the two disagree,
verified repository state governs, and the disagreement is reported rather
than silently absorbed.

Do not repeat inspection already established and known to remain
unchanged. Do not perform repository-wide discovery when an existing
current-status record (for example `HANDOFF.md`) and a narrow, targeted
check already answer the question.

## 6. Evidence-Based Collaboration

Unless explicitly stated otherwise, Repository Author feedback, or output
pasted into the working session, is treated as the direct result of the
immediately preceding work order.

Participants should:

- correlate the feedback or pasted output to that work order, rather than
  treating it as an unrelated new request;
- treat verified command output, CI results, and output produced by
  another AI participant (Claude, Codex, ChatGPT, GitHub Copilot) or by
  GitHub itself as workflow evidence, not as an unverified claim;
- continue the work order from that evidence rather than re-deriving it
  independently;
- avoid repeating a check the evidence already proves, unless repository
  or external state may have materially changed since;
- identify an inconsistency between that evidence and prior expectations
  explicitly, rather than silently reconciling it in a way that hides the
  discrepancy; and
- distinguish evidence - something observed or verified - from inference -
  a conclusion drawn from evidence - in how it is reported.

Conversational output never overrides verified repository state. When
pasted output and verified repository state disagree, the disagreement is
reported and verified repository state governs the next action.

## 7. Multi-Agent Engineering Model

Repository engineering work is typically divided across AI participants by
functional specialization. The roles below are operating defaults for
efficient division of labor. They are not permanent grants of repository
authority, and any participant may perform another bounded role when the
current task explicitly authorizes it. Section 8 defines how these
functional roles relate to the repository's authorization hierarchy.

### Repository Author

Owns product direction, governance, consequential architecture and
product decisions, priorities, final acceptance, and release
authorization. May delegate work to any participant. Does not delegate
final accountability.

### ChatGPT

Default functional role: **Lead Product Architect and Engineering Work
Order Designer.**

Typical responsibilities: product architecture, systems thinking, UX
architecture, governance analysis, implementation strategy, Repository
Author decision support, holistic work-order design, and cross-cutting
review.

Must not be described as having repository authority independent of the
current task.

### Claude

Default functional role: **Lead Documentation and Architecture Review
Engineer.**

Typical responsibilities: repository-wide synthesis, specifications,
implementation plans, architecture reviews, long-form documentation, and
consistency verification.

Must not redefine approved product behavior.

### Codex

Default functional role: **Lead Implementation Engineer.**

Typical responsibilities: repository implementation, tests, validation,
deterministic regeneration, branch- and pull-request-oriented delivery,
repository-safe execution, and implementation evidence.

Must stop when implementation requires a product or governance decision.

### GitHub Copilot

Default functional role: **IDE Implementation Companion.**

Typical responsibilities: code navigation, explanation, local refactoring
assistance, test suggestions, focused implementation support, and
developer productivity.

Must not independently define product architecture or governance.

### Applying this model

These are operating defaults, not a ranking and not a permanent grant of
authority. A participant filling one functional role may be asked, within
an explicit work order, to perform another - for example, a documentation
review conducted by an implementation-focused participant, or an
implementation task delegated to a participant whose default role is
review. The work order's stated Role and Authority (Section 9) govern that
task; the default in this section governs only the absence of a more
specific instruction.

Current tool-to-role assignments in active use are recorded as operational
status in `HANDOFF.md`, not in this standard. This standard defines the
model those assignments apply; it does not itself assign a specific tool
to a specific ongoing task.

## 8. Authority and Escalation Boundaries

`AGENTS.md` defines the repository's authorization hierarchy: Repository
Author, Repository Maintainer, and Implementation Agent. That hierarchy is
authoritative and is not restated here in full.

The functional roles in Section 7 describe typical division of engineering
labor. They are not additional entries in that authorization hierarchy.
Whichever AI participant performs repository-mutating work under a given
work order operates under the Implementation Agent role and its associated
authority boundaries, regardless of which functional role it is nominally
filling. A participant acting as Lead Product Architect carries no more
repository-mutation authority than a participant acting as IDE
Implementation Companion; authority comes from the current work order, not
from the functional role.

Escalation is required, not optional, when:

- a task's Role and Authority (Section 9) do not cover the mutation being
  considered;
- a functional role's typical responsibilities would require a decision
  reserved to the Repository Author (a product, constitutional,
  governance, or architectural decision; see Section 12);
- verified repository or external state materially differs from what the
  work order assumed; or
- two participants' outputs conflict and the conflict cannot be resolved
  from verified evidence alone.

Escalation means reporting the exact condition and stopping, not
substituting the participant's own judgment for the Repository Author's.

## 9. Engineering Work Orders

An Engineering Work Order is a complete, bounded, repository-grounded
delegation artifact. It contains:

- **Role** - the functional or authorization role the participant performs
  for this task.
- **Authority** - the exact approval profile and scope authorized (see
  Sections 15 and 16).
- **Objective** - what the task accomplishes and why.
- **Verified Repository State** - the state confirmed before work begins,
  distinguished from expected or assumed state.
- **Governing Inputs** - the specific governing documents, ADRs, and prior
  artifacts this task must read and treat as authoritative.
- **Repository Author Decisions** - decisions the Repository Author has
  already made and that this task must apply without re-litigating.
- **Scope** - the exact paths, systems, or concerns in scope.
- **Non-Goals** - what this task explicitly does not do.
- **Constraints** - protected files, hash-pinned artifacts, frozen
  documents, or other bounded limits that apply.
- **Required Deliverables** - what must exist when the task is done.
- **Validation** - the exact commands and evidence required.
- **Repository Actions** - which mutations (staging, commit, push, PR
  creation, merge, branch deletion, and so on) are authorized, and which
  are explicitly prohibited.
- **Approval Boundaries** - the exact point at which the task must stop
  and return to the Repository Author.
- **Failure Conditions** - what constitutes a fail-closed condition for
  this task, and the required response to it.
- **Required Report** - the exact structure of the completion report.

An Engineering Work Order is not merely a prompt. It may be rendered into a
Claude-specific instruction, a Codex-specific instruction, a
ChatGPT-specific instruction, a Copilot-specific instruction, or a
terminal-specific instruction, but the work order itself remains the
coherent authority for the task. A rendering adapts presentation; it must
not silently contradict or expand what the work order authorized.

When a work order requires material correction - a scope change, a
materially different verified state, or a discovered gap - prefer
replacing it with a revised, holistic work order over layering a patch
instruction on top of the original. Patch layering increases the risk that
a human or participant misses which instruction is currently authoritative.

### Terminal instruction standard

A rendering of a work order, or any instruction issued alongside one, must
be clearly labeled as exactly one of the following, and must be safe for
its labeled execution mode:

- **Terminal Paste** - commands intended to be pasted directly into an
  interactive shell. These must not assume script-file semantics; for
  example, a Terminal Paste must never include a shebang line or assume
  execute permissions.
- **Script File** - content intended to be saved to disk and executed as a
  script.
- **Claude Work Order** - a rendering addressed to Claude.
- **Codex Work Order** - a rendering addressed to Codex.
- **Copilot Instruction** - a rendering addressed to GitHub Copilot.
- **Repository Document Content** - text intended to be written into a
  repository file, not executed at all.

Mutating terminal work, regardless of rendering, follows read-only
pre-flight, then bounded action, then post-flight verification, matching
Section 11 and Section 14.

## 10. Work Order Lifecycle

1. **Issuance.** The Repository Author, or an explicitly authorized
   Repository Maintainer, issues or authorizes a work order.
2. **Pre-flight.** The participant verifies repository state and reads the
   governing inputs the work order names, per Section 11.
3. **Execution.** The participant performs only the scope authorized,
   under the exact approval profile granted.
4. **Validation.** The participant runs the required validation against
   the exact state produced, per Section 14.
5. **Reporting.** The participant reports per the work order's Required
   Report and Section 18.
6. **Closure or escalation.** The work order reaches its approval boundary
   and stops there, or it is superseded by a revised work order per
   Section 9, or it escalates per Section 8.

A work order is not closed by partial completion. If a task cannot be
completed within its authorized scope, the participant reports the exact
point reached and the exact reason it stopped, rather than declaring
completion.

## 11. Repository State and Pre-flight

Before executing any work order, verify:

- current branch;
- working-tree cleanliness, and whether any pre-existing change is
  user-owned or Repository-Author-owned work that must be preserved;
- local and remote synchronization;
- recent history, sufficient to confirm the expected baseline is present;
- existence of any conflicting local or remote branch, or existing pull
  request, relevant to the task; and
- ownership of any file the task would change, per Section 13's Generated
  Files discipline.

Read governing context proportional to the task. A narrow, bounded task
reads the governing documents and artifacts relevant to that task. A task
that changes product behavior, architecture, or governance reads the full
required-context list its own governing documents specify. Do not perform
repository-wide discovery merely to satisfy a checklist when the answer is
already established.

## 12. Specification Preservation

Implementation must preserve the approved product specification.

If a work order's execution uncovers a genuine need to change approved
product behavior, architecture, artifact boundaries, state transitions,
governance, or Author responsibilities, work on that item stops, and the
task returns to product design and Repository Author review rather than
resolving the conflict unilaterally.

Ordinary engineering decisions that do not change approved behavior remain
within the executing participant's authorized scope. Not every technical
choice is a Repository Author decision; escalating routine implementation
judgment as though it were a specification conflict is itself a violation
of proportionate delivery.

## 13. Change Consolidation

Before editing, inspect whether other approved pending changes affect the
same files or a tightly coupled concern. Consolidate them into one
coherent change when scope, risk profile, and delivery timing agree. Do
not split coherent work merely to demonstrate incremental progress.

Keep changes separate when scope differs materially, risk or approval
authority differs, rollback or recovery is safer separated, delivery
timing conflicts, or an explicit repository constraint requires it.
Consolidation never expands authorization beyond what was granted.

Generated files remain governed by the repository's existing Generated
Files discipline: identify the owning bootstrap or generator before
changing a generated artifact; when ownership is ambiguous or multiple
generators conflict, stop and report the conflict rather than guessing.

## 14. Validation and Verification

Before recommending staging or commit of implementation changes, the
required validation suite - as defined by the governing repository
standard in force for the target repository - must pass. For this
repository, that suite is:

```bash
python3 -m compileall -q studio scripts tests
python3 -m unittest discover -s tests -v
python3 studio.py validate
git diff --check
```

Validation evidence must match the exact commit, working tree, and
generated output being delivered. A merge, rebase, regeneration, or code
change invalidates earlier validation; rerun rather than reuse it.

When validation fails: diagnose the failure, repair it within the
authorized scope, update every affected generator, regenerate where
required, rerun the complete suite, and confirm the repair survives
regeneration. Never recommend staging, commit, publication, or merge with
failing or unavailable required validation, and never weaken a test to
obtain a passing result.

## 15. Start, Publish, Complete, and Conservative Profiles

Repository mutation follows the Standard delegated delivery model:

- **Start** covers planning synchronization, branch creation or
  resumption, implementation, generation, repair, validation, diff review,
  and staging of the exact reviewed scope. It stops before publication.
- **Publish** covers commit of the approved staged diff, commit
  verification, push, pull-request creation or reuse, read-only CI
  monitoring, and marking the pull request ready for review only when all
  required conditions pass. It stops before merge.
- **Complete** covers merge, branch cleanup, return to a clean,
  synchronized `develop`, and completion planning synchronization. It
  stops after verified cleanup.
- **Conservative** applies to exceptional, high-risk work, or whenever a
  delegated profile was not explicitly authorized. It requires approval at
  each protected mutation boundary individually.

Each profile requires its own explicit authorization from the current task
or conversation. Authorization for one profile never authorizes a later
profile. Every prerequisite is verified before advancing to the next
transition within an authorized profile. Read-only CI monitoring is
autonomous within an authorized Publish phase and does not require a
separate approval.

This section summarizes the model governed in full by
`docs/engineering/Capability_Delivery_Workflow.md` and `AGENTS.md`. Those
documents control in any conflict.

## 16. Repository Mutation Boundaries

Explicit authorization is required before:

- staging changes with `git add`;
- creating a commit;
- pushing commits or branches;
- creating, editing, closing, reopening, or marking a pull request ready;
- merging a pull request;
- deleting a local or remote branch;
- creating, editing, closing, or reopening a GitHub issue;
- changing a GitHub Project, milestone, field, item, or summary;
- creating a tag, release, or published artifact;
- changing the frozen Constitution or Canonical Vocabulary outside an
  explicitly authorized constitutional change;
- sending, publishing, or submitting content to an external party;
- installing a dependency or changing external credentials or
  permissions; and
- any destructive or difficult-to-recover operation.

Inspection, analysis, planning, bootstrap preview, in-scope file editing,
non-destructive repair, testing, validation, diff review, and read-only
CI or GitHub monitoring do not require separate approval when already
authorized by the current work order.

An approval applies only to the described action, targets, and verified
state. If those materially change before execution, the participant stops
and requests renewed approval rather than proceeding on the strength of
the earlier one.

## 17. Sequential and Parallel Work

One active work order should normally close - reach its approval boundary
or its stated completion - before another begins on overlapping scope.
This preserves a single coherent thread of authority and avoids two
participants reaching materially different conclusions about the same
repository state at the same time.

Parallel work orders are permitted only when their scope is disjoint, or
when a deliberate, documented consolidation decision explicitly accepts
the overlap and assigns responsibility for reconciling it. Absent one of
these, discovering overlapping in-progress work is a stop condition, not a
scheduling detail to work around silently.

## 18. Required Reporting

Every work order's completion report states, proportional to the task:

- what changed, and the exact paths affected;
- validation performed and its result;
- current repository state relevant to the task (branch, working tree,
  synchronization);
- material assumptions made, clearly labeled as assumptions;
- any discrepancy between expected and verified state; and
- the exact next approval boundary, if any remains.

Reporting is proportional to the task. A narrow, low-risk change does not
require a repository-wide status summary. A task that changed
governance-relevant state reports at the depth that state change warrants.

Do not present a speculative future action as though it were already
authorized or already taken. Recommend only the next safe transition
unless the Repository Author has requested a broader plan.

## 19. Quality Standard

Repository engineering output - documentation, implementation, and
reports alike - is written as durable, precise, evidence-based material,
not as conversational narration. It:

- states normative rules clearly and testably;
- cites governing documents rather than restating them;
- distinguishes verified fact from inference and from assumption;
- avoids praise, brainstorming language, and unsupported claims; and
- avoids vendor marketing and model-versus-model comparison.

A work order, a rendering of one, and a completion report are all held to
this standard. Decorative content that does not carry engineering
information is avoided, particularly in terminal-facing renderings, where
it also risks execution failure.

## 20. Failure and Recovery

Delivery observations fail closed on incomplete evidence:

- `FOUND` - one complete, verified matching artifact;
- `NOT_FOUND` - a successful query confirmed zero matches;
- `UNAVAILABLE` - authentication, network, API, parsing, or a required
  field could not be verified; and
- `AMBIGUOUS` - more than one matching artifact was observed.

`UNAVAILABLE` and `AMBIGUOUS` are blocking states. Neither may be treated
as absence, success, or permission to advance.

Recover a partial or interrupted transition rather than restarting it from
scratch; bootstraps and delivery mechanics are designed to tolerate a
rerun after a partial application. Never use a destructive recovery
operation - discarding uncommitted work, force-pushing, resetting shared
history - unless the Repository Author or an explicitly authorized
Repository Maintainer has approved that exact operation and target in the
current task.

## 21. Non-Goals

This standard does not:

- replace `AGENTS.md`, `docs/engineering/Capability_Delivery_Workflow.md`,
  or any governing document it is subordinate to;
- create a new approval profile beyond Start, Publish, Complete, and
  Conservative;
- rank AI tools, vendors, or models against one another;
- define or constrain any product behavior, feature, or architecture;
- grant any AI participant permanent or standing repository authority; or
- serve as onboarding material for a specific product capability. Product
  onboarding remains governed by the documents listed in Section 3 and by
  `CONTRIBUTING.md`.

## 22. Relationship to the Work Order Template

`docs/engineering/AI_Engineering_Work_Order_Template.md` is the
operational counterpart to this standard. This standard defines the
principles an Engineering Work Order must satisfy; the template provides
the copy-ready structure for writing one that does.

A work order that does not use the template's exact structure may still
satisfy this standard if it contains every element Section 9 requires. The
template exists to make that easier to achieve consistently, not to add a
requirement beyond what Section 9 already states.

## 23. Future Evolution

This standard evolves under the same governance discipline as any other
engineering document: deliberately, not silently. A normative lesson
recorded in `AGENT_MEMORY.md` that proves durable is promoted into this
standard, or into the template, rather than left as advisory-only
experience indefinitely.

A revision that changes a rule in Section 4, Section 12, Section 15, or
Section 16 is treated as a governance change and reviewed with the same
care as an Architecture Decision Record, because those sections translate
directly into repository authority and mutation boundaries.
