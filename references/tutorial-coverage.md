# Tutorial Coverage

Use this file to check that the skill remains at least as complete as the raw/wiki LLM Wiki tutorial layout.

## Strict Directory Parity

The default generated vault uses the tutorial structure:

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
  scripts/
    lint.py
  BOOTSTRAP_PROMPT.md
  UPGRADE_PROMPT.md
  CLAUDE.md
  README.md
```

The skill adds hidden generated state under `wiki/.state/`:

- `source-manifest.json`
- `source-dependencies.json`

These files support SHA-256 and impact analysis without changing the visible tutorial layout.

## Functional Parity

- Raw sources are immutable under `raw/`.
- Source summaries live under `wiki/sources/`.
- Compiled concepts live under `wiki/concepts/`.
- Entities live under `wiki/entities/`.
- Cross-source analysis lives under `wiki/synthesis/`.
- Durable answers and reports live under `wiki/outputs/`.
- `wiki/index.md` is the first wiki file to read.
- `wiki/log.md` is append-only.
- `wiki/overview.md` is the health dashboard.
- `wiki/QUESTIONS.md` is the open question queue.
- `CLAUDE.md` is the behavior contract, but its content is portable to non-Claude agents.
- `BOOTSTRAP_PROMPT.md` and `UPGRADE_PROMPT.md` are generated for initialization and system upgrades.
- `scripts/lint.py` is generated as the local health-check entrypoint.

## Enhancements Beyond The Tutorial

- SHA-256 scan with `scripts/scan_sources.py`.
- Generated source manifest under `wiki/.state/source-manifest.json`.
- Source dependency map with `scripts/build_source_dependencies.py`.
- Raw-file to source-note to wiki-page impact tracing.
- Source lifecycle fields: `processed`, `raw_file`, `raw_sha256`, `last_verified`, `possibly_outdated`, `canonical_source`, `language`, `domain`.
- Web Clipper queue: raw clips in `raw/clippings/`, notes in `wiki/sources/`, `processed: false` until ingested.
- Duplicate source URL detection.
- Near-duplicate slug detection.
- Non-kebab wikilink detection.
- Forbidden links to maintenance pages such as `[[log]]` and `[[index]]`.
- High-confidence promotion requires explicit human confirmation.
- Personal writing does not count toward external `source_count`.
- Staleness checks using `domain_volatility` and `last_reviewed`.
- Evolution-log verbs: reinforced, corrected, contradicted, re-ingested, personal-position.
