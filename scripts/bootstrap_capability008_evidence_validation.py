#!/usr/bin/env python3
"""Bootstrap the Capability 008 Evidence Validation increment.

Preview changes nothing. ``--apply`` writes deterministic runtime,
documentation, and tests, then runs the complete repository validation.

This script never commits, pushes, changes GitHub planning, creates a pull
request, or merges.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import textwrap
from pathlib import Path


EXPECTED_REPOSITORY = "Ramrattan-AI-Editorial-Studio"
EXPECTED_REMOTE_FRAGMENT = "RamrattanN/Ramrattan-AI-Editorial-Studio"
EXPECTED_BRANCH = "feature/evidence-validation-editorial-risk"
SCRIPT_PATH = "scripts/bootstrap_capability008_evidence_validation.py"
SENTINEL = "CAPABILITY_008_EVIDENCE_VALIDATION_COMPLETE"


def clean(value: str) -> str:
    return textwrap.dedent(value).strip() + "\n"


RUNTIME = clean(r'''
    """Evidence Validation and Editorial Risk for Capability 008.

    The runtime records what is known, what remains uncertain, and whether
    material claims have enough independent, current support. It does not
    perform network research and never converts source presence into a false
    verification claim.
    """

    from __future__ import annotations

    from dataclasses import dataclass
    from datetime import date
    from enum import Enum
    from typing import Iterable


    class ClaimClassification(str, Enum):
        """Editorial meaning of a claim."""

        VERIFIED_FACT = "verified_fact"
        SOURCE_ASSERTION = "source_assertion"
        AUTHOR_EXPERIENCE = "author_experience"
        REASONABLE_INFERENCE = "reasonable_inference"
        OPINION = "opinion"
        FORECAST = "forecast"
        UNRESOLVED_UNCERTAINTY = "unresolved_uncertainty"


    class EvidencePosition(str, Enum):
        """How one source relates to one claim."""

        SUPPORTS = "supports"
        CONTRADICTS = "contradicts"
        CONTEXT_ONLY = "context_only"


    class EvidenceStatus(str, Enum):
        """Result of corroborating one claim."""

        VERIFIED = "verified"
        PARTIALLY_SUPPORTED = "partially_supported"
        UNSUPPORTED = "unsupported"
        CONTRADICTED = "contradicted"
        NOT_APPLICABLE = "not_applicable"


    class TemporalStatus(str, Enum):
        """Time validity of evidence used for a claim."""

        CURRENT = "current"
        REVIEW_REQUIRED = "review_required"
        OUTDATED = "outdated"
        UNDATED = "undated"
        NOT_APPLICABLE = "not_applicable"


    class EditorialRisk(str, Enum):
        """Internal LMHS Editorial Risk."""

        LOW = "Low"
        MODERATE = "Moderate"
        HIGH = "High"
        SEVERE = "Severe"


    class EditorialConfidence(str, Enum):
        """Primary Author-facing publication-readiness conclusion."""

        READY = "Ready for publication"
        READY_WITH_REVIEW = "Ready with review"
        NEEDS_EVIDENCE = "Needs stronger evidence"
        NOT_READY = "Not ready for publication"


    @dataclass(frozen=True)
    class Claim:
        """One publication claim requiring editorial treatment."""

        identifier: str
        text: str
        classification: ClaimClassification
        material: bool = True
        time_sensitive: bool = False

        def __post_init__(self) -> None:
            if not self.identifier.strip() or not self.text.strip():
                raise ValueError("Claims require an identifier and text.")


    @dataclass(frozen=True)
    class EvidenceRecord:
        """One attributable source observation about a claim."""

        source_identifier: str
        claim_identifier: str
        position: EvidencePosition
        independent_group: str
        published_on: date | None = None
        checked_on: date | None = None
        source_is_credible: bool = True
        note: str = ""

        def __post_init__(self) -> None:
            required = (
                self.source_identifier,
                self.claim_identifier,
                self.independent_group,
            )
            if not all(value.strip() for value in required):
                raise ValueError(
                    "Evidence requires source, claim, and independence identifiers."
                )


    @dataclass(frozen=True)
    class ClaimAssessment:
        """Transparent assessment of one claim."""

        claim: Claim
        evidence_status: EvidenceStatus
        temporal_status: TemporalStatus
        supporting_sources: tuple[str, ...]
        contradicting_sources: tuple[str, ...]
        independent_support_count: int
        explanation: str
        recommended_action: str | None = None


    @dataclass(frozen=True)
    class EvidenceValidationReport:
        """Complete stage 3 and stage 4 result."""

        assessments: tuple[ClaimAssessment, ...]
        editorial_risk: EditorialRisk
        editorial_confidence: EditorialConfidence
        author_message: str
        may_recommend_publication: bool
        significant_findings: tuple[str, ...]


    def classify_claim(
        text: str,
        *,
        author_experience: bool = False,
        declared_opinion: bool = False,
        forecast: bool = False,
        unresolved: bool = False,
    ) -> ClaimClassification:
        """Classify explicit context without pretending semantic certainty."""
        if not text.strip():
            raise ValueError("Claim text cannot be empty.")
        if unresolved:
            return ClaimClassification.UNRESOLVED_UNCERTAINTY
        if author_experience:
            return ClaimClassification.AUTHOR_EXPERIENCE
        if declared_opinion:
            return ClaimClassification.OPINION
        if forecast:
            return ClaimClassification.FORECAST
        return ClaimClassification.SOURCE_ASSERTION


    class EvidenceValidator:
        """Corroborate claims using attributable evidence records."""

        def __init__(self, *, current_on: date | None = None) -> None:
            self.current_on = current_on or date.today()

        def assess(
            self,
            claim: Claim,
            evidence: Iterable[EvidenceRecord],
        ) -> ClaimAssessment:
            records = tuple(
                item for item in evidence
                if item.claim_identifier == claim.identifier
            )

            if claim.classification in {
                ClaimClassification.AUTHOR_EXPERIENCE,
                ClaimClassification.OPINION,
            }:
                return ClaimAssessment(
                    claim=claim,
                    evidence_status=EvidenceStatus.NOT_APPLICABLE,
                    temporal_status=TemporalStatus.NOT_APPLICABLE,
                    supporting_sources=(),
                    contradicting_sources=(),
                    independent_support_count=0,
                    explanation=(
                        "This is identified as Author experience or opinion, "
                        "not presented as an independently verified fact."
                    ),
                )

            credible = tuple(item for item in records if item.source_is_credible)
            supports = tuple(
                item for item in credible
                if item.position is EvidencePosition.SUPPORTS
            )
            contradicts = tuple(
                item for item in credible
                if item.position is EvidencePosition.CONTRADICTS
            )
            groups = {item.independent_group for item in supports}
            temporal = self._temporal_status(claim, supports)

            if contradicts:
                status = EvidenceStatus.CONTRADICTED
                explanation = "Credible evidence materially contradicts this claim."
                action = "Rebuild or remove the claim using defensible evidence."
            elif len(groups) >= 2:
                status = EvidenceStatus.VERIFIED
                explanation = (
                    "The claim has support from at least two independent "
                    "credible source groups."
                )
                action = None
            elif len(groups) == 1:
                status = EvidenceStatus.PARTIALLY_SUPPORTED
                explanation = (
                    "The claim has credible support, but independent "
                    "corroboration is incomplete."
                )
                action = "Add an independent source or qualify the claim."
            else:
                status = EvidenceStatus.UNSUPPORTED
                explanation = "No credible supporting evidence was recorded."
                action = "Provide evidence, qualify the claim, or remove it."

            if temporal in {TemporalStatus.OUTDATED, TemporalStatus.UNDATED}:
                action = "Revalidate the time-sensitive evidence before publication."

            return ClaimAssessment(
                claim=claim,
                evidence_status=status,
                temporal_status=temporal,
                supporting_sources=tuple(item.source_identifier for item in supports),
                contradicting_sources=tuple(
                    item.source_identifier for item in contradicts
                ),
                independent_support_count=len(groups),
                explanation=explanation,
                recommended_action=action,
            )

        def _temporal_status(
            self,
            claim: Claim,
            supporting: tuple[EvidenceRecord, ...],
        ) -> TemporalStatus:
            if not claim.time_sensitive:
                return TemporalStatus.NOT_APPLICABLE
            if not supporting or any(item.published_on is None for item in supporting):
                return TemporalStatus.UNDATED
            newest = max(item.published_on for item in supporting if item.published_on)
            age = (self.current_on - newest).days
            if age < 0:
                return TemporalStatus.REVIEW_REQUIRED
            if age <= 365:
                return TemporalStatus.CURRENT
            return TemporalStatus.OUTDATED


    class EditorialRiskReviewer:
        """Derive LMHS risk and Author-facing Editorial Confidence."""

        def review(
            self,
            assessments: Iterable[ClaimAssessment],
            *,
            deceptive_intent: bool = False,
            dangerous_falsehood: bool = False,
        ) -> EvidenceValidationReport:
            items = tuple(assessments)
            if not items:
                raise ValueError("At least one claim assessment is required.")

            if deceptive_intent or dangerous_falsehood:
                risk = EditorialRisk.SEVERE
            elif any(
                item.claim.material
                and item.evidence_status is EvidenceStatus.CONTRADICTED
                for item in items
            ):
                risk = EditorialRisk.SEVERE
            elif any(
                item.claim.material
                and (
                    item.evidence_status is EvidenceStatus.UNSUPPORTED
                    or item.temporal_status in {
                        TemporalStatus.OUTDATED,
                        TemporalStatus.UNDATED,
                    }
                )
                for item in items
            ):
                risk = EditorialRisk.HIGH
            elif any(
                item.evidence_status is EvidenceStatus.PARTIALLY_SUPPORTED
                or item.temporal_status is TemporalStatus.REVIEW_REQUIRED
                for item in items
            ):
                risk = EditorialRisk.MODERATE
            else:
                risk = EditorialRisk.LOW

            confidence = {
                EditorialRisk.LOW: EditorialConfidence.READY,
                EditorialRisk.MODERATE: EditorialConfidence.READY_WITH_REVIEW,
                EditorialRisk.HIGH: EditorialConfidence.NEEDS_EVIDENCE,
                EditorialRisk.SEVERE: EditorialConfidence.NOT_READY,
            }[risk]
            messages = {
                EditorialRisk.LOW: (
                    "Editorial review completed. The material provides a "
                    "strong foundation for publication."
                ),
                EditorialRisk.MODERATE: (
                    "The publication has a defensible foundation, with "
                    "specific evidence or timing points to review."
                ),
                EditorialRisk.HIGH: (
                    "Important claims need stronger or more current evidence "
                    "before publication can be recommended."
                ),
                EditorialRisk.SEVERE: (
                    "The material cannot responsibly be recommended for "
                    "publication as presented. A defensible alternative is required."
                ),
            }
            findings = tuple(
                f"{item.claim.identifier}: {item.recommended_action}"
                for item in items
                if item.recommended_action
            )

            return EvidenceValidationReport(
                assessments=items,
                editorial_risk=risk,
                editorial_confidence=confidence,
                author_message=messages[risk],
                may_recommend_publication=risk in {
                    EditorialRisk.LOW,
                    EditorialRisk.MODERATE,
                },
                significant_findings=findings,
            )


    def validate_evidence(
        claims: Iterable[Claim],
        evidence: Iterable[EvidenceRecord],
        *,
        current_on: date | None = None,
        deceptive_intent: bool = False,
        dangerous_falsehood: bool = False,
    ) -> EvidenceValidationReport:
        """Run claim assessment and risk review as one explicit pipeline."""
        claim_items = tuple(claims)
        evidence_items = tuple(evidence)
        validator = EvidenceValidator(current_on=current_on)
        assessments = tuple(
            validator.assess(claim, evidence_items) for claim in claim_items
        )
        return EditorialRiskReviewer().review(
            assessments,
            deceptive_intent=deceptive_intent,
            dangerous_falsehood=dangerous_falsehood,
        )
''')


TESTS = clean(r'''
    """Behavioural tests for Capability 008 Evidence Validation."""

    from datetime import date
    import unittest

    from studio.evidence_validation import (
        Claim,
        ClaimClassification,
        EditorialConfidence,
        EditorialRisk,
        EditorialRiskReviewer,
        EvidencePosition,
        EvidenceRecord,
        EvidenceStatus,
        EvidenceValidator,
        TemporalStatus,
        classify_claim,
        validate_evidence,
    )


    def claim(**changes):
        values = {
            "identifier": "claim-1",
            "text": "The programme reduced processing time.",
            "classification": ClaimClassification.SOURCE_ASSERTION,
        }
        values.update(changes)
        return Claim(**values)


    def evidence(source, group, **changes):
        values = {
            "source_identifier": source,
            "claim_identifier": "claim-1",
            "position": EvidencePosition.SUPPORTS,
            "independent_group": group,
            "published_on": date(2026, 7, 1),
            "checked_on": date(2026, 8, 1),
        }
        values.update(changes)
        return EvidenceRecord(**values)


    class ClaimClassificationTests(unittest.TestCase):
        def test_default_is_source_assertion_not_verified_fact(self):
            self.assertIs(
                classify_claim("A factual statement"),
                ClaimClassification.SOURCE_ASSERTION,
            )

        def test_explicit_context_is_preserved(self):
            self.assertIs(
                classify_claim("I observed this", author_experience=True),
                ClaimClassification.AUTHOR_EXPERIENCE,
            )
            self.assertIs(
                classify_claim("This may happen", forecast=True),
                ClaimClassification.FORECAST,
            )

        def test_empty_claim_is_rejected(self):
            with self.assertRaises(ValueError):
                classify_claim("  ")


    class CorroborationTests(unittest.TestCase):
        def setUp(self):
            self.validator = EvidenceValidator(current_on=date(2026, 8, 1))

        def test_two_independent_sources_verify_claim(self):
            result = self.validator.assess(
                claim(),
                (evidence("primary", "publisher-a"), evidence("audit", "publisher-b")),
            )
            self.assertIs(result.evidence_status, EvidenceStatus.VERIFIED)
            self.assertEqual(result.independent_support_count, 2)

        def test_repeated_reporting_is_not_independent_corroboration(self):
            result = self.validator.assess(
                claim(),
                (evidence("report", "wire-a"), evidence("reprint", "wire-a")),
            )
            self.assertIs(
                result.evidence_status,
                EvidenceStatus.PARTIALLY_SUPPORTED,
            )
            self.assertEqual(result.independent_support_count, 1)

        def test_credible_contradiction_is_preserved(self):
            result = self.validator.assess(
                claim(),
                (
                    evidence("support", "group-a"),
                    evidence(
                        "contradiction",
                        "group-b",
                        position=EvidencePosition.CONTRADICTS,
                    ),
                ),
            )
            self.assertIs(result.evidence_status, EvidenceStatus.CONTRADICTED)
            self.assertEqual(result.contradicting_sources, ("contradiction",))

        def test_uncredible_source_does_not_verify(self):
            result = self.validator.assess(
                claim(),
                (evidence("unknown", "group-a", source_is_credible=False),),
            )
            self.assertIs(result.evidence_status, EvidenceStatus.UNSUPPORTED)

        def test_opinion_is_not_misrepresented_as_verified(self):
            result = self.validator.assess(
                claim(classification=ClaimClassification.OPINION),
                (),
            )
            self.assertIs(result.evidence_status, EvidenceStatus.NOT_APPLICABLE)


    class TemporalIntegrityTests(unittest.TestCase):
        def setUp(self):
            self.validator = EvidenceValidator(current_on=date(2026, 8, 1))

        def test_current_time_sensitive_source(self):
            result = self.validator.assess(
                claim(time_sensitive=True),
                (evidence("a", "a"), evidence("b", "b")),
            )
            self.assertIs(result.temporal_status, TemporalStatus.CURRENT)

        def test_outdated_time_sensitive_source_requires_revalidation(self):
            result = self.validator.assess(
                claim(time_sensitive=True),
                (evidence("old", "a", published_on=date(2024, 1, 1)),),
            )
            self.assertIs(result.temporal_status, TemporalStatus.OUTDATED)
            self.assertIn("Revalidate", result.recommended_action)

        def test_undated_time_sensitive_source_is_visible(self):
            result = self.validator.assess(
                claim(time_sensitive=True),
                (evidence("undated", "a", published_on=None),),
            )
            self.assertIs(result.temporal_status, TemporalStatus.UNDATED)


    class EditorialRiskTests(unittest.TestCase):
        def report(self, claim_value, records, **flags):
            return validate_evidence(
                (claim_value,),
                records,
                current_on=date(2026, 8, 1),
                **flags,
            )

        def test_low_risk_translates_to_author_confidence(self):
            result = self.report(
                claim(),
                (evidence("a", "a"), evidence("b", "b")),
            )
            self.assertIs(result.editorial_risk, EditorialRisk.LOW)
            self.assertIs(result.editorial_confidence, EditorialConfidence.READY)
            self.assertTrue(result.may_recommend_publication)

        def test_partial_support_is_moderate(self):
            result = self.report(claim(), (evidence("a", "a"),))
            self.assertIs(result.editorial_risk, EditorialRisk.MODERATE)
            self.assertIs(
                result.editorial_confidence,
                EditorialConfidence.READY_WITH_REVIEW,
            )

        def test_unsupported_material_claim_is_high(self):
            result = self.report(claim(), ())
            self.assertIs(result.editorial_risk, EditorialRisk.HIGH)
            self.assertIs(
                result.editorial_confidence,
                EditorialConfidence.NEEDS_EVIDENCE,
            )
            self.assertFalse(result.may_recommend_publication)

        def test_contradicted_material_claim_is_severe(self):
            result = self.report(
                claim(),
                (evidence("refutation", "a", position=EvidencePosition.CONTRADICTS),),
            )
            self.assertIs(result.editorial_risk, EditorialRisk.SEVERE)
            self.assertIs(result.editorial_confidence, EditorialConfidence.NOT_READY)

        def test_dangerous_falsehood_is_severe(self):
            result = self.report(
                claim(classification=ClaimClassification.OPINION),
                (),
                dangerous_falsehood=True,
            )
            self.assertIs(result.editorial_risk, EditorialRisk.SEVERE)

        def test_risk_has_no_percentage_or_false_precision(self):
            result = self.report(claim(), ())
            self.assertNotIn("%", result.author_message)

        def test_empty_review_is_rejected(self):
            with self.assertRaises(ValueError):
                EditorialRiskReviewer().review(())


    if __name__ == "__main__":
        unittest.main()
''')


ARCHITECTURE = clean(r'''
    # Evidence Validation Runtime

    ## Status

    Active runtime architecture for the Capability 008 continuation.

    ## Purpose

    Evidence Validation determines whether material claims are supported. It
    follows Editorial Discernment and implements stages 3 and 4 of the
    Editorial Integrity Pipeline.

    ## Responsibilities

    The runtime:

    - classifies claims without presenting assertions as verified facts;
    - records attributable support, contradiction, and context;
    - counts independent source groups rather than repeated reporting;
    - exposes missing, weak, conflicting, undated, and outdated evidence;
    - assigns internal LMHS Editorial Risk;
    - translates that assessment into Author-facing Editorial Confidence; and
    - provides a proportionate recommended action.

    ## Verification Boundary

    A source identifier is not proof. Two records derived from the same
    reporting origin are one independent source group. A claim is Verified
    only when at least two credible independent groups support it and no
    credible contradiction is recorded.

    Provider or network research remains outside this deterministic core.
    Integrations must supply attributable evidence records and must never
    fabricate a source, citation, date, quotation, or verification result.

    ## Temporal Integrity

    Time-sensitive claims record whether supporting evidence is Current,
    Review Required, Outdated, or Undated. The one-year default is a
    conservative implementation threshold, not a universal truth claim;
    callers may later supply domain-specific policy without weakening the
    requirement to revalidate before publication.

    ## Publication Gate

    Low and Moderate risk may support a publication recommendation. High and
    Severe risk do not. Severe risk requires a defensible alternative rather
    than silent continuation.
''')


ADR = clean(r'''
    # ADR-010 - Implement Evidence Validation and Editorial Risk

    ## Status

    Accepted

    ## Date

    2026-08-01

    ## Context

    Capability 008 separated Editorial Discernment from Evidence Validation.
    The repository needed an executable, provider-independent way to preserve
    claim meaning, corroboration, conflicts, and time validity without
    claiming certainty unsupported by the evidence.

    ## Decision

    Adopt explicit Claim, EvidenceRecord, ClaimAssessment, and
    EvidenceValidationReport models. Corroboration counts independent source
    groups. Internal LMHS Editorial Risk is derived from material evidence
    findings and translated into Editorial Confidence as the primary
    Author-facing conclusion.

    Verified requires two credible independent supporting groups and no
    credible contradiction. High and Severe risk block a publication
    recommendation. Percentages are prohibited.

    ## Constitutional Impact

    No constitutional principle changes. This decision implements Evidence
    Before Assertion, Confidence Before Publication, transparent uncertainty,
    and the frozen Canonical Vocabulary.

    ## Consequences

    The core remains deterministic and testable. External research providers
    can be added later, but they must return attributable records. The model is
    intentionally conservative and may request corroboration rather than
    manufacture confidence.
''')


BASELINE = clean(r'''
    # Architecture Baseline - 2026.08.01v06

    ## Status

    Current Version 1.0 runtime baseline.

    ## Baseline ID

    `2026.08.01v06`

    ## Supersedes

    `2026.08.01v05`

    ## Reason for Revision

    Implement the remaining Capability 008 trust-protection increment:

    - Claim Classification
    - Evidence Validation and independent corroboration
    - source contradiction visibility
    - Temporal Integrity
    - internal LMHS Editorial Risk
    - Author-facing Editorial Confidence translation

    ## Architecture

    Editorial Discernment determines what a contribution means. Evidence
    Validation determines whether material claims are supported. Editorial
    Risk evaluates the publication consequence. Editorial Confidence presents
    the readiness conclusion to the Author.

    The runtime is provider-independent. It records evidence supplied by
    integrations but never fabricates verification.

    ## Constitutional Impact

    No frozen constitutional rule changes. Baseline v06 implements Principles
    IV and V and the existing Editorial Integrity Pipeline.
''')


DEMO = clean(r'''
    # Capability 008 Demo - Evidence Validation and Editorial Risk

    ## Problem

    The Studio could assess sources and protect Editorial Intent, but could not
    yet distinguish an assertion from a verified fact, compare independent
    support, expose stale evidence, or produce an executable publication gate.

    ## What Changed

    The Studio now classifies claims, corroborates attributable evidence,
    preserves contradictions, checks Temporal Integrity, assigns internal LMHS
    Editorial Risk, and translates it into Author-facing Editorial Confidence.

    ## Example

    ```text
    Material factual claim
              |
              v
    two independent credible sources? -- no --> strengthen or qualify
              |
             yes
              v
    current and uncontradicted? -------- no --> revalidate or rebuild
              |
             yes
              v
    Low Editorial Risk -> Ready for publication
    ```

    Repeated copies of one wire report count as one source group. A credible
    contradiction remains visible and prevents a false Verified result.

    ## Author Benefit

    The Author receives a concise readiness conclusion and a specific next
    action. Internal mechanics remain available as supporting detail without
    replacing Editorial Confidence.

    ## Acceptance Evidence

    Behavioural tests cover claim classification, independent corroboration,
    contradiction, time-sensitive evidence, every LMHS level, publication
    gating, and the absence of percentage-based false precision.

    ## Learning

    Corroboration is a provenance relationship, not a source count. Recording
    independence explicitly prevents repeated reporting from manufacturing
    confidence.

    ## Next

    Capability 009 can consume the validated report when building the Article
    Engine and Publication Package.
''')


DOC_TESTS = clean(r'''
    """Documentation tests for the Capability 008 continuation."""

    import unittest
    from pathlib import Path

    ROOT = Path(__file__).resolve().parents[1]


    class EvidenceDocumentationTests(unittest.TestCase):
        def content(self, relative):
            return (ROOT / relative).read_text(encoding="utf-8")

        def test_runtime_architecture_records_verification_boundary(self):
            content = self.content("docs/architecture/Evidence_Validation_Runtime.md")
            self.assertIn("independent source groups", content)
            normalized = " ".join(content.split())
            self.assertIn("must never fabricate", normalized)

        def test_adr_and_baseline_exist(self):
            self.assertTrue((ROOT / "docs/architecture/adr/ADR-010-implement-evidence-validation-and-editorial-risk.md").is_file())
            self.assertIn(
                "2026.08.01v06",
                self.content("docs/architecture/baselines/Architecture_Baseline_2026.08.01v06.md"),
            )

        def test_canonical_vocabulary_is_extended(self):
            content = self.content("docs/constitution/Canonical_Vocabulary.md")
            self.assertIn("Claim Classification", content)
            self.assertIn("Editorial Confidence", content)

        def test_roadmap_records_increment_complete(self):
            content = self.content("ROADMAP.md")
            self.assertIn("[x] Evidence Validation", content)
            self.assertIn("[x] LMHS Editorial Risk", content)


    if __name__ == "__main__":
        unittest.main()
''')


VOCABULARY = clean(r'''
    ## Capability 008 Evidence Vocabulary

    ### Claim Classification

    The editorial meaning assigned to a publication claim:

    - Verified Fact
    - Source Assertion
    - Author Experience
    - Reasonable Inference
    - Opinion
    - Forecast
    - Unresolved Uncertainty

    ### Evidence Validation

    The process of determining whether material claims are supported,
    contradicted, current, and responsibly attributable.

    ### Temporal Integrity

    Review of time-sensitive evidence for continued publication validity.

    Editorial Confidence remains the primary Author-facing conclusion. LMHS
    Editorial Risk remains the internal assessment.
''')


ROADMAP = clean(r'''
    ## Capability 008 - Editorial Discernment and Evidence Validation

    Status:

    `Implemented locally; pending delivery workflow completion`

    Delivered:

    - [x] Editorial Intent
    - [x] Editorial Discernment Engine
    - [x] Editorial Guidance
    - [x] Intent Alignment
    - [x] Editorial Coherence Guard
    - [x] No Silent Scope Expansion
    - [x] Workspace lifecycle
    - [x] Stage lifecycle
    - [x] Pause, resume, cancel, abort, complete, and archive
    - [x] Approved-component protection
    - [x] One-question clarification
    - [x] Evidence Validation
    - [x] Claim Classification
    - [x] Independent corroboration and source comparison
    - [x] Temporal Integrity
    - [x] LMHS Editorial Risk
    - [x] Author-facing Editorial Confidence translation
    - [x] Runtime and documentation tests

    Next capability after delivery: Capability 009 - Article Engine and
    Publication Package.
''')


SCORECARD = clean(r'''
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
''')


PRD = clean(r'''
    ## Capability 008 Requirements

    The Product shall:

    - maintain one Editorial Intent per Editorial Session;
    - classify new material as Aligned, Related, Diverging, Separate Intent,
      or Ambiguous;
    - recommend a new Editorial Session for separate publication objectives;
    - never silently merge unrelated sources or expand scope;
    - ask one concise clarification question when ambiguity blocks progress;
    - preserve approved Publication Package components;
    - distinguish Workspace State from Stage State;
    - support pause, resume, cancel, abort, complete, and archive;
    - preserve work and provenance after abort;
    - present Editorial Guidance rather than internal engine language;

    - classify claims using the Canonical Vocabulary;
    - require attributable, credible, independent support before Verified;
    - preserve credible contradiction and unresolved uncertainty;
    - review time-sensitive claims for Temporal Integrity;
    - derive Low, Moderate, High, or Severe Editorial Risk without percentages;
    - use Editorial Confidence as the primary Author-facing conclusion;
    - explain significant findings with a recommended next action; and
    - prevent High or Severe risk from receiving a publication recommendation.
''')


README = clean(r'''
    ## Capability 008 - Editorial Discernment and Evidence Validation

    Capability 008 includes:

    - Editorial Intent and Editorial Discernment Engine
    - Author-facing Editorial Guidance
    - Editorial Coherence Guard and No Silent Scope Expansion
    - Workspace and Stage lifecycle
    - pause, resume, cancel, abort, complete, and archive behaviour
    - approved-component protection and one-question clarification
    - Claim Classification and independent evidence corroboration
    - contradiction visibility and Temporal Integrity
    - internal LMHS Editorial Risk
    - Author-facing Editorial Confidence translation
''')


CHANGELOG = clean(r'''
    ## Capability 008 - Editorial Discernment and Evidence Validation

    ### Added

    - Editorial Discernment Engine and Editorial Guidance
    - Editorial Intent, Intent Alignment, and Editorial Coherence Guard
    - Workspace and Stage lifecycle
    - approved-component protection and one-question clarification
    - Claim Classification and Evidence Validation runtime
    - Independent corroboration and contradiction handling
    - Temporal Integrity review
    - LMHS Editorial Risk and Editorial Confidence translation
    - Architecture Baseline 2026.08.01v06 and ADR-010
    - Behavioural and documentation tests

    ### Changed

    - Separate publication objectives are no longer silently merged
    - Workspace State and Stage State are distinct
    - Aborted sessions preserve work, provenance, and approvals
    - High and Severe Editorial Risk now block publication recommendation
''')


FILES = {
    "studio/evidence_validation.py": RUNTIME,
    "tests/test_capability008_evidence_validation.py": TESTS,
    "tests/test_capability008_evidence_documentation.py": DOC_TESTS,
    "docs/architecture/Evidence_Validation_Runtime.md": ARCHITECTURE,
    "docs/architecture/adr/ADR-010-implement-evidence-validation-and-editorial-risk.md": ADR,
    "docs/architecture/baselines/Architecture_Baseline_2026.08.01v06.md": BASELINE,
    "docs/demos/Capability-008-Evidence-Validation-and-Editorial-Risk.md": DEMO,
}

MARKERS = {
    "docs/constitution/Canonical_Vocabulary.md": ("CAPABILITY_008_EVIDENCE_VOCABULARY", VOCABULARY),
    "ROADMAP.md": ("CAPABILITY_008_ROADMAP", ROADMAP),
    "docs/VERSION_ONE_SCORECARD.md": ("CAPABILITY_008_SCORECARD", SCORECARD),
    "docs/product/PRD_v1.3.md": ("CAPABILITY_008_PRD", PRD),
    "README.md": ("CAPABILITY_008_README", README),
    "CHANGELOG.md": ("CAPABILITY_008_CHANGELOG", CHANGELOG),
}


class CapabilityError(RuntimeError):
    pass


def run(command: list[str], root: Path) -> None:
    print("$", " ".join(command))
    subprocess.run(command, cwd=root, check=True)


def output(command: list[str], root: Path) -> str:
    return subprocess.run(
        command, cwd=root, text=True, capture_output=True, check=True
    ).stdout.strip()


def root_and_state() -> Path:
    root = Path(output(["git", "rev-parse", "--show-toplevel"], Path.cwd())).resolve()
    if root.name != EXPECTED_REPOSITORY:
        raise CapabilityError(f"Expected {EXPECTED_REPOSITORY}, found {root.name}.")
    if EXPECTED_REMOTE_FRAGMENT not in output(["git", "remote", "get-url", "origin"], root):
        raise CapabilityError("Origin does not match the expected repository.")
    branch = output(["git", "branch", "--show-current"], root)
    if branch != EXPECTED_BRANCH:
        raise CapabilityError(f"Expected branch {EXPECTED_BRANCH}, found {branch}.")
    expected = set(FILES) | set(MARKERS) | {SCRIPT_PATH}
    status = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=root,
        text=True,
        capture_output=True,
        check=True,
    ).stdout
    unexpected = []
    for line in status.splitlines():
        path = line[3:].strip().split(" -> ")[-1]
        if path not in expected:
            unexpected.append(line)
    if unexpected:
        raise CapabilityError("Unexpected working-tree changes:\n" + "\n".join(unexpected))
    return root


def managed_block(name: str, content: str) -> str:
    return f"<!-- {name}_START -->\n\n{content.rstrip()}\n\n<!-- {name}_END -->"


def upsert(path: Path, name: str, content: str) -> None:
    original = path.read_text(encoding="utf-8")
    start = f"<!-- {name}_START -->"
    end = f"<!-- {name}_END -->"
    if (start in original) != (end in original):
        raise CapabilityError(f"Incomplete marker pair in {path}.")
    block = managed_block(name, content)
    if start in original:
        before, remainder = original.split(start, 1)
        _, after = remainder.split(end, 1)
        updated = before.rstrip() + "\n\n" + block
        if after.strip():
            updated += "\n\n" + after.strip()
    else:
        updated = original.rstrip() + "\n\n" + block
    path.write_text(updated.rstrip() + "\n", encoding="utf-8")


def preview() -> None:
    print("Capability 008 Evidence Validation preview\n")
    print("Generated files:")
    for path in FILES:
        print(f"  - {path}")
    print("\nManaged documentation:")
    for path in MARKERS:
        print(f"  - {path}")
    print("\nDecisions:")
    for item in (
        "Classify claims without false verification",
        "Require independent corroboration for Verified",
        "Preserve contradiction and uncertainty",
        "Implement Temporal Integrity",
        "Derive internal LMHS Editorial Risk",
        "Translate risk into Author-facing Editorial Confidence",
        "Create Architecture Baseline 2026.08.01v06",
    ):
        print(f"  - {item}")
    print("\nPreview mode changes nothing.")


def apply(root: Path) -> None:
    for relative, content in FILES.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"Wrote {relative}")
    for relative, (name, content) in MARKERS.items():
        upsert(root / relative, name, content)
        print(f"Updated {relative}")
    run([sys.executable, "-m", "compileall", "-q", "studio", "scripts", "tests"], root)
    run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], root)
    run([sys.executable, "studio.py", "validate"], root)
    run(["git", "status", "--short"], root)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        root = root_and_state()
        script = Path(__file__).read_text(encoding="utf-8")
        if SENTINEL not in script:
            raise CapabilityError("Bootstrap integrity sentinel is missing.")
        if args.apply:
            apply(root)
        else:
            preview()
        return 0
    except (CapabilityError, OSError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

# CAPABILITY_008A3_GENERATOR_OVERRIDE_START
from bootstrap_capability008a3_editorial_integrity_hardening import (
    EVIDENCE_VALIDATION_RUNTIME as CAPABILITY_008A3_EVIDENCE_RUNTIME,
    EVIDENCE_VALIDATION_TESTS as CAPABILITY_008A3_EVIDENCE_TESTS,
)
FILES["studio/evidence_validation.py"] = (
    CAPABILITY_008A3_EVIDENCE_RUNTIME
)
FILES["tests/test_capability008_evidence_validation.py"] = (
    CAPABILITY_008A3_EVIDENCE_TESTS
)
# CAPABILITY_008A3_GENERATOR_OVERRIDE_END

if __name__ == "__main__":
    raise SystemExit(main())


# CAPABILITY_008_EVIDENCE_VALIDATION_COMPLETE
