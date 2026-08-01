# Release Checklist

## Preparation

- [ ] Version selected
- [ ] Release scope agreed
- [ ] Acceptance criteria met
- [ ] Changelog updated
- [ ] Documentation updated
- [ ] ADRs accepted where required
- [ ] Known limitations documented

## Validation

- [ ] `python3 studio.py validate` passes
- [ ] Prompt files reviewed
- [ ] Examples reviewed
- [ ] Regression tests pass
- [ ] No secrets or private data are present

## Git

- [ ] Feature branches merged into `develop`
- [ ] Release candidate reviewed
- [ ] `develop` merged into `main`
- [ ] Version tag created
- [ ] Release notes published

## Post-Release

- [ ] Repository release verified
- [ ] Roadmap updated
- [ ] Follow-up issues created
- [ ] Rollback target confirmed
