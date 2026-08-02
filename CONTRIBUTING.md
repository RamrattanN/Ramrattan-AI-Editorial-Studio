# Contributing

Thank you for contributing to Ramrattan AI Editorial Studio.

Trust before convenience.

The repository is the source of truth for repository state. Contributions
follow the Constitution and the Capability Delivery Workflow.

## Authority and Required Reading

Nilesh's current request defines the maximum scope and authorization for a
task. Repository governance defines how authorized work is performed.

Before capability work, read:

- `AGENTS.md`
- `AGENT_MEMORY.md`
- `CONTRIBUTING.md`
- `docs/constitution/Constitution.md`
- `docs/constitution/Canonical_Vocabulary.md`
- `docs/engineering/Capability_Delivery_Workflow.md`
- the current architecture baseline and relevant ADRs
- the active capability plan, roadmap, and scorecard

`AGENTS.md` is the operational agent contract. `AGENT_MEMORY.md` is
advisory experience and never overrides normative repository guidance.

## Development Model

- `main` contains stable releases.
- `develop` contains integrated work for the next release.
- Feature and documentation branches contain one focused increment.

Verify a clean, synchronized `develop` before branch creation. Treat
pre-existing changes as Nilesh's work and never discard, overwrite, stage,
or relocate them without explicit authorization.

Recommended branch names:

```text
feature/short-description
docs/short-description
fix/short-description
test/short-description
```

## Capability Delivery Workflow

Use `scripts/capability_delivery.py` to determine the next safe state. Do
not reconstruct or skip the workflow manually.

The canonical lifecycle is:

1. Verify baseline.
2. Create or resume the feature branch.
3. Create the bootstrap.
4. Preview.
5. Apply.
6. Recover from partial apply when necessary.
7. Validate.
8. Synchronize GitHub planning.
9. Review local changes.
10. Stage and review staged changes.
11. Commit.
12. Push.
13. Create or reuse the pull request.
14. Wait for successful CI and required review state.
15. Merge and delete the feature branch.
16. Return to clean, synchronized `develop`.
17. Synchronize completion planning.

Resume from the helper's verified state. Recover a partial transition
instead of restarting it.

## Autonomous Work and Approval Boundaries

Inspection, in-scope editing, bootstrap preview and apply, validation,
non-destructive repair, and diff review may proceed autonomously once the
phase is authorized.

Explicit Nilesh approval is required before:

- staging changes with `git add`;
- commit;
- push;
- creating or mutating a pull request;
- merge;
- deleting branches;
- creating, editing, closing, or reopening issues;
- changing GitHub Project or milestone state;
- changing the frozen Constitution or Canonical Vocabulary;
- publication or external submission;
- dependency installation; or
- destructive or difficult-to-recover operations.

An approval applies only to the described action, targets, and verified
state.

## Validation

Before staging or commit, all contributions must pass:

```bash
python3 -m compileall -q studio scripts tests
python3 -m unittest discover -s tests -v
python3 studio.py validate
```

Repair failures within scope, regenerate when required, and rerun the
complete suite. A merge, regeneration, or code change invalidates earlier
validation.

## Generated Files

Bootstrap scripts are canonical for the files and managed sections they
declare. Generated artifacts are derived.

When generated behavior or documentation changes:

1. Update every affected implementation or document.
2. Update every owning generator.
3. Regenerate.
4. Validate.
5. Confirm the repair survives regeneration.

Never repair only a generated artifact or only its generator.

## Governance and Architecture

Create or update an ADR when a change establishes a lasting constraint,
changes the system model, changes governance authority, or rejects a
credible alternative.

Update the architecture baseline only when executable architecture changes.
Governance-only clarification does not require a new baseline.

Planning and status artifacts are maintained by the capability that changes
their facts. Do not create a separate reconciliation exercise unless it is
explicitly required.

## Commits and Pull Requests

Use a concise conventional commit message for one coherent increment.

Pull requests must explain:

- summary;
- problem;
- rationale;
- changes;
- validation;
- architecture decision impact;
- related issues; and
- rollback.

CI must pass before merge.

## Stopping Conditions

Stop when the requested phase is complete, the next action is protected, a
conflict requires Nilesh's judgment, unrelated work makes continuation
unsafe, validation cannot be repaired within scope, or the task would
materially exceed its approved budget.

## Engineering Principles

Prefer deterministic behavior, explicit state, reproducible workflows,
repository evidence, focused changes, and comprehensive behavioral tests.

Participation is governed by [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
