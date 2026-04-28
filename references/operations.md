# Operations

Use these operations when the user asks for deeper maintenance beyond normal ingest and query.

## ADD-QUESTION

Use when the user says they want to understand something, record a question, or keep an open problem.

Steps:

1. Normalize the question into one clear sentence.
2. Append it to `00 Meta/questions.md`:
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
3. Deep synthesis: write a durable page under `80 Questions/`, `90 Maps/`, or `95 Outputs/` only when the result would be painful to recreate.
4. Gap report: list concepts with one source, open questions with no sources, stale high-volatility pages, and important topics with thin coverage.
5. Update `00 Meta/overview.md`, `00 Meta/index.md`, and `00 Meta/log.md`.

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
- Move superseded pages to `_archive/` or replace them with a small redirect note if the user's vault convention supports redirects.
- Log the merge.

For cross-language duplicates, keep the English slug and put Chinese names in `aliases` and in the visible title where useful.

## QUERY OUTPUTS

If an answer is durable, save it. Use `95 Outputs/` for:

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

