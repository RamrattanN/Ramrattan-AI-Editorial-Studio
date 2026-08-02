#!/usr/bin/env python3
"""
Capability 008 - Editorial Discernment and Guided Editorial Session

Preview:

    python3 scripts/bootstrap_capability008_editorial_discernment.py

Apply local repository changes:

    python3 scripts/bootstrap_capability008_editorial_discernment.py \
        --apply

Synchronize GitHub planning after local validation:

    python3 scripts/bootstrap_capability008_editorial_discernment.py \
        --sync-project

This bootstrap implements:

- Editorial Discernment Engine
- Author-facing Editorial Guidance
- Editorial Intent
- Editorial Coherence Guard
- No Silent Scope Expansion
- One Editorial Intent per Editorial Session
- Workspace lifecycle
- Stage lifecycle
- Pause, resume, cancel, abort, complete, and archive behaviour
- Supporting-source acceptance
- Unrelated-publication detection
- Single-question clarification
- Approved-component protection
- Editorial Never Events
- ADR-009
- Architecture Baseline 2026.08.01v05
- Runtime and documentation tests
- Complementary documentation alignment
- Idempotent GitHub Project synchronization

Preview mode changes nothing.

--apply changes local repository files only.

--sync-project changes GitHub planning only after the local capability
exists and validates.

This script does not commit, push, create a pull request, or merge.
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

EXPECTED_BRANCH = "feature/editorial-discernment-engine"

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
    "scripts/bootstrap_capability008_editorial_discernment.py"
)

SCRIPT_SENTINEL = (
    "CAPABILITY_008_EDITORIAL_DISCERNMENT_COMPLETE"
)

CAPABILITY_ISSUE_NUMBER = 14

CAPABILITY_ISSUE_TITLE = (
    "Capability 008 - Implement Editorial Discernment, "
    "Evidence Validation, and Editorial Risk"
)

PREVIOUS_CAPABILITY_ISSUE_NUMBER = 13

ARCHITECTURE_BASELINE_VERSION = "2026.08.01v05"


# ---------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------

def clean(value: str) -> str:
    """Dedent text and ensure one trailing newline."""
    return textwrap.dedent(value).strip() + "\n"


def normalize(value: str) -> str:
    """Normalize text for resilient phrase validation."""
    return " ".join(
        value.replace(">", " ").split()
    )


# ---------------------------------------------------------------------
# Runtime implementation
# ---------------------------------------------------------------------

EDITORIAL_DISCERNMENT_RUNTIME = clean(
    '''
    """Editorial Discernment Engine for Capability 008.

    Internal name:
        Editorial Discernment Engine

    Author-facing name:
        Editorial Guidance

    The runtime protects one coherent Editorial Intent per Editorial
    Session while preserving the Author's authority to change direction.
    """

    from __future__ import annotations

    from dataclasses import dataclass, field
    from enum import Enum
    from typing import Iterable


    class ContributionKind(str, Enum):
        """What a new Author contribution appears to mean."""

        CONTINUE = "continue"
        ADD_EVIDENCE = "add_evidence"
        REPLACE_SOURCE = "replace_source"
        CORRECT_INFORMATION = "correct_information"
        REVISE_COMPONENT = "revise_component"
        CHANGE_ANGLE = "change_angle"
        CHANGE_AUDIENCE = "change_audience"
        REQUEST_RESEARCH = "request_research"
        ADD_IDENTITY_ASSET = "add_identity_asset"
        APPROVE = "approve"
        REJECT = "reject"
        PAUSE = "pause"
        RESUME = "resume"
        CANCEL = "cancel"
        ABORT = "abort"
        COMPLETE = "complete"
        ARCHIVE = "archive"
        NEW_PUBLICATION = "new_publication"
        CLARIFICATION_REQUIRED = "clarification_required"


    class IntentAlignment(str, Enum):
        """Relationship between new material and current intent."""

        ALIGNED = "aligned"
        RELATED = "related"
        DIVERGING = "diverging"
        SEPARATE_INTENT = "separate_intent"
        AMBIGUOUS = "ambiguous"


    class WorkspaceState(str, Enum):
        """Lifecycle of the complete Editorial Workspace."""

        CREATED = "created"
        ACTIVE = "active"
        WAITING_FOR_AUTHOR = "waiting_for_author"
        PAUSED = "paused"
        CANCELLED = "cancelled"
        ABORTED = "aborted"
        COMPLETED = "completed"
        ARCHIVED = "archived"


    class StageState(str, Enum):
        """Lifecycle of one Editorial Integrity stage."""

        NOT_STARTED = "not_started"
        IN_PROGRESS = "in_progress"
        COMPLETE = "complete"
        BLOCKED = "blocked"


    class EditorialComponent(str, Enum):
        """Publication Package components that may be revised."""

        HERO_VISUAL = "hero_visual"
        HEADLINE = "headline"
        HOOK = "hook"
        INSIGHT_1 = "insight_1"
        INSIGHT_2 = "insight_2"
        PRACTICAL_TAKEAWAY = "practical_takeaway"
        SOURCE_ATTRIBUTION = "source_attribution"
        CTA = "cta"
        HASHTAGS = "hashtags"
        LINKEDIN_DESCRIPTION = "linkedin_description"


    @dataclass(frozen=True)
    class EditorialIntent:
        """The single coherent objective for one Editorial Session."""

        primary_topic: str
        editorial_objective: str
        intended_audience: str
        publication_goal: str
        scope_terms: tuple[str, ...] = ()
        primary_sources: tuple[str, ...] = ()
        supporting_sources: tuple[str, ...] = ()

        def is_defined(self) -> bool:
            """Return True when the intent has its minimum fields."""
            return all(
                value.strip()
                for value in (
                    self.primary_topic,
                    self.editorial_objective,
                    self.intended_audience,
                    self.publication_goal,
                )
            )


    @dataclass(frozen=True)
    class Contribution:
        """One new Author contribution."""

        text: str
        source_identifiers: tuple[str, ...] = ()
        target_component: EditorialComponent | None = None
        declared_kind: ContributionKind | None = None


    @dataclass(frozen=True)
    class DiscernmentDecision:
        """Decision returned by the Editorial Discernment Engine."""

        contribution_kind: ContributionKind
        alignment: IntentAlignment
        author_message: str
        may_continue_current_session: bool
        recommend_new_session: bool = False
        requires_clarification: bool = False
        clarification_question: str | None = None
        preserve_existing_work: bool = True
        affected_components: tuple[EditorialComponent, ...] = ()
        protected_components: tuple[EditorialComponent, ...] = ()
        rationale: tuple[str, ...] = ()


    @dataclass
    class EditorialSession:
        """Guided Editorial Session state."""

        intent: EditorialIntent
        workspace_state: WorkspaceState = WorkspaceState.CREATED
        stage_states: dict[int, StageState] = field(
            default_factory=lambda: {
                1: StageState.NOT_STARTED,
                2: StageState.NOT_STARTED,
                3: StageState.NOT_STARTED,
                4: StageState.NOT_STARTED,
                5: StageState.NOT_STARTED,
            }
        )
        approved_components: set[EditorialComponent] = field(
            default_factory=set
        )
        preserved_events: list[str] = field(default_factory=list)

        def activate(self) -> None:
            """Activate a new or resumed session."""
            if self.workspace_state in {
                WorkspaceState.CANCELLED,
                WorkspaceState.ARCHIVED,
            }:
                raise ValueError(
                    "Cancelled or archived sessions cannot be "
                    "activated directly."
                )

            self.workspace_state = WorkspaceState.ACTIVE

        def pause(self) -> None:
            """Pause without losing work."""
            if self.workspace_state is not WorkspaceState.ACTIVE:
                raise ValueError(
                    "Only an active session can be paused."
                )

            self.workspace_state = WorkspaceState.PAUSED
            self.preserved_events.append("Session paused.")

        def resume(self) -> None:
            """Resume a paused or aborted session."""
            if self.workspace_state not in {
                WorkspaceState.PAUSED,
                WorkspaceState.ABORTED,
                WorkspaceState.WAITING_FOR_AUTHOR,
            }:
                raise ValueError(
                    "Only paused, aborted, or waiting sessions "
                    "can be resumed."
                )

            self.workspace_state = WorkspaceState.ACTIVE
            self.preserved_events.append("Session resumed.")

        def cancel(self) -> None:
            """Record deliberate Author cancellation."""
            if self.workspace_state in {
                WorkspaceState.COMPLETED,
                WorkspaceState.ARCHIVED,
            }:
                raise ValueError(
                    "Completed or archived sessions cannot be "
                    "cancelled."
                )

            self.workspace_state = WorkspaceState.CANCELLED
            self.preserved_events.append(
                "Session cancelled by the Author."
            )

        def abort(self) -> None:
            """Record exceptional or interrupted termination."""
            if self.workspace_state in {
                WorkspaceState.COMPLETED,
                WorkspaceState.ARCHIVED,
                WorkspaceState.CANCELLED,
            }:
                raise ValueError(
                    "This session cannot be aborted from its "
                    "current state."
                )

            self.workspace_state = WorkspaceState.ABORTED
            self.preserved_events.append(
                "Session aborted; work and provenance preserved."
            )

        def complete(self) -> None:
            """Complete the Editorial Session."""
            if self.workspace_state is not WorkspaceState.ACTIVE:
                raise ValueError(
                    "Only an active session can be completed."
                )

            if not all(
                state is StageState.COMPLETE
                for state in self.stage_states.values()
            ):
                raise ValueError(
                    "All Editorial Integrity stages must be complete."
                )

            self.workspace_state = WorkspaceState.COMPLETED
            self.preserved_events.append("Session completed.")

        def archive(self) -> None:
            """Archive a completed, cancelled, or aborted session."""
            if self.workspace_state not in {
                WorkspaceState.COMPLETED,
                WorkspaceState.CANCELLED,
                WorkspaceState.ABORTED,
            }:
                raise ValueError(
                    "Only completed, cancelled, or aborted sessions "
                    "can be archived."
                )

            self.workspace_state = WorkspaceState.ARCHIVED
            self.preserved_events.append("Session archived.")

        def approve(
            self,
            component: EditorialComponent,
        ) -> None:
            """Protect a Publication Package component."""
            self.approved_components.add(component)

        def mark_stage(
            self,
            number: int,
            state: StageState,
        ) -> None:
            """Update one stage without changing session lifecycle."""
            if number not in self.stage_states:
                raise ValueError("Stage number must be from 1 to 5.")

            self.stage_states[number] = state


    class EditorialDiscernmentEngine:
        """Interpret new contributions and protect editorial coherence."""

        NEW_SESSION_MESSAGE = (
            "This appears to introduce a different publication "
            "objective. To preserve clarity and Reader trust, I "
            "recommend starting a new Editorial Session. Your current "
            "work will remain exactly as it is."
        )

        SCOPE_EXPANSION_MESSAGE = (
            "This material would significantly broaden the current "
            "publication. We can expand the existing scope with your "
            "approval, or start a new Editorial Session."
        )

        def classify(
            self,
            session: EditorialSession,
            contribution: Contribution,
        ) -> DiscernmentDecision:
            """Classify one contribution conservatively."""
            text = contribution.text.strip()

            if contribution.declared_kind is not None:
                return self._declared_decision(
                    session,
                    contribution,
                )

            if not text and not contribution.source_identifiers:
                return self._clarify(
                    session,
                    "What would you like to change or add?",
                )

            lower = text.lower()

            if self._contains_any(
                lower,
                ("abort", "stop immediately", "terminate session"),
            ):
                return DiscernmentDecision(
                    contribution_kind=ContributionKind.ABORT,
                    alignment=IntentAlignment.ALIGNED,
                    author_message=(
                        "I will mark this Editorial Session as "
                        "Aborted while preserving the work, approvals, "
                        "provenance, and session history."
                    ),
                    may_continue_current_session=False,
                    protected_components=tuple(
                        sorted(
                            session.approved_components,
                            key=lambda item: item.value,
                        )
                    ),
                )

            if self._contains_any(
                lower,
                ("cancel this", "discard this session"),
            ):
                return DiscernmentDecision(
                    contribution_kind=ContributionKind.CANCEL,
                    alignment=IntentAlignment.ALIGNED,
                    author_message=(
                        "I will cancel this Editorial Session. "
                        "The project record can still preserve what "
                        "was completed."
                    ),
                    may_continue_current_session=False,
                )

            if self._contains_any(
                lower,
                ("pause", "hold this", "come back later"),
            ):
                return DiscernmentDecision(
                    contribution_kind=ContributionKind.PAUSE,
                    alignment=IntentAlignment.ALIGNED,
                    author_message=(
                        "I will pause the Editorial Session and "
                        "preserve the current state."
                    ),
                    may_continue_current_session=False,
                )

            if self._contains_any(
                lower,
                ("resume", "continue where we left off"),
            ):
                return DiscernmentDecision(
                    contribution_kind=ContributionKind.RESUME,
                    alignment=IntentAlignment.ALIGNED,
                    author_message=(
                        "We can resume from the preserved Editorial "
                        "Session state."
                    ),
                    may_continue_current_session=True,
                )

            if contribution.target_component is not None:
                return self._component_revision(
                    session,
                    contribution,
                )

            if self._looks_like_approval(lower):
                return DiscernmentDecision(
                    contribution_kind=ContributionKind.APPROVE,
                    alignment=IntentAlignment.ALIGNED,
                    author_message=(
                        "Approved work will be preserved unless you "
                        "explicitly choose to revise it later."
                    ),
                    may_continue_current_session=True,
                )

            if self._looks_like_rejection(lower):
                return self._clarify(
                    session,
                    "Which Publication Package component would you "
                    "like to revise?",
                )

            alignment = self.assess_alignment(
                session.intent,
                contribution,
            )

            if alignment is IntentAlignment.SEPARATE_INTENT:
                return DiscernmentDecision(
                    contribution_kind=(
                        ContributionKind.NEW_PUBLICATION
                    ),
                    alignment=alignment,
                    author_message=self.NEW_SESSION_MESSAGE,
                    may_continue_current_session=False,
                    recommend_new_session=True,
                    protected_components=tuple(
                        sorted(
                            session.approved_components,
                            key=lambda item: item.value,
                        )
                    ),
                    rationale=(
                        "The contribution does not materially overlap "
                        "with the established topic or scope.",
                        "Silent merging would weaken editorial "
                        "coherence and traceability.",
                    ),
                )

            if alignment is IntentAlignment.DIVERGING:
                return DiscernmentDecision(
                    contribution_kind=ContributionKind.CHANGE_ANGLE,
                    alignment=alignment,
                    author_message=self.SCOPE_EXPANSION_MESSAGE,
                    may_continue_current_session=False,
                    requires_clarification=True,
                    clarification_question=(
                        "Would you like to broaden the current "
                        "publication, or start a new Editorial Session?"
                    ),
                    protected_components=tuple(
                        sorted(
                            session.approved_components,
                            key=lambda item: item.value,
                        )
                    ),
                    rationale=(
                        "The new material is connected but would "
                        "materially broaden the agreed scope.",
                    ),
                )

            if alignment is IntentAlignment.AMBIGUOUS:
                return self._clarify(
                    session,
                    "Is this intended to support the current "
                    "publication, revise it, or begin a new one?",
                )

            kind = (
                ContributionKind.ADD_EVIDENCE
                if contribution.source_identifiers
                else ContributionKind.CONTINUE
            )

            message = (
                "This material supports the current Editorial Intent "
                "and can be incorporated without changing the "
                "publication objective."
            )

            return DiscernmentDecision(
                contribution_kind=kind,
                alignment=alignment,
                author_message=message,
                may_continue_current_session=True,
                protected_components=tuple(
                    sorted(
                        session.approved_components,
                        key=lambda item: item.value,
                    )
                ),
            )

        def assess_alignment(
            self,
            intent: EditorialIntent,
            contribution: Contribution,
        ) -> IntentAlignment:
            """Assess topic overlap without pretending certainty."""
            text = contribution.text.lower().strip()

            if not text:
                if contribution.source_identifiers:
                    return IntentAlignment.RELATED

                return IntentAlignment.AMBIGUOUS

            intent_terms = self._intent_terms(intent)

            contribution_terms = {
                token
                for token in self._tokens(text)
                if len(token) >= 4
            }

            if not contribution_terms:
                return IntentAlignment.AMBIGUOUS

            overlap = intent_terms & contribution_terms

            if not overlap:
                return IntentAlignment.SEPARATE_INTENT

            # A sourced contribution with meaningful topic overlap is
            # supporting material even when the complete Editorial
            # Intent contains a broader vocabulary.
            if contribution.source_identifiers:
                return IntentAlignment.RELATED

            ratio = len(overlap) / max(1, len(intent_terms))

            if ratio >= 0.40:
                return IntentAlignment.ALIGNED

            if ratio >= 0.20:
                return IntentAlignment.RELATED

            return IntentAlignment.DIVERGING

        def apply_decision(
            self,
            session: EditorialSession,
            decision: DiscernmentDecision,
        ) -> None:
            """Apply lifecycle decisions explicitly."""
            kind = decision.contribution_kind

            if kind is ContributionKind.PAUSE:
                session.pause()
            elif kind is ContributionKind.RESUME:
                session.resume()
            elif kind is ContributionKind.CANCEL:
                session.cancel()
            elif kind is ContributionKind.ABORT:
                session.abort()
            elif kind is ContributionKind.COMPLETE:
                session.complete()
            elif kind is ContributionKind.ARCHIVE:
                session.archive()

        def _declared_decision(
            self,
            session: EditorialSession,
            contribution: Contribution,
        ) -> DiscernmentDecision:
            kind = contribution.declared_kind

            assert kind is not None

            if kind is ContributionKind.NEW_PUBLICATION:
                return DiscernmentDecision(
                    contribution_kind=kind,
                    alignment=IntentAlignment.SEPARATE_INTENT,
                    author_message=self.NEW_SESSION_MESSAGE,
                    may_continue_current_session=False,
                    recommend_new_session=True,
                )

            if kind is ContributionKind.REVISE_COMPONENT:
                return self._component_revision(
                    session,
                    contribution,
                )

            if kind in {
                ContributionKind.PAUSE,
                ContributionKind.RESUME,
                ContributionKind.CANCEL,
                ContributionKind.ABORT,
                ContributionKind.COMPLETE,
                ContributionKind.ARCHIVE,
            }:
                return DiscernmentDecision(
                    contribution_kind=kind,
                    alignment=IntentAlignment.ALIGNED,
                    author_message=(
                        f"Editorial Guidance recognised: "
                        f"{kind.value.replace('_', ' ')}."
                    ),
                    may_continue_current_session=(
                        kind is ContributionKind.RESUME
                    ),
                )

            return DiscernmentDecision(
                contribution_kind=kind,
                alignment=IntentAlignment.ALIGNED,
                author_message=(
                    "The contribution can continue within the "
                    "current Editorial Session."
                ),
                may_continue_current_session=True,
            )

        def _component_revision(
            self,
            session: EditorialSession,
            contribution: Contribution,
        ) -> DiscernmentDecision:
            target = contribution.target_component

            if target is None:
                return self._clarify(
                    session,
                    "Which Publication Package component would you "
                    "like to revise?",
                )

            protected = tuple(
                sorted(
                    (
                        component
                        for component in session.approved_components
                        if component is not target
                    ),
                    key=lambda item: item.value,
                )
            )

            return DiscernmentDecision(
                contribution_kind=(
                    ContributionKind.REVISE_COMPONENT
                ),
                alignment=IntentAlignment.ALIGNED,
                author_message=(
                    f"I will focus on the "
                    f"{target.value.replace('_', ' ')} and preserve "
                    "unaffected approved work."
                ),
                may_continue_current_session=True,
                affected_components=(target,),
                protected_components=protected,
            )

        def _clarify(
            self,
            session: EditorialSession,
            question: str,
        ) -> DiscernmentDecision:
            return DiscernmentDecision(
                contribution_kind=(
                    ContributionKind.CLARIFICATION_REQUIRED
                ),
                alignment=IntentAlignment.AMBIGUOUS,
                author_message=question,
                may_continue_current_session=False,
                requires_clarification=True,
                clarification_question=question,
                protected_components=tuple(
                    sorted(
                        session.approved_components,
                        key=lambda item: item.value,
                    )
                ),
            )

        @staticmethod
        def _looks_like_approval(value: str) -> bool:
            return EditorialDiscernmentEngine._contains_any(
                value,
                (
                    "approved",
                    "looks good",
                    "keep this",
                    "accept this",
                ),
            )

        @staticmethod
        def _looks_like_rejection(value: str) -> bool:
            return EditorialDiscernmentEngine._contains_any(
                value,
                (
                    "i don't like",
                    "i do not like",
                    "reject this",
                    "change it",
                ),
            )

        @staticmethod
        def _contains_any(
            value: str,
            phrases: Iterable[str],
        ) -> bool:
            return any(
                phrase in value
                for phrase in phrases
            )

        @staticmethod
        def _tokens(value: str) -> set[str]:
            cleaned = "".join(
                character.lower()
                if character.isalnum()
                else " "
                for character in value
            )

            return {
                token
                for token in cleaned.split()
                if token
            }

        def _intent_terms(
            self,
            intent: EditorialIntent,
        ) -> set[str]:
            combined = " ".join(
                (
                    intent.primary_topic,
                    intent.editorial_objective,
                    intent.intended_audience,
                    intent.publication_goal,
                    *intent.scope_terms,
                )
            )

            return {
                token
                for token in self._tokens(combined)
                if len(token) >= 4
            }
    '''
)


EDITORIAL_GUIDANCE_RUNTIME = clean(
    '''
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
    '''
)


# ---------------------------------------------------------------------
# Constitutional documentation
# ---------------------------------------------------------------------

EDITORIAL_COHERENCE_PRINCIPLE = clean(
    """
    # Editorial Coherence and Intent Preservation

    ## Status

    Active constitutional principle for Version 1.0.

    ## Product Doctrine

    > Every feature must earn trust before it earns convenience.

    ## Governing Principle

    Every Editorial Session represents one coherent Editorial Intent.

    The Studio must protect:

    - the Author's intent,
    - the Editor's standards,
    - the Reader's confidence,
    - and the traceability of every source and editorial decision.

    ## One Editorial Intent per Session

    Each Editorial Session shall maintain:

    - Primary Topic
    - Editorial Objective
    - Intended Audience
    - Publication Goal
    - Primary Source Set
    - Supporting Sources
    - Editorial Scope

    ## Accepted Expansion

    New material may remain in the current session when it:

    - strengthens the existing argument,
    - supplies supporting evidence,
    - corrects a claim,
    - replaces a source,
    - refines the intended audience,
    - revises a Publication Package component,
    - or adds an Identity Asset.

    ## Separate Intent

    The Studio must recommend a new Editorial Session when new material
    introduces a materially different publication objective.

    The existing session must remain preserved.

    ## No Silent Scope Expansion

    The Studio must not significantly broaden the publication scope
    without making that change explicit to the Author.

    It should offer:

    - broaden the existing scope with approval,
    - preserve the existing scope,
    - or start a new Editorial Session.

    ## No Silent Merging

    The Studio must never silently combine unrelated URLs, documents,
    recordings, observations, or publication objectives into one
    Publication Package.

    ## Reader Test

    Before continuing, the Editor should be able to answer:

    > Would a reasonable Reader believe this was intentionally created
    > as one coherent piece?

    If the answer is uncertain, the Editor should pause and provide one
    concise clarification question.

    ## Author Authority

    Editorial Guidance is advisory.

    The Author retains publication authority, but the Studio must explain
    material editorial consequences before accepting a risky scope change.
    """
)


EDITORIAL_NEVER_EVENTS = clean(
    """
    # Editorial Never Events

    ## Status

    Active Version 1.0 guardrails.

    The Studio must never:

    1. Silently alter approved work.
    2. Silently regenerate dependent Publication Package components.
    3. Merge unrelated Editorial Intents into one session.
    4. Expand publication scope without informing the Author.
    5. Present Source Assessment as Evidence Verification.
    6. Present internal LMHS Editorial Risk as the main Author outcome.
    7. Claim certainty unsupported by the evidence.
    8. Fabricate sources, quotations, statistics, or attribution.
    9. Discard completed work without explicit Author intent.
    10. Use an Identity Asset without rights confirmation.
    11. Compromise Reader trust for speed or convenience.
    12. Prioritise automation over editorial clarity.
    13. Hide significant contradictions between sources.
    14. Continue after detecting a separate publication objective without
        making that change explicit.
    15. Leave a paused, cancelled, or aborted session in an inconsistent
        state.

    ## Engineering Interpretation

    A Never Event is an unacceptable product behaviour.

    It must be prevented by:

    - runtime rules,
    - tests,
    - documentation,
    - and capability acceptance criteria.
    """
)


EDITORIAL_SESSION_LIFECYCLE = clean(
    """
    # Editorial Session Lifecycle

    ## Status

    Active Version 1.0 lifecycle model.

    ## Workspace State

    Workspace State describes the lifecycle of the complete Editorial
    Workspace.

    Allowed states:

    - Created
    - Active
    - Waiting for Author
    - Paused
    - Cancelled
    - Aborted
    - Completed
    - Archived

    ## Stage State

    Stage State describes one Editorial Integrity stage.

    Allowed states:

    - Not Started
    - In Progress
    - Complete
    - Blocked

    Workspace State and Stage State are distinct.

    ## Cancelled

    Cancelled means the Author intentionally chose to end the session.

    ## Aborted

    Aborted means the session ended unexpectedly or was explicitly
    terminated before completion.

    Aborting must preserve:

    - Author material,
    - source provenance,
    - approvals,
    - Identity Asset metadata,
    - Publication Package components,
    - and session history.

    ## Resume

    A paused, waiting, or aborted session may be resumed when its project
    record remains available.

    Missing optional Identity Assets must not block resume.

    ## Completed

    Completed means the Publication Package and all required Editorial
    Integrity stages are complete.

    ## Archived

    Archived means the preserved session is no longer active.

    Archiving must not silently delete the Portable Editorial Project.
    """
)


# ---------------------------------------------------------------------
# Architecture and UX documentation
# ---------------------------------------------------------------------

EDITORIAL_DISCERNMENT_ARCHITECTURE = clean(
    """
    # Editorial Discernment Runtime

    ## Status

    Active runtime architecture for Capability 008.

    ## Internal Name

    Editorial Discernment Engine

    ## Author-Facing Name

    Editorial Guidance

    ## Purpose

    The runtime determines what each new Author contribution means in
    the context of the current Editorial Session.

    ## Supported Contribution Classes

    - Continue
    - Add Evidence
    - Replace Source
    - Correct Information
    - Revise Component
    - Change Angle
    - Change Audience
    - Request Research
    - Add Identity Asset
    - Approve
    - Reject
    - Pause
    - Resume
    - Cancel
    - Abort
    - Complete
    - Archive
    - New Publication
    - Clarification Required

    ## Intent Alignment

    New material is classified as:

    - Aligned
    - Related
    - Diverging
    - Separate Intent
    - Ambiguous

    ## Clarification Rule

    When ambiguity blocks safe progress, ask one concise clarification
    question.

    Do not create a chain of speculative questions.

    ## Preservation

    Approved Publication Package components remain protected unless the
    Author explicitly chooses to revise them.

    ## Evidence Boundary

    Discernment decides what a contribution means.

    Evidence Validation determines whether material claims are supported.

    Both responsibilities belong to Capability 008 but remain separate
    runtime concerns.
    """
)


EDITORIAL_INTENT_ARCHITECTURE = clean(
    """
    # Editorial Intent Runtime

    ## Purpose

    Editorial Intent is the session's editorial north star.

    It contains:

    - Primary Topic
    - Editorial Objective
    - Intended Audience
    - Publication Goal
    - Scope Terms
    - Primary Sources
    - Supporting Sources

    ## Alignment Decision

    Incoming material is compared with established intent.

    The initial deterministic runtime uses topic-term overlap as a
    conservative baseline.

    Future model-assisted interpretation may improve classification, but
    it must preserve the same constitutional behaviours.

    ## Supporting Material

    Supporting evidence, brand guidance, style references, logos, and
    headshots do not create a new Editorial Intent by themselves.

    ## Separate Publication

    Material with no meaningful relationship to the established topic or
    objective should be treated as a potential new publication.

    ## No Forced Merge

    The Studio must not merge separate publication objectives merely
    because the Author supplied them in one conversation.
    """
)


GUIDED_SESSION_UX = clean(
    """
    # Guided Editorial Session

    ## Purpose

    Editorial Guidance helps the Author understand:

    - where the session is,
    - what has been completed,
    - what is happening now,
    - what requires a decision,
    - and what comes next.

    ## Editorial Coherence Message

    Example:

    > This appears to introduce a different publication objective. To
    > preserve clarity and Reader trust, I recommend starting a new
    > Editorial Session. Your current work will remain exactly as it is.

    ## Scope Expansion Message

    Example:

    > This material would significantly broaden the current publication.
    > Would you like to expand the current scope, preserve it, or start a
    > new Editorial Session?

    ## Revision Message

    Example:

    > I will focus on the CTA and preserve unaffected approved work.

    This pattern applies to every Publication Package component, not only
    the headline.

    ## Abort Message

    Example:

    > I will mark this Editorial Session as Aborted while preserving the
    > work, approvals, provenance, and session history.

    ## Clarification

    Ask one concise question when ambiguity blocks safe progress.

    Example:

    > Is this intended to support the current publication, revise it, or
    > begin a new one?
    """
)


EDITORIAL_PROGRESS_UX = clean(
    """
    # Editorial Progress Display

    ## Session State

    Display Workspace State separately from Editorial Integrity stages.

    Example:

    ```text
    Editorial Workspace - Active

    ✓ Understanding your input
    ✓ Assessing your sources
    ◐ Verifying the evidence
    ○ Reviewing editorial risks
    ○ Creating your publication package
    ```

    ## Stage Symbols

    - `○` Not Started
    - `◐` In Progress
    - `✓` Complete
    - `!` Blocked

    ## Session State Examples

    - Editorial Workspace - Active
    - Editorial Workspace - Waiting for Author
    - Editorial Workspace - Paused
    - Editorial Workspace - Aborted
    - Editorial Workspace - Completed
    - Editorial Workspace - Archived

    ## No False Completion

    Workspace completion must not be inferred from the number of stages
    displayed.

    All required stages must be complete.
    """
)


ADR_009 = clean(
    """
    # ADR-009 - Adopt Editorial Discernment and Intent Preservation

    ## Status

    Accepted

    ## Date

    2026-08-01

    ## Context

    Editorial Intake can recognise material, but the Studio also needs to
    determine what each new contribution means.

    Without Editorial Discernment, unrelated sources or publication
    objectives could be merged into incoherent work that undermines the
    Author's credibility and Reader trust.

    ## Decision

    Adopt the Editorial Discernment Engine internally and Editorial
    Guidance as the Author-facing experience.

    Implement:

    - one Editorial Intent per Editorial Session,
    - Intent Alignment,
    - Editorial Coherence Guard,
    - No Silent Scope Expansion,
    - one-question clarification,
    - approved-component protection,
    - Workspace lifecycle,
    - and Editorial Never Events.

    ## Workspace Lifecycle

    Workspace State is distinct from Stage State.

    Distinguish Cancelled from Aborted. Cancellation is deliberate Author termination.

    Abortion is exceptional or interrupted termination.

    Both preserve the project record unless the Author explicitly
    deletes it.

    ## Editorial Authority

    The Author retains final publication authority.

    The Editor must explain material trust or coherence concerns before
    accepting a risky change.

    ## Consequences

    ### Positive

    - Protects one coherent publication objective
    - Prevents silent source blending
    - Preserves approved work
    - Makes pause, resume, cancel, and abort explicit
    - Creates testable Editorial Guidance
    - Improves Reader trust

    ### Costs

    - Requires conservative ambiguity handling
    - Requires session state management
    - Requires intent metadata
    - Requires future model-assisted classification to remain governed by
      deterministic constitutional rules

    ## Alternatives Rejected

    ### Merge Everything Supplied

    Rejected because availability does not imply editorial coherence.

    ### Block Every Scope Change

    Rejected because the Author retains authority.

    ### Ask Multiple Clarifying Questions

    Rejected because the Editor should infer before asking and minimise
    Author effort.
    """
)


ARCHITECTURE_BASELINE = clean(
    f"""
    # Architecture Baseline - {ARCHITECTURE_BASELINE_VERSION}

    ## Status

    Current Version 1.0 runtime baseline.

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
    2026.08.01v04
    ```

    ## Reason for Revision

    Establish:

    - Editorial Discernment Engine
    - Editorial Guidance
    - Editorial Intent
    - Editorial Coherence Guard
    - No Silent Scope Expansion
    - Editorial Never Events
    - Workspace lifecycle
    - Stage lifecycle
    - Pause, resume, cancel, abort, complete, and archive behaviour

    ## Constitutional Impact

    This baseline adopts the rule:

    > One Editorial Intent per Editorial Session.

    It also adopts the Product Doctrine:

    > Every feature must earn trust before it earns convenience.

    ## Capability Boundary

    Capability 008 now contains two related but distinct concerns:

    1. Editorial Discernment - what a contribution means
    2. Evidence Validation - whether material claims are supported

    Editorial Discernment is implemented in this baseline.

    Evidence-validation depth may continue through subsequent Capability
    008 increments without changing the constitutional rules.

    ## VCM

    The same-day architecture family advances to `v05`.
    """
)


CAPABILITY_DEMO = clean(
    """
    # Capability 008 Demo - Editorial Discernment

    ## Objective

    Demonstrate a Guided Editorial Session that protects editorial
    coherence while preserving Author authority.

    ## Scenario 1 - Related Source

    Current topic:

    ```text
    AI governance in financial services
    ```

    New material:

    ```text
    A bank regulator's AI governance guidance
    ```

    Expected:

    - Alignment is Aligned or Related
    - Current session continues
    - No new session recommended

    ## Scenario 2 - Separate Publication

    Current topic:

    ```text
    AI governance in financial services
    ```

    New material:

    ```text
    Leadership lessons from cricket
    ```

    Expected:

    - Separate Intent detected
    - Current session preserved
    - New Editorial Session recommended
    - No silent merging

    ## Scenario 3 - Component Revision

    Author says:

    ```text
    I do not like this CTA.
    ```

    Expected:

    - CTA is the affected component
    - Other approved components remain protected
    - No unrelated regeneration

    ## Scenario 4 - Ambiguous Rejection

    Author says:

    ```text
    I do not like this.
    ```

    Expected:

    - One concise clarification question
    - No speculative question chain

    ## Scenario 5 - Abort

    Author says:

    ```text
    Abort this session.
    ```

    Expected:

    - Workspace State becomes Aborted
    - Approvals remain preserved
    - Provenance remains preserved
    - Resume remains possible

    ## Scenario 6 - Scope Expansion

    New material is related but changes the article from one product to
    an industry-wide comparison.

    Expected:

    - Diverging classification
    - Scope expansion made explicit
    - Author chooses broaden, preserve, or new session

    ## Completion

    Capability 008 passes when the Studio protects coherence without
    taking publication authority away from the Author.
    """
)


# ---------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------

RUNTIME_TESTS = clean(
    '''
    """Runtime tests for Capability 008."""

    from __future__ import annotations

    import unittest

    from studio.editorial_discernment import (
        Contribution,
        ContributionKind,
        EditorialComponent,
        EditorialDiscernmentEngine,
        EditorialIntent,
        EditorialSession,
        IntentAlignment,
        StageState,
        WorkspaceState,
    )


    class Capability008DiscernmentTests(unittest.TestCase):
        def setUp(self) -> None:
            self.engine = EditorialDiscernmentEngine()

            self.intent = EditorialIntent(
                primary_topic=(
                    "AI governance in financial services"
                ),
                editorial_objective=(
                    "Explain why accountable AI governance "
                    "is an operating discipline"
                ),
                intended_audience=(
                    "banking executives and risk leaders"
                ),
                publication_goal=(
                    "publish a professional LinkedIn article"
                ),
                scope_terms=(
                    "governance",
                    "accountability",
                    "financial services",
                    "banking",
                    "risk",
                ),
            )

            self.session = EditorialSession(
                intent=self.intent
            )

            self.session.activate()

        def test_intent_is_defined(self) -> None:
            self.assertTrue(self.intent.is_defined())

        def test_workspace_and_stage_states_are_distinct(
            self,
        ) -> None:
            self.assertEqual(
                self.session.workspace_state,
                WorkspaceState.ACTIVE,
            )
            self.assertEqual(
                self.session.stage_states[1],
                StageState.NOT_STARTED,
            )

        def test_related_source_continues(self) -> None:
            decision = self.engine.classify(
                self.session,
                Contribution(
                    text=(
                        "Banking regulators are publishing "
                        "additional AI governance guidance."
                    ),
                    source_identifiers=("regulator.example",),
                ),
            )

            self.assertIn(
                decision.alignment,
                {
                    IntentAlignment.ALIGNED,
                    IntentAlignment.RELATED,
                },
            )
            self.assertTrue(
                decision.may_continue_current_session
            )
            self.assertFalse(
                decision.recommend_new_session
            )

        def test_unrelated_topic_recommends_new_session(
            self,
        ) -> None:
            decision = self.engine.classify(
                self.session,
                Contribution(
                    text=(
                        "Leadership lessons from international "
                        "cricket captains"
                    )
                ),
            )

            self.assertEqual(
                decision.alignment,
                IntentAlignment.SEPARATE_INTENT,
            )
            self.assertTrue(
                decision.recommend_new_session
            )
            self.assertFalse(
                decision.may_continue_current_session
            )
            self.assertIn(
                "different publication objective",
                decision.author_message,
            )

        def test_no_silent_scope_expansion(self) -> None:
            decision = self.engine.classify(
                self.session,
                Contribution(
                    text=(
                        "Compare banking AI governance with "
                        "healthcare, retail, manufacturing, and "
                        "public-sector governance."
                    )
                ),
            )

            self.assertIn(
                decision.alignment,
                {
                    IntentAlignment.DIVERGING,
                    IntentAlignment.SEPARATE_INTENT,
                },
            )

            self.assertTrue(
                decision.recommend_new_session
                or decision.requires_clarification
            )

        def test_targeted_cta_revision(self) -> None:
            self.session.approve(
                EditorialComponent.HEADLINE
            )
            self.session.approve(
                EditorialComponent.HOOK
            )

            decision = self.engine.classify(
                self.session,
                Contribution(
                    text="I do not like this CTA.",
                    target_component=EditorialComponent.CTA,
                    declared_kind=(
                        ContributionKind.REVISE_COMPONENT
                    ),
                ),
            )

            self.assertEqual(
                decision.affected_components,
                (EditorialComponent.CTA,),
            )
            self.assertIn(
                EditorialComponent.HEADLINE,
                decision.protected_components,
            )
            self.assertIn(
                EditorialComponent.HOOK,
                decision.protected_components,
            )

        def test_revision_applies_to_hero_visual(self) -> None:
            decision = self.engine.classify(
                self.session,
                Contribution(
                    text="Revise the Hero Visual.",
                    target_component=(
                        EditorialComponent.HERO_VISUAL
                    ),
                    declared_kind=(
                        ContributionKind.REVISE_COMPONENT
                    ),
                ),
            )

            self.assertEqual(
                decision.affected_components,
                (EditorialComponent.HERO_VISUAL,),
            )

        def test_ambiguous_rejection_asks_one_question(
            self,
        ) -> None:
            decision = self.engine.classify(
                self.session,
                Contribution(text="I do not like this."),
            )

            self.assertTrue(
                decision.requires_clarification
            )
            self.assertIsNotNone(
                decision.clarification_question
            )
            self.assertEqual(
                decision.author_message.count("?"),
                1,
            )

        def test_pause_preserves_state(self) -> None:
            self.session.approve(
                EditorialComponent.HEADLINE
            )

            decision = self.engine.classify(
                self.session,
                Contribution(text="Pause this for now."),
            )

            self.engine.apply_decision(
                self.session,
                decision,
            )

            self.assertEqual(
                self.session.workspace_state,
                WorkspaceState.PAUSED,
            )
            self.assertIn(
                EditorialComponent.HEADLINE,
                self.session.approved_components,
            )

        def test_resume_after_pause(self) -> None:
            self.session.pause()

            decision = self.engine.classify(
                self.session,
                Contribution(text="Resume."),
            )

            self.engine.apply_decision(
                self.session,
                decision,
            )

            self.assertEqual(
                self.session.workspace_state,
                WorkspaceState.ACTIVE,
            )

        def test_abort_preserves_approvals(self) -> None:
            self.session.approve(
                EditorialComponent.HEADLINE
            )

            decision = self.engine.classify(
                self.session,
                Contribution(text="Abort this session."),
            )

            self.engine.apply_decision(
                self.session,
                decision,
            )

            self.assertEqual(
                self.session.workspace_state,
                WorkspaceState.ABORTED,
            )
            self.assertIn(
                EditorialComponent.HEADLINE,
                self.session.approved_components,
            )
            self.assertTrue(
                self.session.preserved_events
            )

        def test_aborted_session_can_resume(self) -> None:
            self.session.abort()
            self.session.resume()

            self.assertEqual(
                self.session.workspace_state,
                WorkspaceState.ACTIVE,
            )

        def test_cancel_is_distinct_from_abort(self) -> None:
            self.session.cancel()

            self.assertEqual(
                self.session.workspace_state,
                WorkspaceState.CANCELLED,
            )
            self.assertNotEqual(
                self.session.workspace_state,
                WorkspaceState.ABORTED,
            )

        def test_complete_requires_all_stages(self) -> None:
            with self.assertRaises(ValueError):
                self.session.complete()

        def test_complete_after_all_stages(self) -> None:
            for number in range(1, 6):
                self.session.mark_stage(
                    number,
                    StageState.COMPLETE,
                )

            self.session.complete()

            self.assertEqual(
                self.session.workspace_state,
                WorkspaceState.COMPLETED,
            )

        def test_completed_session_can_archive(self) -> None:
            for number in range(1, 6):
                self.session.mark_stage(
                    number,
                    StageState.COMPLETE,
                )

            self.session.complete()
            self.session.archive()

            self.assertEqual(
                self.session.workspace_state,
                WorkspaceState.ARCHIVED,
            )

        def test_empty_contribution_requires_clarification(
            self,
        ) -> None:
            decision = self.engine.classify(
                self.session,
                Contribution(text=""),
            )

            self.assertEqual(
                decision.contribution_kind,
                ContributionKind.CLARIFICATION_REQUIRED,
            )

        def test_declared_new_publication_is_preserved(
            self,
        ) -> None:
            decision = self.engine.classify(
                self.session,
                Contribution(
                    text="Start a piece about cricket.",
                    declared_kind=(
                        ContributionKind.NEW_PUBLICATION
                    ),
                ),
            )

            self.assertTrue(
                decision.recommend_new_session
            )
            self.assertTrue(
                decision.preserve_existing_work
            )


    if __name__ == "__main__":
        unittest.main()
    '''
)


GUIDANCE_TESTS = clean(
    '''
    """Author-facing Editorial Guidance tests."""

    from __future__ import annotations

    import unittest

    from studio.editorial_discernment import (
        Contribution,
        EditorialDiscernmentEngine,
        EditorialIntent,
        EditorialSession,
        StageState,
    )
    from studio.editorial_guidance import (
        guidance_view,
        render_progress,
    )


    class Capability008GuidanceTests(unittest.TestCase):
        def setUp(self) -> None:
            self.session = EditorialSession(
                intent=EditorialIntent(
                    primary_topic="AI governance",
                    editorial_objective=(
                        "Explain accountable governance"
                    ),
                    intended_audience="executives",
                    publication_goal="LinkedIn article",
                    scope_terms=("governance", "accountable"),
                )
            )

            self.session.activate()

        def test_progress_displays_session_state(
            self,
        ) -> None:
            lines = render_progress(self.session)

            self.assertEqual(
                lines[0],
                "Editorial Workspace - Active",
            )

        def test_progress_uses_all_five_stages(
            self,
        ) -> None:
            lines = render_progress(self.session)

            self.assertEqual(len(lines), 6)

        def test_progress_distinguishes_in_progress(
            self,
        ) -> None:
            self.session.mark_stage(
                1,
                StageState.COMPLETE,
            )
            self.session.mark_stage(
                2,
                StageState.IN_PROGRESS,
            )

            lines = render_progress(self.session)

            self.assertIn(
                "✓ Understanding your input",
                lines,
            )
            self.assertIn(
                "◐ Assessing your sources",
                lines,
            )

        def test_separate_intent_guidance_is_conversational(
            self,
        ) -> None:
            engine = EditorialDiscernmentEngine()

            decision = engine.classify(
                self.session,
                Contribution(
                    text="Cricket captain leadership lessons"
                ),
            )

            view = guidance_view(
                self.session,
                decision,
            )

            self.assertIn(
                "Reader trust",
                view.guidance,
            )
            self.assertNotIn(
                "ERROR",
                view.guidance,
            )


    if __name__ == "__main__":
        unittest.main()
    '''
)


DOCUMENTATION_TESTS = clean(
    '''
    """Documentation tests for Capability 008."""

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


    class Capability008DocumentationTests(unittest.TestCase):
        def test_coherence_principle_exists(self) -> None:
            self.assertTrue(
                (
                    ROOT
                    / "docs"
                    / "constitution"
                    / "Editorial_Coherence_Principle.md"
                ).is_file()
            )

        def test_one_intent_per_session(self) -> None:
            content = normalized(
                "docs/constitution/"
                "Editorial_Coherence_Principle.md"
            )

            self.assertIn(
                "one coherent Editorial Intent",
                content,
            )

        def test_no_silent_scope_expansion(self) -> None:
            content = normalized(
                "docs/constitution/"
                "Editorial_Coherence_Principle.md"
            )

            self.assertIn(
                "No Silent Scope Expansion",
                content,
            )

        def test_never_events_exist(self) -> None:
            content = normalized(
                "docs/constitution/Editorial_Never_Events.md"
            )

            self.assertIn(
                "Silently alter approved work",
                content,
            )
            self.assertIn(
                "Merge unrelated Editorial Intents",
                content,
            )

        def test_cancel_and_abort_are_distinct(self) -> None:
            content = normalized(
                "docs/constitution/"
                "Editorial_Session_Lifecycle.md"
            )

            self.assertIn(
                "Cancelled means",
                content,
            )
            self.assertIn(
                "Aborted means",
                content,
            )

        def test_adr_009_exists(self) -> None:
            self.assertTrue(
                (
                    ROOT
                    / "docs"
                    / "architecture"
                    / "adr"
                    / (
                        "ADR-009-adopt-editorial-discernment-"
                        "and-intent-preservation.md"
                    )
                ).is_file()
            )

        def test_baseline_v05_exists(self) -> None:
            self.assertTrue(
                (
                    ROOT
                    / "docs"
                    / "architecture"
                    / "baselines"
                    / "Architecture_Baseline_2026.08.01v05.md"
                ).is_file()
            )

        def test_internal_and_external_names(self) -> None:
            content = normalized(
                "docs/architecture/"
                "Editorial_Discernment_Runtime.md"
            )

            self.assertIn(
                "Editorial Discernment Engine",
                content,
            )
            self.assertIn(
                "Editorial Guidance",
                content,
            )


    if __name__ == "__main__":
        unittest.main()
    '''
)


# ---------------------------------------------------------------------
# Managed documentation updates
# ---------------------------------------------------------------------

CONSTITUTION_BLOCK = clean(
    """
    ## Product Doctrine

    > Every feature must earn trust before it earns convenience.

    ## Editorial Coherence

    Each Editorial Session maintains one coherent Editorial Intent.

    The Studio must not silently merge unrelated publication objectives
    or materially expand scope without informing the Author.

    Editorial Guidance protects the Author's intent, the Editor's
    standards, and the Reader's confidence.
    """
)


CANONICAL_VOCABULARY_BLOCK = clean(
    """
    ## Capability 008 Vocabulary

    ### Editorial Discernment Engine

    Internal runtime that interprets what a new Author contribution
    means.

    ### Editorial Guidance

    Author-facing expression of Editorial Discernment.

    ### Editorial Intent

    The single coherent publication objective for one Editorial Session.

    ### Intent Alignment

    The relationship between new material and the existing Editorial
    Intent:

    - Aligned
    - Related
    - Diverging
    - Separate Intent
    - Ambiguous

    ### Workspace State

    Lifecycle of the complete Editorial Workspace.

    ### Stage State

    Lifecycle of one Editorial Integrity stage.

    Workspace State and Stage State are not synonyms.
    """
)


START_HERE_BLOCK = clean(
    """
    ## Capability 008 Governance

    Before changing session behaviour, read:

    - `constitution/Editorial_Coherence_Principle.md`
    - `constitution/Editorial_Never_Events.md`
    - `constitution/Editorial_Session_Lifecycle.md`
    - `architecture/Editorial_Discernment_Runtime.md`
    - `architecture/Editorial_Intent_Runtime.md`

    Governing rule:

    > One Editorial Intent per Editorial Session.
    """
)


README_BLOCK = clean(
    """
    ## Capability 008 - Editorial Discernment

    Capability 008 adds:

    - Editorial Discernment Engine
    - Author-facing Editorial Guidance
    - Editorial Intent
    - Editorial Coherence Guard
    - No Silent Scope Expansion
    - Workspace lifecycle
    - Pause, resume, cancel, abort, complete, and archive behaviour
    - Approved-component protection
    - One-question clarification
    """
)


CURRENT_FOCUS_BLOCK = clean(
    """
    ## Capability 008 Active Focus

    The current Product focus is Editorial Discernment:

    - interpret each new Author contribution,
    - preserve one coherent Editorial Intent,
    - accept related supporting material,
    - detect separate publication objectives,
    - prevent silent scope expansion,
    - protect approved work,
    - and manage the Editorial Session lifecycle.

    Evidence-validation depth remains part of Capability 008's next
    implementation increment.
    """
)


PRD_BLOCK = clean(
    """
    ## Capability 008 Requirements

    The Product shall:

    - maintain one Editorial Intent per Editorial Session;
    - classify new material as Aligned, Related, Diverging, Separate
      Intent, or Ambiguous;
    - recommend a new Editorial Session for separate publication
      objectives;
    - never silently merge unrelated sources;
    - never silently expand scope;
    - ask one concise clarification question when ambiguity blocks safe
      progress;
    - preserve approved Publication Package components;
    - distinguish Workspace State from Stage State;
    - support pause, resume, cancel, abort, complete, and archive;
    - preserve work and provenance after abort;
    - and present Editorial Guidance rather than internal engine language
      to the Author.
    """
)


RELEASE_BLOCK = clean(
    """
    ## Capability 008 Release Contribution

    Capability 008 adds the Guided Editorial Session foundation.

    It protects editorial coherence, identifies separate publication
    objectives, preserves approved work, and introduces explicit
    Editorial Workspace lifecycle states.

    It does not permit silent merging of unrelated sources or intents.
    """
)


ROADMAP_BLOCK = clean(
    """
    ## Capability 008 - Editorial Discernment

    Status:

    ```text
    In implementation
    ```

    Delivered in this increment:

    - [x] Editorial Intent
    - [x] Editorial Discernment Engine
    - [x] Editorial Guidance
    - [x] Intent Alignment
    - [x] Editorial Coherence Guard
    - [x] No Silent Scope Expansion
    - [x] Workspace lifecycle
    - [x] Stage lifecycle
    - [x] Pause
    - [x] Resume
    - [x] Cancel
    - [x] Abort
    - [x] Complete
    - [x] Archive
    - [x] Approved-component protection
    - [x] One-question clarification
    - [x] Runtime tests
    - [x] Capability demo

    Next Capability 008 increment:

    - Evidence Validation
    - Claim classification
    - Corroboration
    - Temporal Integrity
    - LMHS Editorial Risk
    - Editorial Confidence translation
    """
)


CHANGELOG_BLOCK = clean(
    f"""
    ## Capability 008 - Editorial Discernment

    ### Added

    - Editorial Discernment Engine
    - Editorial Guidance
    - Editorial Intent
    - Intent Alignment
    - Editorial Coherence Guard
    - No Silent Scope Expansion
    - Editorial Never Events
    - Workspace lifecycle
    - Stage lifecycle
    - Pause, resume, cancel, abort, complete, and archive behaviour
    - Approved-component protection
    - One-question clarification
    - ADR-009
    - Architecture Baseline {ARCHITECTURE_BASELINE_VERSION}
    - Capability 008 demo
    - Runtime, guidance, and documentation tests

    ### Changed

    - Capability 008 now explicitly separates Editorial Discernment from
      Evidence Validation
    - Separate publication objectives are no longer silently merged
    - Workspace State and Stage State are now distinct
    - Aborted sessions preserve work, provenance, and approvals
    """
)


DEFINITION_OF_DONE_BLOCK = clean(
    """
    ## Capability 008 Completion Additions

    Confirm:

    - one Editorial Intent is maintained per session;
    - related material may continue;
    - separate publication objectives recommend a new session;
    - no silent scope expansion occurs;
    - ambiguous intent produces one concise clarification question;
    - approved components remain protected;
    - Workspace State and Stage State remain distinct;
    - abort preserves work and provenance;
    - Author-facing language uses Editorial Guidance;
    - runtime tests pass;
    - documentation tests pass;
    - and repository validation passes.
    """
)


DECISION_LOG_BLOCK = clean(
    f"""
    ## Capability 008 Decisions

    | Date | Level | Decision | Rationale |
    |---|---:|---|---|
    | 2026-08-01 | D4 | Adopt one Editorial Intent per Editorial Session | A publication must remain coherent and traceable. |
    | 2026-08-01 | D4 | Adopt Editorial Discernment Engine internally | The Studio must interpret what new contributions mean. |
    | 2026-08-01 | D4 | Use Editorial Guidance with Authors | Internal engine language should not dominate the Author experience. |
    | 2026-08-01 | D4 | Adopt No Silent Scope Expansion | Material scope changes require Author awareness. |
    | 2026-08-01 | D4 | Adopt Editorial Never Events | Unacceptable trust failures require explicit guardrails. |
    | 2026-08-01 | D4 | Separate Workspace State from Stage State | Session lifecycle and work progress are different concerns. |
    | 2026-08-01 | D4 | Distinguish Cancelled from Aborted | Deliberate Author cancellation differs from exceptional termination. |
    | 2026-08-01 | D4 | Preserve aborted work | Interruption must not destroy provenance, approvals, or project history. |
    | 2026-08-01 | D4 | Ask one clarification question | Minimise Author effort while avoiding unsafe assumptions. |
    | 2026-08-01 | D4 | Create Architecture Baseline {ARCHITECTURE_BASELINE_VERSION} | Editorial Discernment becomes part of the Version 1.0 runtime baseline. |
    """
)


SCORECARD_BLOCK = clean(
    """
    ## Capability 008 Progress

    | Area | Status | Evidence |
    |---|---|---|
    | Editorial Intent | Complete | Runtime tests |
    | Editorial Discernment | Complete | `studio/editorial_discernment.py` |
    | Editorial Guidance | Complete | `studio/editorial_guidance.py` |
    | Editorial Coherence Guard | Complete | Runtime tests |
    | No Silent Scope Expansion | Complete | Runtime and constitutional tests |
    | Workspace lifecycle | Complete | Runtime tests |
    | Approved-component protection | Complete | Runtime tests |
    | One-question clarification | Complete | Runtime tests |
    | Evidence Validation | Next increment | Capability 008 continuation |
    | LMHS Editorial Risk | Next increment | Capability 008 continuation |
    """
)


DECISION_REGISTER_BLOCK = clean(
    """
    ## Capability 008 Constitutional Decisions

    | Decision | Status | Adopted | Primary Evidence |
    |---|---|---|---|
    | Every feature must earn trust before convenience | Accepted | 2026-08-01 | Constitution |
    | One Editorial Intent per Editorial Session | Accepted | 2026-08-01 | Editorial Coherence Principle |
    | No Silent Scope Expansion | Accepted | 2026-08-01 | Editorial Coherence Principle |
    | Unrelated publication objectives are not silently merged | Accepted | 2026-08-01 | Editorial Never Events |
    | Workspace State is distinct from Stage State | Accepted | 2026-08-01 | Editorial Session Lifecycle |
    | Cancelled is distinct from Aborted | Accepted | 2026-08-01 | Editorial Session Lifecycle |
    | Aborted work remains preserved | Accepted | 2026-08-01 | Editorial Session Lifecycle |
    | Ambiguity produces one concise clarification question | Accepted | 2026-08-01 | ADR-009 |
    """
)


MARKER_BLOCKS = {
    "docs/constitution/Constitution.md": (
        "CAPABILITY_008_CONSTITUTION",
        CONSTITUTION_BLOCK,
    ),
    "docs/constitution/Canonical_Vocabulary.md": (
        "CAPABILITY_008_CANONICAL_VOCABULARY",
        CANONICAL_VOCABULARY_BLOCK,
    ),
    "docs/constitution/Constitutional_Decision_Register.md": (
        "CAPABILITY_008_DECISION_REGISTER",
        DECISION_REGISTER_BLOCK,
    ),
    "docs/START_HERE.md": (
        "CAPABILITY_008_START_HERE",
        START_HERE_BLOCK,
    ),
    "README.md": (
        "CAPABILITY_008_README",
        README_BLOCK,
    ),
    "docs/product/Current_Product_Focus.md": (
        "CAPABILITY_008_CURRENT_FOCUS",
        CURRENT_FOCUS_BLOCK,
    ),
    "docs/product/PRD_v1.3.md": (
        "CAPABILITY_008_PRD",
        PRD_BLOCK,
    ),
    "docs/product/Release_v1.0.md": (
        "CAPABILITY_008_RELEASE",
        RELEASE_BLOCK,
    ),
    "docs/product/Decision_Log.md": (
        "CAPABILITY_008_DECISION_LOG",
        DECISION_LOG_BLOCK,
    ),
    "docs/architecture/Definition_of_Done.md": (
        "CAPABILITY_008_DEFINITION_OF_DONE",
        DEFINITION_OF_DONE_BLOCK,
    ),
    "docs/VERSION_ONE_SCORECARD.md": (
        "CAPABILITY_008_SCORECARD",
        SCORECARD_BLOCK,
    ),
    "ROADMAP.md": (
        "CAPABILITY_008_ROADMAP",
        ROADMAP_BLOCK,
    ),
    "CHANGELOG.md": (
        "CAPABILITY_008_CHANGELOG",
        CHANGELOG_BLOCK,
    ),
}


NEW_FILES = {
    "studio/editorial_discernment.py":
        EDITORIAL_DISCERNMENT_RUNTIME,

    "studio/editorial_guidance.py":
        EDITORIAL_GUIDANCE_RUNTIME,

    (
        "docs/constitution/"
        "Editorial_Coherence_Principle.md"
    ):
        EDITORIAL_COHERENCE_PRINCIPLE,

    (
        "docs/constitution/"
        "Editorial_Never_Events.md"
    ):
        EDITORIAL_NEVER_EVENTS,

    (
        "docs/constitution/"
        "Editorial_Session_Lifecycle.md"
    ):
        EDITORIAL_SESSION_LIFECYCLE,

    (
        "docs/architecture/"
        "Editorial_Discernment_Runtime.md"
    ):
        EDITORIAL_DISCERNMENT_ARCHITECTURE,

    (
        "docs/architecture/"
        "Editorial_Intent_Runtime.md"
    ):
        EDITORIAL_INTENT_ARCHITECTURE,

    "docs/ui/Guided_Editorial_Session.md":
        GUIDED_SESSION_UX,

    "docs/ui/Editorial_Progress_Display.md":
        EDITORIAL_PROGRESS_UX,

    (
        "docs/architecture/adr/"
        "ADR-009-adopt-editorial-discernment-"
        "and-intent-preservation.md"
    ):
        ADR_009,

    (
        "docs/architecture/baselines/"
        "Architecture_Baseline_2026.08.01v05.md"
    ):
        ARCHITECTURE_BASELINE,

    (
        "docs/demos/"
        "Capability-008-Editorial-Discernment.md"
    ):
        CAPABILITY_DEMO,

    (
        "tests/"
        "test_capability008_editorial_discernment.py"
    ):
        RUNTIME_TESTS,

    (
        "tests/"
        "test_capability008_editorial_guidance.py"
    ):
        GUIDANCE_TESTS,

    (
        "tests/"
        "test_capability008_documentation.py"
    ):
        DOCUMENTATION_TESTS,
}


# ---------------------------------------------------------------------
# Errors and command execution
# ---------------------------------------------------------------------

class CapabilityError(RuntimeError):
    """Raised when Capability 008 cannot proceed safely."""


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
    """Run a command and parse JSON output."""
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
    """Require the Capability 008 feature branch."""
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
    """Detect incomplete or damaged paste."""
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
    """Return complete Git porcelain lines."""
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
    """Permit only expected Capability 008 changes."""
    expected_paths = (
        set(NEW_FILES)
        | set(MARKER_BLOCKS)
        | {SCRIPT_RELATIVE_PATH}
    )

    unexpected: list[str] = []

    for line in working_tree_lines(root):
        relative = line[3:].strip()

        if " -> " in relative:
            relative = relative.split(
                " -> ",
                1,
            )[1].strip()

        if relative not in expected_paths:
            unexpected.append(line)

    if unexpected:
        raise CapabilityError(
            "Unexpected working-tree changes exist:\n"
            + "\n".join(unexpected)
            + "\n\nOnly expected Capability 008 files and "
            "managed-document updates are allowed."
        )

    print(
        "Working tree contains only expected "
        "Capability 008 changes."
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
        before = original.split(
            start,
            1,
        )[0].rstrip()

        after = original.split(
            end,
            1,
        )[1].lstrip()

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
    """Write deterministic Capability 008 files."""
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
    """Update complementary documents."""
    for relative, (
        marker_name,
        content,
    ) in MARKER_BLOCKS.items():
        upsert_managed_block(
            root / relative,
            marker_name,
            content,
        )

        print(f"Updated {relative}")


def apply_local_changes(root: Path) -> None:
    """Apply Capability 008 locally."""
    write_new_files(root)
    update_existing_documents(root)

    print()
    print(
        "Capability 008 Editorial Discernment files "
        "have been written."
    )


# ---------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------

REQUIRED_FILES = tuple(NEW_FILES.keys())


def validate_required_files(root: Path) -> None:
    """Confirm every required file exists."""
    missing = [
        relative
        for relative in REQUIRED_FILES
        if not (root / relative).is_file()
    ]

    if missing:
        raise CapabilityError(
            "Missing Capability 008 files:\n"
            + "\n".join(
                f"  - {relative}"
                for relative in missing
            )
        )

    print("All required Capability 008 files are present.")


def validate_product_language(root: Path) -> None:
    """Validate locked Capability 008 decisions."""
    checks: dict[str, tuple[str, ...]] = {
        (
            "docs/constitution/"
            "Editorial_Coherence_Principle.md"
        ): (
            "Every feature must earn trust before it earns convenience.",
            "one coherent Editorial Intent",
            "No Silent Scope Expansion",
            "never silently combine unrelated",
        ),

        (
            "docs/constitution/"
            "Editorial_Never_Events.md"
        ): (
            "Silently alter approved work",
            "Merge unrelated Editorial Intents",
            "Leave a paused, cancelled, or aborted session",
        ),

        (
            "docs/constitution/"
            "Editorial_Session_Lifecycle.md"
        ): (
            "Cancelled means",
            "Aborted means",
            "Workspace State and Stage State are distinct",
        ),

        (
            "docs/architecture/"
            "Editorial_Discernment_Runtime.md"
        ): (
            "Editorial Discernment Engine",
            "Editorial Guidance",
            "ask one concise clarification question",
        ),

        (
            "docs/architecture/adr/"
            "ADR-009-adopt-editorial-discernment-"
            "and-intent-preservation.md"
        ): (
            "one Editorial Intent per Editorial Session",
            "No Silent Scope Expansion",
            "Cancelled from Aborted",
        ),

        (
            "docs/architecture/baselines/"
            "Architecture_Baseline_2026.08.01v05.md"
        ): (
            ARCHITECTURE_BASELINE_VERSION,
            "Editorial Discernment Engine",
            "One Editorial Intent per Editorial Session",
        ),
    }

    for relative, phrases in checks.items():
        content = normalize(
            (root / relative).read_text(
                encoding="utf-8"
            )
        )

        for phrase in phrases:
            if phrase not in content:
                raise CapabilityError(
                    f"Expected phrase '{phrase}' "
                    f"in {relative}."
                )

    print(
        "Capability 008 product-language validation passed."
    )


def run_repository_validation(root: Path) -> None:
    """Run compilation, unit tests, and repository validation."""
    run(
        [
            sys.executable,
            "-m",
            "compileall",
            "-q",
            "studio",
            "scripts",
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
        "Capability 008 repository validation passed."
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
    print("Capability 008 Editorial Discernment preview:")
    print()

    print("New files:")

    for relative in NEW_FILES:
        print(f"  - {relative}")

    print("\nManaged documentation updates:")

    for relative in MARKER_BLOCKS:
        print(f"  - {relative}")

    print("\nDecisions being implemented:")

    decisions = (
        "Adopt the Product Doctrine",
        "Adopt one Editorial Intent per Editorial Session",
        "Implement the Editorial Discernment Engine",
        "Use Editorial Guidance with Authors",
        "Implement Intent Alignment",
        "Implement the Editorial Coherence Guard",
        "Prevent silent merging of unrelated material",
        "Prevent silent scope expansion",
        "Protect approved Publication Package components",
        "Ask one concise clarification question",
        "Separate Workspace State from Stage State",
        "Distinguish Cancelled from Aborted",
        "Preserve work after abort",
        "Support pause and resume",
        "Support completion and archive",
        "Adopt Editorial Never Events",
        "Create Architecture Baseline 2026.08.01v05",
    )

    for decision in decisions:
        print(f"  - {decision}")

    print("\nPreview mode changes nothing.")

    print("\nApply local files with:")

    print(
        "  python3 scripts/"
        "bootstrap_capability008_editorial_discernment.py "
        "--apply"
    )


# ---------------------------------------------------------------------
# GitHub synchronization
# ---------------------------------------------------------------------

PROJECT_DESCRIPTION = (
    "Version 1.0 capability roadmap governed by the Constitution, "
    "Canonical Vocabulary, Editorial Integrity, Editorial Coherence, "
    "and the repeatable Capability Delivery Workflow."
)


PROJECT_README = f"""# Ramrattan AI Editorial Studio

## Governing principle

Trust is our most valuable feature.

## Product doctrine

Every feature must earn trust before it earns convenience.

## Current implementation

- Capabilities 001-007 - complete
- Capability 008 - Editorial Discernment and Evidence Validation
- Architecture baseline - {ARCHITECTURE_BASELINE_VERSION}

## Capability 008

Current increment:

- Editorial Discernment Engine
- Editorial Guidance
- Editorial Intent
- Editorial Coherence Guard
- No Silent Scope Expansion
- Workspace lifecycle
- Approved-component protection

Next increment:

- Evidence Validation
- Temporal Integrity
- LMHS Editorial Risk
- Editorial Confidence translation
"""


CAPABILITY_ISSUE_BODY = clean(
    """
    ## Objective

    Implement Editorial Discernment, Evidence Validation, and internal
    Editorial Risk as the trust-protection layer between Editorial Intake
    and Publication Package creation.

    ## Current increment

    - Editorial Discernment Engine
    - Editorial Guidance
    - Editorial Intent
    - Intent Alignment
    - Editorial Coherence Guard
    - No Silent Scope Expansion
    - Workspace lifecycle
    - Stage lifecycle
    - Pause, resume, cancel, abort, complete, and archive
    - Approved-component protection
    - One-question clarification
    - Editorial Never Events

    ## Next increment

    - Claim classification
    - Evidence corroboration
    - Source comparison
    - Temporal Integrity
    - LMHS Editorial Risk
    - Editorial Confidence translation

    ## Acceptance criteria

    - One Editorial Intent is maintained per session
    - Related sources may continue
    - Separate publication objectives recommend a new session
    - Unrelated material is never silently merged
    - Scope expansion requires Author awareness
    - Approved components remain protected
    - Workspace State and Stage State remain distinct
    - Cancelled and Aborted remain distinct
    - Aborted work remains resumable
    - One concise clarification question is used
    - Repository validation passes
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


def issue_payload(
    root: Path,
    issue_number: int,
) -> dict[str, Any]:
    """Return one GitHub issue."""
    payload = json_output(
        [
            "gh",
            "issue",
            "view",
            str(issue_number),
            "--repo",
            REPOSITORY,
            "--json",
            "number,title,url,state,body",
        ],
        cwd=root,
    )

    if not isinstance(payload, dict):
        return {}

    return payload


def ensure_capability_issue(root: Path) -> dict[str, Any]:
    """Reconcile Capability 008 issue #14."""
    issue = issue_payload(
        root,
        CAPABILITY_ISSUE_NUMBER,
    )

    if issue.get("number") != CAPABILITY_ISSUE_NUMBER:
        raise CapabilityError(
            "Expected Capability 008 issue #14."
        )

    current_title = str(issue.get("title", ""))
    current_body = str(issue.get("body", ""))

    if (
        current_title != CAPABILITY_ISSUE_TITLE
        or normalize(current_body)
        != normalize(CAPABILITY_ISSUE_BODY)
    ):
        run(
            [
                "gh",
                "issue",
                "edit",
                str(CAPABILITY_ISSUE_NUMBER),
                "--repo",
                REPOSITORY,
                "--title",
                CAPABILITY_ISSUE_TITLE,
                "--body",
                CAPABILITY_ISSUE_BODY,
            ],
            cwd=root,
        )

        print(
            "Reconciled Capability 008 issue #14."
        )

    refreshed = issue_payload(
        root,
        CAPABILITY_ISSUE_NUMBER,
    )

    if refreshed.get("state") == "CLOSED":
        run(
            [
                "gh",
                "issue",
                "reopen",
                str(CAPABILITY_ISSUE_NUMBER),
                "--repo",
                REPOSITORY,
            ],
            cwd=root,
        )

        refreshed = issue_payload(
            root,
            CAPABILITY_ISSUE_NUMBER,
        )

    return refreshed


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
    """Find one Project item by GitHub URL."""
    for item in project_items(root):
        content = item.get("content") or {}

        if content.get("url") == url:
            return item

    return None


def ensure_project_item(
    root: Path,
    url: str,
) -> dict[str, Any]:
    """Add content to Project #1 when missing."""
    existing = project_item_for_url(
        root,
        url,
    )

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
        created = project_item_for_url(
            root,
            url,
        )

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


def mark_previous_capability_done(root: Path) -> None:
    """Ensure Capability 007 remains Done."""
    issue = issue_payload(
        root,
        PREVIOUS_CAPABILITY_ISSUE_NUMBER,
    )

    if not issue:
        raise CapabilityError(
            "Could not resolve Capability 007 issue #13."
        )

    item = ensure_project_item(
        root,
        str(issue["url"]),
    )

    set_status(
        root,
        str(item["id"]),
        "Done",
    )

    if issue.get("state") != "CLOSED":
        run(
            [
                "gh",
                "issue",
                "close",
                str(PREVIOUS_CAPABILITY_ISSUE_NUMBER),
                "--repo",
                REPOSITORY,
                "--comment",
                (
                    "Capability 007 merged through PR #24. "
                    "Repository validation passed."
                ),
            ],
            cwd=root,
        )

    print(
        "Capability 007 confirmed Done."
    )


def sync_project(root: Path) -> None:
    """Synchronize Capability 008 GitHub planning."""
    validate_required_files(root)
    validate_product_language(root)
    run_repository_validation(root)

    run(
        ["gh", "auth", "status"],
        cwd=root,
    )

    validate_project(root)
    mark_previous_capability_done(root)

    issue = ensure_capability_issue(root)

    item = ensure_project_item(
        root,
        str(issue["url"]),
    )

    set_status(
        root,
        str(item["id"]),
        "In Progress",
    )

    print(
        "Capability 008 marked In Progress."
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
        "GitHub Project synchronized for Capability 008."
    )


# ---------------------------------------------------------------------
# Arguments and main
# ---------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Implement Capability 008 Editorial Discernment."
        )
    )

    mode = parser.add_mutually_exclusive_group()

    mode.add_argument(
        "--apply",
        action="store_true",
        help=(
            "Write and validate local Capability 008 files."
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
    """Preview, apply, or synchronize Capability 008."""
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
                "Capability 008 Editorial Discernment "
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


# CAPABILITY_008_EDITORIAL_DISCERNMENT_COMPLETE
# END OF SCRIPT - CAPABILITY 008

# CAPABILITY_008A3_GENERATOR_OVERRIDE_START
from bootstrap_capability008a3_editorial_integrity_hardening import (
    EDITORIAL_DISCERNMENT_RUNTIME as CAPABILITY_008A3_DISCERNMENT_RUNTIME,
    EDITORIAL_GUIDANCE_RUNTIME as CAPABILITY_008A3_GUIDANCE_RUNTIME,
)
NEW_FILES["studio/editorial_discernment.py"] = (
    CAPABILITY_008A3_DISCERNMENT_RUNTIME
)
NEW_FILES["studio/editorial_guidance.py"] = (
    CAPABILITY_008A3_GUIDANCE_RUNTIME
)
# CAPABILITY_008A3_GENERATOR_OVERRIDE_END

if __name__ == "__main__":
    raise SystemExit(main())
