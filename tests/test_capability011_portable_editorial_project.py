"""Behavioral tests for Capability 011 Portable Editorial Projects."""

from dataclasses import replace
from datetime import date
import hashlib
import io
import json
import unittest
import zipfile

from studio.editorial_discernment import EditorialIntent, EditorialSession, WorkspaceState
from studio.evidence_validation import EditorialConfidence, EditorialRisk
from studio.hero_visual import HeroVisualRequest, HeroVisualSystem
from studio.portable_editorial_project import (
    MAX_FILENAME_LENGTH,
    PortableProjectError,
    ProjectState,
    article_download,
    deserialize_project,
    from_publication_package,
    hero_visual_download,
    project_download,
    resume_project,
    safe_slug,
    serialize_project,
    versioned_filename,
    zip_export,
)
from studio.publication_package import (
    HeroVisualPackageState,
    PackageReadiness,
    PublicationPackage,
    PublicationPackageBuilder,
)


ARTICLE = "# Trust Before Convenience\n\nApproved article content.\n"
PROMPT = "A restrained editorial compass protecting evidence."


def package(*, visual=True):
    result = PublicationPackage(
        article_markdown=ARTICLE,
        hero_visual_prompt=PROMPT,
        headline="Trust Before Convenience",
        hook="Trust must be earned.",
        insights=("Verification protects the Author.",),
        practical_takeaway="Review evidence before publication.",
        cta="What will you verify next?",
        source_and_attribution=("Internal editorial standard.",),
        hashtags=("#EditorialIntegrity",),
        linkedin_description="A concise trust-first editorial note.",
        editorial_confidence=EditorialConfidence.READY,
        editorial_risk=EditorialRisk.LOW,
        readiness=PackageReadiness.READY_FOR_HERO_VISUAL,
        review_findings=(),
    )
    if not visual:
        return result
    hero = HeroVisualSystem().generate(
        HeroVisualRequest(prompt=PROMPT, visual_intent="Protect trust.")
    )
    return PublicationPackageBuilder().attach_hero_visual(result, hero)


def project(pkg=None, *, saved_on=date(2026, 8, 2)):
    return from_publication_package(
        pkg or package(), saved_on=saved_on, document_version="2026.08.02v01"
    )


def session():
    intent = EditorialIntent(
        primary_topic="Trust Before Convenience",
        editorial_objective="Explain evidence-led review.",
        intended_audience="Professional Authors",
        publication_goal="Publish a professional article.",
    )
    return EditorialSession(intent=intent, workspace_state=WorkspaceState.PAUSED)


class NamingTests(unittest.TestCase):
    def test_safe_slug_and_daily_sequence(self):
        self.assertEqual(safe_slug("  Trust & Evidence!  "), "Trust-Evidence")
        first, v1 = versioned_filename("Trust & Evidence", date(2026, 8, 2))
        second, v2 = versioned_filename(
            "Trust & Evidence", date(2026, 8, 2), existing_names=(first,)
        )
        self.assertEqual(v1, "2026.08.02v01")
        self.assertEqual(v2, "2026.08.02v02")
        self.assertNotEqual(first, second)

    def test_filename_is_bounded_and_collision_resistant(self):
        name, _ = versioned_filename("meaningful " * 100, date(2026, 8, 2))
        self.assertLessEqual(len(name), MAX_FILENAME_LENGTH)
        self.assertRegex(name, r"-[A-F0-9]{8}_2026\.08\.02v01\.md$")

    def test_daily_sequence_fails_closed_before_overwrite(self):
        names = tuple(
            f"Ramrattan-Editorial-Project_Title_2026.08.02v{number:02d}.md"
            for number in range(1, 100)
        )
        with self.assertRaisesRegex(PortableProjectError, "exhausted"):
            versioned_filename("Title", date(2026, 8, 2), existing_names=names)


