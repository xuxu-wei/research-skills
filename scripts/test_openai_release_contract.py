#!/usr/bin/env python3
"""Deterministic negative tests for the OpenAI plugin release contract."""

from __future__ import annotations

from openai_release_utils import compare_semver, parse_semver, validate_version_transition


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def main() -> int:
    valid = (
        "1.1.9-rc.4",
        "1.2.0-rc.1",
        "1.0.0",
        "1.0.0-rc.1",
    )
    invalid = (
        "1.2",
        "v1.2.0",
        "1.2.0-rc.01",
        "1.2.0+codex.local",
        "1.2.0-rc.1+build",
    )
    for value in valid:
        require(parse_semver(value) is not None, f"valid SemVer rejected: {value}")
    for value in invalid:
        require(parse_semver(value) is None, f"invalid SemVer accepted: {value}")

    require(compare_semver("1.2.0-rc.1", "1.1.9-rc.4") > 0, "minor prerelease ordering")
    require(compare_semver("1.2.0", "1.2.0-rc.9") > 0, "release ordering")
    require(compare_semver("1.2.0-rc.10", "1.2.0-rc.2") > 0, "numeric prerelease ordering")

    behavior_path = ["research-skills-openai/skills/article-orchestrator/SKILL.md"]
    manifest_path = ["research-skills-openai/.codex-plugin/plugin.json"]
    extra_plugin_metadata_path = ["research-skills-openai/.codex-plugin/capabilities/runtime.yaml"]
    marketplace_path = [".agents/plugins/marketplace.json"]
    future_runtime_path = ["research-skills-openai/hooks/preflight.yaml"]
    docs_path = ["research-skills-openai/README.md"]
    runbook_path = ["research-skills-openai/PHASE7-8-RUNBOOK.md"]
    docs_tree_path = ["research-skills-openai/docs/development.md"]
    report_path = ["research-skills-openai/reports/validation.json"]
    require(not validate_version_transition("1.1.9-rc.4", "1.2.0-rc.1", behavior_path), "valid bump")
    require(validate_version_transition("1.1.9-rc.4", "1.1.9-rc.4", behavior_path), "missing bump")
    require(validate_version_transition("1.1.9-rc.4", "1.1.8-rc.9", behavior_path), "downgrade")
    require(validate_version_transition("1.1.9-rc.4", "broken", behavior_path), "malformed")
    require(validate_version_transition("1.1.9-rc.4", "1.1.9-rc.4", manifest_path), "manifest omission")
    require(
        validate_version_transition("1.1.9-rc.4", "1.1.9-rc.4", extra_plugin_metadata_path),
        "additional .codex-plugin file omission",
    )
    require(
        validate_version_transition("1.1.9-rc.4", "1.1.9-rc.4", marketplace_path),
        "marketplace omission",
    )
    require(
        validate_version_transition("1.1.9-rc.4", "1.1.9-rc.4", future_runtime_path),
        "future runtime surface omission",
    )
    require(not validate_version_transition("1.1.9-rc.4", "1.1.9-rc.4", docs_path), "docs-only stability")
    require(
        not validate_version_transition("1.1.9-rc.4", "1.1.9-rc.4", runbook_path),
        "runbook-only stability",
    )
    require(
        not validate_version_transition("1.1.9-rc.4", "1.1.9-rc.4", docs_tree_path),
        "docs-tree-only stability",
    )
    require(
        not validate_version_transition("1.1.9-rc.4", "1.1.9-rc.4", report_path),
        "report-only stability",
    )
    print("OpenAI release-contract tests passed")
    print(
        "negative cases: missing bump, downgrade, malformed, manifest omission, "
        "extra .codex-plugin file, marketplace, future runtime surface"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
