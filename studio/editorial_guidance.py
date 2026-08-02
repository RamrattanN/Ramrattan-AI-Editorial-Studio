"""Author-facing rendering for Editorial Guidance."""

from __future__ import annotations

from dataclasses import dataclass

from .editorial_discernment import (
    DiscernmentDecision,
    EditorialSession,
    StageState,
    WorkspaceState,
)


STAGE_NAMES = {
    1: "Understanding your input",
    2: "Assessing your sources",
    3: "Verifying the evidence",
    4: "Reviewing editorial risks",
    5: "Creating your publication package",
}


@dataclass(frozen=True)
class EditorialGuidanceView:
    """Author-facing Editorial Workspace status."""

    workspace_state: WorkspaceState
    progress_lines: tuple[str, ...]
    guidance: str
    clarification_question: str | None = None


def render_progress(
    session: EditorialSession,
) -> tuple[str, ...]:
    """Render stage and session state separately."""
    symbols = {
        StageState.NOT_STARTED: "○",
        StageState.IN_PROGRESS: "◐",
        StageState.COMPLETE: "✓",
        StageState.BLOCKED: "!",
    }

    lines = [
        f"Editorial Workspace - "
        f"{session.workspace_state.value.replace('_', ' ').title()}"
    ]

    for number in range(1, 6):
        state = session.stage_states[number]
        lines.append(
            f"{symbols[state]} {STAGE_NAMES[number]}"
        )

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
        clarification_question=(
            decision.clarification_question
        ),
    )
