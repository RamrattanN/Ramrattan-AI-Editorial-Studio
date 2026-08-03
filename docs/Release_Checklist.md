# Release Checklist

## Preparation

- [x] Version selected - Version 1.0 RC1
- [x] Release scope agreed - Issue #18
- [ ] Acceptance criteria met
- [x] Changelog updated
- [x] Documentation updated
- [x] ADRs accepted where required
- [x] Known limitations documented in the Version 1 end-to-end demo

## Validation

- [x] `python3 studio.py validate` passes
- [ ] Prompt files reviewed
- [ ] Examples reviewed
- [x] Regression tests pass
- [ ] No secrets or private data are present

## Git

- [ ] Feature branches merged into `develop`
- [ ] Release candidate reviewed
- [ ] `develop` merged into `main`
- [ ] Version tag created
- [ ] Release notes published

## Post-Release

- [ ] Repository release verified
- [x] Roadmap updated
- [ ] Follow-up issues created
- [ ] Rollback target confirmed

## Evidence Boundary

Unchecked items require manual review, human sign-off, Git delivery, external
publication, tagging, or post-release evidence. This checklist does not infer
those outcomes from local automated tests.
