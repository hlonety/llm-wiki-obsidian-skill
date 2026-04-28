# Karpathy Method

Karpathy's LLM Wiki pattern treats a knowledge base as a compiled artifact, not a pile of retrieved chunks.

## Core Insight

Traditional RAG usually keeps raw documents as the primary memory. Each query retrieves chunks and asks the model to synthesize an answer in the moment. That is useful, but the same synthesis work is repeated again and again.

An LLM Wiki changes the unit of memory:

```text
raw sources -> compiled wiki pages -> future answers and updates
```

The expensive part is not storing text. The expensive part is deciding what matters, how it relates to existing knowledge, what changed, and where contradictions live. The wiki captures those decisions so later agents can build on them.

## The Three Layers

### 1. Raw Sources

Raw sources are evidence. They may be web articles, papers, transcripts, screenshots, pasted notes, newsletters, meeting notes, or exported chats.

Rules:

- Preserve the original source as much as practical.
- Add metadata such as URL, author, captured date, and hash.
- Do not rewrite raw source files during synthesis.
- If the source changes later, add a new capture or record drift.

### 2. Wiki

The wiki is the compiled knowledge layer. It is allowed to be edited, merged, split, corrected, and cross-linked.

Wiki pages should answer questions like:

- What is this thing?
- Why does it matter?
- What evidence supports it?
- What changed over time?
- What is it related to?
- What is uncertain or contested?

The wiki is not a summary dump. It is a living map.

### 3. Schema

The schema is the instruction layer for future agents. It defines page types, directory structure, tags, naming conventions, update rules, source policy, and quality standards.

Without a schema, each agent invents its own organization. With a schema, every session starts from the same mental model.

## Human-Agent Division of Labor

The human decides what domains matter, which sources are worth adding, and when synthesis is useful. The agent preserves sources, extracts structure, updates pages, links ideas, flags uncertainty, and keeps navigation healthy.

The agent should not silently make high-impact editorial decisions. If a change would alter many pages, resolve contested claims, or reorganize the vault, it should explain the proposed change first.

## Why Obsidian Fits

Obsidian is a good home for LLM Wiki because it uses plain Markdown, stable file paths, wikilinks, backlinks, graph view, YAML frontmatter, aliases, and optional Dataview queries. The vault remains useful even without any particular agent or app.

## Failure Modes

- Raw and synthesis get mixed together, making provenance unclear.
- Agents create a new page for every named entity, producing noise.
- Tags grow freely until they stop meaning anything.
- Index and logs are skipped, so every session starts cold.
- Old claims are overwritten instead of being dated and compared.
- The wiki becomes a set of summaries rather than a network of concepts.

The skill's rules are designed to prevent these failures.

