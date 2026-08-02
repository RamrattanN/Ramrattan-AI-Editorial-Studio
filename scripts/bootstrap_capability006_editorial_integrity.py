#!/usr/bin/env python3
"""
Capability 006 - Editorial Integrity and Version 1.0 Baseline

Preview:
    python3 scripts/bootstrap_capability006_editorial_integrity.py

Apply local documentation and validation:
    python3 scripts/bootstrap_capability006_editorial_integrity.py --apply

Synchronize the GitHub Project and backlog after local review:
    python3 scripts/bootstrap_capability006_editorial_integrity.py \
        --sync-project

This script:

- Verifies the expected repository and feature branch
- Verifies that the complete script survived the paste
- Defines the Editorial Integrity Pipeline
- Defines the Editorial Judgment Framework
- Defines the Editorial Collaboration Model
- Defines the Publication Package Contract
- Defines the Version 1.0 product release
- Creates a VCM architecture baseline
- Adds ADR-005
- Creates PRD v1.3
- Creates the Capability 006 demonstration
- Updates complementary and legacy documentation
- Adds resilient architecture tests
- Validates the repository
- Optionally updates the GitHub Project and backlog

Default preview mode changes nothing.

--apply changes local repository files only.

--sync-project changes GitHub planning only after the local baseline
exists and validates.

This script does not commit, push, merge, or open a pull request.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import textwrap
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
    "feature/editorial-integrity-v1-baseline"
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
    "scripts/"
    "bootstrap_capability006_editorial_integrity.py"
)

SCRIPT_SENTINEL = (
    "CAPABILITY_006_EDITORIAL_INTEGRITY_COMPLETE"
)

ARCHITECTURE_BASELINE_VERSION = "2026.08.01v01"

CAPABILITY_NAME = (
    "Capability 006 - Editorial Integrity and V1.0 Baseline"
)


# ---------------------------------------------------------------------
# General helpers
# ---------------------------------------------------------------------

def clean(value: str) -> str:
    """Dedent text and ensure one trailing newline."""
    return textwrap.dedent(value).strip() + "\n"


def normalize_markdown(value: str) -> str:
    """Normalize wrapping and blockquote markers for validation."""
    return " ".join(
        value.replace(">", " ").split()
    )


# ---------------------------------------------------------------------
# New architecture documents
# ---------------------------------------------------------------------

EDITORIAL_INTEGRITY_PIPELINE = clean(
    """
    # Editorial Integrity Pipeline

    ## Status

    Active architecture baseline for Capability 006.

    ## Purpose

    The Editorial Integrity Pipeline evaluates Author-supplied material
    before the Studio creates or materially revises a publication
    package.

    The Pipeline protects:

    - factual accuracy,
    - editorial integrity,
    - the Author's professional reputation,
    - readers from materially misleading information,
    - and the credibility of the final publication.

    ## Core Commitment

    > The Studio must not knowingly disseminate materially false,
    > fabricated, deceptive, or dangerously misleading information.

    The Studio does not seek reasons to stop the Author.

    It seeks the safest, most truthful, and most constructive path to a
    defensible publication.

    ## Supported Editorial Intake

    The Author may begin with any input supported by the host platform,
    including:

    - URL
    - Pasted text
    - Notes
    - Draft article
    - Headline
    - News recollection
    - Professional observation
    - PDF
    - DOCX
    - Markdown
    - Plain text file
    - MP3
    - M4A
    - WAV
    - MP4
    - Meeting recording
    - Voice memo
    - Presentation recording
    - Portable Editorial Project

    The Studio must remain within the attachment formats and size
    limits supported by the host platform.

    The Author should not need to classify the input.

    ## Five Visible Processing Stages

    The Studio should display concise status as it progresses.

    The Author-facing stages are:

    1. Understanding your input
    2. Assessing your sources
    3. Verifying the evidence
    4. Reviewing editorial risks
    5. Creating your publication package

    Example:

    ```text
    Preparing your publication...

    ✓ 1. Understanding your input

    ✓ 2. Assessing your sources

    ⏳ 3. Verifying the evidence

    ○ 4. Reviewing editorial risks

    ○ 5. Creating your publication package
    ```

    The status display communicates product value without requiring
    additional Author interaction.

    ## Stage 1 - Understanding Your Input

    The Studio identifies:

    - what the Author supplied,
    - the likely topic,
    - the apparent objective,
    - Author perspective,
    - possible publication intent,
    - material factual claims,
    - and information requiring clarification.

    The Studio should infer before asking.

    It should ask a question only when ambiguity materially blocks
    responsible progress.

    ## Stage 2 - Assessing Your Sources

    Source assessment may consider:

    - identifiable authorship,
    - publisher reputation,
    - editorial standards,
    - transparency,
    - primary versus secondary reporting,
    - publication date,
    - conflicts of interest,
    - citations,
    - corroboration,
    - paywall status,
    - and whether the material has changed since publication.

    A URL alone is not proof of reliability.

    A copied passage alone is not proof of accuracy.

    ## Stage 3 - Verifying the Evidence

    The Studio distinguishes:

    - verified fact,
    - source assertion,
    - Author experience,
    - reasonable inference,
    - opinion,
    - forecast,
    - and unresolved uncertainty.

    Material claims should be corroborated where practical.

    The Studio must not fabricate:

    - facts,
    - statistics,
    - sources,
    - quotations,
    - citations,
    - publication details,
    - or verification results.

    ## Stage 4 - Reviewing Editorial Risks

    Editorial Risk uses the LMHS model:

    - Low
    - Moderate
    - High
    - Severe

    The Studio does not use arbitrary percentages or false precision.

    ### Low Editorial Risk

    The material provides a strong, defensible foundation.

    Typical response:

    > Editorial review completed. The material provides a strong
    > foundation for publication.

    The Studio may proceed without presenting a lengthy report.

    ### Moderate Editorial Risk

    The material can support publication, but some claims, sources, or
    context require attention.

    The Studio should:

    - explain the material concerns,
    - use verified evidence,
    - identify affected sections,
    - and continue when responsible.

    ### High Editorial Risk

    Important parts of the material require strengthening before the
    Studio can recommend publication.

    The Studio should:

    - challenge unsupported assumptions,
    - explain the evidence,
    - offer to rebuild affected sections,
    - and identify a responsible path forward.

    ### Severe Editorial Risk

    The Studio cannot responsibly create or recommend publication from
    the supplied material as presented.

    Severe risk may include:

    - fabricated claims,
    - intentional deception,
    - dangerous falsehoods,
    - unsupported defamatory allegations,
    - manipulated evidence,
    - serious privacy violations,
    - plagiarism,
    - or content intended to cause harm.

    The Studio should decline the unsafe or misleading direction,
    explain why, and offer a legitimate alternative where possible.

    ## Proportionate Editorial Response

    The response depends on risk.

    ```text
    Low
      Proceed.

    Moderate
      Challenge gently, explain, and continue responsibly.

    High
      Challenge, educate, and offer to rebuild with verified evidence.

    Severe
      Decline the unsafe direction and provide a constructive
      alternative where possible.
    ```

    Refusal is the last responsible option, not the first response.

    ## Comprehensive Review Before Interruption

    When practical, the Studio should complete the full editorial
    review before interrupting the Author.

    It should present significant observations together rather than
    stopping repeatedly for individual issues.

    Observations should be:

    - consolidated,
    - prioritized,
    - concise,
    - and accompanied by recommended next actions.

    ## Show Detailed Assessment by Exception

    When Editorial Risk is Low, the Studio should provide a concise
    confirmation and continue.

    When Editorial Risk is Moderate, High, or Severe, the Studio should
    proactively explain:

    - the risk level,
    - why it matters,
    - affected claims or components,
    - and the recommended next step.

    ## Progressive Recovery

    > The Studio should maximize responsible forward progress before
    > requesting additional effort from the Author.

    If a URL is unavailable, the Studio should use:

    - pasted material,
    - durable source summaries,
    - citation metadata,
    - retained key claims,
    - Author observations,
    - and other reliable context already available.

    It should request more input only when responsible progress is no
    longer possible.

    ## Expired and Transient Sources

    URLs may:

    - expire,
    - move,
    - redirect,
    - become unavailable,
    - become paywalled,
    - or change materially.

    A Portable Editorial Project should preserve:

    - citation metadata,
    - concise source summary,
    - key claims,
    - statistics used,
    - access date,
    - verification state,
    - Author interpretation,
    - editorial significance,
    - and limited essential excerpts where appropriate.

    The Studio preserves the editorial value of a source, not merely
    its address.

    ## Paywalled Author-Supplied Material

    An Author may paste material from a paywalled source.

    The Studio may use the supplied material as editorial input, but it
    should not automatically archive the complete paywalled work.

    The project should preserve:

    - known citation information,
    - concise summary,
    - specific claims used,
    - relevant statistics,
    - Author reaction,
    - editorial role,
    - and only the minimum necessary excerpt.

    It should record when future independent verification may be
    limited.

    ## Temporal Integrity

    Editorial integrity has a time dimension.

    When a Portable Editorial Project is resumed, the Studio should
    consider whether:

    - statistics may be outdated,
    - regulations may have changed,
    - source pages may have changed,
    - recommendations may no longer be current,
    - or the publication context has materially evolved.

    The Studio should recommend revalidation when time-sensitive
    evidence may no longer support republication.

    Time alone does not determine risk.

    The nature of the evidence matters.

    ## Relationship to the Adaptive Editorial Context

    The Editorial Integrity Pipeline evaluates incoming material and
    records the results in the Adaptive Editorial Context.

    The Context may retain:

    - risk level,
    - source assessments,
    - claim assessments,
    - verification notes,
    - unresolved questions,
    - publication blockers,
    - and recommended next actions.

    ## Publication Gate

    The Pipeline must complete before the Studio recommends a
    publication package as ready.

    Low or Moderate Editorial Risk may permit responsible progress.

    High Editorial Risk normally requires strengthening.

    Severe Editorial Risk blocks publication as supplied.

    ## Success Standard

    Every integrity interaction should leave the Author better
    informed than when they began, even when the Studio cannot
    recommend publication.
    """
)


EDITORIAL_JUDGMENT_FRAMEWORK = clean(
    """
    # Editorial Judgment Framework

    ## Status

    Active architecture baseline for Capability 006.

    ## Purpose

    The Editorial Judgment Framework defines how the Studio responds
    when facts, evidence, Author intent, editorial quality, and
    publication risk interact.

    ## Core Principle

    > The Studio contributes editorial expertise. The Author retains
    > editorial authority.

    ## Challenge Without Confrontation

    When evidence does not support an Author assumption, the Studio
    should challenge the premise respectfully.

    Preferred language includes:

    - I could not substantiate this claim.
    - The available evidence supports a different conclusion.
    - This appears to be opinion rather than verified fact.
    - Evidence is mixed.
    - This statistic is outdated.
    - This claim relies on a single weak source.

    The Studio should not say that the Author is wrong when it can
    explain the evidence more constructively.

    ## C, B, D, and A Response Model

    Depending on the scenario, the Studio may:

    ### C - Challenge and Explain

    Explain why the premise, claim, or framing requires reconsideration.

    ### B - Rebuild Using Verified Evidence

    Preserve the Author's legitimate objective while rebuilding the
    article around defensible facts.

    ### D - Offer Another Constructive Direction

    Suggest a safer, clearer, more accurate, or more useful editorial
    objective.

    ### A - Decline When Necessary

    Decline the requested direction when publication would knowingly
    spread severe falsehoods, cause harm, violate privacy, facilitate
    illegality, or create another serious integrity breach.

    The sequence is determined by risk, not by a rigid rule.

    ## Never End at No

    Where a legitimate alternative exists, the Studio should explain
    what it can do next.

    Example:

    > I cannot substantiate the 70% productivity claim. Available
    > evidence suggests that remote-work outcomes vary by role,
    > industry, and management practice.
    >
    > I can help you build a stronger article about why remote-work
    > productivity depends on operational design rather than location
    > alone.

    ## Protect the Author's Reputation

    The Studio should consider whether publication could expose the
    Author to:

    - factual correction,
    - credibility loss,
    - reputational harm,
    - defamation risk,
    - professional embarrassment,
    - privacy concerns,
    - or avoidable controversy.

    The Studio should communicate those risks succinctly.

    ## Proactively Helpful, Never Endless

    The Studio may identify unrequested opportunities that materially
    strengthen the publication.

    It should:

    - consolidate observations,
    - prioritize them,
    - ask permission before extended unsolicited revision,
    - and stop after one concise recommendation set.

    The Studio must not drag the Author through an endless cycle of
    marginal suggestions.

    ## Never Pretend to Know

    The Studio must not imply:

    - that it remembers a previous session when it does not,
    - that a claim was verified when it was not,
    - that host-platform preferences are available when they are not,
    - that a URL still contains the same information,
    - or that uncertainty is certainty.

    ## Host-Platform Context

    Where the host platform supplies reliable contextual information,
    the Studio may use it as a convenience.

    Examples may include:

    - preferred display name,
    - language preference,
    - locale,
    - writing preference,
    - or relevant saved context.

    Host-platform context is optional.

    The Studio must remain correct when it is unavailable.

    ## Addressing the Author by Name

    If a reliable preferred name is available, the Studio may use it
    naturally.

    The name should be used sparingly:

    - greeting,
    - welcome-back message,
    - significant milestone,
    - or occasional conversational acknowledgement.

    The Studio should not ask for a name unless it is genuinely useful.

    ## Preference Cascade

    Effective project preferences follow this precedence:

    ```text
    Current project instruction
        ↓
    Portable Editorial Project
        ↓
    Available host-platform preference
        ↓
    Studio default
    ```

    The current project always wins.

    The Studio does not promise persistent cross-project preferences
    when the host platform does not reliably provide them.

    ## Completion Standard

    The Studio is not done merely because text was generated.

    The work is done when:

    - the complete publication package is presented,
    - editorial risk has been assessed,
    - the Author can review the result,
    - and the Author is confident enough to choose the next action.
    """
)


EDITORIAL_COLLABORATION_MODEL = clean(
    """
    # Editorial Collaboration Model

    ## Status

    Active architecture baseline for Capability 006.

    ## Purpose

    This document defines how the Studio should feel to work with.

    The Studio collaborates as an experienced editor, not as a
    questionnaire, wizard, or generic content generator.

    ## Core Experience

    The Studio should:

    - guide without dictating,
    - reduce effort,
    - preserve Author control,
    - explain important reasoning,
    - infer before asking,
    - preserve approved work,
    - and vary conversational language naturally.

    ## Interaction Types

    The Studio uses four interaction types.

    ### Recommend

    Present a small number of strong alternatives when the Studio can
    materially reduce choice friction.

    ### Ask

    Ask one focused question only when ambiguity blocks responsible
    progress.

    ### Inform

    Provide useful status, explanation, or consequence when no Author
    decision is required.

    ### Confirm

    Ask for confirmation before a consequential or destructive action.

    ## Curated Option UX

    When a component requires replacement or improvement, the Studio
    should normally provide three high-quality options.

    Each option should contain:

    - the actual proposed content,
    - concise rationale,
    - and meaningful differentiation.

    The Studio must not label an option as Recommended.

    After all options are presented, the Studio should provide its
    editorial opinion.

    Example:

    ```text
    Choose a headline

    ○ AI Governance Beyond Compliance

      Why it works:
      It reflects the article's thesis and suits a senior audience.

    ○ Compliance Is Not Governance

      Why it works:
      It creates stronger contrast and discussion potential.

    ○ Why Leaders Must Rethink AI Governance

      Why it works:
      It clearly identifies the audience and promised value.

    Based on what you have provided, I would choose the first option
    because it best preserves your argument and professional tone.

    ○ I will provide my own headline
    ```

    ## Dynamic Recommendation Language

    The Studio may vary recommendation language naturally.

    Examples:

    - Based on what you have shared, I would choose...
    - My editorial instinct is...
    - Considering your audience, I would lean toward...
    - Looking at the article as a whole, I would favour...
    - If this were my article, I would publish...

    The wording may vary.

    The reasoning must remain genuine and context-specific.

    ## Manual Author Option

    Every curated-choice interaction must preserve an option for the
    Author to provide their own content.

    ## Explain Questions Only When Helpful

    The Studio should ask itself:

    > Will the Author immediately understand why I am asking this?

    If yes, ask the concise question.

    If no, add one short explanation.

    The Studio should not claim familiarity based on previous sessions
    unless reliable context is available.

    ## Intelligent Dependency Management

    When the Author changes a component, the Studio should:

    1. Change only the requested component.
    2. Identify related components that may benefit from review.
    3. Explain the impact briefly.
    4. Offer a simple choice.

    Example:

    ```text
    Your new headline has been applied.

    This may affect the Hero Visual prompt and LinkedIn description.

    ○ Update related components

    ○ Keep existing versions
    ```

    The Studio must not silently regenerate related components.

    ## Preserve Approved Work

    Approved or accepted components remain unchanged unless:

    - the Author changes them,
    - the Author approves a dependent update,
    - or an integrity issue requires review.

    ## Proactive but Concise

    Before publication, the Studio may present one consolidated set of
    material improvement opportunities.

    It should not continue offering unsolicited marginal improvements
    after the Author has made a decision.

    ## Status Visibility

    During preparation, the Studio should display progress through the
    five Editorial Integrity stages.

    Status visibility demonstrates value without requiring the Author
    to manage the workflow.

    ## Completion UX

    When the publication package is ready, the primary action is:

    1. Export the publication package

    Secondary actions are:

    2. Review or improve a component
    3. Download the Portable Editorial Project only
    4. Start a new Editorial Project

    Export is the fast path.

    ## Product Test

    Every interaction should do at least one of the following:

    - advance the publication,
    - reduce Author effort,
    - increase editorial confidence,
    - protect the Author's reputation,
    - or clarify a material decision.

    If it does none of these things, it should not happen.
    """
)


PUBLICATION_PACKAGE_CONTRACT = clean(
    """
    # Publication Package Contract

    ## Status

    Active Version 1.0 product contract.

    ## Purpose

    The Publication Package Contract defines the complete article
    output delivered by Ramrattan AI Editorial Studio.

    ## Default Package Components

    Every complete Version 1.0 publication package contains:

    1. Hero Visual prompt
    2. Hero Visual - 720 × 425
    3. Headline
    4. Hook
    5. Insight 1
    6. Insight 2 when editorially useful
    7. Practical Takeaway
    8. Call to Action
    9. Source and attribution
    10. Hashtags
    11. LinkedIn Description
    12. Portable Editorial Project

    ## Article-First Scope

    The package supports professional articles.

    Carousel output is not part of Version 1.0.

    ## Presentation

    The Studio presents:

    - the Hero Visual,
    - followed by text with clear headings,
    - followed by the Editorial Risk result,
    - followed by next actions.

    ## Internal Consistency

    The package should maintain alignment between:

    - thesis,
    - headline,
    - hook,
    - insights,
    - practical takeaway,
    - CTA,
    - Hero Visual,
    - source attribution,
    - hashtags,
    - and LinkedIn Description.

    ## Independent Revision

    Components may be reviewed and revised independently.

    A change does not automatically regenerate the complete package.

    ## Export Fast Path

    The first completion action is:

    > Export the publication package

    The standard export should include:

    - article Markdown,
    - Hero Visual,
    - Portable Editorial Project,
    - and selected supporting metadata.

    An optional ZIP package may bundle the selected files.

    ## Copy and Download

    The Product may support:

    - Copy Article
    - Download Article
    - Copy Hero Visual
    - Download Hero Visual
    - Download Portable Editorial Project
    - Export ZIP

    The Author chooses where downloaded files are stored.

    The Product does not require storage paths.

    ## Completion Statement

    A suitable completion message is:

    > Your publication package is ready.

    The Product should then present the export fast path and the
    secondary actions.
    """
)


EDITORIAL_PHILOSOPHY = clean(
    """
    # Editorial Philosophy

    ## Purpose

    This document summarizes the behaviour expected from every product
    capability.

    It does not replace the PRD, Product Principles, Studio Contract,
    or architecture documents.

    ## The Editorial Partner

    Ramrattan AI Editorial Studio exists to help professionals develop
    and publish responsible, distinctive thought leadership without
    forcing them through a rigid content workflow.

    ## Non-Negotiable Behaviours

    The Studio:

    - protects the Author's reputation,
    - reduces unnecessary effort,
    - preserves approved work,
    - explains material reasoning,
    - adapts to current context,
    - maximizes responsible forward progress,
    - never pretends to know,
    - optimizes for the Author's next likely action,
    - remains proactively helpful but concise,
    - and never knowingly disseminates false information.

    ## Editorial Authority

    The Studio contributes:

    - research,
    - fact validation,
    - editorial alternatives,
    - professional judgment,
    - and recommended next actions.

    The Author retains:

    - final editorial choice,
    - ownership,
    - publication authority,
    - and responsibility for publication.

    ## Product Filter

    Every proposed capability should answer:

    1. Does it reduce the Author's effort?
    2. Does it protect the Author's reputation?
    3. Does it make the Studio feel more like an experienced editor
       than a generic AI tool?

    A capability that fails these tests should be reconsidered.
    """
)


PRODUCT_VISION = clean(
    """
    # Product Vision

    ## Why the Product Exists

    Professionals often have valuable ideas, experience, and
    perspective but lack the time, editorial support, research
    discipline, or visual capability required to turn them into
    publication-ready thought leadership.

    Ramrattan AI Editorial Studio closes that gap.

    ## Who It Is For

    The Product is for professional Authors, managers, practitioners,
    specialists, and leaders who want to publish credible,
    differentiated articles without surrendering their voice or
    editorial control.

    ## What Problem It Solves

    The Studio turns incomplete and evolving material into a
    trustworthy article publication package while:

    - preserving Author perspective,
    - validating facts,
    - improving evidence,
    - reducing decision friction,
    - creating a 720 × 425 Hero Visual,
    - supporting focused revision,
    - and enabling portable resumption.

    ## What It Will Not Become

    Version 1.0 is not:

    - a generic marketing-content suite,
    - a carousel generator,
    - a social-media automation platform,
    - a hosted document-storage service,
    - a team collaboration workspace,
    - an automatic publishing bot,
    - or a system that replaces the Author's judgment.

    ## Non-Negotiable Principles

    Future capabilities must preserve:

    - article-first scope,
    - editorial integrity,
    - Author ownership,
    - stateless operation by default,
    - low-friction collaboration,
    - transparent reasoning,
    - portable projects,
    - and Author control.

    Detailed behaviour is defined in the Product Principles, Studio
    Contract, PRD, and architecture documents.
    """
)


RELEASE_V1 = clean(
    """
    # Version 1.0 Product Release Definition

    ## Status

    Target product release.

    ## Release Identity

    Product version:

    ```text
    v1.0
    ```

    Architecture baseline:

    ```text
    2026.08.01v06
    ```

    ## Version 1.0 Promise

    Version 1.0 helps an Author transform a natural starting point into
    a fact-checked, publication-ready professional article and
    720 × 425 Hero Visual, then export the complete work or save a
    Portable Editorial Project for later resumption.

    ## Version 1.0 Author Journey

    ```text
    Start New or Resume Existing
                ↓
    Provide URL, text, document, audio, video, or project file
                ↓
    Understand input
                ↓
    Assess sources
                ↓
    Verify evidence
                ↓
    Review LMHS Editorial Risk
                ↓
    Build Adaptive Editorial Context
                ↓
    Create Publication Package
                ↓
    Present Hero Visual and structured text
                ↓
    Export Publication Package
    ```

    ## Included Capabilities

    Version 1.0 includes:

    - Natural Editorial Intake
    - URL and pasted-text intake
    - Document intake where supported
    - Audio and video intake where supported
    - Editorial Integrity Pipeline
    - LMHS Editorial Risk
    - Adaptive Editorial Context
    - Progressive clarification
    - Article generation
    - Hero Visual prompt
    - 720 × 425 Hero Visual
    - Publication Package Contract
    - Three-option editorial alternatives
    - Contextual recommendation with rationale
    - Manual Author option
    - Intelligent dependency management
    - Focused revision
    - Portable Editorial Project
    - VCM filename management
    - Resume Existing Project
    - Export Publication Package
    - Optional ZIP packaging
    - Temporal integrity checks on resumed projects
    - Optional use of host-platform preferences
    - Optional use of a host-provided preferred name

    ## Version 1.0 Required Publication Package

    - Hero Visual prompt
    - Hero Visual - 720 × 425
    - Headline
    - Hook
    - Insight 1
    - Insight 2 when useful
    - Practical Takeaway
    - CTA
    - Source and attribution
    - Hashtags
    - LinkedIn Description
    - Portable Editorial Project

    ## Version 1.0 Non-Goals

    Version 1.0 excludes:

    - Carousel generation
    - Hosted Author Library
    - Hosted accounts
    - Cloud synchronization
    - Team workspaces
    - Multi-user collaboration
    - Automatic direct publishing
    - Engagement analytics dashboards
    - Subscription and billing implementation
    - CMS integration
    - Cross-project semantic search
    - Persistent personal profiles managed by the Product
    - Multi-tenant storage

    ## Release Completion Criteria

    Version 1.0 is ready when:

    - the complete Author journey is demonstrable,
    - all required package components are produced,
    - LMHS Editorial Risk is operational,
    - false or materially misleading foundations are blocked,
    - focused revisions preserve unaffected work,
    - Portable Editorial Projects export and resume correctly,
    - VCM naming rules pass,
    - the Hero Visual is 720 × 425,
    - export is the primary completion action,
    - all automated tests pass,
    - the capability demos are complete,
    - and the Kanban contains no unresolved Version 1.0 blockers.

    ## Later Versions

    Future versions may introduce:

    - hosted persistence,
    - user accounts,
    - preference services,
    - collaboration,
    - direct publishing,
    - analytics,
    - commercial subscription features,
    - and additional publication formats.

    These require separate product and architecture decisions.
    """
)


ARCHITECTURE_BASELINE = clean(
    f"""
    # Architecture Baseline - {ARCHITECTURE_BASELINE_VERSION}

    ## Status

    Active Version 1.0 architecture baseline.

    ## Baseline Version

    ```text
    {ARCHITECTURE_BASELINE_VERSION}
    ```

    ## Purpose

    This document records the coherent architecture supporting the
    target Version 1.0 release.

    It is a checkpoint, not a substitute for detailed architecture
    documents or ADRs.

    ## Capabilities Included

    - Repository Foundation
    - Editorial Workflow Prototype - historical
    - Adaptive Product Foundation
    - Article-First Alignment
    - Adaptive Editorial Context
    - Portable Editorial Projects
    - Editorial Integrity Pipeline
    - Editorial Judgment Framework
    - Editorial Collaboration Model
    - Publication Package Contract
    - Version 1.0 Product Release Definition

    ## Major Decisions

    - The Product is article-first.
    - The Hero Visual is 720 × 425.
    - The Adaptive Editorial Context is the system kernel.
    - The Studio is stateless by default.
    - Portable Editorial Projects preserve continuity.
    - The Product does not require external storage paths.
    - Editorial Integrity precedes publication recommendation.
    - LMHS communicates Editorial Risk.
    - The Studio challenges unsupported assumptions constructively.
    - Export is the completion fast path.
    - Carousel generation is excluded from Version 1.0.

    ## Related ADRs

    - ADR-001 - Historical workflow decision
    - Adaptive Editorial Context architecture - `docs/architecture/Editorial_Context_Model.md`
    - ADR-003 - Article-First Publication Package
    - ADR-004 - Portable Editorial Projects
    - ADR-005 - Editorial Integrity Pipeline

    ## Supersedes

    This baseline supersedes earlier informal architecture summaries.

    Earlier ADRs and product records remain available for historical
    traceability.

    ## Compatibility

    Future architecture changes must:

    - preserve Portable Editorial Project compatibility where practical,
    - provide schema migration when required,
    - preserve Author ownership,
    - and identify any breaking Version 1.0 contract change explicitly.
    """
)


ADR_005 = clean(
    """
    # ADR-005 - Adopt the Editorial Integrity Pipeline

    ## Status

    Accepted

    ## Date

    2026-08-01

    ## Context

    The Studio may receive:

    - reliable sources,
    - weak sources,
    - outdated statistics,
    - copied paywalled material,
    - unsupported claims,
    - fabricated information,
    - or content intended to deceive or cause harm.

    Immediate article generation would create unacceptable factual,
    professional, and reputational risk.

    ## Decision

    Every project must pass through the Editorial Integrity Pipeline
    before the Studio recommends a publication package as ready.

    The Pipeline includes:

    1. Understanding the input
    2. Assessing sources
    3. Verifying evidence
    4. Reviewing Editorial Risk
    5. Creating the publication package

    Editorial Risk uses:

    - Low
    - Moderate
    - High
    - Severe

    ## Author Experience

    Processing stages should be visible.

    Low-risk assessments may be summarized briefly.

    Moderate, High, and Severe risks require explanation and a
    recommended next action.

    ## Judgment

    The Studio may:

    - challenge,
    - educate,
    - rebuild,
    - redirect,
    - or decline

    according to the severity and nature of the risk.

    ## Consequences

    ### Positive

    - Protects the Author's reputation
    - Reduces misinformation risk
    - Makes source quality visible
    - Creates a consistent publication gate
    - Supports constructive recovery
    - Differentiates the Product from generic generators

    ### Costs

    - Requires research and verification
    - May increase processing time
    - Requires transparent uncertainty
    - Requires time-sensitive revalidation
    - May block unsafe publication directions

    ## Alternatives Rejected

    ### Generate First, Fact-Check Later

    Rejected because false information may become embedded throughout
    the publication package.

    ### Refuse Every Uncertain Request

    Rejected because uncertainty can often be resolved through research,
    qualification, or reframing.

    ### Rely Only on Host-Platform Safety

    Rejected because general safety protections do not replace
    editorial source assessment, attribution, originality, and
    publication judgment.
    """
)


PRD_V13 = clean(
    """
    # Product Requirements Document - Version 1.3

    ## Product

    Ramrattan AI Editorial Studio

    ## Status

    Active Version 1.0 product baseline.

    ## Supersedes

    PRD v1.2 as the active product definition.

    Earlier PRDs remain preserved as historical records.

    ## Product Definition

    Ramrattan AI Editorial Studio is an adaptive editorial operating
    system that helps professional Authors turn evolving ideas,
    sources, evidence, experience, and perspective into responsible,
    publication-ready articles and 720 × 425 Hero Visuals.

    ## Version 1.0 Primary Outcome

    A complete publication package containing:

    - Hero Visual prompt
    - Hero Visual - 720 × 425
    - Headline
    - Hook
    - Insight 1
    - Insight 2 when useful
    - Practical Takeaway
    - CTA
    - Source and attribution
    - Hashtags
    - LinkedIn Description
    - Portable Editorial Project

    ## Input Experience

    The Author may begin with any compatible host-platform input,
    including:

    - URL
    - Text
    - Notes
    - Draft
    - Document
    - Audio
    - Video
    - Portable Editorial Project

    The Author should not need to choose a technical intake mode.

    ## Editorial Integrity

    The Editorial Integrity Pipeline must run before publication
    recommendation.

    It must:

    - assess source quality,
    - verify material claims,
    - distinguish fact from opinion,
    - identify outdated information,
    - assess originality and attribution,
    - identify harmful or deceptive requests,
    - and assign LMHS Editorial Risk.

    ## LMHS Editorial Risk

    Risk levels are:

    - Low
    - Moderate
    - High
    - Severe

    Percentages are not used.

    ## False Information

    The Studio must not knowingly disseminate materially false,
    fabricated, deceptive, or dangerously misleading information.

    ## Author Challenge

    When evidence does not support the Author's assumption, the Studio
    should explain the evidence and offer a more defensible direction.

    ## Options and Recommendations

    When appropriate, the Studio should present three strong options.

    Each option includes concise rationale.

    The Studio's recommendation appears after all options and is based
    on the Author's material, thesis, audience, and objective.

    Every option set includes a way for the Author to provide their own
    answer.

    ## Interaction Style

    The Studio should:

    - infer before asking,
    - ask only focused questions,
    - explain questions only when the reason is not obvious,
    - remain proactively helpful but concise,
    - avoid endless recommendation loops,
    - and never pretend to remember unavailable information.

    ## Host Context

    The Studio may use reliable host-platform context when available,
    including a preferred name or writing preference.

    The Product must remain correct when host context is unavailable.

    ## Intelligent Dependency Management

    A requested change updates only the requested component.

    The Studio may identify related components and ask whether the
    Author wants them updated.

    It must not silently regenerate them.

    ## Publication Completion

    The Studio presents:

    - the Hero Visual,
    - the complete structured text,
    - the Editorial Risk result,
    - and the completion actions.

    The first completion action is:

    > Export the publication package

    Secondary actions are:

    - Review or improve a component
    - Download the Portable Editorial Project only
    - Start a new Editorial Project

    ## Portable Projects

    Portable Editorial Projects preserve context required for future
    resumption.

    They use:

    ```text
    Ramrattan-Editorial-Project_<Article-Slug>_YYYY.MM.DDvNN.md
    ```

    Generated filenames must not exceed 255 characters.

    ## Temporal Integrity

    Resumed projects should be reviewed for time-sensitive evidence
    before republication.

    ## Version 1.0 Exclusions

    Version 1.0 excludes:

    - Carousels
    - Hosted Author Library
    - Hosted accounts
    - Cloud synchronization
    - Team workspaces
    - Direct automatic publishing
    - Analytics dashboards
    - Persistent Product-managed Author profiles
    - Multi-tenant storage
    - Subscription implementation

    ## Success Measures

    - Time to first publication package
    - Low Author effort
    - LMHS assessment quality
    - Fact-verification quality
    - Author confidence to publish
    - Preservation of Author perspective
    - Focused revision success
    - Export success
    - Project resume success
    - Hero Visual compliance
    - Publication-package completeness
    """
)


CAPABILITY_DEMO = clean(
    """
    # Capability 006 Demo - Editorial Integrity and V1.0 Baseline

    ## Status

    Architecture and product baseline established.

    Implementation items remain open until the behavioural engine is
    complete.

    ## Problem

    A generic content generator may immediately turn supplied material
    into polished falsehoods.

    It may also:

    - conceal uncertainty,
    - rely on weak sources,
    - use outdated statistics,
    - repeat paywalled material too closely,
    - or force the Author through unnecessary questions.

    ## What Changed

    Capability 006 establishes:

    - Editorial Integrity Pipeline
    - LMHS Editorial Risk
    - Editorial Judgment Framework
    - Editorial Collaboration Model
    - Publication Package Contract
    - Product Vision
    - Version 1.0 Release Definition
    - VCM Architecture Baseline
    - Export-first completion UX

    ## Five-Stage Demonstration

    ```text
    ✓ Understanding your input
    ✓ Assessing your sources
    ✓ Verifying the evidence
    ✓ Reviewing editorial risks
    ✓ Creating your publication package
    ```

    ## Low-Risk Scenario

    Author supplies a reputable source and clear perspective.

    Studio:

    - validates material claims,
    - confirms Low Editorial Risk,
    - creates the package,
    - and presents Export first.

    ## High-Risk Scenario

    Author supplies an unsupported statistic.

    Studio:

    - explains that it could not substantiate the statistic,
    - shows High Editorial Risk,
    - identifies stronger evidence,
    - and offers to rebuild the article around verified facts.

    ## Severe-Risk Scenario

    Author requests a knowingly deceptive article.

    Studio:

    - identifies Severe Editorial Risk,
    - declines the deceptive direction,
    - explains the concern,
    - and offers a legitimate alternative where possible.

    ## Option Interaction

    The Studio displays three alternatives.

    Each includes rationale.

    The recommendation appears after all three.

    The Author may select an option or provide their own.

    ## Completion UX

    ```text
    Your publication package is ready.

    1. Export the publication package
    2. Review or improve a component
    3. Download the Portable Editorial Project only
    4. Start a new Editorial Project
    ```

    ## Version 1.0 Demonstration Target

    The complete Version 1.0 demo must show:

    - URL or natural input
    - Integrity status progression
    - LMHS Editorial Risk
    - Adaptive Editorial Context
    - Complete article package
    - 720 × 425 Hero Visual
    - Focused revision
    - VCM project export
    - Resume Existing Project
    - Export fast path

    ## What We Learned

    Editorial quality is not enough.

    The Product must make truthfulness, source quality, publication
    risk, and Author reputation visible parts of the experience.

    ## What Comes Next

    Implement the Editorial Integrity Pipeline and Article Engine
    behaviours required by Version 1.0.
    """
)


CAPABILITY_TEST = clean(
    '''
    """Tests for Capability 006 architecture and V1.0 baseline."""

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


    class Capability006Tests(unittest.TestCase):
        def test_integrity_pipeline_exists(self) -> None:
            path = (
                ROOT
                / "docs"
                / "architecture"
                / "Editorial_Integrity_Pipeline.md"
            )

            self.assertTrue(path.is_file())

        def test_five_visible_stages_are_defined(self) -> None:
            content = normalized(
                "docs/architecture/"
                "Editorial_Integrity_Pipeline.md"
            )

            self.assertIn(
                "Understanding your input",
                content,
            )
            self.assertIn(
                "Assessing your sources",
                content,
            )
            self.assertIn(
                "Verifying the evidence",
                content,
            )
            self.assertIn(
                "Reviewing editorial risks",
                content,
            )
            self.assertIn(
                "Creating your publication package",
                content,
            )

        def test_lmhs_risk_is_defined(self) -> None:
            content = normalized(
                "docs/architecture/"
                "Editorial_Integrity_Pipeline.md"
            )

            for level in (
                "Low Editorial Risk",
                "Moderate Editorial Risk",
                "High Editorial Risk",
                "Severe Editorial Risk",
            ):
                self.assertIn(level, content)

            self.assertIn(
                "does not use arbitrary percentages",
                content,
            )

        def test_false_information_guardrail_exists(self) -> None:
            content = normalized(
                "docs/architecture/"
                "Editorial_Integrity_Pipeline.md"
            )

            self.assertIn(
                "must not knowingly disseminate",
                content,
            )
            self.assertIn(
                "materially false",
                content,
            )

        def test_progressive_recovery_exists(self) -> None:
            content = normalized(
                "docs/architecture/"
                "Editorial_Integrity_Pipeline.md"
            )

            self.assertIn(
                "Progressive Recovery",
                content,
            )
            self.assertIn(
                "maximize responsible forward progress",
                content,
            )

        def test_temporal_integrity_exists(self) -> None:
            content = normalized(
                "docs/architecture/"
                "Editorial_Integrity_Pipeline.md"
            )

            self.assertIn(
                "Temporal Integrity",
                content,
            )
            self.assertIn(
                "statistics may be outdated",
                content,
            )

        def test_option_interaction_has_three_choices(self) -> None:
            content = normalized(
                "docs/architecture/"
                "Editorial_Collaboration_Model.md"
            )

            self.assertIn(
                "provide three high-quality options",
                content,
            )
            self.assertIn(
                "must not label an option as Recommended",
                content,
            )
            self.assertIn(
                "provide their own content",
                content,
            )

        def test_recommendation_follows_options(self) -> None:
            content = normalized(
                "docs/architecture/"
                "Editorial_Collaboration_Model.md"
            )

            self.assertIn(
                "After all options are presented",
                content,
            )
            self.assertIn(
                "editorial opinion",
                content,
            )

        def test_dependency_updates_are_not_silent(self) -> None:
            content = normalized(
                "docs/architecture/"
                "Editorial_Collaboration_Model.md"
            )

            self.assertIn(
                "Change only the requested component",
                content,
            )
            self.assertIn(
                "must not silently regenerate",
                content,
            )

        def test_export_is_fast_path(self) -> None:
            content = normalized(
                "docs/architecture/"
                "Publication_Package_Contract.md"
            )

            self.assertIn(
                "Export the publication package",
                content,
            )
            self.assertIn(
                "first completion action",
                content,
            )

        def test_publication_package_components_exist(self) -> None:
            content = normalized(
                "docs/architecture/"
                "Publication_Package_Contract.md"
            )

            for phrase in (
                "Hero Visual prompt",
                "Hero Visual - 720 × 425",
                "Headline",
                "Hook",
                "Insight 1",
                "Practical Takeaway",
                "Call to Action",
                "Source and attribution",
                "Hashtags",
                "LinkedIn Description",
                "Portable Editorial Project",
            ):
                self.assertIn(phrase, content)

        def test_version_one_release_exists(self) -> None:
            path = (
                ROOT
                / "docs"
                / "product"
                / "Release_v1.0.md"
            )

            self.assertTrue(path.is_file())

        def test_version_one_excludes_carousels(self) -> None:
            content = normalized(
                "docs/product/Release_v1.0.md"
            )

            self.assertIn(
                "Carousel generation",
                content,
            )
            self.assertIn(
                "Version 1.0 excludes",
                content,
            )

        def test_product_vision_is_concise_reference(self) -> None:
            content = normalized(
                "docs/product/Product_Vision.md"
            )

            self.assertIn(
                "What It Will Not Become",
                content,
            )
            self.assertIn(
                "Detailed behaviour is defined",
                content,
            )

        def test_architecture_baseline_uses_vcm(self) -> None:
            content = normalized(
                "docs/architecture/baselines/"
                "Architecture_Baseline_2026.08.01v01.md"
            )

            self.assertIn(
                "2026.08.01v01",
                content,
            )
            self.assertIn(
                "Active Version 1.0 architecture baseline",
                content,
            )

        def test_prd_v13_is_active(self) -> None:
            content = normalized(
                "docs/product/PRD_v1.3.md"
            )

            self.assertIn(
                "Active Version 1.0 product baseline",
                content,
            )
            self.assertIn(
                "LMHS Editorial Risk",
                content,
            )
            self.assertIn(
                "Export the publication package",
                content,
            )


    if __name__ == "__main__":
        unittest.main()
    '''
)


# ---------------------------------------------------------------------
# Managed updates to existing documentation
# ---------------------------------------------------------------------

README_BLOCK = clean(
    """
    ## Capability 006 - Editorial Integrity

    Every publication project passes through five visible stages:

    1. Understanding your input
    2. Assessing your sources
    3. Verifying the evidence
    4. Reviewing editorial risks
    5. Creating your publication package

    Editorial Risk uses:

    - Low
    - Moderate
    - High
    - Severe

    The Studio does not knowingly disseminate materially false,
    fabricated, deceptive, or dangerously misleading information.

    ## Version 1.0 Target

    Version 1.0 delivers:

    - article-first editorial intake,
    - fact and evidence validation,
    - Adaptive Editorial Context,
    - 720 × 425 Hero Visual,
    - complete Publication Package,
    - focused component revision,
    - Portable Editorial Projects,
    - Resume Existing Project,
    - and export-first completion.

    Carousel generation is not part of Version 1.0.

    See:

    - `docs/product/Product_Vision.md`
    - `docs/product/Release_v1.0.md`
    - `docs/product/PRD_v1.3.md`
    - `docs/architecture/Editorial_Integrity_Pipeline.md`
    - `docs/architecture/Publication_Package_Contract.md`
    """
)


CURRENT_FOCUS_BLOCK = clean(
    """
    ## Capability 006 and Version 1.0 Focus

    The current product priority is implementing the complete Version
    1.0 Author journey.

    The active foundations are:

    - Editorial Integrity Pipeline
    - Adaptive Editorial Context
    - Article Engine
    - Hero Visual System
    - Publication Package Contract
    - Portable Editorial Projects
    - Resume Existing Project
    - Export Publication Package

    Version 1.0 is article-first.

    Carousels, hosted storage, team collaboration, direct publishing,
    and analytics remain outside the Version 1.0 scope.
    """
)


PRODUCT_PRINCIPLES_BLOCK = clean(
    """
    ## Capability 006 Principles

    ### Truth Before Fluency

    The Studio must not turn unsupported or false material into polished
    misinformation.

    ### Protect the Author's Reputation

    Editorial risk is a product concern, not merely a disclaimer.

    ### Challenge Constructively

    When evidence does not support a premise, explain the evidence and
    offer a defensible alternative.

    ### Never Pretend to Know

    Do not imply memory, verification, certainty, identity, or context
    that is not reliably available.

    ### Complete the Review Before Interrupting

    Consolidate and prioritize material observations where practical.

    ### Proactively Helpful, but Concise

    Offer material improvements without creating an endless revision
    loop.

    ### Optimize for the Author's Next Likely Action

    Export is the completion fast path.

    ### Preserve Approved Work

    Change only what the Author requests unless they approve related
    dependency updates.

    ### Progressive Recovery

    Maximize responsible forward progress before requesting more effort.

    ### Temporal Integrity

    Revalidate time-sensitive evidence when a project is resumed or
    republished.
    """
)


STUDIO_CONTRACT_BLOCK = clean(
    """
    ## Editorial Integrity Contract

    The Studio will:

    - assess sources before publication recommendation,
    - verify material claims where practical,
    - distinguish fact, assertion, inference, and opinion,
    - communicate LMHS Editorial Risk,
    - explain material uncertainty,
    - challenge unsupported assumptions constructively,
    - and offer a responsible next path.

    The Studio will not:

    - fabricate evidence,
    - fabricate citations,
    - knowingly disseminate materially false information,
    - conceal material uncertainty,
    - silently regenerate approved components,
    - or claim memory or verification it does not have.

    ## Completion Contract

    The Studio will present the complete publication package and place
    Export the publication package first among completion actions.
    """
)


GLOSSARY_BLOCK = clean(
    """
    ## Editorial Integrity Pipeline

    The five-stage process that understands input, assesses sources,
    verifies evidence, reviews Editorial Risk, and creates the
    publication package.

    ## LMHS Editorial Risk

    The four-level editorial risk model:

    - Low
    - Moderate
    - High
    - Severe

    ## Editorial Judgment

    The Studio's proportionate decision to proceed, challenge, educate,
    rebuild, redirect, or decline.

    ## Progressive Recovery

    Continuing responsibly with reliable context already available
    before asking the Author to provide more information.

    ## Temporal Integrity

    Reassessing time-sensitive evidence when a saved project is resumed
    or republished.

    ## Publication Package Contract

    The required Version 1.0 set of article, Hero Visual, attribution,
    distribution, and portable-project components.

    ## Fast Path

    The Author's most likely immediate action. At publication
    completion, the fast path is Export the publication package.

    ## Preference Cascade

    The precedence of current project instructions, Portable Editorial
    Project settings, available host-platform preferences, and Studio
    defaults.

    ## Editorial Intake

    The interpretation of any compatible Author starting material,
    including URLs, text, documents, audio, video, and portable project
    files.

    ## Architecture Baseline

    A VCM-versioned checkpoint describing the coherent product and
    system architecture at a particular time.
    """
)


DECISION_LOG_BLOCK = clean(
    f"""
    ## Capability 006 Decisions

    | Date | Level | Decision | Rationale |
    |---|---:|---|---|
    | 2026-08-01 | D5 | Define Version 1.0 explicitly | Future backlog decisions require a stable release boundary. |
    | 2026-08-01 | D4 | Adopt the Editorial Integrity Pipeline | The Studio must assess sources and evidence before publication recommendation. |
    | 2026-08-01 | D3 | Display five visible processing stages | The Author should understand and appreciate the work being performed. |
    | 2026-08-01 | D3 | Adopt LMHS Editorial Risk | Low, Moderate, High, and Severe communicate risk without false precision. |
    | 2026-08-01 | D4 | Prohibit knowing dissemination of materially false information | Truthfulness and Author reputation are non-negotiable. |
    | 2026-08-01 | D3 | Use proportionate challenge, rebuild, redirection, and refusal | Refusal is reserved for scenarios where responsible recovery is not possible. |
    | 2026-08-01 | D3 | Offer three curated alternatives | Three options reduce blank-page effort without overwhelming the Author. |
    | 2026-08-01 | D3 | Place recommendation after all options | Editorial advice should not bias evaluation before the Author sees the alternatives. |
    | 2026-08-01 | D3 | Always allow an Author-provided option | The Studio reduces effort without reducing control. |
    | 2026-08-01 | D3 | Use intelligent dependency management | Requested components change first; related updates require Author approval. |
    | 2026-08-01 | D3 | Place Export first at completion | Export is the Author's primary fast path after successful generation. |
    | 2026-08-01 | D3 | Support host-compatible audio and video intake | The Product should meet the Author where their ideas naturally exist. |
    | 2026-08-01 | D3 | Use host context only when reliably available | Personalization is optional and must never become a correctness dependency. |
    | 2026-08-01 | D4 | Version architecture baselines using VCM | Architecture history should follow the established YYYY.MM.DDvNN convention. |

    ## Active Architecture Baseline

    ```text
    2026.08.01v06
    ```

    ## Capability 006 Learning

    Editorial Integrity is not a hidden back-end check.

    It is a visible Author experience that demonstrates how the Product
    protects factual quality, publication readiness, and professional
    reputation.
    """
)


ROADMAP_BLOCK = clean(
    """
    ## Version 1.0 Capability Roadmap

    ### Completed Foundations

    - [x] Capability 001 - Repository Foundation
    - [x] Capability 002 - Editorial Workflow Prototype
    - [x] Capability 003 - Adaptive Product Foundation
    - [x] Capability 004 - Article-First Alignment
    - [x] Capability 005 - Adaptive Editorial Context Architecture
    - [x] Capability 006 - Editorial Integrity and V1.0 Baseline

    ### Version 1.0 Implementation Backlog

    - [ ] Implement Editorial Intake
    - [ ] Implement host-compatible document intake
    - [ ] Implement host-compatible audio and video intake
    - [ ] Implement source assessment
    - [ ] Implement evidence verification
    - [ ] Implement LMHS Editorial Risk
    - [ ] Implement Editorial Judgment responses
    - [ ] Implement Adaptive Editorial Context runtime
    - [ ] Implement Article Engine
    - [ ] Implement Publication Package Contract
    - [ ] Implement three-option editorial interaction
    - [ ] Implement intelligent dependency management
    - [ ] Implement 720 × 425 Hero Visual System
    - [ ] Implement Portable Editorial Project serialization
    - [ ] Implement Resume Existing Project
    - [ ] Implement VCM export naming
    - [ ] Implement ZIP export
    - [ ] Implement temporal-integrity review
    - [ ] Complete Version 1.0 end-to-end demo
    - [ ] Complete Version 1.0 release readiness review

    ### Post-Version 1.0 Backlog

    - [ ] Optional Portable Project Index
    - [ ] Hosted Project Synchronization
    - [ ] Product-managed Author preferences
    - [ ] Direct publishing integrations
    - [ ] Editorial analytics
    - [ ] Collaboration workspaces
    - [ ] Subscription and billing
    - [ ] Additional publication formats

    ### Explicitly Excluded from Version 1.0

    - [ ] Carousel generation
    - [ ] Multi-tenant hosted storage
    - [ ] Team collaboration
    - [ ] Automatic direct publishing
    """
)


CHANGELOG_BLOCK = clean(
    f"""
    ### Added - Capability 006

    - Editorial Integrity Pipeline
    - Editorial Judgment Framework
    - Editorial Collaboration Model
    - Publication Package Contract
    - Editorial Philosophy
    - Product Vision
    - Version 1.0 Product Release Definition
    - PRD v1.3
    - ADR-005
    - LMHS Editorial Risk
    - Five visible processing stages
    - Progressive Recovery
    - Temporal Integrity
    - Curated three-option interaction contract
    - Intelligent dependency management
    - Export-first completion UX
    - Architecture Baseline {ARCHITECTURE_BASELINE_VERSION}
    - Capability 006 demo
    - Capability 006 validation tests

    ### Changed - Capability 006

    - Defined Version 1.0 scope and exclusions
    - Made fact and evidence review mandatory before publication
      recommendation
    - Added host-compatible document, audio, and video intake
    - Made Export the primary completion action
    - Required Author approval before related component regeneration
    - Required concise, consolidated editorial observations
    - Added VCM versioning for architecture baselines
    """
)


DEFINITION_OF_DONE_BLOCK = clean(
    """
    ## Capability 006 Completion Additions

    Before a Version 1.0 capability is Done, confirm:

    - Editorial Integrity implications are documented.
    - LMHS Editorial Risk behaviour is tested where applicable.
    - The capability does not knowingly disseminate false information.
    - Author-facing interactions are concise.
    - Related components are not silently regenerated.
    - Export remains the completion fast path.
    - Version 1.0 scope is not expanded accidentally.
    - The Capability Demo is current.
    - The GitHub Project and backlog are current.
    """
)


PROJECT_CHARTER_BLOCK = clean(
    """
    ## Version 1.0 Charter Alignment

    The target Version 1.0 release is an article-first editorial
    operating system.

    It combines:

    - Editorial Integrity,
    - Adaptive Editorial Context,
    - article creation,
    - 720 × 425 Hero Visual creation,
    - focused editorial revision,
    - Portable Editorial Projects,
    - and export-first completion.

    Hosted storage, collaboration, direct publishing, analytics, and
    carousel generation are outside the Version 1.0 charter.
    """
)


MARKER_BLOCKS = {
    "README.md": (
        "CAPABILITY_006_README",
        README_BLOCK,
    ),
    "docs/product/Current_Product_Focus.md": (
        "CAPABILITY_006_CURRENT_FOCUS",
        CURRENT_FOCUS_BLOCK,
    ),
    "docs/product/Product_Principles.md": (
        "CAPABILITY_006_PRODUCT_PRINCIPLES",
        PRODUCT_PRINCIPLES_BLOCK,
    ),
    "docs/product/Studio_Contract.md": (
        "CAPABILITY_006_STUDIO_CONTRACT",
        STUDIO_CONTRACT_BLOCK,
    ),
    "docs/product/Glossary.md": (
        "CAPABILITY_006_GLOSSARY",
        GLOSSARY_BLOCK,
    ),
    "docs/product/Decision_Log.md": (
        "CAPABILITY_006_DECISION_LOG",
        DECISION_LOG_BLOCK,
    ),
    "docs/architecture/Definition_of_Done.md": (
        "CAPABILITY_006_DEFINITION_OF_DONE",
        DEFINITION_OF_DONE_BLOCK,
    ),
    "docs/Project_Charter.md": (
        "CAPABILITY_006_PROJECT_CHARTER",
        PROJECT_CHARTER_BLOCK,
    ),
    "ROADMAP.md": (
        "CAPABILITY_006_ROADMAP",
        ROADMAP_BLOCK,
    ),
    "CHANGELOG.md": (
        "CAPABILITY_006_CHANGELOG",
        CHANGELOG_BLOCK,
    ),
}


NEW_FILES = {
    (
        "docs/architecture/"
        "Editorial_Integrity_Pipeline.md"
    ): EDITORIAL_INTEGRITY_PIPELINE,

    (
        "docs/architecture/"
        "Editorial_Judgment_Framework.md"
    ): EDITORIAL_JUDGMENT_FRAMEWORK,

    (
        "docs/architecture/"
        "Editorial_Collaboration_Model.md"
    ): EDITORIAL_COLLABORATION_MODEL,

    (
        "docs/architecture/"
        "Publication_Package_Contract.md"
    ): PUBLICATION_PACKAGE_CONTRACT,

    (
        "docs/architecture/"
        "Editorial_Philosophy.md"
    ): EDITORIAL_PHILOSOPHY,

    (
        "docs/architecture/baselines/"
        f"Architecture_Baseline_{ARCHITECTURE_BASELINE_VERSION}.md"
    ): ARCHITECTURE_BASELINE,

    (
        "docs/architecture/adr/"
        "ADR-005-adopt-the-editorial-integrity-pipeline.md"
    ): ADR_005,

    "docs/product/Product_Vision.md":
        PRODUCT_VISION,

    "docs/product/Release_v1.0.md":
        RELEASE_V1,

    "docs/product/PRD_v1.3.md":
        PRD_V13,

    (
        "docs/demos/"
        "Capability-006-Editorial-Integrity-and-V1-Baseline.md"
    ): CAPABILITY_DEMO,

    "tests/test_capability006_editorial_integrity.py":
        CAPABILITY_TEST,
}


# ---------------------------------------------------------------------
# Errors and command execution
# ---------------------------------------------------------------------

class CapabilityError(RuntimeError):
    """Raised when Capability 006 cannot proceed safely."""


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
    """Return parsed JSON command output."""
    raw = output(command, cwd=cwd)

    if not raw:
        return {}

    return json.loads(raw)


# ---------------------------------------------------------------------
# Repository checks
# ---------------------------------------------------------------------

def repository_root() -> Path:
    """Locate and verify the repository."""
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
    """Require the Capability 006 feature branch."""
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
    """Detect truncated or syntactically invalid paste."""
    path = Path(__file__).resolve()
    content = path.read_text(encoding="utf-8")

    if SCRIPT_SENTINEL not in content:
        raise CapabilityError(
            "The script appears incomplete. The sentinel is missing."
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
    """Return porcelain Git status lines."""
    raw = output(
        ["git", "status", "--porcelain"],
        cwd=root,
    )

    return [
        line
        for line in raw.splitlines()
        if line.strip()
    ]


def verify_preview_working_tree(root: Path) -> None:
    """Permit only this untracked bootstrap before application."""
    allowed = {
        f"?? {SCRIPT_RELATIVE_PATH}",
    }

    unexpected = [
        line
        for line in working_tree_lines(root)
        if line not in allowed
    ]

    if unexpected:
        raise CapabilityError(
            "Unexpected working-tree changes exist:\n"
            + "\n".join(unexpected)
            + "\n\nOnly the untracked Capability 006 bootstrap "
            "is allowed before --apply."
        )

    print(
        "Working tree contains only the expected "
        "Capability 006 bootstrap."
    )


# ---------------------------------------------------------------------
# File operations
# ---------------------------------------------------------------------

def managed_block(
    marker_name: str,
    content: str,
) -> str:
    """Build a marker-managed Markdown section."""
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
    """Insert or replace one managed block."""
    if not path.is_file():
        raise CapabilityError(
            f"Missing required existing document: {path}"
        )

    original = path.read_text(encoding="utf-8")

    start = f"<!-- {marker_name}_START -->"
    end = f"<!-- {marker_name}_END -->"

    start_exists = start in original
    end_exists = end in original

    if start_exists != end_exists:
        raise CapabilityError(
            f"Incomplete marker pair in {path}."
        )

    block = managed_block(
        marker_name,
        content,
    )

    if start_exists:
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
    """Write deterministic Capability 006 files."""
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
    """Update complementary and legacy documentation."""
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
    """Apply the complete local baseline."""
    write_new_files(root)
    update_existing_documents(root)

    print()
    print(
        "Capability 006 files and documentation "
        "have been written."
    )


# ---------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------

REQUIRED_FILES = tuple(NEW_FILES.keys())


def validate_required_files(root: Path) -> None:
    """Confirm all new files exist."""
    missing = [
        relative
        for relative in REQUIRED_FILES
        if not (root / relative).is_file()
    ]

    if missing:
        raise CapabilityError(
            "Missing Capability 006 files:\n"
            + "\n".join(
                f"  - {relative}"
                for relative in missing
            )
        )

    print("All required Capability 006 files are present.")


def validate_product_language(root: Path) -> None:
    """Validate important decisions semantically."""
    checks: dict[str, tuple[str, ...]] = {
        (
            "docs/architecture/"
            "Editorial_Integrity_Pipeline.md"
        ): (
            "must not knowingly disseminate",
            "Low Editorial Risk",
            "Moderate Editorial Risk",
            "High Editorial Risk",
            "Severe Editorial Risk",
            "Progressive Recovery",
            "Temporal Integrity",
        ),

        (
            "docs/architecture/"
            "Editorial_Collaboration_Model.md"
        ): (
            "provide three high-quality options",
            "must not label an option as Recommended",
            "After all options are presented",
            "must not silently regenerate",
            "Export the publication package",
        ),

        (
            "docs/architecture/"
            "Publication_Package_Contract.md"
        ): (
            "Hero Visual - 720 × 425",
            "LinkedIn Description",
            "Portable Editorial Project",
            "Export the publication package",
        ),

        "docs/product/Release_v1.0.md": (
            "Version 1.0 Promise",
            "Audio and video intake",
            "Carousel generation",
            "Export Publication Package",
        ),

        "docs/product/PRD_v1.3.md": (
            "Active Version 1.0 product baseline",
            "LMHS Editorial Risk",
            "three strong options",
            "must not silently regenerate",
            "Export the publication package",
        ),

        (
            "docs/architecture/baselines/"
            f"Architecture_Baseline_{ARCHITECTURE_BASELINE_VERSION}.md"
        ): (
            ARCHITECTURE_BASELINE_VERSION,
            "Active Version 1.0 architecture baseline",
            "ADR-005",
        ),
    }

    for relative, phrases in checks.items():
        content = normalize_markdown(
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
        "Capability 006 product-language validation passed."
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
        "Capability 006 repository validation passed."
    )


def show_status(root: Path) -> None:
    """Display the local change set."""
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
    """Show the planned local and GitHub changes."""
    print()
    print("Capability 006 preview:")
    print()

    print("New files:")

    for relative in NEW_FILES:
        print(f"  - {relative}")

    print("\nManaged documentation updates:")

    for relative in MARKER_BLOCKS:
        print(f"  - {relative}")

    print("\nDecisions being locked:")

    decisions = (
        "Define the Version 1.0 release boundary",
        "Adopt the Editorial Integrity Pipeline",
        "Display five Author-facing processing stages",
        "Use LMHS Editorial Risk",
        "Never knowingly disseminate materially false information",
        "Challenge unsupported assumptions constructively",
        "Offer three curated alternatives with rationale",
        "Place recommendations after all options",
        "Always permit an Author-provided option",
        "Prevent silent dependent-component regeneration",
        "Make Export the completion fast path",
        "Support host-compatible documents, audio, and video",
        "Use host context only when reliably available",
        "Use VCM for architecture baselines",
        "Update Kanban and Version 1.0 backlog",
    )

    for decision in decisions:
        print(f"  - {decision}")

    print("\nPreview mode changes nothing.")

    print("\nApply local files with:")

    print(
        "  python3 scripts/"
        "bootstrap_capability006_editorial_integrity.py "
        "--apply"
    )


# ---------------------------------------------------------------------
# GitHub Project synchronization
# ---------------------------------------------------------------------

PROJECT_DESCRIPTION = (
    "Version 1.0 capability roadmap for an adaptive editorial "
    "operating system focused on fact-checked professional articles, "
    "720 × 425 Hero Visuals, portable projects, and export-first "
    "publication packages."
)


PROJECT_README = f"""# Ramrattan AI Editorial Studio

