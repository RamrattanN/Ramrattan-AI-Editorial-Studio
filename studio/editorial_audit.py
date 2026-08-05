"""V11-06 Editorial Audit: analysis-only re-assessment of edited content.

Editorial Audit re-invokes the existing, unmodified Evidence Validation
pipeline (`evidence_validation.validate_evidence`) to produce a fresh LMHS
Assessment, computes Editorial Drift against the single Generate-Once
baseline, and reports the resulting Editorial Confidence. It never writes to
Publication Content and never transmits content anywhere; it is pure
computation over data already held by the session.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from datetime import date
from typing import Iterable

from .evidence_validation import (
    Claim,
    EditorialConfidence,
    EditorialRisk,
    EvidenceRecord,
    EvidenceValidationReport,
    validate_evidence,
)
from .publication_studio import PublicationContent


@dataclass(frozen=True, slots=True)
class EditorialDriftAssessment:
    """How far the Author's edits have moved from the approved baseline.

    The baseline is the content Generation produced from the approved
    Editorial Plan and the evidence confirmed at Editorial Discovery
    (`PublicationEditor.generated_content`) - the one fixed, non-arbitrary
    reference point Generate Once establishes. Drift is always measured
    against that same baseline, never against a prior edit or a prior
    audit, so repeated audits remain comparable across a session.
    """

    changed_fields: tuple[str, ...]
    drifted: bool
    explanation: str


def compute_editorial_drift(
    generated: PublicationContent, current: PublicationContent
) -> EditorialDriftAssessment:
    """Report which Publication Content fields differ from the baseline."""
    if not isinstance(generated, PublicationContent) or not isinstance(
        current, PublicationContent
    ):
        raise ValueError("Editorial Drift requires two Publication Content values.")
    changed = tuple(
        sorted(
            field.name
            for field in fields(PublicationContent)
            if getattr(generated, field.name) != getattr(current, field.name)
        )
    )
    drifted = bool(changed)
    explanation = (
        "The Author has changed: " + ", ".join(changed) + "."
        if drifted
        else "The Author-edited publication matches the approved, generated content."
    )
    return EditorialDriftAssessment(
        changed_fields=changed,
        drifted=drifted,
        explanation=explanation,
    )


@dataclass(frozen=True, slots=True)
class EditorialAuditResult:
    """The complete, read-only output of one Editorial Audit."""

    lmhs_report: EvidenceValidationReport
    drift: EditorialDriftAssessment
    editorial_confidence: EditorialConfidence
    audited_content: PublicationContent

    def __post_init__(self) -> None:
        if not isinstance(self.lmhs_report, EvidenceValidationReport):
            raise ValueError("Editorial Audit requires an LMHS Assessment.")
        if not isinstance(self.drift, EditorialDriftAssessment):
            raise ValueError("Editorial Audit requires an Editorial Drift assessment.")
        if self.editorial_confidence is not self.lmhs_report.editorial_confidence:
            raise ValueError(
                "Editorial Confidence must reflect the LMHS Assessment just produced."
            )

    @property
    def editorial_risk(self) -> EditorialRisk:
        return self.lmhs_report.editorial_risk


def perform_editorial_audit(
    claims: Iterable[Claim],
    evidence: Iterable[EvidenceRecord],
    *,
    generated_content: PublicationContent,
    current_content: PublicationContent,
    current_on: date | None = None,
) -> EditorialAuditResult:
    """Produce one Editorial Audit result without mutating any input."""
    lmhs_report = validate_evidence(claims, evidence, current_on=current_on)
    drift = compute_editorial_drift(generated_content, current_content)
    return EditorialAuditResult(
        lmhs_report=lmhs_report,
        drift=drift,
        editorial_confidence=lmhs_report.editorial_confidence,
        audited_content=current_content,
    )
