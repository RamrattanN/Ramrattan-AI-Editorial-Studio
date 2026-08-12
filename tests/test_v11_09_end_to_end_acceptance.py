"""Canonical Version 1.1 end-to-end Author acceptance evidence."""

from __future__ import annotations

from datetime import date
import inspect
import json
from pathlib import Path
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
    GenerationStatus,
    WorkflowMode,
)
from studio.editorial_discernment import (
    EditorialIntent,
    EditorialSession,
    WorkspaceState,
)
from studio.evidence_validation import (
    Claim,
    ClaimClassification,
    EvidencePosition,
    EvidenceRecord,
)
from studio.hero_visual import HeroVisualRequest
from studio.portable_editorial_project import deserialize_project
from studio.publication_studio import PublicationEditorAction


CURRENT_ON = date(2026, 8, 5)
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
        "Evidence exposes assumptions before they become polished claims.",
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

ACCEPTANCE_TRACEABILITY = {
    "AC-ENTRY-1 through AC-ENTRY-8": "V11-01 and V11-07 acceptance tests",
    "AC-CONFIG-1 through AC-CONFIG-17": "V11-01, V11-02, and V11-08 acceptance tests",
    "AC-WORKFLOW-1 through AC-WORKFLOW-6": "V11-01 and V11-02 acceptance tests",
    "AC-SRC-1 through AC-SRC-4": "V11-02 and V11-03 acceptance tests",
    "AC-BRD-1 through AC-BRD-5": "V11-02 acceptance tests",
    "AC-DISC-1 through AC-DISC-5": "V11-03 acceptance tests",
    "AC-PLAN-1 through AC-PLAN-4": "V11-03 acceptance tests",
    "AC-GEN-1 through AC-GEN-7": "V11-04 acceptance tests",
    "AC-PSTUDIO-1 through AC-PSTUDIO-3": "V11-05 acceptance tests",
    "AC-EDITOR-1 through AC-EDITOR-6": "V11-05 and V11-06 acceptance tests",
    "AC-CONTENT-1 through AC-CONTENT-4": "V11-05 acceptance tests",
    "AC-REVIEW-1 through AC-REVIEW-4": "V11-05 acceptance tests",
    "AC-AUDIT-1 through AC-AUDIT-13": "V11-06 acceptance tests",
    "AC-LEAVE-1 through AC-LEAVE-3": "V11-08 and V11-09 acceptance tests",
    "AC-COMPLETE-1 through AC-COMPLETE-5": "V11-08 acceptance tests",
    "AC-XCUT-1 through AC-XCUT-5": "V11-09 acceptance tests",
}


def evidence(count: int = 2) -> tuple[EvidenceRecord, ...]:
    return tuple(
        EvidenceRecord(
            source_identifier=f"source-{number}",
            claim_identifier=CLAIM.identifier,
            position=EvidencePosition.SUPPORTS,
            independent_group=f"group-{number}",
            published_on=date(2026, 7, 1),
        )
        for number in range(1, count + 1)
    )


def generation_request(count: int = 2) -> GenerationRequest:
    records = evidence(count)
    attributions = tuple(
        SourceAttribution(
            record.source_identifier,
            f"{record.source_identifier} — reviewed evidence",
        )
        for record in records
    ) or (SourceAttribution("unverified", "Unverified source material"),)
    article = ArticleRequest(
        intent_identifier="v11-09-canonical-session",
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
        source_attributions=attributions,
    )
    return GenerationRequest(
        article=article,
        claims=(CLAIM,),
        evidence=records,
        hero_visual=HeroVisualRequest(
            prompt=article.hero_visual_prompt,
            visual_intent="Show disciplined review protecting trust.",
            brand_context="Approved business branding",
        ),
        current_on=CURRENT_ON,
    )


def start_to_generation(
    mode: WorkflowMode,
    *,
    configuration: bytes | None = None,
) -> AuthorJourney:
    journey = AuthorJourney()
    journey.begin()
    journey.choose_entry_path(EntryPath.START_NEW_PUBLICATION)
    if configuration is None:
        journey.skip_configuration()
    else:
        journey.load_configuration(
            "Ramrattan-AI-Configuration-2026.08.05v01.json",
            configuration,
        )
    journey.select_workflow(mode)
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
    journey.review_discovery()
    journey.approve_discovery()
    journey.propose_plan(PLAN)
    journey.review_plan()
    journey.approve_plan()
    return journey


def complete_new_session(
    mode: WorkflowMode,
    *,
    generate_configuration: bool,
    configuration: bytes | None = None,
):
    journey = start_to_generation(mode, configuration=configuration)
    outcome = journey.run_generation(generation_request())
    assert outcome.status is GenerationStatus.COMPLETE
    journey.edit_publication(
        headline=f"{PLAN.headline} — Author Final",
        cta="What evidence gate will you strengthen next?",
    )
    journey.request_editorial_audit()
    journey.complete_editorial_audit(current_on=CURRENT_ON)
    copied = journey.copy_linkedin_publication()
    journey.signal_completion()
    prompt = journey.completion_prompt()
    artifacts = journey.complete_session(
        generate_configuration=generate_configuration,
        completed_on=CURRENT_ON,
    )
    return journey, artifacts, copied, prompt


