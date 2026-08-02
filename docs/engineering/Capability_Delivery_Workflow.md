# Capability Delivery Workflow

## Status

Active engineering standard.

## Purpose

This workflow defines the repeatable delivery process for every
repository capability.

It exists to prevent recurring procedural mistakes, reduce manual
interpretation, preserve repository integrity, and ensure that each
capability returns the project to a clean, known baseline.

## Governing Principles

### State Before Action

Determine the repository's current state before providing or
executing the next command.

### Exact Commands

Commands must be paste-ready.

Do not provide unresolved placeholders when the required value is
already known.

Incorrect:

```text
gh pr checks <PR_NUMBER>
```

Correct:

```text
gh pr checks 24
```

### Verified Transitions Within an Authorized Profile

Provide one safe next action after verifying the previous action. A delegated
profile may authorize a conditional sequence, but every prerequisite must be
verified before the next transition.

Stop immediately when any state is unknown, unavailable, mismatched, or failed.
Do not issue or execute a sequence that assumes intermediate success.

### Recover Rather Than Restart

Bootstrap scripts must permit deterministic reruns after a partial
application.

Expected generated files and managed documentation updates are not
treated as unexpected changes during recovery.

### Trust Repository Evidence

Use:

- Git status
- current branch
- commit history
- GitHub issue state
- Project item state
- pull-request state
- CI state

Do not infer repository state when it can be verified.

### Fail Closed on Incomplete Evidence

Delivery observations use explicit results:

- `FOUND` means one complete matching artifact was verified;
- `NOT_FOUND` means a successful query confirmed zero matches;
- `UNAVAILABLE` means authentication, network, API, parsing, or required-field
  evidence failed; and
- `AMBIGUOUS` means more than one matching artifact was observed.

`UNAVAILABLE` and `AMBIGUOUS` are blocking states. Neither may be treated as
absence, success, or permission to advance.

Remote-dependent recommendations require a successful direct observation of
`origin/develop` and the feature branch. Cached remote-tracking references do
not independently prove freshness.

### Protected Mutations and Read-Only Automation

Inspection, validation, and CI monitoring are read-only and may proceed
automatically inside an authorized delivery phase.

Staging, commit, push, pull-request mutation, merge, branch deletion, issue
mutation, and Project mutation require explicit role-based authority through
the applicable delegated profile or the Conservative profile. Recommendations
must identify both workflow state and the next profile boundary and must never
execute a protected command automatically.

### Change Consolidation

Before editing, inspect whether other approved pending changes affect the same
files or tightly coupled concern. Consolidate them into one coherent change set
when scope, risk profile, and delivery timing agree. Do not split work merely
to demonstrate incremental progress.

Separate changes only for materially different scope, different risk or
approval authority, safer rollback or recovery, conflicting delivery timing,
or an explicit repository constraint. Consolidation never expands authority.

## Delegated Approval Profiles

The Standard delivery profile consists of three separately authorized phases.
Authority must come from the current task or conversation. Approval for one
profile never authorizes a later profile.

### Start Profile

Start may conditionally authorize planning synchronization to `In Progress`,
branch creation or resumption, implementation, bootstrap preview and apply,
diagnosis and repair, regeneration, testing and validation, complete diff
review, and staging of the exact reviewed scope. Stop before publication unless
Publish was explicitly included.

### Publish Profile

Publish may conditionally authorize commit of the approved staged diff, commit
hash verification, push, pull-request creation or reuse, automatic read-only CI
monitoring, and marking the pull request ready for review when all required
conditions pass. Stop before merge.

### Complete Profile

Complete may conditionally authorize merge, local and remote branch cleanup,
return to clean synchronized `develop`, completion planning synchronization,
Project item `Done`, Project summary update, issue closure, and the Capability
Delivery Receipt. Stop immediately if any verification condition fails.

### Conservative Profile

