# Decision Log Schema

Create `09_state/decision-log.md` at project initialization. Every irreversible or quality-affecting decision gets an entry.

```markdown
## D{N}: [Short decision]

- Time: [ISO-8601 or local timestamp]
- Step: [workflow step]
- Trigger: [user request / evaluator route / panel route / compositor return]
- Inputs reviewed: [artifact paths]
- Decision: [route or action]
- Alternatives considered: [brief list]
- Rationale: [why this route was chosen]
- Risks accepted: [none or list]
- User confirmation: required / obtained / not required
- Follow-up artifact: [path]
```

Mandatory entries:
- mode selection
- outlet retarget
- thesis redesign
- evidence rebuild
- overriding evaluator/07_panel/compositor recommendations
- caveat budget choice
- stop decision
- final readiness declaration
