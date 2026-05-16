# Reviewer Panel Roles

This reference defines the default reviewer roles for `proposal-review-panel`.

## Panel Tiers

### lightweight_panel

Three reviewers:

- domain expert reviewer: `narrow-domain reviewer`, or `practicing-clinician reviewer` when the proposal involves medicine, clinical practice, or public health;
- methodology / statistics reviewer;
- submission-guard reviewer.

Use for fast pre-submission critique, early mock review, or when the user asks for a smaller review.

### standard_panel

Five reviewers, and the default tier:

- broad-field reviewer;
- domain expert reviewer: `narrow-domain reviewer`, or `practicing-clinician reviewer` for medicine, clinical practice, or public health;
- methodology / statistics reviewer;
- skeptical reviewer;
- submission-guard reviewer.

### full_panel

Seven reviewers:

- broad-field reviewer;
- domain expert reviewer: `narrow-domain reviewer`, or `practicing-clinician reviewer` for medicine, clinical practice, or public health;
- methodology / statistics reviewer;
- cross-disciplinary senior reviewer;
- translational / end-user reviewer;
- skeptical reviewer;
- submission-guard reviewer.

The clinical rule fills the domain expert slot; it does not add an eighth reviewer unless the user explicitly requests both a narrow-domain reviewer and a practicing-clinician reviewer.

## Reviewer Role Definitions

### broad-field reviewer
Evaluates whether the proposal is important, understandable, and defensible to a knowledgeable non-specialist in the broader field.

Primary concerns:
- significance and positioning;
- clarity of research question;
- fit with field-level trends;
- whether the proposal sounds important beyond a narrow niche.

### narrow-domain reviewer
Evaluates technical and conceptual fit within the specific research domain.

Primary concerns:
- domain-specific novelty;
- adequacy of literature positioning;
- whether the proposed gap is real;
- whether aims and methods align with current domain standards.

### methodology / statistics reviewer
Evaluates study design, methods, analytic logic, endpoint-method fit, bias, confounding, and feasibility.

Primary concerns:
- internal validity;
- data-method fit;
- whether the methods can answer the research question;
- endpoint / outcome / metric clarity;
- statistical or methodological risks.

### cross-disciplinary senior reviewer
Evaluates conceptual maturity, strategic framing, feasibility across fields, and long-term research value.

Primary concerns:
- whether the proposal is overextended;
- whether cross-disciplinary claims are justified;
- integration across domains;
- senior-level reviewer defensibility.

### translational / end-user reviewer
Evaluates applied value, clinical / engineering / social relevance, implementation barriers, and stakeholder usefulness.

Primary concerns:
- real-world need;
- deliverable usefulness;
- implementation path;
- whether the expected outcomes matter to users or stakeholders.

### skeptical reviewer
Actively searches for hidden weaknesses, overclaims, unproven assumptions, fatal flaws, and likely reviewer attack points.

Primary concerns:
- unsupported novelty;
- feasibility gaps;
- vague endpoints;
- inflated impact;
- weak evidence;
- unresolved methodological risks.

### submission-guard reviewer
Evaluates the clarity, consistency, and anti-sedimentation health of the proposal's core claim across revisions, and performs pre-submission archival cleanup.

Primary concerns:
- core claim clarity: can the primary claim be stated in one sentence without nested conditionals?
- caveat accumulation: has revision added hedging layers that obscure the claim?
- reviewer-response sedimentation: does the body contain language that reads as reply to criticism?
- self-hedging: does the proposal acknowledge a gap between promises and deliverability, then paper over it?
- claim-drift: has the central claim shifted substantively without acknowledgment?
- archival cleanup: narrative clinical scenes, Socratic rhetorical questions, explanatory term dictionaries, version markers — all flagged for removal.

### practicing-clinician reviewer
Evaluates from the perspective of a doctor who currently treats patients — clinical importance, endpoint relevance, narrative credibility, and actionability.

Primary concerns:
- clinical importance: does the research question address a real problem from practice?
- endpoint relevance: do outcomes matter to patients and clinicians, or only to methodologists?
- credibility of clinical narrative: does the framing ring true, or feel like a methodologist's caricature?
- actionability: if the method succeeds, what changes on Monday morning?
- communication: can a clinician understand the aims without specialized statistical training?

## Role Use Rules

- Each reviewer must be run independently.
- Each reviewer should use the same proposal file but a role-specific evaluation stance.
- Reviewers must not see other reviewer outputs before submitting their own review.
- The default panel tier is `standard_panel`.
- The skeptical reviewer is enabled by default unless the user explicitly disables it. If disabled, record lower panel confidence.
- The submission-guard reviewer is mandatory and must not be deleted.
- The practicing-clinician reviewer is mandatory as the domain expert when the proposal domain involves medicine, clinical practice, or public health.
