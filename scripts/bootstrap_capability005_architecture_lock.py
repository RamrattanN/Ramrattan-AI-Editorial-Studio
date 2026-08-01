#!/usr/bin/env python3
"""
Capability 5 - Architecture Lockdown

Ramrattan AI Editorial Studio

Preview:
    python3 scripts/bootstrap_capability005_architecture_lock.py

Apply local repository changes:
    python3 scripts/bootstrap_capability005_architecture_lock.py --apply

Synchronize GitHub planning after local review:
    python3 scripts/bootstrap_capability005_architecture_lock.py \
        --sync-project

This script:

- Verifies the expected repository and feature branch
- Verifies that the pasted script is complete
- Creates the Capability 5 architecture baseline
- Creates PRD v1.2 while preserving earlier PRDs
- Documents the Adaptive Editorial Context
- Documents Portable Editorial Projects
- Documents durable source context
- Documents paywalled and transient source handling
- Documents Editorial Integrity
- Establishes the Capability Definition of Done
- Creates the Capability 5 demo baseline
- Updates existing product documents using managed marker blocks
- Adds resilient architecture-baseline tests
- Validates the complete repository
- Optionally aligns GitHub Project planning

The default preview changes nothing.

The --apply mode changes local files only.

The --sync-project mode changes GitHub planning only after the local
architecture baseline exists and validates.

This script does not commit, push, or open a pull request.
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
# Repository and branch configuration
# ---------------------------------------------------------------------

EXPECTED_REPOSITORY = "Ramrattan-AI-Editorial-Studio"

EXPECTED_REMOTE_FRAGMENT = (
    "RamrattanN/Ramrattan-AI-Editorial-Studio"
)

OWNER = "RamrattanN"

REPO_SLUG = (
    "RamrattanN/Ramrattan-AI-Editorial-Studio"
)

EXPECTED_BRANCH = "feature/adaptive-editorial-context"

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
    "bootstrap_capability005_architecture_lock.py"
)

EXPECTED_UNTRACKED_FILES = {
    "scripts/start_next_capability.py",
    SCRIPT_RELATIVE_PATH,
}

SCRIPT_SENTINEL = (
    "CAPABILITY_005_ARCHITECTURE_LOCK_COMPLETE"
)

CAPABILITY_NAME = (
    "Capability 5 - Adaptive Editorial Context"
)


# ---------------------------------------------------------------------
# General helpers
# ---------------------------------------------------------------------

def clean(value: str) -> str:
    """
    Remove embedded indentation and ensure one trailing newline.
    """
    return textwrap.dedent(value).strip() + "\n"


def normalize_markdown(value: str) -> str:
    """
    Normalize Markdown for resilient phrase validation.

    Blockquote markers and line wrapping should not create false
    failures.
    """
    return " ".join(
        value.replace(">", " ").split()
    )


# ---------------------------------------------------------------------
# Architecture document - Adaptive Editorial Context
# ---------------------------------------------------------------------

EDITORIAL_CONTEXT_MODEL = clean(
    """
    # Adaptive Editorial Context Model

    ## Status

    Active architecture baseline for Capability 5.

    ## Purpose

    The Adaptive Editorial Context is the working memory of Ramrattan
    AI Editorial Studio.

    It represents what the Studio currently understands about one
    Author-led article project.

    It exists:

    - before the first article draft,
    - during first-pass generation,
    - during review and refinement,
    - during Hero Visual development,
    - before publication,
    - after publication,
    - and when a saved project is resumed later.

    ## Core Principle

    > The Studio continuously interprets Author contributions, updates
    > a shared Editorial Context, and determines the most useful next
    > editorial action.

    The Author does not need to select a rigid workflow mode.

    ## Author Experience

    The Context must reduce cognitive load.

    It must not become a questionnaire, wizard, or laborious intake
    form.

    The Studio should:

    1. infer before asking,
    2. preserve creative momentum,
    3. ask only focused questions,
    4. retain useful context,
    5. preserve unaffected approved work,
    6. explain significant recommendations,
    7. remain reversible,
    8. and aim for a publication-ready first pass quickly.

    ## Natural Contributions

    The Author may contribute:

    - a URL,
    - copied source material,
    - a headline,
    - a topic,
    - something remembered from the news,
    - a personal observation,
    - professional experience,
    - a perspective,
    - a correction,
    - a draft,
    - a revision request,
    - a publication URL,
    - or a previously saved Portable Editorial Project.

    The Author does not need to label the contribution.

    ## Context Components

    ```text
    Adaptive Editorial Context
    ├── Project Identity
    ├── Author Intent
    ├── Inputs
    ├── Sources
    ├── Durable Source Context
    ├── Evidence
    ├── Author Perspective
    ├── Editorial Thesis
    ├── Candidate Angles
    ├── Constraints
    ├── Open Questions
    ├── Article State
    ├── Hero Visual State
    ├── Decisions
    ├── Editorial Integrity
    ├── Readiness
    ├── Revision History
    └── Publication Information
    ```

    ## Project Identity

    Project Identity answers:

    - What body of work is this?
    - What permanent identifier belongs to it?
    - What human-readable title describes it?
    - Which project version is current?
    - When was it created?
    - When was it last updated?

    Project Identity remains stable when:

    - the article headline changes,
    - the article slug changes,
    - the thesis changes,
    - or the saved project filename changes.

    A duplicated project receives a new Project ID while optionally
    preserving a reference to its parent project.

    ## Author Intent

    Author Intent is the Studio's current interpretation of what the
    Author is trying to accomplish.

    Intent may be:

    - explicit,
    - inferred,
    - revised,
    - uncertain,
    - or superseded.

    Intent is not a compulsory field the Author must complete.

    ## Inputs

    Inputs preserve what the Author supplied.

    Examples:

    - URLs
    - Pasted excerpts
    - Headlines
    - Topics
    - News recollections
    - Observations
    - Perspectives
    - Notes
    - Drafts
    - Corrections
    - Constraints
    - Publication links
    - Resume-project documents

    Inputs should retain:

    - their original form where appropriate,
    - their contribution type,
    - their timestamp,
    - and their relationship to the project.

    ## Sources

    Sources identify where information originated.

    A source may include:

    - URL,
    - title,
    - source author,
    - publisher,
    - publication date,
    - access date,
    - source type,
    - paywall status,
    - source-quality assessment,
    - verification status,
    - and relevance to the article.

    A URL is useful provenance.

    A URL is not durable memory.

    ## Durable Source Context

    Referenced URLs may:

    - expire,
    - move,
    - change,
    - become unavailable,
    - become paywalled,
    - or display materially different content later.

    The Context must therefore preserve the editorial value of a
    source, not merely its address.

    Durable Source Context may include:

    - citation metadata,
    - a concise source summary,
    - key claims,
    - important statistics,
    - relevant dates,
    - the Author's reaction,
    - the source's role in the article,
    - the evidence actually used,
    - verification notes,
    - and a limited essential excerpt where appropriate.

    The purpose is continuity.

    The purpose is not to create an unauthorized archive of the full
    source.

    ## Paywalled and Author-Supplied Material

    An Author may paste material that:

    - came from a paywalled publication,
    - cannot be revisited later,
    - is visible only through the Author's subscription,
    - or may disappear after the current interaction.

    The Context should preserve enough information to understand the
    editorial significance later.

    It should normally retain:

    - known citation metadata,
    - a concise source summary,
    - the specific claims used,
    - relevant statistics,
    - the Author's interpretation,
    - how the material affected the thesis,
    - and only the minimum necessary excerpt.

    It should not automatically retain the complete paywalled article.

    It should record when:

    - the complete source was not retained,
    - future independent verification may be limited,
    - or reverification may be needed before republication.

    ## Evidence

    Evidence is information used to support, qualify, or challenge a
    claim.

    Evidence may include:

    - verified facts,
    - statistics,
    - research findings,
    - official statements,
    - professional experience,
    - quotations,
    - examples,
    - and documented observations.

    Evidence must distinguish:

    - verified fact,
    - source assertion,
    - Author experience,
    - reasonable inference,
    - and unresolved uncertainty.

    ## Author Perspective

    Author Perspective records what the Author:

    - believes,
    - observes,
    - questions,
    - agrees with,
    - rejects,
    - or has learned through experience.

    Perspective is a first-class component.

    It must never be silently replaced with generic AI opinion.

    ## Editorial Thesis

    The Editorial Thesis is the central proposition the article
    develops and supports.

    It is not necessarily the headline.

    The thesis may evolve when:

    - new evidence appears,
    - the Author changes position,
    - a weak claim is removed,
    - or a stronger editorial angle emerges.

    ## Candidate Angles

    The Context may retain several possible editorial directions.

    One angle may be current while others remain:

    - proposed,
    - rejected,
    - superseded,
    - or reserved for future use.

    Rejected ideas may remain valuable because they explain the
    evolution of the article.

    ## Constraints

    Constraints may include:

    - intended audience,
    - tone,
    - word count,
    - LinkedIn article requirements,
    - privacy requirements,
    - subjects to avoid,
    - timing,
    - source restrictions,
    - brand rules,
    - or professional sensitivities.

    ## Open Questions

    Open Questions represent unresolved matters that could affect:

    - quality,
    - accuracy,
    - integrity,
    - or editorial direction.

    The Studio should ask the Author only when an unresolved question
    materially blocks useful progress.

    ## Article State

    Article State may contain:

    - working title,
    - headline,
    - hook,
    - structure,
    - first draft,
    - revised drafts,
    - approved article,
    - supporting publication copy,
    - and publication status.

    Article State is versioned.

    Earlier meaningful versions should remain recoverable where
    practical.

    ## Hero Visual State

    Hero Visual State may contain:

    - visual thesis,
    - visual direction,
    - Hero Visual copy,
    - image-generation prompt,
    - dimensions,
    - suggested filename,
    - approval status,
    - and version.

    The required Hero Visual size is 720 × 425.

    The Author may copy or save the Hero Visual wherever they choose.

    The Product does not require the Author to report its storage
    location.

    The conversational term infographic may be accepted, while
    Hero Visual remains the architectural term.

    ## Decisions

    Decisions record meaningful Author or Studio choices.

    Examples:

    - thesis approved,
    - source rejected,
    - headline selected,
    - visual direction changed,
    - article approved,
    - publication channel selected,
    - or project duplicated.

    Decisions must remain understandable and revisable.

    ## Editorial Integrity

    Editorial Integrity records whether the project currently satisfies
    professional, evidentiary, ethical, and safety expectations.

    It includes:

    - source quality,
    - attribution completeness,
    - claim support,
    - uncertainty disclosure,
    - originality,
    - privacy,
    - professional conduct,
    - safety concerns,
    - and publication blockers.

    ## Readiness

    Readiness is multidimensional.

    The Studio may independently assess:

    - intent readiness,
    - source readiness,
    - evidence readiness,
    - perspective readiness,
    - thesis readiness,
    - article readiness,
    - Hero Visual readiness,
    - integrity readiness,
    - and publication readiness.

    Readiness should guide behaviour without exposing a rigid workflow
    to the Author.

    ## Revision History

    Revision History records meaningful editorial events.

    Examples:

    - perspective added,
    - thesis changed,
    - source removed,
    - evidence challenged,
    - article revised,
    - Hero Visual replaced,
    - publication URL recorded,
    - or project resumed.

    Revision History should not record every keystroke.

    ## Publication Information

    Publication Information may include:

    - publication channel,
    - publication date,
    - public URL,
    - publication status,
    - post-publication observations,
    - and follow-up opportunities.

    Public URLs are optional.

    A project must remain useful when:

    - no publication URL was supplied,
    - the URL later expires,
    - the post is removed,
    - or the platform changes its URL structure.

    LinkedIn is the initial article channel.

    Facebook or another channel may be recorded when the Author
    chooses to reference or republish the article elsewhere.

    ## Component Versioning

    Editorial components support:

    - a permanent component identifier,
    - one current version,
    - earlier versions,
    - status,
    - provenance,
    - dependency information,
    - and timestamps.

    A component may be:

    - missing,
    - observed,
    - inferred,
    - proposed,
    - approved,
    - revised,
    - superseded,
    - rejected,
    - archived,
    - or removed.

    ## Dependency Intelligence

    Dependencies do not create a fixed workflow.

    They identify which work may require review after a change.

    Examples:

    - A changed palette should not rewrite the article.
    - A changed Hero Visual should not alter verified evidence.
    - A changed headline may require a revised hook.
    - A changed thesis may affect the article and Hero Visual.
    - A new source may strengthen evidence without changing the thesis.
    - A changed publication URL should not alter editorial content.

    ## First-Pass and Refinement Behaviour

    The Context supports both:

    1. development before the first article package, and
    2. refinement after the first article package.

    The Author is not required to choose between these modes.

    The Studio interprets the contribution and updates the appropriate
    components.

    ## Time-to-Value

    When sufficient starting material exists, the Studio should aim to
    produce the first publication-ready article package within
    approximately 10 minutes.

    The Context must support rapid understanding without imposing a
    laborious intake process.

    ## Insufficient Starting Material

    When the material cannot support a distinctive, defensible article,
    the Studio should not generate generic filler.

    It should:

    1. explain why the material is insufficient,
    2. identify what is missing,
    3. provide an example of a stronger starting point,
    4. and recommend one useful next action.

    ## Relationship to Portable Editorial Projects

    The Adaptive Editorial Context is the live in-session
    representation of the work.

    A Portable Editorial Project is the Author-owned, human-readable
    export of the context needed to resume work later.

    The Studio is stateless by default.

    The Author controls the exported files and chooses where to save
    them.

    The Product does not depend on external file paths.
    """
)


# ---------------------------------------------------------------------
# Architecture document - Portable Editorial Projects
# ---------------------------------------------------------------------

PORTABLE_EDITORIAL_PROJECT = clean(
    """
    # Portable Editorial Project Specification

    ## Status

    Active architecture baseline for Capability 5.

    ## Purpose

    A Portable Editorial Project allows an Author to resume an article
    project later without requiring the Studio to host or retain the
    Author's work.

    It preserves a small amount of high-value context in a
    human-readable Markdown file.

    ## Core Principle

    > The Studio's memory belongs to the Author.

    Every project should be:

    - portable,
    - resumable,
    - human-readable,
    - versioned,
    - private by default,
    - and under the Author's control.

    ## Product Boundary

    The Studio creates downloadable or copyable outputs.

    The Author may:

    - download the article,
    - copy the article text,
    - download the Hero Visual,
    - copy the Hero Visual,
    - download the Portable Editorial Project,
    - or download an optional ZIP package.

    The Author chooses where those outputs are stored.

    The Product does not require:

    - a local path,
    - a Dropbox path,
    - a OneDrive path,
    - a Google Drive path,
    - or any other storage location.

    The Product must not burden the Author with reporting file paths.

    ## Why Saving Matters

    At the appropriate point, the Studio should explain the value of
    saving the Portable Editorial Project.

    Example:

    > Save your Editorial Project
    >
    > This small file preserves the context behind your article,
    > including its thesis, sources, Author perspective, important
    > evidence, editorial decisions, publication information, and next
    > actions.
    >
    > Saving it allows the Studio to resume your work later without
    > asking you to reconstruct the project from memory.
    >
    > Store it wherever you keep important work. The Studio does not
    > need to retain a copy.

    Saving should be encouraged without becoming a mandatory or
    laborious step.

    ## Start Experience

    The opening experience should support:

    - Start a New Editorial Project
    - Resume an Existing Editorial Project

    Resume should accept a compatible Portable Editorial Project file.

    The Studio should validate the file before restoring context.

    ## File Naming Standard

    The project Markdown filename follows:

    ```text
    Ramrattan-Editorial-Project_<Article-Slug>_YYYY.MM.DDvNN.md
    ```

    Example:

    ```text
    Ramrattan-Editorial-Project_AI-Governance-Beyond-Compliance_2026.08.01v01.md
    ```

    ## Version Control Method

    The version identifier follows:

    ```text
    YYYY.MM.DDvNN
    ```

    Where:

    - `YYYY` is the four-digit year,
    - `MM` is the two-digit month,
    - `DD` is the two-digit day,
    - `vNN` is the sequential version for that date.

    Examples:

    ```text
    2026.08.01v01
    2026.08.01v02
    2026.08.01v03
    2026.08.07v01
    ```

    The daily sequence begins at `v01`.

    Existing versions are not silently overwritten.

    ## Filename Length

    Generated filenames must never exceed 255 characters.

    The product must preserve:

    - the fixed product prefix,
    - the version suffix,
    - and the file extension.

    The article slug is shortened when required.

    When shortening could create ambiguity or collision, the filename
    receives a short collision-resistant identifier.

    Example:

    ```text
    Ramrattan-Editorial-Project_How-Enterprise-AI-Governance-Changes-Decision-Making-8F3A2C_2026.08.01v01.md
    ```

    The Product may warn when a destination rejects a generated file.

    It must not require the Author to disclose the destination path.

    ## Slug Rules

    The article slug should:

    - remain human-readable,
    - use letters, numbers, and hyphens,
    - replace whitespace with hyphens,
    - remove unsafe characters,
    - collapse repeated hyphens,
    - remove leading and trailing hyphens,
    - and preserve meaningful words where practical.

    ## Permanent Identity

    Every project contains a permanent machine-readable Project ID.

    Example:

    ```yaml
    project_id: REP-7F3A91C2
    project_slug: AI-Governance-Beyond-Compliance
    document_version: 2026.08.01v01
    previous_version:
    ```

    The permanent Project ID is not derived solely from the title or
    filename.

    ## Portable Project Contents

    The Markdown file should preserve enough context to resume the work
    without carrying unnecessary bulk.

    Suggested structure:

    ```yaml
    studio:
      product: Ramrattan AI Editorial Studio
      schema_version: 1
      created_with_version:
      capability_level:

    project:
      project_id:
      title:
      slug:
      document_version:
      previous_version:
      created_at:
      updated_at:
      status:

    author:
      intent:
      perspective:
      audience:
      tone:
      constraints:

    editorial:
      thesis:
      current_angle:
      key_decisions:
      open_questions:
      next_actions:

    article:
      title:
      suggested_file_name:
      approved:
      word_count:
      article_summary:
      article_text_included:

    hero_visual:
      suggested_file_name:
      dimensions: 720x425
      visual_thesis:
      hero_copy:
      generation_prompt:
      approved:
      image_included:

    publication:
      status:
      linkedin_url:
      facebook_url:
      published_at:

    sources:
      - source_id:
        source_type:
        url:
        title:
        source_author:
        publisher:
        publication_date:
        accessed_at:
        paywalled:
        source_quality:
        verification_status:
        durable_summary:
        key_claims:
        statistics_used:
        author_reaction:
        editorial_role:
        retained_excerpt:
        full_source_retained: false
        reverification_may_be_required:

    integrity:
      attribution_complete:
      claims_supported:
      uncertainty_disclosed:
      originality_reviewed:
      privacy_reviewed:
      safety_reviewed:
      blockers:

    history:
      - version:
        date:
        summary:
    ```

    The final format may use structured front matter plus readable
    Markdown sections.

    ## Article Content

    The project file may contain:

    - the complete current article,
    - a concise article summary,
    - or a reference to an accompanying article file within the ZIP.

    The Author may also copy the article directly from the Product.

    Resumption must remain possible when the separately downloaded
    article file is missing.

    ## Hero Visual Context

    The Markdown project cannot be expected to contain the complete
    binary Hero Visual unless it is part of an optional ZIP package.

    It should preserve enough context to understand or recreate it:

    - visual thesis,
    - Hero Visual copy,
    - dimensions,
    - generation prompt,
    - visual direction,
    - approval status,
    - and suggested filename.

    The Author may download or copy the Hero Visual independently.

    The Product does not need to know where the Author saved it.

    ## Durable Source Context

    URLs may expire or change.

    The project file must therefore preserve enough source context to
    understand the evidence later.

    For each material source, preserve where available:

    - citation metadata,
    - concise durable summary,
    - key claims,
    - statistics used,
    - the Author's interpretation,
    - editorial role,
    - access date,
    - verification state,
    - and limited essential excerpts.

    A resumed project should remain understandable when a URL:

    - expires,
    - becomes unavailable,
    - moves behind a paywall,
    - changes content,
    - or redirects elsewhere.

    ## Paywalled Material

    Authors may paste material from a paywalled source.

    The Studio should preserve:

    - known citation metadata,
    - a concise summary,
    - the claims used,
    - important statistics,
    - the Author's response,
    - and only the minimum necessary excerpt.

    The Studio should not automatically place the complete paywalled
    article into the project file.

    The project should record when:

    - the full source was not retained,
    - future independent access may be limited,
    - or reverification may be needed before future publication.

    ## Optional Publication Links

    The project may record:

    - LinkedIn article URL,
    - Facebook post URL,
    - company website URL,
    - or another public publication URL.

    Publication URLs are optional.

    The project must remain useful when a URL:

    - was never supplied,
    - later expires,
    - changes,
    - or becomes inaccessible.

    ## Optional Export Package

    The Studio may offer:

    - Save Project File
    - Download Article
    - Download Hero Visual
    - Copy Article
    - Copy Hero Visual
    - Export ZIP

    Example ZIP contents:

    ```text
    AI-Governance-Beyond-Compliance/
    ├── Ramrattan-Editorial-Project_AI-Governance-Beyond-Compliance_2026.08.01v01.md
    ├── Ramrattan-Article_AI-Governance-Beyond-Compliance_2026.08.01v01.md
    └── Ramrattan-Hero-Visual_AI-Governance-Beyond-Compliance_2026.08.01v01.png
    ```

    The Author may choose to download only the small project file.

    ## Resume Behaviour

    When a compatible project file is supplied, the Studio should:

    1. validate the schema,
    2. identify the project and version,
    3. summarize the restored context,
    4. identify any missing optional assets,
    5. identify unresolved integrity blockers,
    6. explain the most recent known state,
    7. and continue without unnecessary re-entry.

    Example:

    > Welcome back.
    >
    > The latest saved project is
    > `AI Governance Beyond Compliance`, version
    > `2026.08.01v03`.
    >
    > The article was marked as published on LinkedIn.
    >
    > A publication URL was not preserved.
    >
    > The Hero Visual context is available and can be revised or
    > regenerated.
    >
    > The last open action was to consider a follow-up article about
    > operational accountability.

    ## Missing Optional Assets

    A missing article file or Hero Visual file must not corrupt the
    Portable Editorial Project.

    The Studio should:

    - explain which optional asset was not supplied,
    - preserve the remaining editorial context,
    - use included article text where available,
    - regenerate the Hero Visual when appropriate,
    - or continue without the asset.

    ## Privacy

    The project is private by default.

    The Author chooses:

    - whether to download it,
    - where to store it,
    - whether to share it,
    - whether supporting files are included,
    - and whether it is deleted.

    ## Storage Responsibility

    The Studio is stateless by default.

    The initial product does not require:

    - user accounts,
    - hosted document storage,
    - cloud synchronization,
    - reported file paths,
    - multi-tenant databases,
    - or custody of Author files.

    Future hosted storage requires a separate explicit product,
    security, privacy, and commercial decision.

    ## Reuse

    The Author may resume a project to:

    - revise the article,
    - update the Hero Visual,
    - add a publication URL,
    - create a follow-up article,
    - duplicate the project,
    - review earlier evidence,
    - or continue an unfinished idea.

    Reuse should reduce effort without silently carrying outdated,
    weak, or unsupported claims into new work.
    """
)


# ---------------------------------------------------------------------
# Architecture document - Editorial Integrity
# ---------------------------------------------------------------------

EDITORIAL_INTEGRITY_CHARTER = clean(
    """
    # Editorial Integrity Charter

    ## Purpose

    Ramrattan AI Editorial Studio helps Authors create professional
    work that is accurate, original, well-attributed, responsible, and
    suitable for publication.

    Editorial Integrity is a product capability, not a final cosmetic
    check.

    ## Relationship to Platform Safety

    The Studio may operate on an AI platform that supplies evolving
    baseline safety protections.

    Those protections remain valuable.

    They do not replace the Studio's editorial-specific requirements
    for:

    - source assessment,
    - evidence review,
    - attribution,
    - originality,
    - privacy,
    - professional conduct,
    - and publication readiness.

    ## Core Commitments

    The Studio should help the Author produce work that is:

    - truthful about uncertainty,
    - clear about fact versus opinion,
    - supported by defensible evidence,
    - appropriately attributed,
    - original in expression,
    - respectful of privacy,
    - professionally responsible,
    - and free from intentional harm.

    ## Harmful Intent

    The Studio should not assist with article projects intended to:

    - cause physical harm,
    - facilitate illegal activity,
    - harass or threaten another person,
    - deceive readers,
    - impersonate another person,
    - defraud an individual or organization,
    - deliberately spread false information,
    - defame someone through unsupported claims,
    - reveal private or confidential information improperly,
    - or encourage targeted abuse.

    When declining, the Studio should explain the concern without
    providing instructions that enable the harmful objective.

    ## Source Reputation

    The Studio should not treat every URL or pasted passage as equally
    trustworthy.

    Source evaluation may consider:

    - authorship,
    - publisher reputation,
    - editorial standards,
    - primary versus secondary reporting,
    - publication date,
    - conflicts of interest,
    - corroboration,
    - transparency,
    - and evidentiary support.

    A weak source should normally trigger:

    - an explanation,
    - a quality warning,
    - a request for corroboration,
    - or research for stronger evidence.

    A weak source should not silently become the factual foundation of
    an article.

    ## Expired and Transient Sources

    The Studio should assume that URLs may later become unavailable or
    materially change.

    It should preserve:

    - durable source summaries,
    - key claims,
    - statistics actually used,
    - access dates,
    - verification notes,
    - and the Author's interpretation.

    It must not imply that a previously verified source remains current
    indefinitely.

    ## Paywalled and Author-Supplied Excerpts

    The Studio may use Author-supplied excerpts from paywalled
    material as editorial input.

    It should preserve only the source context needed to understand the
    project later.

    It should not automatically archive the complete paywalled work.

    The project should record:

    - known citation metadata,
    - concise summary,
    - claims used,
    - relevant statistics,
    - Author response,
    - limited necessary excerpts,
    - and any future reverification limitation.

    ## Fact, Inference, and Perspective

    The Studio must distinguish:

    - verified facts,
    - claims made by a source,
    - reasonable inference,
    - Author perspective,
    - professional experience,
    - and unresolved uncertainty.

    These categories must not be collapsed into one authoritative tone.

    ## Attribution

    The Studio should preserve provenance for:

    - facts,
    - statistics,
    - quotations,
    - distinctive ideas,
    - research findings,
    - and material source claims.

    It should not fabricate:

    - citations,
    - publication details,
    - quotations,
    - statistics,
    - or source relationships.

    ## Originality

    The Studio synthesizes rather than imitates.

    Source material may inform:

    - evidence,
    - context,
    - and the Author's response.

    It must not determine distinctive wording, structure, framing, or
    expression.

    Close paraphrasing is not sufficient originality.

    ## Author Perspective

    The Studio must preserve the Author's legitimate perspective.

    It may:

    - question unsupported assumptions,
    - identify counterevidence,
    - recommend qualification,
    - or explain reputational risk.

    It must not silently replace the Author's position with generic AI
    opinion.

    ## Privacy and Confidentiality

    The Studio should avoid incorporating:

    - confidential employer information,
    - personal data,
    - private correspondence,
    - protected health information,
    - trade secrets,
    - or sensitive third-party information

    unless the Author has the right and a legitimate reason to use it.

    The Studio should identify possible privacy concerns before
    publication.

    ## Professional Conduct

    The Studio should avoid turning professional disagreement into
    personal attack.

    It should encourage:

    - evidence-led criticism,
    - fair characterization,
    - proportionate language,
    - respectful counterargument,
    - and clear separation between conduct and identity.

    ## Editorial Integrity State

    Every Editorial Context may record:

    - source quality reviewed,
    - attribution complete,
    - claims supported,
    - uncertainty disclosed,
    - originality reviewed,
    - privacy reviewed,
    - safety reviewed,
    - reputational concerns,
    - unresolved blockers,
    - and publication recommendation.

    ## Publication Blockers

    Examples include:

    - unsupported central claim,
    - fabricated or unverifiable citation,
    - materially misleading framing,
    - unresolved privacy concern,
    - defamatory unsupported allegation,
    - harmful intent,
    - plagiarism risk,
    - or a source foundation too weak for the proposed article.

    ## Constructive Refusal

    A refusal should help the Author understand:

    - what concern prevents the Studio from proceeding,
    - why the concern matters,
    - what legitimate alternative may be available,
    - and what safer or more defensible starting point would work.

    ## Publication Responsibility

    The Author retains final publication authority and responsibility.

    The Studio supports judgment.

    It does not replace professional, legal, medical, financial, or
    ethical review where those are required.
    """
)


# ---------------------------------------------------------------------
# Definition of Done
# ---------------------------------------------------------------------

DEFINITION_OF_DONE = clean(
    """
    # Capability Definition of Done

    ## Purpose

    A capability is complete only when the product, architecture,
    implementation, validation, documentation, demonstration, and
    planning artifacts agree.

    Completion is not defined solely by merged code.

    ## 1. Product Alignment

    The capability must state:

    - the problem it solves,
    - the Author benefit,
    - the product principle it reinforces,
    - the current scope,
    - and explicit non-goals.

    The PRD is updated when product behaviour changes.

    The Product Decision Log is updated when a meaningful product
    decision is made.

    ## 2. Author Experience

    The capability must avoid unnecessary Author burden.

    It should confirm:

    - progressive clarification,
    - no avoidable questionnaire,
    - no unnecessary file-path collection,
    - no unnecessary account requirement,
    - clear explanation of important outputs,
    - and a low-friction route to the primary outcome.

    ## 3. Architecture

    An Architecture Decision Record is required when the capability:

    - changes the system model,
    - introduces a major dependency,
    - changes persistence,
    - changes privacy or security assumptions,
    - or materially affects future implementation.

    Architecture documents must explain:

    - responsibilities,
    - boundaries,
    - dependencies,
    - alternatives,
    - consequences,
    - and migration considerations.

    ## 4. Implementation

    Production code must be:

    - understandable,
    - modular,
    - typed where practical,
    - provider-independent where appropriate,
    - and free from hard-coded demonstration topics.

    Temporary repair code must not be merged unless it has a durable
    repository purpose.

    ## 5. Validation

    The capability must pass:

    ```bash
    python3 -m compileall -q studio tests
    python3 -m unittest discover -s tests -v
    python3 studio.py validate
    ```

    Tests should validate behaviour rather than fragile line wrapping
    or formatting accidents.

    ## 6. Documentation

    Required documentation is updated before merge.

    This may include:

    - README
    - Current Product Focus
    - PRD
    - Product Principles
    - Studio Contract
    - Glossary
    - Architecture documents
    - ADRs
    - Roadmap
    - Changelog
    - Decision Log

    ## 7. Capability Demo

    Every completed capability must include a demo document.

    The demo must answer:

    1. What problem existed?
    2. What changed?
    3. Why does it matter?
    4. What can the product now do?
    5. Which acceptance criteria passed?
    6. What was learned?
    7. What comes next?

    The demo should include at least one clear example or diagram.

    ## 8. Project Planning

    The GitHub Project must reflect:

    - completed work,
    - current work,
    - next work,
    - and explicitly deferred work.

    Completed pull requests should be marked Done.

    Active capability work should be marked In Progress.

    ## 9. Repository Hygiene

    Before commit:

    ```bash
    git add -A
    git diff --cached --name-status
    ```

    Review must confirm:

    - correct paths,
    - no double-nested directories,
    - no accidental private files,
    - no credentials,
    - no temporary repair artifacts,
    - and no unrelated changes.

    ## 10. Pull Request

    The pull request must explain:

    - summary,
    - problem,
    - changes,
    - product alignment,
    - Author benefit,
    - validation,
    - risks,
    - and rollback.

    Automated checks must pass before merge.

    ## 11. Merge and Cleanup

    After merge:

    - synchronize `develop`,
    - delete local and remote feature branches,
    - prune stale references,
    - confirm the working tree is clean,
    - and confirm the Kanban board is current.

    ## 12. Learning

    Every capability should record:

    > What did we learn that changed our understanding of the product?

    A capability is not complete until this question has been answered.
    """
)


# ---------------------------------------------------------------------
# Capability demo
# ---------------------------------------------------------------------

CAPABILITY_DEMO = clean(
    """
    # Capability 5 Demo - Adaptive Editorial Context

    ## Status

    Architecture baseline established.

    Implementation demonstration will be completed before Capability 5
    is considered Done.

    ## 1. Problem

    The earlier workflow prototype represented article creation as an
    ordered sequence.

    That model could not fully support:

    - natural mixed input,
    - rapid first-pass creation,
    - changes of direction,
    - focused revision,
    - expired source URLs,
    - paywalled Author-supplied material,
    - portable resumption,
    - or Author-controlled project memory.

    ## 2. What Changed

    Capability 5 establishes:

    - the Adaptive Editorial Context as the system kernel,
    - Editorial Contributions as interpreted events,
    - versioned editorial components,
    - multidimensional readiness,
    - dependency-aware revision,
    - durable source context,
    - Editorial Integrity as a first-class component,
    - and Portable Editorial Projects.

    ## 3. Why It Matters

    The Studio can follow the Author's creative process without turning
    article development into a form or wizard.

    It can preserve context while allowing the Author to:

    - add another source,
    - revise perspective,
    - change the thesis,
    - revise only the conclusion,
    - replace only the Hero Visual,
    - or resume the project later.

    It can also preserve the editorial value of a source when the
    original URL later expires or becomes inaccessible.

    ## 4. Architecture Demonstration

    ```text
    Author Contribution
            │
            ▼
    Intent and Event Interpretation
            │
            ▼
    Adaptive Editorial Context
    ├── Inputs
    ├── Sources
    ├── Durable Source Context
    ├── Evidence
    ├── Perspective
    ├── Thesis
    ├── Article
    ├── Hero Visual
    ├── Integrity
    ├── Readiness
    └── Revision History
            │
            ├───────────────┐
            ▼               ▼
    First Article Package   Focused Revision
            │               │
            └───────┬───────┘
                    ▼
          Portable Editorial Project
    ```

    ## 5. Intended Author Demonstration

    **Author**

    > Here is a URL. I disagree with its conclusion because the real
    > problem is operational accountability.

    **Studio interpretation**

    - Source supplied
    - Topic inferred
    - Author perspective supplied
    - Research may be required
    - Candidate thesis can be proposed

    **Author**

    > I copied this paragraph from a paywalled article. The important
    > part is the statistic and the author's conclusion.

    **Studio behaviour**

    - Record known citation metadata
    - Preserve a concise source summary
    - Preserve the statistic used
    - Preserve the Author's reaction
    - Retain only the minimum necessary excerpt
    - Record that future independent access may be limited

    **Author**

    > Now write the article.

    **Studio behaviour**

    - Use the accumulated Editorial Context
    - Produce the first article package
    - Include a 720 × 425 Hero Visual
    - Preserve evidence provenance

    **Author**

    > Keep the article, but change the Hero Visual.

    **Studio behaviour**

    - Preserve the article
    - Revise only the Hero Visual component
    - Record the decision and new version

    ## 6. Portable Resume Demonstration

    The Author saves:

    ```text
    Ramrattan-Editorial-Project_Operational-Accountability-in-AI_2026.08.01v01.md
    ```

    The Author decides where the file is stored.

    The Product does not ask for or depend on the storage path.

    Later, the Author chooses:

    > Resume an Existing Editorial Project

    The Studio restores:

    - project identity,
    - current thesis,
    - Author perspective,
    - durable source summaries,
    - evidence used,
    - article context,
    - Hero Visual context,
    - optional publication URLs,
    - integrity state,
    - and next actions.

    ## 7. Acceptance Criteria

    Architecture baseline:

    - [x] Adaptive Editorial Context defined
    - [x] Portable Editorial Project defined
    - [x] VCM filename standard defined
    - [x] 255-character filename maximum defined
    - [x] Resume behaviour defined
    - [x] No external path dependency
    - [x] Expired URL resilience defined
    - [x] Paywalled excerpt handling defined
    - [x] Editorial Integrity defined
    - [x] Capability Definition of Done defined
    - [x] Capability Demo standard introduced

    Implementation:

    - [ ] Context model implemented
    - [ ] Component versioning implemented
    - [ ] VCM filename generation implemented
    - [ ] Markdown serialization implemented
    - [ ] Resume validation implemented
    - [ ] Durable source context implemented
    - [ ] Integrity state implemented
    - [ ] Behavioural tests passing

    ## 8. What We Learned

    The product does not need to know where the Author stores their
    files.

    A few kilobytes of well-structured, Author-owned context can
    preserve enough knowledge to resume an article project.

    The durable value of a source is not merely its URL.

    The project should preserve the claims, evidence, metadata,
    interpretation, and editorial significance required to understand
    the work later.

    ## 9. What Comes Next

    Implement the Adaptive Editorial Context and Portable Editorial
    Project model in Python.

    The first implementation should remain independent of article and
    image-generation providers.
    """
)


# ---------------------------------------------------------------------
# ADR
# ---------------------------------------------------------------------

ADR_004 = clean(
    """
    # ADR-004 - Adopt Portable Editorial Projects

    ## Status

    Accepted

    ## Date

    2026-08-01

    ## Decision Level

    D4 - Architecture

    ## Context

    The product requires Authors to resume, review, revise, duplicate,
    or continue article projects later.

    A hosted Author Library would introduce:

    - accounts,
    - authentication,
    - storage costs,
    - synchronization,
    - backups,
    - privacy obligations,
    - retention policies,
    - and multi-tenant architecture.

    The Product also should not require the Author to disclose where
    downloaded files are stored.

    ## Decision

    The Studio will be stateless by default.

    The initial continuity mechanism will be a Portable Editorial
    Project owned and stored by the Author.

    The project will use a small, human-readable Markdown file that
    preserves enough Adaptive Editorial Context to resume work later.

    The Studio will not rely on:

    - local paths,
    - Dropbox paths,
    - OneDrive paths,
    - Google Drive paths,
    - or another reported storage location.

    ## File Naming

    Portable project files use:

    ```text
    Ramrattan-Editorial-Project_<Article-Slug>_YYYY.MM.DDvNN.md
    ```

    Generated filenames must not exceed 255 characters.

    The VCM identifier uses:

    ```text
    YYYY.MM.DDvNN
    ```

    ## Export

    The Author may:

    - download the project Markdown file,
    - download or copy the article,
    - download or copy the Hero Visual,
    - or export an optional ZIP package.

    ## Source Durability

    URLs are preserved as provenance but are not treated as durable
    memory.

    The project should preserve:

    - citation metadata,
    - source summary,
    - key claims,
    - statistics used,
    - Author reaction,
    - editorial role,
    - verification information,
    - and limited necessary excerpts.

    ## Paywalled Material

    When an Author supplies paywalled material, the project should
    preserve the editorial substance required for resumption without
    automatically retaining the complete source.

    ## Resume

    Resume Existing Project becomes a first-class opening experience.

    ## Privacy

    The Author decides where project files and generated outputs are
    stored.

    The Studio does not require custody of the Author's work.

    ## Alternatives Considered

    ### Hosted Author Library

    Deferred because it introduces significant infrastructure,
    security, privacy, and commercial scope.

    ### Local Database

    Deferred because a database creates unnecessary coupling and is
    less portable than an Author-owned project file.

    ### File-Path Tracking

    Rejected because storage paths:

    - burden the Author,
    - become stale,
    - reveal unnecessary information,
    - and are not required for project resumption.

    ### Save Only the Finished Article

    Rejected because the finished article does not preserve enough
    editorial context to support high-quality resumption.

    ## Consequences

    ### Positive

    - Author ownership
    - Privacy by default
    - Low storage burden
    - Human readability
    - Easy backup
    - Easy transfer
    - No required account system
    - No required hosted database
    - No path-management burden
    - Lower operating cost
    - Reduced compliance scope

    ### Costs and Risks

    - The Author may lose the file
    - Separately downloaded assets may be unavailable later
    - Search across many projects is not initially provided
    - Schema migration must be supported
    - Project files must be validated before resumption
    - Some expired sources may require reverification

    ## Future Options

    A future optional index may catalog Portable Editorial Projects
    without replacing Author ownership.

    Hosted synchronization requires a new explicit architecture,
    security, privacy, and commercial decision.
    """
)


# ---------------------------------------------------------------------
# PRD v1.2
# ---------------------------------------------------------------------

PRD_V12 = clean(
    """
    # Product Requirements Document - Version 1.2

    ## Product

    Ramrattan AI Editorial Studio

    ## Status

    Active Capability 5 product baseline.

    ## Supersedes

    PRD v1.1 as the active product definition.

    Earlier PRDs remain preserved as historical product records.

    ## North Star

    > Ramrattan AI Editorial Studio is an adaptive editorial operating
    > system that helps Authors transform evolving ideas, evidence,
    > expertise, and perspective into publication-ready professional
    > articles.

    > The Studio adapts to the Author's creative process - never the
    > other way around.

    ## Primary Product Outcome

    The Studio produces a publication-ready article package containing:

    - Hero Visual - 720 × 425
    - Headline
    - Publication-ready article
    - Source attribution
    - Practical takeaway
    - Call to action
    - Hashtags
    - LinkedIn description
    - Publication metadata
    - Portable Editorial Project

    ## Time-to-Value

    When sufficient starting material exists, the Studio should aim to
    produce the first publication-ready package within approximately
    10 minutes.

    The Author experience must not become laborious or questionnaire
    driven.

    ## Adaptive Editorial Context

    The Adaptive Editorial Context is the system kernel.

    It must:

    - exist before the first draft,
    - support first-pass generation,
    - support focused revision,
    - preserve version history,
    - support changes of direction,
    - assess readiness,
    - track Editorial Integrity,
    - preserve durable source context,
    - and serialize into a Portable Editorial Project.

    ## Natural Author Input

    The Author may begin or continue with:

    - URLs,
    - pasted material,
    - paywalled excerpts,
    - headlines,
    - observations,
    - news recollections,
    - perspectives,
    - notes,
    - drafts,
    - corrections,
    - publication links,
    - or compatible Portable Editorial Projects.

    The Author is not required to classify the contribution.

    ## Progressive Clarification

    The Studio should infer before asking.

    It should ask one focused question only when ambiguity materially
    blocks:

    - accuracy,
    - distinctiveness,
    - ethical publication,
    - or the Author's intended direction.

    ## Portable Editorial Projects

    The Studio is stateless by default.

    The Author may export a small, human-readable project file that
    preserves enough context to resume the work later.

    The Author chooses where the project is stored.

    The Product must not require or depend on the storage path.

    ## Resume Existing Project

    Resume Existing Project is a first-class opening action.

    The Studio must:

    - validate the project file,
    - identify the project and version,
    - restore compatible context,
    - explain missing optional assets,
    - summarize the last known state,
    - identify unresolved integrity issues,
    - and continue without unnecessary re-entry.

    ## File Naming and VCM

    Project files use:

    ```text
    Ramrattan-Editorial-Project_<Article-Slug>_YYYY.MM.DDvNN.md
    ```

    The VCM identifier uses:

    ```text
    YYYY.MM.DDvNN
    ```

    Requirements:

    - maximum filename length of 255 characters,
    - no silent overwrite,
    - daily sequencing from `v01`,
    - preserved version suffix,
    - readable slug,
    - and collision protection when truncation is required.

    ## Download and Copy Options

    The Product should support appropriate combinations of:

    - Download Portable Editorial Project
    - Download Article
    - Copy Article
    - Download Hero Visual
    - Copy Hero Visual
    - Export ZIP

    The Studio should explain the future value of saving the Portable
    Editorial Project.

    ## Durable Source Context

    The Project must remain understandable when a source URL:

    - expires,
    - moves,
    - changes,
    - becomes inaccessible,
    - or becomes paywalled.

    It should preserve:

    - citation metadata,
    - concise source summary,
    - key claims,
    - statistics used,
    - Author interpretation,
    - editorial role,
    - verification status,
    - and limited essential excerpts.

    ## Paywalled Material

    When an Author supplies copied material from a paywalled source,
    the Studio should preserve enough editorial context to resume the
    project later.

    It should not automatically retain the complete source.

    It should clearly record:

    - that the complete source was not retained,
    - that future access may be limited,
    - and that reverification may be needed.

    ## Publication URLs

    LinkedIn, Facebook, or other public URLs may be stored as optional
    metadata.

    They are not required for resumption.

    The Project must remain useful when the URL was never supplied or
    later becomes unavailable.

    ## Reuse

    A resumed project may support:

    - article revision,
    - Hero Visual revision,
    - publication-link updates,
    - follow-up articles,
    - project duplication,
    - evidence review,
    - or continuation of unfinished work.

    Reuse must not silently carry unsupported or outdated claims into
    new work.

    ## Editorial Integrity

    Editorial Integrity is a first-class component.

    The Studio must assess:

    - harmful intent,
    - source quality,
    - attribution,
    - evidence support,
    - uncertainty,
    - originality,
    - privacy,
    - professional conduct,
    - and publication blockers.

    ## Source Quality

    Disreputable or weak sources must not silently become the factual
    foundation of an article.

    The Studio should explain source-quality concerns and help the
    Author find stronger support where appropriate.

    ## Harmful Requests

    The Studio should not assist with article projects intended to:

    - cause harm,
    - facilitate illegality,
    - deceive,
    - harass,
    - defame through unsupported allegations,
    - reveal private information improperly,
    - impersonate,
    - defraud,
    - or deliberately spread false information.

    ## Author Ownership

    The Author owns:

    - the project,
    - the ideas,
    - the article,
    - the Hero Visual,
    - the project file,
    - and the publication decision.

    ## Non-Goals

    The current product does not require:

    - hosted Author storage,
    - user accounts,
    - cloud synchronization,
    - reported file paths,
    - collaboration workspaces,
    - a multi-tenant database,
    - carousel generation,
    - or automatic direct publishing.

    ## Success Measures

    - Time to first publication-ready package
    - Author confidence to publish
    - Low-friction interaction
    - Perspective preservation
    - Evidence quality
    - Originality
    - Editorial Integrity
    - Successful focused revision
    - Successful project export
    - Successful project resumption
    - Resilience to expired URLs
    - Responsible handling of paywalled excerpts
    - Author-controlled storage
    """
)


# ---------------------------------------------------------------------
# Resilient architecture tests
# ---------------------------------------------------------------------

CAPABILITY_TEST = clean(
    '''
    """Tests for the Capability 5 architecture baseline."""

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


    class Capability005ArchitectureTests(unittest.TestCase):
        def test_editorial_context_model_exists(self) -> None:
            path = (
                ROOT
                / "docs"
                / "architecture"
                / "Editorial_Context_Model.md"
            )

            self.assertTrue(path.is_file())

        def test_context_is_the_working_memory(self) -> None:
            content = normalized(
                "docs/architecture/"
                "Editorial_Context_Model.md"
            )

            self.assertIn("working memory", content)
            self.assertIn(
                "before the first article draft",
                content,
            )
            self.assertIn(
                "dependency intelligence",
                content.lower(),
            )

        def test_product_does_not_require_paths(self) -> None:
            content = normalized(
                "docs/architecture/"
                "Portable_Editorial_Project.md"
            )

            self.assertIn(
                "The Product does not require:",
                content,
            )
            self.assertIn(
                "must not burden the Author "
                "with reporting file paths",
                content,
            )

        def test_portable_project_is_author_owned(self) -> None:
            content = normalized(
                "docs/architecture/"
                "Portable_Editorial_Project.md"
            )

            self.assertIn(
                "The Studio's memory belongs to the Author",
                content,
            )
            self.assertIn(
                "stateless by default",
                content,
            )
            self.assertIn(
                "Resume an Existing Editorial Project",
                content,
            )

        def test_vcm_filename_standard_is_defined(self) -> None:
            content = normalized(
                "docs/architecture/"
                "Portable_Editorial_Project.md"
            )

            self.assertIn("YYYY.MM.DDvNN", content)
            self.assertIn(
                "Ramrattan-Editorial-Project_",
                content,
            )
            self.assertIn(
                "must never exceed 255 characters",
                content,
            )

        def test_expired_urls_are_supported(self) -> None:
            content = normalized(
                "docs/architecture/"
                "Portable_Editorial_Project.md"
            )

            self.assertIn(
                "URLs may expire or change",
                content,
            )
            self.assertIn(
                "concise durable summary",
                content,
            )
            self.assertIn(
                "remain understandable when a URL",
                content,
            )

        def test_paywalled_material_is_handled(self) -> None:
            content = normalized(
                "docs/architecture/"
                "Portable_Editorial_Project.md"
            )

            self.assertIn(
                "Authors may paste material "
                "from a paywalled source",
                content,
            )
            self.assertIn(
                "should not automatically place "
                "the complete paywalled article",
                content,
            )
            self.assertIn(
                "reverification may be needed",
                content,
            )

        def test_publication_urls_are_optional(self) -> None:
            content = normalized(
                "docs/architecture/"
                "Portable_Editorial_Project.md"
            )

            self.assertIn(
                "Publication URLs are optional",
                content,
            )
            self.assertIn(
                "must remain useful when a URL",
                content,
            )

        def test_editorial_integrity_is_first_class(self) -> None:
            content = normalized(
                "docs/architecture/"
                "Editorial_Integrity_Charter.md"
            )

            self.assertIn(
                "Editorial Integrity is a product capability",
                content,
            )
            self.assertIn(
                "harmful intent",
                content.lower(),
            )
            self.assertIn(
                "source reputation",
                content.lower(),
            )
            self.assertIn(
                "originality",
                content.lower(),
            )

        def test_definition_of_done_requires_demo(self) -> None:
            content = normalized(
                "docs/architecture/"
                "Definition_of_Done.md"
            )

            self.assertIn(
                "Every completed capability must include "
                "a demo document",
                content,
            )
            self.assertIn(
                "What did we learn",
                content,
            )

        def test_capability_demo_exists(self) -> None:
            path = (
                ROOT
                / "docs"
                / "demos"
                / "Capability-005-"
                "Adaptive-Editorial-Context.md"
            )

            self.assertTrue(path.is_file())

        def test_prd_v12_is_active(self) -> None:
            content = normalized(
                "docs/product/PRD_v1.2.md"
            )

            self.assertIn(
                "Active Capability 5 product baseline",
                content,
            )
            self.assertIn(
                "Portable Editorial Project",
                content,
            )
            self.assertIn(
                "maximum filename length of 255 characters",
                content,
            )
            self.assertIn(
                "must not require or depend on "
                "the storage path",
                content,
            )

        def test_article_first_scope_remains(self) -> None:
            content = normalized(
                "docs/product/PRD_v1.2.md"
            )

            self.assertIn(
                "publication-ready article package",
                content,
            )
            self.assertIn(
                "Hero Visual - 720 × 425",
                content,
            )
            self.assertIn(
                "carousel generation",
                content,
            )


    if __name__ == "__main__":
        unittest.main()
    '''
)


# ---------------------------------------------------------------------
# Managed updates to existing product documents
# ---------------------------------------------------------------------

CURRENT_FOCUS_BLOCK = clean(
    """
    ## Capability 5 - Current Architecture Direction

    The Adaptive Editorial Context is the system kernel.

    The Studio continuously interprets Author contributions and updates
    a shared representation of:

    - intent,
    - sources,
    - durable source context,
    - evidence,
    - Author perspective,
    - thesis,
    - article state,
    - Hero Visual state,
    - integrity,
    - readiness,
    - and revision history.

    The Studio is stateless by default.

    Project continuity is provided through Portable Editorial Projects
    owned and stored by the Author.

    The Product does not request or rely on storage paths.

    Each project may be exported as a small Markdown file using:

    ```text
    Ramrattan-Editorial-Project_<Article-Slug>_YYYY.MM.DDvNN.md
    ```

    Generated filenames must not exceed 255 characters.

    The opening experience supports:

    - Start a New Editorial Project
    - Resume an Existing Editorial Project

    The Author may download or copy:

    - the article,
    - the Hero Visual,
    - the Portable Editorial Project,
    - or an optional ZIP package.

    The project preserves enough source context to remain useful when
    URLs expire or paywalled material becomes inaccessible.

    Editorial Integrity is a first-class component.
    """
)


PRODUCT_PRINCIPLES_BLOCK = clean(
    """
    ## Capability 5 Principles

    ### The Studio's Memory Belongs to the Author

    Every completed project should be portable, resumable,
    human-readable, and remain under the Author's control.

    ### Stateless by Default

    The Studio should not require hosted storage to preserve project
    continuity.

    ### Preserve Editorial Meaning, Not Storage Paths

    The Studio should preserve editorial intent, source context,
    evidence, and decisions.

    It should not depend on knowing where the Author saved downloaded
    files.

    ### Preserve Source Value, Not Merely URLs

    A source's key claims, evidence, metadata, and editorial role should
    remain understandable when its URL later expires or changes.

    ### Handle Paywalled Material Responsibly

    Preserve the editorial context required for future work without
    automatically storing the complete paywalled source.

    ### Explain the Value of Saving

    The Studio should help the Author understand that the Portable
    Editorial Project preserves context needed for future interactions.

    ### Resume Without Repetition

    A resumed project should restore useful context without forcing the
    Author to reconstruct earlier decisions.

    ### Reuse Responsibly

    Reuse should reduce effort without silently carrying outdated,
    weak, or unsupported claims into new work.

    ### Integrity Before Publication

    Source quality, attribution, originality, privacy, safety, and
    evidence support must be considered before publication readiness.

    ### Capability Completion Requires Demonstration

    A capability is not complete until its Author value and behaviour
    have been demonstrated and documented.
    """
)


STUDIO_CONTRACT_BLOCK = clean(
    """
    ## Portable Project Commitment

    The Studio will:

    - offer an Author-controlled project export,
    - explain why the project file matters,
    - preserve enough context for future resumption,
    - validate a resumed project before using it,
    - preserve readable version information,
    - preserve durable source context,
    - and avoid silently overwriting earlier versions.

    The Studio will not:

    - require hosted storage,
    - request a file-storage path unnecessarily,
    - depend on Dropbox, OneDrive, Google Drive, or local paths,
    - claim ownership of project files,
    - or imply that a missing optional asset destroys the project
      context.

    ## Source Continuity Commitment

    The Studio will:

    - retain useful citation metadata,
    - preserve concise source summaries,
    - record key claims and statistics used,
    - preserve the Author's interpretation,
    - and identify future reverification limitations.

    It will not automatically archive complete paywalled publications.

    ## Editorial Integrity Commitment

    The Studio will not knowingly assist with content intended to:

    - cause harm,
    - facilitate illegal activity,
    - deceive,
    - harass,
    - defraud,
    - impersonate,
    - reveal private information improperly,
    - or spread false information deliberately.

    It will explain source-quality concerns and help the Author develop
    a stronger, safer, or more defensible foundation where appropriate.
    """
)


GLOSSARY_BLOCK = clean(
    """
    ## Portable Editorial Project

    A small, human-readable, Author-owned project file containing enough
    Adaptive Editorial Context to resume work later.

    ## VCM

    The version control method using:

    ```text
    YYYY.MM.DDvNN
    ```

    The daily sequence begins at `v01`.

    ## Project ID

    A permanent machine-readable identifier that remains stable even
    when the project title or filename changes.

    ## Resume Existing Project

    The opening action that validates and restores a compatible
    Portable Editorial Project.

    ## Stateless by Default

    The architectural principle that the Studio does not require hosted
    custody of Author project files.

    ## Durable Source Context

    The source metadata, concise summary, key claims, statistics,
    Author interpretation, verification notes, and editorial role
    preserved so a project remains understandable when a URL expires or
    changes.

    ## Author-Supplied Excerpt

    Material copied or pasted by the Author, including material from a
    source that may be paywalled or unavailable later.

    ## Reverification

    A future review required when a source can no longer be accessed,
    may have changed, or cannot be independently confirmed.

    ## Editorial Contribution

    Any Author input that may alter or enrich the Adaptive Editorial
    Context.

    ## Editorial Event

    The interpreted meaning of a contribution, such as adding evidence,
    revising perspective, changing the thesis, approving an asset, or
    recording publication.

    ## Editorial Integrity

    The collection of source-quality, evidence, attribution,
    originality, privacy, safety, professional-conduct, and publication
    readiness checks associated with a project.

    ## Capability Demo

    The document that explains what a completed capability changed,
    demonstrates Author value, records acceptance criteria, and captures
    learning.
    """
)


DECISION_LOG_BLOCK = clean(
    """
    ## Capability 5 Decisions

    | Date | Level | Decision | Rationale |
    |---|---:|---|---|
    | 2026-08-01 | D5 | Make the Adaptive Editorial Context the system kernel | Every capability requires one shared and revisable representation of the Author's evolving work. |
    | 2026-08-01 | D4 | Adopt Portable Editorial Projects | Small Author-owned files provide continuity without hosted-storage complexity. |
    | 2026-08-01 | D4 | Make the Studio stateless by default | The Author retains custody while the product avoids unnecessary account, storage, privacy, and tenancy scope. |
    | 2026-08-01 | D3 | Do not require external file paths | Storage location is the Author's concern and is not required for project resumption. |
    | 2026-08-01 | D3 | Add Start New and Resume Existing as opening actions | Resumption must be a first-class experience rather than an afterthought. |
    | 2026-08-01 | D3 | Adopt VCM format YYYY.MM.DDvNN | The established method gives human-readable daily version management. |
    | 2026-08-01 | D3 | Limit generated filenames to 255 characters | The safer legacy-compatible maximum protects portability. |
    | 2026-08-01 | D3 | Preserve durable source context | URLs may expire, move, or change and cannot be the only retained source information. |
    | 2026-08-01 | D3 | Preserve paywalled excerpts selectively | The project should retain editorial value without automatically archiving complete paywalled works. |
    | 2026-08-01 | D3 | Explain the future value of the project file to the Author | The Author must understand that saving context reduces future repetition. |
    | 2026-08-01 | D4 | Make Editorial Integrity a first-class context component | Responsible publication requires more than generic platform safety. |
    | 2026-08-01 | D2 | Require a Capability Demo in the Definition of Done | Product progress must be demonstrable to stakeholders and future contributors. |

    ## Capability 5 Learning

    A hosted Author Library is not required to provide high-value
    continuity.

    The Product also does not need to know where the Author saves
    downloaded files.

    A few kilobytes of well-structured, Author-owned context can
    preserve enough knowledge to resume an article project.

    The durable value of a source is its evidence, metadata,
    interpretation, and editorial significance, not merely its URL.
    """
)


ROADMAP_BLOCK = clean(
    """
    ## Capability Roadmap - Current Baseline

    ### Completed Foundations

    - [x] Capability 1 - Repository Foundation
    - [x] Capability 2 - Editorial Workflow Prototype
    - [x] Capability 3 - Adaptive Product Foundation
    - [x] Capability 4 - Article-First Alignment

    ### In Progress

    - [ ] Capability 5 - Adaptive Editorial Context
      - [x] Architecture baseline
      - [x] Portable Editorial Project specification
      - [x] No-path-dependency principle
      - [x] Durable source context
      - [x] Expired URL resilience
      - [x] Paywalled excerpt handling
      - [x] Editorial Integrity Charter
      - [x] Capability Definition of Done
      - [x] Capability Demo baseline
      - [ ] Python context model
      - [ ] Versioned components
      - [ ] VCM filename generation
      - [ ] Markdown serialization
      - [ ] Resume validation
      - [ ] Durable source records
      - [ ] Integrity state
      - [ ] Behavioural tests

    ### Next Capabilities

    - [ ] Capability 6 - Article Engine and Publication Package
    - [ ] Capability 7 - Intent and Revision Intelligence
    - [ ] Capability 8 - Evidence and Research
    - [ ] Capability 9 - Hero Visual System

    ### Optional Future Capabilities

    - [ ] Portable Project Index
    - [ ] Hosted project synchronization
    - [ ] Collaboration workspaces
    - [ ] Direct publication integrations
    - [ ] Additional publishing formats

    ### Deferred

    - [ ] Carousel generation
    - [ ] Hosted Author Library
    - [ ] Multi-tenant project storage
    - [ ] External file-path management
    """
)


CHANGELOG_BLOCK = clean(
    """
    ### Added - Capability 5 Architecture Baseline

    - Adaptive Editorial Context Model
    - Portable Editorial Project Specification
    - Editorial Integrity Charter
    - Capability Definition of Done
    - Capability 5 Demo
    - PRD v1.2
    - ADR-004 - Adopt Portable Editorial Projects
    - VCM project filename standard
    - 255-character filename maximum
    - Resume Existing Project experience
    - Download and copy output model
    - Durable source context
    - Expired URL resilience
    - Paywalled excerpt handling
    - Optional project ZIP concept
    - Capability architecture tests

    ### Changed - Capability 5 Architecture Baseline

    - Replaced the hosted Author Library direction with Author-owned
      Portable Editorial Projects
    - Established the Studio as stateless by default
    - Removed external file-path dependency
    - Made publication URLs optional metadata
    - Required preservation of source meaning beyond the URL
    - Defined selective retention for paywalled material
    - Made Editorial Integrity a first-class context component
    - Established Capability Demos as part of completion
    """
)


README_BLOCK = clean(
    """
    ## Capability 5 - Adaptive Editorial Context

    The Adaptive Editorial Context is the working memory of the Studio.

    It interprets natural Author contributions and preserves:

    - intent,
    - sources,
    - durable source context,
    - evidence,
    - perspective,
    - thesis,
    - article state,
    - Hero Visual state,
    - integrity,
    - readiness,
    - and meaningful revision history.

    The Author does not need to select a workflow mode.

    ## Portable Editorial Projects

    The Studio is stateless by default.

    Authors can save a small project file containing the context needed
    to resume later.

    Project files use:

    ```text
    Ramrattan-Editorial-Project_<Article-Slug>_YYYY.MM.DDvNN.md
    ```

    Filenames never exceed 255 characters.

    Authors may:

    - download or copy the article,
    - download or copy the Hero Visual,
    - download the Portable Editorial Project,
    - or export an optional ZIP.

    The Author chooses where files are stored.

    The Product does not request or depend on storage paths.

    ## Durable Source Context

    URLs may expire, change, or become inaccessible.

    The project preserves:

    - citation metadata,
    - concise source summaries,
    - key claims,
    - statistics used,
    - Author interpretation,
    - verification notes,
    - and editorial significance.

    Paywalled material is preserved selectively.

    The complete source is not automatically archived.

    ## Resume Existing Project

    A future opening experience will support:

    - Start a New Editorial Project
    - Resume an Existing Editorial Project

    Resume validates and restores the saved context without requiring
    the Author to reconstruct previous work.

    ## Editorial Integrity

    The Studio evaluates:

    - source quality,
    - evidence support,
    - attribution,
    - uncertainty,
    - originality,
    - privacy,
    - safety,
    - professional conduct,
    - and publication blockers.
    """
)


# ---------------------------------------------------------------------
# Managed marker definitions and deterministic new files
# ---------------------------------------------------------------------

MARKER_BLOCKS = {
    "README.md": (
        "CAPABILITY_005_README",
        README_BLOCK,
    ),
    "docs/product/Current_Product_Focus.md": (
        "CAPABILITY_005_CURRENT_FOCUS",
        CURRENT_FOCUS_BLOCK,
    ),
    "docs/product/Product_Principles.md": (
        "CAPABILITY_005_PRODUCT_PRINCIPLES",
        PRODUCT_PRINCIPLES_BLOCK,
    ),
    "docs/product/Studio_Contract.md": (
        "CAPABILITY_005_STUDIO_CONTRACT",
        STUDIO_CONTRACT_BLOCK,
    ),
    "docs/product/Glossary.md": (
        "CAPABILITY_005_GLOSSARY",
        GLOSSARY_BLOCK,
    ),
    "docs/product/Decision_Log.md": (
        "CAPABILITY_005_DECISION_LOG",
        DECISION_LOG_BLOCK,
    ),
    "ROADMAP.md": (
        "CAPABILITY_005_ROADMAP",
        ROADMAP_BLOCK,
    ),
    "CHANGELOG.md": (
        "CAPABILITY_005_CHANGELOG",
        CHANGELOG_BLOCK,
    ),
}


NEW_FILES = {
    (
        "docs/architecture/"
        "Editorial_Context_Model.md"
    ): EDITORIAL_CONTEXT_MODEL,

    (
        "docs/architecture/"
        "Portable_Editorial_Project.md"
    ): PORTABLE_EDITORIAL_PROJECT,

    (
        "docs/architecture/"
        "Editorial_Integrity_Charter.md"
    ): EDITORIAL_INTEGRITY_CHARTER,

    (
        "docs/architecture/"
        "Definition_of_Done.md"
    ): DEFINITION_OF_DONE,

    (
        "docs/architecture/adr/"
        "ADR-004-adopt-portable-editorial-projects.md"
    ): ADR_004,

    (
        "docs/product/"
        "PRD_v1.2.md"
    ): PRD_V12,

    (
        "docs/demos/"
        "Capability-005-Adaptive-Editorial-Context.md"
    ): CAPABILITY_DEMO,

    (
        "tests/"
        "test_capability005_architecture.py"
    ): CAPABILITY_TEST,
}


# ---------------------------------------------------------------------
# Errors and command execution
# ---------------------------------------------------------------------

class ArchitectureLockError(RuntimeError):
    """
    Raised when the architecture baseline cannot proceed safely.
    """


def run(
    command: list[str],
    *,
    cwd: Path,
    capture: bool = False,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    """
    Run and display a command.
    """
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
    """
    Return stripped command output.
    """
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
    """
    Run a command and parse its JSON output.
    """
    raw = output(command, cwd=cwd)

    if not raw:
        return {}

    return json.loads(raw)


# ---------------------------------------------------------------------
# Repository verification
# ---------------------------------------------------------------------

def repository_root() -> Path:
    """
    Locate and verify the expected Git repository.
    """
    try:
        root = Path(
            output(
                [
                    "git",
                    "rev-parse",
                    "--show-toplevel",
                ],
                cwd=Path.cwd(),
            )
        ).resolve()

    except (
        FileNotFoundError,
        subprocess.CalledProcessError,
    ) as exc:
        raise ArchitectureLockError(
            "Run this script from inside the cloned repository."
        ) from exc

    if root.name != EXPECTED_REPOSITORY:
        raise ArchitectureLockError(
            f"Expected repository '{EXPECTED_REPOSITORY}', "
            f"found '{root.name}'."
        )

    remote = output(
        [
            "git",
            "remote",
            "get-url",
            "origin",
        ],
        cwd=root,
    )

    if EXPECTED_REMOTE_FRAGMENT not in remote:
        raise ArchitectureLockError(
            "The origin remote does not match the expected "
            "GitHub repository."
        )

    return root


def current_branch(root: Path) -> str:
    """
    Return the active Git branch.
    """
    return output(
        [
            "git",
            "branch",
            "--show-current",
        ],
        cwd=root,
    )


def verify_branch(root: Path) -> None:
    """
    Require the Capability 5 feature branch.
    """
    branch = current_branch(root)

    print(f"Branch: {branch}")

    if branch != EXPECTED_BRANCH:
        raise ArchitectureLockError(
            f"Expected branch '{EXPECTED_BRANCH}', "
            f"found '{branch}'."
        )


def verify_script_integrity() -> None:
    """
    Fail safely when the pasted script is incomplete.
    """
    script_path = Path(__file__).resolve()

    content = script_path.read_text(
        encoding="utf-8"
    )

    if SCRIPT_SENTINEL not in content:
        raise ArchitectureLockError(
            "The script appears incomplete or truncated. "
            "The final sentinel is missing."
        )

    try:
        compile(
            content,
            str(script_path),
            "exec",
        )
    except SyntaxError as exc:
        raise ArchitectureLockError(
            "The pasted script is not syntactically complete: "
            f"{exc}"
        ) from exc

    print("Script integrity check passed.")


def working_tree_lines(root: Path) -> list[str]:
    """
    Return non-empty porcelain Git status lines.
    """
    status = output(
        [
            "git",
            "status",
            "--porcelain",
        ],
        cwd=root,
    )

    return [
        line
        for line in status.splitlines()
        if line.strip()
    ]


def verify_expected_working_tree(root: Path) -> None:
    """
    Permit only the known untracked Capability 5 scripts before the
    architecture baseline is generated.
    """
    lines = working_tree_lines(root)

    unexpected: list[str] = []

    for line in lines:
        if not line.startswith("?? "):
            unexpected.append(line)
            continue

        relative = line[3:]

        if relative not in EXPECTED_UNTRACKED_FILES:
            unexpected.append(line)

    if unexpected:
        raise ArchitectureLockError(
            "Unexpected working-tree changes exist:\n"
            + "\n".join(unexpected)
            + "\n\nOnly the known untracked Capability 5 scripts "
            "are allowed before the architecture baseline is applied."
        )

    if lines:
        print(
            "Working tree contains only the expected "
            "untracked Capability 5 scripts."
        )
    else:
        print("Working tree is clean.")


# ---------------------------------------------------------------------
# Managed file operations
# ---------------------------------------------------------------------

def managed_block(
    marker_name: str,
    content: str,
) -> str:
    """
    Construct one managed Markdown block.
    """
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
    """
    Insert or replace one managed Markdown block.

    Existing unrelated content is preserved.
    """
    if not path.is_file():
        raise ArchitectureLockError(
            f"Missing required document: {path}"
        )

    original = path.read_text(
        encoding="utf-8"
    )

    start = f"<!-- {marker_name}_START -->"
    end = f"<!-- {marker_name}_END -->"

    block = managed_block(
        marker_name,
        content,
    )

    start_present = start in original
    end_present = end in original

    if start_present and end_present:
        before = original.split(
            start,
            1,
        )[0].rstrip()

        after = original.split(
            end,
            1,
        )[1].lstrip()

        updated = (
            before
            + "\n\n"
            + block
        )

        if after:
            updated += "\n\n" + after

        updated = updated.rstrip() + "\n"

    elif start_present or end_present:
        raise ArchitectureLockError(
            f"Incomplete managed marker pair in {path}."
        )

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
    """
    Write deterministic Capability 5 architecture files.
    """
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
    """
    Update existing product documents with marker-managed blocks.
    """
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
    """
    Apply the complete local architecture baseline.
    """
    write_new_files(root)
    update_existing_documents(root)

    print()
    print(
        "Capability 5 architecture files "
        "have been written."
    )


# ---------------------------------------------------------------------
# Local validation
# ---------------------------------------------------------------------

REQUIRED_LOCAL_FILES = (
    (
        "docs/architecture/"
        "Editorial_Context_Model.md"
    ),
    (
        "docs/architecture/"
        "Portable_Editorial_Project.md"
    ),
    (
        "docs/architecture/"
        "Editorial_Integrity_Charter.md"
    ),
    (
        "docs/architecture/"
        "Definition_of_Done.md"
    ),
    (
        "docs/architecture/adr/"
        "ADR-004-adopt-portable-editorial-projects.md"
    ),
    "docs/product/PRD_v1.2.md",
    (
        "docs/demos/"
        "Capability-005-Adaptive-Editorial-Context.md"
    ),
    "tests/test_capability005_architecture.py",
)


def validate_required_files(root: Path) -> None:
    """
    Confirm all Capability 5 architecture files exist.
    """
    missing = [
        relative
        for relative in REQUIRED_LOCAL_FILES
        if not (root / relative).is_file()
    ]

    if missing:
        raise ArchitectureLockError(
            "Missing Capability 5 files:\n"
            + "\n".join(
                f"  - {relative}"
                for relative in missing
            )
        )

    print(
        "All required Capability 5 "
        "architecture files are present."
    )


def validate_product_language(root: Path) -> None:
    """
    Validate the most important architecture decisions.
    """
    checks: dict[str, tuple[str, ...]] = {
        (
            "docs/architecture/"
            "Editorial_Context_Model.md"
        ): (
            "working memory",
            "before the first article draft",
            "Durable Source Context",
            "Paywalled and Author-Supplied Material",
            "Product does not depend on external file paths",
        ),

        (
            "docs/architecture/"
            "Portable_Editorial_Project.md"
        ): (
            "The Studio's memory belongs to the Author",
            "must not burden the Author with reporting file paths",
            "YYYY.MM.DDvNN",
            "must never exceed 255 characters",
            "URLs may expire or change",
            "Authors may paste material from a paywalled source",
            "Publication URLs are optional",
        ),

        (
            "docs/architecture/"
            "Editorial_Integrity_Charter.md"
        ): (
            "Editorial Integrity is a product capability",
            "Harmful Intent",
            "Source Reputation",
            "Paywalled and Author-Supplied Excerpts",
            "Constructive Refusal",
        ),

        (
            "docs/architecture/"
            "Definition_of_Done.md"
        ): (
            "Every completed capability must include "
            "a demo document",
            "no unnecessary file-path collection",
            "What did we learn",
        ),

        "docs/product/PRD_v1.2.md": (
            "Active Capability 5 product baseline",
            "Adaptive Editorial Context is the system kernel",
            "must not require or depend on the storage path",
            "maximum filename length of 255 characters",
            "Durable Source Context",
            "Paywalled Material",
        ),
    }

    for relative, phrases in checks.items():
        path = root / relative

        normalized = normalize_markdown(
            path.read_text(
                encoding="utf-8"
            )
        )

        for phrase in phrases:
            if phrase not in normalized:
                raise ArchitectureLockError(
                    f"Expected phrase '{phrase}' "
                    f"in {relative}."
                )

    print(
        "Capability 5 product-language "
        "validation passed."
    )


def run_repository_validation(root: Path) -> None:
    """
    Run compilation, unit tests, and repository validation.
    """
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
        "Capability 5 repository validation passed."
    )


def show_local_status(root: Path) -> None:
    """
    Display current uncommitted local changes.
    """
    print("\nGit status:")

    run(
        [
            "git",
            "status",
            "--short",
        ],
        cwd=root,
    )

    print("\nTracked change summary:")

    run(
        [
            "git",
            "diff",
            "--stat",
        ],
        cwd=root,
    )


# ---------------------------------------------------------------------
# Preview
# ---------------------------------------------------------------------

def preview(root: Path) -> None:
    """
    Display the intended change without modifying files.
    """
    print()
    print(
        "Capability 5 architecture "
        "lockdown preview:"
    )
    print()

    print("New files:")

    for relative in NEW_FILES:
        print(f"  - {relative}")

    print("\nManaged updates:")

    for relative in MARKER_BLOCKS:
        print(f"  - {relative}")

    print("\nDecisions being locked:")

    decisions = (
        "Adaptive Editorial Context becomes the system kernel",
        "Portable Editorial Projects replace hosted storage",
        "The Studio is stateless by default",
        "The Author owns and stores project memory",
        "The Product does not require file paths",
        "Article and Hero Visual outputs may be copied or downloaded",
        "Start New and Resume Existing become opening actions",
        "VCM uses YYYY.MM.DDvNN",
        "Generated filenames never exceed 255 characters",
        "URLs are provenance, not durable memory",
        "Durable source context survives expired URLs",
        "Paywalled material is preserved selectively",
        "Publication URLs remain optional",
        "Editorial Integrity becomes first-class",
        "Capability Demos become part of completion",
    )

    for decision in decisions:
        print(f"  - {decision}")

    print("\nThis preview changes nothing.")

    print("\nApply with:")

    print(
        "  python3 scripts/"
        "bootstrap_capability005_architecture_lock.py "
        "--apply"
    )


# ---------------------------------------------------------------------
# GitHub Project synchronization
# ---------------------------------------------------------------------

PROJECT_DESCRIPTION = (
    "Capability roadmap for an adaptive editorial operating system "
    "focused on publication-ready professional articles, "
    "720 × 425 Hero Visuals, durable source context, and "
    "Author-owned portable projects."
)


PROJECT_README = """# Ramrattan AI Editorial Studio

