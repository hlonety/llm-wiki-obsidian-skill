---
name: llm-wiki-obsidian
description: Use when creating, maintaining, querying, or auditing a persistent Markdown or Obsidian knowledge base based on Karpathy's LLM Wiki pattern, especially strict raw/wiki knowledge-base layouts for AI, LLM, agent, prompt, research, paper, tool, workflow, or learning notes.
---

# LLM Wiki Obsidian

Use this skill to maintain a compounding Markdown knowledge base where raw sources stay preserved, wiki pages improve over time, and a behavior contract tells future agents how to continue the work.

The default target is the strict `knowledge-base/raw/wiki` structure from the LLM Wiki tutorial, with additional source hashing, dependency mapping, audit, confidence, and Obsidian-friendly conventions.

## Source Principle

This skill follows Andrej Karpathy's LLM Wiki idea: do not answer every question by rediscovering raw material from scratch. Compile sources into an evolving wiki first, then query and update that wiki.

Keep three layers separate:

1. Raw sources: immutable evidence and clippings.
2. Wiki pages: agent-maintained synthesis, links, comparisons, and answers.
3. Behavior contract: local rules for structure, tags, page thresholds, and update policy.

Read `references/karpathy-method.md` when you need the deeper reasoning behind these rules.
Read `references/tutorial-coverage.md` when checking parity with the raw/wiki tutorial or explaining what this skill adds beyond it.

## First Action

When a user mentions an existing wiki, Obsidian vault, AI knowledge base, notes folder, or LLM wiki:

1. Locate the vault. Prefer an explicit path from the user. Otherwise check `LLM_WIKI_PATH`, `OBSIDIAN_VAULT_PATH`, then `~/wiki`.
2. Read `CLAUDE.md` first when present. It is the portable behavior contract even outside Claude Code.
3. Read `wiki/index.md`, then `wiki/log.md`, `wiki/overview.md`, and `wiki/QUESTIONS.md`.
4. Search `wiki/concepts/`, `wiki/entities/`, `wiki/synthesis/`, and `wiki/sources/` for the user's topic before creating anything.
5. Check `wiki/.state/source-manifest.json` and `wiki/.state/source-dependencies.json` if source freshness matters.

Never ingest, rename, or create pages before this orientation step unless the user explicitly asks to create a brand-new vault.

## Default Layout

For a new AI knowledge vault, create this strict structure:

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

Map Karpathy's layers like this:

- Raw sources: `raw/`.
- Source summaries: `wiki/sources/`.
- Compiled wiki pages: `wiki/concepts/`, `wiki/entities/`, `wiki/synthesis/`, and `wiki/outputs/`.
- Behavior contract and prompts: `CLAUDE.md`, `BOOTSTRAP_PROMPT.md`, `UPGRADE_PROMPT.md`.
- Generated state: `wiki/.state/`.

Read `references/obsidian-conventions.md` before initializing or significantly restructuring an Obsidian vault.

## Core Rules

- Raw source files are immutable. Add corrections and later interpretation to wiki pages, not source files.
- Source notes live in `wiki/sources/` and track `processed`, `raw_file`, `raw_sha256`, `last_verified`, `possibly_outdated`, `canonical_source`, `language`, `source_url`, `domain`, and `author` when known.
- Treat `processed: false`, changed hashes, or `possibly_outdated: true` as an ingest/review queue.
- Every wiki page has YAML frontmatter with `title`, `created`, `updated`, `type`, `status`, `tags`, and `sources`.
- Every substantial factual claim must be traceable to a source through `sources`, `evidence`, or a page-level Sources section.
- Use Obsidian wikilinks for internal pages: `[[agentic-workflow]]` or `[[agentic-workflow|Agentic workflow]]`.
- Prefer lowercase kebab-case filenames for agent stability. Human-readable titles live in frontmatter.
- Before creating a concept, check existing filenames, titles, and aliases. Keep English lowercase kebab-case slugs; put Chinese names in `title` and `aliases`.
- Do not create pages for passing mentions. Create a page when the thing is central to one source or appears meaningfully in two or more sources.
- When a claim conflicts with existing content, keep both claims with dates and sources. Mark the page `contested: true`.
- Add or update `wiki/index.md` and `wiki/log.md` after every non-trivial change. Log whether the change reinforced, corrected, contradicted, re-ingested, or recorded a personal position.
- If an ingest would update more than 10 existing pages, summarize the planned scope and ask before proceeding.
- Personal writing can record the user's position, but it must not count toward external `source_count`.
- `confidence: high` requires explicit human confirmation. Do not promote it automatically from source count alone.

