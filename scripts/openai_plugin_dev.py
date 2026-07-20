#!/usr/bin/env python3
"""Inspect, install, and verify the OpenAI plugin development channels.

The tracked worktree is always treated as immutable source. Local cachebuster
versions are written only to the installed copy under ``~/plugins``.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Sequence

import yaml


PLUGIN_NAME = "research-skills-openai"
GIT_MARKETPLACE = "xuxu-research-preview"
LOCAL_VERSION_RE = re.compile(
    r"^(?P<base>.+)\+codex\.local-\d{8}-\d{6}-\d{6}$"
)
PLUGIN_SELECTOR_RE = re.compile(r'^plugins\."(?P<selector>[^"]+)"$')
CommandRunner = Callable[[Sequence[str], Path], subprocess.CompletedProcess[str]]


class DevEnvironmentError(RuntimeError):
    """A safe local development precondition was not met."""


@dataclass(frozen=True)
class PluginIdentity:
    root: Path
    version: str
    registry_version: str
    skill_count: int
    reviewer_count: int
    source_cachebuster: bool


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def default_home() -> Path:
    return Path.home()


def default_config(home: Path) -> Path:
    configured = os.environ.get("CODEX_HOME")
    codex_home = Path(configured).expanduser() if configured else home / ".codex"
    return codex_home / "config.toml"


def plugin_root(root: Path) -> Path:
    return root / PLUGIN_NAME


def local_plugin_root(home: Path) -> Path:
    return home / "plugins" / PLUGIN_NAME


def personal_marketplace_path(home: Path) -> Path:
    return home / ".agents" / "plugins" / "marketplace.json"


def load_toml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    with path.open("rb") as handle:
        payload = tomllib.load(handle)
    if not isinstance(payload, dict):
        raise DevEnvironmentError(f"Codex config is not a TOML object: {path}")
    return payload


def load_json_object(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise DevEnvironmentError(f"Required JSON file is missing: {path}") from exc
    except json.JSONDecodeError as exc:
        raise DevEnvironmentError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise DevEnvironmentError(f"Expected a JSON object: {path}")
    return payload


def load_yaml_object(path: Path) -> dict[str, Any]:
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise DevEnvironmentError(f"Required YAML file is missing: {path}") from exc
    except yaml.YAMLError as exc:
        raise DevEnvironmentError(f"Invalid YAML in {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise DevEnvironmentError(f"Expected a YAML object: {path}")
    return payload


def inspect_plugin(root: Path) -> PluginIdentity:
    manifest = load_json_object(root / ".codex-plugin" / "plugin.json")
    registry = load_yaml_object(root / "workflow-registry.yaml")
    version = manifest.get("version")
    registry_version = registry.get("plugin_version")
    if not isinstance(version, str) or not version:
        raise DevEnvironmentError(f"Missing plugin version in {root}")
    if not isinstance(registry_version, str) or not registry_version:
        raise DevEnvironmentError(f"Missing registry version in {root}")
    skills_root = root / "skills"
    skill_count = sum(
        1
        for child in skills_root.iterdir()
        if child.is_dir() and (child / "SKILL.md").is_file()
    ) if skills_root.is_dir() else 0
    skills = registry.get("skills")
    if not isinstance(skills, list):
        raise DevEnvironmentError(f"Registry skills must be a list: {root}")
    reviewer_count = sum(
        1 for entry in skills if isinstance(entry, dict) and entry.get("role") == "reviewer"
    )
    cachebuster = "+codex." in version or "+codex." in registry_version
    return PluginIdentity(
        root=root.resolve(),
        version=version,
        registry_version=registry_version,
        skill_count=skill_count,
        reviewer_count=reviewer_count,
        source_cachebuster=cachebuster,
    )


def plugin_selectors(config: dict[str, Any]) -> dict[str, bool]:
    plugins = config.get("plugins", {})
    if not isinstance(plugins, dict):
        return {}
    selectors: dict[str, bool] = {}
    for selector, settings in plugins.items():
        if not isinstance(selector, str) or not selector.startswith(f"{PLUGIN_NAME}@"):
            continue
        enabled = isinstance(settings, dict) and settings.get("enabled") is True
        selectors[selector] = enabled
    return selectors


def marketplace_types(config: dict[str, Any]) -> dict[str, str]:
    marketplaces = config.get("marketplaces", {})
    if not isinstance(marketplaces, dict):
        return {}
    result: dict[str, str] = {}
    for name, settings in marketplaces.items():
        if isinstance(name, str) and isinstance(settings, dict):
            source_type = settings.get("source_type")
            if isinstance(source_type, str):
                result[name] = source_type
    return result


def git_selectors(config: dict[str, Any]) -> dict[str, bool]:
    types = marketplace_types(config)
    result: dict[str, bool] = {}
    for selector, enabled in plugin_selectors(config).items():
        marketplace = selector.split("@", 1)[1]
        if types.get(marketplace) == "git" or marketplace == GIT_MARKETPLACE:
            result[selector] = enabled
    return result


def read_personal_marketplace(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    return load_json_object(path)


def personal_marketplace_name(payload: dict[str, Any] | None) -> str | None:
    name = payload.get("name") if payload else None
    return name if isinstance(name, str) and name.strip() else None


def local_marketplace_entry(payload: dict[str, Any] | None) -> dict[str, Any] | None:
    plugins = payload.get("plugins") if payload else None
    if not isinstance(plugins, list):
        return None
    for entry in plugins:
        if isinstance(entry, dict) and entry.get("name") == PLUGIN_NAME:
            return entry
    return None


def local_selector_names(config: dict[str, Any], marketplace: dict[str, Any] | None) -> set[str]:
    name = personal_marketplace_name(marketplace)
    expected = {f"{PLUGIN_NAME}@{name}"} if name else set()
    types = marketplace_types(config)
    for selector in plugin_selectors(config):
        marketplace_name = selector.split("@", 1)[1]
        if types.get(marketplace_name) == "local":
            expected.add(selector)
    return expected


def cache_candidates(home: Path, config: dict[str, Any]) -> list[Path]:
    configured = os.environ.get("CODEX_HOME")
    codex_home = Path(configured).expanduser() if configured else home / ".codex"
    cache_root = codex_home / "plugins" / "cache"
    candidates: list[Path] = []
    for selector in git_selectors(config):
        marketplace = selector.split("@", 1)[1]
        plugin_cache = cache_root / marketplace / PLUGIN_NAME
        if plugin_cache.is_dir():
            candidates.extend(path for path in plugin_cache.iterdir() if path.is_dir())
    return sorted(candidates, key=lambda path: path.name)


def cache_candidates_for_selector(
    home: Path,
    config: dict[str, Any],
    selector: str,
) -> list[Path]:
    """Return only caches owned by one exact configured selector."""

    prefix = f"{PLUGIN_NAME}@"
    if not selector.startswith(prefix):
        return []
    marketplace = selector[len(prefix) :]
    configured = os.environ.get("CODEX_HOME")
    codex_home = Path(configured).expanduser() if configured else home / ".codex"
    plugin_cache = codex_home / "plugins" / "cache" / marketplace / PLUGIN_NAME
    if not plugin_cache.is_dir():
        return []
    return sorted(
        (path for path in plugin_cache.iterdir() if path.is_dir()),
        key=lambda path: path.name,
    )


def configured_cli_path(config: dict[str, Any]) -> Path | None:
    servers = config.get("mcp_servers")
    if not isinstance(servers, dict):
        return None
    node_repl = servers.get("node_repl")
    if not isinstance(node_repl, dict):
        return None
    env = node_repl.get("env")
    raw = env.get("CODEX_CLI_PATH") if isinstance(env, dict) else None
    return Path(raw).expanduser() if isinstance(raw, str) and raw else None


def resolve_codex_cli(home: Path, config: dict[str, Any], explicit: Path | None = None) -> Path:
    candidates: list[Path] = []
    if explicit is not None:
        candidates.append(explicit.expanduser())
    env_cli = os.environ.get("CODEX_CLI_PATH")
    if env_cli:
        candidates.append(Path(env_cli).expanduser())
    configured = configured_cli_path(config)
    if configured is not None:
        candidates.append(configured)
    on_path = shutil.which("codex")
    if on_path:
        candidates.append(Path(on_path))
    app_bins = home / "AppData" / "Local" / "OpenAI" / "Codex" / "bin"
    if app_bins.is_dir():
        candidates.extend(sorted(app_bins.glob("*/codex.exe"), reverse=True))
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    raise DevEnvironmentError(
        "Codex CLI was not found. Set CODEX_CLI_PATH or pass --codex-cli."
    )


def expected_local_source_path() -> str:
    return f"./plugins/{PLUGIN_NAME}"


def summarize(root: Path, home: Path, config_path: Path, explicit_cli: Path | None) -> dict[str, Any]:
    source = inspect_plugin(plugin_root(root))
    config = load_toml(config_path)
    marketplace_path = personal_marketplace_path(home)
    marketplace = read_personal_marketplace(marketplace_path)
    local_root = local_plugin_root(home)
    local = inspect_plugin(local_root) if local_root.is_dir() else None
    selectors = plugin_selectors(config)
    git = git_selectors(config)
    local_names = local_selector_names(config, marketplace)
    enabled = sorted(selector for selector, value in selectors.items() if value)
    try:
        cli: str | None = str(resolve_codex_cli(home, config, explicit_cli))
    except DevEnvironmentError:
        cli = None
    entry = local_marketplace_entry(marketplace)
    source_field = entry.get("source") if isinstance(entry, dict) else None
    personal_name = personal_marketplace_name(marketplace)
    personal_selector = f"{PLUGIN_NAME}@{personal_name}" if personal_name else None
    return {
        "source": identity_dict(source),
        "codex_config": str(config_path.resolve()),
        "codex_cli": cli,
        "selectors": selectors,
        "git_selectors": git,
        "local_selectors": sorted(local_names),
        "personal_local_selector": personal_selector,
        "enabled_selectors": enabled,
        "duplicate_enabled": len(enabled) > 1,
        "git_enabled": any(git.values()),
        "local_enabled": any(selectors.get(name, False) for name in local_names),
        "git_cache_roots": [str(path.resolve()) for path in cache_candidates(home, config)],
        "local_plugin": identity_dict(local) if local else None,
        "personal_marketplace": str(marketplace_path.resolve()),
        "personal_marketplace_name": personal_name,
        "local_marketplace_entry": entry,
        "local_entry_points_to_expected_copy": (
            isinstance(source_field, dict)
            and source_field.get("source") == "local"
            and source_field.get("path") == expected_local_source_path()
        ),
    }


def identity_dict(identity: PluginIdentity | None) -> dict[str, Any] | None:
    if identity is None:
        return None
    return {
        "root": str(identity.root),
        "version": identity.version,
        "registry_version": identity.registry_version,
        "skill_count": identity.skill_count,
        "reviewer_count": identity.reviewer_count,
        "source_cachebuster": identity.source_cachebuster,
    }


def print_summary(payload: dict[str, Any]) -> None:
    source = payload["source"]
    print(f"worktree: {source['root']}")
    print(
        "source identity: "
        f"version={source['version']} skills={source['skill_count']} "
        f"reviewers={source['reviewer_count']}"
    )
    print(f"source cachebuster: {source['source_cachebuster']}")
    print(f"Codex CLI: {payload['codex_cli'] or '<not found>'}")
    print(f"Git enabled: {payload['git_enabled']}")
    print(f"local enabled: {payload['local_enabled']}")
    print(f"duplicate enabled: {payload['duplicate_enabled']}")
    print(f"enabled selectors: {payload['enabled_selectors'] or []}")
    print(f"Git cache roots: {payload['git_cache_roots'] or []}")
    local = payload["local_plugin"]
    print(f"local copy: {local['root'] if local else '<not installed>'}")
    if local:
        print(
            "local identity: "
            f"version={local['version']} skills={local['skill_count']} "
            f"reviewers={local['reviewer_count']}"
        )


def assert_source_ready(identity: PluginIdentity) -> None:
    problems: list[str] = []
    if identity.version != identity.registry_version:
        problems.append("plugin.json and workflow-registry.yaml versions differ")
    if identity.source_cachebuster:
        problems.append("tracked source contains a Codex cachebuster")
    if identity.skill_count == 0:
        problems.append("no skills were discovered")
    if problems:
        raise DevEnvironmentError("Source is not installable: " + "; ".join(problems))


def default_runner(command: Sequence[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(command),
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def validator_path(home: Path, explicit: Path | None) -> Path:
    if explicit is not None:
        path = explicit.expanduser()
    else:
        path = home / ".codex" / "skills" / ".system" / "plugin-creator" / "scripts" / "validate_plugin.py"
    if not path.is_file():
        raise DevEnvironmentError(f"Plugin validator is missing: {path}")
    return path.resolve()


def validate_source(
    root: Path,
    home: Path,
    explicit_validator: Path | None,
    runner: CommandRunner,
) -> None:
    source_root = plugin_root(root)
    assert_source_ready(inspect_plugin(source_root))
    audit = root / "scripts" / "audit_openai_research_plugin.py"
    if not audit.is_file():
        raise DevEnvironmentError(f"Plugin audit is missing: {audit}")
    runner([sys.executable, str(audit)], root)
    runner(
        [sys.executable, str(validator_path(home, explicit_validator)), str(source_root)],
        root,
    )


def cachebuster_version(base_version: str, now: dt.datetime | None = None) -> str:
    base = base_version.split("+", 1)[0]
    instant = now or dt.datetime.now(dt.timezone.utc)
    token = instant.astimezone(dt.timezone.utc).strftime("%Y%m%d-%H%M%S-%f")
    return f"{base}+codex.local-{token}"


def comparable_plugin_files(root: Path) -> dict[str, Path]:
    """Return the deterministic plugin inventory used for copy verification."""

    result: dict[str, Path] = {}
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if (
            "__pycache__" in relative.parts
            or path.suffix == ".pyc"
            or path.name in {".DS_Store"}
        ):
            continue
        result[relative.as_posix()] = path
    return result


def compare_plugin_copy(source_root: Path, copy_root: Path, *, local: bool) -> list[str]:
    """Compare full inventories without computing or persisting content hashes."""

    source_files = comparable_plugin_files(source_root)
    copy_files = comparable_plugin_files(copy_root)
    errors: list[str] = []
    missing = sorted(set(source_files) - set(copy_files))
    extra = sorted(set(copy_files) - set(source_files))
    if missing:
        errors.append("copy is missing files: " + ", ".join(missing))
    if extra:
        errors.append("copy contains unexpected files: " + ", ".join(extra))

    for relative in sorted(set(source_files) & set(copy_files)):
        source_path = source_files[relative]
        copy_path = copy_files[relative]
        if local and relative in {
            ".codex-plugin/plugin.json",
            "workflow-registry.yaml",
        }:
            try:
                source_bytes = normalize_local_version_bytes(
                    relative, source_path.read_bytes()
                )
                copy_bytes = normalize_local_version_bytes(
                    relative, copy_path.read_bytes()
                )
            except DevEnvironmentError as exc:
                errors.append(f"copy version normalization failed: {relative}: {exc}")
                continue
            matches = copy_bytes == source_bytes
        else:
            matches = source_path.read_bytes() == copy_path.read_bytes()
        if not matches:
            errors.append(f"copy content differs: {relative}")
    return errors


def normalize_local_version_bytes(relative: str, payload: bytes) -> bytes:
    """Mask only the permitted local version value and preserve every other byte."""

    if relative == ".codex-plugin/plugin.json":
        pattern = re.compile(br'("version"[ \t]*:[ \t]*")[^"\r\n]+(")')
    elif relative == "workflow-registry.yaml":
        pattern = re.compile(br'(?m)^(plugin_version:[ \t]*")[^"\r\n]+(")')
    else:
        raise DevEnvironmentError(f"unsupported local version file: {relative}")
    normalized, count = pattern.subn(br'\1<CACHEBUSTER>\2', payload, count=1)
    if count != 1:
        raise DevEnvironmentError("expected exactly one version field")
    return normalized


def write_local_version(root: Path, version: str) -> None:
    manifest_path = root / ".codex-plugin" / "plugin.json"
    version_bytes = version.encode("utf-8")
    manifest_pattern = re.compile(br'("version"[ \t]*:[ \t]*")[^"\r\n]+(")')
    manifest_bytes, manifest_count = manifest_pattern.subn(
        lambda match: match.group(1) + version_bytes + match.group(2),
        manifest_path.read_bytes(),
        count=1,
    )
    if manifest_count != 1:
        raise DevEnvironmentError(f"Manifest version is missing: {manifest_path}")
    manifest_path.write_bytes(manifest_bytes)
    registry_path = root / "workflow-registry.yaml"
    registry_pattern = re.compile(br'(?m)^(plugin_version:[ \t]*")[^"\r\n]+(")')
    registry_bytes, registry_count = registry_pattern.subn(
        lambda match: match.group(1) + version_bytes + match.group(2),
        registry_path.read_bytes(),
        count=1,
    )
    if registry_count != 1:
        raise DevEnvironmentError(f"Registry plugin_version is missing: {registry_path}")
    registry_path.write_bytes(registry_bytes)


def copy_to_staging(source: Path, target: Path) -> Path:
    target.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{PLUGIN_NAME}.staging-", dir=target.parent))
    shutil.rmtree(staging)
    shutil.copytree(
        source,
        staging,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache", ".DS_Store"),
    )
    return staging


def install_local(
    root: Path,
    home: Path,
    config_path: Path,
    explicit_cli: Path | None,
    explicit_validator: Path | None,
    runner: CommandRunner = default_runner,
    now: dt.datetime | None = None,
) -> str:
    config = load_toml(config_path)
    enabled_git = sorted(selector for selector, enabled in git_selectors(config).items() if enabled)
    if enabled_git:
        raise DevEnvironmentError(
            "Disable the Git marketplace plugin in the Codex app before local installation: "
            + ", ".join(enabled_git)
        )
    validate_source(root, home, explicit_validator, runner)
    source = inspect_plugin(plugin_root(root))
    version = cachebuster_version(source.version, now)
    target = local_plugin_root(home)
    marketplace_path = personal_marketplace_path(home)
    marketplace = read_personal_marketplace(marketplace_path)
    marketplace_name = personal_marketplace_name(marketplace)
    entry = local_marketplace_entry(marketplace)
    source_field = entry.get("source") if isinstance(entry, dict) else None
    if (
        marketplace_name is None
        or not isinstance(source_field, dict)
        or source_field.get("source") != "local"
        or source_field.get("path") != expected_local_source_path()
    ):
        raise DevEnvironmentError(
            "The personal marketplace must already contain a local "
            f"{PLUGIN_NAME} entry pointing to {expected_local_source_path()}. "
            "Create or repair that entry with plugin-creator before using the update loop."
        )
    staging = copy_to_staging(plugin_root(root), target)
    backup = target.parent / f".{PLUGIN_NAME}.backup"
    target_was_moved = False
    try:
        write_local_version(staging, version)
        staged = inspect_plugin(staging)
        if staged.version != version or staged.registry_version != version:
            raise DevEnvironmentError("Local staging versions did not update together")
        runner(
            [sys.executable, str(validator_path(home, explicit_validator)), str(staging)],
            root,
        )
        if backup.exists():
            raise DevEnvironmentError(
                f"Stale local-install backup must be resolved before retrying: {backup}"
            )
        if target.exists():
            target.rename(backup)
            target_was_moved = True
        staging.rename(target)
        cli = resolve_codex_cli(home, config, explicit_cli)
        runner([str(cli), "plugin", "add", f"{PLUGIN_NAME}@{marketplace_name}", "--json"], root)
    except Exception:
        if target.exists() and (target_was_moved or not staging.exists()):
            shutil.rmtree(target)
        if target_was_moved and backup.exists():
            backup.rename(target)
        if staging.exists():
            shutil.rmtree(staging)
        raise
    if backup.exists():
        shutil.rmtree(backup)
    print(f"Installed local copy: {target}")
    print(f"Local version: {version}")
    print("Start a new Codex task before testing the updated skills.")
    return version


def version_matches_local(actual: str, expected: str) -> bool:
    match = LOCAL_VERSION_RE.fullmatch(actual)
    return match is not None and match.group("base") == expected


def verify_channel(
    channel: str,
    expected_version: str,
    root: Path,
    home: Path,
    config_path: Path,
    explicit_cli: Path | None,
) -> list[str]:
    config = load_toml(config_path)
    summary = summarize(root, home, config_path, explicit_cli)
    source = summary["source"]
    errors: list[str] = []
    if source["version"] != expected_version or source["registry_version"] != expected_version:
        errors.append("worktree manifest/registry do not match the expected version")
    if source["source_cachebuster"]:
        errors.append("worktree contains a local cachebuster")
    if summary["duplicate_enabled"]:
        errors.append("more than one research-skills-openai channel is enabled")
    if channel == "local":
        local = summary["local_plugin"]
        if local is None:
            errors.append("local plugin copy is missing")
        else:
            if not version_matches_local(local["version"], expected_version):
                errors.append("local manifest lacks the expected local cachebuster version")
            if local["registry_version"] != local["version"]:
                errors.append("local manifest and registry versions differ")
            if local["skill_count"] != source["skill_count"]:
                errors.append("local skill inventory differs from the worktree")
            if local["reviewer_count"] != source["reviewer_count"]:
                errors.append("local reviewer inventory differs from the worktree")
            errors.extend(
                "local " + message
                for message in compare_plugin_copy(
                    plugin_root(root), local_plugin_root(home), local=True
                )
            )
        if not summary["local_entry_points_to_expected_copy"]:
            errors.append("personal marketplace does not point at the expected local copy")
        if summary["git_enabled"]:
            errors.append("Git marketplace channel is still enabled")
        personal_selector = summary["personal_local_selector"]
        if not isinstance(personal_selector, str) or not summary["selectors"].get(
            personal_selector, False
        ):
            errors.append("the personal Local plugin selector is not enabled")
    elif channel == "github":
        if summary["local_enabled"]:
            errors.append("local plugin channel is still enabled")
        expected_selector = f"{PLUGIN_NAME}@{GIT_MARKETPLACE}"
        expected_enabled = summary["selectors"].get(expected_selector, False)
        if not expected_enabled:
            errors.append("the expected Git marketplace selector is not enabled")
        cache_roots = (
            cache_candidates_for_selector(home, config, expected_selector)
            if expected_enabled
            else []
        )
        matching_cache = False
        for candidate in cache_roots:
            try:
                identity = inspect_plugin(candidate)
            except DevEnvironmentError:
                continue
            if (
                identity.version == expected_version
                and identity.registry_version == expected_version
                and identity.skill_count == source["skill_count"]
                and identity.reviewer_count == source["reviewer_count"]
                and not compare_plugin_copy(plugin_root(root), candidate, local=False)
            ):
                matching_cache = True
                break
        if not matching_cache:
            errors.append("no Git marketplace cache matches the expected source identity")
    else:
        errors.append(f"unsupported verification channel: {channel}")
    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=repo_root())
    parser.add_argument("--home", type=Path, default=default_home())
    parser.add_argument("--config", type=Path)
    parser.add_argument("--codex-cli", type=Path)
    subparsers = parser.add_subparsers(dest="command", required=True)
    status = subparsers.add_parser("status", help="Read development-channel state.")
    status.add_argument("--json", action="store_true")
    install = subparsers.add_parser("install-local", help="Install an isolated local copy.")
    install.add_argument("--validator", type=Path)
    verify = subparsers.add_parser("verify", help="Verify the selected active channel.")
    verify.add_argument("--channel", choices=("local", "github"), required=True)
    verify.add_argument("--expected-version", required=True)
    verify.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = args.repo_root.expanduser().resolve()
    home = args.home.expanduser().resolve()
    config_path = (args.config or default_config(home)).expanduser().resolve()
    try:
        if args.command == "status":
            payload = summarize(root, home, config_path, args.codex_cli)
            if args.json:
                print(json.dumps(payload, ensure_ascii=False, indent=2))
            else:
                print_summary(payload)
            return 0
        if args.command == "install-local":
            install_local(
                root,
                home,
                config_path,
                args.codex_cli,
                args.validator,
            )
            return 0
        if args.command == "verify":
            errors = verify_channel(
                args.channel,
                args.expected_version,
                root,
                home,
                config_path,
                args.codex_cli,
            )
            payload = {"channel": args.channel, "ok": not errors, "errors": errors}
            if args.json:
                print(json.dumps(payload, ensure_ascii=False, indent=2))
            elif errors:
                print(f"{args.channel} channel verification failed:")
                for error in errors:
                    print(f"- {error}")
            else:
                print(f"{args.channel} channel verified for {args.expected_version}")
            return 0 if not errors else 1
    except (DevEnvironmentError, OSError, subprocess.CalledProcessError) as exc:
        print(f"OpenAI plugin development command failed: {exc}", file=sys.stderr)
        if isinstance(exc, subprocess.CalledProcessError):
            if exc.stdout:
                print(exc.stdout.rstrip(), file=sys.stderr)
            if exc.stderr:
                print(exc.stderr.rstrip(), file=sys.stderr)
        return 2
    raise AssertionError("unreachable")


if __name__ == "__main__":
    raise SystemExit(main())
