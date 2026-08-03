"""Portable Editorial Project resume and export runtime for Capability 011.

The RC1 schema deliberately contains only values supplied by the current
Publication Package and Editorial Session runtimes. It is human-readable,
offline, deterministic, and strict at the trust boundary.
"""

from __future__ import annotations

import hashlib
import io
import json
import re
import zipfile
from dataclasses import asdict, dataclass
from datetime import date
from enum import Enum
from typing import TYPE_CHECKING

from .editorial_discernment import EditorialSession

if TYPE_CHECKING:
    from .publication_package import PublicationPackage


SCHEMA_VERSION = 1
PRODUCT_NAME = "Ramrattan AI Editorial Studio"
PROJECT_PREFIX = "Ramrattan-Editorial-Project"
ARTICLE_PREFIX = "Ramrattan-Article"
HERO_PREFIX = "Ramrattan-Hero-Visual"
MAX_FILENAME_LENGTH = 255
_PROJECT_SUFFIX = ".md"
_VERSION_RE = re.compile(r"^\d{4}\.\d{2}\.\d{2}v\d{2}$")
_PROJECT_ID_RE = re.compile(r"^REP-[A-F0-9]{8}$")
_BLOCK_START = "```portable-editorial-project-json\n"
_BLOCK_END = "\n```"
_CONFIDENCE_VALUES = {
    "Ready for publication",
    "Ready with review",
    "Not ready - stronger evidence required",
    "Not ready - publication blocked",
}
_RISK_VALUES = {"Low", "Moderate", "High", "Severe"}
_READINESS_VALUES = {"ready_for_hero_visual", "review_before_hero_visual"}
_HERO_VALUES = {"pending", "ready", "failed", "blocked"}


class ProjectState(str, Enum):
    """Explicit project load and resume outcomes."""

    READY = "ready"
    STALE = "stale"
    MALFORMED = "malformed"
    UNSUPPORTED = "unsupported"
    INVALID = "invalid"
    BLOCKED = "blocked"


class PortableProjectError(ValueError):
    """Fail-closed Portable Editorial Project error."""

    def __init__(self, state: ProjectState, message: str) -> None:
        super().__init__(message)
        self.state = state


@dataclass(frozen=True)
class PortableEditorialProject:
    """Narrow RC1 project state available from current runtime objects."""

    schema_version: int
    product: str
    project_id: str
    title: str
    slug: str
    document_version: str
    previous_version: str | None
    saved_on: str
    article_markdown: str
    hero_visual_prompt: str
    hero_visual_status: str
    hero_visual_sha256: str | None
    editorial_confidence: str
    editorial_risk: str
    package_readiness: str
    review_findings: tuple[str, ...]
    integrity_blockers: tuple[str, ...]


@dataclass(frozen=True)
class ResumeResult:
    """Validated resume outcome with mandatory Temporal Integrity review."""

    state: ProjectState
    project: PortableEditorialProject
    temporal_integrity_review_required: bool
    findings: tuple[str, ...]


@dataclass(frozen=True)
class Download:
    """One downloadable offline artifact."""

    filename: str
    content: bytes
    media_type: str


def safe_slug(title: str) -> str:
    """Return a deterministic ASCII filename slug."""
    normalized = title.encode("ascii", "ignore").decode("ascii")
    normalized = re.sub(r"[^A-Za-z0-9]+", "-", normalized).strip("-")
    return normalized or "Untitled"


def _version(day: date, sequence: int) -> str:
    if not 1 <= sequence <= 99:
        raise PortableProjectError(
            ProjectState.BLOCKED,
            "The daily project sequence is exhausted; no file was overwritten.",
        )
    return f"{day:%Y.%m.%d}v{sequence:02d}"


def _bounded_slug(prefix: str, slug: str, version: str, suffix: str) -> str:
    fixed = len(prefix) + 1 + 1 + len(version) + len(suffix)
    available = MAX_FILENAME_LENGTH - fixed
    if available < 1:
        raise PortableProjectError(ProjectState.INVALID, "Filename contract is invalid.")
    if len(slug) <= available:
        return slug
    digest = hashlib.sha256(slug.encode("utf-8")).hexdigest()[:8].upper()
    word_space = available - len(digest) - 1
    if word_space < 1:
        raise PortableProjectError(ProjectState.INVALID, "Filename cannot be bounded safely.")
    return f"{slug[:word_space].rstrip('-')}-{digest}"


def versioned_filename(
    title: str,
    day: date,
    *,
    existing_names: tuple[str, ...] = (),
    prefix: str = PROJECT_PREFIX,
    suffix: str = _PROJECT_SUFFIX,
) -> tuple[str, str]:
    """Choose the first unused daily sequential VCM filename."""
    slug = safe_slug(title)
    occupied = set(existing_names)
    for sequence in range(1, 100):
        version = _version(day, sequence)
        bounded = _bounded_slug(prefix, slug, version, suffix)
        candidate = f"{prefix}_{bounded}_{version}{suffix}"
        if candidate not in occupied:
            return candidate, version
    raise PortableProjectError(
        ProjectState.BLOCKED,
        "The daily project sequence is exhausted; no file was overwritten.",
    )


