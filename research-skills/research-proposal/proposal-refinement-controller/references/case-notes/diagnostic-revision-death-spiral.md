# Case Note: Diagnostic: Multi-Reviewer Proposal Death Spiral

## Symptoms

A proposal undergoing multiple review-revise cycles exhibits progressive degradation:

1. **Blind growth**: word count doubles or triples across revisions (v2: 23KB → v7: 45KB)
2. **Claim collapse**: the core thesis shifts from "we will do X" to "we might do X, or maybe Y"
3. **Reviewer-response sedimentation**: proposal body accumulates language that addresses reviewer criticism
4. **Caveat overrun**: the core claim accumulates >2 layers of hedging conditionals
5. **"Two-tier delivery"**: the proposal papers over a promise-capability gap with a dual-track fallback

## Mechanism

Each reviewer is individually right about their concern. But satisfying all reviewers simultaneously produces a document that satisfies none. The skeptical reviewer plays an outsized role — legitimate concerns get amplified by consensus-seeking across the panel.

## Prevention (built into v1.3+)

1. **Dual-file revision**: drafter produces (a) revised proposal + (b) separate response-to-reviewers file
2. **Caveat budget**: refinement-controller triggers stop_no_gain when core claim exceeds 2 layers of hedging
3. **Thesis integrity check**: evaluator assesses whether core thesis is sharper or blurrier; if blurrier, direction is deletion
4. **Thesis-integrity reviewer**: panel reviewer whose sole concern is thesis health

## Response When Detected

Do not attempt another revision round. Return to orchestrator with stop_no_gain. The fix is choosing which reviewer to disappoint — not satisfying all of them.
