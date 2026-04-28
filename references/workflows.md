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
9. Suggest 3-5 first sources or topics.

## Ingest a Source

1. Capture the raw source under `10 Sources/`.
2. Run `scripts/scan_sources.py <vault> --write` when available to compute hashes and detect new or changed files.
3. Add source metadata: URL/path, author if known, captured date, hash when practical.
4. If using `00 Meta/source-manifest.json`, copy the source file's SHA-256 into the related source note when creating one.
5. Extract candidate concepts, tools, people, papers, prompts, workflows, and claims.
6. Search existing pages before creating new ones.
7. Update pages that already cover the topic.
8. Create new pages only when the source is central to the topic or the topic appears across multiple sources.
9. Add sources and evidence to frontmatter or a Sources section.
10. If the source is personal writing, update `## My Position` sections but do not increment external `source_count`.
11. Add wikilinks in both directions when useful.
12. Check `00 Meta/questions.md` for questions the source might answer.
13. Update index and log.
14. Report created and modified files.

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
- Large pages that should be split.
- Duplicate pages for the same concept.
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
