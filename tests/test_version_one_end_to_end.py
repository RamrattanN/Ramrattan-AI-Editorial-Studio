"""Issue #18 evidence for the connected Version 1 Author journey."""

from dataclasses import fields, replace
from datetime import date
import unittest

from studio.article_engine import (
    ArticleEngine,
    ArticleRequest,
    PublicationBlockedError,
    SourceAttribution,
)
from studio.editorial_discernment import (
    Contribution,
    ContributionKind,
    EditorialComponent,
    EditorialDiscernmentEngine,
    EditorialIntent,
    EditorialSession,
    WorkspaceState,
)
from studio.editorial_guidance import StageState
from studio.editorial_intake import EditorialWorkspace, InputKind
from studio.evidence_validation import (
    Claim,
    ClaimClassification,
    EditorialRisk,
    EvidencePosition,
    EvidenceRecord,
    validate_evidence,
)
from studio.hero_visual import (
    HERO_VISUAL_HEIGHT,
    HERO_VISUAL_WIDTH,
    HeroVisualRequest,
    HeroVisualSystem,
)
from studio.portable_editorial_project import (
    ProjectState,
    article_download,
    from_publication_package,
    hero_visual_download,
    project_download,
    resume_project,
    serialize_project,
    zip_export,
)
from studio.publication_package import PublicationPackageBuilder


class VersionOneEndToEndTests(unittest.TestCase):
    def test_connected_author_journey_and_release_evidence(self):
        intake = EditorialWorkspace().process("https://example.gov/editorial-trust")
        self.assertIs(intake.descriptor.kind, InputKind.URL)
        self.assertEqual(
            [stage.state for stage in intake.stages[:2]],
            [StageState.COMPLETE, StageState.COMPLETE],
        )

        intent = EditorialIntent(
            primary_topic="Evidence-led editorial review",
            editorial_objective="Explain how verification protects trust",
            intended_audience="Professional leaders",
            publication_goal="Publish a professional article",
            scope_terms=("evidence", "editorial", "review", "trust"),
            primary_sources=("source-1", "source-2"),
        )
        session = EditorialSession(intent=intent)
        session.activate()
        for number in range(1, 6):
            session.mark_stage(number, StageState.COMPLETE)
        self.assertIs(session.intent, intent)

        claim = Claim(
            identifier="claim-1",
            text="Structured review reduced avoidable rework.",
            classification=ClaimClassification.SOURCE_ASSERTION,
        )
        records = tuple(
            EvidenceRecord(
                source_identifier=f"source-{number}",
                claim_identifier=claim.identifier,
                position=EvidencePosition.SUPPORTS,
                independent_group=f"group-{number}",
                published_on=date(2026, 7, 1),
            )
            for number in (1, 2)
        )
        evidence = validate_evidence((claim,), records, current_on=date(2026, 8, 2))
        self.assertIs(evidence.editorial_risk, EditorialRisk.LOW)

        article_request = ArticleRequest(
            intent_identifier="issue-18-intent",
            editorial_intent=intent.editorial_objective,
            thesis="Evidence-Led Review Protects Editorial Trust",
            author_perspective="Disciplined review protects both speed and trust.",
            audience=intent.intended_audience,
            insights=(
                "Evidence exposes assumptions before they become polished claims.",
                "Focused revision preserves approved work.",
            ),
            practical_takeaway="Require evidence gates for material claims.",
            cta_question="Where would stronger evidence review improve your decisions?",
            hero_visual_prompt="A restrained editorial evidence checkpoint.",
            hashtags=("#EditorialIntegrity", "#Leadership"),
            linkedin_description="A practical case for evidence-led editorial review.",
            source_attributions=tuple(
                SourceAttribution(f"source-{number}", f"source-{number} — reviewed evidence")
                for number in (1, 2)
            ),
        )
        engine = ArticleEngine()
        draft = engine.create_article(article_request, evidence)
        self.assertEqual(draft.intent_identifier, article_request.intent_identifier)
        self.assertEqual(article_request.editorial_intent, session.intent.editorial_objective)
        self.assertIn("## Sources and Attribution", draft.article_markdown)

        blocked = validate_evidence((claim,), (), current_on=date(2026, 8, 2))
        self.assertIn(blocked.editorial_risk, {EditorialRisk.HIGH, EditorialRisk.SEVERE})
        with self.assertRaises(PublicationBlockedError):
            engine.create_article(article_request, blocked)

        builder = PublicationPackageBuilder()
        package = builder.build(draft, evidence)
        self.assertTrue(all(package.required_text_components()))

        hero = HeroVisualSystem().generate(
            HeroVisualRequest(
                prompt=package.hero_visual_prompt,
                visual_intent="Show disciplined review protecting trust.",
            )
        )
        self.assertTrue(hero.ready)
        self.assertEqual((hero.width, hero.height), (HERO_VISUAL_WIDTH, HERO_VISUAL_HEIGHT))
        with_hero = builder.attach_hero_visual(package, hero)

        portable = from_publication_package(
            with_hero,
            saved_on=date(2026, 8, 2),
            document_version="2026.08.02v01",
        )
        markdown = serialize_project(portable)
        complete_package = builder.attach_portable_editorial_project(with_hero, portable)
        self.assertTrue(complete_package.version_one_complete)
        self.assertEqual(complete_package.deferred_components, ())

        resumed_session = EditorialSession(intent=intent, workspace_state=WorkspaceState.PAUSED)
        resumed = resume_project(markdown, resumed_session, current_on=date(2026, 8, 3))
        self.assertIs(resumed.state, ProjectState.STALE)
        self.assertTrue(resumed.temporal_integrity_review_required)
        self.assertIs(resumed_session.intent, intent)

        for component in (
            EditorialComponent.HEADLINE,
            EditorialComponent.HOOK,
            EditorialComponent.HERO_VISUAL,
        ):
            resumed_session.approve(component)
        decision = EditorialDiscernmentEngine().classify(
            resumed_session,
            Contribution(
                text="Revise only the call to action.",
                target_component=EditorialComponent.CTA,
                declared_kind=ContributionKind.REVISE_COMPONENT,
            ),
        )
        self.assertEqual(decision.affected_components, (EditorialComponent.CTA,))
        self.assertEqual(
            set(decision.protected_components), resumed_session.approved_components
        )
        revised = replace(complete_package, cta="What evidence gate will you strengthen next?")
        changed = {
            field.name
            for field in fields(complete_package)
            if getattr(complete_package, field.name) != getattr(revised, field.name)
        }
        self.assertEqual(changed, {"cta"})

        self.assertTrue(article_download(portable).content)
        self.assertEqual(hero_visual_download(complete_package, portable).content, hero.artifact)
        self.assertEqual(project_download(portable).content.decode(), markdown)
        self.assertTrue(zip_export(portable, complete_package).content)


if __name__ == "__main__":
    unittest.main()