Ramrattan AI Editorial Studio is an adaptive editorial operating
system for publication-ready professional articles and their
720 × 425 Hero Visuals.

## Current capability

Capability 5 - Adaptive Editorial Context

## Capability sequence

1. Repository Foundation - complete
2. Editorial Workflow Prototype - complete
3. Adaptive Product Foundation - complete
4. Article-First Alignment - complete
5. Adaptive Editorial Context - in progress
6. Article Engine and Publication Package - next
7. Intent and Revision Intelligence
8. Evidence and Research
9. Hero Visual System

## Portable Editorial Projects

The Studio is stateless by default.

Authors own and store their project context in portable Markdown files
using the VCM standard:

`YYYY.MM.DDvNN`

Generated filenames do not exceed 255 characters.

The Product does not request or depend on storage paths.

## Durable source context

The project preserves source meaning beyond the URL so work can remain
understandable when URLs expire or paywalled material becomes
unavailable.

## Product principle

The Studio adapts to the Author's creative process - never the other
way around.
"""


ISSUE_RENAMES = {
    4: (
        "Capability 5 - Build the "
        "Adaptive Editorial Context"
    ),
    5: (
        "Future - Optional Portable "
        "Project Index"
    ),
    6: (
        "Capability 7 - Add Intent "
        "and Revision Intelligence"
    ),
    7: (
        "Capability 8 - Build the "
        "Evidence and Research Engine"
    ),
    8: (
        "Capability 9 - Build the "
        "720 × 425 Hero Visual System"
    ),
    9: (
        "Future - Hosted Project "
        "Synchronization"
    ),
}


def validate_project_identity(root: Path) -> None:
    """
    Confirm that Project #1 is the expected GitHub Project.
    """
    project = json_output(
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

    if project.get("id") != PROJECT_ID:
        raise ArchitectureLockError(
            "GitHub Project #1 does not match "
            "the expected project ID."
        )


def project_items(root: Path) -> list[dict[str, Any]]:
    """
    Return the current GitHub Project items.
    """
    payload = json_output(
        [
            "gh",
            "project",
            "item-list",
            str(PROJECT_NUMBER),
            "--owner",
            OWNER,
            "--limit",
            "200",
            "--format",
            "json",
        ],
        cwd=root,
    )

    return payload.get("items", [])


def project_item_for_issue(
    root: Path,
    issue_number: int,
) -> str | None:
    """
    Return a Project item ID for one repository issue.
    """
    for item in project_items(root):
        content = item.get("content") or {}

        if (
            content.get("type") == "Issue"
            and content.get("number") == issue_number
        ):
            return item.get("id")

    return None


def set_project_status(
    root: Path,
    item_id: str,
    status: str,
) -> None:
    """
    Set a Project item's Status value.
    """
    option_id = STATUS_OPTIONS[status]

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
            option_id,
        ],
        cwd=root,
    )


def sync_project(root: Path) -> None:
    """
    Align GitHub issues and Project #1 with Capability 5.
    """
    validate_required_files(root)
    validate_product_language(root)
    run_repository_validation(root)

    run(
        [
            "gh",
            "auth",
            "status",
        ],
        cwd=root,
    )

    validate_project_identity(root)

    for issue_number, title in ISSUE_RENAMES.items():
        run(
            [
                "gh",
                "issue",
                "edit",
                str(issue_number),
                "--repo",
                REPO_SLUG,
                "--title",
                title,
            ],
            cwd=root,
        )

        print(
            f"Renamed issue #{issue_number}: {title}"
        )

    item_id = project_item_for_issue(
        root,
        4,
    )

    if item_id:
        set_project_status(
            root,
            item_id,
            "In Progress",
        )

        print(
            "Capability 5 issue marked In Progress."
        )
    else:
        print(
            "Capability 5 issue was not found "
            "on Project #1."
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
        "GitHub Project planning synchronized."
    )


# ---------------------------------------------------------------------
# Argument parsing and main
# ---------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    """
    Parse command-line options.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Lock the Capability 5 "
            "architecture baseline."
        )
    )

    mode = parser.add_mutually_exclusive_group()

    mode.add_argument(
        "--apply",
        action="store_true",
        help=(
            "Write and validate the local "
            "Capability 5 architecture baseline."
        ),
    )

    mode.add_argument(
        "--sync-project",
        action="store_true",
        help=(
            "Synchronize GitHub planning after "
            "the local architecture baseline validates."
        ),
    )

    return parser.parse_args()


def main() -> int:
    """
    Preview, apply, or synchronize Capability 5.
    """
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
            show_local_status(root)

            print()
            print(
                "Capability 5 architecture baseline "
                "has been applied and validated."
            )

            print(
                "Nothing has been committed, pushed, "
                "or changed on GitHub."
            )

        else:
            verify_expected_working_tree(root)
            preview(root)

        return 0

    except ArchitectureLockError as exc:
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


# CAPABILITY_005_ARCHITECTURE_LOCK_COMPLETE
# END OF SCRIPT - CAPABILITY 5 ARCHITECTURE LOCK


if __name__ == "__main__":
    raise SystemExit(main())