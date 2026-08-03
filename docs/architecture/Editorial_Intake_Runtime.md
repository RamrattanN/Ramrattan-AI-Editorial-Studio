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
