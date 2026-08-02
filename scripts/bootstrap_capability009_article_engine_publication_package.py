#!/usr/bin/env python3
"""Bootstrap Capability 009 - Article Engine and Publication Package.

Preview is non-mutating. ``--apply`` writes the narrow, generator-owned
Capability 009 implementation and runs the canonical validation suite.
The bootstrap deliberately excludes Capability 010 Hero Visual generation,
Capability 011 Portable Editorial Project behavior, and broader workspace,
context, collaboration, or orchestration product surfaces.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import textwrap
from pathlib import Path


EXPECTED_REPOSITORY = "Ramrattan-AI-Editorial-Studio"
EXPECTED_BRANCH = "feature/capability-009-article-engine-publication-package"
SCRIPT_PATH = "scripts/bootstrap_capability009_article_engine_publication_package.py"
SENTINEL = "CAPABILITY_009_ARTICLE_ENGINE_PUBLICATION_PACKAGE_COMPLETE"


class CapabilityError(RuntimeError):
    """Raised when Capability 009 cannot proceed safely."""


def clean(value: str) -> str:
    """Normalize one deterministic text template."""
    return textwrap.dedent(value).strip() + "\n"


FILES = {
    "studio/article_engine.py": clean(
        r'''
        """Provider-independent Article Engine for Capability 009.

        The engine consumes explicit Author-owned editorial inputs and an
        existing Evidence Validation report. It never performs research,
        creates a workspace, persists context, or generates Hero Visuals.
        """

        from __future__ import annotations

        from dataclasses import dataclass
        from typing import Protocol

        from .evidence_validation import (
            EditorialConfidence,
            EditorialRisk,
            EvidenceValidationReport,
        )


        class ArticleEngineError(ValueError):
            """Base error for invalid Article Engine input or output."""


        class PublicationBlockedError(ArticleEngineError):
            """Raised when Editorial Integrity blocks article generation."""


        @dataclass(frozen=True)
        class SourceAttribution:
            """One human-readable source attribution used by the article."""

            source_identifier: str
            citation: str

            def __post_init__(self) -> None:
                if not self.source_identifier.strip() or not self.citation.strip():
                    raise ArticleEngineError(
                        "Source attribution requires an identifier and citation."
                    )


        @dataclass(frozen=True)
        class ArticleRequest:
            """Approved inputs needed to construct one professional article."""

            intent_identifier: str
            editorial_intent: str
            thesis: str
            author_perspective: str
            audience: str
            insights: tuple[str, ...]
            practical_takeaway: str
            cta_question: str
            hero_visual_prompt: str
            hashtags: tuple[str, ...]
            linkedin_description: str
            source_attributions: tuple[SourceAttribution, ...]

            def __post_init__(self) -> None:
                required = (
                    self.intent_identifier,
                    self.editorial_intent,
                    self.thesis,
                    self.author_perspective,
                    self.audience,
                    self.practical_takeaway,
                    self.cta_question,
                    self.hero_visual_prompt,
                    self.linkedin_description,
                )
                if not all(value.strip() for value in required):
                    raise ArticleEngineError(
                        "Article requests require complete approved editorial inputs."
                    )
                if not 1 <= len(self.insights) <= 2:
                    raise ArticleEngineError("An article requires one or two insights.")
                if any(not insight.strip() for insight in self.insights):
                    raise ArticleEngineError("Insights cannot be empty.")
                if not self.cta_question.rstrip().endswith("?"):
                    raise ArticleEngineError(
                        "The CTA must contain an article-specific question."
                    )
                if not self.hashtags or any(
                    not item.startswith("#") or len(item) == 1
                    for item in self.hashtags
                ):
                    raise ArticleEngineError(
                        "Hashtags must contain at least one canonical #tag."
                    )
                if not self.source_attributions:
                    raise ArticleEngineError(
                        "The Publication Package requires source and attribution."
                    )
                identifiers = [
                    item.source_identifier.strip().casefold()
                    for item in self.source_attributions
                ]
                if len(identifiers) != len(set(identifiers)):
                    raise ArticleEngineError(
                        "Source attribution identifiers must be unique."
                    )


        @dataclass(frozen=True)
        class ArticleDraft:
            """One evidence-aligned article draft and its package components."""

            intent_identifier: str
            headline: str
            hook: str
            insights: tuple[str, ...]
            practical_takeaway: str
            cta: str
            source_attributions: tuple[SourceAttribution, ...]
            hashtags: tuple[str, ...]
            linkedin_description: str
            hero_visual_prompt: str
            article_markdown: str
            used_claim_identifiers: tuple[str, ...]


        class ArticleDraftProvider(Protocol):
            """Provider boundary for constructing article language."""

            def create_draft(
                self,
                request: ArticleRequest,
                evidence_report: EvidenceValidationReport,
            ) -> ArticleDraft:
                """Return an original draft grounded in the approved request."""


        class DeterministicArticleDraftProvider:
            """Repository-safe provider that structures approved Author material."""

            def create_draft(
                self,
                request: ArticleRequest,
                evidence_report: EvidenceValidationReport,
            ) -> ArticleDraft:
                headline = request.thesis.strip()
                hook = request.author_perspective.strip()
                insight_blocks = "\n\n".join(
                    f"## Insight {number}\n\n{insight.strip()}"
                    for number, insight in enumerate(request.insights, start=1)
                )
                sources = "\n".join(
                    f"- {source.citation.strip()}"
                    for source in request.source_attributions
                ) or "- Author experience and perspective; no external citation supplied."
                cta = (
                    f"{request.cta_question.strip()}\n\n"
                    "I would value your perspective. Continue the conversation "
                    "in the comments below."
                )
                markdown = (
                    f"# {headline}\n\n"
                    f"{hook}\n\n"
                    f"{insight_blocks}\n\n"
                    "## Practical Takeaway\n\n"
                    f"{request.practical_takeaway.strip()}\n\n"
                    "## Sources and Attribution\n\n"
                    f"{sources}\n\n"
                    "## Continue the Conversation\n\n"
                    f"{cta}\n"
                )
                return ArticleDraft(
                    intent_identifier=request.intent_identifier,
                    headline=headline,
                    hook=hook,
                    insights=tuple(item.strip() for item in request.insights),
                    practical_takeaway=request.practical_takeaway.strip(),
                    cta=cta,
                    source_attributions=request.source_attributions,
                    hashtags=request.hashtags,
                    linkedin_description=request.linkedin_description.strip(),
                    hero_visual_prompt=request.hero_visual_prompt.strip(),
                    article_markdown=markdown,
                    used_claim_identifiers=tuple(
                        item.claim.identifier for item in evidence_report.assessments
                    ),
                )


        class ArticleEngine:
            """Validate integrity gates and construct one ArticleDraft."""

            def __init__(self, provider: ArticleDraftProvider | None = None) -> None:
                self.provider = provider or DeterministicArticleDraftProvider()

            def create_article(
                self,
                request: ArticleRequest,
                evidence_report: EvidenceValidationReport,
            ) -> ArticleDraft:
                if evidence_report.publication_blocked or evidence_report.editorial_risk in {
                    EditorialRisk.HIGH,
                    EditorialRisk.SEVERE,
                }:
                    raise PublicationBlockedError(evidence_report.author_message)
                if evidence_report.editorial_confidence not in {
                    EditorialConfidence.READY,
                    EditorialConfidence.READY_WITH_REVIEW,
                }:
                    raise PublicationBlockedError(
                        "Editorial Confidence does not permit article generation."
                    )

                draft = self.provider.create_draft(request, evidence_report)
                self._validate_draft(request, evidence_report, draft)
                return draft

            @staticmethod
            def _validate_draft(
                request: ArticleRequest,
                evidence_report: EvidenceValidationReport,
                draft: ArticleDraft,
            ) -> None:
                if draft.intent_identifier != request.intent_identifier:
                    raise ArticleEngineError(
                        "The Article Engine must preserve the approved Editorial Intent."
                    )
                required = (
                    draft.headline,
                    draft.hook,
                    draft.practical_takeaway,
                    draft.cta,
                    draft.linkedin_description,
                    draft.hero_visual_prompt,
                    draft.article_markdown,
                )
                if not all(value.strip() for value in required):
                    raise ArticleEngineError(
                        "The Article Engine returned an incomplete article draft."
                    )
                if draft.insights != tuple(item.strip() for item in request.insights):
                    raise ArticleEngineError(
                        "The provider changed approved insights without authorization."
                    )
                known_claims = {
                    item.claim.identifier for item in evidence_report.assessments
                }
                if known_claims and not draft.used_claim_identifiers:
                    raise ArticleEngineError(
                        "The Article Engine must identify validated claims used."
                    )
                if not set(draft.used_claim_identifiers).issubset(known_claims):
                    raise ArticleEngineError(
                        "The draft references claims absent from Evidence Validation."
                    )
                available_sources = {
                    item.source_identifier.strip().casefold()
                    for item in request.source_attributions
                }
                used_sources = {
                    source.strip().casefold()
                    for assessment in evidence_report.assessments
                    if assessment.claim.identifier in draft.used_claim_identifiers
                    for source in (
                        assessment.supporting_sources
                        + assessment.contradicting_sources
                    )
                }
                if not used_sources.issubset(available_sources):
                    raise ArticleEngineError(
                        "Every evidence source used by the article requires attribution."
                    )
        '''
    ),
    "studio/publication_package.py": clean(
        r'''
        """Textual Publication Package assembly for Capability 009.

        Rendered Hero Visual generation remains Capability 010. Portable
        Editorial Project serialization remains Capability 011.
        """

        from __future__ import annotations

        from dataclasses import dataclass
        from enum import Enum

        from .article_engine import ArticleDraft, PublicationBlockedError
        from .evidence_validation import (
            EditorialConfidence,
            EditorialRisk,
            EvidenceValidationReport,
        )


        class PackageReadiness(str, Enum):
            """Capability 009 textual package readiness."""

            READY_FOR_HERO_VISUAL = "ready_for_hero_visual"
            REVIEW_BEFORE_HERO_VISUAL = "review_before_hero_visual"


        @dataclass(frozen=True)
        class PublicationPackage:
            """Validated textual package with later deliverables explicit."""

            article_markdown: str
            hero_visual_prompt: str
            headline: str
            hook: str
            insights: tuple[str, ...]
            practical_takeaway: str
            cta: str
            source_and_attribution: tuple[str, ...]
            hashtags: tuple[str, ...]
            linkedin_description: str
            editorial_confidence: EditorialConfidence
            editorial_risk: EditorialRisk
            readiness: PackageReadiness
            review_findings: tuple[str, ...]
            rendered_hero_visual: None = None
            portable_editorial_project: None = None
            deferred_components: tuple[str, ...] = (
                "Rendered Hero Visual - Capability 010",
                "Portable Editorial Project - Capability 011",
            )
            version_one_complete: bool = False

            def required_text_components(self) -> tuple[str, ...]:
                """Return canonical textual components in package order."""
                return (
                    self.hero_visual_prompt,
                    self.headline,
                    self.hook,
                    *self.insights,
                    self.practical_takeaway,
                    self.cta,
                    *self.source_and_attribution,
                    *self.hashtags,
                    self.linkedin_description,
                    self.article_markdown,
                )


        class PublicationPackageBuilder:
            """Assemble one validated Capability 009 textual package."""

            def build(
                self,
                draft: ArticleDraft,
                evidence_report: EvidenceValidationReport,
            ) -> PublicationPackage:
                if evidence_report.publication_blocked or evidence_report.editorial_risk in {
                    EditorialRisk.HIGH,
                    EditorialRisk.SEVERE,
                }:
                    raise PublicationBlockedError(evidence_report.author_message)
                readiness = {
                    EditorialConfidence.READY: PackageReadiness.READY_FOR_HERO_VISUAL,
                    EditorialConfidence.READY_WITH_REVIEW: (
                        PackageReadiness.REVIEW_BEFORE_HERO_VISUAL
                    ),
                }.get(evidence_report.editorial_confidence)
                if readiness is None:
                    raise PublicationBlockedError(
                        "Editorial Confidence does not permit package assembly."
                    )
                package = PublicationPackage(
                    article_markdown=draft.article_markdown,
                    hero_visual_prompt=draft.hero_visual_prompt,
                    headline=draft.headline,
                    hook=draft.hook,
                    insights=draft.insights,
                    practical_takeaway=draft.practical_takeaway,
                    cta=draft.cta,
                    source_and_attribution=tuple(
                        item.citation for item in draft.source_attributions
                    ),
                    hashtags=draft.hashtags,
                    linkedin_description=draft.linkedin_description,
                    editorial_confidence=evidence_report.editorial_confidence,
                    editorial_risk=evidence_report.editorial_risk,
                    readiness=readiness,
                    review_findings=evidence_report.significant_findings,
                )
                if not package.insights or any(
                    not value.strip() for value in package.required_text_components()
                ):
                    raise ValueError(
                        "Publication Packages require every textual component."
                    )
                return package
        '''
    ),
    "tests/test_capability009_article_engine.py": clean(
        r'''
        """Behavioural tests for Capability 009's narrow runtime scope."""

        from datetime import date
        import unittest

        from studio.article_engine import (
            ArticleDraft,
            ArticleEngine,
            ArticleEngineError,
            ArticleRequest,
            PublicationBlockedError,
            SourceAttribution,
        )
        from studio.evidence_validation import (
            Claim,
            ClaimClassification,
            EditorialConfidence,
            EditorialRisk,
            EvidencePosition,
            EvidenceRecord,
            validate_evidence,
        )
        from studio.publication_package import (
            PackageReadiness,
            PublicationPackageBuilder,
        )


        def report(*, supports=2, material=True, contradiction=False):
            claim = Claim(
                identifier="claim-1",
                text="Structured review reduced avoidable rework.",
                classification=ClaimClassification.SOURCE_ASSERTION,
                material=material,
            )
            records = [
                EvidenceRecord(
                    source_identifier=f"source-{number}",
                    claim_identifier="claim-1",
                    position=EvidencePosition.SUPPORTS,
                    independent_group=f"group-{number}",
                    published_on=date(2026, 7, 1),
                )
                for number in range(1, supports + 1)
            ]
            if contradiction:
                records.append(
                    EvidenceRecord(
                        source_identifier="contradiction",
                        claim_identifier="claim-1",
                        position=EvidencePosition.CONTRADICTS,
                        independent_group="contradiction",
                    )
                )
            return validate_evidence(
                (claim,), records, current_on=date(2026, 8, 1)
            )


        def request(*, sources=("source-1", "source-2")):
            return ArticleRequest(
                intent_identifier="intent-1",
                editorial_intent="Explain why evidence-led review improves decisions.",
                thesis="Evidence-Led Review Strengthens Editorial Decisions",
                author_perspective=(
                    "In my experience, disciplined review protects both speed and trust."
                ),
                audience="Senior professional leaders",
                insights=(
                    "Evidence exposes assumptions before they become polished claims.",
                    "Clear editorial gates preserve confidence without replacing judgement.",
                ),
                practical_takeaway="Make material claims pass an explicit evidence gate.",
                cta_question="Where would stronger evidence review improve your decisions?",
                hero_visual_prompt="A restrained editorial evidence checkpoint.",
                hashtags=("#EditorialIntegrity", "#Leadership"),
                linkedin_description="A practical case for evidence-led editorial review.",
                source_attributions=tuple(
                    SourceAttribution(item, f"{item} — reviewed evidence")
                    for item in sources
                ),
            )


        class ArticleRequestTests(unittest.TestCase):
            def test_request_requires_one_or_two_insights(self):
                values = request().__dict__ | {"insights": ()}
                with self.assertRaisesRegex(ArticleEngineError, "one or two"):
                    ArticleRequest(**values)

            def test_cta_requires_article_specific_question(self):
                values = request().__dict__ | {"cta_question": "Share your view."}
                with self.assertRaisesRegex(ArticleEngineError, "question"):
                    ArticleRequest(**values)

            def test_source_identifiers_must_be_unique(self):
                with self.assertRaisesRegex(ArticleEngineError, "unique"):
                    request(sources=("Source", " source "))

            def test_source_and_attribution_is_required(self):
                with self.assertRaisesRegex(ArticleEngineError, "source and attribution"):
                    request(sources=())


        class ArticleEngineTests(unittest.TestCase):
            def test_low_risk_builds_original_structured_article(self):
                draft = ArticleEngine().create_article(request(), report())
                self.assertEqual(draft.intent_identifier, "intent-1")
                self.assertIn("# Evidence-Led Review", draft.article_markdown)
                self.assertIn("## Sources and Attribution", draft.article_markdown)
                self.assertNotIn("source material excerpt", draft.article_markdown)

            def test_high_risk_blocks_provider_before_generation(self):
                class NeverCalled:
                    def create_draft(self, request, evidence_report):
                        raise AssertionError("provider must not be called")

                with self.assertRaises(PublicationBlockedError):
                    ArticleEngine(NeverCalled()).create_article(request(), report(supports=0))

            def test_severe_contradiction_blocks_generation(self):
                with self.assertRaises(PublicationBlockedError):
                    ArticleEngine().create_article(
                        request(sources=("source-1", "source-2", "contradiction")),
                        report(contradiction=True),
                    )

            def test_provider_cannot_change_approved_intent(self):
                class ChangedIntent:
                    def create_draft(self, request, evidence_report):
                        base = ArticleEngine().provider.create_draft(
                            request, evidence_report
                        )
                        return ArticleDraft(
                            **(base.__dict__ | {"intent_identifier": "different"})
                        )

                with self.assertRaisesRegex(ArticleEngineError, "Editorial Intent"):
                    ArticleEngine(ChangedIntent()).create_article(request(), report())

            def test_every_used_evidence_source_requires_attribution(self):
                with self.assertRaisesRegex(ArticleEngineError, "requires attribution"):
                    ArticleEngine().create_article(
                        request(sources=("source-1",)), report()
                    )

            def test_provider_must_identify_validated_claims_used(self):
                class OmitsClaims:
                    def create_draft(self, request, evidence_report):
                        base = ArticleEngine().provider.create_draft(
                            request, evidence_report
                        )
                        return ArticleDraft(
                            **(base.__dict__ | {"used_claim_identifiers": ()})
                        )

                with self.assertRaisesRegex(ArticleEngineError, "validated claims"):
                    ArticleEngine(OmitsClaims()).create_article(request(), report())


        class PublicationPackageTests(unittest.TestCase):
            def test_package_contains_every_capability009_component(self):
                evidence = report()
                draft = ArticleEngine().create_article(request(), evidence)
                package = PublicationPackageBuilder().build(draft, evidence)
                self.assertIs(
                    package.readiness, PackageReadiness.READY_FOR_HERO_VISUAL
                )
                self.assertTrue(all(package.required_text_components()))
                self.assertIs(package.editorial_confidence, EditorialConfidence.READY)

            def test_moderate_risk_requires_review_before_hero_visual(self):
                evidence = report(supports=1, material=False)
                draft = ArticleEngine().create_article(
                    request(sources=("source-1",)), evidence
                )
                package = PublicationPackageBuilder().build(draft, evidence)
                self.assertIs(package.editorial_risk, EditorialRisk.MODERATE)
                self.assertIs(
                    package.readiness,
                    PackageReadiness.REVIEW_BEFORE_HERO_VISUAL,
                )
                self.assertTrue(package.review_findings)

            def test_later_capability_outputs_are_explicitly_deferred(self):
                evidence = report()
                draft = ArticleEngine().create_article(request(), evidence)
                package = PublicationPackageBuilder().build(draft, evidence)
                self.assertIsNone(package.rendered_hero_visual)
                self.assertIsNone(package.portable_editorial_project)
                self.assertFalse(package.version_one_complete)
                self.assertEqual(
                    package.deferred_components,
                    (
                        "Rendered Hero Visual - Capability 010",
                        "Portable Editorial Project - Capability 011",
                    ),
                )

            def test_blocked_report_cannot_assemble_package(self):
                evidence = report(supports=0)
                draft = ArticleDraft(
                    intent_identifier="intent-1",
                    headline="Headline",
                    hook="Hook",
                    insights=("Insight",),
                    practical_takeaway="Takeaway",
                    cta="Question? Conversation invitation.",
                    source_attributions=(),
                    hashtags=("#Tag",),
                    linkedin_description="Description",
                    hero_visual_prompt="Prompt",
                    article_markdown="# Article",
                    used_claim_identifiers=(),
                )
                with self.assertRaises(PublicationBlockedError):
                    PublicationPackageBuilder().build(draft, evidence)


        if __name__ == "__main__":
            unittest.main()
        '''
    ),
    "tests/test_capability009_documentation.py": clean(
        r'''
        """Documentation and boundary tests for Capability 009."""

        import unittest
        from pathlib import Path


        ROOT = Path(__file__).resolve().parents[1]


        class Capability009DocumentationTests(unittest.TestCase):
            def content(self, relative):
                return (ROOT / relative).read_text(encoding="utf-8")

            def test_adr_and_baseline_record_narrow_scope(self):
                adr = self.content(
                    "docs/architecture/adr/ADR-015-article-engine-publication-package.md"
                )
                baseline = self.content(
                    "docs/architecture/baselines/Architecture_Baseline_2026.08.02v10.md"
                )
                adr = " ".join(adr.split())
                baseline = " ".join(baseline.split())
                for value in ("Article Engine", "Publication Package", "Capability 010", "Capability 011"):
                    self.assertIn(value, adr)
                    self.assertIn(value, baseline)

            def test_scope_conflict_is_resolved_in_authorities(self):
                for relative in (
                    "ROADMAP.md",
                    "docs/product/Current_Product_Focus.md",
                    "docs/product/PRD_v1.3.md",
                    "docs/programs/Capability_008A_Master_Roadmap.md",
                ):
                    content = self.content(relative)
                    self.assertIn("Capability 009 Scope Clarification", content)
                    self.assertIn("Article Engine", content)
                    self.assertIn("Publication Package", content)
                    self.assertIn("Integrated Editorial Workspace", content)

            def test_scorecard_and_contract_do_not_claim_later_outputs(self):
                scorecard = self.content("docs/VERSION_ONE_SCORECARD.md")
                contract = self.content(
                    "docs/architecture/Publication_Package_Contract.md"
                )
                self.assertIn("Textual Publication Package", scorecard)
                self.assertIn("rendered Hero Visual", contract)
                self.assertIn("Capability 010", contract)
                self.assertIn("Capability 011", contract)

            def test_demo_and_definition_of_done_exist(self):
                self.assertTrue(
                    (ROOT / "docs/demos/Capability-009-Article-Engine-and-Publication-Package.md").is_file()
                )
                done = self.content("docs/architecture/Definition_of_Done.md")
                self.assertIn("Capability 009 Completion Additions", done)
                self.assertIn("no new Author-facing workflow", done)

            def test_brand_masters_remain_the_approved_baseline(self):
                master = self.content("assets/brand/logo/master/README.md")
                self.assertIn(
                    "b2cd1c22239b7176b43578892b0c37ac502ca5ab696b7c083a0b397bfe285727",
                    master,
                )
                self.assertIn(
                    "ae56f16f3e4b3a2bfbf5cefbf6ee807482cd8814e30b7496a917b9eae3a5ba72",
                    master,
                )


        if __name__ == "__main__":
            unittest.main()
        '''
    ),
    "docs/architecture/Article_Engine_and_Publication_Package.md": clean(
        r'''
        # Article Engine and Publication Package

        ## Status

        Capability 009 executable architecture.

        ## Responsibilities

        The Article Engine consumes explicit Author-owned editorial inputs and
        the completed Evidence Validation report. It preserves the approved
        Editorial Intent, refuses High or Severe Editorial Risk, requires
        attribution for evidence used, and delegates language construction
        through a provider-independent interface.

        The Publication Package builder assembles and validates the textual
        package: Hero Visual prompt, headline, hook, one or two insights,
        practical takeaway, CTA, source and attribution, hashtags, LinkedIn
        Description, article Markdown, and the existing Editorial Confidence
        and Editorial Risk result.

        ## Boundaries

        Capability 009 does not add an Integrated Editorial Workspace,
        Adaptive Editorial Context runtime, Component Collaboration, stable
        Author-facing orchestration API, or final integrated Editorial
        Confidence presentation.

        A rendered Hero Visual remains Capability 010. Portable Editorial
        Project serialization and export remain Capability 011. The runtime
        represents both as deferred and never reports the complete Version 1.0
        package while they are absent.

        ## Provider Independence

        `ArticleDraftProvider` is the only article-language provider boundary.
        The repository includes a deterministic provider that structures
        approved Author material without network access or source imitation.
        Future providers must obey the same intent, evidence, attribution, and
        publication-gate validations.

        ## Dependencies

        Capability 009 depends only on the existing Evidence Validation report
        and canonical editorial vocabulary. It introduces no persistence,
        ingestion, UI, Hero Visual generation, Portable Project, collaboration,
        or orchestration dependency.
        '''
    ),
    "docs/architecture/adr/ADR-015-article-engine-publication-package.md": clean(
        r'''
        # ADR-015 - Article Engine and Publication Package

        ## Status

        Accepted

        ## Date

        2026-08-02

        ## Decision Level

        D4 - Architecture

        ## Context

        Capabilities 007 and 008 can interpret input, preserve Editorial Intent,
        validate evidence, and determine Editorial Risk, but the repository has
        no executable Article Engine or textual Publication Package assembly.
        Earlier planning also assigned broader integrated product surfaces to
        Capability 009, conflicting with issue #15, ROADMAP, and the Version 1
        Scorecard.

        ## Decision

        Capability 009 implements only the Article Engine and Publication
        Package. The Article Engine uses a provider-independent draft boundary,
        preserves approved Editorial Intent and insights, requires attribution
        for used evidence, and fails closed when Editorial Risk is High or
        Severe.

        The Publication Package validates the Capability 009 textual components
        and carries the existing Editorial Confidence and LMHS Editorial Risk.
        It explicitly records rendered Hero Visual and Portable Editorial
        Project outputs as deferred and does not claim the full Version 1.0
        package is complete.

        ## Explicit Deferrals

        Integrated Editorial Workspace, Adaptive Editorial Context runtime,
        Component Collaboration, a stable Author-facing orchestration API, and
        final integrated Editorial Confidence presentation are not independent
        Capability 009 scope. Rendered Hero Visual generation remains Capability
        010. Portable Editorial Project behavior remains Capability 011.

        ## Constitutional Impact

        This decision implements Author ownership, Understanding Before
        Generation, Evidence Before Assertion, Confidence Before Publication,
        Professional Judgement, and approved-work protection. It changes no
        frozen constitutional principle or canonical term.

        ## Alternatives Considered

        ### Implement the broader integrated workflow

        Rejected because it combines several product surfaces, creates new
        Author-facing behavior, and absorbs later capability scope.

        ### Generate before Editorial Integrity completes

        Rejected because unsupported claims could become polished publication
        content before evidence and risk gates run.

        ### Couple runtime to one model provider

        Rejected because editorial invariants must remain deterministic and
        provider-independent.

        ## Consequences

        Capability 009 produces an evidence-aligned textual article package
        ready for later Hero Visual work. The complete Version 1.0 package
        remains intentionally incomplete until Capabilities 010 and 011.

        ## Architecture Baseline

        Recorded by Architecture Baseline `2026.08.02v10`.
        '''
    ),
    "docs/architecture/baselines/Architecture_Baseline_2026.08.02v10.md": clean(
        r'''
        # Architecture Baseline - 2026.08.02v10

        ## Status

        Current Capability 009 product-runtime baseline when delivered.

        ## Baseline ID

        `2026.08.02v10`

        ## Supersedes

        `2026.08.01v09`

        ## Reason for Revision

        Implement the Article Engine and textual Publication Package under
        ADR-015 without absorbing Capability 010, Capability 011, or broader
        integration work.

        ## Runtime Architecture

        `studio.article_engine` owns approved article inputs, the provider
        boundary, evidence-attribution validation, Editorial Intent preservation,
        and High/Severe publication blocking.

        `studio.publication_package` owns the validated textual package and
        explicit later-capability placeholders. Package readiness distinguishes
        Ready for Hero Visual from Review before Hero Visual and never claims
        Version 1.0 completion while deferred outputs are absent.

        ## Integrity Boundary

        The runtime consumes the existing `EvidenceValidationReport`. It does
        not perform ingestion, research, claim classification, corroboration, or
        risk reassessment. A provider cannot override the report, invent claim
        identifiers, change approved intent, or omit attribution for evidence
        used.

        ## Deferred Architecture

        Integrated Editorial Workspace, Adaptive Editorial Context runtime,
        Component Collaboration, stable Author-facing orchestration API, and
        final integrated Editorial Confidence presentation remain deferred.
        Rendered Hero Visual behavior remains Capability 010. Portable Editorial
        Project behavior remains Capability 011.

        ## Generated Ownership

        `scripts/bootstrap_capability009_article_engine_publication_package.py`
        owns the Capability 009 runtime, tests, ADR, baseline, demo, architecture
        contract, and managed documentation sections.

        ## Constitutional Impact

        No frozen principle or canonical vocabulary changes. The implementation
        applies existing Author ownership, evidence, attribution, risk, and
        approved-work protections.
        '''
    ),
    "docs/demos/Capability-009-Article-Engine-and-Publication-Package.md": clean(
        r'''
        # Capability 009 Demo - Article Engine and Publication Package

        ## Problem

        The Studio could validate evidence and editorial risk but could not
        construct an evidence-aligned article or assemble its textual package.

        ## What Changed

        A provider-independent Article Engine now preserves approved Editorial
        Intent, uses attributable evidence, blocks High and Severe risk, and
        constructs a structured professional article. The Publication Package
        builder validates every Capability 009 textual component.

        ## Example

        ```text
        Approved Author inputs + Evidence Validation report
                              |
                              v
                    High or Severe risk? -- yes --> stop
                              |
                             no
                              v
                 provider-independent Article Engine
                              |
                              v
                   validated textual package
                              |
                    +---------+---------+
                    |                   |
             Capability 010       Capability 011
             rendered visual      portable project
        ```

        ## Author Benefit

        The Author receives a coherent article grounded in approved intent and
        evidence without the Studio inventing sources, silently changing
        approved insights, or pretending later deliverables exist.

        ## Acceptance Evidence

        Tests cover input validity, intent preservation, source attribution,
        provider independence, Low/Moderate readiness, High/Severe blocking,
        complete textual components, and explicit Capability 010/011 deferral.

        ## Learning

        Publication readiness and Version 1.0 package completeness are different
        facts. Modeling deferred deliverables explicitly prevents partial product
        state from being presented as finished.

        ## Next

        Capability 010 may consume the approved Hero Visual prompt to create the
        rendered 720 × 425 Hero Visual. Capability 011 remains separate.
        '''
    ),
}

# CAPABILITY_010_HERO_VISUAL_OWNER_SYNC_START
from bootstrap_capability010_hero_visual_system import (
    PUBLICATION_PACKAGE as _capability010_publication_package,
)

FILES["studio/publication_package.py"] = _capability010_publication_package
# CAPABILITY_010_HERO_VISUAL_OWNER_SYNC_END

MANAGED = {
    "docs/architecture/adr/README.md": (
        "CAPABILITY_009_ADR_INDEX",
        clean(
            '''
            ## Capability 009 Decision

            - [ADR-015 - Article Engine and Publication Package](ADR-015-article-engine-publication-package.md)
            '''
        ),
    ),
    "docs/architecture/Publication_Package_Contract.md": (
        "CAPABILITY_009_PUBLICATION_PACKAGE_CONTRACT",
        clean(
            '''
            ## Capability 009 Implementation Boundary

            Capability 009 implements the Article Engine and the textual
            Publication Package: Hero Visual prompt, headline, hook, one or two
            insights, practical takeaway, CTA, source and attribution, hashtags,
            LinkedIn Description, article Markdown, Editorial Confidence, and
            LMHS Editorial Risk.

            A rendered Hero Visual remains Capability 010. Portable Editorial
            Project serialization remains Capability 011. The Capability 009
            runtime records both as deferred and must not report the complete
            Version 1.0 package while they are absent.
            '''
        ),
    ),
    "ROADMAP.md": (
        "CAPABILITY_009_ROADMAP",
        clean(
            '''
            ## Capability 009 Scope Clarification

            Status: **In Progress**

            Approved scope:

            - [x] Article Engine runtime
            - [x] Textual Publication Package assembly
            - [x] Evidence and attribution gate
            - [x] Editorial Intent preservation
            - [x] High and Severe publication blocking
            - [x] Explicit Capability 010 and Capability 011 deferral

            Integrated Editorial Workspace, Adaptive Editorial Context runtime,
            Component Collaboration, stable Author-facing orchestration API, and
            final integrated Editorial Confidence presentation are not independent
            Capability 009 scope.

            Capability 010 and Capability 011 remain Todo and unstarted. B002
            remains Todo, Low Priority, Post-RC1, and non-blocking.
            '''
        ),
    ),
    "docs/product/Current_Product_Focus.md": (
        "CAPABILITY_009_CURRENT_FOCUS",
        clean(
            '''
            ## Capability 009 Scope Clarification

            Capability 009 is the active product capability and implements only
            the Article Engine and textual Publication Package.

            The Article Engine consumes explicit Author-owned inputs and completed
            Editorial Integrity results. The package includes the article and its
            required textual publication components while preserving Editorial
            Confidence and publication blocking.

            Integrated Editorial Workspace, Adaptive Editorial Context runtime,
            Component Collaboration, stable Author-facing orchestration API, and
            final integrated Editorial Confidence presentation remain deferred.
            Rendered Hero Visual remains Capability 010. Portable Editorial Project
            behavior remains Capability 011.
            '''
        ),
    ),
    "docs/product/PRD_v1.3.md": (
        "CAPABILITY_009_PRD",
        clean(
            '''
            ## Capability 009 Scope Clarification

            Version 1.0 shall provide an Article Engine that:

            - preserves approved Editorial Intent and Author perspective;
            - consumes completed Evidence Validation rather than bypassing it;
            - requires attribution for evidence used;
            - blocks generation when Editorial Risk is High or Severe; and
            - uses a provider-independent draft boundary.

            Capability 009 shall assemble the textual Publication Package with a
            Hero Visual prompt, headline, hook, one or two insights, practical
            takeaway, CTA, source and attribution, hashtags, LinkedIn Description,
            article Markdown, Editorial Confidence, and LMHS Editorial Risk.

            Integrated Editorial Workspace, Adaptive Editorial Context runtime,
            Component Collaboration, stable Author-facing orchestration API, and
            final integrated Editorial Confidence presentation are deferred.
            Rendered Hero Visual remains Capability 010 and Portable Editorial
            Project behavior remains Capability 011.
            '''
        ),
    ),
    "docs/VERSION_ONE_SCORECARD.md": (
        "CAPABILITY_009_SCORECARD",
        clean(
            '''
            ## Capability 009 Progress

            | Area | Status | Evidence |
            |---|---|---|
            | Article Engine | Complete locally | `studio/article_engine.py` |
            | Textual Publication Package | Complete locally | `studio/publication_package.py` |
            | Evidence and attribution gate | Complete locally | Behavioral tests |
            | Editorial Intent preservation | Complete locally | Provider-boundary tests |
            | High and Severe blocking | Complete locally | Risk-gate tests |
            | Rendered Hero Visual | Planned | Capability 010 |
            | Portable Editorial Project | Planned | Capability 011 |

            The complete Version 1.0 Publication Package remains pending until
            Capabilities 010 and 011 deliver their assigned outputs.
            '''
        ),
    ),
    "docs/architecture/Definition_of_Done.md": (
        "CAPABILITY_009_DEFINITION_OF_DONE",
        clean(
            '''
            ## Capability 009 Completion Additions

            Confirm:

            - Article generation preserves approved Editorial Intent;
            - evidence used by the article has explicit attribution;
            - High and Severe Editorial Risk block article and package creation;
            - the provider boundary cannot bypass deterministic integrity checks;
            - every Capability 009 textual component is validated;
            - rendered Hero Visual and Portable Editorial Project outputs remain
              explicitly deferred;
            - no new Author-facing workflow, collaboration feature, orchestration
              API, persistence model, or later-capability behavior is introduced;
            - the Capability 009 demo is current; and
            - complete repository validation passes.
            '''
        ),
    ),
    "docs/product/Decision_Log.md": (
        "CAPABILITY_009_DECISION_LOG",
        clean(
            '''
            ## Capability 009 Decisions

            | Date | Level | Decision | Rationale |
            |---|---:|---|---|
            | 2026-08-02 | D4 | Limit Capability 009 to Article Engine and Publication Package | Issue #15, ROADMAP, scorecard, and Project planning define one coherent capability. |
            | 2026-08-02 | D4 | Require a provider-independent draft boundary | Editorial invariants must not depend on one generation provider. |
            | 2026-08-02 | D4 | Apply Evidence Validation before generation | High and Severe risk must not become polished publication content. |
            | 2026-08-02 | D4 | Represent Capability 010 and 011 outputs as deferred | Partial product state must not be presented as the complete Version 1.0 package. |

            ADR-015 and Architecture Baseline `2026.08.02v10` record the durable
            architecture.
            '''
        ),
    ),
    "docs/programs/Capability_008A_Master_Roadmap.md": (
        "CAPABILITY_009_SCOPE_CLARIFICATION",
        clean(
            '''
            ## Capability 009 Scope Clarification

            The Repository Author resolved the post-008A Capability 009 scope in
            favor of issue #15, ROADMAP, the Version 1 Scorecard, the Capability
            008 demo, and the GitHub Project summary.

            Capability 009 implements only the Article Engine and Publication
            Package. Integrated Editorial Workspace, Adaptive Editorial Context
            runtime, Component Collaboration, stable Author-facing orchestration
            API, and final integrated Editorial Confidence presentation remain
            deferred and may appear only as minimal internal support strictly
            necessary for the approved scope. They must not create new product
            surface or independent runtime subsystems.
            '''
        ),
    ),
    "README.md": (
        "CAPABILITY_009_README",
        clean(
            '''
            ## Capability 009 - Article Engine and Publication Package

            The executable Article Engine now converts approved Author inputs and
            completed Evidence Validation into an evidence-aligned professional
            article. A provider-independent boundary preserves Editorial Intent,
            attribution, and publication gates.

            The Capability 009 Publication Package contains the article and its
            textual publication components. Rendered Hero Visual generation remains
            Capability 010, and Portable Editorial Project behavior remains
            Capability 011.
            '''
        ),
    ),
    "CHANGELOG.md": (
        "CAPABILITY_009_CHANGELOG",
        clean(
            '''
            ### Added - Capability 009

            - Provider-independent Article Engine
            - Evidence and attribution validation before generation
            - Editorial Intent preservation
            - High and Severe publication blocking
            - Textual Publication Package assembly
            - Explicit Capability 010 and Capability 011 deferrals
            - ADR-015 and Architecture Baseline 2026.08.02v10
            - Capability 009 behavioral, documentation, and demo coverage
            '''
        ),
    ),
}


def run(command: list[str], *, cwd: Path, capture: bool = False) -> str:
    """Run one checked command."""
    result = subprocess.run(
        command,
        cwd=cwd,
        check=False,
        text=True,
        capture_output=capture,
    )
    if result.returncode:
        detail = (result.stderr or result.stdout or "command failed").strip()
        raise CapabilityError(f"{' '.join(command)}: {detail}")
    return result.stdout if capture else ""


def repository_root() -> Path:
    """Resolve and verify the repository root."""
    root = Path(__file__).resolve().parents[1]
    if root.name != EXPECTED_REPOSITORY or not (root / ".git").exists():
        raise CapabilityError("Run this bootstrap from the expected repository.")
    return root


def verify_branch(root: Path) -> None:
    branch = run(["git", "branch", "--show-current"], cwd=root, capture=True).strip()
    if branch != EXPECTED_BRANCH:
        raise CapabilityError(f"Expected branch {EXPECTED_BRANCH}; found {branch}.")


def changed_paths(root: Path) -> set[str]:
    output = run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=root,
        capture=True,
    )
    paths: set[str] = set()
    for line in output.splitlines():
        if not line:
            continue
        value = line[3:]
        if " -> " in value:
            value = value.split(" -> ", 1)[1]
        paths.add(value.strip('"'))
    return paths


def verify_worktree(root: Path) -> None:
    allowed = {SCRIPT_PATH, *FILES, *MANAGED}
    unexpected = changed_paths(root) - allowed
    if unexpected:
        raise CapabilityError(
            "Unexpected working-tree paths: " + ", ".join(sorted(unexpected))
        )


def managed_text(original: str, marker: str, body: str) -> str:
    start = f"<!-- {marker}_START -->"
    end = f"<!-- {marker}_END -->"
    block = f"{start}\n\n{body.rstrip()}\n\n{end}"
    if start in original and end in original:
        prefix, rest = original.split(start, 1)
        _, suffix = rest.split(end, 1)
        return prefix.rstrip() + "\n\n" + block + suffix
    return original.rstrip() + "\n\n" + block + "\n"


def apply(root: Path) -> None:
    for relative, content in FILES.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    for relative, (marker, body) in MANAGED.items():
        path = root / relative
        original = path.read_text(encoding="utf-8")
        path.write_text(managed_text(original, marker, body), encoding="utf-8")


def validate_generated(root: Path) -> None:
    for relative, content in FILES.items():
        path = root / relative
        if not path.is_file() or path.read_text(encoding="utf-8") != content:
            raise CapabilityError(f"Generated file differs from bootstrap: {relative}")
    for relative, (marker, body) in MANAGED.items():
        content = (root / relative).read_text(encoding="utf-8")
        if content.count(f"<!-- {marker}_START -->") != 1:
            raise CapabilityError(f"Managed start marker invalid: {relative}")
        if content.count(f"<!-- {marker}_END -->") != 1:
            raise CapabilityError(f"Managed end marker invalid: {relative}")
        if body.rstrip() not in content:
            raise CapabilityError(f"Managed content differs: {relative}")
    forbidden = (
        "studio/adaptive_editorial_context.py",
        "studio/component_collaboration.py",
        "studio/editorial_orchestrator.py",
        "studio/hero_visual.py",
        "studio/portable_editorial_project.py",
    )
    if any((root / relative).exists() for relative in forbidden):
        raise CapabilityError("A deferred runtime subsystem was introduced.")
    mark = run(
        ["shasum", "-a", "256", "assets/brand/logo/master/editorial-compass-mark-master.png"],
        cwd=root,
        capture=True,
    ).split()[0]
    lockup = run(
        ["shasum", "-a", "256", "assets/brand/logo/master/editorial-compass-lockup-master.png"],
        cwd=root,
        capture=True,
    ).split()[0]
    if mark != "b2cd1c22239b7176b43578892b0c37ac502ca5ab696b7c083a0b397bfe285727":
        raise CapabilityError("Approved brand mark master changed.")
    if lockup != "ae56f16f3e4b3a2bfbf5cefbf6ee807482cd8814e30b7496a917b9eae3a5ba72":
        raise CapabilityError("Approved brand lockup master changed.")


def validate_repository(root: Path) -> None:
    run([sys.executable, "-m", "compileall", "-q", "studio", "scripts", "tests"], cwd=root)
    run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=root)
    run([sys.executable, "studio.py", "validate"], cwd=root)
    run(["git", "diff", "--check"], cwd=root)


def preview() -> None:
    print("Capability 009 preview - no files will be changed.\n")
    print("Approved scope:")
    print("- Article Engine")
    print("- Textual Publication Package")
    print("\nExplicitly deferred:")
    print("- Integrated Editorial Workspace and Adaptive Context runtime")
    print("- Component Collaboration and orchestration API")
    print("- final integrated Editorial Confidence presentation")
    print("- Capability 010 rendered Hero Visual")
    print("- Capability 011 Portable Editorial Project")
    print("\nGenerated files:")
    for relative in FILES:
        print(f"- {relative}")
    print("\nManaged documents:")
    for relative in MANAGED:
        print(f"- {relative}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = repository_root()
    verify_branch(root)
    verify_worktree(root)
    if not args.apply:
        preview()
        return 0
    apply(root)
    verify_worktree(root)
    validate_generated(root)
    validate_repository(root)
    print(SENTINEL)
    run(["git", "status", "--short"], cwd=root)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CapabilityError as exc:
        print(f"Capability 009 bootstrap stopped: {exc}", file=sys.stderr)
        raise SystemExit(1)
