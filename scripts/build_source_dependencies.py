#!/usr/bin/env python3
"""Build a source-to-page dependency map for an LLM Wiki vault."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


WIKILINK_RE = re.compile(r"!\[\[[^\]]+\]\]|\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
SOURCE_ROOTS = ["10 Sources", "raw"]
META_FILENAMES = {"schema.md", "index.md", "log.md", "topic-map.md", "overview.md", "questions.md", "readme.md"}
IGNORED_DIRS = {".git", "assets", "_archive", "templates", "references", "scripts", "tests"}


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    raw = text[4:end].strip()
    body = text[end + len("\n---") :].lstrip("\n")
    return parse_frontmatter(raw), body


def parse_frontmatter(raw: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current_key: str | None = None
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith(" ") and current_key:
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        current_key = key
        data[key] = parse_value(value.strip())
    return data


def parse_value(value: str) -> Any:
    if value == "":
        return ""
    if value in {"true", "false"}:
        return value == "true"
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [item.strip().strip("\"'") for item in inner.split(",")]
    return value.strip("\"'")


def as_list(value: Any) -> list[Any]:
    if value in (None, ""):
        return []
    if isinstance(value, list):
        return value
    return [value]


def dependencies_path(wiki: Path) -> Path:
    meta = wiki / "00 Meta"
    return meta / "source-dependencies.json" if meta.exists() else wiki / "source-dependencies.json"


def iter_markdown_files(wiki: Path) -> list[Path]:
    files: list[Path] = []
    for path in wiki.rglob("*.md"):
        rel_parts = path.relative_to(wiki).parts
        if any(part in IGNORED_DIRS for part in rel_parts):
            continue
        files.append(path)
    return sorted(files)


def is_source_note(wiki: Path, path: Path) -> bool:
    parts = path.relative_to(wiki).parts
    return bool(parts and parts[0] in SOURCE_ROOTS)


def is_wiki_page(wiki: Path, path: Path) -> bool:
    rel = path.relative_to(wiki)
    if rel.name.lower() in META_FILENAMES:
        return False
    if rel.parts and rel.parts[0] in SOURCE_ROOTS:
        return False
    return True


def link_target(raw_target: str) -> str:
    target = raw_target.strip().replace("\\", "/")
    if target.endswith(".md"):
        target = target[:-3]
    return Path(target).name


def extract_wikilinks(text: str) -> list[str]:
    links: list[str] = []
    for match in WIKILINK_RE.finditer(text):
        target = match.group(1)
        if target:
            links.append(link_target(target))
    return links


def normalize_ref(value: Any) -> str:
    text = str(value).strip().replace("\\", "/")
    if text.startswith("[[") and text.endswith("]]"):
        text = text[2:-2].split("|", 1)[0].split("#", 1)[0].strip()
    return text


def source_reference_keys(rel: str) -> set[str]:
    path = Path(rel)
    keys = {rel, rel.removesuffix(".md"), path.name, path.stem}
    return {key for key in keys if key}


def build_source_dependencies(wiki_path: str | Path) -> dict[str, Any]:
    wiki = Path(wiki_path).expanduser().resolve()
    source_notes: dict[str, dict[str, Any]] = {}
    wiki_pages: dict[str, dict[str, Any]] = {}

    for path in iter_markdown_files(wiki):
        rel = path.relative_to(wiki).as_posix()
        frontmatter, body = split_frontmatter(path.read_text(encoding="utf-8"))
        item = {"frontmatter": frontmatter, "body": body, "stem": path.stem}
        if is_source_note(wiki, path):
            source_notes[rel] = item
        elif is_wiki_page(wiki, path):
            wiki_pages[rel] = item

    wiki_by_stem = {item["stem"]: rel for rel, item in wiki_pages.items()}
    source_by_key: dict[str, str] = {}
    for rel in source_notes:
        for key in source_reference_keys(rel):
            source_by_key[key] = rel

    dependencies: dict[str, dict[str, Any]] = {}
    pages: dict[str, dict[str, Any]] = {}
    raw_to_source_notes: dict[str, set[str]] = {}

    for rel, item in source_notes.items():
        frontmatter = item["frontmatter"]
        raw_file = normalize_ref(frontmatter.get("raw_file"))
        raw_sha256 = str(frontmatter.get("raw_sha256") or "")
        dependencies[rel] = {
            "kind": "source-note",
            "wiki_pages": [],
            "raw_file": raw_file,
            "raw_sha256": raw_sha256,
            "source_url": str(frontmatter.get("source_url") or ""),
            "processed": frontmatter.get("processed", ""),
        }
        if raw_file:
            raw_to_source_notes.setdefault(raw_file, set()).add(rel)

    for page_rel, item in wiki_pages.items():
        frontmatter = item["frontmatter"]
        page_sources = {normalize_ref(source) for source in as_list(frontmatter.get("sources", []))}
        body_links = set(extract_wikilinks(item["body"]))
        matched_sources: set[str] = set()
        for source_ref in page_sources | body_links:
            source_rel = source_by_key.get(source_ref)
            if source_rel:
                matched_sources.add(source_rel)
        for source_rel in sorted(matched_sources):
            add_unique(dependencies[source_rel]["wiki_pages"], page_rel)
        if matched_sources:
            pages[page_rel] = {"sources": sorted(matched_sources)}

    for source_rel, item in source_notes.items():
        for target in extract_wikilinks(item["body"]):
            page_rel = wiki_by_stem.get(target)
            if page_rel:
                add_unique(dependencies[source_rel]["wiki_pages"], page_rel)
                pages.setdefault(page_rel, {"sources": []})
                add_unique(pages[page_rel]["sources"], source_rel)

    for raw_file, notes in sorted(raw_to_source_notes.items()):
        wiki_page_set: set[str] = set()
        for source_rel in notes:
            wiki_page_set.update(dependencies[source_rel]["wiki_pages"])
        dependencies[raw_file] = {
            "kind": "raw-file",
            "source_notes": sorted(notes),
            "wiki_pages": sorted(wiki_page_set),
        }

    for item in dependencies.values():
        if "wiki_pages" in item:
            item["wiki_pages"] = sorted(item["wiki_pages"])

    return {
        "version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "wiki": str(wiki),
        "dependencies": dict(sorted(dependencies.items())),
        "pages": dict(sorted(pages.items())),
    }


def add_unique(values: list[str], value: str) -> None:
    if value not in values:
        values.append(value)


def write_dependencies(wiki_path: str | Path, report: dict[str, Any]) -> Path:
    wiki = Path(wiki_path).expanduser().resolve()
    path = dependencies_path(wiki)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {key: value for key, value in report.items() if key != "wiki"}
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    return path


def format_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Source Dependencies",
        "",
        f"Vault: `{report['wiki']}`",
        f"Tracked items: {len(report['dependencies'])}",
        "",
    ]
    if not report["dependencies"]:
        lines.append("No source dependencies found.")
    else:
        for path, item in report["dependencies"].items():
            pages = ", ".join(f"`{page}`" for page in item.get("wiki_pages", [])) or "no wiki pages"
            lines.append(f"- `{path}` -> {pages}")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build source-to-page dependencies for an LLM Wiki vault.")
    parser.add_argument("wiki", help="Path to the wiki or Obsidian vault")
    parser.add_argument("--write", action="store_true", help="Write 00 Meta/source-dependencies.json")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown")
    args = parser.parse_args(argv)

    report = build_source_dependencies(args.wiki)
    if args.write:
        write_dependencies(args.wiki, report)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))
    else:
        print(format_markdown(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
