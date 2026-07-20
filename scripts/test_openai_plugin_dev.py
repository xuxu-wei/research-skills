#!/usr/bin/env python3
"""Deterministic tests for the isolated OpenAI plugin development channels."""

from __future__ import annotations

import datetime as dt
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

import openai_plugin_dev as dev


VERSION = "0.11.0"


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def write(path: Path, contents: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contents, encoding="utf-8")


def make_plugin(root: Path, version: str = VERSION) -> Path:
    plugin = root / dev.PLUGIN_NAME
    manifest = {
        "name": dev.PLUGIN_NAME,
        "version": version,
        "description": "Fixture",
        "author": {"name": "Fixture"},
        "skills": "./skills/",
        "interface": {
            "displayName": "Fixture",
            "shortDescription": "Fixture",
            "longDescription": "Fixture",
            "developerName": "Fixture",
            "category": "Research",
            "capabilities": [],
            "defaultPrompt": "Fixture",
        },
    }
    write(plugin / ".codex-plugin" / "plugin.json", json.dumps(manifest, indent=2) + "\n")
    write(
        plugin / "workflow-registry.yaml",
        f'''schema_version: "openai-workflow-registry.v1"
plugin_version: "{version}"
skills:
  - name: writer
    role: generator
  - name: reviewer
    role: reviewer
''',
    )
    write(plugin / "skills" / "writer" / "SKILL.md", "---\nname: writer\ndescription: Fixture\n---\n")
    write(plugin / "skills" / "reviewer" / "SKILL.md", "---\nname: reviewer\ndescription: Fixture\n---\n")
    return plugin


def make_repo(base: Path) -> Path:
    root = base / "repo"
    make_plugin(root)
    write(root / "scripts" / "audit_openai_research_plugin.py", "raise SystemExit(0)\n")
    return root


def make_home(base: Path) -> tuple[Path, Path, Path]:
    home = base / "home"
    config = home / ".codex" / "config.toml"
    cli = home / "bin" / "codex.exe"
    validator = home / "validator.py"
    write(cli, "fixture")
    write(validator, "raise SystemExit(0)\n")
    return home, config, validator


def config_text(*, git_enabled: bool, local_enabled: bool, local_name: str = "local") -> str:
    git = str(git_enabled).lower()
    local = str(local_enabled).lower()
    return f'''
[marketplaces.{dev.GIT_MARKETPLACE}]
source_type = "git"
source = "https://example.invalid/repo.git"

[plugins."{dev.PLUGIN_NAME}@{dev.GIT_MARKETPLACE}"]
enabled = {git}

[plugins."{dev.PLUGIN_NAME}@{local_name}"]
enabled = {local}
'''


def make_marketplace(home: Path) -> Path:
    path = dev.personal_marketplace_path(home)
    payload = {
        "name": "local",
        "interface": {"displayName": "Local Plugins"},
        "plugins": [
            {
                "name": "unrelated-plugin",
                "source": {"source": "local", "path": "./plugins/unrelated-plugin"},
                "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                "category": "Other",
            },
            {
                "name": dev.PLUGIN_NAME,
                "source": {
                    "source": "local",
                    "path": dev.expected_local_source_path(),
                },
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL",
                },
                "category": "Research",
            },
        ],
    }
    write(path, json.dumps(payload, indent=2) + "\n")
    return path


class RecordingRunner:
    def __init__(self, *, fail_add: bool = False) -> None:
        self.commands: list[list[str]] = []
        self.fail_add = fail_add

    def __call__(self, command: list[str] | tuple[str, ...], cwd: Path) -> subprocess.CompletedProcess[str]:
        normalized = list(command)
        self.commands.append(normalized)
        if self.fail_add and "add" in normalized:
            raise subprocess.CalledProcessError(1, normalized, stderr="fixture add failure")
        return subprocess.CompletedProcess(normalized, 0, stdout="{}", stderr="")


