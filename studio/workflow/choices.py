"""Authoritative selectable choices for the editorial workflow."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


IMAGE_WIDTH = 720
IMAGE_HEIGHT = 425
IMAGE_ASPECT_RATIO = IMAGE_WIDTH / IMAGE_HEIGHT


class ContentType(StrEnum):
    """Supported LinkedIn content formats."""

    ARTICLE = "linkedin_article"
    CAROUSEL = "linkedin_carousel"
    RECOMMENDED = "recommended"


class VisualStyle(StrEnum):
    """Supported hero-graphic creative directions."""

    EXECUTIVE_EDITORIAL = "executive_editorial"
    MAGAZINE_COVER = "magazine_cover"
    DATA_STORY = "data_story"
    RECOMMENDED = "recommended"


class HeroCopyDirection(StrEnum):
    """Supported hero-copy positioning choices."""

    RECOMMENDED = "recommended"
    PROVOCATIVE = "provocative"
    EXECUTIVE = "executive"
    GENERATE_NEW = "generate_new"


class ReviewAction(StrEnum):
    """Actions available during a review checkpoint."""

    APPROVE = "approve"
    REVISE_TEXT = "revise_text"
    CHANGE_STYLE = "change_style"
    REGENERATE = "regenerate"
    CHANGE_PALETTE = "change_palette"
    BACK = "back"
    RESTART = "restart"


@dataclass(frozen=True, slots=True)
class Choice:
    """A user-facing selectable workflow option."""

    number: int
    value: str
    title: str
    description: str
    recommended: bool = False

    @property
    def label(self) -> str:
        recommendation = " - Recommended" if self.recommended else ""
        return f"Option {self.number} - {self.title}{recommendation}"


CONTENT_TYPE_OPTIONS = (
    Choice(
        number=1,
        value=ContentType.ARTICLE,
        title="LinkedIn Article",
        description="A concise thought-leadership analysis.",
    ),
    Choice(
        number=2,
        value=ContentType.CAROUSEL,
        title="LinkedIn Carousel",
        description="A seven-slide visual narrative.",
    ),
    Choice(
        number=3,
        value=ContentType.RECOMMENDED,
        title="Use the Recommendation",
        description="Select the format best suited to the source.",
        recommended=True,
    ),
)


VISUAL_STYLE_OPTIONS = (
    Choice(
        number=1,
        value=VisualStyle.EXECUTIVE_EDITORIAL,
        title="Executive Editorial",
        description=(
            "Premium, restrained, authoritative, and insight-led."
        ),
        recommended=True,
    ),
    Choice(
        number=2,
        value=VisualStyle.MAGAZINE_COVER,
        title="Magazine Cover",
        description=(
            "Bold, cinematic, and designed to stop scrolling."
        ),
    ),
    Choice(
        number=3,
        value=VisualStyle.DATA_STORY,
        title="Data Story",
        description=(
            "Research-led with one prominent statistic."
        ),
    ),
    Choice(
        number=4,
        value=VisualStyle.RECOMMENDED,
        title="Use the Recommendation",
        description=(
            "Match the visual treatment to the source."
        ),
    ),
)


HERO_COPY_OPTIONS = (
    Choice(
        number=1,
        value=HeroCopyDirection.RECOMMENDED,
        title="Recommended",
        description=(
            "The strongest balanced editorial direction."
        ),
        recommended=True,
    ),
    Choice(
        number=2,
        value=HeroCopyDirection.PROVOCATIVE,
        title="More Provocative",
        description=(
            "A sharper, curiosity-led interpretation."
        ),
    ),
    Choice(
        number=3,
        value=HeroCopyDirection.EXECUTIVE,
        title="More Executive",
        description=(
            "A restrained leadership-oriented interpretation."
        ),
    ),
    Choice(
        number=4,
        value=HeroCopyDirection.GENERATE_NEW,
        title="Generate New Options",
        description="Create three fresh combinations.",
    ),
)


REVIEW_OPTIONS = (
    Choice(
        number=1,
        value=ReviewAction.APPROVE,
        title="Approve and Continue",
        description="Accept the current work and advance.",
        recommended=True,
    ),
    Choice(
        number=2,
        value=ReviewAction.REVISE_TEXT,
        title="Revise the Text",
        description="Change the headline or supporting statement.",
    ),
    Choice(
        number=3,
        value=ReviewAction.CHANGE_STYLE,
        title="Change the Visual Direction",
        description="Select a different creative treatment.",
    ),
    Choice(
        number=4,
        value=ReviewAction.REGENERATE,
        title="Regenerate the Same Concept",
        description="Keep the approved copy and vary the image.",
    ),
    Choice(
        number=5,
        value=ReviewAction.BACK,
        title="Back",
        description="Return to the previous workflow stage.",
    ),
)
