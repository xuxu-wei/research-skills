"""Validate/install the OpenAI preview plugin and optionally build flat skills.

This script supports two distinct outputs:

- skills-flatten: a plain flat skills directory for broad agent compatibility.
- research-skills-openai: the maintained Codex plugin source.

Codex mode never regenerates or overwrites the maintained plugin from Hermes
sources. The plugin is the source of truth for OpenAI builds.
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import yaml


CORE_PACKAGES = [
    "research-idea",
    "research-proposal",
    "research-article",
    "research-perspective",
]

SKILLS_DIR_NAME = "research-skills"

RESEARCH_DEPENDENCIES = [
    "methodology-statistics-preflight",
    "research-landscape-mapper",
    "pubmed",
    "arxiv",
    "focused-literature-synthesizer",
    "academic-language-assessor",
    "medical-journal-review",
    "llm-wiki",
]

OBSIDIAN_DEPENDENCIES = [
    "obsidian-markdown",
]

PRODUCTIVITY_DEPENDENCIES = [
    "ocr-and-documents",
    "powerpoint",
]

PLUGIN_VARIANTS = {
    "openai": "research-skills-openai",
}

MARKETPLACE_CATEGORY = "Research"
FLATTEN_DIR = "skills-flatten"
LEGACY_FLATTEN_PLUGIN = "skills-flatten"
LEGACY_OPENAI_PLUGIN = "skills-openai-plugin"


@dataclass(frozen=True)
class SkillSource:
    name: str
    source_dir: Path
    package: str
    relative_source: str


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def skills_root(root: Path) -> Path:
    return root / SKILLS_DIR_NAME


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def try_write_text(path: Path, content: str) -> str | None:
    try:
        write_text(path, content)
    except PermissionError as exc:
        return f"Could not write {path}: {exc}"
    return None


def parse_frontmatter(text: str) -> dict[str, object]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}

    raw = text[4:end].splitlines()
    parsed: dict[str, object] = {}
    current_key: str | None = None
    current_list: list[str] | None = None
    for line in raw:
        if not line.strip():
            continue
        if not line.startswith((" ", "\t")) and ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            current_key = key
            current_list = None
            if value.startswith("[") and value.endswith("]"):
                parsed[key] = [item.strip().strip("'\"") for item in value[1:-1].split(",") if item.strip()]
            elif value:
                parsed[key] = value.strip("'\"")
            else:
                parsed[key] = ""
            continue
        if current_key and line.lstrip().startswith("- "):
            if current_list is None:
                current_list = []
                parsed[current_key] = current_list
            current_list.append(line.lstrip()[2:].strip().strip("'\""))
    return parsed


def frontmatter_text(text: str) -> str:
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---", 4)
    if end == -1:
        return ""
    return text[4:end]


def extract_related_skills(text: str) -> set[str]:
    """Extract only metadata related_skills values from YAML frontmatter."""
    fm = frontmatter_text(text)
    if not fm:
        return set()

    related: set[str] = set()
    lines = fm.splitlines()
    for index, line in enumerate(lines):
        if "related_skills:" not in line:
            continue

        prefix, value = line.split("related_skills:", 1)
        base_indent = len(prefix) - len(prefix.lstrip(" "))
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            related.update(item.strip().strip("'\"") for item in value[1:-1].split(",") if item.strip())
            continue

        for child in lines[index + 1 :]:
            if not child.strip():
                continue
            indent = len(child) - len(child.lstrip(" "))
            stripped = child.strip()
            if indent <= base_indent and not stripped.startswith("- "):
                break
            if stripped.startswith("- "):
                related.add(stripped[2:].strip().strip("'\""))
                continue
            if indent <= base_indent:
                break

    return {item for item in related if item}


def skill_name(skill_dir: Path) -> str:
    text = read_text(skill_dir / "SKILL.md")
    fm = parse_frontmatter(text)
    name = fm.get("name")
    if isinstance(name, str) and name.strip():
        return name.strip()
    return skill_dir.name


def safe_replace_dir(target: Path, allowed_parent: Path, allowed_names: Iterable[str]) -> None:
    target_resolved = target.resolve()
    parent_resolved = allowed_parent.resolve()
    allowed = set(allowed_names)
    if target_resolved.parent != parent_resolved or target_resolved.name not in allowed:
        raise RuntimeError(f"Refusing to replace unexpected directory: {target}")
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True, exist_ok=True)


def copy_dir(src: Path, dst: Path) -> None:
    if not src.exists():
        raise FileNotFoundError(src)
    shutil.copytree(src, dst, dirs_exist_ok=True)


def copy_file(src: Path, dst: Path) -> None:
    if not src.exists():
        raise FileNotFoundError(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def discover_leaf_skills(root: Path) -> list[Path]:
    return sorted(path.parent for path in root.rglob("SKILL.md"))


def legacy_hermes_skill_source_aliases(root: Path) -> dict[str, str]:
    registry_path = root / PLUGIN_VARIANTS["openai"] / "workflow-registry.yaml"
    registry = yaml.safe_load(read_text(registry_path)) or {}
    aliases = registry.get("legacy_skill_name_aliases", {})
    if not isinstance(aliases, dict):
        raise RuntimeError("Registry legacy_skill_name_aliases must be a mapping")
    return {str(current): str(legacy) for legacy, current in aliases.items()}


def source_packages(root: Path) -> list[Path]:
    root_skills = skills_root(root)
    hermes_aliases = legacy_hermes_skill_source_aliases(root)
    paths = [root_skills / package for package in CORE_PACKAGES]
    paths.extend(
        root_skills
        / "research"
        / hermes_aliases.get(name, name)
        for name in RESEARCH_DEPENDENCIES
    )
    paths.extend(root_skills / "obsidian-skills" / name for name in OBSIDIAN_DEPENDENCIES)
    paths.extend(root_skills / "productivity" / name for name in PRODUCTIVITY_DEPENDENCIES)
    return paths


def discover_sources(root: Path) -> list[SkillSource]:
    sources: list[SkillSource] = []
    for package_path in source_packages(root):
        if not package_path.exists():
            raise FileNotFoundError(f"Configured source does not exist: {package_path}")
        for skill_dir in discover_leaf_skills(package_path):
            name = skill_name(skill_dir)
            sources.append(
                SkillSource(
                    name=name,
                    source_dir=skill_dir,
                    package=package_path.name,
                    relative_source=skill_dir.relative_to(skills_root(root)).as_posix(),
                )
            )
    names = [source.name for source in sources]
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        raise RuntimeError(f"Duplicate skill names would collide: {', '.join(duplicates)}")
    return sorted(sources, key=lambda item: item.name)


def discover_openai_sources(root: Path) -> list[SkillSource]:
    """Discover the fixed OpenAI skill set from the maintained plugin."""
    plugin_skills = root / PLUGIN_VARIANTS["openai"] / "skills"
    if not plugin_skills.exists():
        raise FileNotFoundError(f"OpenAI plugin skills directory does not exist: {plugin_skills}")
    sources: list[SkillSource] = []
    for skill_dir in discover_leaf_skills(plugin_skills):
        relative = skill_dir.relative_to(plugin_skills)
        sources.append(
            SkillSource(
                name=skill_name(skill_dir),
                source_dir=skill_dir,
                package=relative.parts[0],
                relative_source=relative.as_posix(),
            )
        )
    names = [source.name for source in sources]
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        raise RuntimeError(f"Duplicate OpenAI skill names: {', '.join(duplicates)}")
    registry_path = root / PLUGIN_VARIANTS["openai"] / "workflow-registry.yaml"
    if registry_path.is_file():
        registry = yaml.safe_load(read_text(registry_path)) or {}
        registry_names = {
            str(entry.get("name", ""))
            for entry in registry.get("skills", [])
            if entry.get("name")
        }
        if set(names) != registry_names:
            raise RuntimeError(
                "OpenAI plugin discovery differs from registry: "
                f"missing={sorted(registry_names - set(names))} "
                f"extra={sorted(set(names) - registry_names)}"
            )
    if not sources:
        raise RuntimeError("OpenAI plugin contains no skills")
    return sorted(sources, key=lambda item: item.name)


def plugin_manifest(plugin_name: str) -> dict[str, object]:
    display_name = "Hermes Research Skills" if plugin_name == "skills-openai-plugin" else "Hermes Research Skills Flat"
    description = (
        "Research idea, proposal, article, perspective, evidence mapping, and methodology skills converted "
        "from my-hermes-skills."
    )
    return {
        "name": plugin_name,
        "version": "1.0.0",
        "description": description,
        "author": {"name": "Xuxu Wei"},
        "license": "MIT",
        "keywords": [
            "research",
            "research-idea",
            "research-proposal",
            "research-perspective",
            "academic-workflow",
            "codex-skills",
        ],
        "skills": "./skills/",
        "interface": {
            "displayName": display_name,
            "shortDescription": "Research workflow skills converted from my-hermes-skills",
            "longDescription": (
                "A local Codex plugin containing the research-idea, research-proposal, "
                "research-article, and research-perspective workflows plus the research support skills they reference "
                "for evidence mapping, literature lookup, and methodology/statistics preflight."
            ),
            "developerName": "Xuxu Wei",
            "category": MARKETPLACE_CATEGORY,
            "capabilities": ["Interactive", "Read", "Write"],
            "defaultPrompt": [
                "Run the research idea to proposal workflow.",
                "Evaluate and refine a research proposal.",
                "Draft a research perspective with evidence checks.",
            ],
            "brandColor": "#0F766E",
            "screenshots": [],
        },
    }


def dependency_package_list() -> str:
    lines = [f"- `research/{name}`" for name in RESEARCH_DEPENDENCIES]
    lines.extend(f"- `obsidian-skills/{name}`" for name in OBSIDIAN_DEPENDENCIES)
    lines.extend(f"- `productivity/{name}`" for name in PRODUCTIVITY_DEPENDENCIES)
    return "\n".join(lines)


def plugin_readme(plugin_name: str, sources: list[SkillSource]) -> str:
    skill_list = "\n".join(f"- `{source.name}` from `skills/{source.relative_source}`" for source in sources)
    marketplace_entry = {
        "name": plugin_name,
        "source": {"source": "local", "path": f"./plugins/{plugin_name}"},
        "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
        "category": MARKETPLACE_CATEGORY,
    }
    return f"""# {plugin_name}

