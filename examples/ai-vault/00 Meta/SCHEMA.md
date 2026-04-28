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
- Store durable answers and reports in `95 Outputs/`.
- Keep open questions in `00 Meta/questions.md`.
- Personal writing may update positions but does not count as external source support.

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

## Confidence

- One external source: `confidence: low`.
- Three or more external sources: `confidence: medium`.
- Five or more external sources: candidate for high confidence.
- `confidence: high` requires explicit user confirmation.

## Staleness

- `domain_volatility: high` should be reviewed after 90 days.
- `domain_volatility: medium` should be reviewed after 180 days.
- `domain_volatility: low` should be reviewed after 365 days.

## Update Policy

When information conflicts, keep both claims with dates and sources, mark the page `contested: true`, and flag it for user review.
