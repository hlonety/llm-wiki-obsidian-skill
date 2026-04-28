# LLM Behavior Contract

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
