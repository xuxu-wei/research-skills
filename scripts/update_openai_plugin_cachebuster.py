#!/usr/bin/env python3
"""Apply one Codex cachebuster suffix to the OpenAI preview plugin version."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "research-skills-openai"
MANIFEST = PLUGIN / ".codex-plugin" / "plugin.json"
REGISTRY = PLUGIN / "workflow-registry.yaml"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cachebuster", help="Override the default UTC local timestamp token.")
    args = parser.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    current = str(manifest["version"])
    base = current.split("+", 1)[0]
    token = args.cachebuster or dt.datetime.now(dt.timezone.utc).strftime("local-%Y%m%d-%H%M%S")
    version = f"{base}+codex.{token}"
    manifest["version"] = version
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    registry = REGISTRY.read_text(encoding="utf-8")
    registry, count = re.subn(
        r'(?m)^plugin_version:\s*"[^"]+"$',
        f'plugin_version: "{version}"',
        registry,
        count=1,
    )
    if count != 1:
        raise RuntimeError("workflow-registry.yaml is missing plugin_version")
    REGISTRY.write_text(registry, encoding="utf-8", newline="\n")
    print(version)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
