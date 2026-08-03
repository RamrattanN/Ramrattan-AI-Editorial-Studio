"""Behavioural tests for Capability 008 Evidence Validation."""

from datetime import date
import unittest

from studio import editorial_discernment, editorial_intake
from studio.editorial_discernment import EditorialIntent, EditorialSession
from studio.editorial_guidance import (
    EditorialStage,
    STAGE_NAMES,
    STAGE_ORDER,
    StageState,
    initial_stage_states,
    transition_stage,
)
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
    if values["classification"] in {
        ClaimClassification.AUTHOR_EXPERIENCE,
        ClaimClassification.OPINION,
    }:
        values.setdefault("attribution", "the Author")
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

    def test_verified_fact_cannot_be_selected_initially(self):
        with self.assertRaisesRegex(ValueError, "earned"):
            claim(classification=ClaimClassification.VERIFIED_FACT)

    def test_author_experience_and_opinion_require_attribution(self):
        for classification in (
            ClaimClassification.AUTHOR_EXPERIENCE,
            ClaimClassification.OPINION,
        ):
            with self.subTest(classification=classification):
                with self.assertRaisesRegex(ValueError, "attribution"):
                    Claim(
                        identifier="attributed",
                        text="The Author describes a professional judgement.",
                        classification=classification,
                    )


class CorroborationTests(unittest.TestCase):
    def setUp(self):
        self.validator = EvidenceValidator(current_on=date(2026, 8, 1))

    def test_two_independent_sources_verify_claim(self):
        result = self.validator.assess(
            claim(),
            (evidence("primary", "publisher-a"), evidence("audit", "publisher-b")),
        )
        self.assertIs(result.evidence_status, EvidenceStatus.VERIFIED)
        self.assertIs(
            result.resolved_classification,
            ClaimClassification.VERIFIED_FACT,
        )
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

    def test_duplicate_source_identifier_cannot_manufacture_independence(self):
        result = self.validator.assess(
            claim(),
            (
                evidence("Same Source", "publisher-a"),
                evidence(" same source ", "publisher-b"),
            ),
        )
        self.assertIs(result.evidence_status, EvidenceStatus.PARTIALLY_SUPPORTED)
        self.assertEqual(result.independent_support_count, 1)
        self.assertEqual(result.supporting_sources, ("Same Source",))

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
        self.assertIs(
            result.resolved_classification,
            ClaimClassification.OPINION,
        )
        self.assertIn("the Author", result.explanation)

    def test_inference_forecast_and_uncertainty_never_become_verified_fact(self):
        for classification in (
            ClaimClassification.REASONABLE_INFERENCE,
            ClaimClassification.FORECAST,
            ClaimClassification.UNRESOLVED_UNCERTAINTY,
        ):
            with self.subTest(classification=classification):
                result = self.validator.assess(
                    claim(classification=classification),
                    (evidence("a", "a"), evidence("b", "b")),
                )
                self.assertIs(
                    result.resolved_classification,
                    classification,
                )
                self.assertIs(
                    result.evidence_status,
                    EvidenceStatus.PARTIALLY_SUPPORTED,
                )

    def test_stale_time_sensitive_evidence_cannot_earn_verified_fact(self):
        result = self.validator.assess(
            claim(time_sensitive=True),
            (
                evidence("old-a", "a", published_on=date(2024, 1, 1)),
                evidence("old-b", "b", published_on=date(2024, 2, 1)),
            ),
        )
        self.assertIs(result.temporal_status, TemporalStatus.OUTDATED)
        self.assertIs(
            result.resolved_classification,
            ClaimClassification.SOURCE_ASSERTION,
        )
        self.assertIs(result.evidence_status, EvidenceStatus.PARTIALLY_SUPPORTED)


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
        self.assertFalse(result.publication_blocked)
        self.assertEqual(result.significant_findings, ())

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
        self.assertTrue(result.publication_blocked)
        self.assertIn("blocked", result.author_message.lower())

    def test_contradicted_material_claim_is_severe(self):
        result = self.report(
            claim(),
            (evidence("refutation", "a", position=EvidencePosition.CONTRADICTS),),
        )
        self.assertIs(result.editorial_risk, EditorialRisk.SEVERE)
        self.assertIs(result.editorial_confidence, EditorialConfidence.NOT_READY)
        self.assertTrue(result.publication_blocked)
        self.assertIn("Publication gate", result.significant_findings[-1])

    def test_nonmaterial_contradiction_is_moderate_not_low(self):
        result = self.report(
            claim(material=False),
            (evidence("refutation", "a", position=EvidencePosition.CONTRADICTS),),
        )
        self.assertIs(result.editorial_risk, EditorialRisk.MODERATE)
        self.assertFalse(result.publication_blocked)

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


class CanonicalStageStateTests(unittest.TestCase):
    def test_all_runtime_components_share_one_stage_state(self):
        self.assertIs(editorial_intake.StageState, StageState)
        self.assertIs(editorial_discernment.StageState, StageState)
        self.assertEqual(
            tuple(StageState),
            (
                StageState.NOT_STARTED,
                StageState.IN_PROGRESS,
                StageState.COMPLETE,
                StageState.BLOCKED,
            ),
        )

    def test_stage_names_and_order_are_canonical(self):
        self.assertEqual(tuple(STAGE_ORDER), tuple(EditorialStage))
        self.assertEqual(tuple(int(stage) for stage in STAGE_ORDER), (1, 2, 3, 4, 5))
        self.assertEqual(
            tuple(STAGE_NAMES[int(stage)] for stage in STAGE_ORDER),
            editorial_intake.EditorialWorkspace.STAGE_NAMES,
        )

    def test_later_stage_cannot_start_before_prior_stages_complete(self):
        with self.assertRaisesRegex(ValueError, "Earlier stages"):
            transition_stage(initial_stage_states(), 2, StageState.IN_PROGRESS)

    def test_invalid_external_snapshot_cannot_skip_an_incomplete_stage(self):
        states = initial_stage_states()
        states[3] = StageState.IN_PROGRESS
        with self.assertRaisesRegex(ValueError, "skip"):
            transition_stage(states, 3, StageState.COMPLETE)

    def test_complete_stage_cannot_reopen(self):
        states = transition_stage(initial_stage_states(), 1, StageState.COMPLETE)
        with self.assertRaisesRegex(ValueError, "not allowed"):
            transition_stage(states, 1, StageState.IN_PROGRESS)

    def test_blocked_stage_can_resume_but_not_skip_order(self):
        states = transition_stage(initial_stage_states(), 1, StageState.BLOCKED)
        states = transition_stage(states, 1, StageState.IN_PROGRESS)
        states = transition_stage(states, 1, StageState.COMPLETE)
        self.assertIs(states[1], StageState.COMPLETE)

    def test_workspace_state_remains_distinct_from_stage_state(self):
        session = EditorialSession(
            intent=EditorialIntent(
                primary_topic="Editorial integrity",
                editorial_objective="Explain trustworthy evidence",
                intended_audience="professional Authors",
                publication_goal="publish an article",
            )
        )
        session.activate()
        workspace_state = session.workspace_state
        session.mark_stage(1, StageState.IN_PROGRESS)
        self.assertIs(session.workspace_state, workspace_state)


if __name__ == "__main__":
    unittest.main()
