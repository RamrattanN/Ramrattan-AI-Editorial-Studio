# Capability 008A - Engineering Hardening Program

## 1. Executive Summary

Capability 008A hardens the foundations established through Capability 008
before Capability 009 expands the product surface.

The completed repository reviews identified three distinct classes of risk:

1. Governance authority and documentation can drift or become ambiguous.
2. The Capability Delivery helper can misinterpret incomplete repository or
   GitHub state.
3. Evidence Validation and editorial workflow semantics contain correctness
   and consistency risks.

Combining these concerns into one capability would create an oversized change
spanning governance, delivery automation, product runtime, architecture,
generators, and tests. It would also make failures harder to isolate and
approval boundaries harder to review.

Capability 008A is therefore divided into three ordered increments:

- Capability 008A.1 - Governance Consolidation
- Capability 008A.2 - Delivery Hardening
- Capability 008A.3 - Editorial Integrity Hardening

Each increment has one primary concern, a hard file budget of approximately
10-15 files, and an explicit handoff condition. The series must complete
before Capability 009 begins.

## Capability 008A Principles

1. One concern per increment.
2. One authoritative owner for every concept.
3. No increment may exceed its approved scope.
4. Every increment must leave develop cleaner than it found it.
5. Capability 009 shall begin only after all Capability 008A success criteria
   are satisfied.

## 2. Repository Starting State

Verified starting state after PR #30:

- Active branch: `develop`
- Working tree: clean
- Local `develop`: synchronized with `origin/develop`
- Current commit: `7b9f7189ef2e5826c3e904ddc243e630f9c046b5`
- PR #30: merged with a merge commit
- PR #30 feature branch: deleted locally and remotely
- Capability 008: complete
- Capability 008 implementation PR: #29
- Capability 008 validation at completion: 158 tests passing
- Issue #14: closed after Capability 008 planning synchronization
- `AGENTS.md`: complete governance version from PR #30
- Capability 009: next planned product capability
- Capability 008A: approved in principle but not started
- No Capability 008A implementation branch exists
- No Capability 008A implementation or GitHub planning changes have begun

Capability 008A begins from this clean, synchronized `develop` baseline.

## 3. Increment Overview

### Capability 008A.1 - Governance Consolidation

#### Objective

Establish an unambiguous, testable governance authority model across
`AGENTS.md`, `AGENT_MEMORY.md`, `CONTRIBUTING.md`, delivery guidance,
architectural records, and current-status documentation.

#### Scope

- Validate the structural integrity of `AGENTS.md`.
- Clarify `AGENT_MEMORY.md` as advisory memory subordinate to current
  repository authority.
- Align `CONTRIBUTING.md` with approval boundaries, validation requirements,
  generator ownership, dirty-tree protections, and stopping conditions.
- Remove or reconcile duplicated normative governance instructions.
- Define the lifecycle and update responsibility of governance documents.
- Reconcile current capability, roadmap, scorecard, ADR index, baseline
  references, and release-status documentation.
- Investigate the broken ADR-002 reference without inventing repository
  history.
- Add focused governance contract tests.
- Create a deterministic bootstrap for this increment.

#### Exclusions

- Product runtime changes
- Capability Delivery helper behavior
- Evidence Validation semantics
- StageState consolidation
- Capability 009 implementation
- General documentation rewriting unrelated to governance integrity

#### Estimated Effort

Two focused working days.

#### Estimated File Impact

Approximately 12-15 files, including its bootstrap and tests.

#### Required ADR

ADR-011 - Governance Authority.

ADR-011 must remain narrowly scoped to authority, precedence, document roles,
lifecycle, and enforcement. It must not define delivery-helper or editorial
runtime behavior.

#### Required Architecture Baseline

No new architecture baseline.

#### Expected Validation

- `AGENTS.md` structural and balanced-fence validation
- Governance precedence and cross-document consistency tests
- Dirty-tree and approval-boundary documentation checks
- ADR and current-status reference checks
- Bootstrap preview, apply, regeneration, and idempotence checks
- Complete repository validation:

```text
python3 -m compileall -q studio scripts tests
python3 -m unittest discover -s tests -v
python3 studio.py validate
```

#### Exact Handoff Condition

Capability 008A.1 may hand off to 008A.2 only when:

- ADR-011 is accepted and recorded.
- Governance documents have consistent authority and terminology.
- `AGENT_MEMORY.md` has an explicit advisory role and lifecycle.
- Current capability, roadmap, scorecard, ADR index, baseline references, and
  release-status documentation agree.
