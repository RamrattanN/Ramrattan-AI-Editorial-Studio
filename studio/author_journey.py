"""Early-session orchestration for the Version 1.1 Author Journey.

V11-01 owns Welcome through Workflow Selection. V11-02 adds structurally
independent Editorial Source and Branding intake. V11-03 adds the separate
Editorial Discovery and Editorial Plan approval gates. V11-04 orchestrates
the existing Version 1.0 generation contracts without changing them. V11-05
opens the Author-owned Publication Studio and stops at the Editorial Audit
routing seam. V11-06 completes that seam with a real, read-only Editorial
Audit and the Copy LinkedIn Publication gate, then stops at the Session
Completion routing seam. V11-07 integrates the existing Portable Editorial
Project resume mechanism as a separate path directly into Publication
Studio. The orchestrator wraps an optional Version 1.0
``EditorialSession`` without changing that runtime.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import date
from enum import StrEnum
from typing import TYPE_CHECKING, Final

from .article_engine import (
    ArticleEngine,
    ArticleRequest,
    PublicationBlockedError,
)
from .editorial_audit import EditorialAuditResult, perform_editorial_audit
from .evidence_validation import (
    Claim,
    EditorialRisk,
    EvidenceRecord,
    EvidenceValidationReport,
    validate_evidence,
)
from .hero_visual import HeroVisualRequest, HeroVisualSystem
from .portable_editorial_project import (
    PortableProjectError,
    ProjectState,
    ResumeResult,
    resume_project,
)
from .publication_package import PublicationPackage, PublicationPackageBuilder
from .publication_studio import PublicationContent, PublicationStudio
from .session_completion import (
    SessionArtifacts,
    build_session_artifacts,
)

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
    EDITORIAL_PLAN = "editorial_plan"
    GENERATION = "generation"
    PUBLICATION_STUDIO = "publication_studio"
    EDITORIAL_AUDIT = "editorial_audit"
    SESSION_COMPLETION = "session_completion"
    COMPLETE = "complete"


class GenerationStatus(StrEnum):
    """The three explicit outcomes owned by V11-04."""

    COMPLETE = "complete"
    BLOCKED = "blocked"
    FAILED = "failed"


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


@dataclass(frozen=True, slots=True)
class EditorialUnderstanding:
    """The complete intake understanding presented at Discovery."""

    intent: str
    audience: str
    platform: str
    desired_outcome: str
    branding: BrandingSelection


@dataclass(frozen=True, slots=True)
class EditorialPlan:
    """The complete proposal that must be approved before Generation."""

    headline: str
    hook: str
    key_insights: tuple[str, ...]
    practical_takeaway: str
    call_to_action: str

    def __post_init__(self) -> None:
        text_fields = (
            "headline",
            "hook",
            "practical_takeaway",
            "call_to_action",
        )
        for field_name in text_fields:
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise AuthorJourneyError(
                    f"Editorial Plan {field_name} must not be empty."
                )
        if not isinstance(self.key_insights, tuple) or not self.key_insights:
            raise AuthorJourneyError(
                "Editorial Plan requires at least one Key Insight."
            )
        if not all(
            isinstance(insight, str) and insight.strip()
            for insight in self.key_insights
        ):
            raise AuthorJourneyError(
                "Editorial Plan Key Insights must not be empty."
            )


@dataclass(frozen=True, slots=True)
class GenerationRequest:
    """Existing Version 1.0 contracts bound to the approved journey data."""

    article: ArticleRequest
    claims: tuple[Claim, ...]
    evidence: tuple[EvidenceRecord, ...]
    hero_visual: HeroVisualRequest
    current_on: date | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.article, ArticleRequest):
            raise AuthorJourneyError("Generation requires an Article Request.")
        if not isinstance(self.claims, tuple) or not all(
            isinstance(item, Claim) for item in self.claims
        ):
            raise AuthorJourneyError("Generation claims are not supported.")
        if not isinstance(self.evidence, tuple) or not all(
            isinstance(item, EvidenceRecord) for item in self.evidence
        ):
            raise AuthorJourneyError("Generation evidence is not supported.")
        if not isinstance(self.hero_visual, HeroVisualRequest):
            raise AuthorJourneyError("Generation requires a Hero Visual Request.")


@dataclass(frozen=True, slots=True)
class GenerationOutcome:
    """One complete publication or one explicit non-producing outcome."""

    status: GenerationStatus
    explanation: str
    evidence_report: EvidenceValidationReport | None
    publication_package: PublicationPackage | None = None

    @property
    def complete(self) -> bool:
        return (
            self.status is GenerationStatus.COMPLETE
            and self.publication_package is not None
        )


@dataclass(frozen=True, slots=True)
class ResumeValidationOutcome:
    """One explicit success or failure from Resume Validation."""

    succeeded: bool
    explanation: str
    state: ProjectState | None = None
    result: ResumeResult | None = None


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

    def resume_existing_project(
        self, markdown: str, *, current_on: date
    ) -> ResumeValidationOutcome:
        """Run the existing Version 1.0 resume path without Configuration."""
        self._require(
            AuthorJourneyState.RESUME_VALIDATION,
            "resume an existing Portable Editorial Project",
        )
        if self.editorial_session is None:
            outcome = ResumeValidationOutcome(
                False,
                "The project cannot be resumed without an Editorial Session.",
            )
            self._resume_validation_outcome = outcome
            self.state = AuthorJourneyState.ENTRY_PATH
            return outcome
        try:
            result = resume_project(
                markdown,
                self.editorial_session,
                current_on=current_on,
            )
        except (PortableProjectError, ValueError) as exc:
            project_state = (
                exc.state if isinstance(exc, PortableProjectError) else None
            )
            detail = str(exc).strip() or "Portable Editorial Project validation failed."
            outcome = ResumeValidationOutcome(
                False,
                "The project cannot be resumed: " + detail,
                project_state,
            )
            self._resume_validation_outcome = outcome
            self.state = AuthorJourneyState.ENTRY_PATH
            return outcome

        self._publication_studio = PublicationStudio.from_resume(result)
        self._resume_result = result
        outcome = ResumeValidationOutcome(
            True,
            "The Portable Editorial Project was restored in Publication Studio.",
            result.state,
            result,
        )
        self._resume_validation_outcome = outcome
        self.state = AuthorJourneyState.PUBLICATION_STUDIO
        return outcome

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
        self.branding_preference = selection.mode.value
        self.state = AuthorJourneyState.EDITORIAL_DISCOVERY
        return selection

    def review_discovery(self) -> EditorialUnderstanding:
        """Present the complete Source inference and Branding decision."""
        self._require(
            AuthorJourneyState.EDITORIAL_DISCOVERY,
            "review Editorial Discovery",
        )
        inference = self.editorial_inference
        branding = self.branding_selection
        if inference is None or branding is None:
            raise AuthorJourneyError(
                "Editorial Discovery requires Source inference and Branding."
            )
        return EditorialUnderstanding(
            intent=inference.intent,
            audience=inference.audience,
            platform=inference.platform,
            desired_outcome=inference.desired_outcome,
            branding=branding,
        )

    def approve_discovery(self) -> None:
        """Confirm the complete understanding and enter Editorial Plan."""
        self.review_discovery()
        self._discovery_approved = True
        self.state = AuthorJourneyState.EDITORIAL_PLAN

    def refine_editorial_source(self) -> None:
        """Return to Source without discarding the Branding selection."""
        self._require(
            AuthorJourneyState.EDITORIAL_DISCOVERY,
            "request Editorial Source refinement",
        )
        self.state = AuthorJourneyState.EDITORIAL_SOURCE

    def refine_branding(self) -> None:
        """Return to Branding without discarding Source or its inference."""
        self._require(
            AuthorJourneyState.EDITORIAL_DISCOVERY,
            "request Branding refinement",
        )
        self.state = AuthorJourneyState.BRANDING

    def propose_plan(self, plan: EditorialPlan) -> EditorialPlan:
        """Present a complete plan only after Discovery approval."""
        self._require(AuthorJourneyState.EDITORIAL_PLAN, "propose Editorial Plan")
        if not getattr(self, "_discovery_approved", False):
            raise AuthorJourneyError(
                "Editorial Discovery must be approved before planning."
            )
        if not isinstance(plan, EditorialPlan):
            raise AuthorJourneyError("Editorial Plan proposal is not supported.")
        self._editorial_plan = plan
        return plan

    def review_plan(self) -> EditorialPlan:
        """Return the current proposal for focused Author review."""
        self._require(AuthorJourneyState.EDITORIAL_PLAN, "review Editorial Plan")
        plan = self.editorial_plan
        if plan is None:
            raise AuthorJourneyError(
                "An Editorial Plan must be proposed before review."
            )
        return plan

    def revise_plan(self, plan: EditorialPlan) -> EditorialPlan:
        """Replace the proposal while remaining inside the Plan gate."""
        self.review_plan()
        if not isinstance(plan, EditorialPlan):
            raise AuthorJourneyError("Editorial Plan revision is not supported.")
        self._editorial_plan = plan
        return plan

    def approve_plan(self) -> EditorialPlan:
        """Approve the current plan and enter the Generation routing seam."""
        plan = self.review_plan()
        self._approved_editorial_plan = plan
        self.state = AuthorJourneyState.GENERATION
        return plan

    def run_generation(self, request: GenerationRequest) -> GenerationOutcome:
        """Run the approved Version 1.0 generation chain exactly once."""
        self._require(AuthorJourneyState.GENERATION, "run Generation")
        if getattr(self, "_generation_completed", False):
            raise InvalidAuthorJourneyTransition(
                "Generation has already completed for this session."
            )
        if not isinstance(request, GenerationRequest):
            raise AuthorJourneyError("Generation request is not supported.")
        self._validate_generation_request(request)

        report: EvidenceValidationReport | None = None
        try:
            report = validate_evidence(
                request.claims,
                request.evidence,
                current_on=request.current_on,
            )
            if report.publication_blocked or report.editorial_risk in {
                EditorialRisk.HIGH,
                EditorialRisk.SEVERE,
            }:
                return self._generation_did_not_complete(
                    GenerationStatus.BLOCKED,
                    "Generation was blocked by Editorial Risk: "
                    + report.author_message,
                    report,
                )
            draft = ArticleEngine().create_article(request.article, report)
            builder = PublicationPackageBuilder()
            package = builder.build(draft, report)
            visual = HeroVisualSystem().generate(request.hero_visual)
            if not visual.ready:
                reason = visual.failure_reason or "Hero Visual generation failed."
                return self._generation_did_not_complete(
                    GenerationStatus.FAILED,
                    "Generation failed independently of Editorial Risk: " + reason,
                    report,
                )
            completed = builder.attach_hero_visual(package, visual)
        except PublicationBlockedError as exc:
            explanation = str(exc).strip() or "Editorial Risk blocked Generation."
            return self._generation_did_not_complete(
                GenerationStatus.BLOCKED,
                "Generation was blocked by Editorial Risk: " + explanation,
                report,
            )
        except Exception as exc:  # Generation providers fail closed here.
            explanation = str(exc).strip() or "Generation validation failed."
            return self._generation_did_not_complete(
                GenerationStatus.FAILED,
                "Generation failed independently of Editorial Risk: " + explanation,
                report,
            )

        outcome = GenerationOutcome(
            status=GenerationStatus.COMPLETE,
            explanation="Generation completed and entered Publication Studio.",
            evidence_report=report,
            publication_package=completed,
        )
        self._generation_completed = True
        self._generation_outcome = outcome
        self._generation_claims = request.claims
        self._generation_evidence = request.evidence
        branding = self.branding_selection
        understanding = self.editorial_understanding
        if branding is None or understanding is None:
            raise AuthorJourneyError(
                "Publication Studio requires confirmed Discovery and Branding."
            )
        material_count = len(branding.materials)
        branding_summary = (
            f"{branding.mode.value.replace('_', ' ')}; "
            f"{material_count} Author-supplied reference"
            + ("s" if material_count != 1 else "")
        )
        self._publication_studio = PublicationStudio.from_generation(
            completed,
            branding_summary=branding_summary,
            session_summary=understanding.desired_outcome,
        )
        self.state = AuthorJourneyState.PUBLICATION_STUDIO
        return outcome

    def edit_publication(self, **changes: object) -> PublicationContent:
        """Apply an explicit Author edit without invoking Generation."""
        self._require(
            AuthorJourneyState.PUBLICATION_STUDIO,
            "edit Publication Content",
        )
        studio = self.publication_studio
        if studio is None:
            raise AuthorJourneyError("Publication Studio is not available.")
        return studio.author_edit(**changes)

    def request_editorial_audit(self) -> PublicationContent:
        """Enter Editorial Audit; the audit itself runs on completion."""
        self._require(
            AuthorJourneyState.PUBLICATION_STUDIO,
            "request Editorial Audit",
        )
        studio = self.publication_studio
        if studio is None:
            raise AuthorJourneyError("Publication Studio is not available.")
        content = studio.editorial_audit_input()
        self.state = AuthorJourneyState.EDITORIAL_AUDIT
        return content

    def complete_editorial_audit(
        self, *, current_on: date | None = None
    ) -> EditorialAuditResult:
        """Run the read-only Editorial Audit and return to Author Editing.

        Re-invokes `evidence_validation.validate_evidence` against the same
        claims and evidence established at Generation - the Editorial
        Integrity Pipeline's internal risk-derivation logic is not altered
        or duplicated here - and computes Editorial Drift against the
        Generate Once baseline. The result never modifies Publication
        Content; it only refreshes Editorial Review and the Copy LinkedIn
        Publication gate.
        """
        self._require(
            AuthorJourneyState.EDITORIAL_AUDIT, "complete Editorial Audit"
        )
        studio = self.publication_studio
        claims = getattr(self, "_generation_claims", None)
        evidence = getattr(self, "_generation_evidence", None)
        if studio is None or claims is None or evidence is None:
            raise AuthorJourneyError(
                "Editorial Audit requires a completed Generation."
            )
        result = perform_editorial_audit(
            claims,
            evidence,
            generated_content=studio.editor.generated_content,
            current_content=studio.editor.current_content,
            current_on=current_on,
        )
        studio.apply_editorial_audit(result)
        self._last_audit_result = result
        self.state = AuthorJourneyState.PUBLICATION_STUDIO
        return result

    def copy_linkedin_publication(self) -> str:
        """Return the Author's current Publication Content when matched."""
        self._require(
            AuthorJourneyState.PUBLICATION_STUDIO, "copy LinkedIn Publication"
        )
        studio = self.publication_studio
        if studio is None:
            raise AuthorJourneyError("Publication Studio is not available.")
        return studio.copy_linkedin_publication()

    def signal_completion(self) -> None:
        """Enter the V11-08 Session Completion routing seam.

        No Editorial Audit is required to reach this seam (AC-AUDIT-7); the
        gate governs Copy LinkedIn Publication only.
        """
        self._require(
            AuthorJourneyState.PUBLICATION_STUDIO, "signal completion"
        )
        self.state = AuthorJourneyState.SESSION_COMPLETION

    def completion_prompt(self) -> str:
        """Present the one optional Configuration decision at completion."""
        self._require(
            AuthorJourneyState.SESSION_COMPLETION,
            "present the Session Completion prompt",
        )
        return (
            "Would you like to generate a Ramrattan AI Configuration from "
            "today's session for future use?"
        )

    def complete_session(
        self,
        *,
        generate_configuration: bool,
        completed_on: date,
        existing_project_names: tuple[str, ...] = (),
        existing_configuration_names: tuple[str, ...] = (),
    ) -> SessionArtifacts:
        """Deliver final artifacts, enter Complete, and retain no session data."""
        self._require(AuthorJourneyState.SESSION_COMPLETION, "complete the session")
        if not isinstance(generate_configuration, bool):
            raise AuthorJourneyError(
                "Session Completion requires an explicit Configuration choice."
            )
        studio = self.publication_studio
        if studio is None:
            raise AuthorJourneyError(
                "Session Completion requires an active Publication Studio."
            )
        artifacts = build_session_artifacts(
            studio,
            completed_on=completed_on,
            generate_configuration=generate_configuration,
            preferred_workflow=(
                self.workflow_mode.value if self.workflow_mode is not None else None
            ),
            branding_preference=self.branding_preference,
            existing_project_names=existing_project_names,
            existing_configuration_names=existing_configuration_names,
        )
        self.__dict__.clear()
        self.state = AuthorJourneyState.COMPLETE
        return artifacts

    def _validate_generation_request(self, request: GenerationRequest) -> None:
        plan = self.approved_editorial_plan
        understanding = self.editorial_understanding
        branding = self.branding_selection
        if plan is None or understanding is None or branding is None:
            raise AuthorJourneyError(
                "Generation requires an approved Plan and confirmed Discovery."
            )
        expected = (
            (request.article.editorial_intent, understanding.intent, "intent"),
            (request.article.audience, understanding.audience, "audience"),
            (request.article.thesis, plan.headline, "headline"),
            (request.article.author_perspective, plan.hook, "hook"),
            (request.article.insights, plan.key_insights, "Key Insights"),
            (
                request.article.practical_takeaway,
                plan.practical_takeaway,
                "Practical Takeaway",
            ),
            (request.article.cta_question, plan.call_to_action, "Call to Action"),
            (
                request.hero_visual.prompt,
                request.article.hero_visual_prompt,
                "Hero Visual prompt",
            ),
        )
        mismatches = [label for actual, approved, label in expected if actual != approved]
        if mismatches:
            raise AuthorJourneyError(
                "Generation input differs from approved session data: "
                + ", ".join(mismatches)
                + "."
            )
        if (
            branding.mode is BrandingMode.STUDIO_THEME
            and request.hero_visual.brand_context is not None
        ):
            raise AuthorJourneyError(
                "Studio Theme Generation cannot introduce Branding material."
            )
        if (
            branding.mode is not BrandingMode.STUDIO_THEME
            and not (request.hero_visual.brand_context or "").strip()
        ):
            raise AuthorJourneyError(
                "Selected Branding must be present in the Generation request."
            )

    def _generation_did_not_complete(
        self,
        status: GenerationStatus,
        explanation: str,
        report: EvidenceValidationReport | None,
    ) -> GenerationOutcome:
        outcome = GenerationOutcome(status, explanation, report)
        self._generation_outcome = outcome
        self.state = AuthorJourneyState.EDITORIAL_PLAN
        return outcome

    @property
    def editorial_source(self) -> EditorialSourceMaterial | None:
        return getattr(self, "_editorial_source", None)

    @property
    def editorial_inference(self) -> EditorialInference | None:
        return getattr(self, "_editorial_inference", None)

    @property
    def branding_selection(self) -> BrandingSelection | None:
        return getattr(self, "_branding_selection", None)

    @property
    def editorial_plan(self) -> EditorialPlan | None:
        return getattr(self, "_editorial_plan", None)

    @property
    def approved_editorial_plan(self) -> EditorialPlan | None:
        return getattr(self, "_approved_editorial_plan", None)

    @property
    def editorial_understanding(self) -> EditorialUnderstanding | None:
        if not getattr(self, "_discovery_approved", False):
            return None
        inference = self.editorial_inference
        branding = self.branding_selection
        if inference is None or branding is None:
            return None
        return EditorialUnderstanding(
            intent=inference.intent,
            audience=inference.audience,
            platform=inference.platform,
            desired_outcome=inference.desired_outcome,
            branding=branding,
        )

    @property
    def generation_outcome(self) -> GenerationOutcome | None:
        return getattr(self, "_generation_outcome", None)

    @property
    def publication_studio(self) -> PublicationStudio | None:
        return getattr(self, "_publication_studio", None)

    @property
    def last_audit_result(self) -> EditorialAuditResult | None:
        return getattr(self, "_last_audit_result", None)

    @property
    def resume_validation_outcome(self) -> ResumeValidationOutcome | None:
        return getattr(self, "_resume_validation_outcome", None)

    def _require(self, expected: AuthorJourneyState, action: str) -> None:
        if self.state is not expected:
            raise InvalidAuthorJourneyTransition(
                f"Cannot {action} from {self.state.value}; "
                f"required state is {expected.value}."
            )
