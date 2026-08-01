#!/usr/bin/env python3
"""
Bootstrap Sprint 2 - Editorial Workflow System.

Default behavior:
- Verifies the repository and GitHub remote
- Updates develop safely
- Creates or switches to the Sprint 2 feature branch
- Generates the workflow package, tests, documentation, and ADR-001
- Runs validation and unit tests
- Stops before committing or pushing

Publishing behavior:
    python3 scripts/bootstrap_sprint2_workflow.py --publish

This will:
- Stage the Sprint 2 changes
- Commit them
- Push the feature branch
- Open PR-002 against develop
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import textwrap
from pathlib import Path


REPOSITORY_NAME = "Ramrattan-AI-Editorial-Studio"
REMOTE_FRAGMENT = "RamrattanN/Ramrattan-AI-Editorial-Studio"

BASE_BRANCH = "develop"
FEATURE_BRANCH = "feature/editorial-workflow-system"

COMMIT_MESSAGE = (
    "feat: add the editorial workflow system"
)

PR_TITLE = "PR-002: Add the editorial workflow system"


def clean(value: str) -> str:
    """Normalize embedded file content."""
    return textwrap.dedent(value).strip() + "\n"


FILES: dict[str, str] = {
    "studio/__init__.py": clean(
        '''
        """Ramrattan AI Editorial Studio package."""

        __all__ = ["workflow"]
        '''
    ),

    "studio/workflow/__init__.py": clean(
        '''
        """Public interface for the editorial workflow system."""

        from .choices import (
            CONTENT_TYPE_OPTIONS,
            HERO_COPY_OPTIONS,
            REVIEW_OPTIONS,
            VISUAL_STYLE_OPTIONS,
            ContentType,
            HeroCopyDirection,
            ReviewAction,
            VisualStyle,
        )
        from .state import EditorialState
        from .workflow import (
            EditorialWorkflow,
            InvalidTransitionError,
            WorkflowStage,
        )

        __all__ = [
            "CONTENT_TYPE_OPTIONS",
            "HERO_COPY_OPTIONS",
            "REVIEW_OPTIONS",
            "VISUAL_STYLE_OPTIONS",
            "ContentType",
            "EditorialState",
            "EditorialWorkflow",
            "HeroCopyDirection",
            "InvalidTransitionError",
            "ReviewAction",
            "VisualStyle",
            "WorkflowStage",
        ]
        '''
    ),

    "studio/workflow/choices.py": clean(
        '''
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
        '''
    ),

    "studio/workflow/state.py": clean(
        '''
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
        '''
    ),

    "studio/workflow/workflow.py": clean(
        '''
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
        '''
    ),

    "studio/workflow/README.md": clean(
        '''
        # Editorial Workflow System

        ## Purpose

        The workflow system coordinates the complete editorial journey
        without embedding generation logic in one monolithic prompt.

        The central principle is:

        > The workflow controls the AI, not the other way around.

        ## Responsibilities

        The package is responsible for:

        - Representing editorial session state
        - Defining selectable user choices
        - Enforcing valid workflow transitions
        - Preserving approved work
        - Resetting only affected downstream work
        - Supporting backward navigation
        - Supporting future save-and-resume behavior

        It is not responsible for:

        - Fetching source pages
        - Generating editorial copy
        - Generating images
        - Publishing to LinkedIn
        - Rendering interface components

        Those capabilities will be supplied by separate engines.

        ## Package Structure

        ```text
        studio/workflow/
        ├── __init__.py
        ├── choices.py
        ├── state.py
        └── workflow.py
        ```

        ## Workflow Stages

        ```text
        START
          ↓
        SOURCE_ANALYZED
          ↓
        CONTENT_TYPE_SELECTED
          ↓
        VISUAL_STYLE_SELECTED
          ↓
        HERO_COPY_SELECTED
          ↓
        GRAPHIC_GENERATED
          ↓
        GRAPHIC_APPROVED
          ↓
        WRITTEN_CONTENT_GENERATED
          ↓
        FINAL_REVIEW
          ↓
        COMPLETE
        ```

        ## State Preservation

        Moving backward does not immediately delete approved work.

        Changing an earlier decision clears only the assets that depend
        on that decision.

        Examples:

        - Changing a color palette does not rewrite the article.
        - Changing the visual style clears hero copy and visual assets.
        - Changing the content type clears visual and written assets.
        - Restarting clears the complete session.

        ## Example

        ```python
        from studio.workflow import (
            ContentType,
            EditorialWorkflow,
            HeroCopyDirection,
            VisualStyle,
        )

        workflow = EditorialWorkflow()

        workflow.analyze_source(
            source_url="https://example.com/article",
            strongest_insight="Remote work changes occupancy economics.",
            supporting_statistic="$200 per month",
            provocative_claim=(
                "Utility models were not designed for remote work."
            ),
        )

        workflow.choose_content_type(ContentType.ARTICLE)

        workflow.choose_visual_style(
            VisualStyle.EXECUTIVE_EDITORIAL
        )

        workflow.choose_hero_copy(
            direction=HeroCopyDirection.RECOMMENDED,
            headline=(
                "Remote Work Is Reshaping Rental Economics"
            ),
            supporting_text=(
                "Higher daytime occupancy is changing utility costs."
            ),
        )
        ```

        ## Why This Matters

        A structured workflow makes prompt behavior testable,
        comprehensible, and replaceable.

        The AI model may change. The product journey should remain stable.
        '''
    ),

    "docs/architecture/adr/ADR-001-the-workflow-is-the-product.md": clean(
        '''
        # ADR-001 - The Workflow Is the Product

        ## Status

        Accepted

        ## Date

        2026-08-01

        ## Context

        The original Article & Post Generator used one instruction set
        to analyze sources, develop editorial positioning, propose visual
        treatments, and generate final LinkedIn content.

        As the product evolved, this approach created several risks:

        - Workflow behavior could be hidden inside prompt language.
        - Moving backward could lose approved decisions.
        - User choices could be represented inconsistently.
        - Visual and editorial logic could become tightly coupled.
        - Replacing the underlying model could require redesigning the
          complete experience.

        ## Decision

        Ramrattan AI Editorial Studio will treat the guided workflow as
        the stable product layer.

        AI models, prompts, visual generators, and publishing adapters
        will operate as replaceable capabilities coordinated by that
        workflow.

        The workflow will explicitly represent:

        - Editorial session state
        - User choices
        - Valid transitions
        - Review checkpoints
        - Backward navigation
        - Downstream dependency resets
        - Final approval

        ## Alternatives Considered

        ### One Monolithic Prompt

        Rejected because behavior would remain difficult to test,
        extend, and restore.

        ### Generate Everything in One Step

        Rejected because it provides speed but weak editorial control.

        ### Build a Full Web Application Immediately

        Deferred because the workflow must be validated before investing
        in a complete interface.

        ## Consequences

        ### Positive

        - The workflow can be tested independently.
        - AI providers can be replaced.
        - User state can eventually be persisted.
        - Navigation becomes predictable.
        - Visual and written engines remain modular.
        - Product behavior is easier to document.

        ### Costs and Risks

        - More explicit code is required.
        - State dependencies must be maintained carefully.
        - Workflow versioning becomes a product responsibility.
        - Mock implementations are needed before all engines exist.

        ## Outcome

        Accepted as the core architectural principle for Sprint 2.
        '''
    ),

    "tests/test_workflow.py": clean(
        '''
        """Tests for the editorial workflow system."""

        from __future__ import annotations

        import unittest

        from studio.workflow import (
            ContentType,
            EditorialState,
            EditorialWorkflow,
            HeroCopyDirection,
            InvalidTransitionError,
            VisualStyle,
            WorkflowStage,
        )


        class EditorialWorkflowTests(unittest.TestCase):
            def create_source_workflow(self) -> EditorialWorkflow:
                workflow = EditorialWorkflow()

                workflow.analyze_source(
                    source_url="https://example.com/article",
                    source_title="Example Article",
                    strongest_insight=(
                        "Remote work changes building economics."
                    ),
                    supporting_statistic="$200 per month",
                    provocative_claim=(
                        "Utility models were not built for remote work."
                    ),
                )

                return workflow

            def create_graphic_approved_workflow(
                self,
            ) -> EditorialWorkflow:
                workflow = self.create_source_workflow()

                workflow.choose_content_type(
                    ContentType.ARTICLE
                )
                workflow.choose_visual_style(
                    VisualStyle.EXECUTIVE_EDITORIAL
                )
                workflow.choose_hero_copy(
                    direction=HeroCopyDirection.RECOMMENDED,
                    headline=(
                        "Remote Work Is Reshaping Rental Economics"
                    ),
                    supporting_text=(
                        "Higher daytime occupancy is changing "
                        "utility costs."
                    ),
                )
                workflow.record_graphic(
                    "generated-image-reference"
                )
                workflow.approve_graphic()

                return workflow

            def test_initial_stage_is_start(self) -> None:
                workflow = EditorialWorkflow()

                self.assertEqual(
                    workflow.stage,
                    WorkflowStage.START,
                )

            def test_complete_happy_path(self) -> None:
                workflow = self.create_graphic_approved_workflow()

                workflow.record_written_content(
                    article_headline=(
                        "Remote Work Is Reshaping Rental Economics"
                    ),
                    hook="Remote work changed more than commuting.",
                    insight_1=(
                        "Daytime occupancy increases utility usage."
                    ),
                    practical_takeaway=(
                        "Use transparent utility allocation models."
                    ),
                    source_mention="@Example",
                    cta="Surcharge or smarter metering?",
                    hashtags=[
                        "#RealEstate",
                        "#RemoteWork",
                        "#Multifamily",
                        "#PropertyManagement",
                        "#Utilities",
                        "#AssetManagement",
                    ],
                    linkedin_description=(
                        "An analysis of remote-work utility costs."
                    ),
                )

                self.assertEqual(
                    workflow.stage,
                    WorkflowStage.FINAL_REVIEW,
                )

                workflow.approve_final_content()

                self.assertEqual(
                    workflow.stage,
                    WorkflowStage.COMPLETE,
                )
                self.assertTrue(
                    workflow.state.final_content_approved
                )

            def test_cannot_choose_style_before_content_type(
                self,
            ) -> None:
                workflow = self.create_source_workflow()

                with self.assertRaises(
                    InvalidTransitionError
                ):
                    workflow.choose_visual_style(
                        VisualStyle.DATA_STORY
                    )

            def test_hero_copy_word_limits(self) -> None:
                workflow = self.create_source_workflow()

                workflow.choose_content_type(
                    ContentType.ARTICLE
                )
                workflow.choose_visual_style(
                    VisualStyle.EXECUTIVE_EDITORIAL
                )

                with self.assertRaises(ValueError):
                    workflow.choose_hero_copy(
                        direction=(
                            HeroCopyDirection.RECOMMENDED
                        ),
                        headline="Too Short",
                        supporting_text="Supporting text.",
                    )

            def test_changing_visual_style_resets_downstream(
                self,
            ) -> None:
                workflow = self.create_graphic_approved_workflow()

                workflow.choose_visual_style(
                    VisualStyle.DATA_STORY
                )

                self.assertEqual(
                    workflow.stage,
                    WorkflowStage.VISUAL_STYLE_SELECTED,
                )
                self.assertIsNone(
                    workflow.state.hero_headline
                )
                self.assertIsNone(
                    workflow.state.hero_image_reference
                )
                self.assertFalse(
                    workflow.state.hero_image_approved
                )

            def test_state_json_round_trip(self) -> None:
                state = EditorialState(
                    source_url="https://example.com",
                    content_type=ContentType.ARTICLE,
                    visual_style=VisualStyle.DATA_STORY,
                    hashtags=["#One", "#Two"],
                )

                restored = EditorialState.from_json(
                    state.to_json()
                )

                self.assertEqual(
                    restored.source_url,
                    state.source_url,
                )
                self.assertEqual(
                    restored.content_type,
                    ContentType.ARTICLE,
                )
                self.assertEqual(
                    restored.visual_style,
                    VisualStyle.DATA_STORY,
                )
                self.assertEqual(
                    restored.hashtags,
                    ["#One", "#Two"],
                )

            def test_restart_clears_session(self) -> None:
                workflow = self.create_graphic_approved_workflow()

                workflow.restart()

                self.assertEqual(
                    workflow.stage,
                    WorkflowStage.START,
                )
                self.assertIsNone(
                    workflow.state.source_url
                )


        if __name__ == "__main__":
            unittest.main()
        '''
    ),
}


CHANGELOG_ENTRY = clean(
    '''
    ### Added - Sprint 2 Editorial Workflow System

    - Explicit editorial workflow state machine
    - Serializable editorial session state
    - Centralized selectable user choices
    - Back and restart navigation
    - Dependency-aware downstream resets
    - Hero-copy validation
    - Unit tests for workflow behavior
    - ADR-001 - The Workflow Is the Product
    '''
)


class BootstrapError(RuntimeError):
    """Raised when Sprint 2 automation cannot proceed safely."""


def run(
    command: list[str],
    *,
    cwd: Path,
    check: bool = True,
    capture: bool = False,
) -> subprocess.CompletedProcess[str]:
    """Run a command and print it first."""
    print("$", " ".join(command))

    return subprocess.run(
        command,
        cwd=cwd,
        check=check,
        text=True,
        capture_output=capture,
    )


def output(command: list[str], *, cwd: Path) -> str:
    """Run a command and return stdout."""
    result = run(
        command,
        cwd=cwd,
        capture=True,
    )
    return result.stdout.strip()


def repository_root() -> Path:
    """Find and validate the Git repository."""
    try:
        root = Path(
            output(
                ["git", "rev-parse", "--show-toplevel"],
                cwd=Path.cwd(),
            )
        ).resolve()
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise BootstrapError(
            "Run the script from inside the cloned repository."
        ) from exc

    if root.name != REPOSITORY_NAME:
        raise BootstrapError(
            f"Expected repository '{REPOSITORY_NAME}', "
            f"found '{root.name}'."
        )

    remote = output(
        ["git", "remote", "get-url", "origin"],
        cwd=root,
    )

    if REMOTE_FRAGMENT not in remote:
        raise BootstrapError(
            "The origin remote does not match the expected repository."
        )

    return root


def current_branch(root: Path) -> str:
    """Return the current branch."""
    return output(
        ["git", "branch", "--show-current"],
        cwd=root,
    )


def ensure_branch(root: Path) -> None:
    """Update develop and create or switch to the feature branch."""
    branch = current_branch(root)

    if branch == FEATURE_BRANCH:
        print(f"Already on {FEATURE_BRANCH}.")
        return

    if branch != BASE_BRANCH:
        raise BootstrapError(
            f"Run this script from '{BASE_BRANCH}' or "
            f"'{FEATURE_BRANCH}'. Current branch: '{branch}'."
        )

    status = output(
        ["git", "status", "--porcelain"],
        cwd=root,
    )

    allowed_untracked = {
        "?? scripts/bootstrap_sprint2_workflow.py"
    }

    unexpected = [
        line
        for line in status.splitlines()
        if line not in allowed_untracked
    ]

    if unexpected:
        details = "\n".join(unexpected)
        raise BootstrapError(
            "The develop branch has unexpected local changes:\n"
            f"{details}\n"
            "Commit, stash, or discard them before continuing."
        )

    run(["git", "fetch", "origin", "--prune"], cwd=root)
    run(
        ["git", "pull", "--ff-only", "origin", BASE_BRANCH],
        cwd=root,
    )

    local_exists = subprocess.run(
        [
            "git",
            "show-ref",
            "--verify",
            "--quiet",
            f"refs/heads/{FEATURE_BRANCH}",
        ],
        cwd=root,
    ).returncode == 0

    remote_exists = subprocess.run(
        [
            "git",
            "ls-remote",
            "--exit-code",
            "--heads",
            "origin",
            FEATURE_BRANCH,
        ],
        cwd=root,
        capture_output=True,
        text=True,
    ).returncode == 0

    if local_exists:
        run(["git", "switch", FEATURE_BRANCH], cwd=root)
    elif remote_exists:
        run(
            [
                "git",
                "switch",
                "--track",
                f"origin/{FEATURE_BRANCH}",
            ],
            cwd=root,
        )
    else:
        run(
            ["git", "switch", "-c", FEATURE_BRANCH],
            cwd=root,
        )


def write_files(root: Path) -> None:
    """Write all Sprint 2 files deterministically."""
    for relative, content in FILES.items():
        destination = root / relative
        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        destination.write_text(
            content,
            encoding="utf-8",
        )
        print(f"Wrote {relative}")


def update_changelog(root: Path) -> None:
    """Insert the Sprint 2 changelog entry once."""
    path = root / "CHANGELOG.md"

    if not path.exists():
        raise BootstrapError("CHANGELOG.md is missing.")

    content = path.read_text(encoding="utf-8")

    marker = "### Added - Sprint 2 Editorial Workflow System"

    if marker in content:
        print("Sprint 2 changelog entry already exists.")
        return

    insertion_point = "## [Unreleased]\n"

    if insertion_point not in content:
        raise BootstrapError(
            "Could not locate the Unreleased changelog section."
        )

    updated = content.replace(
        insertion_point,
        insertion_point + "\n" + CHANGELOG_ENTRY + "\n",
        1,
    )

    path.write_text(updated, encoding="utf-8")
    print("Updated CHANGELOG.md")


def validate_python(root: Path) -> None:
    """Compile package files and run unit tests."""
    run(
        [
            sys.executable,
            "-m",
            "compileall",
            "-q",
            "studio",
            "tests",
        ],
        cwd=root,
    )

    run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "tests",
            "-v",
        ],
        cwd=root,
    )

    run(
        [
            sys.executable,
            "studio.py",
            "validate",
        ],
        cwd=root,
    )


def validate_files(root: Path) -> None:
    """Ensure all expected files exist."""
    missing = [
        relative
        for relative in FILES
        if not (root / relative).is_file()
    ]

    if missing:
        formatted = "\n".join(
            f"  - {relative}" for relative in missing
        )
        raise BootstrapError(
            f"Missing generated files:\n{formatted}"
        )

    print("Sprint 2 file validation passed.")


def publish(root: Path) -> None:
    """Commit, push, and open PR-002."""
    if current_branch(root) != FEATURE_BRANCH:
        raise BootstrapError(
            f"Publishing requires branch '{FEATURE_BRANCH}'."
        )

    run(["gh", "auth", "status"], cwd=root)
    run(["git", "add", "."], cwd=root)

    staged = output(
        ["git", "diff", "--cached", "--name-only"],
        cwd=root,
    )

    if not staged:
        print("No staged changes are available to publish.")
        return

    run(
        [
            "git",
            "commit",
            "-m",
            COMMIT_MESSAGE,
        ],
        cwd=root,
    )

    run(
        [
            "git",
            "push",
            "--set-upstream",
            "origin",
            FEATURE_BRANCH,
        ],
        cwd=root,
    )

    existing = subprocess.run(
        [
            "gh",
            "pr",
            "view",
            FEATURE_BRANCH,
            "--json",
            "url",
            "--jq",
            ".url",
        ],
        cwd=root,
        text=True,
        capture_output=True,
    )

    if existing.returncode == 0 and existing.stdout.strip():
        print(
            "Pull request already exists: "
            f"{existing.stdout.strip()}"
        )
        return

    body = clean(
        '''
        ## Summary

        Adds the first product-level architecture for Ramrattan AI
        Editorial Studio: an explicit, testable editorial workflow.

        ## Problem

        The product journey was previously represented mainly through
        prompt instructions. That made workflow transitions, state
        preservation, backward navigation, and dependency resets
        difficult to test independently.

        ## Changes

        - Adds the `studio.workflow` Python package
        - Adds centralized user choices
        - Adds serializable editorial state
        - Adds an explicit workflow state machine
        - Adds backward and restart navigation
        - Adds dependency-aware reset behavior
        - Adds hero-copy validation
        - Adds workflow unit tests
        - Adds workflow package documentation
        - Adds ADR-001 - The Workflow Is the Product
        - Updates the changelog

        ## Acceptance Criteria

        - Workflow stages are explicit
        - Invalid transitions raise an error
        - State can be serialized and restored
        - Changing earlier decisions clears affected downstream work
        - Back and restart operations are supported
        - Hero-copy constraints are validated
        - Unit tests pass

        ## Validation

        ```bash
        python3 -m compileall -q studio tests
        python3 -m unittest discover -s tests -v
        python3 studio.py validate
        ```

        ## Rollback

        Close the pull request without merging, or revert the Sprint 2
        feature commit after merge.
        '''
    )

    run(
        [
            "gh",
            "pr",
            "create",
            "--base",
            BASE_BRANCH,
            "--head",
            FEATURE_BRANCH,
            "--title",
            PR_TITLE,
            "--body",
            body,
        ],
        cwd=root,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create the Sprint 2 editorial workflow system."
        )
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help=(
            "Commit, push, and open PR-002 after validation."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        root = repository_root()

        print(f"Repository: {root}")
        print(f"Starting branch: {current_branch(root)}")

        ensure_branch(root)

        print(f"Working branch: {current_branch(root)}")

        write_files(root)
        update_changelog(root)
        validate_files(root)
        validate_python(root)

        print("\nGit status:")
        run(["git", "status", "--short"], cwd=root)

        print("\nTracked change summary:")
        run(["git", "diff", "--stat"], cwd=root)

        if args.publish:
            publish(root)
        else:
            print("\nSprint 2 workflow system created.")
            print("Validation and unit tests passed.")
            print("Nothing has been committed or pushed.")
            print()
            print("Review the files in VS Code, then run:")
            print(
                "  python3 "
                "scripts/bootstrap_sprint2_workflow.py "
                "--publish"
            )

        return 0

    except BootstrapError as exc:
        print(f"\nERROR: {exc}", file=sys.stderr)
        return 1

    except subprocess.CalledProcessError as exc:
        print(
            f"\nERROR: Command failed with exit code "
            f"{exc.returncode}.",
            file=sys.stderr,
        )
        return exc.returncode

    except Exception as exc:
        print(
            f"\nUNEXPECTED ERROR: {exc}",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())