- Governance structural tests pass.
- Generated files and the 008A.1 bootstrap are synchronized.
- The increment is merged.
- Its feature branch is deleted locally and remotely.
- `develop` is clean and synchronized with `origin/develop`.
- GitHub planning marks 008A.1 complete and 008A.2 as the next active
  increment.

### Capability 008A.2 - Delivery Hardening

#### Objective

Make the Capability Delivery helper fail closed, distinguish unavailable state
from absent state, improve recovery, and ensure delivery decisions are based
on complete local and GitHub evidence.

#### Scope

- Introduce explicit discovery results such as `FOUND`, `NOT_FOUND`, and
  `UNAVAILABLE`.
- Verify remote freshness before state transitions that depend on the remote
  repository.
- Model draft state, review readiness, mergeability, and check availability
  explicitly.
- Treat zero reported checks as unavailable unless repository policy proves
  that no checks are required.
- Detect and block ambiguous multiple-PR conditions.
- Handle malformed or incomplete GitHub responses safely.
- Improve recovery following partial merge, branch deletion, or
  synchronization operations.
- Expand CI so the canonical complete validation suite runs.
- Reduce unnecessary Author pauses by identifying safe read-only transitions
  and presenting coherent approval bundles.
- Add focused high-risk workflow tests.
- Keep the delivery helper and its canonical bootstrap synchronized.

#### Exclusions

- GitHub Project redesign
- Automatic approval of protected operations
- Product runtime or editorial behavior
- StageState changes
- Release packaging
- Performance engineering
- Version 2 generator consolidation

#### Estimated Effort

Two to three focused working days.

#### Estimated File Impact

Approximately 11-14 files, including generator and high-risk workflow tests.

#### Required ADR

ADR-012 - Delivery Hardening.

#### Required Architecture Baseline

Architecture Baseline v07.

#### Expected Validation

- Delivery state-transition tests
- GitHub failure-versus-absence tests
- Remote freshness tests
- Draft, mergeability, and check-availability tests
- Multiple-PR and malformed-response tests
- Post-merge recovery tests
- CI workflow inspection
- Bootstrap preview, apply, regeneration, and idempotence checks
- Complete repository validation:

```text
python3 -m compileall -q studio scripts tests
python3 -m unittest discover -s tests -v
python3 studio.py validate
```

#### Exact Handoff Condition

Capability 008A.2 may hand off to 008A.3 only when:

- ADR-012 is accepted and recorded.
- Architecture Baseline v07 is current.
- The helper fails closed when repository or GitHub state is unavailable or
  ambiguous.
- Required approval boundaries remain explicit.
- Recovery paths are deterministic and tested.
- CI runs the complete canonical validation suite.
- Generated delivery files and their bootstrap remain synchronized.
- The increment is merged.
- Its feature branch is deleted locally and remotely.
- `develop` is clean and synchronized with `origin/develop`.
- GitHub planning marks 008A.2 complete and 008A.3 as the next active
  increment.

### Capability 008A.3 - Editorial Integrity Hardening

#### Objective

Correct Evidence Validation semantics, strengthen corroboration and editorial
risk behavior, and replace duplicated workflow-stage representations with one
canonical StageState model.

#### Scope

- Make Verified Fact an earned classification rather than a caller-selected
  starting state.
- Preserve distinctions among source assertion, author experience, author
  opinion, inference, forecast, and uncertainty.
- Prevent inference, forecast, and uncertainty from becoming Verified Fact
  merely through corroboration.
- Prevent duplicate source identifiers from manufacturing independent
  corroboration.
- Define contradiction severity consistently.
- Require material contradictions to produce Severe editorial risk.
- Ensure Low risk contains no actionable finding.
- Preserve High and Severe risk as publication-blocking states.
- Translate internal LMHS editorial risk into clear Author-facing Editorial
  Confidence without obscuring blocking conditions.
- Introduce a canonical shared StageState model.
- Consolidate stage names, ordering, and allowed transitions across affected
  runtime components.
- Keep persistent workspace state distinct from transient stage execution
  state.
- Add focused evidence and stage-integration behavioral tests.
- Synchronize every affected generated artifact with its canonical bootstrap.
- Reconcile editorial architecture documentation and recorded decisions.

#### Exclusions

- Article Engine
- Publication Package
- Component Collaboration
- Hero Visual
- Portable Project
- Real ingestion
- User interface work
- Release packaging
- Performance engineering
- Version 2 generator consolidation

