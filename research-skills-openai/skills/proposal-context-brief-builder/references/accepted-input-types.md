# accepted-input-types

Purpose: define acceptable input types and how to normalize them into a proposal context brief.

## Raw Research Idea

A user-provided idea that may be vague or incomplete.

Handling:
- Preserve the user's wording in source notes if useful.
- Normalize only enough to support triage.
- Mark missing population, data, endpoint, or method as unknown.

## Promoted Idea Package

A structured idea already screened by a research-idea workflow.

Handling:
- Preserve existing title, research question, hypothesis, value claim, method, data, and evaluation summary.
- Carry forward assumptions and uncertainties.
- Do not re-score the idea.

## Funding Call or Grant Requirement

A call for proposals, award description, review criterion, or institutional funding requirement.

Handling:
- Extract target scope, eligibility, required output, deadlines, review priorities, and required sections.
- Distinguish sponsor requirements from the user's research idea.

## Clinical or Practical Problem

A real-world problem without a fully specified research question.

Handling:
- Extract population, setting, decision problem, current gap, and practical value.
- Mark endpoint, comparator, data source, and design as unknown if not stated.

## Data Opportunity

An available dataset, cohort, registry, platform, archive, experiment, or operational data source.

Handling:
- Extract data type, population, coverage, access, time span, key variables, and limitations.
- Do not infer endpoints or causal questions unless stated.

## Literature-Driven Topic

An idea derived from literature review, evidence map, paper set, guideline, or controversy.

Handling:
- Extract the stated gap, controversy, evidence base, and proposed contribution.
- Mark novelty as unverified unless already assessed by a separate evaluator.

## Method-Driven Topic

A proposal centered on a method, model, measurement strategy, benchmark, or analytic technique.

Handling:
- Extract method, target problem, comparator, evaluation metric, data requirement, and expected contribution.
- Distinguish method development from method application.

## User Constraint-Driven Topic

A proposal constrained primarily by available time, data, clinical access, collaborator needs, target journal, or institutional requirement.

Handling:
- Extract constraints first.
- Identify which aspects of the idea are flexible and which are fixed.

## Mixed Input

Many real requests contain multiple input types.

Handling:
- Assign multiple input types when appropriate.
- Do not force a single category.
- Preserve conflicts and uncertainties for triage.
