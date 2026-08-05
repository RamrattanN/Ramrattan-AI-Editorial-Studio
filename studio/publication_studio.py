"""Publication Studio workspace and Author Editing boundary.

V11-05 owns the two-workspace layout, the Publication Editor, and the
Editorial Review panel. V11-06 completes the Copy LinkedIn Publication
gate's matched/unmatched enforcement, applying read-only Editorial Audit
results from `editorial_audit.py` without ever writing to Publication
Content.
"""

from __future__ import annotations

from dataclasses import dataclass, fields, replace
from enum import StrEnum
from typing import TYPE_CHECKING

from .evidence_validation import EditorialConfidence, EditorialRisk
from .hero_visual import HeroVisualResult
from .publication_package import PublicationPackage

if TYPE_CHECKING:
    from .editorial_audit import EditorialAuditResult


class PublicationStudioError(ValueError):
    """Raised when Publication Studio input or editing fails closed."""


class WorkspaceKind(StrEnum):
    """The two workspaces presented side by side."""

    HERO_VISUAL = "hero_visual"
    PUBLICATION_EDITOR = "publication_editor"


class HeroVisualAction(StrEnum):
    """Author-controlled actions available for the generated visual."""

    COPY = "copy"
    SAVE = "save"
    DOWNLOAD = "download"


class PublicationEditorAction(StrEnum):
    """The one and only Studio action in the Publication Editor."""

    COPY_LINKEDIN_PUBLICATION = "copy_linkedin_publication"


class CopyGateState(StrEnum):
    """Session-owned Editorial Audit Gate state, enforced by V11-06."""

    UNMATCHED = "unmatched"
    MATCHED = "matched"