#### Estimated Effort

Two to three focused working days.

#### Estimated File Impact

Approximately 13-15 files. The implementation must consolidate tests and
documentation deliberately to remain within this hard budget.

#### Required ADR

ADR-013 - Editorial Integrity.

#### Required Architecture Baseline

Architecture Baseline v08.

#### Expected Validation

- Claim-classification transition tests
- Corroboration-independence tests
- Contradiction and editorial-risk tests
- Publication-blocking behavior tests
- Author-facing Editorial Confidence translation tests
- Canonical StageState integration tests
- Invalid transition and invalid ordering tests
- Cross-component stage consistency tests
- Bootstrap preview, apply, regeneration, and idempotence checks
- Complete repository validation:

```text
python3 -m compileall -q studio scripts tests
python3 -m unittest discover -s tests -v
python3 studio.py validate
```

#### Exact Handoff Condition

Capability 008A.3 may hand off to Capability 009 only when:

- ADR-013 is accepted and recorded.
- Architecture Baseline v08 is current.
- Evidence classifications cannot overstate evidentiary certainty.
- Corroboration requires genuinely distinct sources.
- Editorial risk and Author-facing Editorial Confidence remain consistent.
- High and Severe risk reliably block publication.
- StageState is canonical across the affected runtime.
- Generated files and all affected bootstraps are synchronized.
- The complete validation suite passes.
- The increment is merged.
- Its feature branch is deleted locally and remotely.
- `develop` is clean and synchronized with `origin/develop`.
- GitHub planning marks Capability 008A complete and Capability 009 as the
  active next capability.

## 4. Dependency Diagram

```text
Capability 008
        ↓
Capability 008A.1
Governance Consolidation
        ↓
Capability 008A.2
Delivery Hardening
        ↓
Capability 008A.3
Editorial Integrity Hardening
        ↓
Capability 009
```

The order is mandatory:

- Delivery hardening depends on the governance authority established by
  008A.1.
- Editorial hardening must use the safer delivery workflow established by
  008A.2.
- Capability 009 must consume the corrected editorial semantics and canonical
  StageState established by 008A.3.

## 5. Findings Mapping

This ledger consolidates the accepted recommendations from the six completed
reviews. Each finding appears exactly once.

Review sources:

- R1 - Repository Health Review
- R2 - Technical Debt Review
- R3 - Version 1 Release Review
- R4 - `AGENTS.md` and `AGENT_MEMORY.md` Governance Review
- R5 - Capability 008 Workflow Review
- R6 - Capability 009 and Capability 008A Design Review

### Capability 008A.1 - Governance Consolidation

| ID | Accepted finding | Source | Disposition |
|---|---|---|---|
| F01 | Protect `AGENTS.md` against truncation, malformed structure, and unbalanced fences. | R1, R4 | Add structural governance validation. |
| F02 | Make repository authority, constitutional precedence, current-task authority, and conversation precedence unambiguous. | R4 | Define through ADR-011 and aligned governance text. |
| F03 | Define `AGENT_MEMORY.md` as advisory memory with an explicit lifecycle and subordinate authority. | R4 | Reconcile `AGENT_MEMORY.md` and its maintenance rules. |
| F04 | Remove duplicated or competing normative governance instructions. | R1, R4 | Establish one authoritative rule location with references elsewhere. |
| F05 | Align `CONTRIBUTING.md` with approval boundaries, validation, generator ownership, dirty-tree protection, autonomy, and stopping conditions. | R1, R4, R5 | Reconcile contributor workflow guidance. |
| F06 | Add automated checks for governance structure and critical governance clauses. | R1, R2, R4 | Add focused governance contract tests. |
| F07 | Reconcile current capability, roadmap, scorecard, release-status, and Version 1 status statements. | R1, R3, R6 | Update only the affected planning authorities. |
| F08 | Repair the ADR index and investigate the broken ADR-002 reference without inventing history. | R1, R2, R4 | Investigate history and repair reference integrity. |
| F09 | Clarify repository version identity where status documents disagree about Version 1 completion or readiness. | R1, R3 | Establish one current release-status statement. |

### Capability 008A.2 - Delivery Hardening

