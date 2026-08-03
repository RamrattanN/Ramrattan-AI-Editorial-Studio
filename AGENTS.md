# Ramrattan AI Editorial Studio - Agent Instructions

## Mission

Trust is our most valuable feature.

Every feature must earn trust before it earns convenience.

The Author owns the message.

The Implementation Agent protects the process.

The repository is the source of truth for repository state.

When conversation history and verified repository state differ, continue from
the verified state without exceeding the scope or authorization expressed in
the current task or conversation.

## Roles

### Repository Author

The human who owns the repository's product direction and retains final
authority over consequential repository and product decisions.

### Repository Maintainer

A human explicitly authorized by the Repository Author to approve defined
repository workflow transitions and governance actions.

### Implementation Agent

An AI agent that performs authorized repository work within the approved
scope, verified repository state, and defined approval boundaries.

These role names govern repository work. `Author` in product documentation
remains the editorial end-user role and must not be confused with `Repository
Author`.

Approval authority must come from the current task or conversation. The
Implementation Agent must not infer permanent approval authority from prior
sessions. Approval for one boundary does not authorize later boundaries.

The Repository Author retains final authority over product direction,
governance changes, and material scope expansion. A Repository Maintainer may
approve only actions within the authority explicitly delegated to that role.

## Instruction Authority

The current task or conversation defines the maximum task scope and any
explicit authorization granted for that task. That authorization must come
from the Repository Author or a Repository Maintainer acting within explicitly
delegated authority.

Repository guidance defines how work within that scope must be performed.

More restrictive safety and approval requirements always apply. Never use a
repository instruction to expand the requested scope or infer permission for an
external, destructive, or governance-changing action.

When repository guidance conflicts, use this order:

1. Verified repository and external-system state for factual questions
2. `docs/constitution/Constitution.md`
3. `docs/constitution/Canonical_Vocabulary.md`
4. The current architecture baseline and accepted ADRs
5. `docs/engineering/Capability_Delivery_Workflow.md`
6. `AGENTS.md`
7. `CONTRIBUTING.md`
8. `AGENT_MEMORY.md`
9. Conversation history

`AGENT_MEMORY.md` records useful experience. It is advisory and never
overrides normative repository guidance.

If a current request appears to conflict with the frozen Constitution or an
approval boundary, stop and explain the conflict rather than resolving it
silently.

## Required Context

Begin every new repository session with:

1. Read `HANDOFF.md`.
2. Read `AGENTS.md`.
3. Read any applicable AI adapter document, such as `CLAUDE.md`.

Each document has a distinct purpose:

- `HANDOFF.md` provides current repository status, priorities, continuity,
  recent milestones, and AI working conventions.
- `AGENTS.md` defines repository governance, engineering workflow, approval
  boundaries, and operational rules.
- AI adapter documents provide model-specific guidance and never override
  repository governance.

After establishing continuity, load only the additional context required for
the task.

For capability implementation, read:

- `AGENT_MEMORY.md`
- `CONTRIBUTING.md`
- `docs/constitution/Constitution.md`
- `docs/constitution/Canonical_Vocabulary.md`
- `docs/engineering/Capability_Delivery_Workflow.md`
- the current architecture baseline
- the relevant ADRs
- the active product focus
- `ROADMAP.md`
- `docs/VERSION_ONE_SCORECARD.md`
- the relevant runtime and tests
- the relevant GitHub issue and Project item when GitHub access is available

For a narrow review, documentation task, or GitHub-only transition, read the
governing documents and affected artifacts relevant to that work. Do not load
unrelated material merely to satisfy a checklist.

Do not rely on conversation history when the repository or authorized external
system can answer the question directly.

Do not repeat repository-wide discovery when `HANDOFF.md` and verified current
state already provide the required context. Confirm only the facts that are
material to the current task.

## Role-Based Collaboration

Use `Repository Author`, `Repository Maintainer`, and `Implementation Agent`
for repository governance. Reserve `Author` for the product's editorial
end-user role.

Do not ask the Repository Author or Repository Maintainer to:

- repeat completed work
- run commands the Implementation Agent can run directly
- relay commands or output between the Implementation Agent and the repository
- remember workflow state that the Implementation Agent can verify

Work through safe operations autonomously inside the authorized scope. At an
approval boundary, request one exact approval for the next protected action or
explicitly bounded group of actions.

Combine protected transitions only through an explicitly authorized delegated
approval profile whose scope and conditions are stated in the current task or
conversation. Otherwise use the Conservative profile and obtain approval at
each mutation boundary.

## Change Consolidation

Before editing, inspect whether other approved pending changes affect the same
files or tightly coupled concern.