def install_fixture(base: Path) -> tuple[Path, Path, Path, RecordingRunner]:
    root = make_repo(base)
    home, config, validator = make_home(base)
    write(config, config_text(git_enabled=False, local_enabled=False))
    marketplace = make_marketplace(home)
    original_marketplace = marketplace.read_bytes()
    cli = home / "bin" / "codex.exe"
    runner = RecordingRunner()
    installed_version = dev.install_local(
        root,
        home,
        config,
        cli,
        validator,
        runner=runner,
        now=dt.datetime(2026, 7, 18, 1, 2, 3, tzinfo=dt.timezone.utc),
    )
    require(
        installed_version == f"{VERSION}+codex.local-20260718-010203-000000",
        "cachebuster format",
    )
    require(dev.inspect_plugin(root / dev.PLUGIN_NAME).version == VERSION, "source version mutated")
    installed = dev.inspect_plugin(dev.local_plugin_root(home))
    require(installed.version == installed_version, "installed manifest version")
    require(installed.registry_version == installed_version, "installed registry version")
    payload = json.loads(marketplace.read_text(encoding="utf-8"))
    require(marketplace.read_bytes() == original_marketplace, "update loop rewrote marketplace")
    names = [entry.get("name") for entry in payload["plugins"]]
    require("unrelated-plugin" in names, "unrelated marketplace entry was lost")
    entry = next(entry for entry in payload["plugins"] if entry.get("name") == dev.PLUGIN_NAME)
    require(entry["source"]["path"] == dev.expected_local_source_path(), "local source path")
    require(any(command[1:3] == ["plugin", "add"] for command in runner.commands), "plugin add not run")
    return root, home, config, runner


def test_status_and_duplicate_detection(base: Path) -> None:
    root = make_repo(base)
    home, config, _ = make_home(base)
    make_marketplace(home)
    write(config, config_text(git_enabled=True, local_enabled=True))
    summary = dev.summarize(root, home, config, home / "bin" / "codex.exe")
    require(summary["source"]["skill_count"] == 2, "skill count")
    require(summary["source"]["reviewer_count"] == 1, "reviewer count")
    require(summary["duplicate_enabled"] is True, "duplicate enablement not detected")
    require(summary["git_enabled"] is True, "Git enablement not detected")
    require(summary["local_enabled"] is True, "local enablement not detected")


def test_git_enabled_refusal(base: Path) -> None:
    root = make_repo(base)
    home, config, validator = make_home(base)
    write(config, config_text(git_enabled=True, local_enabled=False))
    runner = RecordingRunner()
    try:
        dev.install_local(
            root,
            home,
            config,
            home / "bin" / "codex.exe",
            validator,
            runner=runner,
        )
    except dev.DevEnvironmentError as exc:
        require("Disable the Git marketplace plugin" in str(exc), "wrong refusal reason")
    else:
        raise AssertionError("Git-enabled install was not refused")
    require(not runner.commands, "validation ran before Git-channel refusal")
    require(not dev.local_plugin_root(home).exists(), "local copy created after refusal")


def test_missing_marketplace_entry_refusal(base: Path) -> None:
    root = make_repo(base)
    home, config, validator = make_home(base)
    write(config, config_text(git_enabled=False, local_enabled=False))
    marketplace = make_marketplace(home)
    payload = json.loads(marketplace.read_text(encoding="utf-8"))
    payload["plugins"] = [
        entry for entry in payload["plugins"] if entry.get("name") != dev.PLUGIN_NAME
    ]
    write(marketplace, json.dumps(payload, indent=2) + "\n")
    before = marketplace.read_bytes()
    runner = RecordingRunner()
    try:
        dev.install_local(
            root,
            home,
            config,
            home / "bin" / "codex.exe",
            validator,
            runner=runner,
        )
    except dev.DevEnvironmentError as exc:
        require("must already contain a local" in str(exc), "wrong marketplace refusal")
    else:
        raise AssertionError("missing marketplace entry was not refused")
    require(marketplace.read_bytes() == before, "refusal rewrote marketplace")
    require(not dev.local_plugin_root(home).exists(), "local copy created after refusal")


