# LLM Wiki Obsidian Skill

A portable agent skill for maintaining a strict `raw/` + `wiki/` LLM Wiki based on Andrej Karpathy's LLM Wiki pattern.

It is designed for AI knowledge bases: LLMs, agents, prompts, tools, papers, workflows, evaluation, RAG, MCP, automation, and learning notes.

## What It Does

This skill teaches an agent to maintain a compounding Markdown wiki:

- Preserve raw sources.
- Compile durable source summaries, concepts, entities, synthesis pages, outputs, and questions.
- Keep Obsidian wikilinks and frontmatter clean.
- Track sources, confidence, stale claims, and contradictions.
- Keep open questions, durable outputs, and personal writing separate from external evidence.
- Compute SHA-256 hashes for raw source files and detect new, changed, or deleted files.
- Build source-to-page dependency maps so changed raw files can trigger targeted review.
- Track source lifecycle fields such as `processed`, `raw_file`, `raw_sha256`, `last_verified`, and `possibly_outdated`.
- Audit broken links, missing index entries, orphan pages, duplicate URLs, near-duplicate slugs, link hygiene, and drift.

## Install

### Codex

Ask Codex to install or use this skill from the GitHub repository URL:

```text
Install the skill from https://github.com/hlonety/llm-wiki-obsidian-skill
```

If installing manually, copy this repository into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/hlonety/llm-wiki-obsidian-skill ~/.codex/skills/llm-wiki-obsidian
```

Restart Codex after installation.

### Other Agents

Point the agent at `SKILL.md` and ask it to follow the instructions. The skill avoids provider-specific tool names, so Claude Code, OpenCode, OpenClaw, Hermes, Gemini, Codex, and other file-capable agents can adapt it.

Common patterns:

- Claude Code: clone or copy this folder into the local skills/rules location you use, or reference `SKILL.md` from `CLAUDE.md`.
- OpenCode / OpenClaw: add this repository as a reusable skill/rules folder and point the agent to `SKILL.md`.
- Hermes: import the folder as a skill or copy the `SKILL.md` body into a Hermes skill wrapper.
- Any other agent: give it the repository URL and ask it to read `SKILL.md` before touching the vault.

The instructions are tool-neutral. When a platform has different tool names for file search, file editing, web extraction, or code execution, the agent should translate the action to its local equivalent.

## Quick Start

Create an AI knowledge vault:

```text
Use llm-wiki-obsidian to create a strict knowledge-base for my AI knowledge at ~/wiki/knowledge-base.
```

Or run the scaffold script directly:

```bash
python3 scripts/init_knowledge_base.py ~/wiki/knowledge-base
```

Ingest a source:

```text
Use llm-wiki-obsidian to add this article to my AI vault and update related concept pages: https://example.com/article
```

Query the wiki:

```text
Based on my LLM Wiki, explain the difference between RAG memory and compiled wiki memory.
```

Audit the vault:

```bash
python3 scripts/lint_wiki.py ~/wiki/knowledge-base
```

Scan raw sources and update the hash manifest:

```bash
python3 scripts/scan_sources.py ~/wiki/knowledge-base
python3 scripts/scan_sources.py ~/wiki/knowledge-base --write
```

Build the source dependency map:

```bash
python3 scripts/build_source_dependencies.py ~/wiki/knowledge-base --write
```

Rebuild the index:

```bash
python3 scripts/rebuild_index.py ~/wiki/knowledge-base --write
```

## Strict Knowledge-Base Layout

```text
knowledge-base/
  raw/
    articles/
    clippings/
    images/
    pdfs/
    notes/
    personal/
  wiki/
    index.md
    log.md
    overview.md
    QUESTIONS.md
    sources/
    concepts/
    entities/
    synthesis/
    outputs/
    templates/
    .state/
      source-manifest.json
      source-dependencies.json
  scripts/
    lint.py
  BOOTSTRAP_PROMPT.md
  UPGRADE_PROMPT.md
  CLAUDE.md
  README.md
```

`CLAUDE.md` is the tutorial-compatible behavior contract. It is not Claude-only; other agents should read it as a normal Markdown rules file.

## Knowledge Rules

- `confidence: high` is never automatic. It requires explicit user confirmation.
- Personal writing records the user's position but does not count toward external `source_count`.
- Fast-moving pages use `domain_volatility` and `last_reviewed` so stale claims can be audited.
- Durable query results, reflection reports, comparison tables, and slide outlines go in `wiki/outputs/`.
- `scan_sources.py` maintains `wiki/.state/source-manifest.json` and reports `new`, `changed`, `deleted`, and `unchanged` source files.
- `build_source_dependencies.py` maintains `wiki/.state/source-dependencies.json` for raw-file, source-note, and wiki-page impact tracking.
- Web Clipper or browser-saved notes should enter as `processed: false` source notes and be batch-ingested later.
- Use English lowercase kebab-case slugs; put Chinese names and alternate terms in titles and aliases.
- `REFLECT`, `MERGE`, and `ADD-QUESTION` operations are documented in `references/operations.md`.
- qmd-style tools are optional adapters, not required dependencies.

## Source

Inspired by Andrej Karpathy's original LLM Wiki method:

https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

## License

MIT
