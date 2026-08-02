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
