# Phase 2 Targeted Search Smoke Test

Date: 2026-07-12
Capability: ChatGPT/Codex built-in Search
Route: targeted/current authoritative-source verification
Local retrieval scripts used: no

## Question

What is the current CONSORT statement for reporting randomized trials, how many
checklist items does it contain, and where was the statement published?

## Search and Open Trace

1. Searched for the official CONSORT 2025 statement, DOI, and PubMed identity.
2. Opened the EQUATOR Network CONSORT 2025 guideline record:
   <https://www.equator-network.org/reporting-guidelines/consort/>
3. Opened the official SPIRIT-CONSORT home page:
   <https://www.consort-spirit.org/>
4. Opened the official published-statements page:
   <https://www.consort-spirit.org/published-statements>
5. BMJ and PubMed pages were also attempted but returned access challenges in
   this environment; they were not treated as opened verification sources.

## Observed Result

This is a self-attested source-verification snapshot from the task that
created the report. It is useful as a routing smoke but is not durable platform
tool provenance and does not satisfy a current-release live gate.

- The current generic reporting guideline is CONSORT 2025 for reports of
  randomized trials.
- The official SPIRIT-CONSORT site describes a 30-item checklist plus a flow
  diagram.
- The EQUATOR and SPIRIT-CONSORT records agree that the statement was published
  simultaneously in BMJ, JAMA, The Lancet, Nature Medicine, and PLOS Medicine.
- The BMJ version is identified as DOI `10.1136/bmj-2024-081123`; the official
  publication page also records the JAMA, Lancet, Nature Medicine, and PLOS
  Medicine DOI links.

## Source Verification

| Source | Authority | Opened | Identity/support checked |
|---|---|---:|---|
| EQUATOR guideline record | Reporting-guideline registry | yes | guideline scope, title, journal versions, PMIDs |
| SPIRIT-CONSORT home | Guideline developer site | yes | 30-item checklist, flow diagram, intended use |
| SPIRIT-CONSORT published statements | Guideline developer site | yes | five journal versions and DOI identities |

Status: `self_attested_search_snapshot_validated`
