# Permitted Packaging Operations

The compositor may perform only operations outside source prose:

1. Copy the latest evaluated source without text changes.
2. Create package directories and filenames.
3. Create or update `08_final/package-manifest.md` and proposed canonical-index
   entries; only the orchestrator may write `09_state/artifact-index.md`.
4. Record logical artifact identity, source/evaluated versions, index completeness, and direct text-identity results.
5. Create audit, risk, dissent, fatal-finding, and human-signoff reports.
6. Record proposed edits as return-route requests without applying them.

The compositor must not change formatting, grammar, punctuation, title, abstract,
headings, citations, duplicate wording, terminology, claims, evidence, caveats,
or any other source text. Any required change returns to the drafter, creates a
new version, and requires a fresh evaluator before composition restarts.

Do not calculate or persist SHA, content hashes, or digests for new LLM-facing
artifacts. Legacy digest metadata may be read but is never required, copied forward,
or used as a readiness gate.
