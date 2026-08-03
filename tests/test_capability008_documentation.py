"""Documentation tests for Capability 008."""

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


class Capability008DocumentationTests(unittest.TestCase):
    def test_coherence_principle_exists(self) -> None:
        self.assertTrue(
            (
                ROOT
                / "docs"
                / "constitution"
                / "Editorial_Coherence_Principle.md"
            ).is_file()
        )

    def test_one_intent_per_session(self) -> None:
        content = normalized(
            "docs/constitution/"
            "Editorial_Coherence_Principle.md"
        )

        self.assertIn(
            "one coherent Editorial Intent",
            content,
        )

    def test_no_silent_scope_expansion(self) -> None:
        content = normalized(
            "docs/constitution/"
            "Editorial_Coherence_Principle.md"
        )

        self.assertIn(
            "No Silent Scope Expansion",
            content,
        )

    def test_never_events_exist(self) -> None:
        content = normalized(
            "docs/constitution/Editorial_Never_Events.md"
        )

        self.assertIn(
            "Silently alter approved work",
            content,
        )
        self.assertIn(
            "Merge unrelated Editorial Intents",
            content,
        )

    def test_cancel_and_abort_are_distinct(self) -> None:
        content = normalized(
            "docs/constitution/"
            "Editorial_Session_Lifecycle.md"
        )

        self.assertIn(
            "Cancelled means",
            content,
        )
        self.assertIn(
            "Aborted means",
            content,
        )

    def test_adr_009_exists(self) -> None:
        self.assertTrue(
            (
                ROOT
                / "docs"
                / "architecture"
                / "adr"
                / (
                    "ADR-009-adopt-editorial-discernment-"
                    "and-intent-preservation.md"
                )
            ).is_file()
        )

    def test_baseline_v05_exists(self) -> None:
        self.assertTrue(
            (
                ROOT
                / "docs"
                / "architecture"
                / "baselines"
                / "Architecture_Baseline_2026.08.01v05.md"
            ).is_file()
        )

    def test_internal_and_external_names(self) -> None:
        content = normalized(
            "docs/architecture/"
            "Editorial_Discernment_Runtime.md"
        )

        self.assertIn(
            "Editorial Discernment Engine",
            content,
        )
        self.assertIn(
            "Editorial Guidance",
            content,
        )


if __name__ == "__main__":
    unittest.main()