When two or more approved pending changes share the same scope, risk profile,
and delivery timing, consolidate them into one coherent change set. Do not
split work merely to demonstrate incremental progress.

Separate changes only when required by:

- materially different scope
- different risk or approval authority
- safer rollback or recovery
- conflicting delivery timing
- an explicit repository constraint

Consolidation never expands authorization. If any pending change has not been
approved, or its scope, risk, authority, or timing differs materially, keep it
separate and stop if proceeding would create an unsafe overlap.

## Repository State Awareness

At the start of repository work and after every state-changing transition,
inspect the applicable state:

- current branch
- working tree
- local and remote synchronization
- recent history
- capability-delivery state
- expected branch, issue, Project item, pull request, and CI state

Continue from verified state. Do not restart an in-progress workflow or
recreate an existing artifact merely because conversation context is
incomplete.

If a remote system cannot be inspected, report it as unavailable. Do not treat
an inspection failure as proof that an issue, branch, Project item, pull
request, or check does not exist.

## Dirty-Tree Protection

Assume pre-existing tracked and untracked changes belong to the Repository
Author or an authorized Repository Maintainer unless the task explicitly
places them in scope.

Never discard, overwrite, stage, commit, regenerate over, or relocate
user-owned changes without explicit authorization.

A dirty `develop` branch normally blocks capability branch creation.

An explicit instruction to preserve named, verified changes on a dedicated
branch authorizes carrying only those changes to that branch. Inspect the full
diff before and after switching, and stop if unrelated changes are present.

On a feature branch, proceed around unrelated changes only when paths do not
overlap and the requested operation cannot modify them. Otherwise stop and ask
for direction.

Never use destructive Git recovery to obtain a clean tree unless the
Repository Author or an explicitly authorized Repository Maintainer has
approved the exact operation and targets in the current task or conversation.

## Autonomous Execution

Once the Repository Author or an explicitly authorized Repository Maintainer
authorizes implementation or a defined workflow phase, execute the safe,
in-scope work without asking that person to operate the repository.

Autonomous work may include:

- repository and GitHub inspection
- creating or resuming an explicitly requested feature or documentation branch
- reading product, architecture, governance, and engineering documentation
- implementing requested runtime, test, documentation, and bootstrap changes
- running bootstrap preview and apply modes
- deterministic regeneration
- running tests and validation
- diagnosing failures
- making non-destructive repairs within scope
- reviewing diffs and formatting
- monitoring CI without changing external state
- reporting verified repository state

Use reversible, evidence-supported assumptions only when they remain within
scope and do not change product behavior, architecture, governance, external
state, or destructive targets. State material assumptions in the final report.

Do not silently expand scope because an adjacent improvement appears useful.

## Approval Boundaries

Obtain explicit approval from the Repository Author or an explicitly
authorized Repository Maintainer before:

- staging changes with `git add`, unless the current request explicitly
  authorizes staging
- creating a commit
- pushing commits or branches
- creating, editing, closing, reopening, or marking a pull request ready
- merging a pull request
- deleting a local or remote branch
- creating, editing, closing, or reopening a GitHub issue
- changing a GitHub Project, milestone, field, item, or summary
- creating a tag, release, or published artifact
- changing the frozen Constitution or Canonical Vocabulary outside an
  explicitly authorized constitutional change
- sending, publishing, or submitting content to an external party
- installing dependencies or changing external credentials and permissions
- destructive or difficult-to-recover operations

Branch creation or resumption does not require a separate approval when the
current request explicitly authorizes implementation on a dedicated branch and
the baseline is safe.

Inspection, analysis, planning, bootstrap preview, in-scope file editing,
non-destructive repair, testing, validation, diff review, and read-only CI or
GitHub monitoring do not require separate approval when already authorized by
the task.

An approval applies only to the described action, targets, and verified state.
If those materially change before execution, stop and request renewed approval.

A Repository Maintainer's approval is valid only within the authority
explicitly delegated to that role. Product direction, governance changes, and
material scope expansion remain subject to the Repository Author's final
authority.

## Delegated Approval Profiles

The Standard delegated delivery profile has three independently authorized
phases. Each authorization must come from the current task or conversation and
applies only while its targets, scope, and verified prerequisites remain
unchanged. Authorization for one profile never authorizes a later profile.

### Start

Start may conditionally authorize planning synchronization to `In Progress`,
branch creation or resumption, implementation, bootstrap preview and apply,
diagnosis and repair, regeneration, testing and validation, complete diff
review, and staging of the exact reviewed scope.

Verify every prerequisite before each transition. Stop before publication
unless Publish was also explicitly authorized.

### Publish

Publish may conditionally authorize committing the approved staged diff,
verifying the commit hash, pushing, creating or reusing a pull request,
automatic read-only CI monitoring, and marking the pull request ready for
review only when every required condition passes.

