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

### One Transition at a Time

Provide one safe next action after verifying the previous action.

Do not issue a long sequence that assumes every intermediate step
will succeed.

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
  --state open \
  --json number,title,url
```

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

### Phase 14 - Merge and Delete the Branch

When CI passes:

```bash
gh pr merge 24 --merge --delete-branch
```

This should:

- merge into `develop`,
- delete the remote feature branch,
- delete the local feature branch,
- and switch the repository to `develop`.

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
| Push output pasted into shell | Ignore harmless shell errors and verify push |
| Pager shows `(END)` | Exit with `q` |
| Develop is dirty after merge | Stop and investigate |
| Local develop is behind | Pull with `--ff-only` |

## Never Events

The workflow must never:

- create a branch from an unverified baseline;
- use unresolved placeholders when values are known;
- merge before CI passes;
- silently ignore unrelated working-tree changes;
- create duplicate GitHub issues unnecessarily;
- assume Project items appear immediately;
- treat terminal output as executable commands;
- declare a capability complete while still on a feature branch;
- leave the repository in a dirty or ambiguous state;
- or skip the return-to-`develop` verification.

## Completion Standard

A capability is complete only when repository state, GitHub state,
documentation, tests, and branch state all agree.
