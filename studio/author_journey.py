"""Early-session orchestration for the Version 1.1 Author Journey.

V11-01 owns Welcome through Workflow Selection. V11-02 adds structurally
independent Editorial Source and Branding intake plus the routing seam into
Editorial Discovery. The orchestrator wraps an optional Version 1.0
``EditorialSession`` without changing that runtime.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    from .editorial_discernment import EditorialSession


CONFIGURATION_FIELDS: Final = frozenset(
    {"preferred_workflow", "branding_preference"}
)
CONFIGURATION_FILENAME_PATTERN: Final = re.compile(
    r"^Ramrattan-AI-Configuration-\d{4}\.\d{2}\.\d{2}v\d{2}\.json$"
)


class AuthorJourneyError(ValueError):
    """Base error for invalid V11-01 input or orchestration."""


class InvalidAuthorJourneyTransition(AuthorJourneyError):
    """Raised when an action is attempted from the wrong journey state."""


class ConfigurationValidationError(AuthorJourneyError):
    """Raised when a Ramrattan AI Configuration fails validation."""


class AuthorJourneyState(StrEnum):
    """Implemented early states and stable downstream routing seams."""

    WELCOME = "welcome"
    ENTRY_PATH = "entry_path"
    CONFIGURATION_LOAD = "configuration_load"
    RESUME_VALIDATION = "resume_validation"
    WORKFLOW_SELECTION = "workflow_selection"
    EDITORIAL_SOURCE = "editorial_source"
    BRANDING = "branding"
    EDITORIAL_DISCOVERY = "editorial_discovery"


class EntryPath(StrEnum):
    """The two and only two choices available at Entry Path."""

    START_NEW_PUBLICATION = "start_new_publication"
    RESUME_EXISTING_PROJECT = "resume_existing_project"


class WorkflowMode(StrEnum):
    """Presentation modes over the single Author Journey state machine."""

    GUIDED = "guided"
    EXPRESS = "express"


class EditorialSourceKind(StrEnum):
    """The approved forms of Editorial Source material."""

    URL = "url"
    ARTICLE = "article"
    DOCUMENT = "document"
    RESEARCH_MATERIAL = "research_material"
    TOPIC = "topic"
    NOTES = "notes"


class BrandingMode(StrEnum):
    """Author-controlled branding choices and the material-free fallback."""

    PERSONAL = "personal"
    BUSINESS = "business"
    STUDIO_THEME = "studio_theme"


class BrandingMaterialKind(StrEnum):
    """The approved forms of optional Branding material."""

    WEBSITE = "website"
    LOGO = "logo"
    PROFESSIONAL_HEADSHOT = "professional_headshot"
    BRAND_COLOURS = "brand_colours"
    BRAND_GUIDE = "brand_guide"
    PRESENTATION = "presentation"
    PREVIOUS_HERO_VISUAL = "previous_hero_visual"
    OTHER_VISUAL_REFERENCE = "other_visual_reference"


@dataclass(frozen=True, slots=True)
class EditorialSourceMaterial:
    """One explicit source contribution supplied by the Author."""

    kind: EditorialSourceKind
    content: str

    def __post_init__(self) -> None:
        if not isinstance(self.kind, EditorialSourceKind):
            raise AuthorJourneyError("Editorial Source kind is not supported.")
        if not isinstance(self.content, str) or not self.content.strip():
            raise AuthorJourneyError("Editorial Source content must not be empty.")


@dataclass(frozen=True, slots=True)
class EditorialInference:
    """The four Editorial Source inferences required before Branding."""

    intent: str
    audience: str
    platform: str
    desired_outcome: str

    def __post_init__(self) -> None:
        for field_name in ("intent", "audience", "platform", "desired_outcome"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise AuthorJourneyError(
                    f"Editorial inference {field_name} must not be empty."
                )


@dataclass(frozen=True, slots=True)
class BrandingMaterial:
    """One optional visual Branding reference, kept separate from Source."""

    kind: BrandingMaterialKind
    reference: str

    def __post_init__(self) -> None:
        if not isinstance(self.kind, BrandingMaterialKind):
            raise AuthorJourneyError("Branding material kind is not supported.")
        if not isinstance(self.reference, str) or not self.reference.strip():
            raise AuthorJourneyError("Branding material reference must not be empty.")


@dataclass(frozen=True, slots=True)
class BrandingSelection:
    """An explicit Branding choice made during this session."""

    mode: BrandingMode
    materials: tuple[BrandingMaterial, ...]


@dataclass(frozen=True, slots=True)
class IntakePresentation:
    """Presentation data over the single Author Journey state machine."""

    visible_states: tuple[AuthorJourneyState, ...]
    carried_branding_preference: str | None


@dataclass(frozen=True, slots=True)
class BrandingPrompt:
    """Branding choices, including any Configuration-carried preference."""

    choices: tuple[BrandingMode, ...]
    material_kinds: tuple[BrandingMaterialKind, ...]
    carried_preference_to_confirm: str | None


def infer_editorial_source(material: EditorialSourceMaterial) -> EditorialInference:
    """Return deterministic, conservative inferences for one Source input."""
    if not isinstance(material, EditorialSourceMaterial):
        raise AuthorJourneyError("Editorial Source input is not supported.")
    source_label = material.kind.value.replace("_", " ")
    return EditorialInference(
        intent=f"Develop a publication from the supplied {source_label}.",
        audience="Professional readers",
        platform="LinkedIn",
        desired_outcome="A clear, evidence-aware professional publication.",
    )


@dataclass(frozen=True, slots=True)
class StudioConfiguration:
    """The complete two-field Version 1.1 Configuration schema."""

    preferred_workflow: WorkflowMode
    branding_preference: str

    def __post_init__(self) -> None:
        if not isinstance(self.preferred_workflow, WorkflowMode):
            raise ConfigurationValidationError(
                "Configuration preferred_workflow must be guided or express."
            )
        if not isinstance(self.branding_preference, str):
            raise ConfigurationValidationError(
                "Configuration branding_preference must be text."
            )
        if not self.branding_preference.strip():
            raise ConfigurationValidationError(
                "Configuration branding_preference must not be empty."
            )

    def to_json(self) -> str:
        """Return deterministic JSON containing exactly the approved fields."""
        return json.dumps(
            {
                "branding_preference": self.branding_preference,
                "preferred_workflow": self.preferred_workflow.value,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ) + "\n"


def load_studio_configuration(
    filename: str, content: str | bytes
) -> StudioConfiguration:
    """Validate and load one session-scoped JSON Configuration."""
    if not CONFIGURATION_FILENAME_PATTERN.fullmatch(filename):
        raise ConfigurationValidationError(
            "Configuration filename must match "
            "Ramrattan-AI-Configuration-[YYYY.MM.DDvNN].json."
        )
    if isinstance(content, bytes):
        try:
            content = content.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ConfigurationValidationError(
                "Configuration content must be UTF-8 JSON text."
            ) from exc
    if not isinstance(content, str):
        raise ConfigurationValidationError(
            "Configuration content must be JSON text."
        )
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ConfigurationValidationError(
            f"Configuration contains invalid JSON: {exc.msg}."
        ) from exc
    if not isinstance(parsed, dict):
        raise ConfigurationValidationError(
            "Configuration JSON must contain one object."
        )
    fields = set(parsed)
    if fields != CONFIGURATION_FIELDS:
        missing = sorted(CONFIGURATION_FIELDS - fields)
        extra = sorted(fields - CONFIGURATION_FIELDS)
        details = []
        if missing:
            details.append("missing fields: " + ", ".join(missing))
        if extra:
            details.append("unsupported fields: " + ", ".join(extra))
        raise ConfigurationValidationError(
            "Configuration must contain exactly preferred_workflow and "
            "branding_preference (" + "; ".join(details) + ")."
        )
    try:
        workflow = WorkflowMode(parsed["preferred_workflow"])
    except (TypeError, ValueError) as exc:
        raise ConfigurationValidationError(
            "Configuration preferred_workflow must be guided or express."
        ) from exc
    return StudioConfiguration(
        preferred_workflow=workflow,
        branding_preference=parsed["branding_preference"],
    )


class AuthorJourney:
    """Thin, deterministic orchestrator for the beginning of one session."""

    ENTRY_PATH_CHOICES: Final = tuple(EntryPath)
    WORKFLOW_CHOICES: Final = tuple(WorkflowMode)
    BRANDING_CHOICES: Final = (BrandingMode.PERSONAL, BrandingMode.BUSINESS)
    BRANDING_MATERIAL_KINDS: Final = tuple(BrandingMaterialKind)

    def __init__(
        self, editorial_session: EditorialSession | None = None
    ) -> None:
        self.editorial_session = editorial_session
        self.state = AuthorJourneyState.WELCOME
        self.workflow_mode: WorkflowMode | None = None
        self.branding_preference: str | None = None
        self.configuration_loaded = False

    def begin(self) -> None:
        """Perform Welcome's automatic transition to Entry Path."""
        self._require(AuthorJourneyState.WELCOME, "begin the Author Journey")
        self.state = AuthorJourneyState.ENTRY_PATH

    def choose_entry_path(self, choice: EntryPath) -> None:
        """Route to new-publication Configuration Load or the resume seam."""
        self._require(AuthorJourneyState.ENTRY_PATH, "choose an Entry Path")
        if not isinstance(choice, EntryPath):
            raise AuthorJourneyError(
                "Entry Path must be Start New Publication or Resume Existing Project."
            )
        if choice is EntryPath.START_NEW_PUBLICATION:
            self.state = AuthorJourneyState.CONFIGURATION_LOAD
            return
        self.state = AuthorJourneyState.RESUME_VALIDATION

    def skip_configuration(self) -> None:
        """Continue with Studio defaults and no warning or error state."""
        self._require(
            AuthorJourneyState.CONFIGURATION_LOAD, "skip Configuration Load"
        )
        self.configuration_loaded = False
        self.workflow_mode = None
        self.branding_preference = None
        self.state = AuthorJourneyState.WORKFLOW_SELECTION

    def load_configuration(self, filename: str, content: str | bytes) -> None:
        """Restore two preferences for this in-memory session only."""
        self._require(
            AuthorJourneyState.CONFIGURATION_LOAD, "load a Configuration"
        )
        configuration = load_studio_configuration(filename, content)
        self.workflow_mode = configuration.preferred_workflow
        self.branding_preference = configuration.branding_preference
        self.configuration_loaded = True
        self.state = AuthorJourneyState.WORKFLOW_SELECTION

    def select_workflow(self, mode: WorkflowMode) -> None:
        """Confirm or change presentation mode, then enter the next seam."""
        self._require(
            AuthorJourneyState.WORKFLOW_SELECTION, "select a Workflow mode"
        )
        if not isinstance(mode, WorkflowMode):
            raise AuthorJourneyError(
                "Workflow mode must be Guided Workflow or Express Workflow."
            )
        self.workflow_mode = mode
        self.state = AuthorJourneyState.EDITORIAL_SOURCE

    def intake_presentation(self) -> IntakePresentation:
        """Describe Guided or Express intake without changing transitions."""
        self._require(
            AuthorJourneyState.EDITORIAL_SOURCE, "present Editorial Source intake"
        )
        visible_states = (AuthorJourneyState.EDITORIAL_SOURCE,)
        carried_preference = None
        if self.workflow_mode is WorkflowMode.EXPRESS:
            visible_states += (AuthorJourneyState.BRANDING,)
            carried_preference = self.branding_preference
        return IntakePresentation(visible_states, carried_preference)

    def submit_editorial_source(
        self,
        material: EditorialSourceMaterial,
        *,
        inference: EditorialInference | None = None,
    ) -> EditorialInference:
        """Accept Source, establish its four inferences, then enter Branding."""
        self._require(
            AuthorJourneyState.EDITORIAL_SOURCE, "submit Editorial Source"
        )
        if not isinstance(material, EditorialSourceMaterial):
            raise AuthorJourneyError("Editorial Source input is not supported.")
        resolved = infer_editorial_source(material) if inference is None else inference
        if not isinstance(resolved, EditorialInference):
            raise AuthorJourneyError("Editorial Source inference is not supported.")
        self._editorial_source = material
        self._editorial_inference = resolved
        self.state = AuthorJourneyState.BRANDING
        return resolved

    def branding_prompt(self) -> BrandingPrompt:
        """Present independent Branding input and carried preference data."""
        self._require(AuthorJourneyState.BRANDING, "present Branding intake")
        return BrandingPrompt(
            choices=self.BRANDING_CHOICES,
            material_kinds=self.BRANDING_MATERIAL_KINDS,
            carried_preference_to_confirm=self.branding_preference,
        )

    def submit_branding(
        self,
        mode: BrandingMode | None,
        materials: tuple[BrandingMaterial, ...] = (),
    ) -> BrandingSelection:
        """Accept an explicit Branding choice and enter the Discovery seam."""
        self._require(AuthorJourneyState.BRANDING, "submit Branding")
        if mode is not None and not isinstance(mode, BrandingMode):
            raise AuthorJourneyError("Branding choice must be personal or business.")
        if not isinstance(materials, tuple) or not all(
            isinstance(item, BrandingMaterial) for item in materials
        ):
            raise AuthorJourneyError("Branding materials are not supported.")
        if mode is BrandingMode.STUDIO_THEME and materials:
            raise AuthorJourneyError(
                "Studio Theme cannot be combined with supplied Branding material."
            )
        if not materials:
            mode = BrandingMode.STUDIO_THEME
        elif mode not in self.BRANDING_CHOICES:
            raise AuthorJourneyError(
                "Supplied Branding material requires personal or business branding."
            )
        selection = BrandingSelection(mode=mode, materials=materials)
        self._branding_selection = selection
        self.state = AuthorJourneyState.EDITORIAL_DISCOVERY
        return selection

    @property
    def editorial_source(self) -> EditorialSourceMaterial | None:
        return getattr(self, "_editorial_source", None)

    @property
    def editorial_inference(self) -> EditorialInference | None:
        return getattr(self, "_editorial_inference", None)

    @property
    def branding_selection(self) -> BrandingSelection | None:
        return getattr(self, "_branding_selection", None)

    def _require(self, expected: AuthorJourneyState, action: str) -> None:
        if self.state is not expected:
            raise InvalidAuthorJourneyTransition(
                f"Cannot {action} from {self.state.value}; "
                f"required state is {expected.value}."
            )
