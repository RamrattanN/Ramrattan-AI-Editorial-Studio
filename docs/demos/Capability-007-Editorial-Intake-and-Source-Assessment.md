# Capability 007 Demo - Editorial Intake and Source Assessment

## Objective

Demonstrate the first executable portion of the Canonical Editorial
Session.

## Scenario 1 - Welcome

The Author opens the Editorial Workspace.

The Workspace explains:

- what may be supplied,
- what the Editor will do,
- the five visible stages,
- and that the Author remains in control.

## Scenario 2 - URL

Input:

```text
https://example.org/article
```

Expected:

- Input classified as URL
- Stage 1 complete
- Stage 2 complete
- Deeper verification required
- Stages 3 through 5 pending

## Scenario 3 - Pasted Text

Expected:

- Input classified as Pasted Text
- Provenance marked as incomplete
- Deeper verification required
- Author is not forced to choose an input type

## Scenario 4 - Audio

Input:

```text
interview.m4a
```

Expected:

- Input classified as Audio
- Host-platform limit note preserved
- Speaker, date, and context identified as requiring review

## Scenario 5 - Optional Logo

The Author supplies a logo.

Expected:

- Rights confirmation required
- Brand-neutral path remains available
- No storage path requested

## Scenario 6 - Optional Headshot

The Author supplies a headshot.

Expected:

- Rights confirmation required
- Recognisability must be preserved
- Asset remains optional

## Scenario 7 - Resume Without Asset

A Portable Editorial Project records previous logo use but does not
include the logo.

Expected response:

- Upload again
- Continue without it
- Create a brand-neutral Hero Visual

The project remains valid.

## Completion

Capability 007 is complete when:

- runtime tests pass,
- Stage 1 and Stage 2 are executable,
- the Editorial Workspace vocabulary is consistent,
- identity assets are optional and governed,
- and full evidence verification is not falsely claimed.