def project_id_for(title: str, saved_on: date) -> str:
    """Create a stable deterministic identity from explicit creation inputs."""
    seed = f"{safe_slug(title)}|{saved_on.isoformat()}".encode("utf-8")
    return "REP-" + hashlib.sha256(seed).hexdigest()[:8].upper()


def from_publication_package(
    package: "PublicationPackage",
    *,
    saved_on: date,
    document_version: str,
    project_id: str | None = None,
    previous_version: str | None = None,
) -> PortableEditorialProject:
    """Capture only state reliably supplied by the current package runtime."""
    title = package.headline.strip()
    visual = package.rendered_hero_visual
    blockers = (
        tuple(package.review_findings)
        if not package.version_one_complete
        and package.editorial_risk.value in {"High", "Severe"}
        else ()
    )
    return PortableEditorialProject(
        schema_version=SCHEMA_VERSION,
        product=PRODUCT_NAME,
        project_id=project_id or project_id_for(title, saved_on),
        title=title,
        slug=safe_slug(title),
        document_version=document_version,
        previous_version=previous_version,
        saved_on=saved_on.isoformat(),
        article_markdown=package.article_markdown,
        hero_visual_prompt=package.hero_visual_prompt,
        hero_visual_status=package.hero_visual_state.value,
        hero_visual_sha256=(visual.artifact_sha256 if visual else None),
        editorial_confidence=package.editorial_confidence.value,
        editorial_risk=package.editorial_risk.value,
        package_readiness=package.readiness.value,
        review_findings=tuple(package.review_findings),
        integrity_blockers=blockers,
    )


def serialize_project(project: PortableEditorialProject) -> str:
    """Serialize one project as deterministic Markdown plus strict JSON."""
    _validate_project(project)
    payload = asdict(project)
    payload["review_findings"] = list(project.review_findings)
    payload["integrity_blockers"] = list(project.integrity_blockers)
    encoded = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
    return (
        f"# Portable Editorial Project — {project.title}\n\n"
        f"Project ID: `{project.project_id}`  \n"
        f"Document version: `{project.document_version}`  \n"
        f"Saved: `{project.saved_on}`\n\n"
        "The structured block below is the authoritative resumable state.\n\n"
        f"{_BLOCK_START}{encoded}{_BLOCK_END}\n\n"
        "## Article\n\n"
        f"{project.article_markdown.rstrip()}\n"
    )


def deserialize_project(markdown: str) -> PortableEditorialProject:
    """Validate and deserialize a narrow RC1 project, rejecting legacy bulk."""
    if not isinstance(markdown, str) or not markdown.strip():
        raise PortableProjectError(ProjectState.MALFORMED, "Project Markdown is empty.")
    start = markdown.find(_BLOCK_START)
    if start < 0:
        raise PortableProjectError(ProjectState.MALFORMED, "Project data block is missing.")
    payload_start = start + len(_BLOCK_START)
    end = markdown.find(_BLOCK_END, payload_start)
    if end < 0:
        raise PortableProjectError(ProjectState.MALFORMED, "Project data block is incomplete.")
    try:
        data = json.loads(markdown[payload_start:end])
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise PortableProjectError(ProjectState.MALFORMED, "Project data is not valid JSON.") from exc
    if not isinstance(data, dict):
        raise PortableProjectError(ProjectState.MALFORMED, "Project data must be an object.")
    fields = set(PortableEditorialProject.__dataclass_fields__)
    if set(data) != fields:
        extra = sorted(set(data) - fields)
        state = ProjectState.UNSUPPORTED if extra else ProjectState.INVALID
        raise PortableProjectError(state, "Project fields do not match the RC1 schema.")
    if data.get("schema_version") != SCHEMA_VERSION:
        raise PortableProjectError(ProjectState.UNSUPPORTED, "Project schema version is unsupported.")
    try:
        data["review_findings"] = tuple(data["review_findings"])
        data["integrity_blockers"] = tuple(data["integrity_blockers"])
        project = PortableEditorialProject(**data)
    except (TypeError, KeyError) as exc:
        raise PortableProjectError(ProjectState.INVALID, "Project field types are invalid.") from exc
    _validate_project(project)
    return project


