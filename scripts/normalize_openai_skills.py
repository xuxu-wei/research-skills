#!/usr/bin/env python3
"""Normalize the ChatGPT/Codex plugin skills without touching Hermes sources.

The OpenAI plugin intentionally keeps only ``name`` and ``description`` in
SKILL.md frontmatter. Product-facing metadata and invocation policy live in
``agents/openai.yaml``.
"""

from __future__ import annotations

import re
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO / "research-skills-openai" / "skills"

IMPLICIT_SKILLS = {
    "research-idea-orchestrator",
    "proposal-orchestrator",
    "article-orchestrator",
    "perspective-orchestrator",
    "research-opportunity-mapper",
    "academic-deep-search",
}

DESCRIPTIONS = {
    "academic-deep-search": "Answer a narrow academic question by finding and carefully reading 2-5 papers. Use for specific method, marker, finding, or representative-figure questions; route broader synthesis to research-opportunity-mapper.",
    "academic-language-assessor": "Independently assess English, Chinese, or bilingual academic language. Use for manuscripts, proposals, perspectives, portfolios, or handoffs that need locatable language findings without rewriting.",
    "article-architect": "Design a manuscript blueprint, claim-evidence structure, evidence displays, supplementary plan, results skeleton, journal adapter, and reviewer-risk preview before drafting.",
    "article-claim-auditor": "Independently audit manuscript claims against frozen evidence. Use to identify unsupported inference, overclaiming, wording mismatch, and required downscaling without editing the manuscript.",
    "article-context-builder": "Normalize research inputs into an article context brief, classify study/article type, select reporting standards, and gate missing information before architecture or drafting.",
    "article-cover-letter": "Draft a journal cover letter and quality-check artifact from frozen manuscript materials. Use after manuscript evaluation without changing manuscript or frontmatter source files.",
    "article-drafter": "Draft or revise a versioned manuscript body and organize supplements from approved context, blueprint, evidence, audit findings, and revision plans without self-evaluation.",
    "article-evaluator": "Independently evaluate a frozen manuscript with non-compensatory scientific, evidence-claim, reporting, language, and submission-readiness gates; do not edit source text.",
    "article-frontmatter-drafter": "Draft versioned article frontmatter—abstract, key points, titles, running title, highlights, and graphical-abstract text—from an evaluated manuscript and blueprint.",
    "article-literature-grounder": "Build an auditable literature-grounding report for an article, covering search scope, novelty position, competing evidence, coverage limits, and citation risk.",
    "article-methods-statistics-auditor": "Independently audit study design, methods, endpoints, and statistics before manuscript drafting; identify reanalysis needs or methodological blocks without rewriting.",
    "article-orchestrator": "Orchestrate article drafting, independent review, revision, and human-review packaging. Use for full, draft fast-track, blueprint, section, or submission-only manuscript workflows.",
    "article-readiness-triage": "Independently determine whether study materials can enter article workflow, identify article type and blocking gaps, and recommend a route without drafting content.",
    "article-refinement-controller": "Plan and control targeted manuscript revision after independent review, route edits to the drafter, maintain lineage, and require fresh re-evaluation.",
    "article-review-panel": "Define isolated role-specific peer review for a frozen manuscript and non-compensatory aggregation rules that preserve fatal findings, conflict, and dissent.",
    "article-submission-compositor": "Independently assemble and verify a research-article submission package for human sign-off. Use after the final manuscript version has qualifying audits, evaluation, and required panel outputs.",
    "idea-adversarial-review-panel": "Independently challenge promoted research ideas through novelty/gap, feasibility/method, and PI-strategy roles before proposal handoff; preserve dissent and do not rescore ideas.",
    "idea-evaluator": "Independently score and gate frozen research ideas for novelty, feasibility, impact, relevance, clarity, and completion; recommend promotion, revision, merge, backup, or rejection.",
    "idea-portfolio-assembler": "Assemble evaluated research ideas into a PI-review portfolio with rankings, lineage, limitations, dissent, and proposal-handoff status without rescoring or rewriting candidates.",
    "medical-journal-review": "Independently review a medical study, protocol, manuscript, or cover letter from an editorial, methodological, statistical, claim, and journal-fit perspective without drafting.",
    "methodology-statistics-preflight": "Independently preflight research designs, ideas, proposals, protocols, or analysis plans for endpoint clarity, data-method fit, feasibility blockers, and minimal repair routes.",
    "multi-path-idea-generator": "Generate a diverse, non-duplicative set of research ideas from approved context and opportunity maps using selected generation paths; do not evaluate or rank candidates.",
    "perspective-argument-architect": "Design a contestable Perspective argument chain, contribution type, narrative strategy, paragraph plan, and claim mapping before drafting; do not write prose.",
    "perspective-claim-evidence-curator": "Create and maintain the Perspective claim ledger, claim-evidence matrix, discourse baseline, contrary-evidence log, citation risks, and approved claim changes.",
    "perspective-drafter": "Draft or revise a versioned Perspective from approved architecture and claim artifacts, with paragraph mapping and separate reviewer responses; do not self-evaluate.",
    "perspective-evaluator": "Independently evaluate a frozen Perspective across argument, evidence, contribution, narrative, claim discipline, language, and outlet-fit gates without editing source text.",
    "perspective-final-compositor": "Independently assemble and verify a text-identical Perspective delivery package for human review. Use only after the frozen source has qualifying current-version evaluation and panel outputs.",
    "perspective-input-builder": "Normalize a Perspective thesis, audience, outlet, evidence, and constraints into an input brief and outlet profile; use before claim curation and architecture.",
    "perspective-orchestrator": "Orchestrate Perspective, Viewpoint, or Commentary writing from thesis and evidence through independent evaluation, revision, panel review, and final human-review delivery.",
    "perspective-refinement-controller": "Plan and control targeted Perspective revision after independent evaluation, route writing to the drafter, preserve lineage, and require fresh re-evaluation.",
    "perspective-review-panel": "Independently review a frozen Perspective from one assigned counter-position, evidence, narrative, methodology, clinician, or outlet-fit role without peer-output access.",
    "proposal-context-brief-builder": "Normalize an idea, promoted package, draft, funding call, or data opportunity into a concise proposal context brief with constraints and unresolved facts.",
    "proposal-drafter": "Draft or revise a versioned research proposal from an approved context, evidence set, structure, and revision plan. Use after proposal readiness triage.",
    "proposal-evaluator": "Independently evaluate a frozen proposal for significance, logic, evidence, methods, feasibility, completion, and reviewer defensibility without rewriting it.",
    "proposal-orchestrator": "Orchestrate proposal drafting, independent evaluation, revision, optional SAP, panel review, and human-review packaging. Use from an idea, funding call, data opportunity, or existing proposal.",
    "proposal-package-assembler": "Assemble evaluated proposal, state, review, revision, panel, unresolved-issue, and optional SAP artifacts into a human-review package without rewriting or rescoring.",
    "proposal-readiness-triage": "Independently determine whether a research idea can enter proposal drafting, identify blocking gaps, and route clarification, idea refinement, or methods preflight.",
    "proposal-refinement-controller": "Plan and control targeted proposal revision after independent evaluation. Use to route fixes to the drafter, preserve version lineage, and require fresh re-evaluation.",
    "proposal-review-panel": "Independently review a frozen proposal from one assigned panel role. Use after proposal evaluation passes or for an explicitly requested early mock/internal advisory review.",
    "research-context-builder": "Normalize a rough research direction, practical problem, evidence set, funding call, or data asset into a structured context brief for idea generation.",
    "research-idea-orchestrator": "Orchestrate research idea development from a rough topic, evidence, funding call, practical problem, or data asset into an independently evaluated and ranked PI-review portfolio.",
    "research-opportunity-mapper": "Build source-grounded evidence and opportunity maps. Use for broad literature retrieval, claim verification, novelty positioning, evidence limitations, and research-gap mapping.",
    "sap-evaluator": "Independently evaluate a frozen Statistical Analysis Plan for endpoint alignment, data-method fit, feasibility, rigor, missing data, sensitivity analysis, and reproducibility.",
    "sap-refinement-controller": "Plan and control targeted Statistical Analysis Plan revision after independent evaluation, route writing to sap-writer, preserve lineage, and require fresh re-evaluation.",
    "sap-writer": "Draft or revise a versioned Statistical Analysis Plan from approved endpoints, design, data structure, methodology preflight, and revision instructions without self-evaluation.",
}


