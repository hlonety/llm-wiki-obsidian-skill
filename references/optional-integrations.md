# 可选集成

这个 skill 是工具中立的。某些工具可以加快操作，但知识库必须仍然能通过普通的文件读取、搜索、编辑和脚本运行来使用。

## qmd

有些 LLM Wiki 教程会使用一个叫 `qmd` 的命令，用来做 Markdown 查询、批量读取、添加文件或查看状态。这里把它当成可选的便利层，而不是必须安装的运行环境。

如果当前环境有 `qmd`：

- 可以用 `qmd query` 快速搜索知识库。
- 可以用 `qmd multi-get` 一次读取多篇笔记。
- 只有在它能保留文件名、frontmatter 和 wikilink 约定时，才用 `qmd add` 添加文件。
- 可以用 `qmd status` 辅助查看状态，但仍然应该运行本 skill 的哈希扫描和审计脚本。

如果当前环境没有 `qmd`，就把同一类动作翻译成普通操作：

- query -> 用 `rg` 或 agent 自带搜索。
- multi-get -> 正常读取多个文件。
- add -> 正常创建或编辑 Markdown 文件。
- status -> 用 `git status`、`scripts/lint_wiki.py` 或直接检查知识库。

## Agent 规则文件

不同 agent 可以有自己的入口文件，但这些文件应该只做转发，不要复制整套规则：

- Claude Code：`CLAUDE.md`
- Codex / OpenAI 风格 agent：`AGENTS.md` 或已安装的 skill 目录
- Gemini 风格 agent：`GEMINI.md`
- Hermes：`HERMES.md` 或本地 skill wrapper
- OpenClaw：`OPENCLAW.md` 或本地 skill wrapper
- OpenCode：本地 skill 或 rules wrapper

这些文件要保持很短。它们只需要说明知识库位置，并要求 agent 遵守 `CLAUDE.md` 和 `$llm-wiki-obsidian`。不要把所有规则重复粘贴进去，否则后续维护会出现多份规则不一致的问题。

## Obsidian Web Clipper

Web Clipper 只作为原始资料入口使用：

1. 把原始剪藏保存到 `raw/clippings/`。
2. 在 `wiki/sources/` 里用 `templates/web-clipper-source.md` 创建来源摘要。
3. 初始保留 `processed: false`。
4. 后续批量吸收进 wiki 页面后，再改成 `processed: true`。
