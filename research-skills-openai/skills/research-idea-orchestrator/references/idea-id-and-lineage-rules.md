# Idea ID and Lineage Rules

Use this file to keep research idea identities stable across generation paths, evaluation rounds, revision, merge, reframe, backup, and proposal handoff.

## Canonical ID Format

Canonical idea IDs use this format:

```text
I<round>-<sequence>
```

Examples:

```text
I01-001
I01-002
I02-001
```

Rules:

- `round` is the idea workflow round that first created the idea.
- `sequence` is the order in which the orchestrator accepted the idea into the idea pool during that round.
- IDs are assigned or normalized by `research-idea-orchestrator`.
- Generator-provided provisional IDs must be replaced or mapped before evaluation.

## Derived ID Format

Derived ideas keep the parent visible:

```text
I01-002-R01      # revision of I01-002 in repair round 1
I01-002-F01      # reframe of I01-002
I01-002-S01      # salvage attempt
```

Merge IDs list the merge round and sequence:

```text
I02-M001
```

The lineage record must list all parent IDs for merged ideas.

## Stability Rules

- Do not rename an idea after it has an independent evaluation report.
- If an ID must be normalized, record `previous_ids`.
- Revisions, reframes, merges, and salvage attempts get new IDs unless the change is purely clerical.
- Rejected and backup ideas keep their IDs; do not recycle IDs.
- Proposal handoff packages use the final promoted idea ID and list all parent IDs.

## Required Fields

Every idea-like artifact should include:

```yaml
idea_id: "I01-001"
previous_ids: []
created_round: 1
origin_round: 1
revision_round: 0
parent_idea_ids: []
lineage_id: "L-I01-001"
```

## Artifact Naming

Idea pool files should include the round:

```text
03_ideas/round-001/generated-idea-set.md
03_ideas/round-001/idea-pool.yaml
03_ideas/round-002/revised-idea-set.md
05_evaluations/round-001/idea-evaluation-I01-001.md
06_adversarial/round-002/adversarial-review-I01-001.md
07_portfolio/research-idea-portfolio.md
```

The portfolio may show short display labels, but machine-readable handoff fields must use canonical IDs.
