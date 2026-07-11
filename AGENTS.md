# AGENTS.md

## Top-level action principles

- Read the nearest applicable `AGENTS.md` before changing files; nested instructions override this file within their subtree.
- Preserve the two maintained profiles: Hermes sources under `research-skills/` and the OpenAI plugin under `research-skills-openai/`. Do not copy platform-specific metadata or runtime syntax between them.
- Use `skill-creator` before creating or substantially rewriting a skill, and use `plugin-creator` for plugin structure, marketplace, or installation changes.
- Keep changes scoped, preserve unrelated user work, and do not modify external or third-party skills unless the request explicitly includes them.
- Maintain single responsibility, progressive disclosure, independent evaluation, artifact lineage, visible dissent, and explicit stop conditions.
- Treat generators, evaluators, reviewers, and assemblers as separate roles. A changed substantive artifact must receive a fresh independent evaluation before promotion or final handoff.
- Update generated registries, manifests, documentation, and validation expectations together with source changes.
- Run the relevant repository and plugin audits before handoff; fix all errors and report remaining warnings.
