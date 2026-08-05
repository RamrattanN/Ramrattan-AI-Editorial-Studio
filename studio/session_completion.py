"""Deterministic Session Completion and artifact delivery for V11-08."""

from __future__ import annotations

import json
from dataclasses import dataclass, replace
from datetime import date

from .evidence_validation import EditorialConfidence, EditorialRisk
from .portable_editorial_project import (
    Download,
    PortableEditorialProject,
    from_publication_package,
    project_download,
    versioned_filename,
)
from .publication_package import (
    HeroVisualPackageState,
    PackageReadiness,
    PublicationPackage,
    PublicationPackageBuilder,
)
from .publication_studio import PublicationStudio


CONFIGURATION_PREFIX = "Ramrattan-AI-Configuration"
CONFIGURATION_SUFFIX = ".json"


class SessionCompletionError(ValueError):
    """Raised when Session Artifacts cannot be produced safely."""

    def __init__(
        self,
        message: str,
        *,
        partial_artifacts: SessionArtifacts | None = None,
    ) -> None:
        super().__init__(message)
        self.partial_artifacts = partial_artifacts


@dataclass(frozen=True, slots=True)
class SessionArtifacts:
    """Artifacts delivered to the caller and never retained by the Studio."""

    publication_package: PublicationPackage
    portable_editorial_project: Download
    configuration: Download | None


def configuration_download(
    *,
    preferred_workflow: str,
    branding_preference: str,
    completed_on: date,
    existing_names: tuple[str, ...] = (),
) -> Download:
    """Serialize the exact two-field JSON Configuration contract."""
    if preferred_workflow not in {"guided", "express"}:
        raise SessionCompletionError(
            "Configuration generation requires a selected Workflow mode."
        )
    if not isinstance(branding_preference, str) or not branding_preference.strip():
        raise SessionCompletionError(
            "Configuration generation requires the Branding preference last used."
        )
    occupied = set(existing_names)
    filename = ""
    for sequence in range(1, 100):
        candidate = (
            f"{CONFIGURATION_PREFIX}-{completed_on:%Y.%m.%d}"
            f"v{sequence:02d}{CONFIGURATION_SUFFIX}"
        )
        if candidate not in occupied:
            filename = candidate
            break
    if not filename:
        raise SessionCompletionError(
            "The daily Configuration sequence is exhausted; no file was overwritten."
        )
    content = json.dumps(
        {
            "branding_preference": branding_preference,
            "preferred_workflow": preferred_workflow,
        },
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ) + "\n"
    return Download(filename, content.encode("utf-8"), "application/json")


def _live_publication_package(studio: PublicationStudio) -> PublicationPackage:
    content = studio.editor.current_content
    if studio.generated_package is not None:
        return replace(
            studio.generated_package,
            article_markdown=content.article,
            headline=content.headline,
            hook=content.hook,
            cta=content.cta,
            hashtags=content.hashtags,
            linkedin_description=content.linkedin_description or "",
            portable_editorial_project=None,
            deferred_components=("Portable Editorial Project - Capability 011",),
            version_one_complete=False,
        )

    project = studio.resumed_project
    if project is None:
        raise SessionCompletionError(
            "Session Completion requires Publication Studio content."
        )
    return PublicationPackage(
        article_markdown=content.article,
        hero_visual_prompt=project.hero_visual_prompt,
        headline=content.headline,
        hook=content.hook,
        insights=(content.hook,),
        practical_takeaway=content.cta,
        cta=content.cta,
        source_and_attribution=(),
        hashtags=content.hashtags,
        linkedin_description=content.linkedin_description or "",
        editorial_confidence=EditorialConfidence(project.editorial_confidence),
        editorial_risk=EditorialRisk(project.editorial_risk),
        readiness=PackageReadiness(project.package_readiness),
        review_findings=project.review_findings,
        hero_visual_state=HeroVisualPackageState(project.hero_visual_status),
        rendered_hero_visual=None,
        deferred_components=("Portable Editorial Project - Capability 011",),
    )


def build_session_artifacts(
    studio: PublicationStudio,
    *,
    completed_on: date,
    generate_configuration: bool,
    preferred_workflow: str | None,
    branding_preference: str | None,
    existing_project_names: tuple[str, ...] = (),
    existing_configuration_names: tuple[str, ...] = (),
) -> SessionArtifacts:
    """Build mandatory artifacts and the independently optional Configuration."""
    if not isinstance(studio, PublicationStudio):
        raise SessionCompletionError(
            "Session Completion requires an active Publication Studio."
        )
    if not isinstance(completed_on, date):
        raise SessionCompletionError("Session Completion requires a valid date.")

    try:
        package = _live_publication_package(studio)
        _, document_version = versioned_filename(
            package.headline,
            completed_on,
            existing_names=existing_project_names,
        )
        prior = studio.resumed_project
        project = from_publication_package(
            package,
            saved_on=completed_on,
            document_version=document_version,
            project_id=prior.project_id if prior is not None else None,
            previous_version=prior.document_version if prior is not None else None,
        )
        if prior is not None and package.rendered_hero_visual is None:
            project = replace(
                project,
                hero_visual_status=prior.hero_visual_status,
                hero_visual_sha256=prior.hero_visual_sha256,
            )
        package = PublicationPackageBuilder().attach_portable_editorial_project(
            package, project
        )
        portable = project_download(project, existing_names=existing_project_names)
    except Exception as exc:
        if isinstance(exc, SessionCompletionError):
            raise
        detail = str(exc).strip() or "mandatory artifact validation failed"
        raise SessionCompletionError(
            "Mandatory Session Artifacts could not be produced: " + detail
        ) from exc

    configuration = None
    if generate_configuration:
        try:
            configuration = configuration_download(
                preferred_workflow=preferred_workflow or "",
                branding_preference=branding_preference or "",
                completed_on=completed_on,
                existing_names=existing_configuration_names,
            )
        except SessionCompletionError as exc:
            raise SessionCompletionError(
                str(exc),
                partial_artifacts=SessionArtifacts(package, portable, None),
            ) from exc
    return SessionArtifacts(package, portable, configuration)
