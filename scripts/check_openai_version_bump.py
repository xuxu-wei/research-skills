#!/usr/bin/env python3
"""Require an OpenAI plugin SemVer bump for installable behavior changes."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
MANIFEST = "research-skills-openai/.codex-plugin/plugin.json"
BEHAVIOR_PREFIXES = (
    "research-skills-openai/skills/",
    "research-skills-openai/workflow-registry.yaml",
)


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
        print("Version-bump check skipped: event has no usable base SHA")
        return 0
    try:
        changed = git("diff", "--name-only", base, "HEAD").splitlines()
        old_manifest = git("show", f"{base}:{MANIFEST}")
    except subprocess.CalledProcessError as exc:
        print(f"Version-bump check failed to inspect base {base}: {exc}")
        return 1

    behavior_changed = any(path.startswith(BEHAVIOR_PREFIXES) for path in changed)
    current_manifest = (REPO / MANIFEST).read_text(encoding="utf-8")
    old_version = manifest_version(old_manifest)
    new_version = manifest_version(current_manifest)
    if "+codex." in new_version:
        print("Installable manifest must not contain a local Codex cachebuster")
        return 1
    if behavior_changed and old_version == new_version:
        print(f"Installable behavior changed without a plugin version bump: {old_version}")
        return 1
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?", new_version):
        print(f"Plugin version is not release SemVer without build metadata: {new_version}")
        return 1
    print(f"Version-bump check passed: {old_version} -> {new_version}; behavior_changed={behavior_changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
