"""Generate, install, and register the Codex plugin variant.

Output:
  ./skills-openai-plugin/
  %USERPROFILE%/plugins/skills-openai-plugin

This script updates:
  %USERPROFILE%/.agents/plugins/marketplace.json
  %USERPROFILE%/.codex/config.toml

It also removes the older accidental `skills-flatten@local` Codex plugin entry,
because `skills-flatten` is now a plain portable skills directory, not a plugin.
"""

from __future__ import annotations

from pathlib import Path

from scripts.codex_plugin_converter import (
    LEGACY_FLATTEN_PLUGIN,
    build_codex,
    install_plugins,
    repo_root,
)


if __name__ == "__main__":
    import json

    root = repo_root()
    plugin_dir, _sources, report = build_codex(root)
    if report["ok"]:
        install_plugins(root, [plugin_dir.name], remove_plugin_names=[LEGACY_FLATTEN_PLUGIN])
    print(json.dumps({
        "ok": report["ok"],
        "output": str(plugin_dir),
        "validation_report": str(root / "codex-plugin-validation.json"),
        "installed": bool(report["ok"]),
        "local_plugin": str(Path.home() / "plugins" / plugin_dir.name),
        "marketplace": str(Path.home() / ".agents" / "plugins" / "marketplace.json"),
        "codex_config": str(Path.home() / ".codex" / "config.toml"),
        "removed_legacy_plugin_entries": [LEGACY_FLATTEN_PLUGIN] if report["ok"] else [],
        "skill_count": report["plugin"]["skill_count"],  # type: ignore[index]
    }, indent=2, ensure_ascii=False))
    raise SystemExit(0 if report["ok"] else 1)
