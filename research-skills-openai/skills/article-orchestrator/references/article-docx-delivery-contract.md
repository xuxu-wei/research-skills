# Article DOCX Delivery Contract

Read this contract when producing a user-facing article draft or final package
with DOCX-capable ChatGPT/Codex document tooling.

## Authority and files

- Keep `06_drafts/manuscript-vNNN.md` as the canonical content, lineage, diff,
  and scientific-review source. Every version must be a complete manuscript.
- Treat the synchronized `manuscript-vNNN.docx` as the primary user-facing
  draft. Put the final verified copy under `12_package/`.
- Register `04_blueprint/display-asset-manifest.yaml` as the authority for every
  main-text and supplementary table or figure.
- A DOCX is a faithful format transform, not a new substantive version. Any
  changed prose, data, table content, caption, claim, or evidence link requires
  a new Markdown version and fresh independent scientific evaluation.

## Display asset manifest

For each display record its ID, `table | figure`, source path and SHA-256,
`main | supplement`, intended order/location, caption, manuscript callout,
availability (`available | missing_source_asset | pending_confirmation`), image
alt text when applicable, DOCX embedding status, and render status.

- Use native Word tables for tabular data; do not substitute screenshots.
- Embed available figures at readable resolution with captions and alt text.
- Keep numbering, captions, callouts, ordering, and supplementary references
  consistent. Do not invent unavailable data or assets.
- A required missing asset may have a clearly labeled development placeholder,
  but it blocks `human_signoff_required`.

## Formatting and parity

Use a restrained scientific-manuscript style or a supplied template. Use real
Word heading, body, caption, and numbering styles; explicit table geometry and
repeating headers; readable margins; and deliberate figure placement. Do not
implement target-journal styling without a verified adapter or user template.

Extract and normalize headings, body text, table cells, and captions from the
DOCX. Compare them with the frozen Markdown and display manifest. Record:

```yaml
canonical_markdown_ref: ""
canonical_content_digest: "sha256:"
docx_ref: ""
docx_content_digest: "sha256:"
display_manifest_ref: "04_blueprint/display-asset-manifest.yaml"
docx_sync_status: synchronized | content_drift | not_generated
render_qa_status: passed | docx_visual_qa_pending | failed | not_generated
```

`content_drift` invalidates the DOCX and routes back to faithful composition;
it does not authorize the compositor to repair the source.

## Render gate and fallback

Use the available document skill/tooling to render the DOCX to page PNGs and
inspect every page at 100% zoom. Re-render after every layout-sensitive change.
Check clipping, overlap, blank pages, page breaks, table width, repeated headers,
figure readability, captions, cross-references, and missing glyphs.

- If rendering is unavailable, return `docx_visual_qa_pending` and do not claim
  visual QA or `human_signoff_required`.
- If DOCX generation is unavailable, retain the canonical Markdown, emit a
  self-contained continuation package, and return `docx_generation_pending`.
- Keep PNG/PDF QA intermediates internal unless the user requests them.
