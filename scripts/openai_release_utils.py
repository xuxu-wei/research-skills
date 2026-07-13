#!/usr/bin/env python3
"""Shared release-contract helpers for the OpenAI research plugin."""

from __future__ import annotations

import re
from pathlib import Path


STRICT_SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"
)

MARKETPLACE_PATH = ".agents/plugins/marketplace.json"
PLUGIN_ROOT_PREFIX = "research-skills-openai/"
NON_INSTALLABLE_DOCUMENTATION_PATHS = {
    "research-skills-openai/AGENTS.md",
    "research-skills-openai/PHASE7-8-RUNBOOK.md",
    "research-skills-openai/README.md",
    "research-skills-openai/ROADMAP.md",
}
NON_INSTALLABLE_DOCUMENTATION_PREFIXES = (
    "research-skills-openai/docs/",
    "research-skills-openai/reports/",
)


def parse_semver(value: str) -> tuple[tuple[int, int, int], tuple[int | str, ...] | None] | None:
    """Parse strict SemVer without build metadata."""
    match = STRICT_SEMVER_RE.fullmatch(value)
    if not match:
        return None
    prerelease: tuple[int | str, ...] | None = None
    if match.group(4) is not None:
        identifiers: list[int | str] = []
        for identifier in match.group(4).split("."):
            if identifier.isdigit():
                if len(identifier) > 1 and identifier.startswith("0"):
                    return None
                identifiers.append(int(identifier))
            else:
                identifiers.append(identifier)
        prerelease = tuple(identifiers)
    return (int(match.group(1)), int(match.group(2)), int(match.group(3))), prerelease


def compare_semver(left: str, right: str) -> int:
    """Return -1, 0, or 1 using SemVer precedence."""
    parsed_left = parse_semver(left)
    parsed_right = parse_semver(right)
    if parsed_left is None or parsed_right is None:
        raise ValueError("invalid strict SemVer without build metadata")
    left_core, left_pre = parsed_left
    right_core, right_pre = parsed_right
    if left_core != right_core:
        return -1 if left_core < right_core else 1
    if left_pre is None or right_pre is None:
        if left_pre is right_pre:
            return 0
        return 1 if left_pre is None else -1
    for left_item, right_item in zip(left_pre, right_pre):
        if left_item == right_item:
            continue
        if isinstance(left_item, int) and isinstance(right_item, str):
            return -1
        if isinstance(left_item, str) and isinstance(right_item, int):
            return 1
        return -1 if left_item < right_item else 1
    if len(left_pre) == len(right_pre):
        return 0
    return -1 if len(left_pre) < len(right_pre) else 1


def is_installable_behavior_path(path: str) -> bool:
    normalized = Path(path).as_posix()
    if normalized == MARKETPLACE_PATH:
        return True
    if not normalized.startswith(PLUGIN_ROOT_PREFIX):
        return False
    if normalized in NON_INSTALLABLE_DOCUMENTATION_PATHS:
        return False
    if normalized.startswith(NON_INSTALLABLE_DOCUMENTATION_PREFIXES):
        return False
    # Default to installable for the plugin package. This covers the complete
    # .codex-plugin subtree and future apps, hooks, MCP, assets, or other files
    # that may affect discovery, installation, or runtime behavior.
    return True


def validate_version_transition(old_version: str, new_version: str, changed_paths: list[str]) -> list[str]:
    """Validate release ordering and required bumps for installable changes."""
    errors: list[str] = []
    if parse_semver(old_version) is None:
        errors.append(f"base manifest version is not strict SemVer: {old_version}")
        return errors
    if parse_semver(new_version) is None:
        errors.append(f"plugin version is not strict SemVer without build metadata: {new_version}")
        return errors
    ordering = compare_semver(new_version, old_version)
    if ordering < 0:
        errors.append(f"plugin version decreased: {old_version} -> {new_version}")
    behavior_changed = any(is_installable_behavior_path(path) for path in changed_paths)
    if behavior_changed and ordering <= 0:
        errors.append(
            "installable behavior changed without a strictly increasing plugin version: "
            f"{old_version} -> {new_version}"
        )
    return errors