class CanonicalAuthorJourneyTests(unittest.TestCase):
    def test_guided_workflow_runs_from_welcome_to_complete(self) -> None:
        journey, artifacts, copied, prompt = complete_new_session(
            WorkflowMode.GUIDED,
            generate_configuration=True,
        )
        self.assertEqual(journey.state, AuthorJourneyState.COMPLETE)
        self.assertIn("Author Final", copied)
        self.assertIn("generate a Ramrattan AI Configuration", prompt)
        self.assertIsNotNone(artifacts.configuration)
        self.assertTrue(artifacts.publication_package.version_one_complete)
        self.assertEqual(
            deserialize_project(
                artifacts.portable_editorial_project.content.decode("utf-8")
            ).article_markdown,
            artifacts.publication_package.article_markdown,
        )

    def test_express_workflow_uses_same_gates_and_completes(self) -> None:
        journey = start_to_generation(WorkflowMode.EXPRESS)
        self.assertEqual(journey.state, AuthorJourneyState.GENERATION)
        self.assertIsNotNone(journey.approved_editorial_plan)
        journey.run_generation(generation_request())
        journey.signal_completion()
        artifacts = journey.complete_session(
            generate_configuration=False,
            completed_on=CURRENT_ON,
        )
        self.assertEqual(journey.state, AuthorJourneyState.COMPLETE)
        self.assertIsNone(artifacts.configuration)

    def test_resume_entry_runs_validation_to_complete_without_new_generation(self) -> None:
        _, first_artifacts, _, _ = complete_new_session(
            WorkflowMode.GUIDED,
            generate_configuration=False,
        )
        session = EditorialSession(
            intent=EditorialIntent(
                primary_topic="Evidence-led review",
                editorial_objective=INFERENCE.intent,
                intended_audience=INFERENCE.audience,
                publication_goal=INFERENCE.desired_outcome,
            ),
            workspace_state=WorkspaceState.PAUSED,
        )
        journey = AuthorJourney(session)
        journey.begin()
        journey.choose_entry_path(EntryPath.RESUME_EXISTING_PROJECT)
        resumed = journey.resume_existing_project(
            first_artifacts.portable_editorial_project.content.decode("utf-8"),
            current_on=CURRENT_ON,
        )
        self.assertTrue(resumed.succeeded)
        self.assertEqual(journey.state, AuthorJourneyState.PUBLICATION_STUDIO)
        self.assertIsNone(journey.workflow_mode)
        self.assertIsNone(journey.generation_outcome)
        journey.edit_publication(headline="Resumed Author Final")
        journey.signal_completion()
        artifacts = journey.complete_session(
            generate_configuration=False,
            completed_on=CURRENT_ON,
            existing_project_names=(
                first_artifacts.portable_editorial_project.filename,
            ),
        )
        self.assertEqual(journey.state, AuthorJourneyState.COMPLETE)
        self.assertEqual(artifacts.publication_package.headline, "Resumed Author Final")

    def test_blocked_generation_returns_to_plan_then_recovers(self) -> None:
        journey = start_to_generation(WorkflowMode.GUIDED)
        blocked = journey.run_generation(generation_request(0))
        self.assertEqual(blocked.status, GenerationStatus.BLOCKED)
        self.assertEqual(journey.state, AuthorJourneyState.EDITORIAL_PLAN)
        journey.approve_plan()
        self.assertEqual(
            journey.run_generation(generation_request()).status,
            GenerationStatus.COMPLETE,
        )

    def test_configuration_round_trip_connects_two_stateless_sessions(self) -> None:
        first, artifacts, _, _ = complete_new_session(
            WorkflowMode.GUIDED,
            generate_configuration=True,
        )
        self.assertEqual(first.__dict__, {"state": AuthorJourneyState.COMPLETE})
        assert artifacts.configuration is not None
        second = AuthorJourney()
        second.begin()
        second.choose_entry_path(EntryPath.START_NEW_PUBLICATION)
        second.load_configuration(
            artifacts.configuration.filename,
            artifacts.configuration.content,
        )
        self.assertEqual(second.workflow_mode, WorkflowMode.GUIDED)
        self.assertEqual(second.branding_preference, "business")
        self.assertIsNone(second.editorial_source)
        self.assertIsNone(second.publication_studio)


class CrossCuttingAcceptanceTests(unittest.TestCase):
    def test_stateless_completion_and_no_persistent_identity(self) -> None:
        journey, _, _, _ = complete_new_session(
            WorkflowMode.GUIDED,
            generate_configuration=False,
        )
        self.assertEqual(journey.__dict__, {"state": AuthorJourneyState.COMPLETE})
        parameters = inspect.signature(AuthorJourney).parameters
        self.assertNotIn("account", parameters)
        self.assertNotIn("login", parameters)
        self.assertNotIn("user_id", parameters)

    def test_publication_studio_has_no_rewrite_or_publish_action(self) -> None:
        self.assertEqual(
            tuple(PublicationEditorAction),
            (PublicationEditorAction.COPY_LINKEDIN_PUBLICATION,),
        )
        prohibited = {
            "rewrite",
            "regenerate",
            "improve",
            "shorten",
            "expand",
            "publish",
            "transmit",
        }
        self.assertTrue(prohibited.isdisjoint(vars(AuthorJourney)))

    def test_source_and_branding_remain_structurally_independent(self) -> None:
        source_parameters = inspect.signature(
            AuthorJourney.submit_editorial_source
        ).parameters
        branding_parameters = inspect.signature(AuthorJourney.submit_branding).parameters
        self.assertNotIn("branding", source_parameters)
        self.assertNotIn("source", branding_parameters)
        self.assertNotIn("inference", branding_parameters)

    def test_acceptance_traceability_covers_every_governing_group(self) -> None:
        self.assertEqual(len(ACCEPTANCE_TRACEABILITY), 16)
        self.assertTrue(all(ACCEPTANCE_TRACEABILITY.values()))
        root = Path(__file__).resolve().parents[1]
        for slice_number in range(1, 9):
            pattern = f"tests/test_v11_{slice_number:02d}_*.py"
            self.assertTrue(tuple(root.glob(pattern)), pattern)


if __name__ == "__main__":
    unittest.main()
