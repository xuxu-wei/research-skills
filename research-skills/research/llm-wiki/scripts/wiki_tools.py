#!/usr/bin/env python3
"""Cross-platform helper tools for Karpathy-style LLM Wikis.

The script intentionally uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import shutil
from pathlib import Path
from typing import Any


PAGE_DIRS = ["sources", "entities", "concepts", "syntheses", "comparisons", "queries"]
PAGE_TYPE_BY_DIR = {
    "sources": "source",
    "entities": "entity",
    "concepts": "concept",
    "syntheses": "synthesis",
    "comparisons": "comparison",
    "queries": "query",
}
RAW_DIRS = ["raw/inbox", "raw/articles", "raw/papers", "raw/transcripts", "raw/data", "raw/media"]
META_DIRS = ["_meta", "_archive"]
ROOT_FILES = ["AGENTS.md", "README.md", "index.md", "log.md"]
VALID_TYPES = {"source", "entity", "concept", "synthesis", "comparison", "query"}
SCIENTIFIC_KINDS = {"paper", "preprint", "book", "chapter", "report", "thesis", "dataset"}
REQUIRED_PAGE_FIELDS = ["title", "created", "updated", "type", "tags", "sources", "summary"]
REQUIRED_CITATION_FIELDS = ["authors", "year", "venue", "publisher", "doi", "isbn", "url", "source_kind"]
HASH_SCHEME_TEXT = "sha256_body_v1"
HASH_SCHEME_BYTES = "sha256_bytes_v1"
VALID_HASH_SCHEMES = {HASH_SCHEME_TEXT, HASH_SCHEME_BYTES}
TEXT_HASH_EXTS = {
    ".bib",
    ".csv",
    ".htm",
    ".html",
    ".json",
    ".jsonl",
    ".md",
    ".ris",
    ".srt",
    ".tsv",
    ".txt",
    ".vtt",
    ".xml",
    ".yaml",
    ".yml",
}


def today() -> str:
    return dt.date.today().isoformat()


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def template_path(name: str) -> Path:
    return skill_root() / "templates" / name


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def read_utf8_text_for_hash(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{path}: invalid UTF-8 text for {HASH_SCHEME_TEXT}") from exc
    return normalize_newlines(text)


def render_template(name: str, values: dict[str, str]) -> str:
    text = read_text(template_path(name))
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text.replace("{{date}}", today())


def frontmatter_block(text: str) -> tuple[dict[str, Any], str, bool]:
    if not text.startswith("---"):
        return {}, text, False
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if not match:
        return {}, text, False
    raw_fm, body = match.group(1), match.group(2)
    return parse_simple_yaml(raw_fm), body, True


def parse_simple_yaml(raw: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current_key: str | None = None
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")) and current_key and line.strip().startswith("- "):
            data.setdefault(current_key, [])
            if isinstance(data[current_key], list):
                data[current_key].append(clean_scalar(line.strip()[2:]))
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        current_key = key
        data[key] = parse_value(value)
    return data


def parse_value(value: str) -> Any:
    if value == "":
        return ""
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [clean_scalar(part.strip()) for part in inner.split(",")]
    return clean_scalar(value)


def clean_scalar(value: str) -> str:
    value = value.strip()
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    return value


def dump_simple_yaml(data: dict[str, Any]) -> str:
    lines: list[str] = []
    for key, value in data.items():
        if isinstance(value, list):
            if not value:
                lines.append(f"{key}: []")
            else:
                rendered = ", ".join(str(item) for item in value)
                lines.append(f"{key}: [{rendered}]")
        else:
            lines.append(f"{key}: {value}")
    return "\n".join(lines) + "\n"


def body_hash_for_text(path: Path) -> str:
    text = read_utf8_text_for_hash(path)
    _fm, body, has_fm = frontmatter_block(text)
    content = body if has_fm else text
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def bytes_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def default_hash_scheme(path: Path) -> str:
    return HASH_SCHEME_TEXT if path.suffix.lower() in TEXT_HASH_EXTS else HASH_SCHEME_BYTES


def compute_source_hash(path: Path, scheme: str | None = None) -> tuple[str, str]:
    selected = scheme or default_hash_scheme(path)
    if selected == HASH_SCHEME_TEXT:
        return body_hash_for_text(path), selected
    if selected == HASH_SCHEME_BYTES:
        return bytes_hash(path), selected
    raise ValueError(f"{path}: unsupported hash_scheme {selected!r}")


def normalize_wiki_rel(value: Any) -> str:
    text = str(value or "").strip()
    if text.lower() in {"", "unknown", "none", "null"}:
        return ""
    return text.replace("\\", "/").lstrip("./")


def list_value(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, str) and value:
        return [value]
    return []


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "untitled"


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    stem, suffix = path.stem, path.suffix
    parent = path.parent
    index = 2
    while True:
        candidate = parent / f"{stem}-{index}{suffix}"
        if not candidate.exists():
            return candidate
        index += 1


def classify_file(path: Path) -> str:
    suffix = path.suffix.lower()
    name = path.name.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".mp3", ".wav", ".mp4", ".mov", ".m4a"}:
        return "raw/media"
    if suffix in {".pdf", ".epub", ".mobi"}:
        return "raw/papers"
    if suffix in {".csv", ".tsv", ".json", ".jsonl", ".xlsx", ".xls", ".parquet", ".sav", ".dta"}:
        return "raw/data"
    if suffix in {".vtt", ".srt"} or any(token in name for token in ["transcript", "interview", "meeting", "lecture"]):
        return "raw/transcripts"
    if suffix in {".md", ".txt", ".html", ".htm"}:
        try:
            text = read_text(path)[:4000].lower()
        except OSError:
            text = ""
        if any(token in text for token in ["doi:", "abstract", "journal", "isbn", "publisher"]):
            return "raw/papers"
        if any(token in text for token in ["speaker:", "transcript", "interview"]):
            return "raw/transcripts"
        return "raw/articles"
    return "raw/articles"


def iter_page_files(wiki: Path) -> list[Path]:
    files: list[Path] = []
    for folder in PAGE_DIRS:
        root = wiki / folder
        if root.exists():
            files.extend(sorted(path for path in root.rglob("*.md") if path.is_file()))
    return sorted(files)


def wiki_link_target(link: str) -> str:
    link = link.split("|", 1)[0].split("#", 1)[0].strip()
    if link.endswith(".md"):
        link = link[:-3]
    return link.replace("\\", "/")


def page_key(path: Path, wiki: Path) -> str:
    rel = path.relative_to(wiki).as_posix()
    return rel[:-3] if rel.endswith(".md") else rel


def extract_wikilinks(text: str) -> list[str]:
    return [wiki_link_target(match.group(1)) for match in re.finditer(r"\[\[([^\]]+)\]\]", text)]


def first_summary(body: str) -> str:
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith(">") or stripped.startswith("- "):
            continue
        return stripped[:180]
    return ""


def tags_from_agents(wiki: Path) -> set[str]:
    path = wiki / "AGENTS.md"
    if not path.exists():
        return set()
    text = read_text(path)
    tags: set[str] = set()
    in_taxonomy = False
    for line in text.splitlines():
        if re.match(r"^##+\s+(Tag Taxonomy|Evidence Tags)\b", line, re.I):
            in_taxonomy = True
            continue
        if in_taxonomy and line.startswith("#"):
            in_taxonomy = False
            continue
        if in_taxonomy:
            match = re.match(r"\s*-\s+`?([A-Za-z0-9_/-]+)`?", line)
            if match:
                tags.add(match.group(1))
    return tags


def command_init(args: argparse.Namespace) -> int:
    wiki = Path(args.wiki).expanduser().resolve()
    values = {"domain": args.domain}
    for rel in RAW_DIRS + PAGE_DIRS + META_DIRS:
        (wiki / rel).mkdir(parents=True, exist_ok=True)
    for name in ROOT_FILES:
        target = wiki / name
        if target.exists() and not args.force:
            continue
        write_text(target, render_template(name, values))
    if args.research:
        add_on = render_template("research-schema.md", values)
        agents = wiki / "AGENTS.md"
        current = read_text(agents)
        if "Research Schema Add-on" not in current:
            write_text(agents, current.rstrip() + "\n\n" + add_on)
    print(json.dumps({"wiki": str(wiki), "created": True}, indent=2))
    return 0


def command_classify(args: argparse.Namespace) -> int:
    wiki = Path(args.wiki).expanduser().resolve()
    inbox = wiki / "raw" / "inbox"
    results: list[dict[str, str]] = []
    if not inbox.exists():
        print(json.dumps({"wiki": str(wiki), "classified": []}, indent=2))
        return 0
    for path in sorted(item for item in inbox.iterdir() if item.is_file()):
        target_dir = wiki / classify_file(path)
        target = unique_path(target_dir / path.name)
        if args.move:
            target_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(path), str(target))
        results.append({"source": str(path), "target": str(target), "moved": str(bool(args.move)).lower()})
    print(json.dumps({"wiki": str(wiki), "classified": results}, indent=2))
    return 0


def command_hash_source(args: argparse.Namespace) -> int:
    path = Path(args.path).expanduser().resolve()
    try:
        digest, scheme = compute_source_hash(path)
    except (OSError, ValueError) as exc:
        print(json.dumps({"path": str(path), "error": str(exc)}, indent=2))
        return 2
    written = False
    if args.write:
        if scheme != HASH_SCHEME_TEXT:
            print(
                json.dumps(
                    {
                        "path": str(path),
                        "hash_scheme": scheme,
                        "sha256": digest,
                        "error": "--write is only supported for UTF-8 text sources",
                    },
                    indent=2,
                )
            )
            return 2
        text = read_utf8_text_for_hash(path)
        fm, body, has_fm = frontmatter_block(text)
        fm["sha256"] = digest
        fm["hash_scheme"] = scheme
        fm["hashed_at"] = today()
        fm.setdefault("ingested", today())
        new_text = "---\n" + dump_simple_yaml(fm) + "---\n" + (body if has_fm else text)
        write_text(path, new_text)
        written = True
    print(json.dumps({"path": str(path), "hash_scheme": scheme, "sha256": digest, "written": written}, indent=2))
    return 0


def command_update_index(args: argparse.Namespace) -> int:
    wiki = Path(args.wiki).expanduser().resolve()
    sections = {
        "source": "Sources",
        "entity": "Entities",
        "concept": "Concepts",
        "synthesis": "Syntheses",
        "comparison": "Comparisons",
        "query": "Queries",
    }
    entries: dict[str, list[str]] = {section: [] for section in sections.values()}
    for path in iter_page_files(wiki):
        text = read_text(path)
        fm, body, _has_fm = frontmatter_block(text)
        page_type = str(fm.get("type") or PAGE_TYPE_BY_DIR.get(path.parent.name, "concept"))
        section = sections.get(page_type, "Concepts")
        title = str(fm.get("title") or path.stem.replace("-", " ").title())
        summary = str(fm.get("summary") or first_summary(body) or "No summary.")
        target = page_key(path, wiki)
        entries.setdefault(section, []).append(f"- [[{target}|{title}]] - {summary}")
    lines = [
        "# Wiki Index",
        "",
        "> Catalog of wiki pages. Keep one concise line per durable page.",
        f"> Last updated: {today()} | Total pages: {sum(len(v) for v in entries.values())}",
        "",
    ]
    for section in ["Sources", "Entities", "Concepts", "Syntheses", "Comparisons", "Queries"]:
        lines.append(f"## {section}")
        lines.append("")
        lines.extend(sorted(entries.get(section, [])))
        lines.append("")
    write_text(wiki / "index.md", "\n".join(lines).rstrip() + "\n")
    print(json.dumps({"wiki": str(wiki), "pages": sum(len(v) for v in entries.values())}, indent=2))
    return 0


def lint_wiki(wiki: Path) -> dict[str, list[str]]:
    issues: dict[str, list[str]] = {
        "missing_root_files": [],
        "inbox_files": [],
        "missing_frontmatter": [],
        "missing_fields": [],
        "invalid_types": [],
        "missing_citation_metadata": [],
        "broken_links": [],
        "orphan_pages": [],
        "missing_index_entries": [],
        "tag_drift": [],
        "source_hash_drift": [],
        "oversized_pages": [],
        "log_rotation": [],
    }
    for name in ROOT_FILES:
        if not (wiki / name).exists():
            issues["missing_root_files"].append(name)
    inbox = wiki / "raw" / "inbox"
    if inbox.exists():
        issues["inbox_files"].extend(str(path.relative_to(wiki)) for path in sorted(inbox.iterdir()) if path.is_file())
    page_files = iter_page_files(wiki)
    known_pages = {page_key(path, wiki): path for path in page_files}
    known_stems = {path.stem: path for path in page_files}
    inbound: dict[str, int] = {key: 0 for key in known_pages}
    indexed = read_text(wiki / "index.md") if (wiki / "index.md").exists() else ""
    allowed_tags = tags_from_agents(wiki)
    for path in page_files:
        rel = path.relative_to(wiki).as_posix()
        text = read_text(path)
        fm, body, has_fm = frontmatter_block(text)
        if not has_fm:
            issues["missing_frontmatter"].append(rel)
            fm = {}
            body = text
        missing: list[str] = []
        for field in REQUIRED_PAGE_FIELDS:
            value = fm.get(field)
            if field not in fm or value == "" or (field == "tags" and value == []):
                missing.append(field)
        if missing:
            issues["missing_fields"].append(f"{rel}: {', '.join(missing)}")
        page_type = str(fm.get("type", ""))
        if page_type and page_type not in VALID_TYPES:
            issues["invalid_types"].append(f"{rel}: {page_type}")
        if page_type == "source" or path.parent.name == "sources":
            kind = str(fm.get("source_kind", "")).lower()
            if kind in SCIENTIFIC_KINDS:
                missing_citation = [field for field in REQUIRED_CITATION_FIELDS if field not in fm or fm.get(field) in ("", [])]
                if missing_citation:
                    issues["missing_citation_metadata"].append(f"{rel}: {', '.join(missing_citation)}")
        tags = fm.get("tags", [])
        if isinstance(tags, str):
            tags = [tags]
        if allowed_tags:
            for tag in tags:
                if tag not in allowed_tags:
                    issues["tag_drift"].append(f"{rel}: {tag}")
        for link in extract_wikilinks(text):
            if not link:
                continue
            if link in known_pages:
                inbound[link] += 1
            elif link in known_stems:
                inbound[page_key(known_stems[link], wiki)] += 1
            else:
                issues["broken_links"].append(f"{rel}: [[{link}]]")
        if page_key(path, wiki) not in indexed and path.stem not in indexed:
            issues["missing_index_entries"].append(rel)
        if len(text.splitlines()) > 200:
            issues["oversized_pages"].append(rel)
    for key, count in sorted(inbound.items()):
        if count == 0 and not key.startswith("sources/"):
            issues["orphan_pages"].append(key + ".md")
    raw_root = wiki / "raw"
    if raw_root.exists():
        for path in sorted(raw_root.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in TEXT_HASH_EXTS:
                continue
            fm, _body, has_fm = frontmatter_block(read_text(path))
            expected = fm.get("sha256") if has_fm else None
            if expected:
                rel = path.relative_to(wiki).as_posix()
                scheme = str(fm.get("hash_scheme") or HASH_SCHEME_TEXT)
                try:
                    actual, _used_scheme = compute_source_hash(path, scheme)
                except (OSError, ValueError) as exc:
                    issues["source_hash_drift"].append(f"{rel}: {exc}")
                    continue
                if str(expected) != actual:
                    issues["source_hash_drift"].append(f"{rel}: {scheme}")
    log_path = wiki / "log.md"
    if log_path.exists() and read_text(log_path).count("\n## [") > 500:
        issues["log_rotation"].append("log.md has more than 500 entries")
    return issues


def command_lint(args: argparse.Namespace) -> int:
    wiki = Path(args.wiki).expanduser().resolve()
    issues = lint_wiki(wiki)
    total = sum(len(items) for items in issues.values())
    if args.json:
        print(json.dumps({"wiki": str(wiki), "total_issues": total, "issues": issues}, indent=2))
    else:
        print(f"Wiki: {wiki}")
        print(f"Total issues: {total}")
        for name, items in issues.items():
            if not items:
                continue
            print(f"\n{name}:")
            for item in items:
                print(f"- {item}")
    return 1 if total and args.fail_on_issues else 0


def source_page_records(wiki: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in iter_page_files(wiki):
        text = read_text(path)
        fm, _body, _has_fm = frontmatter_block(text)
        page_type = str(fm.get("type", ""))
        if page_type == "source" or path.parent.name == "sources":
            records.append({"path": path, "rel": path.relative_to(wiki).as_posix(), "fm": fm, "text": text})
    return records


def normalized_page_ref(value: Any) -> str:
    rel = normalize_wiki_rel(value)
    return rel[:-3] if rel.endswith(".md") else rel


def source_aliases(path: Path, wiki: Path) -> set[str]:
    key = page_key(path, wiki)
    return {key, path.stem}


def source_pages_for_raw(raw_rel: str, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized = normalize_wiki_rel(raw_rel)
    return [record for record in records if normalize_wiki_rel(record["fm"].get("raw_source")) == normalized]


def affected_pages_for_source(wiki: Path, source_path: Path) -> list[str]:
    aliases = source_aliases(source_path, wiki)
    affected: list[str] = []
    for path in iter_page_files(wiki):
        if path == source_path:
            continue
        text = read_text(path)
        fm, _body, _has_fm = frontmatter_block(text)
        source_refs = {normalized_page_ref(item) for item in list_value(fm.get("sources"))}
        wikilinks = set(extract_wikilinks(text))
        if aliases & source_refs or aliases & wikilinks:
            affected.append(path.relative_to(wiki).as_posix())
    return sorted(affected)


def collect_raw_frontmatter_drift(wiki: Path, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    drifted: list[dict[str, Any]] = []
    raw_root = wiki / "raw"
    if not raw_root.exists():
        return drifted
    for path in sorted(raw_root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_HASH_EXTS:
            continue
        fm, _body, has_fm = frontmatter_block(read_text(path))
        expected = str(fm.get("sha256") or "").strip() if has_fm else ""
        if not expected:
            continue
        rel = path.relative_to(wiki).as_posix()
        scheme = str(fm.get("hash_scheme") or HASH_SCHEME_TEXT)
        try:
            actual, used_scheme = compute_source_hash(path, scheme)
        except (OSError, ValueError) as exc:
            drifted.append(
                {
                    "raw_source": rel,
                    "source_page": "",
                    "hash_scheme": scheme,
                    "expected_sha256": expected,
                    "actual_sha256": "",
                    "reason": str(exc),
                }
            )
            continue
        if expected == actual:
            continue
        linked_sources = source_pages_for_raw(rel, records)
        if not linked_sources:
            drifted.append(
                {
                    "raw_source": rel,
                    "source_page": "",
                    "hash_scheme": used_scheme,
                    "expected_sha256": expected,
                    "actual_sha256": actual,
                    "reason": "raw_frontmatter_hash_drift",
                }
            )
            continue
        for source_page in linked_sources:
            drifted.append(
                {
                    "raw_source": rel,
                    "source_page": source_page["rel"],
                    "hash_scheme": used_scheme,
                    "expected_sha256": expected,
                    "actual_sha256": actual,
                    "reason": "raw_frontmatter_hash_drift",
                }
            )
    return drifted


def collect_source_summary_health(wiki: Path, records: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    drifted: list[dict[str, Any]] = []
    blocking: list[str] = []
    reference_issues: list[str] = []
    for record in records:
        fm = record["fm"]
        source_rel = record["rel"]
        raw_rel = normalize_wiki_rel(fm.get("raw_source"))
        if not raw_rel:
            reference_issues.append(f"{source_rel}: missing raw_source")
            continue
        raw_path = wiki / raw_rel
        if not raw_path.is_file():
            message = f"{source_rel}: raw_source not found: {raw_rel}"
            reference_issues.append(message)
            blocking.append(message)
            continue
        expected = str(fm.get("raw_sha256") or "").strip()
        scheme = str(fm.get("raw_hash_scheme") or "").strip()
        if not expected or expected.lower() == "unknown":
            reference_issues.append(f"{source_rel}: missing raw_sha256")
            continue
        if not scheme or scheme.lower() == "unknown":
            reference_issues.append(f"{source_rel}: missing raw_hash_scheme")
            continue
        if scheme not in VALID_HASH_SCHEMES:
            message = f"{source_rel}: unsupported raw_hash_scheme {scheme!r}"
            reference_issues.append(message)
            blocking.append(message)
            continue
        default_scheme = default_hash_scheme(raw_path)
        if scheme != default_scheme:
            reference_issues.append(f"{source_rel}: raw_hash_scheme {scheme} differs from default {default_scheme}")
        try:
            actual, used_scheme = compute_source_hash(raw_path, scheme)
        except (OSError, ValueError) as exc:
            message = f"{source_rel}: {exc}"
            reference_issues.append(message)
            blocking.append(message)
            continue
        if expected != actual:
            drifted.append(
                {
                    "raw_source": raw_rel,
                    "source_page": source_rel,
                    "hash_scheme": used_scheme,
                    "expected_sha256": expected,
                    "actual_sha256": actual,
                    "reason": "source_summary_raw_hash_drift",
                }
            )
    return drifted, reference_issues, blocking


def health_report(wiki: Path) -> dict[str, Any]:
    issues = lint_wiki(wiki)
    lint_total = sum(len(items) for items in issues.values())
    records = source_page_records(wiki)
    raw_drift = collect_raw_frontmatter_drift(wiki, records)
    summary_drift, source_reference_issues, source_blocking = collect_source_summary_health(wiki, records)
    drifted_sources = raw_drift + summary_drift
    blocking_issues: list[str] = []
    for category in ["missing_root_files", "broken_links", "missing_frontmatter", "invalid_types"]:
        for item in issues.get(category, []):
            blocking_issues.append(f"{category}: {item}")
    blocking_issues.extend(source_blocking)
    affected_pages: list[dict[str, Any]] = []
    seen_source_pages: set[str] = set()
    for item in drifted_sources:
        source_page = item.get("source_page")
        if not source_page or source_page in seen_source_pages:
            continue
        seen_source_pages.add(source_page)
        source_path = wiki / str(source_page)
        dependents = affected_pages_for_source(wiki, source_path) if source_path.is_file() else []
        affected_pages.append(
            {
                "source_page": source_page,
                "dependent_pages": dependents,
                "all_pages": [source_page] + dependents,
            }
        )
    return {
        "wiki": str(wiki),
        "update_required": bool(drifted_sources),
        "blocking_issues": blocking_issues,
        "maintenance_recommended": bool(lint_total or drifted_sources or source_reference_issues),
        "drifted_sources": drifted_sources,
        "affected_pages": affected_pages,
        "source_reference_issues": source_reference_issues,
        "lint": {"total_issues": lint_total, "issues": issues},
    }


def command_health(args: argparse.Namespace) -> int:
    wiki = Path(args.wiki).expanduser().resolve()
    report = health_report(wiki)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Wiki: {wiki}")
        print(f"Update required: {str(report['update_required']).lower()}")
        print(f"Maintenance recommended: {str(report['maintenance_recommended']).lower()}")
        print(f"Blocking issues: {len(report['blocking_issues'])}")
        print(f"Drifted sources: {len(report['drifted_sources'])}")
        print(f"Affected source pages: {len(report['affected_pages'])}")
        if report["drifted_sources"]:
            print("\ndrifted_sources:")
            for item in report["drifted_sources"]:
                source_page = item.get("source_page") or "unlinked"
                print(f"- {item['raw_source']} -> {source_page}: {item['reason']}")
        if report["source_reference_issues"]:
            print("\nsource_reference_issues:")
            for item in report["source_reference_issues"]:
                print(f"- {item}")
    if args.fail_on_update and report["update_required"]:
        return 1
    if args.fail_on_issues and report["maintenance_recommended"]:
        return 1
    return 0


def command_append_log(args: argparse.Namespace) -> int:
    wiki = Path(args.wiki).expanduser().resolve()
    log_path = wiki / "log.md"
    files = ", ".join(args.file or [])
    lines = ["", f"## [{today()}] {args.action} | {args.subject}"]
    if files:
        lines.append(f"- Files: {files}")
    if args.notes:
        lines.append(f"- Notes: {args.notes}")
    with log_path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines) + "\n")
    print(json.dumps({"wiki": str(wiki), "logged": True}, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage a Karpathy-style LLM Wiki.")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create wiki root files and directories.")
    init.add_argument("wiki")
    init.add_argument("--domain", default="general knowledge")
    init.add_argument("--research", action="store_true", help="Append research schema guidance to AGENTS.md.")
    init.add_argument("--force", action="store_true", help="Overwrite root template files if they already exist.")
    init.set_defaults(func=command_init)

    classify = sub.add_parser("classify", help="Classify files from raw/inbox.")
    classify.add_argument("wiki")
    classify.add_argument("--move", action="store_true", help="Move files instead of dry-run classification.")
    classify.set_defaults(func=command_classify)

    hash_source = sub.add_parser("hash-source", help="Compute or write a source sha256.")
    hash_source.add_argument("path")
    hash_source.add_argument("--write", action="store_true", help="Write sha256 into text frontmatter.")
    hash_source.set_defaults(func=command_hash_source)

    update_index = sub.add_parser("update-index", help="Regenerate index.md from wiki pages.")
    update_index.add_argument("wiki")
    update_index.set_defaults(func=command_update_index)

    lint = sub.add_parser("lint", help="Audit wiki structure, links, metadata, and raw source drift.")
    lint.add_argument("wiki")
    lint.add_argument("--json", action="store_true")
    lint.add_argument("--fail-on-issues", action="store_true")
    lint.set_defaults(func=command_lint)

    health = sub.add_parser("health", help="Diagnose wiki health, source drift, and update impact.")
    health.add_argument("wiki")
    health.add_argument("--json", action="store_true")
    health.add_argument("--fail-on-update", action="store_true")
    health.add_argument("--fail-on-issues", action="store_true")
    health.set_defaults(func=command_health)

    append_log = sub.add_parser("append-log", help="Append a log.md entry.")
    append_log.add_argument("wiki")
    append_log.add_argument("--action", required=True)
    append_log.add_argument("--subject", required=True)
    append_log.add_argument("--file", action="append")
    append_log.add_argument("--notes")
    append_log.set_defaults(func=command_append_log)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