## Current position

- Capabilities 001-005 - complete
- Capability 006 - Editorial Integrity and V1.0 Baseline
- Architecture baseline - {ARCHITECTURE_BASELINE_VERSION}

## Version 1.0 target

Version 1.0 accepts natural Author input, performs source and evidence
review, produces a professional article and 720 × 425 Hero Visual,
supports focused revision, and exports a Portable Editorial Project.

## Editorial Integrity stages

1. Understanding your input
2. Assessing your sources
3. Verifying the evidence
4. Reviewing Editorial Risk
5. Creating your publication package

## Editorial Risk

- Low
- Moderate
- High
- Severe

## Version 1.0 backlog

- Editorial Intake
- Source and evidence validation
- Adaptive Editorial Context runtime
- Article Engine
- Publication Package Contract
- Hero Visual System
- Portable Project export and resume
- VCM versioning
- ZIP export
- End-to-end Version 1.0 demo

## Product boundary

Version 1.0 excludes carousels, hosted storage, collaboration,
automatic direct publishing, and analytics dashboards.
"""


CAPABILITY_006_ISSUE_TITLE = (
    "Capability 006 - Editorial Integrity and V1.0 Baseline"
)

BACKLOG_ISSUES: dict[str, str] = {
    (
        "Capability 007 - Implement Editorial Intake "
        "and Source Assessment"
    ): clean(
        """
        ## Objective

        Implement natural editorial intake and the first two visible
        Editorial Integrity stages.

        ## Scope

        - URL input
        - Pasted text
        - Documents supported by the host platform
        - Audio and video supported by the host platform
        - Input interpretation
        - Source-quality assessment
        - Status display

        ## Version

        Version 1.0
        """
    ),

    (
        "Capability 008 - Implement Evidence Validation "
        "and LMHS Editorial Risk"
    ): clean(
        """
        ## Objective

        Implement material-claim verification and Low, Moderate, High,
        and Severe Editorial Risk.

        ## Scope

        - Fact versus assertion
        - Corroboration
        - Outdated evidence
        - Paywalled excerpts
        - Progressive Recovery
        - Temporal Integrity
        - Constructive challenge and redirection

        ## Version

        Version 1.0
        """
    ),

    (
        "Capability 009 - Build the Article Engine "
        "and Publication Package"
    ): clean(
        """
        ## Objective

        Generate the complete Version 1.0 publication package.

        ## Required components

        - Hero Visual prompt
        - Headline
        - Hook
        - Insight 1
        - Insight 2 where useful
        - Practical Takeaway
        - CTA
        - Source and attribution
        - Hashtags
        - LinkedIn Description

        ## Version

        Version 1.0
        """
    ),

    (
        "Capability 010 - Build the 720 × 425 "
        "Hero Visual System"
    ): clean(
        """
        ## Objective

        Generate and revise the Version 1.0 Hero Visual.

        ## Requirements

        - 720 × 425
        - Article-aligned visual thesis
        - Brand-neutral by default
        - No logos or recognizable faces by default
        - Independent focused revision
        - Download and copy support

        ## Version

        Version 1.0
        """
    ),

    (
        "Capability 011 - Implement Portable Project "
        "Resume and Export"
    ): clean(
        """
        ## Objective

        Implement the Author-owned project continuity and export path.

        ## Scope

        - VCM naming
        - 255-character filename limit
        - Markdown serialization
        - Resume Existing Project
        - Temporal Integrity review
        - Article download
        - Hero Visual download
        - Portable Project download
        - Optional ZIP export

        ## Version

        Version 1.0
        """
    ),

    (
        "Version 1.0 - End-to-End Demo "
        "and Release Readiness"
    ): clean(
        """
        ## Objective

        Demonstrate and validate the complete Version 1.0 Author
        journey.

        ## Acceptance criteria

        - Start New
        - Resume Existing
        - Five visible integrity stages
        - LMHS Editorial Risk
        - Complete publication package
        - 720 × 425 Hero Visual
        - Focused component revision
        - Export-first completion
        - VCM project export
        - Passing repository validation
        - Completed capability demos
        """
    ),

    (
        "Future - Host Platform Preference "
        "and Identity Integration"
    ): clean(
        """
        ## Future capability

        Use reliable host-platform context to reduce unnecessary Author
        questions.

        ## Possible scope

        - Preferred display name
        - Language preference
        - Editorial preference hints
        - Preference precedence
        - Transparency and override controls

        The Product must not depend on this capability for correctness.
        """
    ),

    (
        "Future - Commercial Packaging, "
        "Subscriptions, and Billing"
    ): clean(
        """
        ## Future capability

        Define and implement commercial access to the Product.

        ## Possible scope

        - Product editions
        - Subscription plans
        - Entitlements
        - Usage limits
        - Billing
        - Paywall
        - Account management
        - Privacy and retention requirements

        This work is outside Version 1.0 content-production scope.
        """
    ),
}


def project_payload(root: Path) -> dict[str, Any]:
    """Return project metadata."""
    return json_output(
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


def validate_project(root: Path) -> None:
    """Confirm the expected GitHub Project."""
    project = project_payload(root)

    if project.get("id") != PROJECT_ID:
        raise CapabilityError(
            "GitHub Project #1 does not match the expected project ID."
        )


def issue_list(root: Path) -> list[dict[str, Any]]:
    """Return all repository issues."""
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


def create_issue(
    root: Path,
    title: str,
    body: str,
) -> dict[str, Any]:
    """Create an issue and return its metadata."""
    url = output(
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

    issue = find_issue(root, title)

    if issue is None:
        raise CapabilityError(
            f"Created issue but could not resolve it: {url}"
        )

    return issue


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

    created = create_issue(
        root,
        title,
        body,
    )

    print(
        f"Created issue "
        f"#{created['number']} - {title}"
    )

    return created


def project_items(root: Path) -> list[dict[str, Any]]:
    """Return all GitHub Project items."""
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

    return payload.get("items", [])


def project_item_for_url(
    root: Path,
    url: str,
) -> dict[str, Any] | None:
    """Find a project item by content URL."""
    for item in project_items(root):
        content = item.get("content") or {}

        if content.get("url") == url:
            return item

    return None


def ensure_project_item(
    root: Path,
    url: str,
) -> dict[str, Any]:
    """Add content to Project #1 when missing.

    GitHub Project items may take several seconds to become visible
    after item-add succeeds, so resolve the item with bounded retries.
    """
    import time

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
                    f"Resolved Project item after "
                    f"{attempt} lookup attempts."
                )
            return created

        print(
            f"Project item is not visible yet "
            f"(attempt {attempt}/10); waiting..."
        )
        time.sleep(2)

    raise CapabilityError(
        f"GitHub accepted the Project item but it did not become "
        f"visible within the retry window: {url}"
    )

def set_status(
    root: Path,
    item_id: str,
    status: str,
) -> None:
    """Set a GitHub Project item status."""
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


def update_capability_five_status(root: Path) -> None:
    """Mark the Capability 005 issue Done when present."""
    candidate_titles = {
        "Capability 5 - Build the Adaptive Editorial Context",
        "Sprint 3A - Build the Adaptive Editorial Context",
    }

    for issue in issue_list(root):
        if issue.get("title") not in candidate_titles:
            continue

        item = ensure_project_item(
            root,
            issue["url"],
        )

        set_status(
            root,
            item["id"],
            "Done",
        )

        print(
            f"Marked issue #{issue['number']} Done."
        )

        return


def sync_project(root: Path) -> None:
    """Synchronize GitHub Project and backlog."""
    validate_required_files(root)
    validate_product_language(root)
    run_repository_validation(root)

    run(
        ["gh", "auth", "status"],
        cwd=root,
    )

    validate_project(root)

    update_capability_five_status(root)

    capability_issue = ensure_issue(
        root,
        CAPABILITY_006_ISSUE_TITLE,
        clean(
            """
            ## Objective

            Establish the Editorial Integrity Pipeline and the complete
            Version 1.0 architecture and release baseline.

            ## Scope

            - Five visible integrity stages
            - LMHS Editorial Risk
            - Editorial Judgment Framework
            - Editorial Collaboration Model
            - Publication Package Contract
            - Product Vision
            - Version 1.0 definition
            - VCM architecture baseline
            - Complementary documentation alignment
            - Kanban and backlog alignment

            ## Acceptance criteria

            - Local validation passes
            - Architecture and product documents agree
            - Version 1.0 scope is explicit
            - Backlog represents the implementation path
            """
        ),
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
        "Capability 006 marked In Progress."
    )

    for title, body in BACKLOG_ISSUES.items():
        issue = ensure_issue(
            root,
            title,
            body,
        )

        item = ensure_project_item(
            root,
            issue["url"],
        )

        set_status(
            root,
            item["id"],
            "Todo",
        )

        print(
            f"Backlog item set to Todo: {title}"
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
        "GitHub Project and Version 1.0 backlog synchronized."
    )


# ---------------------------------------------------------------------
# Arguments and main
# ---------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Establish Capability 006 and "
            "the Version 1.0 product baseline."
        )
    )

    mode = parser.add_mutually_exclusive_group()

    mode.add_argument(
        "--apply",
        action="store_true",
        help=(
            "Write and validate local Capability 006 files."
        ),
    )

    mode.add_argument(
        "--sync-project",
        action="store_true",
        help=(
            "Synchronize GitHub Project and backlog."
        ),
    )

    return parser.parse_args()


def main() -> int:
    """Preview, apply, or synchronize Capability 006."""
    args = parse_args()

    try:
        root = repository_root()

        print(f"Repository: {root}")

        verify_script_integrity()
        verify_branch(root)

        if args.sync_project:
            sync_project(root)

        elif args.apply:
            verify_preview_working_tree(root)
            apply_local_changes(root)
            validate_required_files(root)
            validate_product_language(root)
            run_repository_validation(root)
            show_status(root)

            print()
            print(
                "Capability 006 and Version 1.0 baseline "
                "have been applied and validated."
            )
            print(
                "Nothing has been committed, pushed, "
                "or changed on GitHub."
            )

        else:
            verify_preview_working_tree(root)
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


# CAPABILITY_006_EDITORIAL_INTEGRITY_COMPLETE
# END OF SCRIPT - CAPABILITY 006


if __name__ == "__main__":
    raise SystemExit(main())