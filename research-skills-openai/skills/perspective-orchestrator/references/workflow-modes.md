# Workflow Modes

## Lite

Use for feasibility, argument sharpening, and "can this be a Perspective?" requests.

Required route: STEP 1 -> STEP 2-lite -> STEP 3.

Required outputs:
- `00_input/01-input-brief.md`
- `00_input/target-outlet-profile.md`
- `01_claims/claim-ledger.md` marked `provisional`
- `01_claims/claim-evidence-matrix.md` marked `provisional`
- `02_evidence/evidence-limitations.md`
- `01_claims/existing-discourse-baseline.md` marked `provisional`
- `03_skeletons/02-argument-skeleton.md`
- `03_skeletons/early-feasibility-report.md`

No external retrieval is required. Evidence gaps must be explicit.

## Standard

Use for a full first draft. Required route: STEP 1 -> STEP 2 -> STEP 3 -> STEP 4 -> STEP 5 -> STEP 6 once by default.

Standard can end with:
- accepted draft package, if evaluator returns `accept`
- revised draft package with unresolved risks, if max revision is reached
- diagnostic stop report, if routed to `reject_not_salvageable`

## Full

Use for target-outlet preparation or submission-readiness review. Required route: complete STEP 1 through STEP 9.

Full mode requires a non-generic target outlet for `Ready for human review and sign-off: yes`. Generic profiles may only produce `outlet-targeting-only`.
