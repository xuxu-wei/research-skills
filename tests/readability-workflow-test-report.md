# Cross-workflow readability test report

## Scope and handling rules

- Current candidate: `research-skills-openai` `0.11.0`.
- Frozen comparison baseline: `0.10.0` runs for Idea, Proposal, Perspective, and Article, created before source modification.
- Original inputs under `tests/test-*` are read-only. Versioned run directories are generated evidence and are not release assets.
- This report contains contract-level observations only; it does not reproduce confidential scientific content.
- A localized minor miss that does not change science, preservation, readiness, decisions, or broad output is recorded here without a new correction, reproduction attempt, or extra test. More serious failures remain in the active fix-and-retest loop.

## Modification trajectory and root-cause review

The initial Idea investigation found several coupled symptoms: audit-style prose displaced the scientific story; project-internal or unsupported terms appeared before the reader understood the problem; methodological defense and caveats dominated positive claims; the background/current-state/gap/significance/rationale chain was incomplete; limitations were repeated; additive revision made the document longer without restoring its main line; and fluent repair could drift core scientific content.

Repeated movement between language assessment and the writer was not primarily a copyediting defect. The upstream workflow sent scientific-review findings and raw editorial reports directly into prose revision without a single owner for macro structure, conflict resolution, protected content, or action conformance. One reviewer fixed argument architecture, another fixed terminology, and the writer locally satisfied whichever instruction was most salient. This encouraged additive hedging and made a local repair regress another section. Fresh-reviewer variance amplified the effect.

The evidence supports this causal ordering:

1. Macro workflow architecture and input handoff were the primary causes.
2. Missing reader baseline and section-function planning were the next cause.
3. Raw-report overload and absent instruction normalization caused writer execution variance.
4. Long context is a possible secondary cause, but is diagnosed only by a paired same-writer test after input, assessor, and brief failures are excluded.
5. Common model habits—local compliance, additive revision, defensive qualification, and reuse of internal vocabulary—amplified the architecture defect but do not explain it alone.

The `0.11.0` design therefore separates macro narrative assessment from language/terminology assessment, normalizes both into one YAML writer brief, protects scientific content, checks action execution, reassesses a new complete version, and isolates the final evaluator from all repair history. Proposal gains a pre-prose content plan; Perspective reuses its argument architecture; Article gains complete input discovery and a full manuscript content plan.

### Current fresh-run diagnosis

- Idea and Proposal both stopped at their evidence-research boundaries without inventing a dossier or proposal. Their reader-aware context and routing artifacts were produced, but the supplied inputs did not authorize the downstream writing branch.
- Perspective exposed three separable execution layers. Run 001 found two zero-output input-builder attempts and an unnecessary template. After the contract separated three normal outputs from the missing-input-only template, run 002 produced the correct three files on the first fresh delegation and completed a bounded evidence package. Its first architect and one permitted fresh retry then read and planned without writing the required skeleton. A targeted architect execution order fixed this: run 003's first fresh architect saved an early skeleton checkpoint, expanded it one claim/binding at a time, and passed the architecture gate without a retry.
- Run 003 then isolated a related writer behavior. The writer loaded the full skeleton/evidence package before its first write and required one bounded write-now follow-up, but subsequently produced a conforming complete draft and faithfully executed three normalized revisions under the same writer identity. This is evidence of late persistence and broad upfront loading, not inability to write. The minimum drafter change now requires the same writer to create the draft/map pair first, then complete one section at a time with Claim/Binding-targeted reads. In run 004, exactly one fresh writer received no follow-up or replacement, created both process files early, expanded them progressively, and passed all eight deterministic conformance checks.
- Run 003's v005 passed fresh scientific evaluation, but a renewed independent panel still found non-operational comparison and independence requirements after the single allowed panel major revision. The workflow stopped for no further gain, preserved dissent, and created no editorial, final-evaluation, or journal artifacts. This is a legitimate scientific branch stop, not a narrative or language failure.
- Article now discovers the complete supplied inventory and applies the owner-designated semantic authority without discarding compatible execution evidence. Independent preflight found that the unresolved plan-execution choice changes the analysis route, evidence strength, and article objective. It therefore returned `clarification_stop` with no accepted working assumption; prose repair is not allowed to conceal or choose that scientific route.

These results refine the macro diagnosis. The first Perspective failure occurred before a long writer context existed, so raw context length was not the primary cause. The later writer did receive a substantially larger package and completed only after a write-now reminder; the patched writer completed without intervention when persistence occurred before broad evidence loading. Context attention therefore matters at the meso execution layer—input ordering, targeted retrieval, and checkpoint timing—rather than as a blanket model-capacity explanation. The Article stop remains a genuine scientific decision boundary rather than a language problem.

## Frozen `0.10.0` baseline

