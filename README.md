# LLM Wiki Obsidian Skill

A portable agent skill for maintaining an Obsidian-first LLM Wiki based on Andrej Karpathy's LLM Wiki pattern.

It is designed for AI knowledge bases: LLMs, agents, prompts, tools, papers, workflows, evaluation, RAG, MCP, automation, and learning notes.

## What It Does

This skill teaches an agent to maintain a compounding Markdown wiki:

- Preserve raw sources.
- Compile durable concept, tool, paper, prompt, workflow, and question pages.
- Keep Obsidian wikilinks and frontmatter clean.
- Track sources, confidence, stale claims, and contradictions.
- Audit broken links, missing index entries, orphan pages, and drift.

## Install

### Codex

Ask Codex to install or use this skill from the GitHub repository URL:

```text
Install the skill from https://github.com/hlonety/llm-wiki-obsidian-skill
```

If installing manually, copy this repository into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/hlonety/llm-wiki-obsidian-skill ~/.codex/skills/llm-wiki-obsidian
```

Restart Codex after installation.

### Other Agents

Point the agent at `SKILL.md` and ask it to follow the instructions. The skill avoids provider-specific tool names, so Claude, Gemini, Codex, and other file-capable agents can adapt it.

## Quick Start

Create an AI knowledge vault:

```text
Use llm-wiki-obsidian to create an Obsidian vault for my AI knowledge base at ~/wiki/ai.
```

Ingest a source:

```text
Use llm-wiki-obsidian to add this article to my AI vault and update related concept pages: https://example.com/article
```

Query the wiki:

```text
Based on my LLM Wiki, explain the difference between RAG memory and compiled wiki memory.
```

Audit the vault:

```bash
python3 scripts/lint_wiki.py ~/wiki/ai
```

Rebuild the index:

```bash
python3 scripts/rebuild_index.py ~/wiki/ai --write
```

## Recommended Obsidian Layout

```text
00 Meta/
10 Sources/
20 Concepts/
30 Tools/
40 People/
50 Papers/
60 Workflows/
70 Prompts/
80 Questions/
90 Maps/
assets/
_archive/
```

## Source

Inspired by Andrej Karpathy's original LLM Wiki method:

https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

## License

MIT

