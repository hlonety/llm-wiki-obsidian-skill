# LLM Behavior Contract 行为准则

这个文件是给所有能读写文件的 agent 使用的行为准则。文件名沿用原始 LLM Wiki 教程里的 `CLAUDE.md`，但规则不是 Claude 专用；Codex、Hermes、OpenCode、OpenClaw 等也应该读取。

## Directory Contract 目录约定

- `raw/`：不可变的原始来源。新资料放这里，不要改写证据。
- `raw/articles/`：长文章、网页正文、Markdown 文章。
- `raw/clippings/`：Web Clipper 或浏览器剪藏。
- `raw/images/`：截图、图表、图片。
- `raw/pdfs/`：PDF 文件。
- `raw/notes/`：临时记录和零散捕获。
- `raw/personal/`：用户自己写的文章、分析、投资笔记。
- `wiki/index.md`：优先读取的 wiki 索引。
- `wiki/log.md`：只追加的演化日志。
- `wiki/overview.md`：知识库健康仪表盘。
- `wiki/QUESTIONS.md`：开放问题队列。
- `wiki/sources/`：每个来源一页摘要。
- `wiki/concepts/`：长期概念、思想、模式。
- `wiki/entities/`：人物、公司、工具、模型、论文、数据集、基准。
- `wiki/synthesis/`：跨来源分析、地图、工作流。
- `wiki/outputs/`：保存的答案、报告、幻灯片大纲、图表、lint 报告。
- `wiki/templates/`：页面模板。

## Operating Rules 操作规则

- 编辑前先读本文件、`wiki/index.md`、最近的 `wiki/log.md` 和 `wiki/QUESTIONS.md`。
- 保留 raw 原始来源。修正、解释和综合写入 wiki 页面。
- 来源笔记要跟踪 `processed`、`raw_file`、`raw_sha256`、`last_verified` 和 `possibly_outdated`。
- 把 `processed: false`、哈希变化、`possibly_outdated: true` 当作待处理队列。
- 文件名使用 lowercase kebab-case。中文名和别名写进 `title` 和 `aliases`。
- 新建页面前先搜索文件名、标题和别名。
- 事实性主张应能追溯到来源笔记或 raw 文件。
- 个人写作可以更新 `## My Position`，但不能当作外部证据。
- `confidence: high` 必须经过人类明确确认。
- 重要变化要记录为 reinforced、corrected、contradicted、re-ingested 或 personal-position。

## Tag Taxonomy 标签分类

- 领域：`agent`, `llm`, `rag`, `memory`, `evaluation`, `prompt`, `workflow`, `automation`
- 技术：`architecture`, `training`, `fine-tuning`, `inference`, `tool-use`, `mcp`, `data`
- 对象：`model`, `paper`, `tool`, `framework`, `benchmark`, `dataset`, `company`, `person`
- 质量：`security`, `privacy`, `reliability`, `alignment`, `cost`, `latency`
- 元信息：`comparison`, `timeline`, `controversy`, `prediction`, `learning-path`
