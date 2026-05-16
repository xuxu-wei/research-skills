"""Generate a plain flat skills directory for broad agent compatibility.

Output:
  ./skills-flatten/

Each direct child of `skills-flatten` is a skill directory containing `SKILL.md`.
This script does not install anything and does not register a Codex plugin.
"""

from __future__ import annotations

from pathlib import Path

from scripts.codex_plugin_converter import build_flatten, repo_root


if __name__ == "__main__":
    import json
    import sys

    root = repo_root()
    flatten_dir, _sources, report = build_flatten(root)
    print(json.dumps({
        "ok": report["ok"],
        "output": str(flatten_dir),
        "validation_report": str(root / "flatten-validation.json"),
        "skill_count": report["flatten"]["skill_count"],  # type: ignore[index]
    }, indent=2, ensure_ascii=False))
    raise SystemExit(0 if report["ok"] else 1)