| Workflow | Observed outcome | Diagnostic meaning |
|---|---|---|
| Idea | Stopped at an evidence-research handoff before dossier generation | Truthful stop; no narrative artifact was available for this baseline run. |
| Proposal | Stopped at an evidence-research handoff after context creation | Context lacked a reader profile and persisted an unnecessary hash; downstream readability could not be tested. |
| Perspective | Input artifacts were produced; evidence mapping identified the need for a research handoff but omitted the handoff file | The scientific route was correct; the omitted handoff artifact is logged below as a minor execution deviation. |
| Article | Readiness returned `not_ready` although traceable technical-report/result materials had been supplied | Severe input-discovery defect: the workflow relied on a narrow named-source intake instead of inventorying all supplied materials. This is upstream of writer/language behavior. |

## Minor issue log

### MIN-001 — Perspective handoff artifact omitted

- Plugin version: `0.10.0`.
- Symptom: the mapper explicitly concluded that a research handoff was required but did not materialize the corresponding handoff file before the delegated run ended.
- Suspected diagnosis: localized execution omission after the routing decision; no incorrect scientific promotion or broad artifact contamination occurred.
- Proposed solution: retain deterministic handoff-completeness checking in the orchestrator’s normal artifact-index validation. Do not reproduce or start a separate correction cycle unless recurrence affects a current decision.

### MIN-002 — Source/cache line-ending differences

- Plugin version: `0.10.0` development channel; observed again after the `0.11.0` Git release.
- Symptom: `openai_plugin_dev.py verify --channel github` rejected the installed `0.11.0` cache although the source and cache both contained 428 files, declared the same version, 51 Skills, and 22 reviewers. Direct byte comparison reported 59 differing text files; an in-memory CRLF/LF normalization reduced the content difference count to zero.
- Suspected diagnosis: Windows worktree conversion versus canonical Git LF content, not semantic drift or an incomplete Git installation.
- Proposed solution: in a later low-priority development-tool pass, compare normalized text content while retaining exact inventory, version, Skill, reviewer, selector, and unexpected-file checks. Do not persist hashes. The current workflow and release do not require reproduction or correction for this verifier-only false negative.

### MIN-003 — Article readiness category-count wording

- Plugin version: `0.11.0` development source.
- Symptom: `article-readiness-triage/SKILL.md` says to check seven minimum input categories, while the adjacent table currently enumerates six named categories.
- Suspected diagnosis: localized documentation count drift; the named readiness fields and decisions remain explicit, and no current scientific, readiness, or routing result was affected.
- Proposed solution: reconcile the prose count with the canonical readiness schema during a later low-priority documentation pass. Per the minor-issue policy, do not open a new correction or reproduction cycle for this isolated wording issue.

### MIN-004 — Fresh CLI child lacks the desktop task runtime

- Plugin version: `0.11.0` Local development channel.
- Symptom: a fresh `codex exec` subprocess could not inherit the desktop task's authenticated online runtime and opened with a read-only execution boundary, while a fresh Codex App task loaded the Local plugin normally.
- Suspected diagnosis: test-harness/runtime separation rather than plugin discovery or Skill behavior.
- Proposed solution: use fresh Codex App tasks for forward tests and retain `openai_plugin_dev.py verify` for deterministic Local/Git discovery. Do not alter workflow contracts or reproduce this environment-only issue.

### MIN-005 — Article reviewer rereads paired display carriers

- Plugin version: `0.11.0` Local development channel.
- Symptom: readiness and methods reviewers inspect both raster and vector carriers of the same declared displays, substantially increasing review time while still reaching the correct inventory and methods findings.
- Suspected diagnosis: the complete-material rule does not yet distinguish semantic display items from alternate file-format carriers.
- Proposed solution: if this recurs, permit a deterministic equivalence manifest plus one reviewer-visible canonical carrier per display, while retaining complete path indexing and mismatch escalation. Do not change or rerun the current workflow for this performance-only observation.

### MIN-006 — Article fixed ordering performs blocked downstream preparation

- Plugin version: `0.11.0` Local development channel.
- Symptom: readiness explicitly recommended methods preflight, but the fixed standard route still produced literature grounding, an article blueprint, and a display manifest before the decisive methods stop.
- Suspected diagnosis: the orchestrator order assumes all conditionally ready studies should complete preparation before methods audit; it does not yet short-circuit on a readiness-directed methods route.
- Proposed solution: during a later efficiency pass, consider routing `recommended_route: methods_preflight` through the minimum normalized context directly to isolated methods review, and resume literature/architecture only after a pass. The current result was scientifically correct, so do not change or reproduce it in this cycle.

### MIN-007 — Perspective paragraph markers contain a literal escape token

- Plugin version: `0.11.0` Local development channel, Perspective run 003.
- Symptom: panel-major revision v004 contained literal `\\n` text in several paragraph markers instead of real line breaks. The controller's mechanical check detected it before promotion; the same writer produced formatting-only v005, with the scientific content and prior version preserved.
- Suspected diagnosis: localized text-serialization/escaping behavior during a long same-writer revision, not a claim, evidence, routing, or preservation defect.
- Proposed solution: retain the existing literal-token check in pre-evaluation conformance. Per the minor-issue policy, do not add a plugin fix or separate reproduction unless this recurs beyond paragraph markers or escapes deterministic detection.

