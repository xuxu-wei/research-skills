# Generation Quality Gates

Before persistence, require:

- all 15 Dossier sections, a complete whole-Idea summary, references, and the
  five non-empty ordered H3 functions `Background`, `Current state`, `Gap`,
  `Significance`, and `Rationale` under section 3;
- a reader-understanding core that introduces the problem before specialized
  concepts and makes title, summary, abstract, and section 3 understandable
  without definitions deferred to technical sections;
- a one-sentence complete-Idea summary whose visible sequence is central study
  object or question -> primary research approach or planned test -> positive
  planned contribution. Use validation language only when the Idea includes a
  validation task. Use parallel clauses and retain only the conditions needed to
  prevent a material misreading at summary level;
  do not pack the full technical or limitation inventory into that sentence.
  When present, a contingent downstream component is a short purpose-level clause here, not
  an eligibility/alternative/stop decision tree, and its project-specific stage
  or branch labels are deferred until they can be explained. Do not include a
  publication/resource inventory or component-specific visits/items in that
  sentence;
- at least one complete Input -> Method/analysis/processing -> Output chain per
  major objective/work package, with every core hypothesis linked to an output;
- a Claim-Support row for each title or primary positioning claim;
- no unsupported claim in title/summary/positioning and no opaque workflow ID
  used as dossier evidence;
- question/objective, data/evidence base, design/method, expected outputs,
  feasibility, risks, and stop conditions;
- method detail matched to Idea-stage evidence: name each validation
  component's scientific role, calculation family, comparison, direction,
  decision timing, and failure meaning, but do not invent unsupported universal
  thresholds or protocol details merely to appear complete. A data-,
  simulation-, or pilot-dependent choice needs a bounded
  owner/deadline/allowed-information rule before the relevant result is visible.
  Never leave scientifically different primary metrics joined by an
  unexplained `or`;
- one authoritative location in section 14 for complete limitations and working
  assumptions, plus operational risks that do not copy Methods design logic.
  Keep design eligibility, mutually exclusive analysis alternatives, and
  design-specific stopping logic only in Methods. Delete limitations elsewhere
  unless a boundary is necessary to
  explain the immediately following reasoning or design choice. Never retain a
  pointer or cross-reference to section 14; a necessary local boundary is
  self-contained;
- when the design has a sequential success-gated downstream component, the
  dossier contract's optional placement pattern; other architectures use a
  design-faithful placement map. Omit a component from sections with no distinct
  function; never use broad traceability as a reason to mention it everywhere;
- natural reader-language labels rather than machine enum tokens in the
  Claim-Support table, and one complete section-14 list for any deliberately
  unresolved specifications. Free-form reader-facing headings, table headers,
  and labels use the target language; contract-fixed scaffold labels remain
  unchanged and are not rewritten merely for localization;
- a final mechanical pass for consistent terms, first-use explanations,
  unambiguous modifier attachment, deletion of repeated caveats, and removal of
  internal workflow vocabulary from reader-facing prose. On an editorial repair,
  this pass must cover every occurrence of each core role, not only the example
  locators in the reports, and must reject newly invented compressed replacement
  labels. If one compact action word alternately names a diagnostic result, a
  decision, an analysed object's status, or a record, replace it with
  role-specific wording that identifies the trigger, object, and consequence.
  It must also remove internal statements about the current revision,
  preflight approval, reviewer activity, or what a prior version did or did not
  read; express only the present scientific or evidence state;
- matching node pointer, identity anchor, logical artifact reference, reference
  ledger, and Idea index entry; and
- route-compliant count: one focused Idea or two/three supported exploration
  directions.

Reject patches, deltas, partial dossiers, invented evidence, unsupported quota
fillers, and post-remap structural additions. Return a failure report and route
to context, mapping, or human confirmation as appropriate.

Run `scripts/lint_idea_dossier.py` for deterministic structure. Passing the
lint does not permit the generator to declare `narrative_ready`; that decision
belongs to a fresh narrative assessor.
Treat each emitted `ADVISORY` as a bounded reader-language review candidate,
not a universal banned word. Before handoff, either replace it with the domain
object, operation, or record it denotes, or define the legitimate technical
term at first use; record the disposition in the delta for an editorial repair.
