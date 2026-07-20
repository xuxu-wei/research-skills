#!/usr/bin/env python3
"""Unit tests for reader-facing short-form regression diffs."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True

from diff_reader_facing_short_forms import diff_short_forms  # noqa: E402


SOURCE = """---
schema_version: research-idea.v3
internal_stage: QX
---

# 纵向响应研究
## Title, summary, audience, and positioning
- **Title:** 纵向响应研究
基准误差使用 RMSE 描述。
## Research design and methods
模型按预设规则评价。
```text
HIDDEN_LABEL
```
"""

REVISED = """---
schema_version: research-idea.v3
internal_stage: QX
---

# 纵向响应研究
## Title, summary, audience, and positioning
- **Title:** 纵向响应研究
基准误差仍使用 RMSE 描述，并新增 QX 比较。
## Research design and methods
该局部比较简称为“组内差值”，结果另记为 review_state。
```text
HIDDEN_LABEL
```
"""


class ReaderFacingShortFormDiffTests(unittest.TestCase):
    def test_reports_only_new_reader_facing_candidates(self) -> None:
        candidates = diff_short_forms(
            SOURCE.splitlines(keepends=True),
            REVISED.splitlines(keepends=True),
        )
        forms = {item.form for item in candidates}

        self.assertIn("QX", forms)
        self.assertIn("组内差值", forms)
        self.assertIn("review_state", forms)
        self.assertNotIn("RMSE", forms)
        self.assertNotIn("HIDDEN_LABEL", forms)

    def test_identical_text_has_empty_diff(self) -> None:
        self.assertEqual(
            diff_short_forms(
                SOURCE.splitlines(keepends=True),
                SOURCE.splitlines(keepends=True),
            ),
            [],
        )

    def test_reports_all_reader_facing_occurrences_after_detection(self) -> None:
        revised = REVISED.replace(
            "结果另记为 review_state。",
            "结果另记为 review_state。后文继续使用组内差值。",
        )
        candidates = diff_short_forms(
            SOURCE.splitlines(keepends=True),
            revised.splitlines(keepends=True),
        )
        candidate = next(item for item in candidates if item.form == "组内差值")
        self.assertEqual(candidate.line_numbers, (11,))

        revised_separate_line = revised.replace(
            "## Research design and methods\n",
            "## Research design and methods\n组内差值只作描述。\n",
        )
        candidates = diff_short_forms(
            SOURCE.splitlines(keepends=True),
            revised_separate_line.splitlines(keepends=True),
        )
        candidate = next(item for item in candidates if item.form == "组内差值")
        self.assertEqual(candidate.line_numbers, (11, 12))

    def test_cli_is_read_only_and_advisory_by_default(self) -> None:
        script = Path(__file__).with_name("diff_reader_facing_short_forms.py")
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source.md"
            revised = root / "revised.md"
            source.write_text(SOURCE, encoding="utf-8")
            revised.write_text(REVISED, encoding="utf-8")
            before_files = sorted(path.relative_to(root) for path in root.rglob("*"))
            before_content = {path.name: path.read_bytes() for path in (source, revised)}

            result = subprocess.run(
                [sys.executable, str(script), str(source), str(revised)],
                cwd=root,
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

            after_files = sorted(path.relative_to(root) for path in root.rglob("*"))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(before_files, after_files)
            self.assertEqual(before_content[source.name], source.read_bytes())
            self.assertEqual(before_content[revised.name], revised.read_bytes())
            self.assertIn("[new-reader-facing-short-form]", result.stdout)
            self.assertIn("\tQX\t", result.stdout)
            self.assertIn("\t组内差值\t", result.stdout)
            self.assertIn("\treview_state\t", result.stdout)
            self.assertNotIn("\tRMSE\t", result.stdout)

    def test_optional_developer_strict_switch_can_fail(self) -> None:
        script = Path(__file__).with_name("diff_reader_facing_short_forms.py")
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "source.md"
            revised = root / "revised.md"
            source.write_text(SOURCE, encoding="utf-8")
            revised.write_text(REVISED, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(script), str(source), str(revised), "--fail-on-new"],
                cwd=root,
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(result.returncode, 1, result.stderr)


if __name__ == "__main__":
    unittest.main()