Use Conservative delivery for exceptional high-risk work or when a delegated
profile was not explicitly authorized. Approval is then required at each Git or
GitHub mutation boundary.

No Git or GitHub mutation may occur outside the explicitly authorized profile.
Automatic CI monitoring is read-only and does not require separate approval.

### Finish Where We Started

A capability is not complete until:

- the pull request is merged,
- the feature branch is deleted locally,
- the feature branch is deleted remotely,
- the repository is back on `develop`,
- `develop` matches `origin/develop`,
- the working tree is clean,
- the merge commit is visible,
- and GitHub planning reflects reality.

## Capability Lifecycle

### Phase 1 - Establish the Baseline

Confirm:

```bash
git status
git branch --show-current
git log --oneline --decorate -3
```

Required state:

- branch is `develop`,
- working tree is clean,
- local `develop` matches `origin/develop`,
- latest expected merge is present.

Before relying on remote state, observe it directly:

```bash
git ls-remote origin refs/heads/develop refs/heads/<feature-branch>
```

Failure, malformed output, or a missing `develop` reference makes remote state
unavailable and blocks the transition.

If `develop` is behind:

```bash
git pull --ff-only origin develop
```

Do not create a feature branch from an uncertain baseline.

### Phase 2 - Create or Resume the Feature Branch

First check whether the branch exists:

```bash
git branch --list <branch-name>
```

If absent:

```bash
git switch -c <branch-name>
```

If present:

```bash
git switch <branch-name>
```

Verify:

```bash
git branch --show-current
git log --oneline --decorate -3
```

### Phase 3 - Create the Bootstrap

Repository-oriented instructions should use:

> Create this file under `scripts`:

followed by the filename.

Avoid unnecessary path-oriented phrasing when the containing
repository folder is already known.

### Phase 4 - Preview

Run the capability bootstrap without flags.

Preview mode must:

- verify repository identity,
- verify branch identity,
- verify script integrity,
- inspect the working tree,
- list new files,
- list managed-document updates,
- list decisions being implemented,
- and change nothing.

### Phase 5 - Apply

Run:

```bash
python3 scripts/<bootstrap-file>.py --apply
```

Apply mode must:

- write deterministic files,
- update complementary documents,
- validate required files,
- validate canonical product language,
- compile runtime and tests,
- run the complete test suite,
- run repository validation,
- and display Git status.

### Phase 6 - Partial-Apply Recovery

A bootstrap must tolerate its own expected changes after a failed
validation.

Working-tree validation must permit:

- the bootstrap file,
- declared new files,
- declared managed-document updates.

It must reject unrelated changes.

Git porcelain parsing must:

- preserve both status columns,
- use `--untracked-files=all`,
- and expand untracked directories into individual paths.

### Phase 7 - GitHub Synchronization

Run:

```bash
python3 scripts/<bootstrap-file>.py --sync-project
```

Synchronization must:

- rerun local validation,
- verify GitHub authentication,
- verify the expected Project,
- reuse existing issues,
- prevent duplicate issue creation,
- retry delayed Project item propagation,
- mark the previous capability Done where appropriate,
- mark the current capability In Progress,
- and update Project summary material.

GitHub synchronization must not commit or push repository files.

### Phase 8 - Review Local Changes

Run:

```bash
git status --short
```

Confirm:

- only expected files changed,
- no caches are present,
- no editor backups are present,
- no temporary files are present,
- no unrelated files are present.

### Phase 9 - Stage

Run:

```bash
git add -A
git diff --cached --name-status
```

Review the entire staged set.

Pager output such as `(END)` is not a Git entry.

Exit the pager using:

```text
q
```

### Phase 10 - Commit

Use a capability-scoped message.

Examples:

```text
feat: implement Editorial Workspace intake and source assessment
```

```text
docs: establish the Version 0.9 constitutional foundation
```

```text
chore: establish the capability delivery workflow
```

Verify the commit output before continuing.

### Phase 11 - Push

Run the exact branch command:

