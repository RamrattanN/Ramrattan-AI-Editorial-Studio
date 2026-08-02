# Version 1.0 Scorecard

## Purpose

This scorecard tracks whether Version 1.0 can complete the
Canonical Editorial Session.

## Constitutional Foundation

| Area | Status | Evidence |
|---|---|---|
| Constitution | Complete | `docs/constitution/Constitution.md` |
| Human Collaboration Model | Complete | `docs/constitution/Human_Collaboration_Model.md` |
| Author Journey | Complete | `docs/constitution/Author_Journey.md` |
| Editor Journey | Complete | `docs/constitution/Editor_Journey.md` |
| Editor Charter | Complete | `docs/constitution/Editor_Charter.md` |
| Reader Experience Principles | Complete | `docs/constitution/Reader_Experience_Principles.md` |
| Editorial Behaviour Standard | Complete | `docs/constitution/Editorial_Behaviour_Standard.md` |
| Editorial Language Framework | Complete | `docs/constitution/Editorial_Language_Framework.md` |
| Editorial Fingerprint | Complete | `docs/constitution/Editorial_Fingerprint.md` |
| Canonical Editorial Session | Complete | `docs/constitution/Canonical_Editorial_Session.md` |
| Constitutional Governance | Complete | ADR-006 |

## Version 1.0 Runtime

| Area | Status | Planned Capability |
|---|---|---|
| Editorial Workspace | Complete | Capability 007 runtime |
| Editorial Intake | Complete | Capability 007 runtime |
| Source Assessment | Complete | Capability 007 runtime |
| Evidence Validation | Complete | Capability 008 runtime |
| LMHS Editorial Risk | Complete | Capability 008 runtime |
| Editorial Confidence Translation | Complete | Capability 008 runtime |
| Article Engine | Planned | Capability 009 |
| Publication Package | Planned | Capability 009 |
| Hero Visual System | Planned | Capability 010 |
| Component Collaboration | Planned | Capabilities 009-010 |
| Portable Project Export | Planned | Capability 011 |
| Resume Existing Project | Planned | Capability 011 |
| End-to-End Demo | Planned | Version 1.0 Release Readiness |

## Release Rule

Version 1.0 is not ready until every runtime area required by the
Canonical Editorial Session is complete and demonstrable.

<!-- CAPABILITY_007_SCORECARD_START -->

## Capability 007 Progress

| Area | Status | Evidence |
|---|---|---|
| Canonical Vocabulary | Complete | `docs/constitution/Canonical_Vocabulary.md` |
| Editorial Workspace | Complete | `studio/editorial_intake.py` |
| Natural Editorial Intake | Complete | Runtime tests |
| Understanding your input | Complete | Runtime tests |
| Assessing your sources | Complete | Runtime tests |
| Optional logo | Complete | Runtime tests |
| Optional headshot | Complete | Runtime tests |
| Rights confirmation | Complete | Runtime tests |
| Resume without assets | Complete | Runtime tests |
| Evidence verification | Planned | Capability 008 |

<!-- CAPABILITY_007_SCORECARD_END -->

<!-- CAPABILITY_DELIVERY_SCORECARD_START -->

## Engineering Delivery Readiness

| Area | Status | Evidence |
|---|---|---|
| Delivery workflow | Complete | `docs/engineering/Capability_Delivery_Workflow.md` |
| State-aware helper | Complete | `scripts/capability_delivery.py` |
| Exact command resolution | Complete | Automated tests |
| Existing branch detection | Complete | Automated tests |
| Pull-request discovery | Complete | Automated tests |
| CI gating | Complete | Automated tests |
| Merge cleanup standard | Complete | Delivery workflow |
| Return-to-develop verification | Complete | Delivery workflow |

<!-- CAPABILITY_DELIVERY_SCORECARD_END -->

<!-- CAPABILITY_008_SCORECARD_START -->

## Capability 008 Progress

