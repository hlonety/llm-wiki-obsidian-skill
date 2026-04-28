# Wiki Schema

## Domain

AI, LLMs, agents, prompts, tools, papers, workflows, evaluation, RAG, MCP, automation, and learning notes.

## Conventions

- Use lowercase kebab-case filenames.
- Use YAML frontmatter on every wiki page.
- Preserve source notes under `10 Sources/`.
- Put synthesis pages under `20 Concepts/` through `90 Maps/`.
- Link related pages with Obsidian wikilinks.
- Update `00 Meta/index.md` and `00 Meta/log.md` after non-trivial changes.

## Tag Taxonomy

- Areas: `agent`, `llm`, `rag`, `memory`, `evaluation`, `prompt`, `workflow`, `automation`
- Technical: `architecture`, `training`, `fine-tuning`, `inference`, `tool-use`, `mcp`, `data`
- Objects: `model`, `paper`, `tool`, `framework`, `benchmark`, `dataset`, `company`, `person`
- Quality: `security`, `privacy`, `reliability`, `alignment`, `cost`, `latency`
- Meta: `comparison`, `timeline`, `controversy`, `prediction`, `learning-path`

## Page Thresholds

- Create a page when a concept is central to one source or appears meaningfully in two or more sources.
- Add to an existing page when the source reinforces or updates an existing concept.
- Do not create pages for passing mentions.
- Split pages longer than about 200 lines.

## Update Policy

When information conflicts, keep both claims with dates and sources, mark the page `contested: true`, and flag it for user review.

