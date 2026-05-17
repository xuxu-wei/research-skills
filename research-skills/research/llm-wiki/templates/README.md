# LLM Wiki README

This wiki is a plain Markdown knowledge base for human-agent collaboration. It
keeps raw materials separate from agent-maintained wiki pages, so knowledge can
compound across sessions instead of being rediscovered from scratch.

## Directory Structure

```text
AGENTS.md          Agent collaboration contract and schema.
README.md          Human-facing guide to workflow and maintenance.
index.md           Catalog of wiki pages.
log.md             Append-only timeline of actions.
raw/inbox/         New materials before classification.
raw/articles/      Web articles, blog posts, documentation, clippings.
raw/papers/        Papers, books, chapters, reports, preprints, PDFs, EPUBs.
raw/transcripts/   Meetings, interviews, lectures, captions, chats.
raw/data/          CSV, TSV, JSON, spreadsheets, datasets.
raw/media/         Images, audio, video, diagrams, attachments.
sources/           Source summaries and citation metadata.
entities/          People, organizations, products, datasets, tools, projects.
concepts/          Concepts, methods, phenomena, definitions, topic notes.
syntheses/         Cross-source synthesis and state-of-knowledge pages.
comparisons/       Side-by-side analyses.
queries/           Durable filed answers worth reusing.
_meta/             Taxonomies, maps, dashboards, lint reports, admin notes.
_archive/          Superseded or out-of-scope pages.
```

## Standard User-Agent-Wiki Workflow

1. User provides a goal, question, or source.
2. Agent orients by reading `AGENTS.md`, this README, `index.md`, and recent
   `log.md`.
3. New material goes into `raw/inbox/`.
4. Agent classifies raw material into `raw/articles/`, `raw/papers/`,
   `raw/transcripts/`, `raw/data/`, or `raw/media/`.
5. Agent creates or updates `sources/` summaries.
6. Agent updates durable pages in `entities/`, `concepts/`, `syntheses/`,
   `comparisons/`, or `queries/`.
7. Agent updates `index.md`.
8. Agent appends an entry to `log.md`.
9. User reviews the result and resolves any contested interpretations.

## Common Commands

Run these from the skill directory or adjust the path to `wiki_tools.py`.

```bash
python scripts/wiki_tools.py init <wiki-path> --domain "domain"
python scripts/wiki_tools.py classify <wiki-path> --move
python scripts/wiki_tools.py hash-source <raw-source-path> --write
python scripts/wiki_tools.py update-index <wiki-path>
python scripts/wiki_tools.py lint <wiki-path>
python scripts/wiki_tools.py health <wiki-path>
python scripts/wiki_tools.py append-log <wiki-path> --action ingest --subject "new source"
```

## Maintenance

- Run lint after bulk ingest or major cleanup.
- Run health when source drift or update scope matters.
- Keep `raw/inbox/` empty unless work is intentionally pending.
- Fix broken wikilinks before style issues.
- Keep `index.md` current.
- If health reports drift, review the affected `sources/` page before updating
  dependent wiki pages.
- Rotate or archive logs when they become too large.
- Archive superseded pages under `_archive/` instead of deleting them.

## Scientific Literature Tips

For papers and books, preserve citation metadata in the matching `sources/`
page: authors, title, year, journal or publisher, DOI, ISBN, URL, and source
kind. Mark missing fields as `unknown`.

## Extra Tips

- Use `[[wikilinks]]` for internal links.
- Use one durable page per durable concept or entity.
- Do not create pages for passing mentions.
- Put long source-specific detail in `sources/`; put cross-source judgment in
  `syntheses/`.
- Mark unresolved disagreements with `status: contested`.
- Confirm before operations that will touch more than 10 pages.
