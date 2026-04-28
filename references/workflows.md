# Workflows

## Initialize a Vault

1. Confirm the vault path.
2. Create the default Obsidian layout.
3. Ask for the domain if it is unclear. For the default AI vault, use "AI, LLMs, agents, prompts, tools, papers, workflows, and learning notes."
4. Write `00 Meta/SCHEMA.md` with:
   - domain
   - folder layout
   - page types
   - tag taxonomy
   - page creation thresholds
   - confidence and source-count policy
   - update and contradiction policy
5. Write `00 Meta/index.md` with section headings for all page types.
6. Write `00 Meta/log.md` with an initialization entry.
7. Write `00 Meta/questions.md` with Open and Resolved sections.
8. Write `00 Meta/overview.md` with a small health dashboard.
9. Create empty `00 Meta/source-manifest.json` and `00 Meta/source-dependencies.json` when practical.
10. Suggest 3-5 first sources or topics.

## Ingest a Source

1. Capture the raw source under `10 Sources/`.
2. Run `scripts/scan_sources.py <vault> --write` when available to compute hashes and detect new or changed files.
3. Add source metadata: URL/path, domain, author if known, captured date, language, `processed`, `raw_file`, `raw_sha256`, `last_verified`, and `possibly_outdated` when practical.
4. If using `00 Meta/source-manifest.json`, copy the source file's SHA-256 into the related source note when creating one.
5. Extract candidate concepts, tools, people, papers, prompts, workflows, and claims.
6. Search existing pages before creating new ones.
7. Check filename stems, titles, and aliases before creating pages. Use English lowercase kebab-case slugs; put Chinese names in `title` and `aliases`.
8. Update pages that already cover the topic.
9. Create new pages only when the source is central to the topic or the topic appears across multiple sources.
10. Add sources and evidence to frontmatter or a Sources section.
11. If the source is personal writing, update `## My Position` sections but do not increment external `source_count`.
12. Add wikilinks in both directions when useful.
13. Set the source note `processed: true` only after affected wiki pages have been updated.
14. Check `00 Meta/questions.md` for questions the source might answer.
15. Run `scripts/build_source_dependencies.py <vault> --write` when available.
16. Update index and log.
17. Report created and modified files.

## Web Clipper Intake

Use this when the user clips pages with Obsidian Web Clipper, a browser save, or another capture tool.

1. Save the clip under `10 Sources/clips/` or a topic-specific subfolder.
2. Use `templates/web-clipper-source.md`.
3. Fill `source_url`, `domain`, `captured`, `language`, and obvious author/published fields.
4. Leave `processed: false` until the clip has updated wiki pages.
5. Do not create concept pages during clipping unless the user explicitly asks for immediate ingest.
6. During the next ingest batch, process clips marked `processed: false`.

## Scan Sources

Use when the user asks whether there are new files, changed files, or raw files that need ingesting.

1. Run:
   ```bash
   python3 scripts/scan_sources.py /path/to/vault
   ```
2. Review files marked `new`, `changed`, or `deleted`.
3. If the report looks correct, run:
   ```bash
   python3 scripts/scan_sources.py /path/to/vault --write
   ```
4. Ingest `new` and `changed` files.
5. Treat `deleted` files as a warning. Do not remove wiki pages automatically; ask the user what happened.

## Build Source Dependencies

Use when hashes changed, when a source note was ingested, or before a maintenance pass.

1. Run:
   ```bash
   python3 scripts/build_source_dependencies.py /path/to/vault
   ```
2. Review which source notes and raw files map to which wiki pages.
3. If the map looks correct, run:
   ```bash
   python3 scripts/build_source_dependencies.py /path/to/vault --write
   ```
4. When a raw file changes later, use `00 Meta/source-dependencies.json` to identify pages needing review.

## Re-ingest Changed Sources

1. Run `scripts/scan_sources.py <vault>` and list `changed` files.
2. Read `00 Meta/source-dependencies.json` to identify source notes and affected pages.
3. Re-extract the changed source. Do not assume the previous summary is still accurate.
4. Update the source note with new hash fields and set `last_verified`.
5. Update affected wiki pages. Mark claims as corrected, reinforced, contradicted, or removed.
6. If uncertainty remains, set `possibly_outdated: true` on the source note or `status: contested` on affected pages.
7. Rebuild source dependencies, rebuild the index if pages changed, and add a log entry.

## Query the Wiki

1. Read schema, index, and recent log if not already oriented.
2. Search for key terms and aliases.
3. Read relevant wiki pages before raw sources.
4. Answer from compiled pages first.
5. Cite the wiki pages and important source notes.
6. If the answer is durable, create a question, comparison, map, workflow, or output page.
7. Log the query when it changes or adds knowledge.

## Audit the Wiki

Check:

- Broken wikilinks.
- Orphan pages with no inbound links.
- Pages missing from index.
- Missing or invalid frontmatter.
- Tags not listed in schema.
- Source files with changed hashes.
- Unprocessed or possibly outdated source notes.
- Source dependency drift after hash changes.
- Large pages that should be split.
- Duplicate pages for the same concept.
- Near-duplicate slugs.
- Non-kebab wikilinks and links to system/output pages such as `[[log]]`.
- Duplicate source URLs.
- Alias overlaps, especially cross-language duplicates.
- Stale pages based on `domain_volatility`.
- Stub pages with too little body content.
- `confidence: high` without explicit confirmation.
- Personal writing incorrectly counted as external source support.
- Low-confidence or contested pages needing user review.

Use `scripts/lint_wiki.py` when available.

## Refactor the Wiki

Use refactors to reduce entropy:

- Merge duplicates into one canonical page and redirect links.
- Split pages longer than about 200 lines.
- Move superseded pages to `_archive/`.
- Convert repeated answer patterns into workflow pages.
- Promote important query answers from `80 Questions/` into concepts, comparisons, or maps.

Before reorganizing more than 10 files, describe the plan and ask for confirmation.

## Promote Confidence

1. Count only independent external sources.
2. Leave single-source claims at `confidence: low`.
3. Use `confidence: medium` when three or more external sources broadly agree.
4. When a page reaches five or more external sources, show the user the definition, source list, and known contradictions.
5. Promote to `confidence: high` only after explicit user confirmation.
6. Record `high_confirmed`, `high_confirmed_by`, and `high_confirmed_on`.

## Personal Writing

1. Store the writing under `10 Sources/personal/`.
2. Capture its hash and metadata.
3. Extract the user's claims and positions.
4. Add those views to relevant concept pages under `## My Position`.
5. Do not increment `source_count`.
6. Do not promote confidence based on the user's own writing.
7. Log the position update.

## Daily Rhythm

- Daily: clip useful sources quickly and leave them `processed: false`.
- Weekly: ingest the queue, update source hashes, and build dependencies.
- Every two weeks: run the audit and clean duplicates, stale pages, and broken links.
- Monthly: reflect on gaps, contradictions, and high-value open questions.
