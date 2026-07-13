#!/usr/bin/env python3
"""Normalize the ChatGPT/Codex plugin skills without touching Hermes sources.

The OpenAI plugin intentionally keeps only ``name`` and ``description`` in
SKILL.md frontmatter. Product-facing metadata and invocation policy live in
``agents/openai.yaml``.
"""

from __future__ import annotations

from pathlib import Path

from openai_ui_utils import short_description_error


REPO = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO / "research-skills-openai" / "skills"

PUBLIC_ENTRY_SKILLS = {
    "research-idea-orchestrator",
    "proposal-orchestrator",
    "article-orchestrator",
    "perspective-orchestrator",
    "research-polisher-orchestrator",
    "research-opportunity-mapper",
    "academic-deep-search",
}

# The seventh public entry is discoverable and explicitly callable in 0.7, but
# the owner-approved roadmap keeps implicit routing frozen until the Phase 7-8
# external evidence gates are complete.
IMPLICIT_SKILLS = PUBLIC_ENTRY_SKILLS - {"research-polisher-orchestrator"}

DISPLAY_NAMES = {
    "research-polisher-orchestrator": "Research Polisher",
}

DESCRIPTIONS = {
    "academic-deep-search": "Answer one bounded academic question from 2-5 closely read papers; route broader or multi-stage synthesis to research-opportunity-mapper.",
    "academic-language-assessor": "Independently assess academic language in a frozen research artifact; report locatable issues without rewriting.",
    "article-architect": "Design a pre-drafting manuscript blueprint, claim-evidence structure, displays, supplements, results skeleton, and risk plan.",
    "article-claim-auditor": "Independently audit frozen manuscript claims against evidence; report unsupported inference, overclaiming, and wording mismatch.",
    "article-context-builder": "Normalize study materials into an article context brief before readiness review, architecture, or drafting; expose missing inputs.",
    "article-cover-letter": "Draft a journal cover letter and quality check from frozen evaluated materials without altering source artifacts.",
    "article-drafter": "Draft or revise a versioned manuscript and supplements from approved context, blueprint, evidence, audits, and revision instructions.",
    "article-evaluator": "Independently evaluate a frozen manuscript against scientific, evidence-claim, reporting, language, and submission-readiness gates.",
    "article-frontmatter-drafter": "Draft versioned abstract, titles, key points, highlights, and related frontmatter from an evaluated manuscript and blueprint.",
    "article-literature-grounder": "Build an auditable literature-grounding report covering scope, novelty, competing evidence, limits, and citation risk.",
    "article-methods-statistics-auditor": "Independently audit a frozen study's design, methods, endpoints, and statistics before drafting; report reanalysis needs or blocks.",
    "article-orchestrator": "Orchestrate full, fast-track, blueprint-only, section-specific, or submission-only article workflows through review and human handoff.",
    "article-readiness-triage": "Independently triage study materials for article readiness, article type, blocking gaps, and workflow route without drafting.",
    "article-refinement-controller": "Plan reviewed manuscript revisions, route edits to the drafter, preserve lineage, and require fresh evaluation.",
    "article-review-panel": "Run one isolated article peer-review role on a frozen manuscript; preserve fatal findings, conflicts, and dissent without editing.",
    "article-submission-compositor": "Independently verify and assemble a frozen article and qualifying reviews into a package for human sign-off.",
    "idea-adversarial-review-panel": "Independently challenge a frozen promoted idea in one assigned novelty, feasibility, or strategy role before proposal handoff.",
    "idea-evaluator": "Independently score and gate frozen ideas for novelty, feasibility, impact, relevance, clarity, and completion.",
    "idea-portfolio-assembler": "Assemble evaluated ideas into a PI-review portfolio with ranking, lineage, limitations, dissent, and handoff status.",
    "medical-journal-review": "Independently review frozen medical research artifacts for editorial fit, methods, statistics, and claims.",
    "methodology-statistics-preflight": "Independently preflight a frozen research plan for endpoint, data-method, and feasibility problems.",
    "multi-path-idea-generator": "Generate a diverse, non-duplicative research-idea set from approved context and opportunity maps; do not evaluate or rank it.",
    "perspective-argument-architect": "Design a contestable Perspective argument chain, contribution, narrative, paragraph plan, and claim mapping before prose drafting.",
    "perspective-claim-evidence-curator": "Build and maintain Perspective claim, evidence, contrary-evidence, citation-risk, and approved-change artifacts before drafting.",
    "perspective-drafter": "Draft or revise a versioned Perspective from approved argument and claim artifacts, keeping reviewer responses separate.",
    "perspective-evaluator": "Independently evaluate a frozen Perspective for argument, evidence, contribution, narrative, claim discipline, and outlet fit.",
    "perspective-final-compositor": "Independently verify and assemble a text-identical Perspective package for human review from current qualifying review artifacts.",
    "perspective-input-builder": "Normalize a Perspective thesis, audience, outlet, evidence, and constraints into an input brief and target-outlet profile.",
    "perspective-orchestrator": "Orchestrate a Perspective, Viewpoint, or Commentary from thesis and evidence through review, revision, panel, and human delivery.",
    "perspective-refinement-controller": "Plan Perspective revision after independent review, route prose to the drafter, preserve lineage, and require fresh evaluation.",
    "perspective-review-panel": "Independently review a frozen Perspective from one assigned counter-position, evidence, narrative, method, or outlet role.",
    "proposal-context-brief-builder": "Normalize an idea, package, draft, funding call, or data opportunity into a proposal context brief with constraints and open facts.",
    "proposal-drafter": "Draft or revise a versioned proposal from approved context, evidence, structure, and revision instructions after readiness triage.",
    "proposal-evaluator": "Independently evaluate a frozen proposal for significance, logic, evidence, methods, feasibility, and reviewer defensibility.",
    "proposal-orchestrator": "Orchestrate an idea, call, data opportunity, or draft through proposal review, revision, optional SAP, panel, and human handoff.",
    "proposal-package-assembler": "Assemble evaluated proposal, review, revision, panel, issue, and optional SAP artifacts without rewriting.",
    "proposal-readiness-triage": "Independently triage proposal-drafting readiness, identify blockers, and route clarification, refinement, or preflight.",
    "proposal-refinement-controller": "Plan targeted proposal revision after evaluation, route fixes to the drafter, preserve lineage, and require fresh evaluation.",
    "proposal-review-panel": "Independently review a frozen proposal from one assigned panel role after evaluation or in an early advisory review.",
    "research-context-builder": "Normalize a research direction, problem, evidence set, funding call, or data asset into a structured brief for idea generation.",
    "research-idea-orchestrator": "Orchestrate a topic, evidence, call, problem, or data asset into independently evaluated ideas and a PI-review portfolio.",
    "research-opportunity-mapper": "Build source-grounded evidence and opportunity maps for broad retrieval, claim checks, novelty, evidence limits, and research gaps.",
    "research-polisher-methodology-publishability-reviewer": "Independently review a frozen impact portfolio for method rigor, claim fit, feasibility, tier validity, and publishability.",
    "research-polisher-orchestrator": "Orchestrate reviewed impact strategies for completed research. Use for reframing or bounded extensions; exclude language editing, drafting, idea generation, and general search.",
    "research-polisher-plan-assembler": "Assemble sealed Research Polisher reports into an anonymous portfolio without scoring, inventing options, or hiding dissent.",
    "research-polisher-strategy-reviewer": "Independently propose scientific, practical, or dissemination impact strategies across three effort tiers for frozen research.",
    "sap-evaluator": "Independently evaluate a frozen SAP for endpoint alignment, data-method fit, feasibility, sensitivity, and reproducibility.",
    "sap-refinement-controller": "Plan targeted SAP revision after evaluation, route writing to sap-writer, preserve lineage, and require fresh evaluation.",
    "sap-writer": "Draft or revise a versioned SAP from approved endpoints, design, data structure, preflight findings, and revision instructions.",
}

