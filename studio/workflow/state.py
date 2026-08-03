"""Serializable state for one editorial workflow session."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .choices import (
    ContentType,
    HeroCopyDirection,
    VisualStyle,
)


@dataclass(slots=True)
class EditorialState:
    """
    Single source of truth for an editorial session.

    The state contains approved user decisions and generated
    editorial assets. It can be serialized for future persistence.
    """

    source_url: str | None = None
    source_title: str | None = None
    source_summary: str | None = None
    source_limitations: list[str] = field(default_factory=list)

    strongest_insight: str | None = None
    supporting_statistic: str | None = None
    provocative_claim: str | None = None

    content_type: ContentType | None = None
    visual_style: VisualStyle | None = None
    hero_copy_direction: HeroCopyDirection | None = None

    hero_headline: str | None = None
    hero_supporting_text: str | None = None
    hero_image_reference: str | None = None
    hero_image_approved: bool = False

    article_headline: str | None = None
    hook: str | None = None
    insight_1: str | None = None
    insight_2: str | None = None
    practical_takeaway: str | None = None
    source_mention: str | None = None
    cta: str | None = None
    hashtags: list[str] = field(default_factory=list)
    linkedin_description: str | None = None

    carousel_slides: list[dict[str, str]] = field(
        default_factory=list
    )

    final_content_approved: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible representation."""
        result = asdict(self)

        for key in (
            "content_type",
            "visual_style",
            "hero_copy_direction",
        ):
            value = result[key]
            if value is not None:
                result[key] = str(value)

        return result

    def to_json(self, *, indent: int = 2) -> str:
        """Serialize the state to JSON."""
        import json

        return json.dumps(
            self.to_dict(),
            indent=indent,
            ensure_ascii=False,
            sort_keys=True,
        )

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "EditorialState":
        """Restore a state instance from a dictionary."""
        values = dict(data)

        if values.get("content_type"):
            values["content_type"] = ContentType(
                values["content_type"]
            )

        if values.get("visual_style"):
            values["visual_style"] = VisualStyle(
                values["visual_style"]
            )

        if values.get("hero_copy_direction"):
            values["hero_copy_direction"] = HeroCopyDirection(
                values["hero_copy_direction"]
            )

        return cls(**values)

    @classmethod
    def from_json(cls, payload: str) -> "EditorialState":
        """Restore a state instance from JSON."""
        import json

        parsed = json.loads(payload)

        if not isinstance(parsed, dict):
            raise ValueError(
                "Editorial state JSON must contain an object."
            )

        return cls.from_dict(parsed)

    def reset_visual_assets(self) -> None:
        """Clear visual decisions and all downstream content."""
        self.visual_style = None
        self.hero_copy_direction = None
        self.hero_headline = None
        self.hero_supporting_text = None
        self.hero_image_reference = None
        self.hero_image_approved = False
        self.reset_written_content()

    def reset_hero_image(self) -> None:
        """Clear the generated image and downstream content."""
        self.hero_image_reference = None
        self.hero_image_approved = False
        self.reset_written_content()

    def reset_written_content(self) -> None:
        """Clear generated written assets."""
        self.article_headline = None
        self.hook = None
        self.insight_1 = None
        self.insight_2 = None
        self.practical_takeaway = None
        self.source_mention = None
        self.cta = None
        self.hashtags.clear()
        self.linkedin_description = None
        self.carousel_slides.clear()
        self.final_content_approved = False

    def validate_hero_copy(self) -> list[str]:
        """Return hero-copy validation errors."""
        errors: list[str] = []

        if not self.hero_headline:
            errors.append("Hero headline is required.")
        elif not 6 <= len(self.hero_headline.split()) <= 10:
            errors.append(
                "Hero headline must contain 6 to 10 words."
            )

        if not self.hero_supporting_text:
            errors.append(
                "Hero supporting text is required."
            )
        elif len(self.hero_supporting_text.split()) > 20:
            errors.append(
                "Hero supporting text must not exceed 20 words."
            )

        return errors