This plugin is generated from `my-hermes-skills`.

## Layout

This is the Codex plugin variant. It preserves the original recursive package layout under `skills/`.

The generated plugin includes the core workflow packages plus external research skills that those workflows reference:

- `research-idea`
- `research-proposal`
- `research-article`
- `research-perspective`
{dependency_package_list()}

## Included Skills

{skill_list}

## Third-party Notices

The generated plugin includes `obsidian-markdown` derived from
`kepano/obsidian-skills` by Steph Ango (@kepano), MIT License. The notice is
copied to `skills/obsidian-skills/NOTICE.md`.

## Regenerate And Install

From the repository root:

```powershell
python install_codex_plugin.py
```

That command rebuilds this plugin from the current `skills/` tree, validates it, installs it to:

```text
%USERPROFILE%\\plugins\\{plugin_name}
```

and updates:

```text
%USERPROFILE%\\.agents\\plugins\\marketplace.json
```

## Manual Marketplace Entry

If you want to register this plugin by hand, add this entry to `~/.agents/plugins/marketplace.json`:

```json
{json.dumps(marketplace_entry, indent=2, ensure_ascii=False)}
```

The marketplace file should have a top-level shape like:

```json
{{
  "name": "local",
  "interface": {{
    "displayName": "Local Plugins"
  }},
  "plugins": []
}}
```

