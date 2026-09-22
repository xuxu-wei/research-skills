"""Export the maintained OpenAI skills as a plain, portable skills directory.

Uses only the standard library. Does not install plugins or change source files.
Run from any directory; --output is relative to the caller's working directory.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import tempfile


REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = REPO_ROOT / "research-skills-openai" / "skills"
DEFAULT_OUTPUT = REPO_ROOT / "dist" / "skills-flatten"
CACHE_DIRECTORIES = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}


class ExportError(ValueError):
    """The requested export cannot be performed without losing or escaping files."""


def _is_link(path: Path) -> bool:
    # Resolve detects directory junctions on Python 3.11 as well as newer Python.
    return path.is_symlink() or path.resolve() != path.absolute()


def _collect_files(directory: Path, skill_root: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(directory.iterdir()):
        if path.name in CACHE_DIRECTORIES or path.name == "tests":
            continue
        if directory == skill_root and path.name == "agents":
            continue
        if path.suffix in {".pyc", ".pyo"} or (path.name.startswith("test_") and path.suffix == ".py"):
            continue
        if _is_link(path):
            raise ExportError(f"Linked resources are not supported: {path}")
        if path.is_dir():
            files.extend(_collect_files(path, skill_root))
        elif path.is_file():
            files.append(path)
        else:
            raise ExportError(f"Not a regular file or directory: {path}")
    return files


def _check_output(output: Path) -> None:
    if output.exists() and (not output.is_dir() or next(output.iterdir(), None) is not None):
        raise ExportError(f"Output must be absent or an empty directory: {output}")


def export_skills(source_root: Path, output_dir: Path) -> list[str]:
    """Copy discovered skills and resources, returning their directory names.

    Build in a sibling temporary directory and publish only after all copies
    succeed. Existing nonempty output is never replaced, including on a repeat
    invocation. Skill instructions and retained resources are copied unchanged.
    """
    source = source_root.expanduser().resolve()
    output = output_dir.expanduser().resolve()
    if not source.is_dir():
        raise ExportError(f"Skill source directory does not exist: {source}")
    if source == output or source in output.parents or output in source.parents:
        raise ExportError("Source and output directories must not overlap.")
    _check_output(output)

    names: list[str] = []
    files: list[tuple[Path, Path]] = []
    seen_names: set[str] = set()
    for skill in sorted(source.iterdir()):
        if skill.name in CACHE_DIRECTORIES or skill.name in {"agents", "tests"}:
            continue
        if not skill.is_dir() or not (skill / "SKILL.md").is_file():
            continue
        if _is_link(skill):
            raise ExportError(f"Linked skill directories are not supported: {skill}")
        if skill.name.casefold() in seen_names:
            raise ExportError(f"Skill directory names collide ignoring case: {skill.name}")
        seen_names.add(skill.name.casefold())
        names.append(skill.name)
        files.extend((path, path.relative_to(source)) for path in _collect_files(skill, skill))
    if not names:
        raise ExportError(f"No skill directories containing SKILL.md were found: {source}")

    output.parent.mkdir(parents=True, exist_ok=True)
    existed = output.exists()
    staging = Path(tempfile.mkdtemp(prefix=f".{output.name}-", dir=output.parent))
    try:
        for source_file, relative in files:
            target = staging / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_file, target)
        # Recheck after copying in case another process populated the output.
        _check_output(output)
        if output.exists():
            output.rmdir()  # Empty only; never recursively remove user output.
        try:
            staging.rename(output)
        except OSError:
            if existed and not output.exists():
                output.mkdir()
            raise
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    return names


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT,
                        help="new or empty output directory (default: repository dist/skills-flatten)")
    args = parser.parse_args()
    try:
        names = export_skills(SOURCE_ROOT, args.output)
    except (ExportError, OSError) as exc:
        parser.exit(1, f"Export failed: {exc}\n")
    print(f"Exported {len(names)} skills to {args.output.expanduser().resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
