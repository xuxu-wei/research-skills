#!/usr/bin/env python3
"""Tests for the deterministic Idea dossier lint."""

from __future__ import annotations

import unittest

from lint_idea_dossier import REQUIRED_H2, lint_text, reader_language_advisories


def valid_dossier() -> str:
    sections: list[str] = []
    for number, title in enumerate(REQUIRED_H2, start=1):
        sections.append(f"## {title}")
        if number == 1:
            sections.extend(
                [
                    "- **Title:** A clear research title",
                    "- **One-sentence complete-Idea summary:** This study addresses a defined problem with a specified design and contribution.",
                ]
            )
        elif number == 3:
            for function in [
                "Background",
                "Current state",
                "Gap",
                "Significance",
                "Rationale",
            ]:
                sections.extend([f"### {function}", f"Substantive {function.lower()} content."])
        elif number == 14:
            sections.extend(
                [
                    "### Feasibility and resources",
                    "Resources are specified.",
                    "### Limitations and boundary conditions",
                    "A bounded limitation is stated once.",
                ]
            )
        else:
            sections.append(f"Substantive content for section {number}.")
    return "# A clear research title\n\n" + "\n\n".join(sections) + "\n"


def versioned_dossier(version: str, *, path_only_lineage: bool = False) -> str:
    if path_only_lineage:
        based_on = "  - inputs/source.md"
    else:
        based_on = "\n".join(
            [
                "  - artifact_id: source-v001",
                "    version: v001",
                "    path: inputs/source.md",
            ]
        )
    frontmatter = "\n".join(
        [
            "---",
            f"plugin_version: {version}",
            "artifact_id: idea-dossier-v002",
            "version_id: v002",
            "path: dossiers/idea-dossier-v002.md",
            "change_type: editorial_repair",
            "based_on:",
            based_on,
            "---",
            "",
        ]
    )
    return frontmatter + valid_dossier()


class IdeaDossierLintTests(unittest.TestCase):
    def test_valid_structure_passes(self) -> None:
        self.assertEqual(lint_text(valid_dossier()), [])

    def test_active_plugin_version_mismatch_fails(self) -> None:
        dossier = versioned_dossier("0.9.0-preview.1")
        self.assertTrue(
            any(
                "active plugin version" in error
                for error in lint_text(dossier, "0.9.0-preview.3")
            )
        )

    def test_active_plugin_version_match_passes(self) -> None:
        dossier = versioned_dossier("0.9.0-preview.3")
        self.assertEqual(lint_text(dossier, "0.9.0-preview.3"), [])

    def test_path_only_lineage_fails(self) -> None:
        dossier = versioned_dossier("0.9.0-preview.3", path_only_lineage=True)
        self.assertTrue(
            any("artifact_id, version, and path" in error for error in lint_text(dossier, "0.9.0-preview.3"))
        )

    def test_missing_significance_fails(self) -> None:
        text = valid_dossier().replace(
            "### Significance\n\nSubstantive significance content.\n\n", ""
        )
        self.assertTrue(any("Significance" in error for error in lint_text(text)))

    def test_deprecated_chain_limit_field_fails(self) -> None:
        text = valid_dossier().replace(
            "Substantive content for section 9.",
            "- **Limits and failure conditions:** repeated caveat",
        )
        self.assertTrue(any("deprecated limits" in error for error in lint_text(text)))

    def test_authority_heading_outside_section_14_fails(self) -> None:
        text = valid_dossier().replace(
            "Substantive content for section 7.",
            "### Limitations\nA repeated limitation.",
        )
        self.assertTrue(any("only inside section 14" in error for error in lint_text(text)))

    def test_limitation_pointer_outside_section_14_fails(self) -> None:
        text = valid_dossier().replace(
            "Substantive content for section 7.",
            "The design is described here; limitations are discussed in section 14.",
        )
        self.assertTrue(any("must not point" in error for error in lint_text(text)))

    def test_internal_implementation_vocabulary_is_advisory_not_universal_error(self) -> None:
        text = valid_dossier().replace(
            "Substantive content for section 8.",
            "The public prose names review_state, editorial-review-pending, and (QX).",
        )
        self.assertEqual(lint_text(text), [])
        advisories = reader_language_advisories(text)
        self.assertTrue(
            any(
                "review_state" in item
                and "editorial-review-pending" in item
                and "QX" in item
                for item in advisories
            )
        )

    def test_ordinary_scientific_words_do_not_trigger_the_advisory(self) -> None:
        text = valid_dossier().replace(
            "Substantive content for section 8.",
            "The candidate analysis uses projection and perturbation to update the estimate.",
        )
        self.assertEqual(reader_language_advisories(text), [])


if __name__ == "__main__":
    unittest.main()
