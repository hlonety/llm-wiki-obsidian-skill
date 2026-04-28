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
   - update and contradiction policy
5. Write `00 Meta/index.md` with section headings for all page types.
6. Write `00 Meta/log.md` with an initialization entry.
7. Suggest 3-5 first sources or topics.

## Ingest a Source

1. Capture the raw source under `10 Sources/`.
2. Add source metadata: URL/path, author if known, captured date, hash when practical.
3. Extract candidate concepts, tools, people, papers, prompts, workflows, and claims.
4. Search existing pages before creating new ones.
5. Update pages that already cover the topic.
6. Create new pages only when the source is central to the topic or the topic appears across multiple sources.
7. Add sources and evidence to frontmatter or a Sources section.
8. Add wikilinks in both directions when useful.
9. Update index and log.
10. Report created and modified files.

## Query the Wiki

1. Read schema, index, and recent log if not already oriented.
2. Search for key terms and aliases.
3. Read relevant wiki pages before raw sources.
4. Answer from compiled pages first.
5. Cite the wiki pages and important source notes.
6. If the answer is durable, create a question, comparison, map, or workflow page.
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