@dataclass(frozen=True, slots=True)
class PublicationContent:
    """Only the content that belongs in the Author-owned editor."""

    headline: str
    hook: str
    article: str
    cta: str
    hashtags: tuple[str, ...] = ()
    linkedin_description: str | None = None

    def __post_init__(self) -> None:
        for name in ("headline", "hook", "article", "cta"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise PublicationStudioError(
                    f"Publication Content {name} must not be empty."
                )
        if not isinstance(self.hashtags, tuple) or not all(
            isinstance(item, str) and item.strip() for item in self.hashtags
        ):
            raise PublicationStudioError("Publication hashtags are not supported.")
        if self.linkedin_description is not None and (
            not isinstance(self.linkedin_description, str)
            or not self.linkedin_description.strip()
        ):
            raise PublicationStudioError(
                "LinkedIn Description must be omitted or contain text."
            )

    @classmethod
    def from_package(cls, package: PublicationPackage) -> PublicationContent:
        """Create editable content without changing the generated package."""
        return cls(
            headline=package.headline,
            hook=package.hook,
            article=package.article_markdown,
            cta=package.cta,
            hashtags=package.hashtags,
            linkedin_description=package.linkedin_description or None,
        )

    def rendered(self) -> str:
        """Return exactly displayed Publication Content, omitting absent fields."""
        sections = [
            self.headline,
            self.hook,
            self.article,
            self.cta,
        ]
        if self.hashtags:
            sections.append(" ".join(self.hashtags))
        if self.linkedin_description is not None:
            sections.append(self.linkedin_description)
        return "\n\n".join(sections)


class PublicationEditor:
    """A direct Author-edit surface with no AI writing actions."""

    STUDIO_ACTIONS = (PublicationEditorAction.COPY_LINKEDIN_PUBLICATION,)
    EDITABLE_FIELDS = frozenset(field.name for field in fields(PublicationContent))

    def __init__(self, generated_content: PublicationContent) -> None:
        if not isinstance(generated_content, PublicationContent):
            raise PublicationStudioError(
                "Publication Editor requires generated Publication Content."
            )
        self._generated_content = generated_content
        self._current_content = generated_content

    @property
    def generated_content(self) -> PublicationContent:
        return self._generated_content

    @property
    def current_content(self) -> PublicationContent:
        return self._current_content

    @property
    def studio_actions(self) -> tuple[PublicationEditorAction, ...]:
        return self.STUDIO_ACTIONS

    def author_edit(self, **changes: object) -> PublicationContent:
        """Apply only the exact fields explicitly edited by the Author."""
        if not changes:
            raise PublicationStudioError("An Author edit must change a field.")
        unsupported = set(changes) - self.EDITABLE_FIELDS
        if unsupported:
            raise PublicationStudioError(
                "Unsupported Publication Content fields: "
                + ", ".join(sorted(unsupported))
                + "."
            )
        updated = replace(self._current_content, **changes)
        self._current_content = updated
        return updated

    def copy_payload(self) -> str:
        """Return displayed content only; this performs no external copy action."""
        return self._current_content.rendered()


@dataclass(frozen=True, slots=True)
class HeroVisualWorkspace:
    """Display the generated visual with Author-controlled local actions."""

    visual: HeroVisualResult
    actions: tuple[HeroVisualAction, ...] = tuple(HeroVisualAction)

    def __post_init__(self) -> None:
        if not isinstance(self.visual, HeroVisualResult) or not self.visual.ready:
            raise PublicationStudioError(
                "Publication Studio requires a generated Hero Visual."
            )


@dataclass(frozen=True, slots=True)
class EditorialReview:
    """Generation-time editorial context kept outside Publication Content."""

    editorial_confidence: EditorialConfidence
    editorial_risk: EditorialRisk
    sources: tuple[str, ...]
    suggested_mentions: tuple[str, ...]
    branding_summary: str
    session_summary: str
    assessment_label: str = "As of Generation"
    may_not_reflect_current_edits: bool = False


@dataclass(frozen=True, slots=True)
class PublicationStudioPresentation:
    """Presentation data for the two workspaces and separate review panel."""

    workspaces: tuple[WorkspaceKind, ...]
    editorial_review_separate: bool
    editorial_review_collapsible: bool
    copy_action_enabled: bool


class PublicationStudio:
    """Session-local workspace containing generated artifacts and Author edits."""

    def __init__(
        self,
        generated_package: PublicationPackage,
        hero_visual: HeroVisualWorkspace,
        editor: PublicationEditor,
        editorial_review: EditorialReview,
    ) -> None:
        self.generated_package = generated_package
        self.hero_visual = hero_visual
        self.editor = editor
        self.editorial_review = editorial_review
        self.copy_gate_state = CopyGateState.UNMATCHED

    @classmethod
    def from_generation(
        cls,
        package: PublicationPackage,
        *,
        branding_summary: str,
        session_summary: str,
        suggested_mentions: tuple[str, ...] = (),
    ) -> PublicationStudio:
        if not isinstance(package, PublicationPackage):
            raise PublicationStudioError(
                "Publication Studio requires a generated Publication Package."
            )
        if package.rendered_hero_visual is None:
            raise PublicationStudioError(
                "Publication Studio requires the generated Hero Visual."
            )
        content = PublicationContent.from_package(package)
        return cls(
            generated_package=package,
            hero_visual=HeroVisualWorkspace(package.rendered_hero_visual),
            editor=PublicationEditor(content),
            editorial_review=EditorialReview(
                editorial_confidence=package.editorial_confidence,
                editorial_risk=package.editorial_risk,
                sources=package.source_and_attribution,
                suggested_mentions=suggested_mentions,
                branding_summary=branding_summary,
                session_summary=session_summary,
            ),
        )

    def presentation(self) -> PublicationStudioPresentation:
        return PublicationStudioPresentation(
            workspaces=(
                WorkspaceKind.HERO_VISUAL,
                WorkspaceKind.PUBLICATION_EDITOR,
            ),
            editorial_review_separate=True,
            editorial_review_collapsible=True,
            copy_action_enabled=self.copy_gate_state is CopyGateState.MATCHED,
        )

    def author_edit(self, **changes: object) -> PublicationContent:
        updated = self.editor.author_edit(**changes)
        self.copy_gate_state = CopyGateState.UNMATCHED
        base_label = self.editorial_review.assessment_label.split(";")[0]
        self.editorial_review = replace(
            self.editorial_review,
            assessment_label=f"{base_label}; unaudited Author edits exist",
            may_not_reflect_current_edits=True,
        )
        return updated

    def editorial_audit_input(self) -> PublicationContent:
        """Expose the current content to the V11-06 Editorial Audit."""
        return self.editor.current_content

    def apply_editorial_audit(self, result: "EditorialAuditResult") -> None:
        """Refresh Editorial Review and match the gate; never touches content.

        The gate is procedural, not evaluative (ADR-018 rule 4): it is set
        to matched because a completed audit now reflects the currently
        displayed content, regardless of what that audit found. A High or
        Severe result never keeps the gate unmatched or disables the copy
        action; it only withholds a positive Editorial Confidence.
        """
        self.copy_gate_state = CopyGateState.MATCHED
        self.editorial_review = replace(
            self.editorial_review,
            editorial_confidence=result.editorial_confidence,
            editorial_risk=result.lmhs_report.editorial_risk,
            assessment_label="As of most recent Editorial Audit",
            may_not_reflect_current_edits=False,
        )

    def copy_linkedin_publication(self) -> str:
        """Return exactly the displayed content once the gate is matched."""
        if self.copy_gate_state is not CopyGateState.MATCHED:
            raise PublicationStudioError(
                "Copy LinkedIn Publication is disabled until a completed "
                "Editorial Audit reflects the currently displayed content."
            )
        return self.editor.copy_payload()
