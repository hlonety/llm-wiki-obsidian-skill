# Obsidian 适配层

这份文件把 Obsidian 相关技能接到 LLM Wiki 工作流里。核心原则：LLM Wiki 负责知识管理方法论，Obsidian 适配层只负责文件格式、视图、画布、CLI 和网页清洗。

参考来源：[kepano/obsidian-skills](https://github.com/kepano/obsidian-skills)。该项目使用 MIT License，Copyright (c) 2026 Steph Ango (@kepano)。本文件只做中文化整理和 LLM Wiki 场景改编；不要把外部工具变成硬依赖。

## 总体边界

- 保持严格 `raw/wiki` 架构不变。
- Obsidian 专属文件只放在合适的输出层：`.base` 放 `wiki/outputs/`，`.canvas` 放 `wiki/synthesis/` 或 `wiki/outputs/`。
- 任何 Obsidian 视图、画布、CLI 操作都不能替代 `raw/` 来源保存、SHA-256 扫描、依赖图和 `wiki/log.md`。
- 当 Obsidian 工具不可用时，回退到普通文件读写、`rg` 搜索和本 skill 的 Python 脚本。

## obsidian-markdown

用于创建和编辑 Obsidian Flavored Markdown。

在 LLM Wiki 中使用时：

- 普通 wiki 页面继续使用 YAML frontmatter。
- 内部链接优先使用 wikilink：`[[agentic-workflow]]` 或 `[[agentic-workflow|Agentic workflow]]`。
- 外部来源 URL 使用普通 Markdown 链接或 frontmatter 字段，不要伪装成 wikilink。
- 图片、PDF、音频、视频等附件可以用 `![[file.png]]`、`![[paper.pdf#page=3]]` 嵌入，但原始文件仍放 `raw/images/` 或 `raw/pdfs/`。
- Callout 只用于增强人工阅读，不作为唯一的结构化字段。关键状态仍写入 frontmatter。
- 标签必须服从 `CLAUDE.md` 中的 tag taxonomy，不能因为 Obsidian 支持自由 tag 就随意扩散。

适合使用的场景：

- 写概念页、来源摘要、工作流、问题页。
- 给人工阅读页面增加 callout、embed、footnote、LaTeX 或 Mermaid。
- 整理 Obsidian properties 和 aliases。

## obsidian-bases

用于创建 `.base` 文件，把 Markdown 页面显示成表格、卡片、列表或地图视图。

在 LLM Wiki 中使用时：

- `.base` 文件属于可选仪表盘，建议放在 `wiki/outputs/`。
- 不要把 `.base` 当成唯一索引；`wiki/index.md` 仍是 agent 首读入口。
- Bases 可以展示待处理来源、低置信度页面、过期页面、开放问题和输出清单。
- 生成 `.base` 后，仍要运行 `scripts/lint_wiki.py` 检查知识库结构。

推荐模板：

- `templates/source-queue.base`：查看 `processed: false` 或 `possibly_outdated: true` 的来源页。
- `templates/wiki-health.base`：查看低置信度、争议、高波动、待复查页面。

使用规则：

- `.base` 必须是合法 YAML。
- 字符串中含有 `:`、`#`、引号、括号时优先加引号。
- 引用公式字段时，先在 `formulas` 中定义，再在视图里使用 `formula.name`。

## json-canvas

用于创建 `.canvas` 文件，生成 Obsidian Canvas 知识地图。

在 LLM Wiki 中使用时：

- `.canvas` 是可选的可视化输出，不是事实来源。
- 概念地图建议保存到 `wiki/synthesis/`，汇报型画布可以保存到 `wiki/outputs/`。
- Canvas 节点可以引用 wiki 页面，但事实依据仍要回到页面的 `sources` 或 `evidence`。
- 更新 Canvas 后，如果它代表新的综合判断，也要更新相关 wiki 页面和 `wiki/log.md`。

使用规则：

- `.canvas` 必须是合法 JSON。
- 顶层包含 `nodes` 和 `edges` 数组。
- 每个 node 和 edge 都要有唯一 `id`。
- 每条 edge 的 `fromNode` 和 `toNode` 都必须指向现有 node。
- 文本节点中的换行用 JSON 字符串里的 `\n`。

推荐模板：

- `templates/concept-map.canvas`：raw 来源、source note、concept、entity、synthesis 之间的最小知识流地图。

## obsidian-cli

用于通过 `obsidian` CLI 操作正在运行的 Obsidian。

在 LLM Wiki 中使用时，`obsidian` CLI 是可选加速器：

- 有 CLI 时，可以用它读取当前打开文件、搜索 vault、追加 daily note、查看 backlinks、管理 properties。
- 没有 CLI 时，用普通文件系统操作完成同一件事。
- 不要因为 CLI 不存在就停止任务。
- 通过 CLI 修改文件后，仍要按 LLM Wiki 规则更新 `wiki/index.md`、`wiki/log.md` 和审计脚本。

常见映射：

- 读取笔记：`obsidian read` -> 普通 `cat` / 文件读取。
- 搜索 vault：`obsidian search` -> `rg`。
- 设置属性：`obsidian property:set` -> 编辑 YAML frontmatter。
- 查看 backlinks：`obsidian backlinks` -> `rg "\\[\\[page-slug"`。

## defuddle

用于把网页清洗成较干净的 Markdown。

在 LLM Wiki 中使用时：

- 适合网页、博客、在线文档、普通文章。
- 不适合已经是 `.md` 的 URL；这种页面直接读取 Markdown。
- 输出应先保存到 `raw/articles/` 或 `raw/clippings/`，再创建 `wiki/sources/` 来源摘要。
- 不能只把 defuddle 输出当成最终 wiki 页面；仍要做来源摘要、概念抽取、链接和置信度处理。

回退策略：

- 有 `defuddle`：用它清洗网页并保存 Markdown。
- 没有 `defuddle`：用浏览器、Jina Reader、Playwright、curl 或当前 agent 可用的网页读取能力。
- 反爬或登录页面：说明限制，尽量使用用户已登录浏览器或用户提供的本地导出文件。

## 使用判断

| 用户请求 | 适配层动作 |
|---|---|
| 写 Obsidian 笔记、frontmatter、wikilink、callout | 参考 obsidian-markdown |
| 做来源队列、健康仪表盘、表格视图 | 参考 obsidian-bases，输出 `.base` 到 `wiki/outputs/` |
| 做知识图、概念地图、Canvas | 参考 json-canvas，输出 `.canvas` 到 `wiki/synthesis/` 或 `wiki/outputs/` |
| 直接操作打开的 Obsidian vault | 如果有 `obsidian` CLI，按 obsidian-cli；否则普通文件操作 |
| 抓网页进知识库 | 如果有 `defuddle`，用于清洗；否则用普通网页读取能力 |

## 不要做的事

- 不要把 `.base`、`.canvas`、CLI 状态当成知识源。
- 不要让 Obsidian 插件能力覆盖 LLM Wiki 的证据链。
- 不要在 `raw/` 里保存整理后的观点。
- 不要让某个 agent 因为缺少 Obsidian CLI、Bases 或 Defuddle 就无法工作。
