# AI Developer Bootstrap Checklist

A copy-ready checklist for the first hour of a new project (or a new
machine on an existing project), so AI-assisted development starts
correctly instead of accumulating ad-hoc permission approvals over
days. See
[`AI_Developer_Bootstrap_Lessons.md`](AI_Developer_Bootstrap_Lessons.md)
in this directory for the reasoning and evidence behind each item.

Do not fill machine-specific secrets into this file. It contains
principles and checkpoints, not values.

## Acceptance Criterion

Bootstrap is not complete until:

> AI-assisted development setup is not complete until routine repository
> work can proceed without repetitive approval prompts, while
> destructive, privileged, secret-sensitive, merge-governed, and
> production-sensitive actions remain explicitly gated.

Verify both halves before moving on - a setup that still prompts for
`git status` has not removed friction; a setup that auto-approves a
force push has not preserved control.

## 1. Developer Machine

- [ ] Git installed and configured (user name/email, credential helper)
- [ ] GitHub CLI (`gh`) installed and authenticated
- [ ] Repository cloned
- [ ] Integration branch (`develop` or equivalent) fetched and
      synchronized; local `HEAD` verified against `origin/<branch>`
- [ ] Language/runtime toolchain installed at the version the project
      actually requires (confirm the real requirement - don't assume
      "whatever is newest" is correct)
- [ ] Local database (or other required local service) installed,
      running, and the project's expected local database(s) created
- [ ] Gitignored local secret-storage convention identified and
      verified ignored (`git check-ignore -v <exact path>`) **before**
      any real secret is written to it
- [ ] The project's full validation suite run once, successfully, before
      starting feature work

## 2. Claude Code Configuration

- [ ] Local, gitignored permissions file identified (confirm the
      project's actual convention and verify it's ignored before
      writing anything to it)
- [ ] Allow rules configured for: routine read-only Git inspection,
      the project's real validation commands, ordinary file edits,
      `git add`/`commit`/`push` on feature branches, non-destructive
      GitHub CLI reads and PR lifecycle actions
- [ ] Deny rules configured for: `sudo`, recursive deletion, destructive
      git operations (`reset --hard`, `clean`, `restore`, `rebase`,
      `filter-branch`), force push, push to protected branches by exact
      name, branch deletion, PR merge/close, dependency installation,
      OS privilege changes, all authentication commands, secret-reading
      commands, destructive database operations, and any locked/frozen
      repository artifact
- [ ] Explicitly double-checked that no broad allow rule accidentally
      covers a dangerous variant of the same command (e.g. a scoped
      `git push origin *` rule does not by itself exclude a force push
      or a protected-branch push embedded in the same invocation - add
      the specific deny pattern)
- [ ] Confirmed a representative safe command runs without a prompt, and
      a representative dangerous command is still blocked, by
      inspection rather than by actually executing anything destructive

## 3. Codex Configuration

- [ ] Workspace-scoped sandbox/access boundary configured deliberately
      (not "full access" merely to remove prompts)
- [ ] Approval policy set deliberately
- [ ] Safe reads/writes/validation streamlined, mirroring the Claude
      Code allow list
- [ ] Ordinary GitHub workflow actions allowed where the project's
      governance permits an agent to perform them autonomously
- [ ] Destructive/system/secret/production gates retained, mirroring the
      Claude Code deny list
- [ ] No blanket full-access ("yolo") mode adopted as a shortcut

## 4. Secrets

- [ ] `.env` (or equivalent) confirmed local and gitignored
- [ ] No secret ever pasted into an AI chat session, in either direction
- [ ] Cloud/hosting secrets configured via the provider's own
      environment/secret mechanism, never a tracked configuration file
- [ ] Rotation plan understood: a *suspected* exposure is treated the
      same as a confirmed one

## 5. Human Approval Boundaries

Confirm these remain gated regardless of how streamlined routine work
becomes:

- [ ] PR merge into a governed branch
- [ ] Credential/authentication actions of every kind
- [ ] DNS changes
- [ ] Cloud account and paid-plan decisions
- [ ] Production deployment
- [ ] Any destructive or difficult-to-recover operation

## 6. Multi-Machine Discipline

- [ ] Before starting work on any machine: `git fetch origin`,
      synchronize the integration branch safely, verify `HEAD` against
      `origin/<branch>` explicitly
- [ ] Before switching machines: everything meaningful is committed,
      pushed, and merged (or left on a pushed branch) - never assume
      another machine already has unpublished work
- [ ] Known untracked, local-only directories (IDE/agent state, local
      env files, build output) identified, so `git status` is never a
      surprise

## Done

When every box above is checked, AI-assisted development on this
project/machine meets the acceptance criterion. Proceed with feature
work.
