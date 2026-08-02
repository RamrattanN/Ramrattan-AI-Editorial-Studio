#!/usr/bin/env python3
"""
Capability 007 - Editorial Workspace, Editorial Intake, and Source Assessment

Preview:

    python3 scripts/bootstrap_capability007_editorial_intake.py

Apply local repository changes:

    python3 scripts/bootstrap_capability007_editorial_intake.py --apply

Synchronize GitHub planning after local validation:

    python3 scripts/bootstrap_capability007_editorial_intake.py \
        --sync-project

This script:

- Verifies the expected repository and feature branch
- Verifies that the pasted script is complete
- Adds the Canonical Vocabulary
- Establishes Editorial Workspace as the Author-facing environment
- Retains Editorial Intake as the first capability within the Workspace
- Implements deterministic input recognition
- Implements the first two visible Editorial Integrity stages
- Implements initial source assessment
- Supports optional logo and headshot identity assets
- Requires rights confirmation before identity-asset use
- Preserves brand-neutral Hero Visuals as the default
- Adds runtime, architecture, UX, demo, and validation files
- Creates ADR-007
- Creates Architecture Baseline 2026.08.01v03
- Updates complementary documentation
- Optionally synchronizes GitHub Project planning

Preview mode changes nothing.

--apply changes local repository files only.

--sync-project changes GitHub planning only after the local capability
exists and validates.

This script does not commit, push, merge, or open a pull request.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import textwrap
import time
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------
# Repository configuration
# ---------------------------------------------------------------------

EXPECTED_REPOSITORY = "Ramrattan-AI-Editorial-Studio"

EXPECTED_REMOTE_FRAGMENT = (
    "RamrattanN/Ramrattan-AI-Editorial-Studio"
)

EXPECTED_BRANCH = (
    "feature/editorial-intake-source-assessment"
)

OWNER = "RamrattanN"

REPOSITORY = (
    "RamrattanN/Ramrattan-AI-Editorial-Studio"
)

PROJECT_NUMBER = 1

PROJECT_ID = "PVT_kwHOAuXHyM4BfHW9"

STATUS_FIELD_ID = (
    "PVTSSF_lAHOAuXHyM4BfHW9zhZclQY"
)

STATUS_OPTIONS = {
    "Todo": "f75ad846",
    "In Progress": "47fc9ee4",
    "Done": "98236657",
}

SCRIPT_RELATIVE_PATH = (
    "scripts/bootstrap_capability007_editorial_intake.py"
)

SCRIPT_SENTINEL = (
    "CAPABILITY_007_EDITORIAL_INTAKE_COMPLETE"
)

CAPABILITY_NAME = (
    "Capability 007 - Editorial Intake and Source Assessment"
)

CAPABILITY_ISSUE_TITLE = (
    "Capability 007 - Implement Editorial Intake "
    "and Source Assessment"
)

PREVIOUS_CAPABILITY_ISSUE_TITLE = (
    "Capability 006A - Constitutional Freeze"
)

ARCHITECTURE_BASELINE_VERSION = "2026.08.01v03"


# ---------------------------------------------------------------------
# General helpers
# ---------------------------------------------------------------------

def clean(value: str) -> str:
    """Dedent text and ensure one trailing newline."""
    return textwrap.dedent(value).strip() + "\n"


def normalize_markdown(value: str) -> str:
    """Normalize Markdown for resilient semantic validation."""
    return " ".join(
        value.replace(">", " ").split()
    )


# ---------------------------------------------------------------------
# Runtime implementation
# ---------------------------------------------------------------------

EDITORIAL_INTAKE_RUNTIME = clean(
    '''
    """Editorial Workspace intake runtime for Capability 007.

    This module implements:

    - the Author-facing Editorial Workspace welcome experience,
    - deterministic input recognition,
    - the first two visible Editorial Integrity stages,
    - initial source assessment,
    - optional logo and headshot identity-asset handling,
    - and rights confirmation.

    It deliberately does not perform full evidence validation.
    That responsibility belongs to Capability 008.
    """

    from __future__ import annotations

    from dataclasses import dataclass, field
    from enum import Enum
    from pathlib import Path
    from typing import Iterable
    from urllib.parse import urlparse


    class InputKind(str, Enum):
        """Canonical Editorial Intake classifications."""

        URL = "url"
        PASTED_TEXT = "pasted_text"
        DOCUMENT = "document"
        IMAGE = "image"
        AUDIO = "audio"
        VIDEO = "video"
        PORTABLE_EDITORIAL_PROJECT = "portable_editorial_project"
        LOGO = "logo"
        HEADSHOT = "headshot"
        UNKNOWN = "unknown"


    class WorkspaceStage(str, Enum):
        """Visible Editorial Integrity Pipeline stages."""

        UNDERSTANDING_INPUT = "understanding_input"
        ASSESSING_SOURCES = "assessing_sources"
        VERIFYING_EVIDENCE = "verifying_evidence"
        REVIEWING_EDITORIAL_RISKS = "reviewing_editorial_risks"
        CREATING_PUBLICATION_PACKAGE = "creating_publication_package"


    class StageState(str, Enum):
        """Presentation state for a visible Workspace stage."""

        COMPLETE = "complete"
        ACTIVE = "active"
        PENDING = "pending"
        BLOCKED = "blocked"


    class IdentityAssetKind(str, Enum):
        """Optional Author identity assets."""

        LOGO = "logo"
        HEADSHOT = "headshot"


    class SourceQuality(str, Enum):
        """Initial source-quality assessment.

        Capability 007 provides an intake-level assessment only.
        It does not claim full verification.
        """

        HIGH = "high"
        MODERATE = "moderate"
        LIMITED = "limited"
        UNKNOWN = "unknown"


    DOCUMENT_EXTENSIONS = {
        ".pdf",
        ".doc",
        ".docx",
        ".ppt",
        ".pptx",
        ".txt",
        ".rtf",
        ".md",
        ".odt",
    }

    IMAGE_EXTENSIONS = {
        ".png",
        ".jpg",
        ".jpeg",
        ".webp",
        ".gif",
        ".tif",
        ".tiff",
        ".heic",
    }

    AUDIO_EXTENSIONS = {
        ".mp3",
        ".m4a",
        ".wav",
        ".aac",
        ".flac",
        ".ogg",
    }

    VIDEO_EXTENSIONS = {
        ".mp4",
        ".mov",
        ".m4v",
        ".webm",
        ".avi",
        ".mkv",
    }

    PORTABLE_PROJECT_SUFFIXES = (
        ".editorial-project.md",
        ".portable-editorial-project.md",
    )


    @dataclass(frozen=True)
    class WorkspaceStageView:
        """One visible stage in the Editorial Workspace."""

        number: int
        name: str
        state: StageState
        detail: str = ""


    @dataclass(frozen=True)
    class InputDescriptor:
        """Normalized description of supplied Author material."""

        kind: InputKind
        value: str
        display_name: str
        extension: str = ""
        host_supported: bool = True
        notes: tuple[str, ...] = ()


    @dataclass(frozen=True)
    class IdentityAsset:
        """An optional logo or headshot supplied by the Author."""

        kind: IdentityAssetKind
        file_name: str
        rights_confirmed: bool = False
        usage_preference: str = "subtle"
        included_in_project_export: bool = False

        def validate(self) -> None:
            """Require rights confirmation before asset use."""
            if not self.rights_confirmed:
                raise ValueError(
                    "Identity assets require confirmation that the "
                    "Author is authorised to use them."
                )

            suffix = Path(self.file_name).suffix.lower()

            if suffix not in IMAGE_EXTENSIONS:
                raise ValueError(
                    "Logo and headshot assets must use a supported "
                    "image format."
                )


    @dataclass(frozen=True)
    class SourceAssessment:
        """Initial, non-verifying source assessment."""

        quality: SourceQuality
        source_identified: bool
        publication_date_known: bool
        primary_source_possible: bool
        requires_deeper_verification: bool
        observations: tuple[str, ...] = ()


    @dataclass
    class EditorialIntakeResult:
        """Result of the first two Workspace stages."""

        descriptor: InputDescriptor
        stages: list[WorkspaceStageView]
        source_assessment: SourceAssessment
        identity_assets: list[IdentityAsset] = field(
            default_factory=list
        )
        significant_findings: list[str] = field(
            default_factory=list
        )

        @property
        def brand_neutral(self) -> bool:
            """Return True when no identity assets are active."""
            return not self.identity_assets


    class EditorialWorkspace:
        """Author-facing Editorial Workspace entry point."""

        WELCOME_HEADLINE = (
            "Create a professional article from almost any source."
        )

        TRUST_PROMISE = (
            "Every article is reviewed for source quality, factual "
            "accuracy, and editorial risk before publication."
        )

        SUPPORTED_INPUTS = (
            "Web URL",
            "Pasted text",
            "PDF, Word, PowerPoint, Markdown, or plain text document",
            "Image containing readable text",
            "Audio supported by the host platform",
            "Video supported by the host platform",
            "Portable Editorial Project",
            "Professional observation or article idea",
            "Optional logo or headshot for the Hero Visual",
        )

        STAGE_NAMES = (
            "Understanding your input",
            "Assessing your sources",
            "Verifying the evidence",
            "Reviewing editorial risks",
            "Creating your publication package",
        )

        def welcome_message(
            self,
            preferred_name: str | None = None,
        ) -> str:
            """Return concise Author-facing Workspace copy."""
            greeting = "Welcome."

            if preferred_name and preferred_name.strip():
                greeting = (
                    f"Welcome back, {preferred_name.strip()}."
                )

            supported = "\\n".join(
                f"- {item}"
                for item in self.SUPPORTED_INPUTS
            )

            return (
                f"{greeting}\\n\\n"
                f"{self.WELCOME_HEADLINE}\\n\\n"
                f"{self.TRUST_PROMISE}\\n\\n"
                "You may provide:\\n"
                f"{supported}\\n\\n"
                "The Editor will:\\n"
                "1. Understand your input\\n"
                "2. Assess your sources\\n"
                "3. Verify the evidence\\n"
                "4. Review editorial risks\\n"
                "5. Create your publication package\\n\\n"
                "You remain in control throughout."
            )

        def recognize_input(
            self,
            value: str,
            *,
            declared_file_name: str | None = None,
        ) -> InputDescriptor:
            """Classify Author input without requiring a menu."""
            normalized = value.strip()

            if not normalized:
                return InputDescriptor(
                    kind=InputKind.UNKNOWN,
                    value=value,
                    display_name="Empty input",
                    notes=("No usable material was supplied.",),
                )

            file_name = declared_file_name or normalized
            suffix = Path(file_name).suffix.lower()

            if self._is_url(normalized):
                parsed = urlparse(normalized)

                return InputDescriptor(
                    kind=InputKind.URL,
                    value=normalized,
                    display_name=parsed.netloc or normalized,
                    notes=(
                        "A URL is provenance, not durable memory.",
                    ),
                )

            lower_name = file_name.lower()

            if lower_name.endswith(
                PORTABLE_PROJECT_SUFFIXES
            ) or (
                suffix == ".md"
                and "editorial-project" in lower_name
            ):
                return InputDescriptor(
                    kind=InputKind.PORTABLE_EDITORIAL_PROJECT,
                    value=normalized,
                    display_name=Path(file_name).name,
                    extension=suffix,
                )

            if suffix in DOCUMENT_EXTENSIONS:
                return InputDescriptor(
                    kind=InputKind.DOCUMENT,
                    value=normalized,
                    display_name=Path(file_name).name,
                    extension=suffix,
                )

            if suffix in AUDIO_EXTENSIONS:
                return InputDescriptor(
                    kind=InputKind.AUDIO,
                    value=normalized,
                    display_name=Path(file_name).name,
                    extension=suffix,
                    notes=(
                        "Processing remains subject to host-platform "
                        "file and size limits.",
                    ),
                )

            if suffix in VIDEO_EXTENSIONS:
                return InputDescriptor(
                    kind=InputKind.VIDEO,
                    value=normalized,
                    display_name=Path(file_name).name,
                    extension=suffix,
                    notes=(
                        "Processing remains subject to host-platform "
                        "file and size limits.",
                    ),
                )

            if suffix in IMAGE_EXTENSIONS:
                return InputDescriptor(
                    kind=InputKind.IMAGE,
                    value=normalized,
                    display_name=Path(file_name).name,
                    extension=suffix,
                )

            if self._looks_like_pasted_text(normalized):
                return InputDescriptor(
                    kind=InputKind.PASTED_TEXT,
                    value=normalized,
                    display_name="Pasted text",
                )

            return InputDescriptor(
                kind=InputKind.PASTED_TEXT,
                value=normalized,
                display_name="Author description",
                notes=(
                    "The material will be treated as an Author "
                    "observation or article idea.",
                ),
            )

        def classify_identity_asset(
            self,
            file_name: str,
            *,
            declared_kind: IdentityAssetKind,
            rights_confirmed: bool,
            usage_preference: str = "subtle",
            included_in_project_export: bool = False,
        ) -> IdentityAsset:
            """Create and validate an optional identity asset."""
            asset = IdentityAsset(
                kind=declared_kind,
                file_name=file_name,
                rights_confirmed=rights_confirmed,
                usage_preference=usage_preference,
                included_in_project_export=(
                    included_in_project_export
                ),
            )

            asset.validate()

            return asset

        def process(
            self,
            value: str,
            *,
            declared_file_name: str | None = None,
            identity_assets: Iterable[IdentityAsset] = (),
        ) -> EditorialIntakeResult:
            """Execute Understanding and Source Assessment."""
            descriptor = self.recognize_input(
                value,
                declared_file_name=declared_file_name,
            )

            assets = list(identity_assets)

            for asset in assets:
                asset.validate()

            assessment = self.assess_source(descriptor)

            stages = [
                WorkspaceStageView(
                    number=1,
                    name=self.STAGE_NAMES[0],
                    state=StageState.COMPLETE,
                    detail=(
                        f"Recognised {descriptor.kind.value}: "
                        f"{descriptor.display_name}"
                    ),
                ),
                WorkspaceStageView(
                    number=2,
                    name=self.STAGE_NAMES[1],
                    state=StageState.COMPLETE,
                    detail=(
                        "Initial source assessment complete. "
                        "Full evidence verification follows in "
                        "Capability 008."
                    ),
                ),
                WorkspaceStageView(
                    number=3,
                    name=self.STAGE_NAMES[2],
                    state=StageState.PENDING,
                ),
                WorkspaceStageView(
                    number=4,
                    name=self.STAGE_NAMES[3],
                    state=StageState.PENDING,
                ),
                WorkspaceStageView(
                    number=5,
                    name=self.STAGE_NAMES[4],
                    state=StageState.PENDING,
                ),
            ]

            findings: list[str] = []

            if descriptor.kind is InputKind.UNKNOWN:
                findings.append(
                    "The supplied material could not be understood."
                )

            if assessment.quality in {
                SourceQuality.LIMITED,
                SourceQuality.UNKNOWN,
            }:
                findings.append(
                    "The current material requires deeper source "
                    "verification before publication."
                )

            if assets:
                findings.append(
                    "Optional identity assets are available for the "
                    "Hero Visual. Brand-neutral generation remains "
                    "available."
                )

            return EditorialIntakeResult(
                descriptor=descriptor,
                stages=stages,
                source_assessment=assessment,
                identity_assets=assets,
                significant_findings=findings,
            )

        def assess_source(
            self,
            descriptor: InputDescriptor,
        ) -> SourceAssessment:
            """Perform an initial source assessment.

            This is intentionally conservative. It does not claim that
            evidence has been independently verified.
            """
            if descriptor.kind is InputKind.URL:
                parsed = urlparse(descriptor.value)
                host = parsed.netloc.lower()
                observations = [
                    "The source URL is identifiable.",
                    "Publication date and authorship require retrieval.",
                    "Important claims require independent verification.",
                ]

                quality = SourceQuality.MODERATE

                if host.endswith(".gov") or host.endswith(".edu"):
                    quality = SourceQuality.HIGH
                    observations.append(
                        "The domain may represent an institutional "
                        "source, but individual claims still require "
                        "review."
                    )

                return SourceAssessment(
                    quality=quality,
                    source_identified=True,
                    publication_date_known=False,
                    primary_source_possible=True,
                    requires_deeper_verification=True,
                    observations=tuple(observations),
                )

            if descriptor.kind in {
                InputKind.DOCUMENT,
                InputKind.PORTABLE_EDITORIAL_PROJECT,
            }:
                return SourceAssessment(
                    quality=SourceQuality.MODERATE,
                    source_identified=True,
                    publication_date_known=False,
                    primary_source_possible=True,
                    requires_deeper_verification=True,
                    observations=(
                        "The supplied file is identifiable.",
                        "Authorship, date, and evidence must be "
                        "derived from its contents.",
                    ),
                )

            if descriptor.kind in {
                InputKind.AUDIO,
                InputKind.VIDEO,
                InputKind.IMAGE,
            }:
                return SourceAssessment(
                    quality=SourceQuality.LIMITED,
                    source_identified=True,
                    publication_date_known=False,
                    primary_source_possible=True,
                    requires_deeper_verification=True,
                    observations=(
                        "The asset may contain primary material.",
                        "Speaker, creator, date, and context require "
                        "confirmation.",
                    ),
                )

            if descriptor.kind is InputKind.PASTED_TEXT:
                return SourceAssessment(
                    quality=SourceQuality.LIMITED,
                    source_identified=False,
                    publication_date_known=False,
                    primary_source_possible=False,
                    requires_deeper_verification=True,
                    observations=(
                        "Pasted text does not establish provenance.",
                        "Material claims require source identification "
                        "and verification.",
                    ),
                )

            return SourceAssessment(
                quality=SourceQuality.UNKNOWN,
                source_identified=False,
                publication_date_known=False,
                primary_source_possible=False,
                requires_deeper_verification=True,
                observations=(
                    "No reliable source assessment can be made yet.",
                ),
            )

        @staticmethod
        def missing_identity_asset_message(
            *,
            logo_was_used: bool,
            headshot_was_used: bool,
        ) -> str:
            """Explain missing optional assets during project resume."""
            missing: list[str] = []

            if logo_was_used:
                missing.append("logo")

            if headshot_was_used:
                missing.append("headshot")

            if not missing:
                return (
                    "No previously used identity assets are missing."
                )

            joined = " and ".join(missing)

            return (
                f"This project previously used a {joined}, but the "
                "original asset was not included. Upload it again, "
                "continue without it, or create a brand-neutral "
                "Hero Visual."
            )

        @staticmethod
        def _is_url(value: str) -> bool:
            parsed = urlparse(value)

            return (
                parsed.scheme in {"http", "https"}
                and bool(parsed.netloc)
            )

        @staticmethod
        def _looks_like_pasted_text(value: str) -> bool:
            return (
                len(value) >= 80
                or "\\n" in value
                or value.count(" ") >= 12
            )
    '''
)


EDITORIAL_INTAKE_INIT = clean(
    '''
    """Capability 007 Editorial Workspace exports."""

    from .editorial_intake import (
        EditorialIntakeResult,
        EditorialWorkspace,
        IdentityAsset,
        IdentityAssetKind,
        InputDescriptor,
        InputKind,
        SourceAssessment,
        SourceQuality,
        StageState,
        WorkspaceStage,
        WorkspaceStageView,
    )

    __all__ = [
        "EditorialIntakeResult",
        "EditorialWorkspace",
        "IdentityAsset",
        "IdentityAssetKind",
        "InputDescriptor",
        "InputKind",
        "SourceAssessment",
        "SourceQuality",
        "StageState",
        "WorkspaceStage",
        "WorkspaceStageView",
    ]
    '''
)


# ---------------------------------------------------------------------
# Constitutional and product documentation
# ---------------------------------------------------------------------

CANONICAL_VOCABULARY = clean(
    """
    # Canonical Vocabulary

    ## Status

    Active constitutional vocabulary for Version 1.0.

    ## Governing Rule

    > One concept. One canonical name.

    Language shapes behaviour.

    Consistent language produces consistent decisions, consistent
    implementation, and a consistent experience for every Author,
    Editor, and Reader.

    ## Engineering Commitment

    > Build once. Name once. Understand everywhere.

    ## Human Roles

    ### Author

    The human who owns:

    - publication intent,
    - expertise,
    - perspective,
    - final editorial decisions,
    - and publication authority.

    Do not use `user`, `client`, or `customer` as substitutes in active
    editorial documentation.

    ### Editor

    The Studio acting as a responsible editorial collaborator.

    Do not use `assistant`, `AI`, `bot`, or `model` as substitutes in
    Author-facing editorial interactions.

    Technical documentation may identify implementation technologies
    where genuinely necessary.

    ### Reader

    The beneficiary of the published work.

    Use `audience` only when describing a target group rather than the
    individual experience of reading.

    ## Product Environment

    ### Editorial Workspace

    The complete Author-facing collaborative environment.

    The Editorial Workspace contains:

    - Editorial Intake,
    - source assessment,
    - evidence verification,
    - editorial judgement,
    - article creation,
    - Hero Visual creation,
    - component collaboration,
    - export,
    - and project resume.

    Editorial Workspace is not a synonym for Editorial Intake.

    ### Editorial Intake

    The first capability executed inside the Editorial Workspace.

    Editorial Intake receives and interprets Author material.

    ## Publication Terms

    ### Publication Package

    The complete Version 1.0 editorial deliverable.

    Do not use `output bundle`, `content package`, or `generated result`
    as active substitutes.

    ### Hero Visual

    The canonical 720 × 425 editorial image.

    Do not use `cover image`, `header image`, `banner`, or `thumbnail`
    as substitutes unless describing an external platform requirement.

    ### Portable Editorial Project

    The Author-owned, human-readable, resumable project record.

    It is not a hosted library or cloud-storage path.

    ## Editorial Quality

    ### Editorial Confidence

    The primary Author-facing publication-readiness conclusion.

    ### LMHS Editorial Risk

    The internal editorial assessment:

    - Low
    - Moderate
    - High
    - Severe

    Editorial Risk may appear as supporting detail.

    It should not replace Editorial Confidence as the main completion
    message.

    ## Workflow Terms

    The five visible Editorial Integrity stages are:

    1. Understanding your input
    2. Assessing your sources
    3. Verifying the evidence
    4. Reviewing editorial risks
    5. Creating your publication package

    ### Canonical Editorial Session

    The Version 1.0 behavioural acceptance demonstration.

    It is not merely a generic workflow diagram.

    ### Component Collaboration

    The process of reviewing and improving one Publication Package
    component while preserving unaffected work.

    ## Identity Assets

    ### Identity Asset

    An optional Author-supplied logo or headshot used in a Hero Visual.

    Identity assets:

    - require rights confirmation,
    - remain optional,
    - Brand-neutral remains the default,
    - do not require hosted storage,
    - and do not block project resume when absent.

    ## Historical and Legacy Language

    Historical documents may preserve former terminology when clearly
    labelled as historical.

    Active documents, runtime code, tests, issues, and demos should use
    canonical terms.

    ## Validation Rule

    New terminology must not be introduced casually.

    A new concept requires:

    - a canonical name,
    - a definition,
    - constitutional-impact review,
    - affected-document updates,
    - and validation where practical.
    """
)


EDITORIAL_WORKSPACE_DOC = clean(
    """
    # Editorial Workspace

    ## Purpose

    The Editorial Workspace is the Author-facing collaborative
    environment for the complete Canonical Editorial Session.

    Editorial Intake is the first capability within the Workspace.

    ## Opening Experience

    The Workspace immediately communicates:

    - what the Author may provide,
    - what the Editor will do,
    - how editorial integrity is reviewed,
    - and that the Author remains in control.

    Suitable opening copy:

    > Create a professional article from almost any source.
    >
    > Every article is reviewed for source quality, factual accuracy,
    > and editorial risk before publication.

    ## Supported Material

    Subject to host-platform support and size limits, the Author may
    provide:

    - Web URL
    - Pasted text
    - PDF
    - Word document
    - PowerPoint presentation
    - Markdown
    - Plain text file
    - Image containing readable text
    - Audio
    - Video
    - Portable Editorial Project
    - Professional observation
    - Article idea

    The Author should not need to classify the material before
    providing it.

    ## Optional Identity Assets

    The Author may optionally provide:

    - a logo,
    - a headshot,
    - or both.

    Brand-neutral Hero Visual creation remains the default.

    Identity assets require a simple confirmation that the Author is
    authorised to use them.

    ## Rights Confirmation

    Suitable confirmation:

    > I confirm that I own this asset or am authorised to use it.

    Rights confirmation is required before an identity asset may be
    incorporated into the Hero Visual.

    ## Storage Boundary

    Identity assets are Author-supplied project inputs.

    The Product:

    - does not require a path,
    - does not require hosted storage,
    - does not require permanent retention,
    - and does not require the asset for later project resume.

    ## Resume Without Assets

    If a Portable Editorial Project records previous logo or headshot
    use but the original asset is absent, the Editor should offer:

    - upload the asset again,
    - continue without it,
    - or create a brand-neutral Hero Visual.

    Missing identity assets never invalidate the project.
    """
)


AUTHOR_CONVERSATION_GUIDE = clean(
    """
    # Author Conversation Guide

    ## Purpose

    This guide defines Author-facing copy for the first part of the
    Canonical Editorial Session.

    It complements the Editorial Language Framework.

    ## Opening

    Example:

    > Welcome.
    >
    > Create a professional article from almost any source.
    >
    > Every article is reviewed for source quality, factual accuracy,
    > and editorial risk before publication.
    >
    > Share a URL, paste text, or upload a document, image, audio
    > recording, video, or Portable Editorial Project supported by the
    > host platform.
    >
    > You remain in control throughout.

    ## Optional Personalisation

    Identity-asset personalisation should not interrupt the intake fast
    path.

    Present it only when the Hero Visual is being prepared or when the
    Author supplies an asset proactively.

    Example:

    > Would you like to personalise the Hero Visual?
    >
    > ○ Keep it brand-neutral
    >
    > ○ Add my logo
    >
    > ○ Add my headshot
    >
    > ○ Add both

    ## Rights Confirmation

    Example:

    > Before I use this asset, please confirm:
    >
    > ○ I own it or am authorised to use it
    >
    > ○ Continue without this asset

    ## Stage 1

    Label:

    > Understanding your input

    Example detail:

    > I have recognised this as a web article about workplace policy.

    Do not say:

    - Processing your prompt
    - Running the model
    - Analysing tokens

    ## Stage 2

    Label:

    > Assessing your sources

    Example detail:

    > The source is identifiable. I am checking authorship, date,
    > supporting evidence, and whether the important claims need
    > independent corroboration.

    ## Significant Finding

    Example:

    > I found one point that needs attention.
    >
    > The source is identifiable, but the main statistic is not linked
    > to its original research. I can continue, but it will need deeper
    > verification before publication.

    ## Missing Asset on Resume

    Example:

    > This project previously used a logo, but the original asset was
    > not included.
    >
    > ○ Upload it again
    >
    > ○ Continue without it
    >
    > ○ Create a brand-neutral Hero Visual
    """
)


EDITORIAL_CONFIDENCE_STAGES = clean(
    """
    # Editorial Confidence Stages

    ## Purpose

    The Editorial Workspace displays the five stages of the Editorial
    Integrity Pipeline.

    Editorial Confidence is the eventual Author-facing outcome.

    ## Visible Stages

    1. Understanding your input
    2. Assessing your sources
    3. Verifying the evidence
    4. Reviewing editorial risks
    5. Creating your publication package

    ## Capability 007 Boundary

    Capability 007 implements:

    - Stage 1 - Understanding your input
    - Stage 2 - Assessing your sources

    Stages 3 through 5 remain visible but pending.

    ## Stage States

    Each stage may be:

    - Pending
    - Active
    - Complete
    - Blocked

    ## Presentation Example

    ```text
    Editorial Integrity Pipeline

    ✓ Understanding your input
    ✓ Assessing your sources
    ○ Verifying the evidence
    ○ Reviewing editorial risks
    ○ Creating your publication package
    ```

    ## Significant Findings

    Routine observations remain concise.

    A finding interrupts only when it materially affects:

    - provenance,
    - source quality,
    - future verification,
    - Author effort,
    - professional reputation,
    - or Reader trust.

    ## No False Completion

    Completion of Stage 2 must not imply that evidence has been fully
    verified.

    Full evidence verification belongs to Capability 008.
    """
)


EDITORIAL_INTAKE_ARCHITECTURE = clean(
    """
    # Editorial Intake Runtime

    ## Status

    Active runtime architecture for Capability 007.

    ## Purpose

    Editorial Intake is the first capability executed within the
    Editorial Workspace.

    It receives Author material, identifies the input type, extracts
    available context, and prepares the project for source assessment.

    ## Input Recognition

    The runtime recognises:

    - URL
    - Pasted text
    - Document
    - Image
    - Audio
    - Video
    - Portable Editorial Project
    - Author observation or idea

    Input recognition is deterministic where a filename or URL provides
    sufficient evidence.

    ## No Classification Burden

    The Author should not need to choose a technical input type before
    submitting material.

    ## Host Boundary

    File-format availability and size limits depend on the host
    platform.

    The Product should describe those constraints honestly rather than
    claiming universal upload support.

    ## Optional Identity Assets

    Logo and headshot assets are separate optional inputs.

    They do not change the classification of the main editorial source.

    ## Identity-Asset Rules

    - Brand-neutral is the default.
    - Rights confirmation is mandatory before use.
    - The Author may supply logo, headshot, or both.
    - Assets are not required for article creation.
    - Assets are not required for project resume.
    - The Product does not require asset storage paths.
    - Headshots should preserve recognisability.
    - Logos should not overpower the editorial concept unless requested.

    ## Runtime Output

    Editorial Intake produces:

    - canonical input classification,
    - display name,
    - relevant extension,
    - host-limit notes,
    - optional identity-asset metadata,
    - and Stage 1 completion detail.

    ## Error Behaviour

    Empty or unusable input returns an Unknown classification.

    The runtime should explain the limitation and request only the
    minimum information needed to continue.
    """
)


SOURCE_ASSESSMENT_ARCHITECTURE = clean(
    """
    # Source Assessment Runtime

    ## Status

    Active runtime architecture for Capability 007.

    ## Purpose

    Source Assessment performs the first editorial evaluation of
    supplied material.

    Source Assessment is not Evidence Verification.

    ## Assessment Dimensions

    Capability 007 may assess:

    - whether a source is identifiable,
    - whether provenance is available,
    - whether a date is known,
    - whether primary material may be present,
    - whether authorship requires extraction,
    - and whether deeper verification is required.

    ## Source Quality

    Initial source quality uses:

    - High
    - Moderate
    - Limited
    - Unknown

    These labels are preliminary.

    They must not be presented as proof that the source is accurate.

    ## Conservative Default

    Material claims require deeper verification unless verification has
    actually occurred.

    URLs, pasted text, files, recordings, and images must not be treated
    as self-validating.

    ## Progressive Recovery

    If a URL is inaccessible or a source is incomplete, the Editor
    should use reliable material already supplied before requesting
    more Author effort.

    ## Capability Boundary

    Capability 007 completes Stage 2.

    Capability 008 performs:

    - claim extraction,
    - corroboration,
    - evidence comparison,
    - temporal review,
    - and LMHS Editorial Risk.
    """
)


ADR_007 = clean(
    """
    # ADR-007 - Implement Editorial Workspace Intake Runtime

    ## Status

    Accepted

    ## Date

    2026-08-01

    ## Context

    The Constitutional Freeze defines the complete Author, Editor, and
    Reader relationship, but the repository still requires an
    executable beginning to the Canonical Editorial Session.

    The Author must be able to provide natural material without
    navigating a technical intake wizard.

    Version 1.0 must also support optional logo and headshot assets
    without weakening:

    - brand-neutral defaults,
    - stateless operation,
    - Author ownership,
    - privacy,
    - or project resumption.

    ## Decision

    Implement the Editorial Workspace as the Author-facing environment.

    Implement Editorial Intake as the first capability within that
    Workspace.

    Capability 007 implements:

    1. Understanding your input
    2. Assessing your sources

    ## Canonical Vocabulary

    Adopt:

    - Editorial Workspace - complete Author-facing environment
    - Editorial Intake - first capability within the Workspace
    - Identity Asset - optional Author-supplied logo or headshot

    ## Identity Assets

    Identity assets:

    - remain optional,
    - require rights confirmation,
    - do not replace brand-neutral defaults,
    - do not require Product-managed storage,
    - and do not block resume when absent.

    ## Source Assessment Boundary

    Capability 007 provides initial source assessment.

    It must not imply full evidence verification.

    ## Consequences

    ### Positive

    - Creates the first runnable Canonical Editorial Session behaviour
    - Reduces Author classification effort
    - Establishes consistent Workspace language
    - Supports future Hero Visual personalisation
    - Preserves stateless product architecture
    - Creates a testable boundary before evidence validation

    ### Costs

    - Requires conservative source-quality language
    - Requires host-platform capability awareness
    - Requires identity-asset rights confirmation
    - Requires later integration with evidence validation

    ## Alternatives Rejected

    ### Require the Author to Select an Input Type

    Rejected because the Editor should infer before asking.

    ### Store Identity Assets Automatically

    Rejected because Version 1.0 is stateless by default.

    ### Treat Source Assessment as Verification

    Rejected because source identity and apparent quality do not prove
    factual accuracy.
    """
)


ARCHITECTURE_BASELINE = clean(
    f"""
    # Architecture Baseline - {ARCHITECTURE_BASELINE_VERSION}

    ## Status

    Current Version 1.0 implementation baseline.

    ## Baseline ID

    ```text
    {ARCHITECTURE_BASELINE_VERSION}
    ```

    ## Baseline Family

    ```text
    2026.08.01
    ```

    ## Supersedes

    ```text
    2026.08.01v02
    ```

    ## Reason for Revision

    Begin Version 1.0 runtime implementation.

    Establish:

    - Canonical Vocabulary
    - Editorial Workspace
    - Editorial Intake runtime
    - Source Assessment runtime
    - Optional identity assets
    - Rights confirmation
    - First two visible Editorial Integrity stages

    ## Constitutional Impact

    This baseline adds a canonical vocabulary without changing the
    trust-first Constitution.

    It clarifies that:

    - Editorial Workspace is the complete Author-facing environment.
    - Editorial Intake is the first capability inside the Workspace.
    - Identity Asset means an optional logo or headshot.

    ## Runtime Boundary

    Capability 007 implements:

    - Understanding your input
    - Assessing your sources

    Capability 008 implements:

    - Verifying the evidence
    - Reviewing editorial risks
    - Editorial Confidence translation

    ## Identity Assets

    Brand-neutral remains the default.

    Logo and headshot assets:

    - require rights confirmation,
    - remain Author-controlled,
    - are not required for resume,
    - and do not create a hosted-storage dependency.

    ## VCM

    The same baseline family date remains in use.

    The revision advances to `v03`.
    """
)


CAPABILITY_DEMO = clean(
    """
    # Capability 007 Demo - Editorial Intake and Source Assessment

    ## Objective

    Demonstrate the first executable portion of the Canonical Editorial
    Session.

    ## Scenario 1 - Welcome

    The Author opens the Editorial Workspace.

    The Workspace explains:

    - what may be supplied,
    - what the Editor will do,
    - the five visible stages,
    - and that the Author remains in control.

    ## Scenario 2 - URL

    Input:

    ```text
    https://example.org/article
    ```

    Expected:

    - Input classified as URL
    - Stage 1 complete
    - Stage 2 complete
    - Deeper verification required
    - Stages 3 through 5 pending

    ## Scenario 3 - Pasted Text

    Expected:

    - Input classified as Pasted Text
    - Provenance marked as incomplete
    - Deeper verification required
    - Author is not forced to choose an input type

    ## Scenario 4 - Audio

    Input:

    ```text
    interview.m4a
    ```

    Expected:

    - Input classified as Audio
    - Host-platform limit note preserved
    - Speaker, date, and context identified as requiring review

    ## Scenario 5 - Optional Logo

    The Author supplies a logo.

    Expected:

    - Rights confirmation required
    - Brand-neutral path remains available
    - No storage path requested

    ## Scenario 6 - Optional Headshot

    The Author supplies a headshot.

    Expected:

    - Rights confirmation required
    - Recognisability must be preserved
    - Asset remains optional

    ## Scenario 7 - Resume Without Asset

    A Portable Editorial Project records previous logo use but does not
    include the logo.

    Expected response:

    - Upload again
    - Continue without it
    - Create a brand-neutral Hero Visual

    The project remains valid.

    ## Completion

    Capability 007 is complete when:

    - runtime tests pass,
    - Stage 1 and Stage 2 are executable,
    - the Editorial Workspace vocabulary is consistent,
    - identity assets are optional and governed,
    - and full evidence verification is not falsely claimed.
    """
)


# ---------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------

CAPABILITY_TEST = clean(
    '''
    """Runtime tests for Capability 007."""

    from __future__ import annotations

    import unittest

    from studio.editorial_intake import (
        EditorialWorkspace,
        IdentityAssetKind,
        InputKind,
        SourceQuality,
        StageState,
    )


    class Capability007RuntimeTests(unittest.TestCase):
        def setUp(self) -> None:
            self.workspace = EditorialWorkspace()

        def test_welcome_uses_editorial_workspace_language(
            self,
        ) -> None:
            message = self.workspace.welcome_message()

            self.assertIn(
                "Create a professional article",
                message,
            )
            self.assertIn(
                "Every article is reviewed",
                message,
            )
            self.assertIn(
                "You remain in control",
                message,
            )

        def test_welcome_supports_optional_name(self) -> None:
            message = self.workspace.welcome_message(
                "Nilesh"
            )

            self.assertIn(
                "Welcome back, Nilesh.",
                message,
            )

        def test_url_is_recognised(self) -> None:
            descriptor = self.workspace.recognize_input(
                "https://example.org/article"
            )

            self.assertEqual(
                descriptor.kind,
                InputKind.URL,
            )

        def test_document_is_recognised(self) -> None:
            descriptor = self.workspace.recognize_input(
                "research.pdf",
                declared_file_name="research.pdf",
            )

            self.assertEqual(
                descriptor.kind,
                InputKind.DOCUMENT,
            )

        def test_audio_is_recognised(self) -> None:
            descriptor = self.workspace.recognize_input(
                "interview.m4a",
                declared_file_name="interview.m4a",
            )

            self.assertEqual(
                descriptor.kind,
                InputKind.AUDIO,
            )
            self.assertTrue(descriptor.notes)

        def test_video_is_recognised(self) -> None:
            descriptor = self.workspace.recognize_input(
                "meeting.mp4",
                declared_file_name="meeting.mp4",
            )

            self.assertEqual(
                descriptor.kind,
                InputKind.VIDEO,
            )

        def test_portable_project_is_recognised(self) -> None:
            descriptor = self.workspace.recognize_input(
                "Ramrattan-Editorial-Project_Test_"
                "2026.08.01v01.md",
                declared_file_name=(
                    "Ramrattan-Editorial-Project_Test_"
                    "2026.08.01v01.md"
                ),
            )

            self.assertEqual(
                descriptor.kind,
                InputKind.PORTABLE_EDITORIAL_PROJECT,
            )

        def test_pasted_text_is_recognised(self) -> None:
            descriptor = self.workspace.recognize_input(
                "This is a sufficiently detailed professional "
                "observation that should be treated as pasted text "
                "without requiring the Author to classify it first."
            )

            self.assertEqual(
                descriptor.kind,
                InputKind.PASTED_TEXT,
            )

        def test_stage_one_and_two_complete(self) -> None:
            result = self.workspace.process(
                "https://example.org/article"
            )

            self.assertEqual(
                result.stages[0].state,
                StageState.COMPLETE,
            )
            self.assertEqual(
                result.stages[1].state,
                StageState.COMPLETE,
            )

            for stage in result.stages[2:]:
                self.assertEqual(
                    stage.state,
                    StageState.PENDING,
                )

        def test_source_assessment_does_not_claim_verification(
            self,
        ) -> None:
            result = self.workspace.process(
                "https://example.org/article"
            )

            self.assertTrue(
                result.source_assessment
                .requires_deeper_verification
            )

        def test_pasted_text_has_limited_provenance(
            self,
        ) -> None:
            result = self.workspace.process(
                "This is a detailed but unattributed passage "
                "containing claims that require independent "
                "verification before publication."
            )

            self.assertEqual(
                result.source_assessment.quality,
                SourceQuality.LIMITED,
            )
            self.assertFalse(
                result.source_assessment.source_identified
            )

        def test_brand_neutral_is_default(self) -> None:
            result = self.workspace.process(
                "https://example.org/article"
            )

            self.assertTrue(result.brand_neutral)

        def test_logo_requires_rights_confirmation(
            self,
        ) -> None:
            with self.assertRaises(ValueError):
                self.workspace.classify_identity_asset(
                    "logo.png",
                    declared_kind=IdentityAssetKind.LOGO,
                    rights_confirmed=False,
                )

        def test_headshot_requires_supported_image(
            self,
        ) -> None:
            with self.assertRaises(ValueError):
                self.workspace.classify_identity_asset(
                    "headshot.pdf",
                    declared_kind=IdentityAssetKind.HEADSHOT,
                    rights_confirmed=True,
                )

        def test_logo_can_be_added(self) -> None:
            logo = self.workspace.classify_identity_asset(
                "logo.png",
                declared_kind=IdentityAssetKind.LOGO,
                rights_confirmed=True,
            )

            result = self.workspace.process(
                "https://example.org/article",
                identity_assets=[logo],
            )

            self.assertFalse(result.brand_neutral)
            self.assertEqual(
                result.identity_assets[0].kind,
                IdentityAssetKind.LOGO,
            )

        def test_resume_without_logo_remains_possible(
            self,
        ) -> None:
            message = (
                self.workspace.missing_identity_asset_message(
                    logo_was_used=True,
                    headshot_was_used=False,
                )
            )

            self.assertIn(
                "upload it again",
                message.lower(),
            )
            self.assertIn(
                "brand-neutral",
                message,
            )

        def test_empty_input_is_unknown(self) -> None:
            descriptor = self.workspace.recognize_input(
                "   "
            )

            self.assertEqual(
                descriptor.kind,
                InputKind.UNKNOWN,
            )


    if __name__ == "__main__":
        unittest.main()
    '''
)


VOCABULARY_TEST = clean(
    '''
    """Documentation tests for Capability 007 canonical vocabulary."""

    from __future__ import annotations

    import unittest
    from pathlib import Path


    ROOT = Path(__file__).resolve().parents[1]


    def normalized(relative: str) -> str:
        content = (
            ROOT / relative
        ).read_text(encoding="utf-8")

        return " ".join(
            content.replace(">", " ").split()
        )


    class Capability007VocabularyTests(unittest.TestCase):
        def test_canonical_vocabulary_exists(self) -> None:
            self.assertTrue(
                (
                    ROOT
                    / "docs"
                    / "constitution"
                    / "Canonical_Vocabulary.md"
                ).is_file()
            )

        def test_one_concept_one_name_rule_exists(
            self,
        ) -> None:
            content = normalized(
                "docs/constitution/Canonical_Vocabulary.md"
            )

            self.assertIn(
                "One concept. One canonical name.",
                content,
            )

        def test_workspace_and_intake_are_distinct(
            self,
        ) -> None:
            content = normalized(
                "docs/constitution/Canonical_Vocabulary.md"
            )

            self.assertIn(
                "Editorial Workspace is not a synonym "
                "for Editorial Intake",
                content,
            )

        def test_identity_asset_is_defined(self) -> None:
            content = normalized(
                "docs/constitution/Canonical_Vocabulary.md"
            )

            self.assertIn(
                "An optional Author-supplied logo or headshot",
                content,
            )

        def test_brand_neutral_remains_default(self) -> None:
            content = normalized(
                "docs/ui/Editorial_Workspace.md"
            )

            self.assertIn(
                "Brand-neutral Hero Visual creation remains "
                "the default",
                content,
            )

        def test_rights_confirmation_is_required(
            self,
        ) -> None:
            content = normalized(
                "docs/ui/Editorial_Workspace.md"
            )

            self.assertIn(
                "Rights confirmation is required",
                content,
            )

        def test_baseline_v03_exists(self) -> None:
            self.assertTrue(
                (
                    ROOT
                    / "docs"
                    / "architecture"
                    / "baselines"
                    / "Architecture_Baseline_2026.08.01v03.md"
                ).is_file()
            )

        def test_adr_007_exists(self) -> None:
            self.assertTrue(
                (
                    ROOT
                    / "docs"
                    / "architecture"
                    / "adr"
                    / "ADR-007-editorial-intake-runtime.md"
                ).is_file()
            )


    if __name__ == "__main__":
        unittest.main()
    '''
)


# ---------------------------------------------------------------------
# Managed updates
# ---------------------------------------------------------------------

START_HERE_BLOCK = clean(
    """
    ## Canonical Vocabulary

    Read:

    - `constitution/Canonical_Vocabulary.md`

    before introducing new product, architecture, runtime, test, demo,
    or user-facing terminology.

    Governing rule:

    > One concept. One canonical name.

    Engineering commitment:

    > Build once. Name once. Understand everywhere.
    """
)


CONSTITUTION_BLOCK = clean(
    """
    ## Language Shapes Behaviour

    Language shapes behaviour.

    Consistent language produces consistent decisions, consistent
    implementation, and a consistent experience for every Author,
    Editor, and Reader.

    Active documentation and runtime behaviour must follow the
    Canonical Vocabulary.

    Governing rule:

    > One concept. One canonical name.
    """
)


DECISION_REGISTER_BLOCK = clean(
    """
    ## Capability 007 Constitutional Decisions

    | Decision | Status | Adopted | Primary Evidence |
    |---|---|---|---|
    | One concept has one canonical name | Accepted | 2026-08-01 | Canonical Vocabulary |
    | Editorial Workspace is the Author-facing environment | Accepted | 2026-08-01 | Canonical Vocabulary, ADR-007 |
    | Editorial Intake is the first Workspace capability | Accepted | 2026-08-01 | Canonical Vocabulary, ADR-007 |
    | Identity Asset means optional logo or headshot | Accepted | 2026-08-01 | Canonical Vocabulary |
    | Brand-neutral remains the default | Accepted | 2026-08-01 | Editorial Workspace |
    | Identity assets require rights confirmation | Accepted | 2026-08-01 | Editorial Workspace, ADR-007 |
    | Missing identity assets do not block resume | Accepted | 2026-08-01 | Editorial Workspace |
    """
)


README_BLOCK = clean(
    """
    ## Capability 007 - Editorial Workspace Runtime

    Capability 007 begins Version 1.0 runtime implementation.

    The Editorial Workspace now supports:

    - natural input recognition,
    - Stage 1 - Understanding your input,
    - Stage 2 - Assessing your sources,
    - optional logo and headshot identity assets,
    - rights confirmation,
    - and brand-neutral Hero Visual defaults.

    Editorial Workspace is the complete Author-facing environment.

    Editorial Intake is the first capability within that Workspace.

    Canonical terminology is defined in:

    - `docs/constitution/Canonical_Vocabulary.md`
    """
)


CURRENT_FOCUS_BLOCK = clean(
    """
    ## Capability 007 Active Focus

    The current implementation focus is the beginning of the Canonical
    Editorial Session:

    - Editorial Workspace welcome experience
    - Natural Editorial Intake
    - Understanding your input
    - Assessing your sources
    - Optional identity assets
    - Rights confirmation
    - Brand-neutral defaults
    - Resume without missing assets

    Full evidence verification remains Capability 008.
    """
)


PRODUCT_PRINCIPLES_BLOCK = clean(
    """
    ## Canonical Language

    Use one canonical name for each active concept.

    Editorial Workspace and Editorial Intake are related but distinct:

    - Editorial Workspace - complete Author-facing environment
    - Editorial Intake - first capability inside the Workspace

    ## Optional Identity Assets

    Logo and headshot assets:

    - remain optional,
    - require rights confirmation,
    - never replace the brand-neutral default,
    - and never create a hosted-storage requirement.
    """
)


STUDIO_CONTRACT_BLOCK = clean(
    """
    ## Editorial Workspace Contract

    The Editor will:

    - accept natural material without forcing technical classification,
    - identify what was supplied,
    - explain the first two Editorial Integrity stages,
    - distinguish source assessment from evidence verification,
    - and preserve the Author's control.

    ## Identity-Asset Contract

    The Editor will not use a logo or headshot without confirmation that
    the Author owns it or is authorised to use it.

    Identity assets remain optional.

    Missing assets do not invalidate a Portable Editorial Project.
    """
)


PRD_BLOCK = clean(
    """
    ## Capability 007 Runtime Requirements

    Version 1.0 shall provide an Editorial Workspace that:

    - explains supported input formats,
    - recognises natural Author input,
    - completes Understanding your input,
    - completes Assessing your sources,
    - keeps later stages visible but pending,
    - and does not falsely imply evidence verification.

    ## Optional Hero Visual Identity Assets

    The Author may optionally provide:

    - logo,
    - headshot,
    - or both.

    Requirements:

    - brand-neutral remains the default,
    - rights confirmation is required,
    - headshot recognisability should be preserved,
    - assets remain Author-controlled,
    - no storage path is required,
    - and resume remains possible without the original asset.
    """
)


RELEASE_BLOCK = clean(
    """
    ## Capability 007 Release Contribution

    Capability 007 delivers the first executable Version 1.0
    Editorial Workspace behaviours:

    - welcome experience,
    - natural Editorial Intake,
    - input recognition,
    - source assessment,
    - first two visible stages,
    - and optional Hero Visual identity assets.

    It does not deliver full evidence verification.
    """
)


ROADMAP_BLOCK = clean(
    """
    ## Capability 007 - Editorial Intake and Source Assessment

    Status:

    ```text
    In implementation
    ```

    Runtime scope:

    - [x] Canonical Vocabulary
    - [x] Editorial Workspace definition
    - [x] Natural input recognition
    - [x] Stage 1 - Understanding your input
    - [x] Stage 2 - Assessing your sources
    - [x] Optional logo intake
    - [x] Optional headshot intake
    - [x] Rights confirmation
    - [x] Brand-neutral default
    - [x] Resume without missing identity assets
    - [x] Runtime tests
    - [x] Capability demo

    Capability 008 continues with evidence validation and LMHS
    Editorial Risk.
    """
)


CHANGELOG_BLOCK = clean(
    f"""
    ## Capability 007 - Editorial Workspace Runtime

    ### Added

    - Canonical Vocabulary
    - Editorial Workspace runtime
    - Editorial Intake runtime
    - Natural input recognition
    - Initial source assessment
    - Stage 1 - Understanding your input
    - Stage 2 - Assessing your sources
    - Optional logo identity asset
    - Optional headshot identity asset
    - Identity-asset rights confirmation
    - Resume guidance for missing identity assets
    - ADR-007
    - Architecture Baseline {ARCHITECTURE_BASELINE_VERSION}
    - Runtime tests
    - Capability 007 demo

    ### Changed

    - Established Editorial Workspace as the complete Author-facing
      environment
    - Established Editorial Intake as the first Workspace capability
    - Preserved brand-neutral Hero Visual creation as the default
    - Clarified that source assessment does not equal evidence
      verification
    - Added canonical vocabulary governance
    """
)


DEFINITION_OF_DONE_BLOCK = clean(
    """
    ## Capability 007 Completion Additions

    Before Capability 007 is Done, confirm:

    - Editorial Workspace terminology is canonical.
    - Editorial Intake is not presented as the complete Workspace.
    - Supported inputs are described honestly.
    - Stage 1 and Stage 2 are executable.
    - Stages 3 through 5 remain pending.
    - Source assessment does not claim verification.
    - Identity assets remain optional.
    - Rights confirmation is enforced.
    - Brand-neutral remains the default.
    - Missing identity assets do not block resume.
    - Runtime and documentation tests pass.
    """
)


GLOSSARY_BLOCK = clean(
    """
    ## Editorial Workspace

    The complete Author-facing collaborative environment for the
    Canonical Editorial Session.

    ## Editorial Intake

    The first capability within the Editorial Workspace.

    It receives and interprets Author material.

    ## Identity Asset

    An optional Author-supplied logo or headshot used in a Hero Visual.

    Identity assets require rights confirmation and do not create a
    hosted-storage dependency.

    ## Source Assessment

    An initial evaluation of provenance, identifiability, freshness,
    and verification needs.

    Source Assessment is not Evidence Verification.
    """
)


DECISION_LOG_BLOCK = clean(
    f"""
    ## Capability 007 Decisions

    | Date | Level | Decision | Rationale |
    |---|---:|---|---|
    | 2026-08-01 | D4 | Adopt Canonical Vocabulary | One concept should have one active name. |
    | 2026-08-01 | D4 | Establish Editorial Workspace | The Author needs one coherent environment across the Canonical Editorial Session. |
    | 2026-08-01 | D4 | Define Editorial Intake as the first Workspace capability | Intake is a capability, not the complete experience. |
    | 2026-08-01 | D3 | Infer input type before asking | The Author should not manage technical classification. |
    | 2026-08-01 | D4 | Support optional logo and headshot assets | Authors may personalise Hero Visuals without changing the default path. |
    | 2026-08-01 | D4 | Require identity-asset rights confirmation | The Studio should not use assets without Author authority. |
    | 2026-08-01 | D4 | Preserve brand-neutral as the default | Identity assets are enhancements, not requirements. |
    | 2026-08-01 | D4 | Permit resume without original identity assets | Portable projects must not depend on separately stored binary assets. |
    | 2026-08-01 | D4 | Create Architecture Baseline {ARCHITECTURE_BASELINE_VERSION} | Version 1.0 runtime implementation begins. |
    """
)


SCORECARD_BLOCK = clean(
    """
    ## Capability 007 Progress

    | Area | Status | Evidence |
    |---|---|---|
    | Canonical Vocabulary | Complete | `docs/constitution/Canonical_Vocabulary.md` |
    | Editorial Workspace | Complete | `studio/editorial_intake.py` |
    | Natural Editorial Intake | Complete | Runtime tests |
    | Understanding your input | Complete | Runtime tests |
    | Assessing your sources | Complete | Runtime tests |
    | Optional logo | Complete | Runtime tests |
    | Optional headshot | Complete | Runtime tests |
    | Rights confirmation | Complete | Runtime tests |
    | Resume without assets | Complete | Runtime tests |
    | Evidence verification | Planned | Capability 008 |
    """
)


MARKER_BLOCKS = {
    "docs/START_HERE.md": (
        "CAPABILITY_007_START_HERE",
        START_HERE_BLOCK,
    ),
    "docs/constitution/Constitution.md": (
        "CAPABILITY_007_CONSTITUTION",
        CONSTITUTION_BLOCK,
    ),
    (
        "docs/constitution/"
        "Constitutional_Decision_Register.md"
    ): (
        "CAPABILITY_007_DECISION_REGISTER",
        DECISION_REGISTER_BLOCK,
    ),
    "README.md": (
        "CAPABILITY_007_README",
        README_BLOCK,
    ),
    "docs/product/Current_Product_Focus.md": (
        "CAPABILITY_007_CURRENT_FOCUS",
        CURRENT_FOCUS_BLOCK,
    ),
    "docs/product/Product_Principles.md": (
        "CAPABILITY_007_PRODUCT_PRINCIPLES",
        PRODUCT_PRINCIPLES_BLOCK,
    ),
    "docs/product/Studio_Contract.md": (
        "CAPABILITY_007_STUDIO_CONTRACT",
        STUDIO_CONTRACT_BLOCK,
    ),
    "docs/product/PRD_v1.3.md": (
        "CAPABILITY_007_PRD",
        PRD_BLOCK,
    ),
    "docs/product/Release_v1.0.md": (
        "CAPABILITY_007_RELEASE",
        RELEASE_BLOCK,
    ),
    "docs/product/Glossary.md": (
        "CAPABILITY_007_GLOSSARY",
        GLOSSARY_BLOCK,
    ),
    "docs/product/Decision_Log.md": (
        "CAPABILITY_007_DECISION_LOG",
        DECISION_LOG_BLOCK,
    ),
    "docs/architecture/Definition_of_Done.md": (
        "CAPABILITY_007_DEFINITION_OF_DONE",
        DEFINITION_OF_DONE_BLOCK,
    ),
    "docs/VERSION_ONE_SCORECARD.md": (
        "CAPABILITY_007_SCORECARD",
        SCORECARD_BLOCK,
    ),
    "ROADMAP.md": (
        "CAPABILITY_007_ROADMAP",
        ROADMAP_BLOCK,
    ),
    "CHANGELOG.md": (
        "CAPABILITY_007_CHANGELOG",
        CHANGELOG_BLOCK,
    ),
}


NEW_FILES = {
    "studio/editorial_intake.py":
        EDITORIAL_INTAKE_RUNTIME,

    "studio/editorial_workspace.py":
        EDITORIAL_INTAKE_INIT,

    "docs/constitution/Canonical_Vocabulary.md":
        CANONICAL_VOCABULARY,

    "docs/ui/Editorial_Workspace.md":
        EDITORIAL_WORKSPACE_DOC,

    "docs/ui/Author_Conversation_Guide.md":
        AUTHOR_CONVERSATION_GUIDE,

    "docs/ui/Editorial_Confidence_Stages.md":
        EDITORIAL_CONFIDENCE_STAGES,

    "docs/architecture/Editorial_Intake_Runtime.md":
        EDITORIAL_INTAKE_ARCHITECTURE,

    "docs/architecture/Source_Assessment_Runtime.md":
        SOURCE_ASSESSMENT_ARCHITECTURE,

    (
        "docs/architecture/adr/"
        "ADR-007-editorial-intake-runtime.md"
    ):
        ADR_007,

    (
        "docs/architecture/baselines/"
        "Architecture_Baseline_2026.08.01v03.md"
    ):
        ARCHITECTURE_BASELINE,

    (
        "docs/demos/"
        "Capability-007-Editorial-Intake-and-Source-Assessment.md"
    ):
        CAPABILITY_DEMO,

    "tests/test_capability007_editorial_intake.py":
        CAPABILITY_TEST,

    "tests/test_capability007_vocabulary.py":
        VOCABULARY_TEST,
}


# ---------------------------------------------------------------------
# Errors and command execution
# ---------------------------------------------------------------------

class CapabilityError(RuntimeError):
    """Raised when Capability 007 cannot proceed safely."""


def run(
    command: list[str],
    *,
    cwd: Path,
    capture: bool = False,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    """Run and display a command."""
    print("$", " ".join(command))

    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=capture,
        check=check,
    )


def output(
    command: list[str],
    *,
    cwd: Path,
) -> str:
    """Return stripped command output."""
    return run(
        command,
        cwd=cwd,
        capture=True,
    ).stdout.strip()


def json_output(
    command: list[str],
    *,
    cwd: Path,
) -> Any:
    """Run a command and parse its JSON output."""
    raw = output(command, cwd=cwd)

    if not raw:
        return {}

    return json.loads(raw)


# ---------------------------------------------------------------------
# Repository checks
# ---------------------------------------------------------------------

def repository_root() -> Path:
    """Locate and verify the expected repository."""
    try:
        root = Path(
            output(
                ["git", "rev-parse", "--show-toplevel"],
                cwd=Path.cwd(),
            )
        ).resolve()

    except (
        FileNotFoundError,
        subprocess.CalledProcessError,
    ) as exc:
        raise CapabilityError(
            "Run this script from inside the cloned repository."
        ) from exc

    if root.name != EXPECTED_REPOSITORY:
        raise CapabilityError(
            f"Expected repository '{EXPECTED_REPOSITORY}', "
            f"found '{root.name}'."
        )

    remote = output(
        ["git", "remote", "get-url", "origin"],
        cwd=root,
    )

    if EXPECTED_REMOTE_FRAGMENT not in remote:
        raise CapabilityError(
            "The origin remote does not match the expected repository."
        )

    return root


def verify_branch(root: Path) -> None:
    """Require the Capability 007 feature branch."""
    branch = output(
        ["git", "branch", "--show-current"],
        cwd=root,
    )

    print(f"Branch: {branch}")

    if branch != EXPECTED_BRANCH:
        raise CapabilityError(
            f"Expected branch '{EXPECTED_BRANCH}', "
            f"found '{branch}'."
        )


def verify_script_integrity() -> None:
    """Detect an incomplete or damaged paste."""
    path = Path(__file__).resolve()
    content = path.read_text(encoding="utf-8")

    if SCRIPT_SENTINEL not in content:
        raise CapabilityError(
            "The script appears incomplete. "
            "The final integrity sentinel is missing."
        )

    try:
        compile(
            content,
            str(path),
            "exec",
        )
    except SyntaxError as exc:
        raise CapabilityError(
            f"The pasted script is not syntactically complete: {exc}"
        ) from exc

    print("Script integrity check passed.")


def working_tree_lines(root: Path) -> list[str]:
    """Return Git porcelain lines with complete untracked paths."""
    result = run(
        [
            "git",
            "status",
            "--porcelain",
            "--untracked-files=all",
        ],
        cwd=root,
        capture=True,
    )

    return [
        line
        for line in result.stdout.splitlines()
        if line.strip()
    ]


def verify_expected_working_tree(root: Path) -> None:
    """Permit only expected Capability 007 changes."""
    expected_paths = (
        set(NEW_FILES)
        | set(MARKER_BLOCKS)
        | {SCRIPT_RELATIVE_PATH}
    )

    unexpected: list[str] = []

    for line in working_tree_lines(root):
        relative = line[3:].strip()

        if " -> " in relative:
            relative = relative.split(" -> ", 1)[1].strip()

        if relative not in expected_paths:
            unexpected.append(line)

    if unexpected:
        raise CapabilityError(
            "Unexpected working-tree changes exist:\n"
            + "\n".join(unexpected)
            + "\n\nOnly expected Capability 007 files and "
            "managed-document updates are allowed."
        )

    print(
        "Working tree contains only expected "
        "Capability 007 changes."
    )


# ---------------------------------------------------------------------
# File operations
# ---------------------------------------------------------------------

def managed_block(
    marker_name: str,
    content: str,
) -> str:
    """Create one marker-managed Markdown block."""
    start = f"<!-- {marker_name}_START -->"
    end = f"<!-- {marker_name}_END -->"

    return (
        start
        + "\n\n"
        + content.rstrip()
        + "\n\n"
        + end
    )


def upsert_managed_block(
    path: Path,
    marker_name: str,
    content: str,
) -> None:
    """Insert or replace one managed Markdown block."""
    if not path.is_file():
        raise CapabilityError(
            f"Missing required existing document: {path}"
        )

    original = path.read_text(encoding="utf-8")

    start = f"<!-- {marker_name}_START -->"
    end = f"<!-- {marker_name}_END -->"

    has_start = start in original
    has_end = end in original

    if has_start != has_end:
        raise CapabilityError(
            f"Incomplete managed marker pair in {path}."
        )

    block = managed_block(
        marker_name,
        content,
    )

    if has_start:
        before = original.split(start, 1)[0].rstrip()
        after = original.split(end, 1)[1].lstrip()

        updated = before + "\n\n" + block

        if after:
            updated += "\n\n" + after

        updated = updated.rstrip() + "\n"

    else:
        updated = (
            original.rstrip()
            + "\n\n"
            + block
            + "\n"
        )

    path.write_text(
        updated,
        encoding="utf-8",
    )


def write_new_files(root: Path) -> None:
    """Write deterministic Capability 007 files."""
    for relative, content in NEW_FILES.items():
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


def update_existing_documents(root: Path) -> None:
    """Update all complementary documentation."""
    for relative, (
        marker_name,
        content,
    ) in MARKER_BLOCKS.items():
        path = root / relative

        upsert_managed_block(
            path,
            marker_name,
            content,
        )

        print(f"Updated {relative}")


def apply_local_changes(root: Path) -> None:
    """Apply Capability 007 locally."""
    write_new_files(root)
    update_existing_documents(root)

    print()
    print(
        "Capability 007 Editorial Workspace runtime "
        "files have been written."
    )


# ---------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------

REQUIRED_FILES = tuple(NEW_FILES.keys())


def validate_required_files(root: Path) -> None:
    """Confirm that every required file exists."""
    missing = [
        relative
        for relative in REQUIRED_FILES
        if not (root / relative).is_file()
    ]

    if missing:
        raise CapabilityError(
            "Missing Capability 007 files:\n"
            + "\n".join(
                f"  - {relative}"
                for relative in missing
            )
        )

    print(
        "All required Capability 007 files are present."
    )


def validate_product_language(root: Path) -> None:
    """Validate canonical Capability 007 decisions."""
    checks: dict[str, tuple[str, ...]] = {
        (
            "docs/constitution/"
            "Canonical_Vocabulary.md"
        ): (
            "One concept. One canonical name.",
            "Editorial Workspace is not a synonym "
            "for Editorial Intake",
            "Identity Asset",
            "Brand-neutral",
        ),

        "docs/ui/Editorial_Workspace.md": (
            "Brand-neutral Hero Visual creation remains "
            "the default",
            "Rights confirmation is required",
            "Missing identity assets never invalidate "
            "the project",
        ),

        (
            "docs/architecture/"
            "Editorial_Intake_Runtime.md"
        ): (
            "Editorial Intake is the first capability",
            "The Author should not need to choose",
            "Rights confirmation is mandatory",
        ),

        (
            "docs/architecture/"
            "Source_Assessment_Runtime.md"
        ): (
            "Source Assessment is not Evidence Verification",
            "Capability 008",
        ),

        (
            "docs/architecture/adr/"
            "ADR-007-editorial-intake-runtime.md"
        ): (
            "Implement the Editorial Workspace",
            "Identity assets",
            "must not imply full evidence verification",
        ),

        (
            "docs/architecture/baselines/"
            "Architecture_Baseline_2026.08.01v03.md"
        ): (
            ARCHITECTURE_BASELINE_VERSION,
            "Begin Version 1.0 runtime implementation",
            "Canonical Vocabulary",
        ),
    }

    for relative, phrases in checks.items():
        path = root / relative

        content = normalize_markdown(
            path.read_text(encoding="utf-8")
        )

        for phrase in phrases:
            if phrase not in content:
                raise CapabilityError(
                    f"Expected phrase '{phrase}' "
                    f"in {relative}."
                )

    print(
        "Capability 007 product-language validation passed."
    )


def run_repository_validation(root: Path) -> None:
    """Run compile, unit, and repository validation."""
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

    print(
        "Capability 007 repository validation passed."
    )


def show_status(root: Path) -> None:
    """Display resulting repository changes."""
    print("\nGit status:")

    run(
        ["git", "status", "--short"],
        cwd=root,
    )

    print("\nTracked change summary:")

    run(
        ["git", "diff", "--stat"],
        cwd=root,
    )


# ---------------------------------------------------------------------
# Preview
# ---------------------------------------------------------------------

def preview() -> None:
    """Show planned changes without modifying files."""
    print()
    print("Capability 007 Editorial Workspace preview:")
    print()

    print("New files:")

    for relative in NEW_FILES:
        print(f"  - {relative}")

    print("\nManaged documentation updates:")

    for relative in MARKER_BLOCKS:
        print(f"  - {relative}")

    print("\nDecisions being implemented:")

    decisions = (
        "Adopt Canonical Vocabulary",
        "Use one concept and one canonical name",
        "Establish Editorial Workspace",
        "Define Editorial Intake as the first Workspace capability",
        "Implement natural input recognition",
        "Implement Understanding your input",
        "Implement Assessing your sources",
        "Keep later stages visible but pending",
        "Support optional logo identity assets",
        "Support optional headshot identity assets",
        "Require rights confirmation",
        "Preserve brand-neutral as the default",
        "Permit resume without original identity assets",
        "Do not confuse source assessment with verification",
        "Create Architecture Baseline 2026.08.01v03",
    )

    for decision in decisions:
        print(f"  - {decision}")

    print("\nPreview mode changes nothing.")

    print("\nApply local files with:")

    print(
        "  python3 scripts/"
        "bootstrap_capability007_editorial_intake.py "
        "--apply"
    )


# ---------------------------------------------------------------------
# GitHub synchronization
# ---------------------------------------------------------------------

PROJECT_DESCRIPTION = (
    "Version 1.0 capability roadmap governed by the Constitution, "
    "Canonical Vocabulary, Editorial Integrity, and the Canonical "
    "Editorial Session."
)


PROJECT_README = f"""# Ramrattan AI Editorial Studio

