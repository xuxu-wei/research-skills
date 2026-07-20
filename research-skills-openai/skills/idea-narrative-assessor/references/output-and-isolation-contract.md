# Output and isolation contract

## Allowed inputs

Narrative-assessment mode accepts:

- one current complete dossier, identified by `artifact_id`, `version`, and `path`;
- one reader-reasoning handoff, supplied either as a logical artifact reference or
  directly in the delegation brief; and
- this skill's own instructions, references, and templates.

No content digest is required. If the handoff is embedded in the brief, do not add a
fictitious file to `files_read`.

Do not open preflight, evaluator or language reports, earlier dossiers, revision
deltas, workflow state, artifact indexes, portfolio outputs, or parent reasoning. If a
forbidden project artifact is exposed, stop and request a clean fresh instance.

## Assessment report

Write `narrative-assessment-rNNN.md`. Its YAML frontmatter must include the logical
input reference, actual project files read, isolation assertions, decision, and
structured findings. The Markdown body explains the reader effect and scope without
drafting replacement prose.

Use the common reviewer provenance fields from `SKILL.md` and
`isolation_mode: fresh_subagent`. `input_artifact_ids` and `input_versions` must
match the declared dossier and any file-backed reader handoff; an embedded
handoff is not a fictitious artifact.

Finding severities are `minor`, `major`, or `clarification`. Each finding needs a
stable ID, category, dossier locator, observed evidence, current reader effect, and
target function. Locators must name a heading and a recognizable paragraph, table, or
content anchor; a line number alone is invalid.

## Repair plan

Always write `narrative-repair-plan-rNNN.yaml`, including for `narrative_ready`.
Allowed operations are exactly:

`replace`, `define`, `move`, `split`, `merge`, `delete`, `reorder`, `add_bridge`, and
`consolidate`.

Each action must contain:

- `action_id`
- `addresses_findings`
- `priority`
- `dossier_locator`
- `operation`
- `current_problem`
- `target_state`
- `required_content_or_function`
- `content_to_preserve`
- `content_to_remove_or_move`
- `destination_if_moved`
- `dependencies`
- `acceptance_test`

An action is executable only when a fresh writer can identify where to work, the
reader-facing function to achieve, what to preserve, what to remove or relocate, any
destination and dependency, and an observable completion test. Do not use instructions
such as “improve clarity” or “strengthen logic” without these particulars. Exact
verified terminology replacements belong to the language assessor's action list, not
this plan. Describe required scientific content, operations, and reproducibility
records directly; do not prescribe software, project-management, or review-state
labels as reader-facing wording. A `replace`, `move`, `merge`, `delete`, `reorder`, or `consolidate` action
must name the content to remove, move, or replace; an empty list is not executable.

The plan must also preserve the current artifact contract. For a
`research-idea.v3` dossier, do not delete or rename any of the 15 required H2
sections or the five required H3 functions under section 3. Evidence chains and
Claim-Support remain mandatory reader-auditable functions. Each evidence chain keeps
`Input`, `Method / analysis / processing`, `Output`, and `Supports`; do not preserve
or recreate a standalone chain-level limitations field. Section 14 is the sole
complete limitations and assumptions authority. Consolidation may shorten or relocate
duplicate prose, but the action must state what distinct function and minimum content
remain in every affected required section. Never solve repetition by silently
replacing several mandatory functions with one new table or by requiring a schema
migration that the task did not authorize.

Do not replace deleted limitation prose with pointers or cross-references to section
14. Outside section 14, omit the item entirely unless a minimal boundary directly
enables the immediately adjacent scientific reasoning and omission would distort it;
that local boundary must stand on its own and must not restate or point to the complete
authority.

Every major finding must be addressed by an action. Dependencies may reference only
other action IDs and must form a directed acyclic graph. For `narrative_ready`, both
findings and actions are empty. For `clarification_required`, list the exact missing or
conflicting information under `clarifications_required`; actions may be empty until it
is supplied.

Validate the pair before handoff:

```powershell
python scripts/validate_narrative_outputs.py --assessment <report.md> --plan <plan.yaml>
```
