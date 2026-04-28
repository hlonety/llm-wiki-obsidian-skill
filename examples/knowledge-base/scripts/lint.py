#!/usr/bin/env python3
"""Local lint entrypoint for this knowledge base.

Preferred: run the richer llm-wiki skill script from the installed skill repo:
python3 /path/to/llm-wiki-obsidian-skill/scripts/lint_wiki.py /path/to/knowledge-base
"""

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