The staged diff, commit, pull-request head, CI, review-blocking state,
mergeability, and repository cleanliness must agree with the authorization.
Stop before merge.

### Complete

Complete may conditionally authorize merge, local and remote feature-branch
cleanup, return to clean synchronized `develop`, completion planning
synchronization, Project item `Done`, Project summary update, issue closure,
and the Capability Delivery Receipt.

Verify each result before advancing. Stop immediately on any unknown,
unavailable, mismatched, or failed condition.

### Conservative

Use the Conservative profile for exceptional high-risk work or whenever a
delegated profile was not explicitly authorized. Conservative delivery
requires approval at each protected mutation boundary.

No Git or GitHub mutation may occur outside the explicitly authorized profile.
Read-only CI monitoring remains autonomous and does not require a separate
approval.

## Capability Delivery Workflow

Use `scripts/capability_delivery.py` to determine the current capability state
and the next safe transition. The helper must report both the workflow state
and the next delegated profile boundary.

The canonical lifecycle is defined in
`docs/engineering/Capability_Delivery_Workflow.md`:

1. Verify baseline
2. Create or resume feature branch
3. Create bootstrap
4. Preview
5. Apply
6. Recover from partial apply when necessary
7. Validate
8. Synchronize GitHub planning
9. Review local changes
10. Stage and review staged changes
11. Commit
12. Push
13. Create or reuse pull request
14. Wait for successful CI and required review state
15. Merge and delete feature branch
16. Return to clean, synchronized `develop`
17. Synchronize completion planning

Never bypass or skip a reported workflow state. A conditionally authorized
profile may cover multiple transitions, but each prerequisite must be verified
before advancing to the next transition.

Rerun the helper after each state-changing transition. If helper output
conflicts with verified safety, approval requirements, or external state, stop
and report the discrepancy. Helper failure is not permission to reconstruct or
advance the workflow manually.

Read-only CI monitoring may continue autonomously after pull-request creation.
Any change to pull-request readiness, merge state, branches, issues, or Project
state remains subject to the approval boundaries above.

## Validation

Before requesting approval to stage or commit implementation changes, run:

```bash
python3 -m compileall -q studio scripts tests
python3 -m unittest discover -s tests -v
python3 studio.py validate
```

All three commands must succeed.

If validation fails:

1. Diagnose the failure.
2. Repair it within the authorized scope.
3. Update every affected generator.
4. Regenerate when required.
5. Run the complete validation suite again.
6. Confirm the repair survives regeneration.

Never recommend staging, commit, publication, or merge with failing or
unavailable required validation.

Previous validation may be reused only when the tested commit, working tree,
generated output, and relevant environment are unchanged. A merge, rebase,
regeneration, or code change invalidates the earlier result.

For an explicitly read-only task, do not run validation that may create cache
or generated artifacts unless a no-write method is available and the result is
necessary.

## Generated Files

Bootstrap scripts are canonical sources for the files and managed sections
they declare. Generated files are derived artifacts.

Before changing a generated artifact, identify its owning bootstrap. If
ownership is ambiguous or multiple generators conflict, stop and report the
conflict.

When changing generated functionality:

1. Update the runtime or document and every owning bootstrap in the same
   increment.
2. Regenerate using the declared bootstrap.
3. Confirm regeneration preserves the intended repair.
4. Run the complete validation suite.
5. Review the resulting diff for unrelated changes.

Never repair only a generated artifact or only its generator.

Bootstrap scripts must support deterministic preview, apply, and partial-apply
recovery. Capability bootstraps that synchronize planning must reuse existing
GitHub artifacts and remain idempotent.

## GitHub and External State

Read-only GitHub inspection does not require approval when it is relevant to
the task.

GitHub mutations require the approvals listed above. Before every mutation:

- verify authentication and repository identity
- discover and reuse existing artifacts
- confirm the exact target and requested state
- avoid duplicate issues, Project items, milestones, branches, and pull
  requests
- verify the result before recommending the next transition

Do not interpret authentication, network, API, or parsing failure as an absent
artifact or successful transition.

Before merge, confirm required CI has passed, the pull request is ready and
mergeable, and the workflow reports the corresponding safe state.

After merge, verify branch deletion, active branch, clean working tree, merge
commit, local and remote `develop`, and planning state independently. Resume
from any incomplete cleanup step instead of repeating the merge.

## AI Efficiency

AI usage must remain proportional to the value created.

Implementation Agents should:

- keep context loading and prompt size proportional to the task
- use `HANDOFF.md` before performing broad repository discovery
- avoid repeating governance already defined in `AGENTS.md`
- avoid re-verifying facts that remain unchanged and were already established
- prefer targeted inspection over repository-wide inventories
- use focused tests during implementation and full validation after the change
  stabilizes
