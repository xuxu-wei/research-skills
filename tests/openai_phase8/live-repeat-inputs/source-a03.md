# Frozen synthetic Perspective source bundle

```yaml
artifact_id: source-a03
version_id: v005
workflow_id: workflow-a03
round_id: r005
plugin_version: 0.6.0-preview.1
source_skill: perspective-drafter
created_by_instance_id: writer-a03
based_on: [source-a03@v004, perspective-context-source@v001, perspective-evidence-ledger-source@v001, stakeholder-source-notes@v001, discourse-baseline-source@v001, outlet-profile-source@v001, threshold-method-source@v001]
change_type: author_update
frozen: true
anonymity: Synthetic case; no person, institution, unpublished dataset, or user source is represented.
```

## Thesis and source evidence

Thesis: organizations adopting a synthetic monitoring practice should pair it
with periodic local reassessment and recalibrate when monitored drift exceeds
a prespecified local tolerance, rather than assume transportability.

The frozen evidence ledger contains findings that performance drift occurred
under documented setting changes, recalibration reduced measured drift in the
represented settings, and implementation cost varied. The source set contains
no evidence of universal effectiveness, a causal mortality effect, or a
mandatory policy. Two studies found little drift in stable settings.

The frozen discourse baseline covers recent general-methods commentaries in
the represented source set. Those commentaries discuss transportability or
fixed-interval recalibration separately; none combines a prespecified local
drift tolerance, conditional recalibration, and an explicit implementation-
burden record. The bounded contribution is that combined decision rule, not a
claim to universal novelty. The intended outlet profile accepts a concise,
evidence-bounded methods Perspective with an actionable counterposition and no
target-specific submission assertions.

The threshold-method source defines local tolerance before monitoring from a held-
out validation period, the minimum operationally meaningful drift, and the
documented cost of false alarms. Teams must validate that tolerance locally,
record changes to it, and treat it as a decision threshold rather than a causal
effect estimate.

## Draft excerpt

Distribution shift can make a fixed monitoring threshold unreliable after a
documented setting change. In the represented studies, local recalibration
reduced measured drift after such changes, while two studies in stable settings
found little drift. These observations do not establish universal effectiveness
or a causal mortality benefit.

Organizations that observe a documented distribution change should test local
calibration before continuing to rely on the original threshold. The evidence
does not establish a default reassessment interval. A stakeholder source argues
that annual reassessment may impose needless burden in stable settings; local
teams should therefore predefine cadence from observed stability and expected
implementation burden, then record actual burden and why the chosen interval
remains appropriate. A testable decision rule is to
recalibrate when observed monitored drift exceeds the prespecified local
tolerance and to retain
the original threshold otherwise. The tolerance is fixed from held-out local
validation data, a minimum meaningful drift, and false-alarm costs before the
monitoring interval begins; it is an operational decision threshold, not a
causal-effect estimate, and any later change is versioned and justified. Once
the drift trigger is crossed, burden informs implementation planning but does
not erase the documented loss of calibration.