### MIN-008 — Private-role CLI smoke falls back to file inspection

- Plugin version: `0.11.0` Git channel.
- Symptom: a fresh raw CLI prompt naming the private `research-narrative-assessor` did not receive that role in its exposed Skill catalog and inspected the installed cache to answer. A separate fresh, read-only, zero-tool task received the public `research-idea-orchestrator` entry at session start and accurately reported its role from injected instructions.
- Suspected diagnosis: the smoke prompt used a private role with `allow_implicit_invocation: false`, so it did not cleanly distinguish runtime entry discovery from filesystem availability. There is no evidence that public entry discovery or orchestrated private-role delegation failed.
- Proposed solution: use a public entry Skill for the no-tool Git discovery smoke, verify private-role inventory deterministically, and assess orchestrated private-role delegation only when a legitimate workflow branch reaches it. Do not open a new workflow correction or reproduction cycle for this test-design issue.

## Current `0.11.0` acceptance record

| Check | Status | Evidence |
|---|---|---|
| Source inventory/version/registry | Pass | Current deterministic audit reports 51 Skills, 22 reviewers, Registry schema v6, 72 declared edges, and no warnings. |
| Shared narrative/language role boundary | Static pass; forward branch not reached | Contract tests pass; the supplied fresh fixtures stopped before editorial review rather than fabricating evidence. |
| Idea reader-aware intake and truthful routing | Pass for current fixture | Fresh context/mapper instances produced the reasoning handoff and a self-contained evidence continuation package; no dossier or evaluator result was invented. |
| Proposal readiness and truthful routing | Pass for current fixture | Fresh readiness review returned idea refinement, then evidence handoff; no planner, writer, or evaluator was dispatched without the required scientific inputs. |
| Proposal content planning and final-evaluator isolation | Contract pass; forward branch not reached | The current fixture stopped upstream; planner/writer separation and evaluator whitelist remain deterministically enforced. |
| Perspective input and evidence routing | Pass for current fixture | Run 002 produced exactly the three normal input artifacts on its first fresh delegation, omitted the conditional template, and built a bounded evidence package with calibrated claims and unresolved gaps. |
| Perspective argument planning and scientific isolation | Pass for reached branch | Run 003's first fresh architect created and completed the skeleton without retry. Successive evaluators and two panels were isolated from prior scores/revision history. The renewed panel stopped v005 for unresolved scientific architecture after the permitted major revision; no editorial or final artifacts were fabricated. |
| Article complete material discovery and semantic authority | Pass for current fixture | Fresh intake covered all supplied files and all declared displays; the sole semantic authority was applied while compatible execution evidence remained visible. Two isolated methods reviewers independently stopped the workflow for reanalysis. |
| Writer action fidelity | Fresh-draft forward pass; editorial branch not reached | Run 004 used one fresh writer, no follow-up or replacement, early draft/map checkpoints, progressive section completion, and 8/8 conformance. Run 003 also retained one writer across all scientific revisions. No current fixture legitimately reached editorial repair, so repair-brief execution remains contract-tested rather than newly forward-tested. |
| Context-attention diagnosis | Meso execution cause supported | The pre-patch writer delayed all persistence while broadly loading the package and needed one reminder. With the same scientific inputs, the patched fresh writer wrote first, expanded section by section, and completed without intervention. This supports retrieval/order/checkpoint design as the actionable cause; it does not establish a universal token threshold. |
| Content preservation | Contract pass; forward branch not reached | The current fixtures stopped before editorial revision. Protected-register and preservation-decision guards pass; no downstream artifact was created from unsupported science. |
| DOCX semantic parity and visual QA | Pass for reached branch | The 13 deterministic DOCX guards pass. Article correctly stopped before drafting and generated no manuscript or DOCX; full render QA was therefore not applicable to this fixture. |
| Local/Git plugin discovery | Pass with recorded verifier caveat | Local verification passed. The Git selector is uniquely enabled at `0.11.0`; source and cache inventories are 428/428, normalized content differences are zero, and a fresh read-only zero-tool task received the public Idea orchestrator from session-start Skill context. The raw-byte CRLF/LF false negative and private-role smoke limitation are recorded as MIN-002 and MIN-008. |

## Forward-test blinding

Fresh workflow agents receive only the original fixture, the requested workflow, allowed resources, and output directory. They do not receive this report, baseline diagnoses, expected readability findings, repair answers, owner oracle, prior artifacts, or prior scores. Acceptance reviewers may consult the oracle only after the run is sealed. If a run stops truthfully for unavailable evidence or reviewer capacity, the stop is recorded; it is not rewritten into a false ready result.
