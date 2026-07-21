#!/usr/bin/env python3
"""Check the v0.12.0 retrieval-skill rename is closed in active OpenAI source."""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml


REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "research-skills-openai"
SKILLS = PLUGIN / "skills"
LEGACY_SKILL_NAME_ALIASES = {
    "academic-deep-search": "focused-literature-synthesizer",
    "research-opportunity-mapper": "research-landscape-mapper",
}
LEGACY_ARTIFACT_ROLE_ALIASES = {"focused_academic_synthesis": "focused_literature_synthesis"}
ACTIVE_SCRIPTS = (
    "audit_openai_research_plugin.py",
    "normalize_openai_skills.py",
    "validate_openai_personal_readiness.py",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_yaml(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"expected mapping: {path}")
    return value


def without_mapping_block(text: str, variable: str) -> str:
    pattern = rf"{variable}\s*=\s*\{{.*?^\}}"
    match = re.search(pattern, text, re.M | re.S)
    require(match is not None, f"legacy mapping block missing: {variable}")
    return text[: match.start()] + text[match.end() :]


def main() -> int:
    registry = load_yaml(PLUGIN / "workflow-registry.yaml")
    manifest = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    require(manifest["version"] == registry["plugin_version"] == "0.13.0-preview.1", "version mismatch")

    skill_dirs = sorted(path for path in SKILLS.iterdir() if path.is_dir())
    require(len(skill_dirs) == 51, f"expected 51 skills, found {len(skill_dirs)}")
    for old, new in LEGACY_SKILL_NAME_ALIASES.items():
        require(not (SKILLS / old).exists(), f"legacy skill directory remains: {old}")
        require((SKILLS / new).is_dir(), f"renamed skill missing: {new}")

    active_skill_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in SKILLS.rglob("*")
        if path.is_file() and path.suffix in {".md", ".yaml", ".json", ".py"}
    )
    for old in (*LEGACY_SKILL_NAME_ALIASES, *LEGACY_ARTIFACT_ROLE_ALIASES):
        require(old not in active_skill_text, f"legacy name remains under active skills: {old}")

    for name in LEGACY_SKILL_NAME_ALIASES.values():
        folder = SKILLS / name
        skill = (folder / "SKILL.md").read_text(encoding="utf-8")
        match = re.search(r"^name:\s*([^\s]+)$", skill, re.M)
        require(match is not None and match.group(1) == name, f"frontmatter mismatch: {name}")
        agent = load_yaml(folder / "agents" / "openai.yaml")
        require(f"${name}" in agent["interface"]["default_prompt"], f"agent prompt mismatch: {name}")
        meta = folder / "_meta.json"
        if meta.exists():
            require(json.loads(meta.read_text(encoding="utf-8"))["slug"] == name, f"meta mismatch: {name}")

    for filename in ("README.md", ".codex-plugin/plugin.json"):
        text = (PLUGIN / filename).read_text(encoding="utf-8")
        for old in (*LEGACY_SKILL_NAME_ALIASES, *LEGACY_ARTIFACT_ROLE_ALIASES):
            require(old not in text, f"legacy name remains in {filename}: {old}")
    for filename in ACTIVE_SCRIPTS:
        text = (REPO / "scripts" / filename).read_text(encoding="utf-8")
        for old in (*LEGACY_SKILL_NAME_ALIASES, *LEGACY_ARTIFACT_ROLE_ALIASES):
            require(old not in text, f"legacy name remains in {filename}: {old}")

    converter = (REPO / "scripts" / "codex_plugin_converter.py").read_text(encoding="utf-8")
    for old in LEGACY_SKILL_NAME_ALIASES:
        require(old not in converter, f"legacy name remains in converter: {old}")

    generator = (REPO / "scripts" / "generate_openai_workflow_registry.py").read_text(encoding="utf-8")
    generator = without_mapping_block(generator, "LEGACY_SKILL_NAME_ALIASES")
    generator = without_mapping_block(generator, "LEGACY_ARTIFACT_ROLE_ALIASES")
    for old in (*LEGACY_SKILL_NAME_ALIASES, *LEGACY_ARTIFACT_ROLE_ALIASES):
        require(old not in generator, f"legacy name escaped generator alias map: {old}")

    require(registry.get("legacy_skill_name_aliases") == LEGACY_SKILL_NAME_ALIASES, "skill alias map mismatch")
    require(registry.get("legacy_artifact_role_aliases") == LEGACY_ARTIFACT_ROLE_ALIASES, "artifact alias map mismatch")
    current_names = {item["name"] for item in registry["skills"]}
    require(set(LEGACY_SKILL_NAME_ALIASES.values()) <= current_names, "new names missing from registry")
    require(not set(LEGACY_SKILL_NAME_ALIASES) & current_names, "legacy names exposed by registry")
    require(len(registry["public_entry_policy"]["declared_entries"]) == 7, "public entry count changed")
    require(len(registry["public_entry_policy"]["implicit_active_entries"]) == 6, "implicit entry count changed")

    mapper = SKILLS / "research-landscape-mapper"
    routing = (mapper / "references" / "search-routing-rules.md").read_text(encoding="utf-8")
    for marker in (
        "evidence_change_assessment",
        "materiality: none | bounded | major",
        "reuse_existing_evidence | built_in_search | focused_literature_synthesizer | research_landscape_mapper",
        "Do not chain",
    ):
        require(marker in routing, f"routing contract missing: {marker}")

    citations = (mapper / "references" / "citation-record-contract.md").read_text(encoding="utf-8")
    for marker in (
        "citation_gbt7714_2015",
        "canonical_url",
        "inferred_unique_match",
        "inferred_series_match",
        "ambiguous_candidates",
        "verification_status",
    ):
        require(marker in citations, f"citation contract missing: {marker}")

    deep_rules = (mapper / "references" / "deep-research-prompt-rules.md").read_text(encoding="utf-8")
    for marker in (
        "deep-research-request-vNNN.md",
        "deep-research-follow-up-guide-vNNN.md",
        "deep-research-report-vNNN.md",
        "novelty_evidence_usable",
    ):
        require(marker in deep_rules, f"Deep Research contract missing: {marker}")

    edges = registry["workflow_edges"]
    for workflow in ("idea", "proposal", "article", "perspective", "research_polisher"):
        destinations = {
            edge["destination"] for edge in edges if edge.get("workflow") == workflow
        }
        require("research-landscape-mapper" in destinations, f"major route missing: {workflow}")
        require("focused-literature-synthesizer" in destinations, f"bounded route missing: {workflow}")

    for markdown in SKILLS.rglob("*.md"):
        text = markdown.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            target = target.split("#", 1)[0]
            if not target or "://" in target or not target.startswith(("./", "../")):
                continue
            require((markdown.parent / target).resolve().exists(), f"broken relative link: {markdown} -> {target}")

    print("OpenAI skill rename closure passed: 51 skills, 7 entries, 6 implicit entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