| ID | Accepted finding | Source | Disposition |
|---|---|---|---|
| F10 | The delivery helper can confuse GitHub failure or unavailability with confirmed absence. | R1, R2, R5 | Introduce explicit discovery-result states. |
| F11 | Remote-dependent decisions can be made without proving remote freshness. | R2, R5 | Require freshness evidence before dependent transitions. |
| F12 | Draft and review-ready PR states are not modeled strongly enough. | R2, R5 | Add explicit PR readiness handling. |
| F13 | Mergeability is insufficiently represented in workflow decisions. | R2, R5 | Treat mergeability as required evidence before merge. |
| F14 | Zero checks can be mistaken for successful CI. | R2, R3, R5 | Distinguish successful checks, no required checks, and unavailable checks. |
| F15 | Multiple matching PRs and malformed GitHub responses can produce unsafe state selection. | R2, R5 | Fail closed on ambiguity or invalid data. |
| F16 | Partial merge and branch-cleanup operations need safer recovery paths. | R1, R5 | Add deterministic recovery and post-operation verification. |
| F17 | CI should run the same complete validation suite required before commit. | R1, R3, R5 | Align CI with canonical validation. |
| F18 | Safe read-only automation and coherent approval bundles can reduce unnecessary Author pauses. | R5 | Automate inspection and validation while preserving protected boundaries. |
| F19 | Planning synchronization and bootstrap behavior need clearer idempotence and recovery. | R1, R2, R5 | Harden synchronization and generation behavior. |
| F20 | High-risk workflow paths lack sufficient behavioral tests. | R1, R2, R5 | Add state-machine and failure-mode tests. |

### Capability 008A.3 - Editorial Integrity Hardening

| ID | Accepted finding | Source | Disposition |
|---|---|---|---|
| F21 | Verified Fact must be earned from evidence and cannot be selected as an unsupported initial classification. | R1, R2, R3, R6 | Correct claim-classification transitions. |
| F22 | Inference, forecast, and uncertainty must not become Verified Fact merely through corroboration. | R1, R3, R6 | Preserve semantic classification boundaries. |
| F23 | Author experience and author opinion require distinct, durable attribution semantics. | R3, R6 | Preserve their classifications and provenance. |
| F24 | Duplicate source identifiers must not count as independent corroboration. | R1, R2, R3 | Deduplicate corroboration by source identity. |
| F25 | Contradictions must produce consistent risk, with material contradictions classified as Severe. | R1, R3, R6 | Correct contradiction-to-risk rules. |
| F26 | Low risk must contain no actionable concern, while High and Severe remain publication-blocking. | R1, R3, R6 | Align risk findings and publication gates. |
| F27 | Duplicated StageState definitions create architectural and behavioral drift. | R1, R2, R6 | Introduce one canonical StageState. |
| F28 | Stage names, ordering, and allowed transitions need shared validation. | R1, R2, R6 | Centralize stage vocabulary and transition rules. |
| F29 | Evidence and workflow-stage behavior lacks enough high-risk behavioral coverage. | R1, R2, R3 | Add focused evidence and integration tests. |
| F30 | Runtime repairs must survive regeneration across every affected bootstrap. | R1, R2, R6 | Synchronize runtime and canonical generators. |
| F31 | Editorial decisions, runtime documentation, ADRs, and the active baseline must agree. | R1, R3, R6 | Record ADR-013 and Architecture Baseline v08. |

### Deferred Findings

