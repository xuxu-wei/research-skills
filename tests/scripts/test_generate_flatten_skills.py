"""Test the exporter with synthetic files, never the maintained Skill content."""

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from scripts.auxiliary import generate_flatten_skills as exporter


class ExportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.source = self.root / "source"
        self.source.mkdir()
        self.output = self.root / "output"

    def write(self, relative, content=b"fixture"):
        path = self.source / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return path

    def skill(self, name="sample"):
        return self.write(f"{name}/SKILL.md", f"---\nname: {name}\ndescription: Fixture\n---\n".encode())

    def test_copies_resources_and_unicode_without_changing_sources(self):
        self.skill()
        self.write("sample/references/证据.md", "引用与说明\n".encode("utf-8"))
        self.write("sample/assets/图.bin", bytes(range(256)))
        self.write("sample/scripts/helper.py", b"print('fixture')\n")
        self.write("sample/templates/example.md", b"Example\n")
        before = {p.relative_to(self.source): p.read_bytes() for p in self.source.rglob("*") if p.is_file()}
        self.assertEqual(exporter.export_skills(self.source, self.output), ["sample"])
        after = {p.relative_to(self.source): p.read_bytes() for p in self.source.rglob("*") if p.is_file()}
        copied = {p.relative_to(self.output): p.read_bytes() for p in self.output.rglob("*") if p.is_file()}
        self.assertEqual(before, after)
        self.assertEqual(before, copied)

    def test_discovers_multiple_skills_and_ignores_non_skills(self):
        self.skill("zeta")
        self.skill("alpha")
        self.write("notes/README.md")
        self.assertEqual(exporter.export_skills(self.source, self.output), ["alpha", "zeta"])
        self.assertEqual(sorted(p.name for p in self.output.iterdir()), ["alpha", "zeta"])

    def test_excludes_platform_metadata_caches_and_tests(self):
        self.skill()
        for relative in ["sample/agents/openai.yaml", "sample/__pycache__/a.pyc",
                         "sample/scripts/__pycache__/b.pyc", "sample/scripts/test_helper.py",
                         "sample/tests/fixture.txt", "sample/.git/config", "sample/.pytest_cache/cache"]:
            self.write(relative)
        self.write("sample/assets/agents/example.txt")
        exporter.export_skills(self.source, self.output)
        self.assertEqual(sorted(p.relative_to(self.output).as_posix() for p in self.output.rglob("*") if p.is_file()),
                         ["sample/SKILL.md", "sample/assets/agents/example.txt"])

    def test_missing_or_empty_source_does_not_create_output(self):
        for source in [self.source, self.root / "missing"]:
            with self.subTest(source=source), self.assertRaises(exporter.ExportError):
                exporter.export_skills(source, self.output)
            self.assertFalse(self.output.exists())

    def test_rejects_source_output_overlap(self):
        original = self.skill().read_bytes()
        for output in [self.source, self.root, self.source / "nested"]:
            with self.subTest(output=output), self.assertRaises(exporter.ExportError):
                exporter.export_skills(self.source, output)
            self.assertEqual((self.source / "sample/SKILL.md").read_bytes(), original)

    def test_preserves_nonempty_directory_and_existing_file(self):
        self.skill()
        self.output.mkdir()
        note = self.output / "user-notes.txt"
        note.write_bytes(b"keep")
        with self.assertRaises(exporter.ExportError):
            exporter.export_skills(self.source, self.output)
        self.assertEqual(note.read_bytes(), b"keep")
        existing_file = self.root / "existing.txt"
        existing_file.write_bytes(b"original")
        with self.assertRaises(exporter.ExportError):
            exporter.export_skills(self.source, existing_file)
        self.assertEqual(existing_file.read_bytes(), b"original")

    def test_accepts_empty_output_but_refuses_repeat_export(self):
        self.skill()
        self.output.mkdir()
        exporter.export_skills(self.source, self.output)
        before = (self.output / "sample/SKILL.md").read_bytes()
        with self.assertRaises(exporter.ExportError):
            exporter.export_skills(self.source, self.output)
        self.assertEqual((self.output / "sample/SKILL.md").read_bytes(), before)

    def test_copy_failure_leaves_no_partial_export(self):
        self.skill()
        self.write("sample/references/example.md")
        copy_file = shutil.copy2
        calls = 0

        def fail_second(source, target):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("simulated copy failure")
            return copy_file(source, target)

        for existing_empty in [False, True]:
            if existing_empty:
                self.output.mkdir()
            calls = 0
            with self.subTest(existing_empty=existing_empty), patch.object(exporter.shutil, "copy2", side_effect=fail_second):
                with self.assertRaises(OSError):
                    exporter.export_skills(self.source, self.output)
            self.assertEqual(self.output.exists(), existing_empty)
            if existing_empty:
                self.assertEqual(list(self.output.iterdir()), [])
            self.assertEqual(list(self.root.glob(".output-*")), [])
            self.assertTrue((self.source / "sample/references/example.md").exists())

    def test_output_populated_during_copy_is_preserved(self):
        self.skill()
        copy_file = shutil.copy2

        def concurrent_write(source, target):
            self.output.mkdir(exist_ok=True)
            (self.output / "user-notes.txt").write_bytes(b"keep")
            return copy_file(source, target)

        with patch.object(exporter.shutil, "copy2", side_effect=concurrent_write):
            with self.assertRaises(exporter.ExportError):
                exporter.export_skills(self.source, self.output)
        self.assertEqual((self.output / "user-notes.txt").read_bytes(), b"keep")
        self.assertEqual(list(self.root.glob(".output-*")), [])

    def test_linked_resource_is_rejected(self):
        self.skill()
        external = self.root / "external.txt"
        external.write_bytes(b"external")
        link = self.source / "sample/linked.txt"
        try:
            link.symlink_to(external)
        except (OSError, NotImplementedError):
            self.skipTest("This environment cannot create symbolic links.")
        with self.assertRaises(exporter.ExportError):
            exporter.export_skills(self.source, self.output)
        self.assertFalse(self.output.exists())
        self.assertEqual(external.read_bytes(), b"external")

    def cli_fixture(self, with_skill=True):
        repo = self.root / "repository"
        script = repo / "scripts/auxiliary/generate_flatten_skills.py"
        script.parent.mkdir(parents=True)
        shutil.copy2(exporter.__file__, script)
        if with_skill:
            skill = repo / "research-skills-openai/skills/sample/SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text("Fixture\n", encoding="utf-8")
        working_dir = self.root / "unrelated"
        working_dir.mkdir()
        return repo, script, working_dir

    def test_cli_default_is_independent_of_working_directory(self):
        repo, script, cwd = self.cli_fixture()
        result = subprocess.run([sys.executable, str(script)], cwd=cwd, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((repo / "dist/skills-flatten/sample/SKILL.md").is_file())
        self.assertFalse((cwd / "dist").exists())

    def test_cli_relative_output_is_relative_to_caller(self):
        repo, script, cwd = self.cli_fixture()
        result = subprocess.run([sys.executable, str(script), "--output", "portable"], cwd=cwd, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((cwd / "portable/sample/SKILL.md").is_file())
        self.assertFalse((repo / "dist").exists())

    def test_cli_error_has_nonzero_exit_and_no_output(self):
        repo, script, cwd = self.cli_fixture(with_skill=False)
        result = subprocess.run([sys.executable, str(script)], cwd=cwd, capture_output=True, text=True, encoding="utf-8")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Export failed", result.stderr)
        self.assertFalse((repo / "dist").exists())


if __name__ == "__main__":
    unittest.main()