def split_frontmatter(text: str) -> tuple[list[str], str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md does not start with YAML frontmatter")
    end = text.find("\n---", 4)
    if end < 0:
        raise ValueError("SKILL.md frontmatter is not closed")
    frontmatter = text[4:end].splitlines()
    body = text[end + 4 :].lstrip("\n")
    return frontmatter, body


def field_block(lines: list[str], field: str) -> list[str]:
    prefix = f"{field}:"
    for index, line in enumerate(lines):
        if not line.startswith(prefix):
            continue
        block = [line]
        value = line[len(prefix) :].strip()
        if value in {"|", ">", "|-", ">-", "|+", ">+"}:
            for child in lines[index + 1 :]:
                if child.startswith((" ", "\t")) or not child.strip():
                    block.append(child)
                else:
                    break
        return block
    raise ValueError(f"Missing required frontmatter field: {field}")


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def description_text(block: list[str]) -> str:
    first = block[0].split(":", 1)[1].strip()
    if first in {"|", ">", "|-", ">-", "|+", ">+"}:
        return " ".join(line.strip() for line in block[1:] if line.strip())
    return unquote(first)


def yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def display_name(name: str) -> str:
    return " ".join(part.capitalize() for part in name.split("-"))


def short_description(description: str) -> str:
    compact = re.sub(r"\s+", " ", description).strip()
    first = re.split(r"(?<=[.!?。！？])\s+", compact, maxsplit=1)[0]
    if len(first) <= 100:
        return first
    candidate = first[:97]
    if " " in candidate:
        candidate = candidate.rsplit(" ", 1)[0]
    return candidate.rstrip(" ,.;:-") + "..."


def default_prompt(name: str) -> str:
    return f"Use ${name} for this task and follow its workflow and output contract."


def normalize_skill(skill_md: Path) -> None:
    text = skill_md.read_text(encoding="utf-8-sig")
    frontmatter, body = split_frontmatter(text)
    name_block = field_block(frontmatter, "name")
    description_block = field_block(frontmatter, "description")
    name = unquote(name_block[0].split(":", 1)[1])
    if name != skill_md.parent.name:
        raise ValueError(f"Skill name does not match directory: {name} != {skill_md.parent.name}")

    description = DESCRIPTIONS.get(name, description_text(description_block))
    normalized_frontmatter = [
        "---",
        f"name: {name}",
        f"description: {yaml_quote(description)}",
        "---",
        "",
    ]
    skill_md.write_text("\n".join(normalized_frontmatter) + body.rstrip() + "\n", encoding="utf-8", newline="\n")

    agent_dir = skill_md.parent / "agents"
    agent_dir.mkdir(exist_ok=True)
    openai_yaml = "\n".join(
        [
            "interface:",
            f"  display_name: {yaml_quote(display_name(name))}",
            f"  short_description: {yaml_quote(short_description(description))}",
            f"  default_prompt: {yaml_quote(default_prompt(name))}",
            "policy:",
            f"  allow_implicit_invocation: {'true' if name in IMPLICIT_SKILLS else 'false'}",
            "",
        ]
    )
    (agent_dir / "openai.yaml").write_text(openai_yaml, encoding="utf-8", newline="\n")


def main() -> int:
    skill_files = sorted(SKILLS_ROOT.rglob("SKILL.md"))
    if len(skill_files) != 45:
        raise RuntimeError(f"Expected 45 OpenAI skills, found {len(skill_files)}")
    for skill_md in skill_files:
        normalize_skill(skill_md)
    print(f"normalized {len(skill_files)} OpenAI skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
