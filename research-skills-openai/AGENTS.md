# AGENTS.md

These instructions apply to the `research-skills-openai/` plugin subtree.

## Product boundary

- Treat the plugin as an owner-operated Personal Experimental/Preview tool for
  the owner's ChatGPT Work and Codex research workflows.
- Optimize for reliable personal use, reproducible artifacts, independent
  evaluation, and explicit human decisions. Do not imply production support,
  public readiness, provider verification, automatic updates, or automatic
  external submission.
- Use `personal-owner` as the default acceptance boundary. Shared/public
  attestation and provider verification remain deferred unless the owner
  explicitly reopens them.
- Keep the plugin skills-only unless a real MCP server, app mapping, or hook is
  implemented and tested.

## Workflow invariants

Preserve single responsibility and close every full workflow through generation,
fresh independent evaluation, targeted revision, fresh re-evaluation or panel
review, and a final human-review package.

- Orchestrators route, track state, and enforce stop conditions; they do not
  score artifacts.
- Generators and drafters do not evaluate their own work. Reviewers run in fresh
  delegated instances against frozen, read-only inputs and write only review or
  verification reports.
- Assemblers preserve provenance, conflicts, minority opinions, and dissent;
  they do not silently repair source artifacts.
- Every substantive artifact change creates a new version and requires a fresh
  evaluator before promotion or a ready state.
- If independent review is unavailable, return `independent_review_pending`
  with a self-contained continuation brief and stop. Never substitute inline
  self-review.

## Artifact and human boundary

- Keep source artifacts immutable; store revisions, review reports, and deltas
  separately with complete lineage and digest bindings.
- A fatal or unresolved blocking finding prevents promotion or ready status.
- Workflows stop at material prepared for human review and signature. They do
  not submit to journals, funders, repositories, or other external platforms.
- Deterministic fixtures establish `deterministic_validated`, not real runtime
  completion. Use `owner_observed` only for a current-version task with bound
  source identity, artifacts, digests, reviewer identities where applicable,
  timestamps, outcome, and owner confirmation.

## Skill and discovery discipline

- Read the target `SKILL.md`, its required references, the registry, and every
  invoking orchestrator before changing a skill. Use `skill-creator` for a new
  or substantially rewritten skill.
- Keep core procedure in `SKILL.md`; move schemas, rubrics, examples, variants,
  and long operational detail into directly linked conditional references.
- Keep the maintained discovery surface stable unless the owner makes a
  deliberate product decision. Research Polisher remains explicit-only.
- Keep descriptions and default-loaded context concise. Existing oversized
  skills and references are Roadmap debt: do not enlarge them when touched.
- Update source, registry, generated metadata, documentation, fixtures, and
  validation expectations together.

## Versioned development and delivery

- Keep `.codex-plugin/plugin.json` and `workflow-registry.yaml` on the same
  SemVer. When the version changes, synchronize every current-version claim
  while preserving intentionally historical records.
- Run the relevant repository and plugin audits before handoff; fix all errors
  and report remaining warnings.
- **When a plugin-version update development task is complete, create a commit
  containing the completed version update and push it to GitHub.** Do not leave
  a completed plugin-version update only in the local working tree.
- Preserve unrelated user work and do not publish local cachebuster versions.

## Progressive disclosure

Load operational detail only when the task requires it:

- `workflow-registry.yaml`: inventory, roles, edges, modes, and invocation policy.
- `README.md`: installation, update, quickstarts, artifact defaults, and the
  maintained validation command set.
- `ROADMAP.md`: current baseline, active phases, acceptance status, and deferred
  scope.
- `PHASE7-8-RUNBOOK.md`: current-version installation, owner-observed receipts,
  runtime acceptance, and stop rules.
- Target `SKILL.md` files and their explicitly linked references: workflow-local
  procedures, schemas, rubrics, templates, and resource-loading conditions.
- Root `AGENTS.md`: repository-wide profile separation, authoring tools, audit
  expectations, and shared Hermes/OpenAI boundaries.
