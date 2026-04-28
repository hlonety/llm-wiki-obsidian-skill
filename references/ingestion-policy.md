# Ingestion Policy

Use this policy when turning raw material into durable wiki pages.

## Source Lifecycle

Source notes move through a small queue:

- `processed: false`: captured but not integrated.
- `processed: true`: source has been summarized and affected wiki pages were updated.
- `possibly_outdated: true`: source content, URL, or hash changed and needs review.
- `last_verified`: last date an agent checked the source against the wiki.

When a raw file changes, do not patch wiki pages from memory. Re-read the source, compare it with the previous source note, update affected pages, and log the change.

## Required Source Fields

Prefer these frontmatter fields for source notes:

```yaml
source_url:
domain:
author:
published:
captured:
language:
canonical_source:
processed: false
raw_file:
raw_sha256:
sha256:
last_verified:
possibly_outdated: false
```

Use `raw_file` for the exact capture or attachment path. Use `raw_sha256` for that raw file's hash. Use `sha256` for a markdown source note body hash when needed.

## Page Creation

Before creating a page:

1. Search existing filenames.
2. Search titles and aliases.
3. Search Chinese and English names if applicable.
4. Prefer one canonical English lowercase kebab-case filename.
5. Put Chinese names, abbreviations, and alternate spellings in `aliases`.

Create pages only for concepts central to a source or recurring across sources. Otherwise add a mention to the relevant existing page.

## Dependency Map

After ingesting or re-ingesting sources, run:

```bash
python3 scripts/build_source_dependencies.py /path/to/vault --write
```

Use `00 Meta/source-dependencies.json` to answer:

- Which wiki pages depend on this source note?
- Which wiki pages may be stale after this raw file changed?
- Which source notes point to a deleted or outdated raw capture?

## Log Semantics

Use precise log language:

- `reinforced`: new source supports an existing claim.
- `corrected`: new source changes an existing claim.
- `contradicted`: source conflicts with existing evidence.
- `re-ingested`: source hash or extraction changed and pages were reviewed.
- `personal-position`: user writing changed a `## My Position` section.