## Common Workflows

Read `references/workflows.md` for exact steps. Use this quick map:

- Initialize: create the strict layout, write `CLAUDE.md`, seed wiki files, and suggest first sources.
- Web clip: save raw clips under `raw/clippings/`, create source notes with `processed: false`, then batch ingest later.
- Ingest: preserve source, extract entities and concepts, search existing wiki, update synthesis pages, update navigation, set `processed: true`.
- Scan sources: compute SHA-256 for files under `raw/`, update `wiki/.state/source-manifest.json`, then ingest files marked `new` or `changed`.
- Build dependencies: update `wiki/.state/source-dependencies.json` so changed source files can be traced to affected wiki pages.
- Re-ingest: when a hash changes, review the dependency map, update source notes and affected pages, then add a re-ingest log entry.
- Query: read index, search pages, synthesize from wiki pages, cite page links and source notes, optionally file durable answers.
- Audit: check broken links, orphan pages, index drift, missing frontmatter, unknown tags, stale pages, source drift, and contested claims.
- Refactor: merge duplicate pages, split oversized pages, archive superseded pages, update inbound links.
- Reflect: search for counter-evidence first, then synthesize patterns, gaps, contradictions, and next questions.
- Merge: deduplicate pages by slug and aliases, preserving sources and personal positions.
- Add question: normalize open questions into `wiki/QUESTIONS.md` so future ingests can answer them.

Read `references/ingestion-policy.md` before source ingestion, re-ingestion, dependency-map, or web-clipper work. Read `references/confidence-policy.md` before changing confidence, source counts, or stale review fields. Read `references/operations.md` before reflect, merge, add-question, evolution-log, or durable output work.

## Page Types

Use the template in `templates/` when creating a page:

- `source.md`: normalized source notes under `wiki/sources/`.
- `web-clipper-source.md`: source notes created from Obsidian Web Clipper or browser saves.
- `concept.md`: `wiki/concepts/` ideas such as RAG, evals, agentic workflows, memory, alignment.
- `tool.md`, `paper.md`, `person.md`: `wiki/entities/` products, models, libraries, papers, researchers, founders, maintainers.
- `workflow.md`, `prompt.md`, `map-of-content.md`: `wiki/synthesis/` reusable processes, prompt patterns, maps, and cross-source analysis.
- `question.md`: durable answers filed from `wiki/QUESTIONS.md`.
- `personal-writing.md`: source notes for `raw/personal/` material. These may update "My Position" sections but do not count as external support.

## Tool Neutrality

This skill is intentionally not tied to one agent. Use whatever equivalent tools are available:

- File listing, file reading, and file writing.
- Text search over the vault.
- Web page extraction for URLs.
- PDF or document text extraction for local files.
- A scripting/runtime tool for audits when available.

If a tool named in another agent's documentation is unavailable, translate the action to the local equivalent instead of stopping.

Compatibility target: Claude Code, OpenCode, OpenClaw, Hermes, Codex, Gemini-style agents, and any file-capable agent. The generated vault includes `CLAUDE.md` because the tutorial names that file as the behavior contract; its content must remain portable and not Claude-only. Other agents should read it as ordinary Markdown.

Do not make Claude Code, qmd, or any other single tool a hard dependency. If qmd-style commands are available, they are optional accelerators; otherwise use normal file reads, search, and scripts. See `references/optional-integrations.md` for adapters.

## Quality Bar

Good LLM Wiki work should leave the vault easier to navigate than before:

- Fewer duplicate concepts.
- More useful cross-links.
- Better source traceability.
- Clear confidence levels for weak or fast-moving claims.
- A log entry that lets the next agent resume without guessing.

Use scripts in `scripts/` when available:

```bash
python3 scripts/init_knowledge_base.py /path/to/knowledge-base
python3 scripts/scan_sources.py /path/to/vault
python3 scripts/scan_sources.py /path/to/vault --write
python3 scripts/build_source_dependencies.py /path/to/vault --write
python3 scripts/lint_wiki.py /path/to/vault
python3 scripts/rebuild_index.py /path/to/vault --write
```
