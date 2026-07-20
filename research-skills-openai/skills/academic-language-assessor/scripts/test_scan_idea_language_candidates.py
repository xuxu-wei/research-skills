#!/usr/bin/env python3
"""Unit tests for the deterministic Idea language-candidate scanner."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True

from scan_idea_language_candidates import (  # noqa: E402
    GROUP_COMPACT_LABEL,
    GROUP_READER_ENTRY,
    GROUP_TOKEN,
    scan_candidates,
)


FIXTURE = """---
schema_version: research-idea.v3
version_id: v099
---

# Repeated-measures response study v003
## Title, summary, audience, and positioning
- **Title:** Repeated-measures response study v003
- **One-sentence complete-Idea summary:** 本研究估计 response_state，并以均方根误差（RMSE）描述拟合误差。
## Structured abstract
- **Background and gap:** Existing studies do not cover the full process.
- **Objective and hypothesis:** 主要比较量称为“局部评分”，其计算在方法部分定义。
## Background, current state, gap, significance, and rationale
This ordinary background line is not an entry candidate.
## Research question, objectives, and core hypothesis
### Primary research question
Can the model describe change over time?
### Objectives
This objective is outside the selected subsection.
### Core hypothesis and non-hypotheses
The bounded comparison reports QX with its definition in the same sentence.
## Research design and methods
The review_state token appears in ordinary prose.
该局部比较简称为“组内差值”，并在本句直接定义。
```text
hidden_pipeline v777 is not reader facing
```
"""


class IdeaLanguageCandidateScannerTests(unittest.TestCase):
    def test_groups_only_structurally_marked_candidates(self) -> None:
        candidates = scan_candidates(FIXTURE.splitlines(keepends=True))

        reader_lines = [candidate.line_number for candidate in candidates[GROUP_READER_ENTRY]]
        token_map = {
            candidate.token: candidate.line_numbers for candidate in candidates[GROUP_TOKEN]
        }
        compact_labels = {
            candidate.token: candidate.line_numbers
            for candidate in candidates[GROUP_COMPACT_LABEL]
        }

        self.assertEqual(reader_lines, sorted(set(reader_lines)))
        self.assertIn(6, reader_lines)   # H1 title
        self.assertIn(8, reader_lines)   # section-1 title field
        self.assertIn(12, reader_lines)  # structured-abstract objective
        self.assertIn(17, reader_lines)  # primary-question prose
        self.assertIn(21, reader_lines)  # core-hypothesis prose
        self.assertNotIn(19, reader_lines)
        self.assertEqual(token_map["response_state"], (9,))
        self.assertEqual(token_map["review_state"], (23,))
        self.assertEqual(token_map["v003"], (6, 8))
        self.assertEqual(compact_labels["RMSE"], (9,))
        self.assertEqual(compact_labels["局部评分"], (12,))
        self.assertEqual(compact_labels["QX"], (21,))
        self.assertEqual(compact_labels["组内差值"], (24,))
        self.assertNotIn("v099", token_map)  # YAML frontmatter is excluded
        self.assertNotIn("hidden_pipeline", token_map)  # fenced code is excluded

    def test_cli_is_read_only_and_output_is_grouped(self) -> None:
        script = Path(__file__).with_name("scan_idea_language_candidates.py")
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            dossier = temp_path / "idea.md"
            dossier.write_text(FIXTURE, encoding="utf-8")
            before_files = sorted(path.relative_to(temp_path) for path in temp_path.rglob("*"))
            before_content = dossier.read_bytes()

            result = subprocess.run(
                [sys.executable, str(script), str(dossier)],
                cwd=temp_path,
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

            after_files = sorted(path.relative_to(temp_path) for path in temp_path.rglob("*"))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(before_files, after_files)
            self.assertEqual(dossier.read_bytes(), before_content)
            self.assertIn("[reader-entry]\n6\t# Repeated-measures response study v003", result.stdout)
            self.assertIn("[compact-reader-label]", result.stdout)
            self.assertIn("[mixed-language-version-internal-token]", result.stdout)
            self.assertNotIn("[consequence-statements]", result.stdout)
            self.assertIn("v003\t6,8", result.stdout)
            self.assertNotIn("hidden_pipeline", result.stdout)
            self.assertNotIn("verdict", result.stdout.casefold())


if __name__ == "__main__":
    unittest.main()
