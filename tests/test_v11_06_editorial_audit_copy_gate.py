"""Acceptance tests for V11-06 Editorial Audit and the Copy Gate."""

from __future__ import annotations

from datetime import date, timedelta
import unittest

from studio.article_engine import ArticleRequest, SourceAttribution
from studio.author_journey import (
    AuthorJourney,
    AuthorJourneyError,
    AuthorJourneyState,
    BrandingMaterial,
    BrandingMaterialKind,
    BrandingMode,
    EditorialInference,
    EditorialPlan,
    EditorialSourceKind,
    EditorialSourceMaterial,
    EntryPath,
    GenerationRequest,
    InvalidAuthorJourneyTransition,
    WorkflowMode,
)
from studio.editorial_audit import (
    EditorialAuditResult,
    EditorialDriftAssessment,
    compute_editorial_drift,
    perform_editorial_audit,
)
from studio.evidence_validation import (
    Claim,
    ClaimClassification,
    EditorialConfidence,
    EditorialRisk,
    EvidencePosition,
    EvidenceRecord,
)
from studio.hero_visual import HeroVisualRequest
from studio.publication_studio import (
    CopyGateState,
    PublicationContent,
    PublicationStudioError,
)


CURRENT_ON = date(2026, 8, 4)
INFERENCE = EditorialInference(
    intent="Explain why evidence-led review protects trust.",
    audience="Editorial leaders",
    platform="LinkedIn",
    desired_outcome="Help leaders adopt an explicit review gate.",
)
PLAN = EditorialPlan(
    headline="Evidence-Led Review Protects Trust",
    hook="Disciplined review protects both speed and trust.",
    key_insights=(
        "Evidence exposes assumptions before publication.",
        "Approval preserves Author control before generation.",
    ),
    practical_takeaway="Require evidence gates for material claims.",
    call_to_action="Where would stronger review improve your decisions?",
)
CLAIM = Claim(
    identifier="claim-1",
    text="Structured review reduced avoidable rework.",
    classification=ClaimClassification.SOURCE_ASSERTION,
)
TIME_SENSITIVE_CLAIM = Claim(
    identifier="claim-2",
    text="Adoption accelerated across reviewed teams this quarter.",
    classification=ClaimClassification.SOURCE_ASSERTION,
    time_sensitive=True,
)


def generation_request(
    *, claims: tuple[Claim, ...] = (CLAIM,), evidence: tuple[EvidenceRecord, ...] | None = None
) -> GenerationRequest:
    if evidence is None:
        evidence = tuple(
            EvidenceRecord(
                source_identifier=f"source-{number}",
                claim_identifier=CLAIM.identifier,
                position=EvidencePosition.SUPPORTS,
                independent_group=f"group-{number}",
                published_on=date(2026, 7, 1),
            )
            for number in (1, 2)
        )
    article = ArticleRequest(
        intent_identifier="v11-06-intent",
        editorial_intent=INFERENCE.intent,
        thesis=PLAN.headline,
        author_perspective=PLAN.hook,
        audience=INFERENCE.audience,
        insights=PLAN.key_insights,
        practical_takeaway=PLAN.practical_takeaway,
        cta_question=PLAN.call_to_action,
        hero_visual_prompt="A restrained editorial evidence checkpoint.",
        hashtags=("#EditorialIntegrity", "#Leadership"),
        linkedin_description="A practical case for evidence-led review.",
        source_attributions=tuple(
            SourceAttribution(
                item.source_identifier,
                f"{item.source_identifier} — reviewed evidence",
            )
            for item in evidence
        ),
    )
    return GenerationRequest(
        article=article,
        claims=claims,
        evidence=evidence,
        hero_visual=HeroVisualRequest(
            prompt=article.hero_visual_prompt,
            visual_intent="Show disciplined review protecting trust.",
            provider="deterministic",
            brand_context="Approved business branding",
        ),
        current_on=CURRENT_ON,
    )


def journey_at_generation() -> AuthorJourney:
    journey = AuthorJourney()
    journey.begin()
    journey.choose_entry_path(EntryPath.START_NEW_PUBLICATION)
    journey.skip_configuration()
    journey.select_workflow(WorkflowMode.GUIDED)
    journey.submit_editorial_source(
        EditorialSourceMaterial(
            EditorialSourceKind.NOTES,
            "Evidence-led review protects editorial trust.",
        ),
        inference=INFERENCE,
    )
    journey.submit_branding(
        BrandingMode.BUSINESS,
        (BrandingMaterial(BrandingMaterialKind.LOGO, "brand/logo.svg"),),
    )
    journey.approve_discovery()
    journey.propose_plan(PLAN)
    journey.approve_plan()
    return journey


