---
name: idea-portfolio-assembler
description: "Assemble evaluated ideas into a PI-review portfolio with ranking, lineage, limitations, dissent, and handoff status."
---
# Idea Portfolio Assembler

## Role

Assemble qualifying current Idea snapshots and sealed decisions into a
self-contained PI-review portfolio. Do not generate/revise Ideas, rescore,
resolve reviewer disagreement, change gates, or write a proposal.

## Invariants

- Use only complete snapshots whose SHA-256 equals the qualifying independent
  evaluation digest and whose identity is preserved.
- Copy or faithfully organize the full current Idea. Scores, novelty changes,
  lineage, and revision history are subordinate; they never replace its body.
- Derive grouping, ranking, and handoff status only from orchestrator decisions
  and valid reports. Do not manufacture consensus or suppress dissent.
- Any adversarial panel unresolved blocking finding yields `blocked`; unavailable review yields
  `independent_review_pending`; only a verified portfolio may yield
  `human_signoff_required`.

## Inputs

Require frozen context and evidence/opportunity summaries; current node pointers,
complete snapshots, versions and digests; qualifying evaluation/preflight
reports; lineage and orchestrator decisions. Require all adversarial role reports
for any proposal-ready or conditional Idea.

## Procedure

1. **Validate.** Confirm every displayed snapshot is complete, current, digest
   matched, independently evaluated, and free of unresolved blocking findings.
2. **Group.** Mechanically group candidates as promoted, revise-then-promote,
   backup, merged, rejected, or evaluation-failed.
3. **Order.** Apply existing orchestrator/ranking policy without changing any
   score, gate, recommendation, or dissent.
4. **Assemble each Idea.** Include its complete one-sentence summary, question,
   objectives, work packages, hypothesis, significance, relevance/impact/
   innovation, applications, evidence base, methods, required analyses/evidence,
   feasibility/resources, risks/assumptions/stops, plus evaluation, lineage,
   dissent, and handoff state.
5. **Preserve trace.** Bind snapshot path/version/SHA-256 and stable report refs.
   Put key changes in a separate subordinate lineage section.
6. **Handoff.** Produce the PI portfolio or a no-promoted/failure report. Stop at
   human review; never create proposal prose.

## Conditional Resources

- Read `references/portfolio-input-schema.md` for minimum inputs.
- Read `references/portfolio-output-schema.md` for output sections.
- Read `references/portfolio-policy.md` for grouping, ordering, and handoff states.
- Read `references/promoted-idea-package-rules.md` when building candidate packages.
- Read `references/lineage-summary-rules.md` when summarizing ancestry/change.
- Read `references/no-promoted-idea-report-rules.md` when no Idea qualifies.
- Read `research-idea-orchestrator/references/idea-artifact-lifecycle.md` for snapshot, digest, node, and identity gates.
- Read `research-idea-orchestrator/references/artifact-contracts.md` for shared fields.
- Read `research-idea-orchestrator/references/workflow-manifest.md` before state handoff.
- Use `templates/research-idea-portfolio.md` for the PI portfolio.
- Use `templates/no-promoted-idea-report.md` when none qualifies.
- Use `templates/portfolio-assembly-failure-report.md` when inputs are invalid.

## Completion Check

Confirm self-contained Idea content, matching snapshot/evaluation digests,
preserved identity/lineage, unchanged decisions, visible dissent/fatal findings,
justified handoff states, and no new evaluation or proposal content.