| ID | Deferred finding | Source | Destination |
|---|---|---|---|
| F32 | Build an integrated Editorial Workspace and adaptive context model. | R1, R3, R6 | Capability 009 |
| F33 | Implement the Article Engine and Publication Package. | R3, R6 | Capability 009 |
| F34 | Implement Component Collaboration, alternatives, and dependency-aware coordination. | R3, R6 | Capability 009 |
| F35 | Define the stable author-facing orchestration API for the integrated editorial flow. | R1, R2, R6 | Capability 009 |
| F36 | Finalize Author-facing Editorial Confidence presentation within the complete editorial workflow. | R3, R6 | Capability 009 |
| F37 | Implement Hero Visual generation and its visual collaboration workflow. | R3, R6 | Capability 010 |
| F38 | Define Hero Visual prompts, dimensions, provenance, and failure behavior. | R1, R3 | Capability 010 |
| F39 | Implement Portable Project serialization and deterministic resume. | R1, R3, R6 | Capability 011 |
| F40 | Add version compatibility, migration, archive, and ZIP behavior for portable projects. | R2, R3 | Capability 011 |
| F41 | Enforce temporal-integrity and stale-evidence policies when projects resume. | R1, R3, R6 | Capability 011 |
| F42 | Replace fixtures-only input with real URL, document, and media ingestion. | R1, R3 | Version 1 Release Readiness |
| F43 | Add source credibility, provider provenance, privacy, and ingestion threat controls. | R1, R2, R3 | Version 1 Release Readiness |
| F44 | Complete the usable UI, accessibility, error handling, and Author interaction flow. | R3 | Version 1 Release Readiness |
| F45 | Establish installation, packaging, release artifacts, tagging, rollback, and distribution procedures. | R2, R3 | Version 1 Release Readiness |
| F46 | Add full-session integration, acceptance, and release demonstration coverage. | R1, R3 | Version 1 Release Readiness |
| F47 | Define and measure Version 1 performance and reliability targets, including the ten-minute objective. | R1, R3 | Version 1 Release Readiness |
| F48 | Add broader security, accessibility, provider-integration, and performance test domains. | R1, R2, R3 | Version 1 Release Readiness |
| F49 | Complete known-limitations, release-checklist, and release-blocker verification. | R1, R3 | Version 1 Release Readiness |
| F50 | Consolidate generators into a Version 2 declarative generation system. | R1, R2, R6 | Version 2 |
| F51 | Consolidate duplicated script, project-field, and test-helper infrastructure. | R1, R2 | Version 2 |
| F52 | Modernize brittle documentation tests beyond the targeted 008A governance contracts. | R1, R2 | Version 2 |
| F53 | Remove or redesign obsolete workflow compatibility surfaces after public API stabilization. | R1, R2 | Version 2 |
| F54 | Perform broad historical roadmap and archive normalization beyond current-status reconciliation. | R1, R2 | Version 2 |

## 6. ADR Plan

### ADR-011 - Governance Authority

ADR-011 shall be narrowly scoped to:

- authority and precedence;
- roles of `AGENTS.md`, `AGENT_MEMORY.md`, `CONTRIBUTING.md`, the
  Constitution, ADRs, baselines, and capability workflow documents;
- lifecycle and ownership of governance documents;
- enforcement and structural validation;
- resolution of conflicting instructions.

It shall not define delivery-helper behavior or product editorial semantics.

### ADR-012 - Delivery Hardening

ADR-012 shall define:

- explicit workflow discovery states;
- failure-versus-absence semantics;
- remote freshness requirements;
- PR readiness, mergeability, and CI evidence;
- ambiguity handling;
- recovery behavior;
- approval-boundary preservation.

### ADR-013 - Editorial Integrity

ADR-013 shall define:

- evidence-classification semantics;
- corroboration independence;
- contradiction severity;
- LMHS editorial risk;
- Author-facing Editorial Confidence translation;
- publication blocking;
- canonical StageState ownership and transition rules.

### ADR-002 Reference Integrity

Do not recreate ADR-002.

> Investigate ADR-002 reference integrity. Restore only if historical evidence
> exists. Otherwise repair the broken reference without inventing repository
> history.

## 7. Baseline Strategy

### Capability 008A.1

No new architecture baseline.

This increment changes governance authority and documentation consistency, not
executable system architecture. ADR-011 is sufficient to record the authority
decision. Existing baseline references may be corrected, but no new baseline
version is created.

### Capability 008A.2

Architecture Baseline v07.

Delivery Hardening changes the architecture of repository delivery state
discovery, transition validation, GitHub evidence handling, recovery, and CI
enforcement. These are durable operational architecture changes and require a
new baseline.

### Capability 008A.3

Architecture Baseline v08.

Editorial Integrity Hardening changes product-domain semantics and shared
runtime structure. Evidence classification, editorial risk, publication
blocking, and canonical StageState are architectural contracts consumed by
later capabilities. They require a separate baseline following v07.

## 8. Capability Budget

The following are hard limits:

| Increment | File budget | Effort target |
|---|---:|---:|
| Capability 008A.1 | Approximately 10-15 files | Two focused working days |
| Capability 008A.2 | Approximately 10-15 files | Two to three focused working days |
| Capability 008A.3 | Approximately 10-15 files | Two to three focused working days |

Bootstrap files, generated artifacts, tests, documentation, ADRs, and
baselines all count toward the file budget.

If implementation exceeds a target by a material amount, implementation must
stop before adding further scope. The increment must be reviewed and re-scoped
with explicit Nilesh approval before continuing.

The budget may not be bypassed by splitting one logical change into
superficial files or by postponing required generator synchronization.

## 9. Planning Principles

- Planning artifacts are maintained by the capability that changes the facts
  recorded in them.
