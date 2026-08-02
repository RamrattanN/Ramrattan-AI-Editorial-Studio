"""Canonical Editorial Integrity stages and Author-facing guidance."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, StrEnum
from types import MappingProxyType
from typing import TYPE_CHECKING, Mapping

if TYPE_CHECKING:
    from .editorial_discernment import (
        DiscernmentDecision,
        EditorialSession,
        WorkspaceState,
    )


class EditorialStage(IntEnum):
    """Canonical order of the five visible Editorial Integrity stages."""

    UNDERSTANDING_INPUT = 1
    ASSESSING_SOURCES = 2
    VERIFYING_EVIDENCE = 3
    REVIEWING_EDITORIAL_RISKS = 4
    CREATING_PUBLICATION_PACKAGE = 5


class StageState(StrEnum):
    """Canonical lifecycle of one Editorial Integrity stage."""

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    BLOCKED = "blocked"

    # Compatibility aliases preserve earlier API member names while every
    # active runtime component uses the canonical names above.
    PENDING = NOT_STARTED
    ACTIVE = IN_PROGRESS


STAGE_NAMES: Mapping[int, str] = MappingProxyType(
    {
        EditorialStage.UNDERSTANDING_INPUT: "Understanding your input",
        EditorialStage.ASSESSING_SOURCES: "Assessing your sources",
        EditorialStage.VERIFYING_EVIDENCE: "Verifying the evidence",
        EditorialStage.REVIEWING_EDITORIAL_RISKS: "Reviewing editorial risks",
        EditorialStage.CREATING_PUBLICATION_PACKAGE: (
            "Creating your publication package"
        ),
    }
)

STAGE_ORDER = tuple(EditorialStage)

_ALLOWED_TRANSITIONS: Mapping[StageState, frozenset[StageState]] = (
    MappingProxyType(
        {
            StageState.NOT_STARTED: frozenset(
                {
                    StageState.IN_PROGRESS,
                    StageState.COMPLETE,
                    StageState.BLOCKED,
                }
            ),
            StageState.IN_PROGRESS: frozenset(
                {StageState.COMPLETE, StageState.BLOCKED}
            ),
            StageState.BLOCKED: frozenset({StageState.IN_PROGRESS}),
            StageState.COMPLETE: frozenset(),
        }
    )
)


def initial_stage_states() -> dict[int, StageState]:
    """Return a new canonical five-stage state map."""
    return {int(stage): StageState.NOT_STARTED for stage in STAGE_ORDER}


def validate_stage_states(states: Mapping[int, StageState]) -> None:
    """Validate stage membership, order, and one-active-stage invariants."""
    expected = {int(stage) for stage in STAGE_ORDER}
    if set(states) != expected:
        raise ValueError("Stage states must contain exactly stages 1 through 5.")
    if any(not isinstance(state, StageState) for state in states.values()):
        raise ValueError("Every stage must use the canonical StageState.")

    active = sum(state is StageState.IN_PROGRESS for state in states.values())
    if active > 1:
        raise ValueError("Only one Editorial Integrity stage may be in progress.")

    incomplete_seen = False
    for stage in STAGE_ORDER:
        state = states[int(stage)]
        if state is StageState.COMPLETE:
            if incomplete_seen:
                raise ValueError("Completed stages must form one ordered prefix.")
        else:
            if (
                incomplete_seen
                and state in {StageState.IN_PROGRESS, StageState.BLOCKED}
            ):
                raise ValueError("A stage cannot skip an earlier incomplete stage.")
            incomplete_seen = True
        if incomplete_seen and state in {StageState.IN_PROGRESS, StageState.BLOCKED}:
            if any(
                states[later] is not StageState.NOT_STARTED
                for later in range(int(stage) + 1, 6)
            ):
                raise ValueError("Later stages cannot start before the active stage.")


def transition_stage(
    states: Mapping[int, StageState],
    number: int,
    target: StageState,
) -> dict[int, StageState]:
    """Return a validated stage snapshot after one allowed transition."""
    validate_stage_states(states)
    if number not in states:
        raise ValueError("Stage number must be from 1 to 5.")
    if not isinstance(target, StageState):
        raise ValueError("Stage transitions require the canonical StageState.")

    current = states[number]
    if target is current:
        return dict(states)
    if target not in _ALLOWED_TRANSITIONS[current]:
        raise ValueError(
            f"Stage transition {current.value} -> {target.value} is not allowed."
        )
    if target is not StageState.NOT_STARTED and any(
        states[prior] is not StageState.COMPLETE
        for prior in range(1, number)
    ):
        raise ValueError("Earlier stages must be complete before this stage starts.")

    updated = dict(states)
    updated[number] = target
    validate_stage_states(updated)
    return updated


@dataclass(frozen=True)
class EditorialGuidanceView:
    """Author-facing Editorial Workspace status."""

    workspace_state: WorkspaceState
    progress_lines: tuple[str, ...]
    guidance: str
    clarification_question: str | None = None


def render_progress(session: EditorialSession) -> tuple[str, ...]:
    """Render canonical stage and persistent workspace state separately."""
    validate_stage_states(session.stage_states)
    symbols = {
        StageState.NOT_STARTED: "○",
        StageState.IN_PROGRESS: "◐",
        StageState.COMPLETE: "✓",
        StageState.BLOCKED: "!",
    }
    lines = [
        "Editorial Workspace - "
        f"{session.workspace_state.value.replace('_', ' ').title()}"
    ]
    for stage in STAGE_ORDER:
        state = session.stage_states[int(stage)]
        lines.append(f"{symbols[state]} {STAGE_NAMES[int(stage)]}")
    return tuple(lines)


def guidance_view(
    session: EditorialSession,
    decision: DiscernmentDecision,
) -> EditorialGuidanceView:
    """Create one Author-facing response."""
    return EditorialGuidanceView(
        workspace_state=session.workspace_state,
        progress_lines=render_progress(session),
        guidance=decision.author_message,
        clarification_question=decision.clarification_question,
    )