def test_install_and_local_verify(base: Path) -> None:
    root, home, config, _ = install_fixture(base)
    write(config, config_text(git_enabled=False, local_enabled=True))
    errors = dev.verify_channel(
        "local",
        VERSION,
        root,
        home,
        config,
        home / "bin" / "codex.exe",
    )
    require(not errors, f"local verification failed: {errors}")


def test_local_verify_detects_stale_same_version_copy(base: Path) -> None:
    root, home, config, _ = install_fixture(base)
    write(config, config_text(git_enabled=False, local_enabled=True))
    source_skill = root / dev.PLUGIN_NAME / "skills" / "writer" / "SKILL.md"
    source_skill.write_text(
        source_skill.read_text(encoding="utf-8") + "\nUpdated instruction.\n",
        encoding="utf-8",
    )
    errors = dev.verify_channel(
        "local",
        VERSION,
        root,
        home,
        config,
        home / "bin" / "codex.exe",
    )
    require(
        any("local copy content differs: skills/writer/SKILL.md" in item for item in errors),
        f"stale same-version copy was not detected: {errors}",
    )
    write(
        root / dev.PLUGIN_NAME / "skills" / "writer" / "references" / "new-rule.md",
        "# New rule\n",
    )
    errors = dev.verify_channel(
        "local",
        VERSION,
        root,
        home,
        config,
        home / "bin" / "codex.exe",
    )
    require(
        any("local copy is missing files: skills/writer/references/new-rule.md" in item for item in errors),
        f"stale inventory was not detected: {errors}",
    )


def test_local_verify_binds_personal_selector_and_exact_bytes(base: Path) -> None:
    root, home, config, _ = install_fixture(base)
    write(
        config,
        f'''
[marketplaces.{dev.GIT_MARKETPLACE}]
source_type = "git"

[marketplaces.other-local]
source_type = "local"

[plugins."{dev.PLUGIN_NAME}@{dev.GIT_MARKETPLACE}"]
enabled = false

[plugins."{dev.PLUGIN_NAME}@local"]
enabled = false

[plugins."{dev.PLUGIN_NAME}@other-local"]
enabled = true
''',
    )
    errors = dev.verify_channel(
        "local", VERSION, root, home, config, home / "bin" / "codex.exe"
    )
    require(
        "the personal Local plugin selector is not enabled" in errors,
        f"another Local selector was accepted: {errors}",
    )

    write(config, config_text(git_enabled=False, local_enabled=True))
    installed_registry = dev.local_plugin_root(home) / "workflow-registry.yaml"
    installed_registry.write_bytes(b"# unexpected installed-only comment\n" + installed_registry.read_bytes())
    installed_manifest = dev.local_plugin_root(home) / ".codex-plugin" / "plugin.json"
    payload = json.loads(installed_manifest.read_text(encoding="utf-8"))
    reordered = {key: payload[key] for key in reversed(payload)}
    installed_manifest.write_text(json.dumps(reordered, indent=2) + "\n", encoding="utf-8")
    errors = dev.verify_channel(
        "local", VERSION, root, home, config, home / "bin" / "codex.exe"
    )
    require(
        any("local copy content differs: workflow-registry.yaml" in item for item in errors),
        f"registry text drift was ignored: {errors}",
    )
    require(
        any("local copy content differs: .codex-plugin/plugin.json" in item for item in errors),
        f"manifest key-order drift was ignored: {errors}",
    )


