"""State-machine orchestration for the editorial workflow."""

from __future__ import annotations

from enum import IntEnum

from .choices import (
    ContentType,
    HeroCopyDirection,
    VisualStyle,
)
from .state import EditorialState


class InvalidTransitionError(RuntimeError):
    """Raised when an invalid workflow transition is attempted."""


class WorkflowStage(IntEnum):
    """Ordered editorial workflow stages."""

    START = 0
    SOURCE_ANALYZED = 1
    CONTENT_TYPE_SELECTED = 2
    VISUAL_STYLE_SELECTED = 3
    HERO_COPY_SELECTED = 4
    GRAPHIC_GENERATED = 5
    GRAPHIC_APPROVED = 6
    WRITTEN_CONTENT_GENERATED = 7
    FINAL_REVIEW = 8
    COMPLETE = 9


class EditorialWorkflow:
    """
    Orchestrate an editorial session.

    The workflow does not generate editorial content itself.
    It controls valid stages, preserves state, and coordinates
    downstream resets when an earlier decision changes.
    """

    def __init__(
        self,
        state: EditorialState | None = None,
    ) -> None:
        self.state = state or EditorialState()
        self.stage = self._infer_stage()

    def _infer_stage(self) -> WorkflowStage:
        if self.state.final_content_approved:
            return WorkflowStage.COMPLETE

        if (
            self.state.article_headline
            or self.state.carousel_slides
        ):
            return WorkflowStage.FINAL_REVIEW

        if self.state.hero_image_approved:
            return WorkflowStage.GRAPHIC_APPROVED

        if self.state.hero_image_reference:
            return WorkflowStage.GRAPHIC_GENERATED

        if (
            self.state.hero_headline
            and self.state.hero_supporting_text
        ):
            return WorkflowStage.HERO_COPY_SELECTED

        if self.state.visual_style:
            return WorkflowStage.VISUAL_STYLE_SELECTED

        if self.state.content_type:
            return WorkflowStage.CONTENT_TYPE_SELECTED

        if self.state.strongest_insight:
            return WorkflowStage.SOURCE_ANALYZED

        return WorkflowStage.START

    def _require(
        self,
        minimum_stage: WorkflowStage,
        action: str,
    ) -> None:
        if self.stage < minimum_stage:
            raise InvalidTransitionError(
                f"Cannot {action} from stage "
                f"{self.stage.name}. Required stage: "
                f"{minimum_stage.name}."
            )

    def analyze_source(
        self,
        *,
        source_url: str,
        strongest_insight: str,
        supporting_statistic: str,
        provocative_claim: str,
        source_title: str | None = None,
        source_summary: str | None = None,
        source_limitations: list[str] | None = None,
    ) -> None:
        """Record source analysis and clear downstream work."""
        if not source_url.startswith(("http://", "https://")):
            raise ValueError(
                "Source URL must begin with http:// or https://."
            )

        self.state = EditorialState(
            source_url=source_url,
            source_title=source_title,
            source_summary=source_summary,
            source_limitations=source_limitations or [],
            strongest_insight=strongest_insight,
            supporting_statistic=supporting_statistic,
            provocative_claim=provocative_claim,
        )
        self.stage = WorkflowStage.SOURCE_ANALYZED

    def choose_content_type(
        self,
        content_type: ContentType,
    ) -> None:
        """Select the content format."""
        self._require(
            WorkflowStage.SOURCE_ANALYZED,
            "choose a content type",
        )

        if self.state.content_type != content_type:
            self.state.content_type = content_type
            self.state.reset_visual_assets()

        self.stage = WorkflowStage.CONTENT_TYPE_SELECTED

    def choose_visual_style(
        self,
        visual_style: VisualStyle,
    ) -> None:
        """Select the visual creative direction."""
        self._require(
            WorkflowStage.CONTENT_TYPE_SELECTED,
            "choose a visual style",
        )

        if self.state.visual_style != visual_style:
            self.state.visual_style = visual_style
            self.state.hero_copy_direction = None
            self.state.hero_headline = None
            self.state.hero_supporting_text = None
            self.state.reset_hero_image()

        self.stage = WorkflowStage.VISUAL_STYLE_SELECTED

    def choose_hero_copy(
        self,
        *,
        direction: HeroCopyDirection,
        headline: str,
        supporting_text: str,
    ) -> None:
        """Record approved hero-copy selection."""
        self._require(
            WorkflowStage.VISUAL_STYLE_SELECTED,
            "choose hero copy",
        )

        self.state.hero_copy_direction = direction
        self.state.hero_headline = headline.strip()
        self.state.hero_supporting_text = (
            supporting_text.strip()
        )

        errors = self.state.validate_hero_copy()

        if errors:
            raise ValueError(" ".join(errors))

        self.state.reset_hero_image()
        self.stage = WorkflowStage.HERO_COPY_SELECTED

    def record_graphic(
        self,
        image_reference: str,
    ) -> None:
        """Record the generated hero image."""
        self._require(
            WorkflowStage.HERO_COPY_SELECTED,
            "record a graphic",
        )

        if not image_reference.strip():
            raise ValueError(
                "Image reference must not be empty."
            )

        self.state.hero_image_reference = (
            image_reference.strip()
        )
        self.state.hero_image_approved = False
        self.state.reset_written_content()
        self.stage = WorkflowStage.GRAPHIC_GENERATED

    def approve_graphic(self) -> None:
        """Approve the generated hero graphic."""
        self._require(
            WorkflowStage.GRAPHIC_GENERATED,
            "approve the graphic",
        )

        self.state.hero_image_approved = True
        self.stage = WorkflowStage.GRAPHIC_APPROVED

    def record_written_content(
        self,
        *,
        article_headline: str,
        hook: str,
        insight_1: str,
        practical_takeaway: str,
        source_mention: str,
        cta: str,
        hashtags: list[str],
        linkedin_description: str,
        insight_2: str | None = None,
        carousel_slides: list[dict[str, str]] | None = None,
    ) -> None:
        """Record generated article or carousel content."""
        self._require(
            WorkflowStage.GRAPHIC_APPROVED,
            "record written content",
        )

        if not 6 <= len(hashtags) <= 10:
            raise ValueError(
                "Final content requires 6 to 10 hashtags."
            )

        self.state.article_headline = (
            article_headline.strip()
        )
        self.state.hook = hook.strip()
        self.state.insight_1 = insight_1.strip()
        self.state.insight_2 = (
            insight_2.strip() if insight_2 else None
        )
        self.state.practical_takeaway = (
            practical_takeaway.strip()
        )
        self.state.source_mention = source_mention.strip()
        self.state.cta = cta.strip()
        self.state.hashtags = list(hashtags)
        self.state.linkedin_description = (
            linkedin_description.strip()
        )
        self.state.carousel_slides = (
            list(carousel_slides or [])
        )
        self.state.final_content_approved = False

        self.stage = WorkflowStage.FINAL_REVIEW

    def approve_final_content(self) -> None:
        """Approve the final editorial package."""
        self._require(
            WorkflowStage.FINAL_REVIEW,
            "approve final content",
        )

        self.state.final_content_approved = True
        self.stage = WorkflowStage.COMPLETE

    def back(self) -> WorkflowStage:
        """
        Return to the previous meaningful stage.

        Approved assets are retained unless the user subsequently
        changes an earlier decision.
        """
        if self.stage == WorkflowStage.START:
            return self.stage

        previous = WorkflowStage(self.stage - 1)
        self.stage = previous
        return self.stage

    def restart(self) -> None:
        """Begin a completely new editorial session."""
        self.state = EditorialState()
        self.stage = WorkflowStage.START

    def status(self) -> dict[str, object]:
        """Return a compact workflow status payload."""
        return {
            "stage": self.stage.name,
            "source_url": self.state.source_url,
            "content_type": (
                str(self.state.content_type)
                if self.state.content_type
                else None
            ),
            "visual_style": (
                str(self.state.visual_style)
                if self.state.visual_style
                else None
            ),
            "graphic_approved": (
                self.state.hero_image_approved
            ),
            "final_content_approved": (
                self.state.final_content_approved
            ),
        }