SHORT_DESCRIPTIONS = {
    "academic-deep-search": "Answer narrow academic questions from 2-5 papers",
    "academic-language-assessor": "Independently assess academic language and report issues",
    "article-architect": "Design manuscript structure, displays, and claim strategy",
    "article-claim-auditor": "Independently audit manuscript claims against evidence",
    "article-context-builder": "Normalize study materials into an article context brief.",
    "article-cover-letter": "Draft journal cover letters from approved materials",
    "article-drafter": "Draft and revise versioned manuscripts and supplements",
    "article-evaluator": "Independently evaluate manuscript quality and readiness",
    "article-frontmatter-drafter": "Draft titles, abstracts, highlights, and key points",
    "article-literature-grounder": "Build auditable manuscript literature-grounding reports",
    "article-methods-statistics-auditor": "Independently audit study methods and statistics",
    "article-orchestrator": "Orchestrate articles through independent review and packaging",
    "article-readiness-triage": "Independently triage study materials for article readiness",
    "article-refinement-controller": "Plan reviewed manuscript revisions and fresh evaluation",
    "article-review-panel": "Run an isolated peer-review role on a frozen manuscript",
    "article-submission-compositor": "Independently verify and package articles for human sign-off",
    "idea-adversarial-review-panel": "Independently challenge promoted ideas by assigned role",
    "idea-evaluator": "Independently evaluate and gate frozen research ideas",
    "idea-portfolio-assembler": "Assemble evaluated ideas into ranked PI-review portfolios",
    "medical-journal-review": "Independently review medical research for rigor and fit",
    "methodology-statistics-preflight": "Independently preflight research methods and statistics",
    "multi-path-idea-generator": "Generate diverse research ideas without evaluating them",
    "perspective-argument-architect": "Design Perspective arguments and claim structures",
    "perspective-claim-evidence-curator": "Curate Perspective claims, evidence, and citation risks",
    "perspective-drafter": "Draft and revise versioned Perspective manuscripts",
    "perspective-evaluator": "Independently evaluate Perspective quality and outlet fit",
    "perspective-final-compositor": "Independently verify and package Perspectives for human review",
    "perspective-input-builder": "Normalize Perspective inputs into a structured brief",
    "perspective-orchestrator": "Orchestrate Perspectives through review and packaging",
    "perspective-refinement-controller": "Plan reviewed Perspective revisions and fresh evaluation",
    "perspective-review-panel": "Run an isolated Perspective review from one assigned role",
    "proposal-context-brief-builder": "Normalize proposal inputs into a structured context brief",
    "proposal-drafter": "Draft and revise versioned research proposals",
    "proposal-evaluator": "Independently evaluate proposal quality and defensibility",
    "proposal-orchestrator": "Orchestrate proposals through independent review and packaging",
    "proposal-package-assembler": "Assemble evaluated proposal artifacts for human review",
    "proposal-readiness-triage": "Independently triage ideas for proposal drafting readiness",
    "proposal-refinement-controller": "Plan reviewed proposal revisions and fresh evaluation",
    "proposal-review-panel": "Run an isolated proposal review from one assigned role",
    "research-context-builder": "Normalize research inputs into an idea-generation brief",
    "research-idea-orchestrator": "Orchestrate research ideas into evaluated PI-review portfolios",
    "research-opportunity-mapper": "Build source-grounded evidence and opportunity maps.",
    "research-polisher-methodology-publishability-reviewer": "Independently review strategy rigor and publishability",
    "research-polisher-orchestrator": "Orchestrate research impact strategies and independent review",
    "research-polisher-plan-assembler": "Assemble anonymous Research Polisher strategy portfolios",
    "research-polisher-strategy-reviewer": "Propose tiered research impact strategies independently",
    "sap-evaluator": "Independently evaluate statistical analysis plans",
    "sap-refinement-controller": "Plan reviewed SAP revisions and fresh evaluation",
    "sap-writer": "Draft and revise versioned statistical analysis plans",
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
    return DISPLAY_NAMES.get(
        name,
        " ".join(part.capitalize() for part in name.split("-")),
    )


def short_description(name: str) -> str:
    value = SHORT_DESCRIPTIONS[name]
    error = short_description_error(value)
    if error:
        raise ValueError(f"{name}: {error}")
    return value


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
            f"  short_description: {yaml_quote(short_description(name))}",
            f"  default_prompt: {yaml_quote(default_prompt(name))}",
            "policy:",
            f"  allow_implicit_invocation: {'true' if name in IMPLICIT_SKILLS else 'false'}",
            "",
        ]
    )
    (agent_dir / "openai.yaml").write_text(openai_yaml, encoding="utf-8", newline="\n")


