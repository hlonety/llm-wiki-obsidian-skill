# Obsidian Conventions

Use these conventions when the user wants an Obsidian-first LLM Wiki.

## Folder Layout

```text
00 Meta/       schema, index, logs, topic maps
10 Sources/    immutable source captures and normalized source notes
20 Concepts/   durable ideas and technical concepts
30 Tools/      models, products, APIs, plugins, frameworks
40 People/     researchers, maintainers, authors, founders
50 Papers/     paper-level notes
60 Workflows/  repeatable processes and playbooks
70 Prompts/    reusable prompts and prompt patterns
80 Questions/  durable answers filed from queries
90 Maps/       MOCs, learning paths, overview maps
assets/        images and attachments
_archive/      superseded pages
```

## Filenames and Links

- Use lowercase kebab-case filenames: `agentic-workflow.md`.
- Use frontmatter `title` for readable names: `title: Agentic Workflow`.
- Link by filename stem: `[[agentic-workflow]]`.
- Use aliases for alternate names.
- Prefer explicit links over tag-only organization.

## Standard Frontmatter

```yaml
---
title: Page Title
aliases: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: concept | tool | paper | person | workflow | prompt | question | map
status: seed | growing | stable | contested | archived
tags: []
sources: []
confidence: medium
---
```

Optional fields:

```yaml
evidence:
  - source: "[[source-slug]]"
    claim: "Short claim supported by the source."
contested: true
contradictions: []
freshness: stable | fast-moving | stale
review_after: YYYY-MM-DD
```

## AI Knowledge Taxonomy

Start with this tag taxonomy for an AI vault. Add tags deliberately in `00 Meta/SCHEMA.md` before using them.

- Areas: `agent`, `llm`, `rag`, `memory`, `evaluation`, `prompt`, `workflow`, `automation`
- Technical: `architecture`, `training`, `fine-tuning`, `inference`, `tool-use`, `mcp`, `data`
- Objects: `model`, `paper`, `tool`, `framework`, `benchmark`, `dataset`, `company`, `person`
- Quality: `security`, `privacy`, `reliability`, `alignment`, `cost`, `latency`
- Meta: `comparison`, `timeline`, `controversy`, `prediction`, `learning-path`

## Dataview Examples

Pages needing review:

```dataview
TABLE status, confidence, updated
FROM "20 Concepts" OR "30 Tools" OR "50 Papers"
WHERE status = "contested" OR confidence = "low"
SORT updated ASC
```

Recently updated pages:

```dataview
TABLE type, status, tags
FROM "20 Concepts" OR "30 Tools" OR "50 Papers" OR "60 Workflows"
SORT updated DESC
LIMIT 20
```

Source-backed tool notes:

```dataview
TABLE sources, confidence
FROM "30 Tools"
WHERE length(sources) > 0
SORT title ASC
```

## Source Notes

A source note is not the same as a concept page. A source note captures what one source said. A concept page synthesizes across one or more sources.

Recommended source frontmatter:

```yaml
---
title: Source Title
source_url:
author:
published:
captured: YYYY-MM-DD
type: source
source_kind: article | paper | transcript | clip | note
sha256:
tags: []
---
```

Keep source notes close to the source. Put interpretation in linked wiki pages.

