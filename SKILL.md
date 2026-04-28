---
name: llm-wiki-obsidian
description: Use when creating, maintaining, querying, or auditing a persistent Markdown or Obsidian knowledge base based on Karpathy's LLM Wiki pattern, especially for AI, LLM, agent, prompt, research, paper, tool, workflow, or learning notes.
---

# LLM Wiki Obsidian

Use this skill to maintain a compounding Markdown knowledge base where raw sources stay preserved, wiki pages improve over time, and the schema tells future agents how to continue the work.

The default target is an Obsidian vault for AI knowledge, but the method is portable to any file-based Markdown system.

## Source Principle

This skill follows Andrej Karpathy's LLM Wiki idea: do not answer every question by rediscovering raw material from scratch. Compile sources into an evolving wiki first, then query and update that wiki.

Keep three layers separate:

1. Raw sources: immutable evidence and clippings.
2. Wiki pages: agent-maintained synthesis, links, comparisons, and answers.
3. Schema: local rules for structure, tags, page thresholds, and update policy.

Read `references/karpathy-method.md` when you need the deeper reasoning behind these rules.

## First Action

When a user mentions an existing wiki, Obsidian vault, AI knowledge base, notes folder, or LLM wiki:

1. Locate the vault. Prefer an explicit path from the user. Otherwise check `LLM_WIKI_PATH`, `OBSIDIAN_VAULT_PATH`, then `~/wiki`.
2. Read `00 Meta/SCHEMA.md` if present, otherwise `SCHEMA.md`.
3. Read the index: `00 Meta/index.md`, `index.md`, or any obvious MOC.
4. Read the latest entries in `00 Meta/log.md` or `log.md`.
5. Search existing pages for the user's topic before creating anything.

Never ingest, rename, or create pages before this orientation step unless the user explicitly asks to create a brand-new vault.

## Default Obsidian Layout

For a new AI knowledge vault, create this structure unless the user requests another convention:

```text
vault/
  00 Meta/
    SCHEMA.md
    index.md
    log.md
    overview.md
    questions.md
    source-manifest.json
    topic-map.md
  10 Sources/
    articles/
    papers/
    transcripts/
    clips/
    personal/
  20 Concepts/
  30 Tools/
  40 People/
  50 Papers/
  60 Workflows/
  70 Prompts/
  80 Questions/
  90 Maps/
  95 Outputs/
  assets/
  _archive/
```

Map Karpathy's layers like this:

- Raw sources: `10 Sources/` and `assets/`.
- Wiki pages: `20 Concepts/` through `95 Outputs/`.
- Schema: `00 Meta/SCHEMA.md`.

Read `references/obsidian-conventions.md` before initializing or significantly restructuring an Obsidian vault.

## Core Rules

- Raw source files are immutable. Add corrections and later interpretation to wiki pages, not source files.
- Every wiki page has YAML frontmatter with `title`, `created`, `updated`, `type`, `status`, `tags`, and `sources`.
- Every substantial factual claim must be traceable to a source through `sources`, `evidence`, or a page-level Sources section.
- Use Obsidian wikilinks for internal pages: `[[agentic-workflow]]` or `[[agentic-workflow|Agentic workflow]]`.
- Prefer lowercase kebab-case filenames for agent stability. Human-readable titles live in frontmatter.
- Do not create pages for passing mentions. Create a page when the thing is central to one source or appears meaningfully in two or more sources.
- When a claim conflicts with existing content, keep both claims with dates and sources. Mark the page `contested: true`.
- Add or update index and log entries after every non-trivial change.
- If an ingest would update more than 10 existing pages, summarize the planned scope and ask before proceeding.
- Personal writing can record the user's position, but it must not count toward external `source_count`.
- `confidence: high` requires explicit human confirmation. Do not promote it automatically from source count alone.

## Common Workflows

Read `references/workflows.md` for exact steps. Use this quick map:

- Initialize: create the layout, write `SCHEMA.md`, seed `index.md`, seed `log.md`, suggest first sources.
- Ingest: preserve source, extract entities and concepts, search existing wiki, update synthesis pages, update navigation.
- Scan sources: compute SHA-256 for files under `10 Sources/` and `raw/`, update `00 Meta/source-manifest.json`, then ingest files marked `new` or `changed`.
- Query: read index, search pages, synthesize from wiki pages, cite page links and source notes, optionally file durable answers.
- Audit: check broken links, orphan pages, index drift, missing frontmatter, unknown tags, stale pages, source drift, and contested claims.
- Refactor: merge duplicate pages, split oversized pages, archive superseded pages, update inbound links.
- Reflect: search for counter-evidence first, then synthesize patterns, gaps, contradictions, and next questions.
- Merge: deduplicate pages by slug and aliases, preserving sources and personal positions.
- Add question: normalize open questions into `00 Meta/questions.md` so future ingests can answer them.

Read `references/confidence-policy.md` before changing confidence, source counts, or stale review fields. Read `references/operations.md` before reflect, merge, add-question, or durable output work.

## Page Types

Use the template in `templates/` when creating a page:

- `source.md`: normalized source notes under `10 Sources/`.
- `concept.md`: ideas such as RAG, evals, agentic workflows, memory, alignment.
- `tool.md`: products, models, libraries, frameworks, plugins, APIs.
- `paper.md`: research papers and technical reports.
- `person.md`: researchers, authors, founders, maintainers.
- `workflow.md`: repeatable processes, playbooks, checklists.
- `prompt.md`: reusable prompts and prompt patterns.
- `question.md`: durable answers worth filing after a query.
- `map-of-content.md`: navigation pages and learning routes.
- `personal-writing.md`: the user's own essays, investment notes, opinions, and analysis. These may update "My Position" sections but do not count as external support.

## Tool Neutrality

This skill is intentionally not tied to one agent. Use whatever equivalent tools are available:

- File listing, file reading, and file writing.
- Text search over the vault.
- Web page extraction for URLs.
- PDF or document text extraction for local files.
- A scripting/runtime tool for audits when available.

If a tool named in another agent's documentation is unavailable, translate the action to the local equivalent instead of stopping.

Compatibility target: Claude Code, OpenCode, OpenClaw, Hermes, Codex, Gemini-style agents, and any file-capable agent. If an agent supports local rules files such as `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, or Hermes skill manifests, those files may point to this skill or summarize its vault-specific conventions. The canonical reusable instructions remain in `SKILL.md` and `references/`.

## Quality Bar

Good LLM Wiki work should leave the vault easier to navigate than before:

- Fewer duplicate concepts.
- More useful cross-links.
- Better source traceability.
- Clear confidence levels for weak or fast-moving claims.
- A log entry that lets the next agent resume without guessing.

Use scripts in `scripts/` when available:

```bash
python3 scripts/scan_sources.py /path/to/vault
python3 scripts/scan_sources.py /path/to/vault --write
python3 scripts/lint_wiki.py /path/to/vault
python3 scripts/rebuild_index.py /path/to/vault --write
```
