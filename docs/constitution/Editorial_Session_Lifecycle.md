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