def journey_at_studio(request: GenerationRequest | None = None) -> AuthorJourney:
    journey = journey_at_generation()
    journey.run_generation(request or generation_request())
    return journey


class EditorialDriftTests(unittest.TestCase):
    def test_no_drift_against_unedited_generated_content(self) -> None:
        studio = journey_at_studio().publication_studio
        drift = compute_editorial_drift(
            studio.editor.generated_content, studio.editor.current_content
        )
        self.assertFalse(drift.drifted)
        self.assertEqual(drift.changed_fields, ())

    def test_drift_reports_exactly_the_changed_fields(self) -> None:
        journey = journey_at_studio()
        journey.edit_publication(headline="A new Author-owned headline")
        studio = journey.publication_studio
        drift = compute_editorial_drift(
            studio.editor.generated_content, studio.editor.current_content
        )
        self.assertTrue(drift.drifted)
        self.assertEqual(drift.changed_fields, ("headline",))

    def test_drift_baseline_stays_fixed_across_repeated_edits(self) -> None:
        journey = journey_at_studio()
        studio = journey.publication_studio
        journey.edit_publication(headline="First edit")
        journey.edit_publication(hook="Second, unrelated edit")
        drift = compute_editorial_drift(
            studio.editor.generated_content, studio.editor.current_content
        )
        self.assertEqual(drift.changed_fields, ("headline", "hook"))


class EditorialAuditExecutionTests(unittest.TestCase):
    def test_audit_produces_lmhs_assessment_drift_and_confidence(self) -> None:
        journey = journey_at_studio()
        journey.request_editorial_audit()
        result = journey.complete_editorial_audit(current_on=CURRENT_ON)
        self.assertIsInstance(result, EditorialAuditResult)
        self.assertEqual(result.lmhs_report.editorial_risk, EditorialRisk.LOW)
        self.assertEqual(result.editorial_confidence, EditorialConfidence.READY)
        self.assertIsInstance(result.drift, EditorialDriftAssessment)
        self.assertFalse(result.drift.drifted)
        self.assertEqual(journey.last_audit_result, result)

    def test_audit_returns_to_author_editing_automatically(self) -> None:
        journey = journey_at_studio()
        journey.request_editorial_audit()
        self.assertEqual(journey.state, AuthorJourneyState.EDITORIAL_AUDIT)
        journey.complete_editorial_audit()
        self.assertEqual(journey.state, AuthorJourneyState.PUBLICATION_STUDIO)

    def test_audit_never_modifies_publication_content(self) -> None:
        journey = journey_at_studio()
        journey.edit_publication(cta="The Author's own question?")
        studio = journey.publication_studio
        before = studio.editor.current_content
        journey.request_editorial_audit()
        journey.complete_editorial_audit()
        self.assertIs(studio.editor.current_content, before)

    def test_audit_transmits_nothing_externally(self) -> None:
        journey = journey_at_studio()
        journey.request_editorial_audit()
        result = journey.complete_editorial_audit()
        for action in ("publish", "send", "transmit", "upload"):
            self.assertFalse(hasattr(result, action))

    def test_perform_editorial_audit_is_a_pure_function(self) -> None:
        studio = journey_at_studio().publication_studio
        result_one = perform_editorial_audit(
            (CLAIM,),
            generation_request().evidence,
            generated_content=studio.editor.generated_content,
            current_content=studio.editor.current_content,
            current_on=CURRENT_ON,
        )
        result_two = perform_editorial_audit(
            (CLAIM,),
            generation_request().evidence,
            generated_content=studio.editor.generated_content,
            current_content=studio.editor.current_content,
            current_on=CURRENT_ON,
        )
        self.assertEqual(result_one, result_two)