def main() -> int:
    skill_files = sorted(SKILLS_ROOT.rglob("SKILL.md"))
    if not skill_files:
        raise RuntimeError("OpenAI plugin contains no skills")
    source_names: set[str] = set()
    for path in skill_files:
        frontmatter, _ = split_frontmatter(path.read_text(encoding="utf-8-sig"))
        name_block = field_block(frontmatter, "name")
        source_names.add(unquote(name_block[0].split(":", 1)[1]))
    if source_names != set(DESCRIPTIONS):
        raise RuntimeError(
            "OpenAI skill inventory differs from the maintained description contract: "
            f"missing={sorted(set(DESCRIPTIONS) - source_names)} "
            f"extra={sorted(source_names - set(DESCRIPTIONS))}"
        )
    if source_names != set(SHORT_DESCRIPTIONS):
        raise RuntimeError(
            "OpenAI skill inventory differs from the maintained UI description contract: "
            f"missing={sorted(source_names - set(SHORT_DESCRIPTIONS))} "
            f"extra={sorted(set(SHORT_DESCRIPTIONS) - source_names)}"
        )
    for name in sorted(source_names):
        error = short_description_error(SHORT_DESCRIPTIONS[name])
        if error:
            raise RuntimeError(f"{name}: {error}")
    for skill_md in skill_files:
        normalize_skill(skill_md)
    print(f"normalized {len(skill_files)} OpenAI skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
