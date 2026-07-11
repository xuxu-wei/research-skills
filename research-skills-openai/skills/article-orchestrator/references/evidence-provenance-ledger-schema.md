# Evidence Provenance Ledger Schema

Schema for tracking the provenance of every piece of evidence supporting manuscript claims. Shared between `article-architect`, `article-drafter`, and `article-claim-auditor`.

## Granularity Tiers

The EPL supports three levels of granularity. MVP (v0.1.0) targets Level 1.

| Level | Granularity | Target Version |
|-------|------------|----------------|
| Level 1 | claim-level | v0.1.0 (MVP) |
| Level 2 | paragraph-level | v0.5.0+ |
| Level 3 | sentence-level | v1.0.0+ |

## Level 1 Schema (claim-level, MVP)

```yaml
evidence_provenance_ledger:
  schema_version: "research-article.v5"
  granularity: claim_level
  entries:
    - evidence_id: "E001"
      claim_ids: ["C001"]
      evidence_type: primary_data | secondary_data | experiment | statistical_result | literature_reference | user_assertion | assumption
      source_description: ""
      verification_status: verified | user_supplied_unverified | inferred | missing
      risk_level: low | medium | high
      notes: ""
```

### Field Rules

- `evidence_id`: Unique within the project. Format `E` + zero-padded sequence number.
- `claim_ids`: References to claims in the Claim-Evidence Matrix (`C001`, `C002`, ...).
- `evidence_type`:
  - `primary_data`: Raw or analyzed data from the study itself
  - `secondary_data`: Data from external sources
  - `experiment`: Experimental result
  - `statistical_result`: Output of a statistical procedure (estimate, CI, p-value)
  - `literature_reference`: Published finding from another study
  - `user_assertion`: Claim made by the user without provided data
  - `assumption`: Axiomatic or methodological assumption
- `verification_status`:
  - `verified`: Evidence source has been checked and confirmed
  - `user_supplied_unverified`: User provided the data/result, system cannot independently verify
  - `inferred`: Reverse-engineered from manuscript text (fast-track backfill)
  - `missing`: Evidence is referenced but not available
- `risk_level`: Assesses the risk that this evidence is incorrect, misrepresented, or insufficient.
- `notes`: Free text for uncertainty, caveats, or verification instructions.

## Level 2 Schema (paragraph-level, v0.5.0+)

Adds to Level 1:

```yaml
    appears_in:
      manuscript_section: "Results"
      paragraph_id: "R-P03"
      display_id: "D001"
    numeric_values:
      estimate: ""
      ci_lower: ""
      ci_upper: ""
      p_value: ""
      sample_size: ""
      model: ""
```

## Level 3 Schema (sentence-level, v1.0.0+)

Adds to Level 2:

```yaml
    sentence_index: 2
    original_text_snippet: ""
```

## Usage Rules

1. **Architect** generates the initial ledger from the Claim-Evidence Matrix during blueprint (Step 4).
2. **Drafter** links each Results paragraph to evidence entries (Level 2+ only; in MVP, drafter verifies that each claim has at least one evidence entry).
3. **Claim-Auditor** reads the ledger during claim audit (Step 9) and verifies:
   - Every claim with `verification_status = missing` is flagged as `evidence_support: absent`.
   - Every claim with `verification_status = user_supplied_unverified` or `inferred` has `risk_level` assessed.
4. **Evaluator** uses the ledger to assess the `Evidence-Claim Alignment` dimension.
5. **Submission-Compositor** checks that no `verification_status = missing` entries remain unaddressed.

## EPL in Fast-Track Backfill

When the EPL is inferred from an existing manuscript (fast-track backfill):
- All entries marked `verification_status: inferred`
- All entries marked `source_description: "Inferred from manuscript text — not verified against primary data"`
- The scope limitation `fast_track_backfill` is recorded
