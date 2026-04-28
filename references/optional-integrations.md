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

## Obsidian CLI

`obsidian` CLI 是可选加速器，适合在 Obsidian 已打开时读取当前文件、搜索 vault、追加内容、查看 backlinks 或管理 properties。

如果当前环境有 `obsidian`：

- 可以用 `obsidian help` 查看当前可用命令。
- 可以用 `obsidian read` 读取当前或指定笔记。
- 可以用 `obsidian search` 搜索 vault。
- 可以用 `obsidian property:set` 辅助修改 properties。
- 修改后仍要运行本 skill 的 lint、哈希扫描或依赖图脚本。

如果当前环境没有 `obsidian`，就回退到普通文件操作：

- read -> 正常读取 Markdown 文件。
- search -> `rg`。
- property:set -> 编辑 YAML frontmatter。
- backlinks -> `rg "\\[\\[page-slug"`。

不要因为缺少 Obsidian CLI 停止任务。

## Defuddle

`defuddle` 是可选网页清洗工具，适合把普通网页、博客、在线文档转换成较干净的 Markdown。

如果当前环境有 `defuddle`：

- 用 Markdown 输出保存网页内容。
- 把清洗结果先放进 `raw/articles/` 或 `raw/clippings/`。
- 再创建 `wiki/sources/` 来源摘要，并按 LLM Wiki 流程吸收进概念页。

如果当前环境没有 `defuddle`，就使用当前 agent 可用的网页读取能力，例如浏览器、Playwright、Jina Reader、curl 或用户提供的本地导出。

不要把 defuddle 输出直接当成最终 wiki 页面。它只是来源捕获的一步，后面仍要保留 raw 文件、计算哈希、创建 source note、更新概念和日志。

## Obsidian Bases 和 Canvas

Bases 和 Canvas 是可选的人工阅读增强：

- `.base` 仪表盘建议保存到 `wiki/outputs/`。
- `.canvas` 知识地图建议保存到 `wiki/synthesis/` 或 `wiki/outputs/`。
- `templates/source-queue.base` 可用于来源处理队列。
- `templates/wiki-health.base` 可用于健康检查视图。
- `templates/concept-map.canvas` 可用于最小知识流地图。

这些文件不能替代 `wiki/index.md`、`wiki/log.md`、来源哈希、依赖图和 lint。
