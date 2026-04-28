# Operations

Use these operations when the user asks for deeper maintenance beyond normal ingest and query.

## ADD-QUESTION

Use when the user says they want to understand something, record a question, or keep an open problem.

Steps:

1. Normalize the question into one clear sentence.
2. Append it to `wiki/QUESTIONS.md`:
   ```markdown
   - [ ] Question text (opened YYYY-MM-DD)
   ```
3. Add useful aliases or related pages if obvious.
4. Log the action.

During future ingest, check whether new sources help answer open questions.

## REFLECT

Use when the user asks to reflect, synthesize, find patterns, or discover gaps.

Stages:

1. Counter-evidence first: before writing a synthesis, search existing sources and pages for disagreement. If none is found, add a limitation note that the synthesis may have echo-chamber risk.
2. Pattern scan: search concepts, tools, people, papers, workflows, prompts, and prior question outputs for repeated themes, contradictions, underlinked pages, and gaps.
3. Deep synthesis: write a durable page under `wiki/synthesis/` or `wiki/outputs/` only when the result would be painful to recreate.
4. Gap report: list concepts with one source, open questions with no sources, stale high-volatility pages, and important topics with thin coverage.
5. Update `wiki/overview.md`, `wiki/index.md`, and `wiki/log.md`.

Do not manufacture certainty. A useful reflect pass often produces open questions and limitations.

## MERGE

Use when pages are duplicates, aliases overlap, or the user asks to deduplicate.

Rules:

- Ask before merging if more than two pages are affected or if either page contains personal positions.
- Prefer one canonical English kebab-case slug.
- Merge `aliases` as a set.
- Merge source lists without duplicate entries.
- Preserve personal positions in a dedicated section.
- Update inbound wikilinks.
- Move superseded pages to `wiki/outputs/archive/`, mark them `status: archived`, or replace them with a small redirect note if the user's vault convention supports redirects.
- Log the merge.

For cross-language duplicates, keep the English slug and put Chinese names in `aliases` and in the visible title where useful.

## QUERY OUTPUTS

If an answer is durable, save it. Use `wiki/outputs/` for:

- deep answers,
- comparison tables,
- gap reports,
- reflection reports,
- slide outlines,
- charts or generated code snippets.

Trivial lookups do not need output files.

Every durable output should include:

- the question or task,
- short answer,
- evidence links,
- confidence notes,
- limitations,
- next questions.

Choose the output shape by task:

- normal answer: Markdown note,
- comparison: Markdown table,
- presentation: Marp-compatible slide outline,
- trend or metric analysis: Python code plus chart output notes,
- checklist: structured bullets with owners or statuses when known.

## EVOLUTION LOG

Use the log to make the next agent's job easier. Each meaningful update should say what changed and why.

Recommended verbs:

- `reinforced`: a new source supports an existing claim.
- `corrected`: a page was changed because newer or better evidence replaced an old claim.
- `contradicted`: a source conflicts with an existing page and the page now carries both claims.
- `re-ingested`: a source hash or extraction changed and affected pages were reviewed.
- `personal-position`: user writing changed the user's own stance without increasing external source count.

Good log entries include the source note, affected pages, and remaining uncertainty.
