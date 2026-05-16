"""Backward-compatible wrapper for the Codex plugin installer.

Prefer the split entrypoints:

- `python generate_flatten_skills.py` only regenerates `./skills-flatten/`.
- `python install_codex_plugin.py` generates, installs, and registers the Codex plugin.
"""

from __future__ import annotations

import runpy


if __name__ == "__main__":
    runpy.run_path("install_codex_plugin.py", run_name="__main__")
