#!/usr/bin/env python3
"""Initialize a strict Karpathy-style LLM Wiki knowledge-base layout."""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


RAW_DIRS = ["articles", "clippings", "images", "pdfs", "notes", "personal"]
WIKI_DIRS = ["sources", "concepts", "entities", "synthesis", "outputs", "templates", ".state"]


def init_knowledge_base(target_path: str | Path, overwrite: bool = False) -> dict[str, Any]:
    target = Path(target_path).expanduser().resolve()
    created_dirs: list[str] = []
    created_files: list[str] = []

    for rel in ["raw", *[f"raw/{name}" for name in RAW_DIRS], "wiki", *[f"wiki/{name}" for name in WIKI_DIRS], "scripts"]:
        path = target / rel
        path.mkdir(parents=True, exist_ok=True)
        created_dirs.append(rel)

    for rel, content in seed_files().items():
        path = target / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if overwrite or not path.exists():
            path.write_text(content, encoding="utf-8")
        created_files.append(rel)

    for rel, payload in state_files().items():
        path = target / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if overwrite or not path.exists():
            path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
        created_files.append(rel)

    return {"root": str(target), "dirs": created_dirs, "files": created_files}


def seed_files() -> dict[str, str]:
    today = date.today().isoformat()
    return {
        "wiki/index.md": f"""# LLM Wiki Index

> First file for agents to read after `CLAUDE.md`.
> Last updated: {today}

## Sources

## Concepts

## Entities

## Synthesis

## Outputs
""",
        "wiki/log.md": f"""# Evolution Log

## {today}

- initialized: created strict `raw/` + `wiki/` LLM Wiki structure.
""",
        "wiki/overview.md": f"""# Knowledge Base Health Dashboard

- Last audit: {today}
- Open source queue: 0
- Possibly outdated sources: 0
- Contested pages: 0
- Thin pages: 0
""",
        "wiki/QUESTIONS.md": """# Questions

## Open

- [ ] What should this knowledge base help answer first?

## Resolved
""",
        "scripts/lint.py": """#!/usr/bin/env python3
\"\"\"Local lint entrypoint for this knowledge base.

Preferred: run the richer llm-wiki skill script from the installed skill repo:
python3 /path/to/llm-wiki-obsidian-skill/scripts/lint_wiki.py /path/to/knowledge-base
\"\"\"

from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    raw = root / "raw"
    wiki = root / "wiki"
    missing = [str(path.relative_to(root)) for path in [raw, wiki, wiki / "index.md", root / "CLAUDE.md"] if not path.exists()]
    if missing:
        print("Missing required paths:")
        for item in missing:
            print(f"- {item}")
        return 1
    print("Basic structure check passed. Use the llm-wiki skill scripts for full lint, hash, and state checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
""",
        "BOOTSTRAP_PROMPT.md": """# Bootstrap Prompt

Use the llm-wiki-obsidian skill to initialize and maintain this knowledge base.

First read `CLAUDE.md`, then `wiki/index.md`, `wiki/log.md`, `wiki/overview.md`, and `wiki/QUESTIONS.md`.
Preserve all raw material under `raw/`. Write compiled knowledge under `wiki/`.
""",
        "UPGRADE_PROMPT.md": """# Upgrade Prompt

Use the llm-wiki-obsidian skill to audit this knowledge base against the current method.

Check raw source hashes, source lifecycle fields, source dependencies, duplicate concepts, broken links,
open questions, stale pages, and missing index entries. Propose a small migration plan before changing
more than 10 files.
""",
        "CLAUDE.md": """# LLM Behavior Contract

This file is a portable behavior contract for any file-capable agent. The filename follows the original
LLM Wiki tutorial, but the rules are not Claude-only.

## Directory Contract

- `raw/`: immutable original sources. Add files here; do not rewrite evidence.
- `raw/articles/`: long-form web or Markdown articles.
- `raw/clippings/`: Web Clipper captures.
- `raw/images/`: screenshots and charts.
- `raw/pdfs/`: PDF files.
- `raw/notes/`: quick notes and scratch captures.
- `raw/personal/`: user-authored essays, analysis, and investment notes.
- `wiki/index.md`: first wiki file to read.
- `wiki/log.md`: append-only evolution log.
- `wiki/overview.md`: knowledge base health dashboard.
- `wiki/QUESTIONS.md`: open question queue.
- `wiki/sources/`: one summary page per source.
- `wiki/concepts/`: durable concepts, ideas, and patterns.
- `wiki/entities/`: people, companies, tools, models, papers, datasets, and benchmarks.
- `wiki/synthesis/`: cross-source analysis and maps.
- `wiki/outputs/`: saved answers, reports, slides, charts, and lint reports.
- `wiki/templates/`: page templates.

## Operating Rules

- Read this file, `wiki/index.md`, recent `wiki/log.md`, and `wiki/QUESTIONS.md` before editing.
- Preserve raw sources. Add corrections and interpretations to wiki pages.
- Source notes track `processed`, `raw_file`, `raw_sha256`, `last_verified`, and `possibly_outdated`.
- Treat `processed: false`, changed hashes, and `possibly_outdated: true` as the ingest queue.
- Use lowercase kebab-case filenames. Put Chinese names and alternate terms in `title` and `aliases`.
- Search filenames, titles, and aliases before creating pages.
- Every factual claim should link back to source notes or raw files.
- Personal writing may update `## My Position`, but it does not count as external evidence.
- `confidence: high` requires explicit human confirmation.
- Log meaningful changes as reinforced, corrected, contradicted, re-ingested, or personal-position.

## Tag Taxonomy

- Areas: `agent`, `llm`, `rag`, `memory`, `evaluation`, `prompt`, `workflow`, `automation`
- Technical: `architecture`, `training`, `fine-tuning`, `inference`, `tool-use`, `mcp`, `data`
- Objects: `model`, `paper`, `tool`, `framework`, `benchmark`, `dataset`, `company`, `person`
- Quality: `security`, `privacy`, `reliability`, `alignment`, `cost`, `latency`
- Meta: `comparison`, `timeline`, `controversy`, `prediction`, `learning-path`
""",
        "README.md": """# Knowledge Base

Strict LLM Wiki layout:

- `raw/` stores original sources.
- `wiki/` stores source summaries, concepts, entities, synthesis, outputs, templates, logs, and questions.
- `scripts/lint.py` is the local health-check entrypoint.

Use the llm-wiki-obsidian skill for full ingest, audit, hash scanning, and source dependency workflows.
""",
    }


def state_files() -> dict[str, Any]:
    return {
        "wiki/.state/source-manifest.json": {
            "version": 1,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "roots": ["raw"],
            "files": {},
        },
        "wiki/.state/source-dependencies.json": {
            "version": 1,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "dependencies": {},
            "pages": {},
        },
    }


def format_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Knowledge Base Initialized",
        "",
        f"Root: `{report['root']}`",
        "",
        "## Directories",
        "",
    ]
    lines.extend(f"- `{item}`" for item in report["dirs"])
    lines.extend(["", "## Files", ""])
    lines.extend(f"- `{item}`" for item in report["files"])
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Initialize a strict raw/wiki LLM Wiki knowledge base.")
    parser.add_argument("target", help="Directory to initialize, for example ./knowledge-base")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing seed files")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown")
    args = parser.parse_args(argv)

    report = init_knowledge_base(args.target, overwrite=args.overwrite)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))
    else:
        print(format_markdown(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
