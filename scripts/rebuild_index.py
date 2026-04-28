#!/usr/bin/env python3
"""Rebuild an index page for an Obsidian-style LLM Wiki vault."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
from typing import Any


META_FILENAMES = {
    "agents.md",
    "bootstrap_prompt.md",
    "claude.md",
    "gemini.md",
    "schema.md",
    "index.md",
    "log.md",
    "topic-map.md",
    "overview.md",
    "questions.md",
    "readme.md",
    "upgrade_prompt.md",
}
IGNORED_DIRS = {".git", "assets", "_archive", "templates", "references", "scripts", "tests"}
SOURCE_ROOTS = {"10 sources", "raw", "wiki/sources"}
TYPE_ORDER = ["concept", "entity", "tool", "paper", "person", "workflow", "prompt", "question", "synthesis", "map", "output"]
TYPE_LABELS = {
    "concept": "Concepts",
    "entity": "Entities",
    "tool": "Tools",
    "paper": "Papers",
    "person": "People",
    "workflow": "Workflows",
    "prompt": "Prompts",
    "question": "Questions",
    "synthesis": "Synthesis",
    "map": "Maps",
    "output": "Outputs",
}


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
    for line in raw.splitlines():
        if not line.strip() or line.startswith(" "):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = parse_value(value.strip())
    return data


def parse_value(value: str) -> Any:
    if value == "":
        return ""
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [item.strip().strip("\"'") for item in inner.split(",")]
    return value.strip("\"'")


def iter_pages(wiki: Path) -> list[Path]:
    files: list[Path] = []
    for path in wiki.rglob("*.md"):
        rel = path.relative_to(wiki)
        lower_parts = {part.lower() for part in rel.parts}
        if lower_parts & IGNORED_DIRS or any(part.startswith(".") for part in lower_parts):
            continue
        if rel.name.lower() in META_FILENAMES:
            continue
        rel_text = rel.as_posix().lower()
        if any(rel_text == root or rel_text.startswith(f"{root}/") for root in SOURCE_ROOTS):
            continue
        if rel.parts[:2] in {("wiki", "templates"), ("wiki", ".state")}:
            continue
        files.append(path)
    return sorted(files)


def first_paragraph(body: str) -> str:
    lines: list[str] = []
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped:
            if lines:
                break
            continue
        if stripped.startswith("#"):
            continue
        if stripped.startswith("- ") and not lines:
            continue
        lines.append(stripped)
    summary = " ".join(lines).strip()
    return summary[:140].rstrip() if summary else ""


def page_record(wiki: Path, path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(text)
    page_type = str(frontmatter.get("type") or infer_type(path)).lower()
    title = str(frontmatter.get("title") or path.stem.replace("-", " ").title())
    summary = str(frontmatter.get("summary") or first_paragraph(body) or title)
    return {
        "type": page_type,
        "title": title,
        "slug": path.stem,
        "summary": summary,
        "path": path.relative_to(wiki).as_posix(),
    }


def infer_type(path: Path) -> str:
    folder = path.parent.name.lower()
    mapping = {
        "20 concepts": "concept",
        "concepts": "concept",
        "wiki/concepts": "concept",
        "entities": "entity",
        "wiki/entities": "entity",
        "30 tools": "tool",
        "tools": "tool",
        "40 people": "person",
        "people": "person",
        "50 papers": "paper",
        "papers": "paper",
        "60 workflows": "workflow",
        "workflows": "workflow",
        "70 prompts": "prompt",
        "prompts": "prompt",
        "80 questions": "question",
        "queries": "question",
        "90 maps": "map",
        "maps": "map",
        "synthesis": "synthesis",
        "wiki/synthesis": "synthesis",
        "outputs": "output",
        "wiki/outputs": "output",
    }
    rel_parent = path.parent.as_posix().lower()
    return mapping.get(rel_parent) or mapping.get(folder, "concept")


def build_index(wiki_path: str | Path, title: str = "LLM Wiki Index") -> str:
    wiki = Path(wiki_path).expanduser().resolve()
    records = [page_record(wiki, path) for path in iter_pages(wiki)]
    grouped: dict[str, list[dict[str, str]]] = {}
    for record in records:
        grouped.setdefault(record["type"], []).append(record)

    lines = [
        f"# {title}",
        "",
        "> Content catalog for the compiled wiki layer.",
        f"> Last updated: {date.today().isoformat()} | Total pages: {len(records)}",
        "",
    ]

    ordered_types = TYPE_ORDER + sorted(page_type for page_type in grouped if page_type not in TYPE_ORDER)
    for page_type in ordered_types:
        items = grouped.get(page_type, [])
        if not items:
            continue
        lines.append(f"## {TYPE_LABELS.get(page_type, page_type.title() + 's')}")
        for item in sorted(items, key=lambda record: record["title"].lower()):
            lines.append(f"- [[{item['slug']}]] - {item['summary']}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def index_path(wiki: Path) -> Path:
    strict = wiki / "wiki"
    if strict.exists():
        return strict / "index.md"
    meta = wiki / "00 Meta"
    return meta / "index.md" if meta.exists() else wiki / "index.md"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Rebuild the index for an Obsidian-style LLM Wiki vault.")
    parser.add_argument("wiki", help="Path to the wiki or Obsidian vault")
    parser.add_argument("--title", default="LLM Wiki Index", help="Index page title")
    parser.add_argument("--write", action="store_true", help="Write the generated index to the vault")
    args = parser.parse_args(argv)

    wiki = Path(args.wiki).expanduser().resolve()
    content = build_index(wiki, title=args.title)
    if args.write:
        target = index_path(wiki)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        print(f"Wrote {target}")
    else:
        print(content, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
