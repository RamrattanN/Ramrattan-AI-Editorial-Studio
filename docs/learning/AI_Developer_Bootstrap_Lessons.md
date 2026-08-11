# AI Developer Bootstrap Lessons

**Status:** Informative (Non-Governing)
**Source:** Web Walking Skeleton 01 foundation and hosted development
deployment (2026-08-10 - 2026-08-11)

## Purpose

This document captures reusable engineering-process lessons learned
while building and deploying the first browser-based Ramrattan AI
Editorial Studio vertical slice, so a future project - inside this
repository or a new one - starts with the right developer-machine and
AI-agent configuration on day one instead of rediscovering it days into
delivery.

It does not define repository governance. Where anything here appears
to conflict with `AGENTS.md`, `docs/engineering/AI_Engineering_Standard.md`,
or `docs/engineering/AI_Collaboration_Standard.md`, those documents
control; this document exists to help a new project reach that
governance-compliant state quickly, not to replace it.

For the copy-ready, first-hour version of this material, see
[`AI_Developer_Bootstrap_Checklist.md`](AI_Developer_Bootstrap_Checklist.md)
in this directory.

## The Central Lesson

> **Agent permission optimization is a project-bootstrap requirement,
> not a late-stage convenience.**

During this delivery, Claude Code's permission system was configured
for low-friction routine work only after several multi-day delivery
sessions had already accumulated dozens of one-off, ad-hoc approval
rules through repeated "always allow" clicks (visible in the
repository's local, gitignored `.claude/settings.json`). That
accumulation was disorganized, incomplete, and happened by accident
rather than by design.

When the permission profile was finally configured deliberately (narrow
`allow`/`deny` rules for git inspection, validation commands, ordinary
edits, and feature-branch delivery, with destructive/privileged/secret/
production actions explicitly denied), the effect was immediate: routine
work stopped generating repetitive prompts, while every consequential
action - PR merge, force push, `npm install`, secret access, DNS,
database drops - remained gated exactly as intended.

**The lesson: do this in the first hour of a project, not the fortieth.**
A deliberately designed permission profile is cheaper to write once, up
front, than to reconstruct from scattered ad-hoc approvals later, and it
is the only way to be confident about what is actually gated versus what
merely hasn't come up yet.

## 1. Claude Code Low-Friction Bootstrap

Configure `.claude/settings.local.json` (verified local-only, gitignored
- see Section 6) at project start with narrow `allow`/`deny` rules, not
a blanket permissive mode:

**Streamline (allow):**

- routine read-only Git inspection (`git status`, `git diff`, `git log`,
  `git show`, `git branch --show-current`, `git fetch`, `git rev-parse`,
  `git check-ignore`)
- the project's actual validation commands (typecheck, lint, test,
  build, and any repository-specific validation script) - use the
  project's real command names, not a guess