def _validate_project(project: PortableEditorialProject) -> None:
    if project.schema_version != SCHEMA_VERSION or project.product != PRODUCT_NAME:
        raise PortableProjectError(ProjectState.UNSUPPORTED, "Project product or schema is unsupported.")
    strings = (project.title, project.slug, project.document_version, project.saved_on, project.article_markdown, project.hero_visual_prompt, project.hero_visual_status, project.editorial_confidence, project.editorial_risk, project.package_readiness)
    if any(not isinstance(value, str) or not value.strip() for value in strings):
        raise PortableProjectError(ProjectState.INVALID, "Required project fields are invalid.")
    if not _PROJECT_ID_RE.fullmatch(project.project_id):
        raise PortableProjectError(ProjectState.INVALID, "Project ID is invalid.")
    if project.slug != safe_slug(project.title) or not _VERSION_RE.fullmatch(project.document_version):
        raise PortableProjectError(ProjectState.INVALID, "Project slug or document version is invalid.")
    if project.previous_version is not None and (
        not isinstance(project.previous_version, str)
        or not _VERSION_RE.fullmatch(project.previous_version)
    ):
        raise PortableProjectError(ProjectState.INVALID, "Previous version is invalid.")
    if project.hero_visual_status not in _HERO_VALUES:
        raise PortableProjectError(ProjectState.INVALID, "Hero Visual status is invalid.")
    if project.editorial_confidence not in _CONFIDENCE_VALUES:
        raise PortableProjectError(ProjectState.INVALID, "Editorial Confidence is invalid.")
    if project.editorial_risk not in _RISK_VALUES:
        raise PortableProjectError(ProjectState.INVALID, "Editorial Risk is invalid.")
    if project.package_readiness not in _READINESS_VALUES:
        raise PortableProjectError(ProjectState.INVALID, "Package readiness is invalid.")
    if project.hero_visual_sha256 is not None and (
        not isinstance(project.hero_visual_sha256, str)
        or re.fullmatch(r"[a-f0-9]{64}", project.hero_visual_sha256) is None
    ):
        raise PortableProjectError(ProjectState.INVALID, "Hero Visual hash is invalid.")
    try:
        date.fromisoformat(project.saved_on)
    except ValueError as exc:
        raise PortableProjectError(ProjectState.INVALID, "Project saved date is invalid.") from exc
    if (
        not isinstance(project.review_findings, tuple)
        or not isinstance(project.integrity_blockers, tuple)
        or any(
            not isinstance(value, str) or not value.strip()
            for value in (*project.review_findings, *project.integrity_blockers)
        )
    ):
        raise PortableProjectError(ProjectState.INVALID, "Project findings are invalid.")


def resume_project(markdown: str, session: EditorialSession, *, current_on: date) -> ResumeResult:
    """Resume a validated project and require Temporal Integrity review."""
    project = deserialize_project(markdown)
    if project.integrity_blockers:
        raise PortableProjectError(ProjectState.BLOCKED, "Project has unresolved Editorial Integrity blockers.")
    saved = date.fromisoformat(project.saved_on)
    stale = saved < current_on
    session.resume()
    finding = "Temporal Integrity review required before publication."
    if stale:
        finding = f"Project saved on {project.saved_on} is stale; Temporal Integrity review required."
    session.preserved_events.append(finding)
    return ResumeResult(ProjectState.STALE if stale else ProjectState.READY, project, True, (finding,))


def project_download(project: PortableEditorialProject, *, existing_names: tuple[str, ...] = ()) -> Download:
    saved = date.fromisoformat(project.saved_on)
    filename, version = versioned_filename(project.title, saved, existing_names=existing_names)
    if version != project.document_version:
        project = PortableEditorialProject(**{**asdict(project), "document_version": version, "previous_version": project.document_version})
    return Download(filename, serialize_project(project).encode("utf-8"), "text/markdown")


def article_download(project: PortableEditorialProject) -> Download:
    slug = _bounded_slug(ARTICLE_PREFIX, project.slug, project.document_version, ".md")
    name = f"{ARTICLE_PREFIX}_{slug}_{project.document_version}.md"
    return Download(name, project.article_markdown.encode("utf-8"), "text/markdown")


def hero_visual_download(package: "PublicationPackage", project: PortableEditorialProject) -> Download:
    visual = package.rendered_hero_visual
    if visual is None or not visual.ready or visual.artifact is None:
        raise PortableProjectError(ProjectState.BLOCKED, "No validated Hero Visual is available for download.")
    slug = _bounded_slug(HERO_PREFIX, project.slug, project.document_version, ".png")
    name = f"{HERO_PREFIX}_{slug}_{project.document_version}.png"
    return Download(name, visual.artifact, "image/png")


def zip_export(project: PortableEditorialProject, package: "PublicationPackage", *, include_hero_visual: bool = True) -> Download:
    """Return a byte-identical ZIP for identical project and package inputs."""
    artifacts = [project_download(project), article_download(project)]
    if include_hero_visual and package.rendered_hero_visual is not None:
        artifacts.append(hero_visual_download(package, project))
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for artifact in sorted(artifacts, key=lambda item: item.filename):
            info = zipfile.ZipInfo(artifact.filename, (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o600 << 16
            archive.writestr(info, artifact.content)
    slug = _bounded_slug("Ramrattan-Editorial-Export", project.slug, project.document_version, ".zip")
    return Download(f"Ramrattan-Editorial-Export_{slug}_{project.document_version}.zip", buffer.getvalue(), "application/zip")