class CopyGateTests(unittest.TestCase):
    def test_gate_is_unmatched_and_copy_disabled_before_any_audit(self) -> None:
        journey = journey_at_studio()
        studio = journey.publication_studio
        self.assertEqual(studio.copy_gate_state, CopyGateState.UNMATCHED)
        self.assertFalse(studio.presentation().copy_action_enabled)
        with self.assertRaises(PublicationStudioError):
            journey.copy_linkedin_publication()

    def test_gate_matches_after_a_completed_audit(self) -> None:
        journey = journey_at_studio()
        journey.request_editorial_audit()
        journey.complete_editorial_audit()
        studio = journey.publication_studio
        self.assertEqual(studio.copy_gate_state, CopyGateState.MATCHED)
        self.assertTrue(studio.presentation().copy_action_enabled)
        payload = journey.copy_linkedin_publication()
        self.assertIn(studio.editor.current_content.headline, payload)

    def test_edit_after_matched_audit_resets_gate_to_unmatched(self) -> None:
        journey = journey_at_studio()
        journey.request_editorial_audit()
        journey.complete_editorial_audit()
        journey.edit_publication(hook="A late Author revision.")
        studio = journey.publication_studio
        self.assertEqual(studio.copy_gate_state, CopyGateState.UNMATCHED)
        with self.assertRaises(PublicationStudioError):
            journey.copy_linkedin_publication()

    def test_repeated_audits_with_intervening_edits(self) -> None:
        journey = journey_at_studio()
        journey.request_editorial_audit()
        journey.complete_editorial_audit()
        self.assertEqual(
            journey.publication_studio.copy_gate_state, CopyGateState.MATCHED
        )
        journey.edit_publication(cta="A revised call to action?")
        self.assertEqual(
            journey.publication_studio.copy_gate_state, CopyGateState.UNMATCHED
        )
        journey.request_editorial_audit()
        journey.complete_editorial_audit()
        self.assertEqual(
            journey.publication_studio.copy_gate_state, CopyGateState.MATCHED
        )

    def test_copy_payload_excludes_editorial_review_content(self) -> None:
        journey = journey_at_studio()
        journey.request_editorial_audit()
        journey.complete_editorial_audit()
        studio = journey.publication_studio
        payload = journey.copy_linkedin_publication()
        self.assertNotIn(studio.editorial_review.branding_summary, payload)
        self.assertNotIn(studio.editorial_review.session_summary, payload)


class HighSeverityAuditTests(unittest.TestCase):
    def _journey_with_time_sensitive_evidence(self) -> AuthorJourney:
        evidence = (
            EvidenceRecord(
                source_identifier="source-1",
                claim_identifier=TIME_SENSITIVE_CLAIM.identifier,
                position=EvidencePosition.SUPPORTS,
                independent_group="group-1",
                published_on=CURRENT_ON,
            ),
            EvidenceRecord(
                source_identifier="source-2",
                claim_identifier=TIME_SENSITIVE_CLAIM.identifier,
                position=EvidencePosition.SUPPORTS,
                independent_group="group-2",
                published_on=CURRENT_ON,
            ),
        )
        return journey_at_studio(
            generation_request(
                claims=(TIME_SENSITIVE_CLAIM,), evidence=evidence
            )
        )

    def test_generation_time_assessment_is_not_high_risk(self) -> None:
        journey = self._journey_with_time_sensitive_evidence()
        self.assertEqual(
            journey.publication_studio.editorial_review.editorial_risk,
            EditorialRisk.LOW,
        )

    def test_high_risk_audit_withholds_positive_confidence(self) -> None:
        journey = self._journey_with_time_sensitive_evidence()
        journey.request_editorial_audit()
        later = CURRENT_ON + timedelta(days=400)
        result = journey.complete_editorial_audit(current_on=later)
        self.assertEqual(result.editorial_risk, EditorialRisk.HIGH)
        self.assertNotEqual(result.editorial_confidence, EditorialConfidence.READY)

    def test_high_risk_still_matches_the_gate(self) -> None:
        journey = self._journey_with_time_sensitive_evidence()
        journey.request_editorial_audit()
        later = CURRENT_ON + timedelta(days=400)
        journey.complete_editorial_audit(current_on=later)
        studio = journey.publication_studio
        self.assertEqual(studio.copy_gate_state, CopyGateState.MATCHED)
        self.assertTrue(studio.presentation().copy_action_enabled)

    def test_high_risk_never_rewrites_content(self) -> None:
        journey = self._journey_with_time_sensitive_evidence()
        studio = journey.publication_studio
        before = studio.editor.current_content
        journey.request_editorial_audit()
        later = CURRENT_ON + timedelta(days=400)
        journey.complete_editorial_audit(current_on=later)
        self.assertIs(studio.editor.current_content, before)

    def test_high_risk_copy_still_enabled_once_matched(self) -> None:
        journey = self._journey_with_time_sensitive_evidence()
        journey.request_editorial_audit()
        later = CURRENT_ON + timedelta(days=400)
        journey.complete_editorial_audit(current_on=later)
        payload = journey.copy_linkedin_publication()
        self.assertIsInstance(payload, str)