- Governance status is reconciled by 008A.1.
- Delivery architecture and workflow status are reconciled by 008A.2.
- Editorial architecture and final Capability 008A status are reconciled by
  008A.3.
- Planning artifacts are not reconciled through a separate documentation-only
  exercise unless explicitly required.
- Each increment updates only the planning records affected by its decisions.
- Historical documents must not be rewritten to imply decisions or events
  unsupported by repository evidence.
- Bootstraps remain the canonical source for generated artifacts.
- Every increment must prove that its changes survive regeneration.
- Protected operations retain explicit Nilesh approval boundaries.
- Capability 009 cannot begin until the entire 008A series satisfies its
  success criteria.

## 10. Deferred Work

### Capability 009

- Integrated Editorial Workspace
- Adaptive Context
- Article Engine
- Publication Package
- Component Collaboration
- Alternative generation and dependency-aware coordination
- Stable author-facing orchestration API
- Final Author-facing Editorial Confidence presentation in the integrated
  workflow

### Capability 010

- Hero Visual
- Visual collaboration
- Prompt, provenance, dimension, and failure contracts for generated visuals

### Capability 011

- Portable Project
- Deterministic serialization and resume
- Version compatibility and migration
- Archive and ZIP behavior
- Temporal-integrity and stale-evidence enforcement during resume

### Version 1 Release Readiness

- Real URL, document, and media ingestion
- Provider integration
- Source credibility and provenance controls
- Privacy and ingestion threat controls
- Complete UI and accessibility
- Author-facing error recovery
- Installation and packaging
- Release artifacts, tagging, rollback, and distribution
- Full-session integration and acceptance testing
- Release demonstrations
- Performance and reliability targets
- Ten-minute workflow validation
- Security, accessibility, provider, and performance test domains
- Known-limitations documentation
- Release checklist and release-blocker verification

### Version 2

- Declarative generator consolidation
- Shared bootstrap infrastructure
- Project-field and test-helper consolidation
- Broad brittle-test modernization
- Obsolete workflow compatibility cleanup
- Historical roadmap and archive normalization beyond current-status needs

## 11. Success Criteria

Capability 008A is complete only when all three increments have been delivered
in order and:

- The repository is on `develop`.
- The working tree is clean.
- Local `develop` matches `origin/develop`.
- Governance authority is explicit, structurally validated, and consistent
  across governed documents.
- `AGENT_MEMORY.md` has a clear advisory role and lifecycle.
- The Capability Delivery helper fails closed on unavailable or ambiguous
  evidence.
- Remote freshness, PR readiness, mergeability, and CI status are verified
  safely.
- Recovery behavior is deterministic and tested.
- Evidence classification semantics prevent unsupported certainty.
- Corroboration requires independent sources.
- Contradictions and LMHS editorial risk behave consistently.
- Author-facing Editorial Confidence does not conceal publication-blocking
  risk.
- StageState is canonical across affected components.
- Generated artifacts and their bootstraps are synchronized.
- ADR-011, ADR-012, and ADR-013 are present and internally consistent.
- Architecture Baseline v07 records Delivery Hardening.
- Architecture Baseline v08 records Editorial Integrity Hardening.
- The complete validation suite is green.
- Each increment has a Capability Delivery Receipt recording:
  - capability or increment;
  - commit;
  - pull request;
  - merge commit;
  - tests;
  - validation;
  - ADR;
  - architecture baseline;
  - repository state;
  - GitHub planning state;
  - delivery profile.
- All Capability 008A pull requests have passed CI and been merged.
- All Capability 008A feature branches have been deleted locally and remotely.
- GitHub planning is synchronized.
- Capability 008A is marked complete.
- Capability 009 becomes the active next capability.

<!-- CAPABILITY_009_SCOPE_CLARIFICATION_START -->

## Capability 009 Scope Clarification

The Repository Author resolved the post-008A Capability 009 scope in
favor of issue #15, ROADMAP, the Version 1 Scorecard, the Capability
008 demo, and the GitHub Project summary.

Capability 009 implements only the Article Engine and Publication
Package. Integrated Editorial Workspace, Adaptive Editorial Context
runtime, Component Collaboration, stable Author-facing orchestration
API, and final integrated Editorial Confidence presentation remain
deferred and may appear only as minimal internal support strictly
necessary for the approved scope. They must not create new product
surface or independent runtime subsystems.

<!-- CAPABILITY_009_SCOPE_CLARIFICATION_END -->