- ordinary file edits within the repository
- `git add`, `git commit`, `git push` for feature/documentation branches
- non-destructive GitHub CLI reads and PR lifecycle actions the
  project's governance allows an agent to perform autonomously (`gh pr
  create`, `gh pr view`, `gh pr checks`, `gh pr ready`)

**Keep gated (deny):**

- `sudo`, `rm -rf` and other recursive deletion, `git reset --hard`,
  `git clean`, `git checkout --`/`git restore` (discard forms),
  `git rebase`, `git filter-branch`
- force push and any push to the protected branches by name (`main`,
  `develop`, or the project's equivalents) - a broad `git push origin *`
  allow rule does not exclude a force-push or protected-branch push
  embedded in the same command; add explicit deny rules for those exact
  patterns rather than assuming a scoped allow rule is enough
- branch deletion (`git branch -d`/`-D`, `git push origin --delete`)
- `gh pr merge`, `gh pr close` - see Section 7 on why merge stayed
  human-gated even though other PR actions were streamlined
- package manager installs (`npm install`, `npm ci`, `brew install`,
  `apt`) - dependency changes are a governance approval boundary in this
  repository (`AGENTS.md`), and the permission system enforces that
  independent of what conversational instruction says
- OS privilege changes (`chmod`, `chown`)
- any authentication command (`gh auth`, `claude auth`, `aws configure`,
  `gcloud auth`, `az login`) and any command that reads or echoes a
  secret (`cat *.env`, `echo $SECRET_VAR`, `printenv`)
- destructive database operations (`dropdb`, destructive `psql -c`)
- `Read`/`Edit`/`Write` on `.env` files and on any locked/frozen
  artifact the project has designated immutable (in this repository,
  the locked private GPT configuration)

State this explicitly to whoever inherits the configuration: **low
friction does not mean unrestricted access.** The two rule categories
above are deliberately asymmetric - broad enough on the safe side to
eliminate repetitive prompts, narrow and explicit enough on the
dangerous side that nothing destructive, privileged, secret-sensitive,
merge-governed, or production-sensitive is ever silently allowed through
because a wildcard happened to match it.

## 2. Codex Low-Friction Bootstrap

The same principle applies to Codex, using its own configuration
surface rather than assuming Claude Code's `settings.local.json` syntax
carries over:

- configure a workspace-scoped sandbox/access boundary at project start,
  not "full access" merely to avoid prompts
- set an approval policy deliberately (which actions require
  confirmation and which proceed automatically) rather than accepting
  whatever the tool's default happens to be
- streamline safe reads, safe edits, and the project's real validation
  commands, mirroring the Claude Code allow list above
- allow ordinary GitHub workflow actions consistent with what the
  repository's governance lets an agent perform autonomously
- retain explicit gates for destructive, system-level, secret-handling,
  and production-facing actions - the same category boundary as
  Section 1, expressed in Codex's own configuration mechanism
- avoid a blanket full-access or "yolo" mode as a shortcut; it produces
  the same accidental-accumulation problem described in "The Central
  Lesson" above, just without even the informal record that ad-hoc
  approval clicks leave behind

Do this at the same time as the Claude Code configuration, as part of
the same first-hour bootstrap pass, not as a follow-up task for later.

## 3. Permission Rules Are Not a Complete Security Control

Command-pattern permission systems (Claude Code's `allow`/`deny` rules,
Codex's approval policy) match on the shape of a command, not its
semantic danger. This delivery surfaced concrete examples of the gap:

- a rule allowing `git push origin *` would, read literally, also match
  a force push or a push to a protected branch embedded in the same
  invocation; the fix was explicit deny rules for those specific
  patterns, not trusting the broader allow rule to stay safe by
  omission
- a deny rule on `psql * -c *DROP*` cannot reliably catch every way a
  destructive SQL statement could be phrased inside a `-c` string -
  pattern matching over free-form command text has a real ceiling
- `deny` rules, once written, are a hard technical block that cannot be
  talked around by conversational instruction in the same session -
  this is a feature, not a limitation, but it means a rule written too
  broadly cannot be selectively relaxed in the moment without either
  editing the settings file (a deliberate, visible, restorable action -
  see the diagnostic-`npm install` example in Section 7) or asking the
  human to run the command directly

**The permission system reduces friction. It does not replace
repository governance, scope discipline, or human judgment at an
approval boundary.** Those remain authoritative exactly as
`AGENTS.md` defines them; the permission profile is an operational aid
that makes following that governance less tedious, not a substitute for
it.

## 4. Developer-Machine Readiness

A newly configured Mac is not engineering-ready merely because the
repository is cloned. This delivery required provisioning Node.js and
PostgreSQL from a machine that had neither, mid-delivery - readiness
gaps discovered this way cost real time that a bootstrap checklist would
have caught in minutes instead.

Required readiness, confirmed before assuming a machine is ready to
work:

- Git installed and configured (user name/email, credential helper)
- GitHub CLI (`gh`) authenticated
- the repository cloned
- `develop` (or the project's integration branch) fetched and
  synchronized
- language/runtime toolchain installed at a version the project
  actually needs (confirm, don't assume - this repository needed a
  specific Node.js version and PostgreSQL major version, not "whatever
  is newest")
- a local database instance running where the project requires one,
  with the project's expected local database(s) created
- a safe, gitignored local secret-storage convention already in place
  and verified ignored **before** any real secret is written to it
  (`git check-ignore -v` the exact path, not an assumption about the
  `.gitignore` pattern's reach)
- Claude Code installed and configured, including the low-friction
  permission profile from Section 1
- Codex installed and configured, including the low-friction profile
  from Section 2
- shell/terminal integration set up where it removes friction (PATH,
  completions, any project-specific shell helpers)
- the project's actual validation suite runnable end to end, once,
  before starting feature work - not assumed runnable because the
  commands exist in a script
- the set of known untracked, local-only directories (IDE/agent state,
  local env files, build output) understood and distinguished from
  actual repository content, so `git status` output is never a surprise

## 5. Multi-Mac Synchronization

**GitHub is the synchronization and handoff point between machines -
never assume local state on one machine.**

Before beginning work on any Mac:

1. `git fetch origin`
2. synchronize the local integration branch safely (fast-forward only;
   never force-reconcile a dirty tree without inspecting it first)
3. verify local `HEAD` against `origin/develop` (or the project's
   equivalent) explicitly, rather than trusting a stale mental model of
   "where things are"

Before switching to a different Mac:

- every piece of tracked work meaningful enough to matter must already
  be committed, pushed, and merged (or explicitly left on a pushed
  feature branch) - a local branch or uncommitted change that exists
  only on one machine does not exist for the purpose of continuing work
  elsewhere
- never assume another Mac already has unpublished work; verify the
  remote, don't infer it

This discipline is what let Render's Blueprint deployment, browser
acceptance, and every fix in between proceed correctly across a session
that spanned repeated human-in-the-loop round trips (Render dashboard
actions, DNS entry, browser testing) without ever losing track of which
machine's state was authoritative - because none of it was: the
repository, synchronized through GitHub, always was.

## 6. Secrets

- `.env` files remain local and gitignored; verify the exact path is
  ignored (`git check-ignore -v <path>`) before writing a real secret
  into it, not after
- never paste a secret into an AI chat session, in either direction -
  when a secret needs to be configured, the correct pattern is: the
  agent verifies and prepares the secure local or platform-native
  storage mechanism, then the human enters the value directly into that
  mechanism, and confirms completion in words only ("configured"), never
  the value itself
- never commit a secret; if one is ever suspected to have been exposed
  (accidentally committed, pasted somewhere it shouldn't have been,
  logged), treat rotation as required, not optional - a suspected
  exposure and a confirmed exposure carry the same obligation, because
  by the time exposure is confirmed the cost of having waited is already
  paid
- cloud deployments use the provider's own environment/secrets
  configuration (this delivery used Render's `sync: false` Blueprint
  field, entered directly in Render's dashboard) - never a value
  embedded in a tracked configuration file, however convenient that
  would be

## 7. Human Approval Boundaries That Proved Valuable

This delivery kept the following gated behind explicit Repository
Author action throughout, even while every other routine action was
streamlined, and the combination consistently delivered both speed and
control:

- **PR merge into a governed branch** - every merge in this delivery
  (five pull requests across the deployment work) was performed by the
  Repository Author directly, blocked at the tool level by a Claude Code
  `deny` rule the agent had itself configured. When explicitly
  instructed to proceed anyway, the agent did not attempt to talk its
  way around the technical block (which is not possible) or silently
  edit the rule to bypass it; it explained the block and asked the human
  to act directly. This is the intended behavior, not friction to be
  optimized away.
- **Credentials and authentication** - OpenAI API key entry, Render
  account authentication, and GitHub authentication were never requested
  in chat and never performed by the agent.
- **DNS** - the exact Hostinger CNAME record was provided to the
  Repository Author to enter manually; DNS was never automated or
  guessed at.
- **Cloud account actions** - Render Blueprint connection and service
  creation were described as exact dashboard steps for the Repository
  Author to click, not performed via an API credential the agent held.
- **Production-sensitive and destructive operations** - remained gated
  throughout, matching Section 1's deny list.

One narrow, deliberate exception is worth recording precisely because it
was an exception: diagnosing the Render build failure required a real
`npm install` under production-like conditions to reproduce and verify
the fix. The agent's own `deny` rule blocked this even inside a
throwaway scratch clone that never touched the tracked repository. On
explicit Repository Author authorization for that specific, narrow,
reversible action, the agent temporarily removed the relevant deny
entries, performed the verification, and restored them immediately
afterward - transparently, as a visible, intentional, logged action, not
a silent or permanent weakening. That pattern - narrow, explicit,
temporary, restored - is the correct way to handle a genuine gap between
a deliberately strict default and a legitimate one-off need, and it is
preferable to either refusing the diagnostic entirely or loosening the
rule permanently.

## Bootstrap Acceptance Criterion

A future project's AI-assisted development setup should be measured
against one concrete criterion:

> **AI-assisted development setup is not complete until routine
> repository work can proceed without repetitive approval prompts,
> while destructive, privileged, secret-sensitive, merge-governed, and
> production-sensitive actions remain explicitly gated.**

Neither half is optional. A setup that still prompts for every `git
status` has not actually removed friction. A setup that auto-approves
`git push --force` or a database drop has not actually preserved
control. Both failure modes were observed and corrected during this
delivery; this document exists so the next project starts from the
corrected state instead of rediscovering both failure modes again.
