---
name: idea-portfolio-assembler
description: "Assemble evaluated ideas into a PI-review portfolio with lineage, limitations, dissent, and handoff status."
---
# Idea Portfolio Assembler

## Role

Assemble qualifying dossier/report pointers and sealed decisions into a concise
PI navigation portfolio. Do not generate/revise Ideas, copy dossier prose,
rescore, resolve reviewer disagreement, select an exploration winner, change
gates, or write a proposal.

## Invariants

- Use only current complete dossiers whose SHA-256 equals the qualifying
  independent evaluation's `reviewed_dossier_digest`.
- The evaluated dossier is the user deliverable and single Idea body. Link it;
  never copy, summarize into a substitute body, or silently repair it.
- Derive grouping/order/status only from orchestrator decisions and sealed
  reports. Preserve fatal/blocking findings, uncertainty, conflict, and dissent.
- An adversarial panel unresolved blocking finding yields `blocked`; unavailable review yields
  `independent_review_pending`. Bounded exploration yields
  `human_direction_selection_required`, never Proposal handoff.
- A verified focused package stops at `human_signoff_required`.
- Treat v1/v2 or snapshot layouts as read-only; return
  `layout_migration_required` without writing into the legacy tree.

## Inputs and Procedure

1. Validate v3 layout, route, current node/dossier pointers, digests, identity, qualifying
   dossier-only evaluations, ledgers, lineage, and sealed decisions. Require all
   adversarial roles for a focused Proposal-handoff candidate.
2. Mechanically group focused outcomes as promoted, revise-then-promote, backup,
   rejected, or evaluation-failed. For bounded exploration, preserve all
   directions in orchestrator order without ranking or selection.
3. Create one navigation entry per Idea with exact dossier/evaluation/ledger
   links, title, short status, fatal/blocking findings, dissent, unresolved
   issues, and next human action.
4. Pair any internal ID with a readable label and ledger resolution. Do not show
   naked IDs in the executive summary or decision table.
5. Produce a portfolio, no-qualifying report, or assembly-failure report. Stop
   at human review.

## Conditional Resources

- Read `references/portfolio-input-schema.md` before validation.
- Read `references/portfolio-output-schema.md` before assembly.
- Read `references/portfolio-policy.md` for route-specific grouping/order/status.
- Read `references/promoted-idea-package-rules.md` for each navigation entry.
- Read `references/lineage-summary-rules.md` when showing ancestry/change.
- Read `references/no-promoted-idea-report-rules.md` when none qualifies.
- Read `research-idea-orchestrator/references/idea-artifact-lifecycle.md` for v3
  dossier/digest/identity gates.
- Read `research-idea-orchestrator/references/reference-ledger-contract.md` when
  displaying internal references.
- Read `research-idea-orchestrator/references/artifact-contracts.md` for shared fields.
- Read `research-idea-orchestrator/references/workflow-manifest.md` before state handoff.
- Use `templates/research-idea-portfolio.md` for a navigation portfolio.
- Use `templates/no-promoted-idea-report.md` when no Idea qualifies.
- Use `templates/portfolio-assembly-failure-report.md` on assembly failure.

## Completion Check

Confirm exact dossier/evaluation digest match, valid relative links, unchanged
decisions, visible fatal/blocking/dissent, readable references, correct human
state, and no copied dossier, new evaluation, winner selection, or proposal text.
