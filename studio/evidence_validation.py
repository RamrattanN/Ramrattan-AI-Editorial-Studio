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
    NEEDS_EVIDENCE = "Not ready - stronger evidence required"
    NOT_READY = "Not ready - publication blocked"


@dataclass(frozen=True)
class Claim:
    """One publication claim requiring editorial treatment."""

    identifier: str
    text: str
    classification: ClaimClassification
    material: bool = True
    time_sensitive: bool = False
    attribution: str | None = None

    def __post_init__(self) -> None:
        if not self.identifier.strip() or not self.text.strip():
            raise ValueError("Claims require an identifier and text.")
        if self.classification is ClaimClassification.VERIFIED_FACT:
            raise ValueError(
                "Verified Fact is earned by Evidence Validation and cannot "
                "be selected as an initial claim classification."
            )
        if self.classification in {
            ClaimClassification.AUTHOR_EXPERIENCE,
            ClaimClassification.OPINION,
        } and not (self.attribution and self.attribution.strip()):
            raise ValueError(
                "Author experience and opinion require durable attribution."
            )


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
    resolved_classification: ClaimClassification
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
    publication_blocked: bool
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
                resolved_classification=claim.classification,
                evidence_status=EvidenceStatus.NOT_APPLICABLE,
                temporal_status=TemporalStatus.NOT_APPLICABLE,
                supporting_sources=(),
                contradicting_sources=(),
                independent_support_count=0,
                explanation=(
                    f"This is attributed as {claim.classification.value.replace('_', ' ')} "
                    f"to {claim.attribution}; it is not presented as an "
                    "independently verified fact."
                ),
            )

        credible = self._distinct_credible_records(records)
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
        resolved = claim.classification

        if contradicts:
            status = EvidenceStatus.CONTRADICTED
            explanation = "Credible evidence materially contradicts this claim."
            action = "Rebuild or remove the claim using defensible evidence."
        elif (
            len(groups) >= 2
            and claim.classification is ClaimClassification.SOURCE_ASSERTION
            and temporal in {
                TemporalStatus.CURRENT,
                TemporalStatus.NOT_APPLICABLE,
            }
        ):
            status = EvidenceStatus.VERIFIED
            resolved = ClaimClassification.VERIFIED_FACT
            explanation = (
                "The claim has support from at least two independent "
                "credible source groups."
            )
            action = None
        elif len(groups) >= 2:
            status = EvidenceStatus.PARTIALLY_SUPPORTED
            explanation = (
                "Independent evidence supports this claim, but its semantic "
                f"classification remains {claim.classification.value.replace('_', ' ')}."
            )
            action = (
                "Preserve the claim qualification and attribution; do not "
                "present it as a Verified Fact."
            )
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

        if temporal in {
            TemporalStatus.REVIEW_REQUIRED,
            TemporalStatus.OUTDATED,
            TemporalStatus.UNDATED,
        }:
            action = "Revalidate the time-sensitive evidence before publication."

        return ClaimAssessment(
            claim=claim,
            resolved_classification=resolved,
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

    @staticmethod
    def _distinct_credible_records(
        records: tuple[EvidenceRecord, ...],
    ) -> tuple[EvidenceRecord, ...]:
        """Deduplicate by source identity, preserving contradictions safely."""
        by_source: dict[str, EvidenceRecord] = {}
        for record in records:
            if not record.source_is_credible:
                continue
            identity = record.source_identifier.strip().casefold()
            existing = by_source.get(identity)
            if existing is None or (
                record.position is EvidencePosition.CONTRADICTS
                and existing.position is not EvidencePosition.CONTRADICTS
            ):
                by_source[identity] = record
        return tuple(by_source.values())

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
            item.evidence_status in {
                EvidenceStatus.PARTIALLY_SUPPORTED,
                EvidenceStatus.UNSUPPORTED,
                EvidenceStatus.CONTRADICTED,
            }
            or item.temporal_status in {
                TemporalStatus.REVIEW_REQUIRED,
                TemporalStatus.OUTDATED,
                TemporalStatus.UNDATED,
            }
            or item.recommended_action is not None
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
                "Publication is blocked until important claims have stronger "
                "or more current evidence."
            ),
            EditorialRisk.SEVERE: (
                "Publication is blocked. The material cannot responsibly be "
                "recommended as presented; a defensible alternative is required."
            ),
        }
        findings = tuple(
            f"{item.claim.identifier}: {item.recommended_action}"
            for item in items
            if item.recommended_action
        )
        blocked = risk in {EditorialRisk.HIGH, EditorialRisk.SEVERE}
        if blocked:
            findings += (f"Publication gate: {messages[risk]}",)
        if risk is EditorialRisk.LOW and findings:
            raise ValueError("Low Editorial Risk cannot contain actionable findings.")

        return EvidenceValidationReport(
            assessments=items,
            editorial_risk=risk,
            editorial_confidence=confidence,
            author_message=messages[risk],
            may_recommend_publication=not blocked,
            publication_blocked=blocked,
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
