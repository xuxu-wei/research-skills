# Wiki Contract

Use this contract when creating or changing an LLM Wiki.

## Root Files

- `CLAUDE.md`, `AGENTS.md`, or another root Markdown config file: platform
  specific instructions for agents operating in the wiki.
- `README.md`: human-facing guide to structure, workflow, commands, tips, and
  maintenance.
- `index.md`: generated or maintained catalog of wiki pages.
- `log.md`: append-only timeline of actions.

## Directory Layout

```text
raw/inbox/        New materials before classification.
raw/articles/     Web articles, blog posts, documentation, clippings.
raw/papers/       Papers, books, chapters, reports, preprints, PDFs, EPUBs.
raw/transcripts/  Meetings, interviews, lectures, captions, chats.
raw/data/         CSV, TSV, JSON, spreadsheets, datasets.
raw/media/        Images, audio, video, diagrams, attachments.
sources/          One source summary per substantive source.
entities/         People, organizations, products, datasets, tools, projects.
concepts/         Concepts, methods, phenomena, definitions, topic notes.
syntheses/        Cross-source synthesis and state-of-knowledge pages.
comparisons/      Side-by-side analyses.
queries/          Durable filed answers worth reusing.
_meta/            Taxonomies, maps, dashboards, lint reports, admin notes.
_archive/         Superseded or out-of-scope pages.
```

## Naming

- Use lowercase slugs with hyphens and `.md`.
- Keep raw filenames descriptive and stable.
- Prefer one page per durable entity or concept.
- Do not create pages for passing mentions.
- Split pages over roughly 200 lines.

## Agent Config Selection

Initialize the root agent contract according to the active ecosystem:

- Claude Code: `CLAUDE.md`.
- Codex/OpenAI agents: `AGENTS.md`.
- Other agents: use `AGENTS.md` by default, or pass an explicit root Markdown
  filename when initializing.

If the selected config file already exists, append the LLM Wiki contract under
a marked section instead of overwriting unrelated project instructions.

## Page Frontmatter

Wiki pages should use:

```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: source | entity | concept | synthesis | comparison | query
tags: [tag]
sources: [sources/source-slug.md]
summary: One-line summary for index.md
confidence: high | medium | low
status: active | contested | superseded | archived
---
```

`confidence` and `status` are especially important for fast-moving topics,
single-source claims, or unresolved contradictions.

## Scientific Source Metadata

For papers, books, chapters, reports, and other scientific literature, source
summary pages should include these fields when available:

```yaml
source_kind: paper | preprint | book | chapter | report | thesis | dataset
authors: [Family Name, Given Name]
year: 2026
venue: Journal or conference name
publisher: Publisher name
doi: 10.xxxx/yyyy
isbn: 000-0-00-000000-0
url: https://example.org/source
```

Use `venue` for journals, conferences, repositories, and proceedings. Use
`publisher` for books and formal reports. If a required bibliographic field is
unknown, write `unknown` rather than inventing it.

## Source Summary Raw Provenance

Every substantive `sources/` page should point back to its raw source and, when
available, record the raw source hash:

```yaml
raw_source: raw/papers/source-file.pdf
raw_hash_scheme: sha256_bytes_v1
raw_sha256: hex-digest
raw_hashed_at: YYYY-MM-DD
```

Use stable slug/path identifiers for raw files and source summaries. Do not
introduce sequential integer IDs unless a separate user workflow explicitly
requires them.

## Raw Source Metadata

Text raw sources may use:

```yaml
---
source_url: https://example.org/source
ingested: YYYY-MM-DD
sha256: hex-digest
hash_scheme: sha256_body_v1
hashed_at: YYYY-MM-DD
source_kind: article | paper | book | transcript | dataset | media
---
```

`sha256_body_v1` is computed over UTF-8 or UTF-8 BOM text after frontmatter is
excluded and newlines are normalized to LF. Raw binary files use
`sha256_bytes_v1`, computed over raw bytes, and are tracked from their source
summary page.

Hash drift means the source version changed; it does not by itself prove the
wiki interpretation is wrong. Use `wiki_tools.py health <wiki-path>` to locate
affected source summaries and dependent pages before updating knowledge pages.

## Link Rules

- Use `[[wikilinks]]` for internal wiki links.
- New durable pages should link to at least two related pages when such pages
  exist.
- When a page is archived, remove it from `index.md` and update incoming links.
- Broken links are higher priority than orphan pages.

## Tag Rules

- Define tag taxonomy in `AGENTS.md` or `_meta/tags.md`.
- Add a tag to the taxonomy before using it.
- Prefer a small stable vocabulary over many near-duplicates.

## Lifecycle

- `raw/inbox`: unprocessed.
- classified raw source: preserved original.
- `sources/`: source interpreted and bibliographically described.
- durable page: linked and indexed.
- synthesis/comparison/query: filed only when reuse value is high.
- `_archive`: superseded or out-of-scope material.
