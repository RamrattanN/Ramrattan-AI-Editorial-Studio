"""Acceptance tests for the V11-05 Publication Studio workspace."""

from __future__ import annotations

from dataclasses import replace
from datetime import date
import unittest

from studio.article_engine import ArticleRequest, SourceAttribution
from studio.author_journey import (
    AuthorJourney,
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
from studio.evidence_validation import (
    Claim,
    ClaimClassification,
    EditorialRisk,
    EvidencePosition,
    EvidenceRecord,
)
from studio.hero_visual import HeroVisualRequest
from studio.publication_studio import (
    CopyGateState,
    HeroVisualAction,
    PublicationContent,
    PublicationEditorAction,
    PublicationStudio,
    PublicationStudioError,
    WorkspaceKind,
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


def generation_request() -> GenerationRequest:
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
        intent_identifier="v11-05-intent",
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
        claims=(CLAIM,),
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


def journey_at_studio() -> AuthorJourney:
    journey = journey_at_generation()
    journey.run_generation(generation_request())
    return journey


class PublicationStudioWorkspaceTests(unittest.TestCase):
    def test_generated_content_enters_publication_studio(self) -> None:
        journey = journey_at_studio()
        studio = journey.publication_studio
        self.assertEqual(journey.state, AuthorJourneyState.PUBLICATION_STUDIO)
        self.assertIsNotNone(studio)
        self.assertEqual(
            studio.editor.generated_content,
            PublicationContent.from_package(studio.generated_package),
        )

    def test_presentation_has_two_distinct_workspaces(self) -> None:
        presentation = journey_at_studio().publication_studio.presentation()
        self.assertEqual(
            presentation.workspaces,
            (WorkspaceKind.HERO_VISUAL, WorkspaceKind.PUBLICATION_EDITOR),
        )
        self.assertTrue(presentation.editorial_review_separate)
        self.assertTrue(presentation.editorial_review_collapsible)

    def test_hero_visual_workspace_has_approved_actions(self) -> None:
        studio = journey_at_studio().publication_studio
        self.assertTrue(studio.hero_visual.visual.ready)
        self.assertEqual(studio.hero_visual.actions, tuple(HeroVisualAction))

    def test_editor_has_exactly_one_studio_action(self) -> None:
        actions = journey_at_studio().publication_studio.editor.studio_actions
        self.assertEqual(
            actions,
            (PublicationEditorAction.COPY_LINKEDIN_PUBLICATION,),
        )

    def test_author_edits_persist_without_rewriting_other_fields(self) -> None:
        journey = journey_at_studio()
        before = journey.publication_studio.editor.current_content
        updated = journey.edit_publication(headline="The Author's exact headline")
        self.assertEqual(updated.headline, "The Author's exact headline")
        self.assertEqual(updated.article, before.article)
        self.assertIs(journey.publication_studio.editor.current_content, updated)

    def test_formatting_mentions_and_links_remain_exact(self) -> None:
        journey = journey_at_studio()
        exact = "**Author emphasis** for @EditorialLead: [source](https://example.com)."
        journey.edit_publication(article=exact)
        self.assertEqual(journey.publication_studio.editor.current_content.article, exact)

    def test_original_generation_remains_distinguishable_after_edit(self) -> None:
        journey = journey_at_studio()
        studio = journey.publication_studio
        original = studio.editor.generated_content
        package = studio.generated_package
        journey.edit_publication(hook="An Author-owned revision.")
        self.assertIs(studio.editor.generated_content, original)
        self.assertEqual(package.hook, original.hook)
        self.assertNotEqual(studio.editor.current_content, original)

    def test_editor_exposes_no_ai_rewrite_actions(self) -> None:
        editor = journey_at_studio().publication_studio.editor
        for action in ("rewrite", "regenerate", "improve", "shorten", "expand"):
            self.assertFalse(hasattr(editor, action))

    def test_copy_payload_contains_only_current_publication_content(self) -> None:
        studio = journey_at_studio().publication_studio
        studio.author_edit(headline="Current Author headline")
        payload = studio.editor.copy_payload()
        self.assertIn("Current Author headline", payload)
        self.assertNotIn(studio.editorial_review.branding_summary, payload)
        self.assertNotIn(studio.editorial_review.session_summary, payload)

    def test_absent_optional_fields_are_omitted_without_placeholders(self) -> None:
        generated = journey_at_studio().publication_studio.generated_package
        package = replace(generated, hashtags=(), linkedin_description="")
        studio = PublicationStudio.from_generation(
            package,
            branding_summary="studio theme",
            session_summary="Prepare a publication.",
        )
        rendered = studio.editor.copy_payload()
        self.assertNotIn("Hashtags", rendered)
        self.assertNotIn("LinkedIn Description", rendered)
        self.assertNotIn("None", rendered)

    def test_editorial_review_preserves_generation_context(self) -> None:
        studio = journey_at_studio().publication_studio
        review = studio.editorial_review
        self.assertEqual(review.editorial_risk, EditorialRisk.LOW)
        self.assertEqual(
            review.editorial_confidence,
            studio.generated_package.editorial_confidence,
        )
        self.assertEqual(review.sources, studio.generated_package.source_and_attribution)
        self.assertEqual(review.suggested_mentions, ())
        self.assertIn("business", review.branding_summary)
        self.assertEqual(review.session_summary, INFERENCE.desired_outcome)

    def test_author_edit_marks_generation_review_stale_without_recomputing(self) -> None:
        studio = journey_at_studio().publication_studio
        original_risk = studio.editorial_review.editorial_risk
        original_confidence = studio.editorial_review.editorial_confidence
        studio.author_edit(article="The Author's revised article.")
        self.assertTrue(studio.editorial_review.may_not_reflect_current_edits)
        self.assertIn("unaudited Author edits", studio.editorial_review.assessment_label)
        self.assertEqual(studio.editorial_review.editorial_risk, original_risk)
        self.assertEqual(
            studio.editorial_review.editorial_confidence,
            original_confidence,
        )

    def test_copy_gate_is_unmatched_and_not_enabled(self) -> None:
        studio = journey_at_studio().publication_studio
        self.assertEqual(studio.copy_gate_state, CopyGateState.UNMATCHED)
        self.assertFalse(studio.presentation().copy_action_enabled)

    def test_transition_to_editorial_audit_is_a_seam_only(self) -> None:
        journey = journey_at_studio()
        edited = journey.edit_publication(cta="The Author's final question?")
        audit_input = journey.request_editorial_audit()
        self.assertIs(audit_input, edited)
        self.assertEqual(journey.state, AuthorJourneyState.EDITORIAL_AUDIT)
        self.assertFalse(hasattr(journey, "run_editorial_audit"))

    def test_edit_before_publication_studio_fails_closed(self) -> None:
        journey = journey_at_generation()
        with self.assertRaises(InvalidAuthorJourneyTransition):
            journey.edit_publication(headline="Too early")
        self.assertEqual(journey.state, AuthorJourneyState.GENERATION)

    def test_audit_transition_before_publication_studio_fails_closed(self) -> None:
        journey = journey_at_generation()
        with self.assertRaises(InvalidAuthorJourneyTransition):
            journey.request_editorial_audit()
        self.assertEqual(journey.state, AuthorJourneyState.GENERATION)

    def test_invalid_edit_field_fails_closed(self) -> None:
        journey = journey_at_studio()
        before = journey.publication_studio.editor.current_content
        with self.assertRaises(PublicationStudioError):
            journey.edit_publication(editorial_review="must remain separate")
        self.assertIs(journey.publication_studio.editor.current_content, before)

    def test_sessions_are_stateless_and_independent(self) -> None:
        first = journey_at_studio()
        second = journey_at_studio()
        first.edit_publication(headline="First session only")
        self.assertNotEqual(
            first.publication_studio.editor.current_content.headline,
            second.publication_studio.editor.current_content.headline,
        )


if __name__ == "__main__":
    unittest.main()
