#!/usr/bin/env python3
"""Require an OpenAI plugin SemVer bump for installable behavior changes."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from openai_release_utils import is_installable_behavior_path, validate_version_transition


REPO = Path(__file__).resolve().parents[1]
MANIFEST = "research-skills-openai/.codex-plugin/plugin.json"
def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO, text=True, encoding="utf-8").strip()


def manifest_version(text: str) -> str:
    return str(json.loads(text)["version"])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True, help="Base commit SHA for the change set")
    args = parser.parse_args()
    base = args.base.strip()
    if not base or set(base) == {"0"}:
        try:
            base = git("rev-parse", "HEAD^")
            print(
                "Version-bump check: event supplied no usable base SHA; "
                f"using first parent {base}"
            )
        except subprocess.CalledProcessError:
            print("Version-bump check skipped: repository has no parent commit")
            return 0
    try:
        # Compare the base directly with the current working tree so this check
        # behaves the same before commit and in CI. Include untracked files as
        # they may add installable plugin behavior too.
        changed = sorted(
            set(git("diff", "--name-only", base).splitlines())
            | set(git("ls-files", "--others", "--exclude-standard").splitlines())
        )
        old_manifest = git("show", f"{base}:{MANIFEST}")
    except subprocess.CalledProcessError as exc:
        print(f"Version-bump check failed to inspect base {base}: {exc}")
        return 1

    behavior_changed = any(is_installable_behavior_path(path) for path in changed)
    current_manifest = (REPO / MANIFEST).read_text(encoding="utf-8")
    old_version = manifest_version(old_manifest)
    new_version = manifest_version(current_manifest)
    errors = validate_version_transition(old_version, new_version, changed)
    if errors:
        for error in errors:
            print(f"Version-bump check failed: {error}")
        return 1
    print(f"Version-bump check passed: {old_version} -> {new_version}; behavior_changed={behavior_changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
