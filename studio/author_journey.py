"""V11-01 early-session orchestration for the Version 1.1 Author Journey.

The orchestrator owns only Welcome, Entry Path, Configuration Load, Workflow
Selection, and the routing seams into later slices. It wraps an optional
Version 1.0 ``EditorialSession`` without changing that runtime.
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
    """V11-01-owned states and its two stable downstream routing seams."""

    WELCOME = "welcome"
    ENTRY_PATH = "entry_path"
    CONFIGURATION_LOAD = "configuration_load"
    RESUME_VALIDATION = "resume_validation"
    WORKFLOW_SELECTION = "workflow_selection"
    EDITORIAL_SOURCE = "editorial_source"


class EntryPath(StrEnum):
    """The two and only two choices available at Entry Path."""

    START_NEW_PUBLICATION = "start_new_publication"
    RESUME_EXISTING_PROJECT = "resume_existing_project"


class WorkflowMode(StrEnum):
    """Presentation modes over the single Author Journey state machine."""

    GUIDED = "guided"
    EXPRESS = "express"


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

    def _require(self, expected: AuthorJourneyState, action: str) -> None:
        if self.state is not expected:
            raise InvalidAuthorJourneyTransition(
                f"Cannot {action} from {self.state.value}; "
                f"required state is {expected.value}."
            )
