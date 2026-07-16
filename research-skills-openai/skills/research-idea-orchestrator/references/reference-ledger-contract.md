# Idea Reference Ledger Contract

Load this reference when internal workflow identifiers appear in technical
artifacts or when preparing user-facing navigation.

Maintain one `<idea-node>/references/reference-ledger.md` per Idea node. Include only items
used by that Idea and update it when a dossier, map, preflight, evaluation, or
panel report adds or retires an identifier.

The orchestrator is the sole metadata writer for this ledger. Delegates return
readable labels and locators and never edit the ledger. If a report schema
requires an ID, the delegate pairs it with its label and the orchestrator
registers it; the ID is never evidence by itself.

| Internal ID | Type | Human-readable label | Definition artifact | Original source | Locator | Version/status |
|---|---|---|---|---|---|---|
| C24 | claim | Full claim text | Relative link | File, URL, DOI, or dataset | Page/section/table/paragraph | current/stale/retired |

Rules:

- Provide a valid relative link to the defining artifact and a usable locator
  in the original source. Record `not_available` rather than inventing one.
- In user-visible technical reports, pair every ID with its human-readable
  label, for example `C24: External validation remains untested`; never show a
  naked ID.
- Do not expose naked internal IDs in README, portfolio summaries, final
  decisions, or dossier prose.
- Standard academic citations are not workflow IDs and resolve through the
  dossier reference list.
- The ledger is navigation metadata, not evidence. `idea-evaluator` must not
  read it; the evaluator receives only the complete dossier.
