"""Publication Package assembly and narrow attachment boundaries."""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum

from .article_engine import ArticleDraft, PublicationBlockedError
from .evidence_validation import (
    EditorialConfidence,
    EditorialRisk,
    EvidenceValidationReport,
)
from .hero_visual import HeroVisualResult, HeroVisualStatus
from .portable_editorial_project import PortableEditorialProject


class PackageReadiness(str, Enum):
    """Capability 009 textual package readiness."""

    READY_FOR_HERO_VISUAL = "ready_for_hero_visual"
    REVIEW_BEFORE_HERO_VISUAL = "review_before_hero_visual"


class HeroVisualPackageState(str, Enum):
    """Hero Visual state at the narrow Publication Package boundary."""

    PENDING = "pending"
    READY = "ready"
    FAILED = "failed"
    BLOCKED = "blocked"


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
    hero_visual_state: HeroVisualPackageState = HeroVisualPackageState.PENDING
    rendered_hero_visual: HeroVisualResult | None = None
    portable_editorial_project: PortableEditorialProject | None = None
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

    def attach_hero_visual(
        self,
        package: PublicationPackage,
        result: HeroVisualResult,
    ) -> PublicationPackage:
        """Attach one existing result without regenerating textual components."""
        if package.hero_visual_state is not HeroVisualPackageState.PENDING:
            raise ValueError("The Publication Package already has a Hero Visual result.")
        if result.prompt != package.hero_visual_prompt:
            raise ValueError("The Hero Visual result must preserve the approved prompt.")

        if result.ready:
            state = HeroVisualPackageState.READY
            deferred = tuple(
                item for item in package.deferred_components
                if item != "Rendered Hero Visual - Capability 010"
            )
        elif result.status is HeroVisualStatus.BLOCKED:
            state = HeroVisualPackageState.BLOCKED
            deferred = package.deferred_components
        else:
            state = HeroVisualPackageState.FAILED
            deferred = package.deferred_components

        return replace(
            package,
            hero_visual_state=state,
            rendered_hero_visual=result,
            deferred_components=deferred,
        )

    def attach_portable_editorial_project(
        self,
        package: PublicationPackage,
        project: PortableEditorialProject,
    ) -> PublicationPackage:
        """Attach one validated project without changing article or visual output."""
        if package.portable_editorial_project is not None:
            raise ValueError("The Publication Package already has a Portable Editorial Project.")
        if project.article_markdown != package.article_markdown:
            raise ValueError("The Portable Editorial Project must preserve the approved article.")
        if project.hero_visual_prompt != package.hero_visual_prompt:
            raise ValueError("The Portable Editorial Project must preserve the approved Hero Visual prompt.")
        deferred = tuple(
            item for item in package.deferred_components
            if item != "Portable Editorial Project - Capability 011"
        )
        return replace(
            package,
            portable_editorial_project=project,
            deferred_components=deferred,
            version_one_complete=not deferred,
        )
