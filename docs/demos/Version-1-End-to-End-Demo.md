# Version 1 End-to-End Demo

## Status

Automated RC1 evidence assembled for Issue #18. Release readiness is not
claimed until this increment is reviewed and delivered.

## Connected Author Journey

The integration test `tests/test_version_one_end_to_end.py` begins with real
Editorial Intake, establishes one Editorial Intent and Editorial Session,
completes the five canonical Editorial Integrity stages, validates evidence and
Editorial Risk, and generates an article through the default
provider-independent Article Engine.

The same journey builds the Publication Package, generates and validates the
deterministic 720 × 425 Hero Visual, creates and serializes the narrow RC1
Portable Editorial Project, resumes it through `EditorialSession.resume()`,
requires Temporal Integrity review, and requests a focused CTA revision while
protecting approved headline, hook, and Hero Visual components. Article, Hero
Visual, project Markdown, and deterministic ZIP outputs remain available.

## Issue #18 Acceptance Evidence

| Acceptance criterion | Evidence | Type |
|---|---|---|
| Start New and five visible stages | Intake result and canonical session stage transitions in the integration test | Automated |
| Editorial Intent preserved | Session intent and Article Engine intent identifier assertions | Automated |
| Evidence and attribution enforced | Real `validate_evidence` report, attributed sources, and existing negative attribution tests | Automated |
| High or Severe risk blocks publication | Unsupported material claim is rejected by the real Article Engine | Automated |
| Provider-independent article generation | Default deterministic Article Engine provider | Automated |
| Complete Publication Package | Required components and final completion state assertions | Automated |
| 720 × 425 Hero Visual | Real deterministic Hero Visual System validation | Automated |
| VCM project save and Resume Existing | Real serialization, project download, and `resume_project` | Automated |
| Temporal Integrity on resume | Stale saved date produces required review | Automated |
| Focused component revision | CTA-only decision protects approved components; only CTA changes | Automated |
| Export-first completion | Article, Hero Visual, project, and deterministic ZIP bytes asserted | Automated |
| Repository validation and capability demos | Full test suite, `studio.py validate`, and existing capability demos | Automated/repository evidence |

## Manual Review and Known Limitations

The repository does not manufacture evidence for human or external actions.
Manual prompt/example review, release-candidate approval, publication to an
external service, merge from `develop` to `main`, version tagging, release-note
publication, and post-release verification remain unchecked. No hosted
workspace, collaboration, orchestration, publishing automation, embedded-asset
project schema, external-provider availability claim, or Version 2 behavior is
introduced.