```bash
git push --set-upstream origin <resolved-branch-name>
```

Terminal output is not a command.

Do not paste push output back into the shell.

If the push reports success, do not repeat it unless verification
shows a problem.

### Phase 12 - Create or Discover the Pull Request

Create the pull request with resolved values:

```bash
gh pr create \
  --base develop \
  --head <resolved-branch-name> \
  --title "<resolved-title>"
```

Capture the actual pull-request number from the returned URL.

If a pull request may already exist, resolve it first:

```bash
gh pr list \
  --head <resolved-branch-name> \
  --base develop \
  --state all \
  --json number,url,state,isDraft,reviewDecision,mergeable,mergeStateStatus,statusCheckRollup,headRefOid
```

Interpret discovery explicitly:

- zero matches after a successful query is `NOT_FOUND`;
- one complete match is `FOUND`;
- more than one match is `AMBIGUOUS` and blocks selection;
- authentication, API, command, JSON, or required-field failure is
  `UNAVAILABLE` and blocks advancement.

An existing draft pull request must be reported as draft. It is never ready to
merge, even when its checks are green. Marking it ready requires Publish
authorization or explicit Conservative approval.

A ready-for-review pull request is distinct from an approved pull request.
`REVIEW_REQUIRED` and `CHANGES_REQUESTED` block merge. An empty review decision
permits merge only when GitHub independently reports clean mergeability and no
required review gate remains.

### Phase 13 - Check CI

Use the actual pull-request number:

```bash
gh pr checks 24
```

Never use an unresolved placeholder when the number is known.

Do not merge while checks are:

- pending,
- failing,
- cancelled,
- or unavailable.

Zero reported checks are unavailable unless repository policy independently
proves that no checks are required. This repository requires the `validate`
job, so an empty check rollup blocks merge.

Normalize and handle these check outcomes explicitly:

- unavailable;
- pending;
- failed;
- cancelled;
- timed out;
- action required; and
- successful.

Pending checks may be monitored automatically with the read-only command:

```bash
gh pr checks 24 --watch
```

Monitoring does not authorize pull-request mutation or merge.

### Phase 14 - Merge and Delete the Branch

Merge is recommended only when all of the following are verified:

- the pull request is open and not a draft;
- required review state is satisfied;
- the remote feature head matches the pull-request head;
- checks are present and successful;
- mergeability is known and clean; and
- no conflict, block, or requested change exists.

Conflict, `BLOCKED`, `UNKNOWN`, missing mergeability, or malformed mergeability
evidence fails closed.

When every condition passes and Complete authorization or explicit
Conservative merge approval is present:

```bash
gh pr merge 24 --merge --delete-branch
```

This should:

- merge into `develop`,
- delete the remote feature branch,
- delete the local feature branch,
- and switch the repository to `develop`.

Do not assume all cleanup completed because the merge command returned
success. Rerun the helper and recover one verified step at a time:

1. If still on the merged feature branch, switch to `develop`.
2. Synchronize `develop` with `origin/develop` using `--ff-only`.
3. If the merged local branch remains, request approval and delete it.
4. If the merged remote branch remains, request approval and delete it.
5. Verify merge ancestry, clean working tree, and synchronized `develop`.

Never repeat the merge when GitHub already reports it merged.

### Phase 15 - Return to Baseline

Verify:

```bash
git status
git branch --show-current
git log --oneline --decorate -3
```

Required state:

- branch is `develop`,
- working tree is clean,
- local `develop` matches `origin/develop`,
- latest merge is present.

### Phase 16 - Close the Capability

Confirm:

- capability issue is Done,
- milestone is updated where relevant,
- Project board reflects the merged state,
- Version 1.0 Scorecard is current,
- next capability remains Todo until work begins.

## Recovery Matrix