## Governing principle

Trust is our most valuable feature.

## Current implementation

- Capability 006A - complete
- Capability 007 - Editorial Workspace, Editorial Intake, and Source
  Assessment
- Architecture baseline - {ARCHITECTURE_BASELINE_VERSION}

## Canonical Vocabulary

- Editorial Workspace - complete Author-facing environment
- Editorial Intake - first capability inside the Workspace
- Editorial Confidence - primary Author-facing outcome
- LMHS Editorial Risk - internal assessment
- Identity Asset - optional logo or headshot

## Capability 007

Implements:

1. Understanding your input
2. Assessing your sources

Supports optional logo and headshot assets with rights confirmation.

Brand-neutral remains the default.
"""


CAPABILITY_ISSUE_BODY = clean(
    """
    ## Objective

    Implement the beginning of the Canonical Editorial Session inside
    the Editorial Workspace.

    ## Runtime scope

    - Welcome experience
    - Supported-input guidance
    - Natural input recognition
    - Stage 1 - Understanding your input
    - Stage 2 - Assessing your sources
    - Initial source-quality assessment
    - Optional logo
    - Optional headshot
    - Rights confirmation
    - Brand-neutral default
    - Resume without original identity assets

    ## Documentation scope

    - Canonical Vocabulary
    - Editorial Workspace UX
    - Author Conversation Guide
    - Editorial Confidence stages
    - Editorial Intake Runtime
    - Source Assessment Runtime
    - ADR-007
    - Architecture Baseline 2026.08.01v03
    - Capability demo

    ## Acceptance criteria

    - Runtime tests pass
    - Repository validation passes
    - Input type is inferred before asking
    - Stage 1 and Stage 2 complete
    - Later stages remain pending
    - Source assessment does not claim verification
    - Rights confirmation is enforced
    - Identity assets remain optional
    - Missing assets do not block resume
    - Canonical Vocabulary is used consistently
    """
)


def project_payload(root: Path) -> dict[str, Any]:
    """Return GitHub Project metadata."""
    payload = json_output(
        [
            "gh",
            "project",
            "view",
            str(PROJECT_NUMBER),
            "--owner",
            OWNER,
            "--format",
            "json",
        ],
        cwd=root,
    )

    if not isinstance(payload, dict):
        return {}

    return payload


def validate_project(root: Path) -> None:
    """Confirm expected Project identity."""
    project = project_payload(root)

    if project.get("id") != PROJECT_ID:
        raise CapabilityError(
            "GitHub Project #1 does not match the expected project ID."
        )


def issue_list(root: Path) -> list[dict[str, Any]]:
    """Return repository issues."""
    payload = json_output(
        [
            "gh",
            "issue",
            "list",
            "--repo",
            REPOSITORY,
            "--state",
            "all",
            "--limit",
            "300",
            "--json",
            "number,title,url,state",
        ],
        cwd=root,
    )

    if not isinstance(payload, list):
        return []

    return payload


def find_issue(
    root: Path,
    title: str,
) -> dict[str, Any] | None:
    """Find an issue by exact title."""
    for issue in issue_list(root):
        if issue.get("title") == title:
            return issue

    return None


def ensure_issue(
    root: Path,
    title: str,
    body: str,
) -> dict[str, Any]:
    """Return an existing issue or create it."""
    existing = find_issue(root, title)

    if existing is not None:
        print(
            f"Issue already exists: "
            f"#{existing['number']} - {title}"
        )
        return existing

    run(
        [
            "gh",
            "issue",
            "create",
            "--repo",
            REPOSITORY,
            "--title",
            title,
            "--body",
            body,
        ],
        cwd=root,
    )

    for attempt in range(1, 6):
        created = find_issue(root, title)

        if created is not None:
            print(
                f"Created issue "
                f"#{created['number']} - {title}"
            )
            return created

        print(
            f"Issue is not visible yet "
            f"(attempt {attempt}/5); waiting..."
        )
        time.sleep(2)

    raise CapabilityError(
        f"Could not resolve issue after creation: {title}"
    )


def project_items(root: Path) -> list[dict[str, Any]]:
    """Return GitHub Project items."""
    payload = json_output(
        [
            "gh",
            "project",
            "item-list",
            str(PROJECT_NUMBER),
            "--owner",
            OWNER,
            "--limit",
            "300",
            "--format",
            "json",
        ],
        cwd=root,
    )

    if not isinstance(payload, dict):
        return []

    items = payload.get("items", [])

    if not isinstance(items, list):
        return []

    return items


def project_item_for_url(
    root: Path,
    url: str,
) -> dict[str, Any] | None:
    """Find a Project item for a GitHub URL."""
    for item in project_items(root):
        content = item.get("content") or {}

        if content.get("url") == url:
            return item

    return None


def ensure_project_item(
    root: Path,
    url: str,
) -> dict[str, Any]:
    """Add an issue to the Project with bounded retries."""
    existing = project_item_for_url(root, url)

    if existing is not None:
        return existing

    run(
        [
            "gh",
            "project",
            "item-add",
            str(PROJECT_NUMBER),
            "--owner",
            OWNER,
            "--url",
            url,
        ],
        cwd=root,
    )

    for attempt in range(1, 11):
        created = project_item_for_url(root, url)

        if created is not None:
            if attempt > 1:
                print(
                    "Resolved Project item after "
                    f"{attempt} lookup attempts."
                )

            return created

        print(
            f"Project item is not visible yet "
            f"(attempt {attempt}/10); waiting..."
        )
        time.sleep(2)

    raise CapabilityError(
        "GitHub accepted the Project item but it did not become "
        f"visible within the retry window: {url}"
    )


def set_status(
    root: Path,
    item_id: str,
    status: str,
) -> None:
    """Set Project item status."""
    run(
        [
            "gh",
            "project",
            "item-edit",
            "--id",
            item_id,
            "--project-id",
            PROJECT_ID,
            "--field-id",
            STATUS_FIELD_ID,
            "--single-select-option-id",
            STATUS_OPTIONS[status],
        ],
        cwd=root,
    )


def update_issue_status(
    root: Path,
    title: str,
    status: str,
) -> None:
    """Update one existing issue when present."""
    issue = find_issue(root, title)

    if issue is None:
        print(
            f"Issue not found, skipping status update: {title}"
        )
        return

    item = ensure_project_item(
        root,
        issue["url"],
    )

    set_status(
        root,
        item["id"],
        status,
    )

    print(
        f"Marked issue #{issue['number']} {status}."
    )


def sync_project(root: Path) -> None:
    """Synchronize GitHub planning."""
    validate_required_files(root)
    validate_product_language(root)
    run_repository_validation(root)

    run(
        ["gh", "auth", "status"],
        cwd=root,
    )

    validate_project(root)

    update_issue_status(
        root,
        PREVIOUS_CAPABILITY_ISSUE_TITLE,
        "Done",
    )

    capability_issue = ensure_issue(
        root,
        CAPABILITY_ISSUE_TITLE,
        CAPABILITY_ISSUE_BODY,
    )

    capability_item = ensure_project_item(
        root,
        capability_issue["url"],
    )

    set_status(
        root,
        capability_item["id"],
        "In Progress",
    )

    print(
        "Capability 007 marked In Progress."
    )

    run(
        [
            "gh",
            "project",
            "edit",
            str(PROJECT_NUMBER),
            "--owner",
            OWNER,
            "--description",
            PROJECT_DESCRIPTION,
            "--readme",
            PROJECT_README,
        ],
        cwd=root,
    )

    print()
    print(
        "GitHub Project synchronized for Capability 007."
    )


# ---------------------------------------------------------------------
# Arguments and main
# ---------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Implement Capability 007 Editorial Workspace, "
            "Editorial Intake, and Source Assessment."
        )
    )

    mode = parser.add_mutually_exclusive_group()

    mode.add_argument(
        "--apply",
        action="store_true",
        help=(
            "Write and validate local Capability 007 files."
        ),
    )

    mode.add_argument(
        "--sync-project",
        action="store_true",
        help=(
            "Synchronize GitHub Project planning."
        ),
    )

    return parser.parse_args()


def main() -> int:
    """Preview, apply, or synchronize Capability 007."""
    args = parse_args()

    try:
        root = repository_root()

        print(f"Repository: {root}")

        verify_script_integrity()
        verify_branch(root)

        if args.sync_project:
            sync_project(root)

        elif args.apply:
            verify_expected_working_tree(root)
            apply_local_changes(root)
            validate_required_files(root)
            validate_product_language(root)
            run_repository_validation(root)
            show_status(root)

            print()
            print(
                "Capability 007 Editorial Workspace runtime "
                "has been applied and validated."
            )
            print(
                "Nothing has been committed, pushed, "
                "or changed on GitHub."
            )

        else:
            verify_expected_working_tree(root)
            preview()

        return 0

    except CapabilityError as exc:
        print(
            f"\nERROR: {exc}",
            file=sys.stderr,
        )
        return 1

    except subprocess.CalledProcessError as exc:
        print(
            f"\nERROR: Command failed with exit code "
            f"{exc.returncode}.",
            file=sys.stderr,
        )
        return exc.returncode

    except json.JSONDecodeError as exc:
        print(
            f"\nERROR: Could not parse GitHub CLI JSON: {exc}",
            file=sys.stderr,
        )
        return 1

    except Exception as exc:
        print(
            f"\nUNEXPECTED ERROR: {exc}",
            file=sys.stderr,
        )
        return 1


# CAPABILITY_007_EDITORIAL_INTAKE_COMPLETE
# END OF SCRIPT - CAPABILITY 007


if __name__ == "__main__":
    raise SystemExit(main())