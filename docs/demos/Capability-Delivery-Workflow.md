# Capability Delivery Workflow Demo

## Objective

Demonstrate that the repository can determine the next safe
capability-delivery action without repeating previously solved
mistakes.

## Scenario 1 - Clean Develop

State:

- branch is `develop`,
- working tree is clean,
- local and remote develop match.

Expected recommendation:

- create or resume the requested feature branch.

## Scenario 2 - Existing Feature Branch

The requested branch already exists.

Expected recommendation:

- switch to the existing branch;
- do not attempt to recreate it.

## Scenario 3 - Partial Bootstrap Application

Expected capability files already exist after validation failure.

Expected behaviour:

- permit declared capability changes;
- reject unrelated changes;
- rerun deterministically.

## Scenario 4 - Pull Request Exists

An open pull request already targets `develop`.

Expected recommendation:

- reuse the existing pull request;
- resolve its number automatically.

## Scenario 5 - CI Pending

Expected recommendation:

- run the resolved `gh pr checks` command;
- do not merge.

## Scenario 6 - CI Passed

Expected recommendation:

- provide the exact merge command using the resolved PR number.

## Scenario 7 - Merge Complete

Expected verification:

- branch is `develop`,
- working tree is clean,
- feature branch is absent locally,
- local and remote develop match,
- latest merge is present.

## Scenario 8 - Terminal Output Re-entered

Push output is accidentally pasted into the shell.

Expected interpretation:

- shell errors are harmless if the push already succeeded;
- verify branch tracking rather than repeating commands blindly.

## Completion

The workflow is complete when:

- documentation exists,
- helper state detection works,
- exact commands are produced,
- tests pass,
- and later capability delivery can use the process directly.