| Condition | Required response |
|---|---|
| Branch already exists | Switch to it instead of recreating it |
| Partial bootstrap apply | Permit expected changes and rerun |
| Exact validation phrase missing | Repair source and generated file |
| GitHub issue already exists | Reuse it |
| Project item is delayed | Retry with bounded waits |
| PR already exists | Discover and reuse it |
| CI pending | Wait and recheck |
| CI failing | Stop and diagnose |
| Remote verification failed | Stop; do not use cached state as fresh evidence |
| GitHub authentication or API failed | Report `UNAVAILABLE`; do not infer absence |
| Malformed GitHub response | Report `UNAVAILABLE`; do not advance |
| Zero matching pull requests | Continue only after a successful query confirms `NOT_FOUND` |
| Multiple matching pull requests | Report `AMBIGUOUS`; do not select one |
| Pull request is draft | Stop before ready-for-review approval |
| Review required | Wait for required review |
| Changes requested | Inspect and resolve feedback |
| Merge conflict | Stop and repair on the feature branch |
| Mergeability blocked or unknown | Stop until GitHub reports clean mergeability |
| Checks unavailable or empty | Stop; do not treat as success |
| Checks cancelled, timed out, or action required | Stop and diagnose |
| Merge completed but checkout did not | Switch to `develop`, then rerun the helper |
| Local branch remains after merge | Delete only with explicit approval |
| Remote branch remains after merge | Delete only with explicit approval |
| Push output pasted into shell | Ignore harmless shell errors and verify push |
| Pager shows `(END)` | Exit with `q` |
| Develop is dirty after merge | Stop and investigate |
| Local develop is behind | Pull with `--ff-only` |

## Never Events

The workflow must never:

- create a branch from an unverified baseline;
- use unresolved placeholders when values are known;
- merge before CI passes;
- treat remote or GitHub failure as confirmed absence;
- treat zero checks as successful CI;
- report a draft pull request ready to merge;
- select arbitrarily among multiple matching pull requests;
- merge with review required, changes requested, conflicts, or unknown
  mergeability;
- silently ignore unrelated working-tree changes;
- create duplicate GitHub issues unnecessarily;
- assume Project items appear immediately;
- treat terminal output as executable commands;
- declare a capability complete while still on a feature branch;
- leave the repository in a dirty or ambiguous state;
- or skip the return-to-`develop` verification.

## CI Validation Contract

Pull-request and protected-branch CI must run the same canonical suite required
before commit:

```bash
python3 -m compileall -q studio scripts tests
python3 -m unittest discover -s tests -v
python3 studio.py validate
```

Local and CI validation are complementary. Neither substitutes for the other.

## Completion Standard

A capability is complete only when repository state, GitHub state,
documentation, tests, and branch state all agree.

<!-- RC1_AUTHORIZATION_CONTINUITY_START -->

## Authorization Continuity Within a Profile

An explicitly authorized Start, Publish, or Complete profile remains satisfied
through every documented transition in that same phase. The Implementation
Agent must not request that profile again merely because it reports status,
reruns the helper, or advances to another state inside the authorized phase.

Authorization ends when the profile reaches its stopping boundary, a genuine
fail-closed condition occurs, verified prerequisites materially change, scope
materially changes, authority is revoked or changed, or the current task or
conversation no longer supplies the authorization context. A later profile
always requires new explicit authorization.

The helper receives the active profile per invocation. It never stores approval
as permanent repository authority and never infers it from prior sessions,
historical commits, earlier capabilities, or old chats.

Helper output distinguishes:

- `authorization already satisfied` for an action or status inside the active
  current-task profile;
- `new profile authorization required` at a later profile boundary; and
- `blocked by fail-closed condition` when state is unsafe, unavailable,
  ambiguous, mismatched, pending, failed, or otherwise blocking.

A status report is not an approval request. A transition inside an already
authorized profile is not a new approval boundary. Conservative delivery
remains available and requires explicit approval for each protected mutation.

<!-- RC1_AUTHORIZATION_CONTINUITY_END -->
