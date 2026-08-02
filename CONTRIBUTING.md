# Contributing

Thank you for contributing to Ramrattan AI Editorial Studio.

This repository is governed by the Constitution and follows a capability-driven development workflow.

---

# Guiding Principle

Every enhancement must make the product more maintainable, more intuitive, or more valuable.

Trust before convenience.

Repository state is the source of truth.

---

# Before You Begin

Read:

- README.md
- AGENTS.md
- AGENT_MEMORY.md
- docs/constitution/Constitution.md

These documents define both the engineering workflow and the editorial principles.

---

# Development Model

- `main` contains stable releases.
- `develop` contains integrated work for the next release.
- Feature branches contain focused changes.

Recommended branch names:

```text
feature/short-description
docs/short-description
fix/short-description
test/short-description
```

One capability should be developed on one feature branch.

---

# Capability Delivery Workflow

Every capability follows the same lifecycle.

1. Create or resume the feature branch.
2. Implement the capability.
3. Validate the repository.
4. Synchronize the GitHub Project.
5. Review staged changes.
6. Commit.
7. Push.
8. Create or reuse the Pull Request.
9. Wait for successful CI.
10. Merge.
11. Delete the feature branch.
12. Return to a clean `develop` branch.

The canonical workflow is implemented by:

```text
scripts/capability_delivery.py
```

Do not manually reconstruct workflow state.

Always inspect repository state before recommending the next action.

---

# Validation

Every contribution must successfully complete:

- compileall
- unittest
- studio.py validate

Repository validation must succeed before creating a commit.

---

# Generated Files

Where runtime files are generated from bootstrap scripts:

- modify the generator
- regenerate the runtime files
- validate the repository

Do not permanently repair generated files without updating their generator.

Generator and generated output must remain synchronized.

---

# Commit Messages

Use concise conventional prefixes:

```text
feat: add a new capability
docs: improve documentation
fix: correct a defect
test: add or improve tests
refactor: improve internal structure
release: prepare or publish a release
```

One commit should represent one coherent capability increment.

---

# Pull Requests

A pull request should:

- Solve one coherent problem
- Explain why the change is needed
- Describe the implementation
- Include validation notes
- Mention related issues
- Preserve approved behaviour unless explicitly replacing it
- Pass repository validation
- Follow the Capability Delivery Workflow

Merge only after successful CI.

---

# Significant Decisions

Create an Architecture Decision Record when a change:

- Alters the product workflow
- Alters the prompt architecture
- Alters the visual system
- Alters release or versioning policy
- Creates a lasting constraint
- Rejects a credible alternative

Architecture baselines should be updated where required.

---

# Editorial Standards

Contributions should preserve:

- Originality
- Evidence-based claims
- Clear source attribution
- Jargon-light language
- Visual and written alignment
- Brand-neutral output
- Space - hyphen - space
- No en dashes or em dashes in generated editorial copy

Editorial integrity is always preferred over convenience.

---

# AI-Assisted Development

AI agents should follow:

- AGENTS.md
- AGENT_MEMORY.md

Repository inspection takes precedence over conversation history.

Always continue from the verified repository state.

Recommend one verified workflow step at a time.

Avoid asking contributors to repeat completed work.

---

# Engineering Principles

Prefer:

- deterministic behaviour
- explicit state transitions
- reproducible workflows
- repository inspection
- constitutional governance
- small, safe changes
- comprehensive automated testing

Avoid:

- hidden state
- speculative assumptions
- duplicated logic
- silent behaviour changes
- manual workflow reconstruction

---

# Code of Conduct

Participation is governed by [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).