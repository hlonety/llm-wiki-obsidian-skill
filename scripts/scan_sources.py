#!/usr/bin/env python3
"""Scan raw source folders, compute hashes, and detect new/changed/deleted files."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_ROOTS = ["10 Sources", "raw"]
MANIFEST_CANDIDATES = ["00 Meta/source-manifest.json", "source-manifest.json"]
IGNORED_NAMES = {".DS_Store", ".gitkeep", "source-manifest.json"}
IGNORED_DIRS = {".git", "__pycache__", "_archive"}


def manifest_path(wiki: Path) -> Path:
    for candidate in MANIFEST_CANDIDATES:
        path = wiki / candidate
        if path.exists():
            return path
    meta = wiki / "00 Meta"
    return meta / "source-manifest.json" if meta.exists() else wiki / "source-manifest.json"


def load_manifest(wiki_path: str | Path) -> dict[str, Any]:
    wiki = Path(wiki_path).expanduser().resolve()
    path = manifest_path(wiki)
    if not path.exists():
        return {"version": 1, "generated_at": None, "files": {}}
    data = json.loads(path.read_text(encoding="utf-8"))
    data.setdefault("version", 1)
    data.setdefault("files", {})
    return data


def write_manifest(wiki_path: str | Path, manifest: dict[str, Any]) -> Path:
    wiki = Path(wiki_path).expanduser().resolve()
    path = manifest_path(wiki)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    return path


def iter_source_files(wiki: Path, roots: list[str] | None = None) -> list[Path]:
    files: list[Path] = []
    for root_name in roots or DEFAULT_ROOTS:
        root = wiki / root_name
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            rel_parts = path.relative_to(wiki).parts
            if any(part in IGNORED_DIRS for part in rel_parts):
                continue
            if path.name in IGNORED_NAMES or path.name.startswith("."):
                continue
            files.append(path)
    return sorted(set(files))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_record(wiki: Path, path: Path) -> dict[str, Any]:
    stat = path.stat()
    return {
        "path": path.relative_to(wiki).as_posix(),
        "sha256": sha256_file(path),
        "size": stat.st_size,
        "modified_at": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
    }


def scan_sources(wiki_path: str | Path, roots: list[str] | None = None) -> dict[str, Any]:
    wiki = Path(wiki_path).expanduser().resolve()
    previous = load_manifest(wiki)
    previous_files: dict[str, dict[str, Any]] = previous.get("files", {})
    current_records = {record["path"]: record for record in (file_record(wiki, path) for path in iter_source_files(wiki, roots))}

    files: list[dict[str, Any]] = []
    for path, record in sorted(current_records.items()):
        old = previous_files.get(path)
        if not old:
            status = "new"
        elif old.get("sha256") != record["sha256"]:
            status = "changed"
        else:
            status = "unchanged"
        files.append({**record, "status": status})

    for path, old in sorted(previous_files.items()):
        if path not in current_records:
            files.append({**old, "path": path, "status": "deleted"})

    summary = {"new": 0, "changed": 0, "deleted": 0, "unchanged": 0, "total": len(files)}
    for item in files:
        summary[item["status"]] += 1

    manifest = {
        "version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "roots": roots or DEFAULT_ROOTS,
        "files": current_records,
    }
    return {"wiki": str(wiki), "manifest_path": str(manifest_path(wiki)), "summary": summary, "files": files, "manifest": manifest}


def format_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Source Scan",
        "",
        f"Vault: `{report['wiki']}`",
        f"Manifest: `{report['manifest_path']}`",
        "",
        "## Summary",
        "",
    ]
    for key in ["new", "changed", "deleted", "unchanged", "total"]:
        lines.append(f"- {key}: {report['summary'][key]}")
    lines.extend(["", "## Files", ""])
    changed_files = [item for item in report["files"] if item["status"] != "unchanged"]
    if not changed_files:
        lines.append("No new, changed, or deleted source files.")
    else:
        for item in changed_files:
            hash_text = item.get("sha256", "")[:12]
            lines.append(f"- [{item['status']}] `{item['path']}` {hash_text}")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan raw source folders and maintain a SHA-256 manifest.")
    parser.add_argument("wiki", help="Path to the wiki or Obsidian vault")
    parser.add_argument("--root", action="append", dest="roots", help="Source root to scan; may be provided multiple times")
    parser.add_argument("--write", action="store_true", help="Write the updated source manifest")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown")
    args = parser.parse_args(argv)

    report = scan_sources(args.wiki, roots=args.roots)
    if args.write:
        write_manifest(args.wiki, report["manifest"])
    if args.json:
        output = {key: value for key, value in report.items() if key != "manifest"}
        print(json.dumps(output, indent=2, ensure_ascii=False, sort_keys=True))
    else:
        print(format_markdown(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

