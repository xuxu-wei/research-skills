# Fatal Flaw Criteria

A fatal flaw is a defect that prevents responsible proposal drafting unless the idea is substantially redesigned.

## Fatal Flaw Categories

### 1. Unanswerable Research Question

The question cannot be answered by any plausible data, experiment, method, or argument within the stated constraints.

### 2. Undefined Primary Target

There is no endpoint, outcome, metric, deliverable, phenomenon, or decision target that would let the work be evaluated.

### 3. No Credible Data or Evidence Path

The required data, system, corpus, sample, experiment, or literature base is unavailable, inaccessible, or not specified enough to support the proposal.

### 4. Data-Question Mismatch

The available data or evidence cannot answer the proposed question.

### 5. Method-Object Mismatch

The implied method cannot validly study the stated object or test the stated claim.

### 6. User Goal Mismatch

The idea does not fit the user's stated goal, output type, audience, or practical constraints.

### 7. Data-Access or Operational Blocker

Known constraints prevent the proposed work from being conducted as framed.

### 8. Non-Research Request

The input is not a research idea, research problem, research plan, or proposal-oriented request.

### 9. Pure Topic Without Claim or Question

The input is only a topic area and lacks any question, aim, objective, hypothesis, target, or value claim.

## Handling

If a fatal flaw is repairable through a small clarification, return `needs_clarification`.

If repair requires idea generation, narrowing, comparison, or reframing, return `needs_idea_refinement`.

If the flaw is methodological and may be resolved by specialist review, return `needs_methodology_preflight`.

If it is not repairable with current information, return `not_proposalizable_yet`.
