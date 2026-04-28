#!/usr/bin/env python3
"""Audit an Obsidian-style LLM Wiki vault."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


WIKILINK_RE = re.compile(r"!\[\[[^\]]+\]\]|\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
REQUIRED_FRONTMATTER = {"title", "created", "updated", "type", "tags", "sources"}
META_FILENAMES = {"schema.md", "index.md", "log.md", "topic-map.md", "readme.md"}
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


def iter_markdown_files(wiki: Path) -> list[Path]:
    files: list[Path] = []
    for path in wiki.rglob("*.md"):
        rel_parts = path.relative_to(wiki).parts
        if any(part in IGNORED_DIRS for part in rel_parts):
            continue
        files.append(path)
    return sorted(files)


def is_wiki_page(wiki: Path, path: Path) -> bool:
    rel = path.relative_to(wiki)
    if rel.name.lower() in META_FILENAMES:
        return False
    if rel.parts and rel.parts[0].lower() in {"10 sources", "raw"}:
        return False
    return True


def page_key(path: Path) -> str:
    return path.stem


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


def parse_schema_tags(wiki: Path) -> set[str]:
    schema = first_existing(wiki, ["00 Meta/SCHEMA.md", "SCHEMA.md"])
    if not schema:
        return set()
    text = schema.read_text(encoding="utf-8")
    tags: set[str] = set()
    for match in re.finditer(r"`([^`]+)`", text):
        value = match.group(1).strip()
        if re.fullmatch(r"[a-z0-9][a-z0-9-]*", value):
            tags.add(value)
    for line in text.splitlines():
        if ":" in line and line.lstrip().startswith("-"):
            _, tail = line.split(":", 1)
            for token in re.split(r"[, ]+", tail):
                token = token.strip(" `.")
                if re.fullmatch(r"[a-z0-9][a-z0-9-]*", token):
                    tags.add(token)
    return tags


def first_existing(wiki: Path, candidates: list[str]) -> Path | None:
    for candidate in candidates:
        path = wiki / candidate
        if path.exists():
            return path
    return None


def index_text(wiki: Path) -> str:
    path = first_existing(wiki, ["00 Meta/index.md", "index.md"])
    if not path:
        return ""
    return path.read_text(encoding="utf-8")


def lint_wiki(wiki_path: str | Path) -> dict[str, Any]:
    wiki = Path(wiki_path).expanduser().resolve()
    issues: list[dict[str, Any]] = []
    if not wiki.exists():
        return {"wiki": str(wiki), "summary": {"pages": 0, "issues": 1}, "issues": [{"code": "missing-vault", "path": str(wiki)}]}

    for required in ["00 Meta/SCHEMA.md", "SCHEMA.md"]:
        if (wiki / required).exists():
            break
    else:
        issues.append({"code": "missing-schema", "severity": "high", "path": "00 Meta/SCHEMA.md"})

    md_files = iter_markdown_files(wiki)
    wiki_pages = [path for path in md_files if is_wiki_page(wiki, path)]
    keys = {page_key(path): path for path in wiki_pages}
    inbound = {key: 0 for key in keys}
    schema_tags = parse_schema_tags(wiki)
    listed_pages = set(extract_wikilinks(index_text(wiki)))

    for path in wiki_pages:
        rel = path.relative_to(wiki).as_posix()
        text = path.read_text(encoding="utf-8")
        frontmatter, body = split_frontmatter(text)
        key = page_key(path)

        missing = sorted(REQUIRED_FRONTMATTER - set(frontmatter))
        if missing:
            issues.append({"code": "missing-frontmatter", "severity": "high", "page": key, "path": rel, "fields": missing})

        tags = frontmatter.get("tags", [])
        if isinstance(tags, str):
            tags = [tags]
        if schema_tags:
            unknown = sorted(tag for tag in tags if tag and tag not in schema_tags)
            if unknown:
                issues.append({"code": "unknown-tag", "severity": "medium", "page": key, "path": rel, "tags": unknown})

        if key not in listed_pages:
            issues.append({"code": "missing-index-entry", "severity": "medium", "page": key, "path": rel})

        for target in extract_wikilinks(body):
            if target not in keys and target not in listed_pages:
                issues.append({"code": "broken-wikilink", "severity": "high", "page": key, "path": rel, "target": target})
            elif target in inbound:
                inbound[target] += 1

    for key, count in inbound.items():
        if count == 0 and len(wiki_pages) > 1:
            issues.append({"code": "orphan-page", "severity": "low", "page": key, "path": keys[key].relative_to(wiki).as_posix()})

    issues.extend(check_raw_hashes(wiki))

    return {
        "wiki": str(wiki),
        "summary": {"pages": len(wiki_pages), "issues": len(issues)},
        "issues": sorted(issues, key=lambda issue: (severity_rank(issue.get("severity", "low")), issue.get("code", ""), issue.get("path", ""))),
    }


def severity_rank(severity: str) -> int:
    return {"high": 0, "medium": 1, "low": 2}.get(severity, 3)


def check_raw_hashes(wiki: Path) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for source_root in ["10 Sources", "raw"]:
        root = wiki / source_root
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.md")):
            text = path.read_text(encoding="utf-8")
            frontmatter, body = split_frontmatter(text)
            expected = frontmatter.get("sha256")
            if not expected:
                continue
            actual = hashlib.sha256(body.encode("utf-8")).hexdigest()
            if actual != expected:
                issues.append(
                    {
                        "code": "source-drift",
                        "severity": "medium",
                        "path": path.relative_to(wiki).as_posix(),
                        "expected": expected,
                        "actual": actual,
                    }
                )
    return issues


def format_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# LLM Wiki Audit",
        "",
        f"Vault: `{report['wiki']}`",
        f"Pages: {report['summary']['pages']}",
        f"Issues: {report['summary']['issues']}",
        "",
    ]
    if not report["issues"]:
        lines.append("No issues found.")
        return "\n".join(lines) + "\n"
    for issue in report["issues"]:
        details = ", ".join(f"{key}={value}" for key, value in issue.items() if key not in {"code", "severity"})
        lines.append(f"- [{issue.get('severity', 'low')}] {issue['code']}: {details}")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit an Obsidian-style LLM Wiki vault.")
    parser.add_argument("wiki", help="Path to the wiki or Obsidian vault")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown")
    args = parser.parse_args(argv)

    report = lint_wiki(args.wiki)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(format_markdown(report), end="")
    return 1 if any(issue.get("severity") == "high" for issue in report["issues"]) else 0


if __name__ == "__main__":
    sys.exit(main())

