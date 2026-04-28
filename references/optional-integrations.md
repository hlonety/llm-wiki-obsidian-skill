# Optional Integrations

This skill is tool-neutral. Optional integrations can speed up work, but the wiki must still be usable through ordinary file reads, search, edits, and scripts.

## qmd

Some LLM Wiki tutorials use a command named `qmd` for quick Markdown operations such as query, multi-get, add, or status. Treat it as an optional convenience layer, not as a required runtime.

If `qmd` is available:

- Use `qmd query` as a fast search over the vault.
- Use `qmd multi-get` to read several notes.
- Use `qmd add` only if it preserves the vault's filename, frontmatter, and wikilink conventions.
- Use `qmd status` as a helper, then still run the repository scripts for source scans and audits when available.

If `qmd` is unavailable, translate the same operation:

- query -> `rg` or agent-native search,
- multi-get -> normal file reads,
- add -> normal file edits,
- status -> `git status`, `scripts/lint_wiki.py`, or vault inspection.

## Agent Rules Files

Platform-specific rule files may point back to this skill:

- Claude Code: `CLAUDE.md`
- Codex/OpenAI-style agents: `AGENTS.md` or installed skill folder
- Gemini-style agents: `GEMINI.md`
- Hermes/OpenClaw/OpenCode: their local skill or rules wrapper

Keep those files short. They should name the vault path and tell the agent to follow this skill. Do not duplicate all instructions there.

## Obsidian Web Clipper

Use Web Clipper as an intake tool:

1. Clip into `10 Sources/clips/`.
2. Use `templates/web-clipper-source.md`.
3. Leave `processed: false`.
4. Later, batch ingest the queue and set `processed: true` only after wiki pages are updated.