class EditorialReviewRefreshTests(unittest.TestCase):
    def test_review_reflects_the_most_recent_completed_audit(self) -> None:
        journey = journey_at_studio()
        journey.edit_publication(headline="Author's own headline")
        journey.request_editorial_audit()
        result = journey.complete_editorial_audit()
        review = journey.publication_studio.editorial_review
        self.assertEqual(review.editorial_confidence, result.editorial_confidence)
        self.assertEqual(review.editorial_risk, result.editorial_risk)
        self.assertFalse(review.may_not_reflect_current_edits)
        self.assertEqual(review.assessment_label, "As of most recent Editorial Audit")

    def test_edit_after_audit_marks_review_stale_again(self) -> None:
        journey = journey_at_studio()
        journey.request_editorial_audit()
        journey.complete_editorial_audit()
        journey.edit_publication(hook="One more Author change.")
        review = journey.publication_studio.editorial_review
        self.assertTrue(review.may_not_reflect_current_edits)
        self.assertIn("unaudited Author edits", review.assessment_label)
        self.assertIn("Editorial Audit", review.assessment_label)


class InvalidTransitionTests(unittest.TestCase):
    def test_complete_audit_without_request_fails_closed(self) -> None:
        journey = journey_at_studio()
        with self.assertRaises(InvalidAuthorJourneyTransition):
            journey.complete_editorial_audit()
        self.assertEqual(journey.state, AuthorJourneyState.PUBLICATION_STUDIO)

    def test_complete_audit_before_publication_studio_fails_closed(self) -> None:
        journey = journey_at_generation()
        with self.assertRaises(InvalidAuthorJourneyTransition):
            journey.complete_editorial_audit()

    def test_signal_completion_requires_author_editing(self) -> None:
        journey = journey_at_studio()
        journey.request_editorial_audit()
        with self.assertRaises(InvalidAuthorJourneyTransition):
            journey.signal_completion()
        self.assertEqual(journey.state, AuthorJourneyState.EDITORIAL_AUDIT)

    def test_signal_completion_succeeds_without_any_audit(self) -> None:
        journey = journey_at_studio()
        journey.signal_completion()
        self.assertEqual(journey.state, AuthorJourneyState.SESSION_COMPLETION)

    def test_copy_linkedin_publication_before_publication_studio_fails_closed(
        self,
    ) -> None:
        journey = journey_at_generation()
        with self.assertRaises(InvalidAuthorJourneyTransition):
            journey.copy_linkedin_publication()

    def test_audit_editorial_confidence_must_match_lmhs_report(self) -> None:
        studio = journey_at_studio().publication_studio
        report = perform_editorial_audit(
            (CLAIM,),
            generation_request().evidence,
            generated_content=studio.editor.generated_content,
            current_content=studio.editor.current_content,
            current_on=CURRENT_ON,
        ).lmhs_report
        with self.assertRaises(ValueError):
            EditorialAuditResult(
                lmhs_report=report,
                drift=compute_editorial_drift(
                    studio.editor.generated_content, studio.editor.current_content
                ),
                editorial_confidence=EditorialConfidence.NOT_READY,
                audited_content=studio.editor.current_content,
            )


class NoAuthorRewritingTests(unittest.TestCase):
    def test_journey_exposes_no_direct_audit_runner(self) -> None:
        journey = journey_at_studio()
        self.assertFalse(hasattr(journey, "run_editorial_audit"))

    def test_audit_result_exposes_no_rewrite_actions(self) -> None:
        journey = journey_at_studio()
        journey.request_editorial_audit()
        result = journey.complete_editorial_audit()
        for action in ("rewrite", "regenerate", "improve", "shorten", "expand"):
            self.assertFalse(hasattr(result, action))

    def test_sessions_are_stateless_and_independent(self) -> None:
        first = journey_at_studio()
        second = journey_at_studio()
        first.edit_publication(headline="Only in the first session")
        first.request_editorial_audit()
        first.complete_editorial_audit()
        self.assertIsNone(second.last_audit_result)
        self.assertEqual(
            second.publication_studio.copy_gate_state, CopyGateState.UNMATCHED
        )


if __name__ == "__main__":
    unittest.main()
