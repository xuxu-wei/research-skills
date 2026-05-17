# LLM Wiki Agent Contract

This directory is an LLM Wiki. It is designed for Claude Code style agent
collaboration over plain Markdown files.

## Purpose

Describe the domain here.

## Agent Contract

- Orient before changing the wiki: read this agent config file, `README.md`,
  `index.md`, and recent `log.md`.
- Preserve raw sources under `raw/`; do not rewrite them as interpretation
  changes.
- Prefer updating existing durable pages over creating duplicates.
- Add new durable pages to `index.md`.
- Append every ingest, query filing, lint, archive, schema change, or major
  maintenance action to `log.md`.
- Use `wiki_tools.py health` before updating pages because of source drift.
- Confirm before schema changes, deletion, mass archival, or any operation
  expected to touch more than 10 wiki pages.

## Directory Contract

See `README.md` for the human-facing description. Required directories:

- `raw/inbox/`
- `raw/articles/`
- `raw/papers/`
- `raw/transcripts/`
- `raw/data/`
- `raw/media/`
- `sources/`
- `entities/`
- `concepts/`
- `syntheses/`
- `comparisons/`
- `queries/`
- `_meta/`
- `_archive/`

## Page Rules

- Use lowercase hyphenated slugs.
- Use Obsidian-style `[[wikilinks]]` for internal links.
- Use frontmatter on all wiki pages.
- Keep source summaries separate from synthesis pages.
- Mark low-confidence or contested claims explicitly.
- Split pages over roughly 200 lines.

## Tag Taxonomy

Add tags here before using them.

- source
- entity
- concept
- synthesis
- comparison
- query
- contested
- archived

## Scientific Literature Rules

For papers, books, chapters, reports, theses, datasets, and other scientific
sources, capture citation metadata when available:

- authors
- title
- year
- venue or publisher
- DOI
- ISBN
- URL
- source kind

If a bibliographic field is unknown, write `unknown`; do not invent it.