| Area | Status | Evidence |
|---|---|---|
| Editorial Intent | Complete | Runtime tests |
| Editorial Discernment | Complete | `studio/editorial_discernment.py` |
| Editorial Guidance | Complete | `studio/editorial_guidance.py` |
| Editorial Coherence Guard | Complete | Runtime tests |
| No Silent Scope Expansion | Complete | Runtime and constitutional tests |
| Workspace lifecycle | Complete | Runtime tests |
| Approved-component protection | Complete | Runtime tests |
| One-question clarification | Complete | Runtime tests |
| Evidence Validation | Complete | `studio/evidence_validation.py` |
| Claim Classification | Complete | Runtime tests |
| Corroboration | Complete | Independence tests |
| Temporal Integrity | Complete | Time-sensitive evidence tests |
| LMHS Editorial Risk | Complete | All-level risk tests |
| Editorial Confidence Translation | Complete | Publication-gate tests |

<!-- CAPABILITY_008_SCORECARD_END -->

<!-- CAPABILITY_008A1_SCORECARD_START -->

## Capability 008A Engineering Hardening Status

- Capability 008 - Complete
- Capability 008A.1 - Governance Consolidation - In Progress
- Capability 008A.2 - Delivery Hardening - Not started
- Capability 008A.3 - Editorial Integrity Hardening - Not started
- Capability 009 - Not started

| Governance area | Status | Evidence |
|---|---|---|
| Agent operating contract | Complete | `AGENTS.md` and governance tests |
| Advisory memory lifecycle | Complete | `AGENT_MEMORY.md` |
| Contributor workflow alignment | Complete | `CONTRIBUTING.md` |
| Governance authority | Complete | ADR-011 |
| ADR-002 reference integrity | Complete | Baseline v01 direct architecture reference |
| Current baseline | Complete | `2026.08.01v06` |

Capability 008A.1 changes governance and status integrity only. It does not
advance product-runtime release readiness.

<!-- CAPABILITY_008A1_SCORECARD_END -->

<!-- CAPABILITY_008A2_SCORECARD_START -->

## Capability 008A Delivery Hardening Status

- Capability 008A.1 - Complete
- Capability 008A.2 - In Progress
- Capability 008A.3 - Todo
- Capability 009 - Todo

| Delivery area | Status | Evidence |
|---|---|---|
| Fail-closed discovery | Complete | Helper and high-risk workflow tests |
| Remote freshness | Complete | Direct remote observation tests |
| Draft and review readiness | Complete | PR #30, #31, and #33 regressions |
| Mergeability gating | Complete | Conflict, blocked, and unknown tests |
| CI outcome gating | Complete | All check-state tests and CI workflow |
| Post-merge recovery | Complete | Cleanup state tests |
| Delivery architecture | Complete | ADR-012 and baseline v07 |

Capability 008A.2 changes engineering delivery safety only. Version 1.0
product-runtime readiness remains unchanged.

<!-- CAPABILITY_008A2_SCORECARD_END -->

<!-- CAPABILITY_008A3_SCORECARD_START -->

## Capability 008A Editorial Integrity Hardening Status

- Capability 008A.1 - Complete
- Capability 008A.2 - Complete
- Capability 008A.3 - In Progress
- Capability 009 - Todo

| Editorial integrity area | Status | Evidence |
|---|---|---|
| Earned Verified Fact | Complete | Claim transition tests |
| Durable Author attribution | Complete | Classification contract tests |
| Distinct-source corroboration | Complete | Duplicate identity tests |
| Semantic classification preservation | Complete | Inference, forecast, and uncertainty tests |
| Contradiction severity | Complete | Material and non-material risk tests |
| Publication blocking | Complete | High and Severe gate tests |
| Editorial Confidence translation | Complete | Author-message tests |
| Canonical StageState | Complete | Cross-component identity and transition tests |
| Editorial architecture | Complete | ADR-013 and baseline v08 |

Capability 008A.3 hardens existing Version 1.0 editorial behavior. It does not
begin the Article Engine, Publication Package, or any Capability 009 scope.

<!-- CAPABILITY_008A3_SCORECARD_END -->
