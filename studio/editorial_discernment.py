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

from .editorial_guidance import (
    StageState,
    initial_stage_states,
    transition_stage,
)


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
        default_factory=initial_stage_states
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
        """Apply one canonical stage transition without changing workspace state."""
        self.stage_states = transition_stage(self.stage_states, number, state)


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