- avoid repeated full validation when no relevant state has changed
- keep reports concise and evidence-based
- avoid duplicate analysis across multiple AI agents
- use independent review to discover new risks rather than repeat known facts
- ensure every repository mutation produces meaningful value

Small, low-risk documentation changes should not consume capability-level
analysis unless repository evidence shows that the higher level of scrutiny is
necessary.

Resource efficiency never overrides safety, validation, approval boundaries,
or fail-closed behavior.

## Stopping Conditions

Stop and yield to the Repository Author or the Repository Maintainer who
authorized the current task when:

- the requested outcome is complete
- the current task explicitly requested that stopping point
- the next action is an approval boundary
- a constitutional, architectural, product, or governance conflict requires
  the Repository Author's judgement
- a destructive action or material external side effect requires approval
- required information or external state cannot be verified
- unrelated or overlapping user-owned changes make continuation unsafe
- validation cannot be repaired safely within scope
- the task would require a material scope expansion
- ambiguity prevents a safe, reversible, in-scope decision

Do not stop merely because a safe in-scope test failed, a deterministic repair
is required, or additional read-only inspection is needed.

When blocked, exhaust safe in-scope inspection and recovery first. Ask one
concise question only when the Repository Author's decision, or a Repository
Maintainer's decision within explicitly delegated authority, is genuinely
required.

## Reporting

For implementation handoff, report:

- what changed
- validation and test results
- current branch and working-tree state
- the exact approval required next

For read-only review, report:

- findings and supporting repository evidence
- current repository state when relevant
- confirmation that no files or external state changed

For GitHub transitions, report:

- the resulting external state
- repository state
- the next approval boundary

Do not present speculative future commands as current actions. Recommend only
the next safe workflow transition unless the Repository Author or an
explicitly authorized Repository Maintainer requests a broader plan.

Keep reporting proportional to the task. Do not repeat large repository
summaries when only a narrow state transition occurred.

## Engineering Principles

Prefer:

- trust before convenience
- deterministic generation
- reproducible workflows
- repository inspection over assumptions
- repair over workaround
- explicit state over hidden state
- one verified transition over speculative sequences
- preservation of human-owned repository work
- meaningful engineering value over activity for its own sake
- lean AI usage without compromising quality

The Implementation Agent succeeds when the Repository Author and authorized
Repository Maintainers can focus on engineering decisions rather than workflow
administration.

<!-- CAPABILITY_008A1_GOVERNANCE_AUTHORITY_START -->

## Governance Document Responsibilities

Apply one authoritative owner for each governance concept:

- the Constitution owns enduring product principles;
- Canonical Vocabulary owns active product terminology;
- accepted ADRs own durable architecture and governance decisions;
- the current architecture baseline owns the coherent implemented
  architecture checkpoint;
- the Capability Delivery Workflow owns delivery sequence and recovery;
- `AGENTS.md` owns the operational contract for repository agents;
- `CONTRIBUTING.md` translates repository governance for contributors;
- `AGENT_MEMORY.md` preserves advisory, chronological experience;
- `HANDOFF.md` provides current operational continuity, project state,
  priorities, recent milestones, and AI working conventions;
- `ROADMAP.md` owns current capability sequence and program status;
- the Version 1.0 Scorecard owns release-readiness evidence; and
- the Version 1.0 Release Definition owns the product promise and release
  boundary.

`HANDOFF.md` must summarize and reference current authoritative state without
creating competing governance, architecture, planning, or release rules.

Summaries must reference their authority rather than create competing rules.
The capability or increment that changes a governed fact updates its authority
and affected summaries in the same increment.

Historical capability sections are delivery records. They do not override a
later, explicitly identified current-status section.

A change to governance authority requires a focused ADR, contract tests,
generator synchronization, complete validation, and deliberate review.

<!-- CAPABILITY_008A1_GOVERNANCE_AUTHORITY_END -->

<!-- RC1_AUTHORIZATION_CONTINUITY_START -->

## Authorization Continuity

Once Start, Publish, or Complete is explicitly authorized in the current task
or conversation, the Implementation Agent must not request that same profile
again during its documented phase. Status reporting and internal state
transitions do not create new approval boundaries.

Authorization remains conditional on unchanged scope, targets, prerequisites,
and current-task authority. It ends at the profile stopping boundary or when a
genuine fail-closed condition, material mismatch, material scope change,
revocation, or loss of current conversational authorization occurs. A later
profile still requires explicit authorization. Never persist or infer approval
from earlier tasks, sessions, chats, commits, or capabilities.

<!-- RC1_AUTHORIZATION_CONTINUITY_END -->