class SerializationTests(unittest.TestCase):
    def test_round_trip_is_byte_stable(self):
        original = project()
        first = serialize_project(original)
        restored = deserialize_project(first)
        self.assertEqual(restored, original)
        self.assertEqual(serialize_project(restored), first)

    def test_malformed_project_fails_closed(self):
        with self.assertRaises(PortableProjectError) as context:
            deserialize_project("# not a project")
        self.assertIs(context.exception.state, ProjectState.MALFORMED)

    def test_unsupported_schema_and_legacy_fields_fail_closed(self):
        markdown = serialize_project(project())
        payload = json.loads(markdown.split("```portable-editorial-project-json\n", 1)[1].split("\n```", 1)[0])
        payload["schema_version"] = 2
        changed = markdown.replace(
            json.dumps(json.loads(markdown.split("```portable-editorial-project-json\n", 1)[1].split("\n```", 1)[0]), ensure_ascii=False, indent=2, sort_keys=True),
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True),
        )
        with self.assertRaises(PortableProjectError) as context:
            deserialize_project(changed)
        self.assertIs(context.exception.state, ProjectState.UNSUPPORTED)

        payload["schema_version"] = 1
        payload["adaptive_editorial_context"] = {"fabricated": True}
        legacy = markdown.replace(
            markdown.split("```portable-editorial-project-json\n", 1)[1].split("\n```", 1)[0],
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True),
        )
        with self.assertRaises(PortableProjectError) as context:
            deserialize_project(legacy)
        self.assertIs(context.exception.state, ProjectState.UNSUPPORTED)

    def test_invalid_identity_fails_closed(self):
        markdown = serialize_project(project()).replace("REP-", "BAD-")
        with self.assertRaises(PortableProjectError) as context:
            deserialize_project(markdown)
        self.assertIs(context.exception.state, ProjectState.INVALID)


class ResumeAndExportTests(unittest.TestCase):
    def test_resume_invokes_session_and_temporal_integrity_review(self):
        editorial_session = session()
        result = resume_project(
            serialize_project(project(saved_on=date(2026, 8, 1))),
            editorial_session,
            current_on=date(2026, 8, 2),
        )
        self.assertIs(result.state, ProjectState.STALE)
        self.assertTrue(result.temporal_integrity_review_required)
        self.assertIs(editorial_session.workspace_state, WorkspaceState.ACTIVE)
        self.assertIn("Temporal Integrity", editorial_session.preserved_events[-1])

    def test_unresolved_blockers_prevent_resume(self):
        blocked = replace(project(), integrity_blockers=("Unsupported claim.",))
        editorial_session = session()
        with self.assertRaises(PortableProjectError) as context:
            resume_project(serialize_project(blocked), editorial_session, current_on=date(2026, 8, 2))
        self.assertIs(context.exception.state, ProjectState.BLOCKED)
        self.assertIs(editorial_session.workspace_state, WorkspaceState.PAUSED)

    def test_article_and_visual_downloads_preserve_bytes(self):
        pkg = package()
        portable = project(pkg)
        self.assertEqual(article_download(portable).content, ARTICLE.encode())
        self.assertEqual(hero_visual_download(pkg, portable).content, pkg.rendered_hero_visual.artifact)

    def test_missing_visual_download_is_blocked(self):
        pkg = package(visual=False)
        with self.assertRaises(PortableProjectError) as context:
            hero_visual_download(pkg, project(pkg))
        self.assertIs(context.exception.state, ProjectState.BLOCKED)

    def test_project_download_collision_advances_version(self):
        portable = project()
        first = project_download(portable)
        second = project_download(portable, existing_names=(first.filename,))
        self.assertIn("v02.md", second.filename)
        restored = deserialize_project(second.content.decode())
        self.assertEqual(restored.previous_version, "2026.08.02v01")

    def test_zip_export_is_deterministic_and_complete(self):
        pkg = package()
        portable = project(pkg)
        first = zip_export(portable, pkg)
        second = zip_export(portable, pkg)
        self.assertEqual(first.content, second.content)
        self.assertEqual(hashlib.sha256(first.content).hexdigest(), hashlib.sha256(second.content).hexdigest())
        with zipfile.ZipFile(io.BytesIO(first.content)) as archive:
            names = archive.namelist()
            self.assertEqual(names, sorted(names))
            self.assertEqual(len(names), 3)

    def test_publication_package_attachment_is_narrow(self):
        pkg = package()
        portable = project(pkg)
        attached = PublicationPackageBuilder().attach_portable_editorial_project(pkg, portable)
        self.assertIs(attached.portable_editorial_project, portable)
        self.assertEqual(attached.article_markdown, pkg.article_markdown)
        self.assertIs(attached.rendered_hero_visual, pkg.rendered_hero_visual)
        self.assertNotIn("Portable Editorial Project - Capability 011", attached.deferred_components)


if __name__ == "__main__":
    unittest.main()