## Notes

The installer is idempotent. Re-running it replaces the local plugin directory with content regenerated from the current repository state and replaces the matching marketplace entry.
"""


def flat_readme(sources: list[SkillSource]) -> str:
    skill_list = "\n".join(f"- `{source.name}` from `skills/{source.relative_source}`" for source in sources)
    return f"""# skills-flatten

This directory is generated from `my-hermes-skills` for agent systems that expect a flat skills directory.

## Layout

Each direct child directory is one skill directory containing `SKILL.md`.

Copy the contents of this directory into the target agent's skills folder, or point the agent at this directory if it supports a custom skills root.

## Included Source Packages

- `research-idea`
- `research-proposal`
- `research-article`
- `research-perspective`
{dependency_package_list()}

## Included Skills

{skill_list}

## Third-party Notices

`obsidian-markdown` is derived from `kepano/obsidian-skills` by Steph Ango
(@kepano), MIT License. The notice is copied to `_notices/`.

## Regenerate

From the repository root:

```powershell
python generate_flatten_skills.py
```

This command only regenerates `skills-flatten`. It does not install or register a Codex plugin.
"""


def dependency_report(sources: list[SkillSource]) -> str:
    included = {source.name for source in sources}
    included_aliases = included | {source.source_dir.name for source in sources}
    related: dict[str, set[str]] = {}
    skill_view_refs: dict[str, set[str]] = {}
    for source in sources:
        text = read_text(source.source_dir / "SKILL.md")
        related[source.name] = extract_related_skills(text)
        for match in re.finditer(r"skill_view\(name=[\"']([^\"']+)[\"']", text):
            skill_view_refs.setdefault(source.name, set()).add(match.group(1))
        for ref_file in source.source_dir.rglob("*.md"):
            ref_text = read_text(ref_file)
            for match in re.finditer(r"skill_view\(name=[\"']([^\"']+)[\"']", ref_text):
                skill_view_refs.setdefault(source.name, set()).add(match.group(1))

    unresolved_related = {
        name: sorted(refs - included_aliases)
        for name, refs in related.items()
        if refs - included_aliases
    }
    unresolved_skill_view = {
        name: sorted(refs - included_aliases)
        for name, refs in skill_view_refs.items()
        if refs - included_aliases
    }

    lines = [
        "# Dependency Report",
        "",
        f"Included skills: {len(included)}",
        "",
        "## Included Skill Names",
        "",
        *[f"- `{name}`" for name in sorted(included)],
        "",
        "## Unresolved `related_skills` Mentions",
        "",
    ]
    if unresolved_related:
        for name, refs in sorted(unresolved_related.items()):
            lines.append(f"- `{name}`: {', '.join(f'`{ref}`' for ref in refs)}")
    else:
        lines.append("- None")

    lines.extend(["", "## Unresolved `skill_view(...)` Mentions", ""])
    if unresolved_skill_view:
        for name, refs in sorted(unresolved_skill_view.items()):
            lines.append(f"- `{name}`: {', '.join(f'`{ref}`' for ref in refs)}")
    else:
        lines.append("- None")
    lines.append("")
    return "\n".join(lines)


def build_codex_plugin(root: Path, sources: list[SkillSource]) -> Path:
    plugin_name = PLUGIN_VARIANTS["openai"]
    target = root / plugin_name
    if not (target / ".codex-plugin" / "plugin.json").exists():
        raise FileNotFoundError(f"Maintained OpenAI plugin manifest is missing: {target}")
    return target


def build_flatten_skills(root: Path, sources: list[SkillSource]) -> Path:
    target = root / FLATTEN_DIR
    safe_replace_dir(target, root, [FLATTEN_DIR])

    for source in sources:
        copy_dir(source.source_dir, target / source.name)
    obsidian_notice = skills_root(root) / "obsidian-skills" / "NOTICE.md"
    if obsidian_notice.exists():
        copy_file(obsidian_notice, target / "_notices" / "obsidian-skills-NOTICE.md")

    # Preserve package-level helper scripts that are not inside leaf skill dirs.
    support_root = target / "_support" / "package-scripts"
    for package in ["research-proposal", "research-perspective"]:
        scripts_dir = skills_root(root) / package / "scripts"
        if scripts_dir.exists():
            copy_dir(scripts_dir, support_root / package / "scripts")

    write_text(target / "README.md", flat_readme(sources))
    write_text(target / "_reports" / "dependency-report.md", dependency_report(sources))
    return target


def skill_root_names(skill_root: Path) -> dict[str, str]:
    skills: dict[str, str] = {}
    for skill_md in sorted(skill_root.rglob("SKILL.md")):
        name = skill_name(skill_md.parent)
        rel = skill_md.parent.relative_to(skill_root).as_posix()
        if name in skills:
            raise RuntimeError(f"{skill_root.name}: duplicate skill name {name}: {skills[name]} and {rel}")
        skills[name] = rel
    return skills


def plugin_skill_names(plugin_dir: Path) -> dict[str, str]:
    return skill_root_names(plugin_dir / "skills")


def validate_plugin(plugin_dir: Path, expected_names: set[str]) -> dict[str, object]:
    manifest_path = plugin_dir / ".codex-plugin" / "plugin.json"
    manifest = json.loads(read_text(manifest_path))
    names = plugin_skill_names(plugin_dir)
    missing = sorted(expected_names - set(names))
    extra = sorted(set(names) - expected_names)
    errors: list[str] = []
    if manifest.get("name") != plugin_dir.name:
        errors.append(f"plugin.json name does not match folder name: {manifest.get('name')} != {plugin_dir.name}")
    if manifest.get("skills") != "./skills/":
        errors.append('plugin.json skills must be "./skills/"')
    if missing:
        errors.append(f"missing skills: {', '.join(missing)}")
    if extra:
        errors.append(f"extra skills: {', '.join(extra)}")
    nested = sorted(rel for rel in names.values() if "/" in rel)
    if nested:
        errors.append(f"plugin skills must be direct children of skills/: {', '.join(nested[:10])}")
    return {
        "plugin": plugin_dir.name,
        "plugin_version": manifest.get("version"),
        "ok": not errors,
        "errors": errors,
        "skill_count": len(names),
        "skills": names,
    }


def validate_flatten(flatten_dir: Path, expected_names: set[str]) -> dict[str, object]:
    names = {
        name: rel
        for name, rel in skill_root_names(flatten_dir).items()
        if not rel.startswith("_support/")
    }
    missing = sorted(expected_names - set(names))
    extra = sorted(set(names) - expected_names)
    errors: list[str] = []
    nested = sorted(rel for rel in names.values() if "/" in rel)
    if missing:
        errors.append(f"missing skills: {', '.join(missing)}")
    if extra:
        errors.append(f"extra skills: {', '.join(extra)}")
    if nested:
        errors.append(f"non-flat skill paths: {', '.join(nested[:10])}")
    return {
        "directory": flatten_dir.name,
        "ok": not errors,
        "errors": errors,
        "skill_count": len(names),
        "skills": names,
    }


def validate_variants(root: Path, plugin_dirs: list[Path], sources: list[SkillSource]) -> dict[str, object]:
    expected_names = {source.name for source in sources}
    results = [validate_plugin(plugin_dir, expected_names) for plugin_dir in plugin_dirs]
    skill_sets = [set(result["skills"].keys()) for result in results]  # type: ignore[index, union-attr]
    consistent = all(skill_set == skill_sets[0] for skill_set in skill_sets)
    report = {
        "ok": all(bool(result["ok"]) for result in results) and consistent,
        "consistent_skill_sets": consistent,
        "expected_skill_count": len(expected_names),
        "plugins": results,
    }
    for plugin_dir in plugin_dirs:
        write_text(plugin_dir / "reports" / "validation.json", json.dumps(report, indent=2, ensure_ascii=False))
    warning = try_write_text(root / "plugin-validation.json", json.dumps(report, indent=2, ensure_ascii=False))
    if warning:
        report.setdefault("warnings", []).append(warning)  # type: ignore[union-attr]
    return report


def validate_codex_plugin(root: Path, plugin_dir: Path, sources: list[SkillSource]) -> dict[str, object]:
    expected_names = {source.name for source in sources}
    result = validate_plugin(plugin_dir, expected_names)
    registry = yaml.safe_load(read_text(plugin_dir / "workflow-registry.yaml"))
    report = {
        "ok": bool(result["ok"]),
        "expected_skill_count": len(expected_names),
        "plugin_version": result["plugin_version"],
        "registry_schema_version": registry.get("schema_version"),
        "plugin": result,
    }
    write_text(plugin_dir / "reports" / "validation.json", json.dumps(report, indent=2, ensure_ascii=False))
    warning = try_write_text(root / "codex-plugin-validation.json", json.dumps(report, indent=2, ensure_ascii=False))
    if warning:
        report.setdefault("warnings", []).append(warning)  # type: ignore[union-attr]
    return report


def validate_flatten_output(root: Path, flatten_dir: Path, sources: list[SkillSource]) -> dict[str, object]:
    expected_names = {source.name for source in sources}
    result = validate_flatten(flatten_dir, expected_names)
    report = {"ok": bool(result["ok"]), "expected_skill_count": len(expected_names), "flatten": result}
    write_text(flatten_dir / "_reports" / "validation.json", json.dumps(report, indent=2, ensure_ascii=False))
    warning = try_write_text(root / "flatten-validation.json", json.dumps(report, indent=2, ensure_ascii=False))
    if warning:
        report.setdefault("warnings", []).append(warning)  # type: ignore[union-attr]
    return report


def marketplace_entry(plugin_name: str) -> dict[str, object]:
    return {
        "name": plugin_name,
        "source": {"source": "local", "path": f"./plugins/{plugin_name}"},
        "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
        "category": MARKETPLACE_CATEGORY,
    }


def update_marketplace(marketplace_path: Path, plugin_names: list[str], remove_plugin_names: Iterable[str] = ()) -> None:
    if marketplace_path.exists():
        data = json.loads(read_text(marketplace_path))
    else:
        data = {"name": "local", "interface": {"displayName": "Local Plugins"}, "plugins": []}

    data.setdefault("name", "local")
    data.setdefault("interface", {}).setdefault("displayName", "Local Plugins")
    plugins = data.setdefault("plugins", [])
    if not isinstance(plugins, list):
        raise RuntimeError(f"marketplace plugins field is not a list: {marketplace_path}")

    remove = set(remove_plugin_names)
    plugins[:] = [entry for entry in plugins if not (isinstance(entry, dict) and entry.get("name") in remove)]
    by_name = {entry.get("name"): index for index, entry in enumerate(plugins) if isinstance(entry, dict)}
    for plugin_name in plugin_names:
        entry = marketplace_entry(plugin_name)
        if plugin_name in by_name:
            plugins[by_name[plugin_name]] = entry
        else:
            plugins.append(entry)

    write_text(marketplace_path, json.dumps(data, indent=2, ensure_ascii=False))


def windows_extended_path(path: Path) -> str:
    resolved = str(path.resolve())
    if resolved.startswith("\\\\?\\"):
        return resolved
    return "\\\\?\\" + resolved


def toml_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def replace_or_append_section(config: str, section_name: str, body: str) -> str:
    header = f"[{section_name}]"
    pattern = re.compile(
        rf"(?ms)^\[{re.escape(section_name)}\]\r?\n.*?(?=^\[|\Z)"
    )
    replacement = f"{header}\n{body.rstrip()}\n"
    if pattern.search(config):
        return pattern.sub(lambda _match: replacement, config)
    if config and not config.endswith("\n"):
        config += "\n"
    return config + "\n" + replacement


def update_codex_config(config_path: Path, marketplace_root: Path, plugin_names: list[str]) -> None:
    if config_path.exists():
        config = read_text(config_path)
    else:
        config = ""

    marketplace_body = "\n".join(
        [
            f'last_updated = "{datetime.datetime.utcnow().replace(microsecond=0).isoformat()}Z"',
            'source_type = "local"',
            f"source = {toml_quote(windows_extended_path(marketplace_root))}",
        ]
    )
    config = replace_or_append_section(config, "marketplaces.local", marketplace_body)

    for plugin_name in plugin_names:
        section = f'plugins."{plugin_name}@local"'
        config = replace_or_append_section(config, section, "enabled = true")

    write_text(config_path, config)


def remove_codex_plugin_entries(config_path: Path, plugin_names: Iterable[str], marketplace_name: str = "local") -> None:
    if not config_path.exists():
        return
    config = read_text(config_path)
    for plugin_name in plugin_names:
        section = f'plugins."{plugin_name}@{marketplace_name}"'
        pattern = re.compile(rf"(?ms)^\[{re.escape(section)}\]\r?\n.*?(?=^\[|\Z)")
        config = pattern.sub("", config)
    write_text(config_path, config)


def install_plugins(root: Path, plugin_names: list[str], remove_plugin_names: Iterable[str] = ()) -> None:
    home = Path.home()
    local_plugins = home / "plugins"
    local_plugins.mkdir(parents=True, exist_ok=True)

    for plugin_name in plugin_names:
        src = root / plugin_name
        if not src.exists():
            raise FileNotFoundError(f"Build plugin first: {src}")
        dst = local_plugins / plugin_name
        safe_replace_dir(dst, local_plugins, plugin_names)
        copy_dir(src, dst)

    update_marketplace(home / ".agents" / "plugins" / "marketplace.json", plugin_names, remove_plugin_names)
    update_codex_config(home / ".codex" / "config.toml", home, plugin_names)
    remove_codex_plugin_entries(home / ".codex" / "config.toml", remove_plugin_names)


def build(root: Path) -> tuple[list[Path], list[SkillSource], dict[str, object]]:
    sources = discover_openai_sources(root)
    plugin_dirs = [
        build_codex_plugin(root, sources),
    ]
    report = validate_codex_plugin(root, plugin_dirs[0], sources)
    return plugin_dirs, sources, report


def build_flatten(root: Path) -> tuple[Path, list[SkillSource], dict[str, object]]:
    sources = discover_openai_sources(root)
    flatten_dir = build_flatten_skills(root, sources)
    report = validate_flatten_output(root, flatten_dir, sources)
    return flatten_dir, sources, report


def build_codex(root: Path) -> tuple[Path, list[SkillSource], dict[str, object]]:
    sources = discover_openai_sources(root)
    plugin_dir = build_codex_plugin(root, sources)
    report = validate_codex_plugin(root, plugin_dir, sources)
    return plugin_dir, sources, report


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate/install the maintained OpenAI preview plugin or build a flat export.")
    parser.add_argument("--mode", choices=["codex", "flatten", "both"], default="both")
    parser.add_argument("--install", action="store_true", help="Install/register the Codex plugin. Ignored for flatten mode.")
    parser.add_argument("--fail-on-invalid", action="store_true")
    args = parser.parse_args()

    root = repo_root()
    reports: list[dict[str, object]] = []
    plugin_dir: Path | None = None
    flatten_dir: Path | None = None

    if args.mode in {"codex", "both"}:
        plugin_dir, _sources, report = build_codex(root)
        reports.append(report)
    if args.mode in {"flatten", "both"}:
        flatten_dir, _sources, report = build_flatten(root)
        reports.append(report)

    ok = all(bool(report["ok"]) for report in reports)

    print(json.dumps({
        "ok": ok,
        "codex_plugin": str(plugin_dir) if plugin_dir else None,
        "flatten_skills": str(flatten_dir) if flatten_dir else None,
        "reports": reports,
    }, indent=2, ensure_ascii=False))

    if not ok:
        if args.fail_on_invalid:
            return 1
        return 0

    if args.install and plugin_dir:
        legacy_plugins = [LEGACY_FLATTEN_PLUGIN, LEGACY_OPENAI_PLUGIN]
        install_plugins(root, [plugin_dir.name], remove_plugin_names=legacy_plugins)
        print(json.dumps({
            "installed": [plugin_dir.name],
            "removed_legacy_plugin_entries": legacy_plugins,
            "plugins_dir": str(Path.home() / "plugins"),
            "marketplace": str(Path.home() / ".agents" / "plugins" / "marketplace.json"),
        }, indent=2, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
