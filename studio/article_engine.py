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
