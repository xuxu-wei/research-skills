#!/usr/bin/env python3
"""Synchronize current-version deterministic fixtures with the plugin manifest.

Historical live receipts are intentionally excluded; their captured plugin
version and content digest must remain immutable evidence.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from openai_release_utils import parse_semver


REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "research-skills-openai"
CURRENT_FIXTURES = (
    REPO / "tests" / "openai_phase4" / "idea.yaml",
    REPO / "tests" / "openai_phase4" / "proposal.yaml",
    REPO / "tests" / "openai_phase4" / "article.yaml",
    REPO / "tests" / "openai_phase4" / "perspective.yaml",
    REPO / "tests" / "openai_phase4" / "research-polisher.yaml",
)
VERSION_LINE = re.compile(r"(?m)^(?P<indent>[ \t]*)plugin_version:[ \t]*[^\r\n#]+(?P<suffix>[ \t]*(?:#.*)?)$")


def main() -> int:
    manifest = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    version = str(manifest.get("version", ""))
    if parse_semver(version) is None:
        raise SystemExit(f"Manifest version is not strict release SemVer: {version}")
    replacements = 0
    for path in CURRENT_FIXTURES:
        text = path.read_text(encoding="utf-8")

        def replace(match: re.Match[str]) -> str:
            nonlocal replacements
            replacements += 1
            return f"{match.group('indent')}plugin_version: {version}{match.group('suffix')}"

        updated = VERSION_LINE.sub(replace, text)
        if updated == text and f"plugin_version: {version}" not in text:
            raise SystemExit(f"No plugin_version field found in {path}")
        path.write_text(updated, encoding="utf-8", newline="\n")
    print(f"Synchronized {replacements} current fixture version fields to {version}")
    print("Historical live receipt versions were not modified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