def test_github_verify(base: Path) -> None:
    root = make_repo(base)
    home, config, _ = make_home(base)
    write(config, config_text(git_enabled=True, local_enabled=False))
    cache = (
        home
        / ".codex"
        / "plugins"
        / "cache"
        / dev.GIT_MARKETPLACE
        / dev.PLUGIN_NAME
        / VERSION
    )
    shutil.copytree(root / dev.PLUGIN_NAME, cache)
    errors = dev.verify_channel(
        "github",
        VERSION,
        root,
        home,
        config,
        home / "bin" / "codex.exe",
    )
    require(not errors, f"GitHub verification failed: {errors}")
    source_skill = root / dev.PLUGIN_NAME / "skills" / "writer" / "SKILL.md"
    source_skill.write_text(
        source_skill.read_text(encoding="utf-8") + "\nUnpushed source change.\n",
        encoding="utf-8",
    )
    errors = dev.verify_channel(
        "github",
        VERSION,
        root,
        home,
        config,
        home / "bin" / "codex.exe",
    )
    require(
        "no Git marketplace cache matches the expected source identity" in errors,
        f"stale Git cache was not detected: {errors}",
    )


def test_github_verify_rejects_disabled_correct_cache(base: Path) -> None:
    root = make_repo(base)
    home, config, _ = make_home(base)
    write(
        config,
        f'''
[marketplaces.{dev.GIT_MARKETPLACE}]
source_type = "git"

[marketplaces.other-git]
source_type = "git"

[plugins."{dev.PLUGIN_NAME}@{dev.GIT_MARKETPLACE}"]
enabled = false

[plugins."{dev.PLUGIN_NAME}@other-git"]
enabled = true
''',
    )
    correct_but_disabled = (
        home
        / ".codex"
        / "plugins"
        / "cache"
        / dev.GIT_MARKETPLACE
        / dev.PLUGIN_NAME
        / VERSION
    )
    shutil.copytree(root / dev.PLUGIN_NAME, correct_but_disabled)
    enabled_but_wrong = (
        home
        / ".codex"
        / "plugins"
        / "cache"
        / "other-git"
        / dev.PLUGIN_NAME
        / VERSION
    )
    shutil.copytree(root / dev.PLUGIN_NAME, enabled_but_wrong)
    (enabled_but_wrong / "skills" / "writer" / "SKILL.md").write_text(
        "wrong enabled cache\n", encoding="utf-8"
    )
    errors = dev.verify_channel(
        "github", VERSION, root, home, config, home / "bin" / "codex.exe"
    )
    require(
        "the expected Git marketplace selector is not enabled" in errors,
        f"disabled correct Git cache was accepted: {errors}",
    )


def test_failed_add_rolls_back(base: Path) -> None:
    root = make_repo(base)
    home, config, validator = make_home(base)
    write(config, config_text(git_enabled=False, local_enabled=False))
    marketplace = make_marketplace(home)
    original_marketplace = marketplace.read_bytes()
    old = make_plugin(home / "plugins", "0.8.0-preview.1")
    old_manifest = (old / ".codex-plugin" / "plugin.json").read_bytes()
    runner = RecordingRunner(fail_add=True)
    try:
        dev.install_local(
            root,
            home,
            config,
            home / "bin" / "codex.exe",
            validator,
            runner=runner,
            now=dt.datetime(2026, 7, 18, tzinfo=dt.timezone.utc),
        )
    except subprocess.CalledProcessError:
        pass
    else:
        raise AssertionError("fixture plugin-add failure was swallowed")
    require(marketplace.read_bytes() == original_marketplace, "marketplace rollback")
    require(
        (dev.local_plugin_root(home) / ".codex-plugin" / "plugin.json").read_bytes()
        == old_manifest,
        "previous local copy rollback",
    )
    require(not (home / "plugins" / f".{dev.PLUGIN_NAME}.backup").exists(), "backup leaked")


def main() -> int:
    tests = (
        test_status_and_duplicate_detection,
        test_git_enabled_refusal,
        test_missing_marketplace_entry_refusal,
        test_install_and_local_verify,
        test_local_verify_detects_stale_same_version_copy,
        test_local_verify_binds_personal_selector_and_exact_bytes,
        test_github_verify,
        test_github_verify_rejects_disabled_correct_cache,
        test_failed_add_rolls_back,
    )
    for test in tests:
        with tempfile.TemporaryDirectory(prefix="openai-plugin-dev-test-") as raw:
            test(Path(raw))
    print("OpenAI plugin development tests passed")
    print(f"cases: {len(tests)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
