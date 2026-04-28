# Obsidian 约定

当用户希望建立面向 Obsidian 的 LLM Wiki，并且要求严格采用教程里的 raw/wiki 结构时，遵守这份约定。

## 目录结构

```text
knowledge-base/
  raw/              不改写的原始资料
  raw/articles/     长文、网页文章或 Markdown 文章
  raw/clippings/    Web Clipper 剪藏
  raw/images/       截图、图表、图片
  raw/pdfs/         PDF 文件
  raw/notes/        快速记录和临时捕获
  raw/personal/     用户自己写的文章、分析、投资笔记
  wiki/             LLM 可读取的整理后 wiki
  wiki/index.md     agent 进入 wiki 层后首先读取的文件
  wiki/log.md       只追加的演化日志
  wiki/overview.md  健康仪表盘
  wiki/QUESTIONS.md 开放问题队列
  wiki/sources/     每个来源一页摘要
  wiki/concepts/    稳定概念、想法、模式
  wiki/entities/    人物、公司、工具、模型、论文、数据集、benchmark
  wiki/synthesis/   跨来源分析、工作流、地图、提示词模式
  wiki/outputs/     保存答案、报告、幻灯片、图表、lint 报告
  wiki/templates/   页面模板
  wiki/.state/      自动生成的 manifest 和依赖图
  scripts/lint.py   本知识库的本地健康检查入口
  BOOTSTRAP_PROMPT.md
  UPGRADE_PROMPT.md
  CLAUDE.md         可移植的行为契约，不是 Claude 专用
  AGENTS.md         Codex/OpenAI 风格 agent 的转发入口
  GEMINI.md         Gemini CLI 的转发入口
  HERMES.md         Hermes 的转发入口
  OPENCLAW.md       OpenClaw 的转发入口
  README.md
```

## 文件名和链接

- 文件名使用小写 kebab-case，例如 `agentic-workflow.md`。
- 可读标题写在 frontmatter 的 `title` 中，例如 `title: Agentic Workflow`。
- wikilink 用文件名主体，例如 `[[agentic-workflow]]`。
- 别名写入 `aliases`，不要用多个相似文件名表达同一个概念。
- 优先使用明确链接，不要只靠 tag 组织知识。
- 普通 wiki 页面避免链接到 `[[log]]`、`[[index]]`、`[[overview]]`、`[[QUESTIONS]]` 等系统维护页。
- 新建页面前，先搜索文件名主体、标题和别名，避免重复概念页。

## 标准 Frontmatter

```yaml
---
title: Page Title
aliases: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: source | concept | entity | tool | paper | person | workflow | prompt | question | synthesis | map | output
status: seed | growing | stable | contested | archived
tags: []
sources: []
source_count: 0
confidence: medium
domain_volatility: medium
last_reviewed: YYYY-MM-DD
high_confirmed: false
---
```

可选字段：

```yaml
evidence:
  - source: "[[source-slug]]"
    claim: "Short claim supported by the source."
contested: true
contradictions: []
freshness: stable | fast-moving | stale
review_after: YYYY-MM-DD
high_confirmed_by:
high_confirmed_on:
```

## AI 知识分类

AI 知识库可以先使用下面这套 tag。新增 tag 前，先在 `CLAUDE.md` 里登记，避免同义 tag 泛滥。

- 领域：`agent`、`llm`、`rag`、`memory`、`evaluation`、`prompt`、`workflow`、`automation`
- 技术：`architecture`、`training`、`fine-tuning`、`inference`、`tool-use`、`mcp`、`data`
- 对象：`model`、`paper`、`tool`、`framework`、`benchmark`、`dataset`、`company`、`person`
- 质量：`security`、`privacy`、`reliability`、`alignment`、`cost`、`latency`
- 元信息：`comparison`、`timeline`、`controversy`、`prediction`、`learning-path`

## Dataview 示例

开放问题：

```dataview
TASK
FROM "wiki/QUESTIONS.md"
WHERE !completed
```

需要复查的页面：

```dataview
TABLE status, confidence, domain_volatility, last_reviewed
FROM "wiki/concepts" OR "wiki/entities" OR "wiki/synthesis"
WHERE status = "contested" OR confidence = "low" OR domain_volatility = "high"
SORT last_reviewed ASC
```

最近更新的页面：

```dataview
TABLE type, status, tags
FROM "wiki/concepts" OR "wiki/entities" OR "wiki/synthesis"
SORT updated DESC
LIMIT 20
```

有来源支持的工具笔记：

```dataview
TABLE sources, confidence
FROM "wiki/entities"
WHERE length(sources) > 0
SORT title ASC
```

## 来源摘要

来源摘要页不是概念页。来源摘要页记录“某一个来源说了什么”；概念页负责综合一个或多个来源，沉淀出更稳定的知识。

推荐的来源 frontmatter：

```yaml
---
title: Source Title
source_url:
domain:
author:
published:
captured: YYYY-MM-DD
type: source
source_kind: article | paper | transcript | clip | note
language:
canonical_source:
processed: false
raw_file:
raw_sha256:
sha256:
last_verified: YYYY-MM-DD
possibly_outdated: false
tags: []
---
```

来源摘要放在 `wiki/sources/`。原始捕获文件放在 `raw/`。解释、判断和综合写到链接的 wiki 页面里。

来源生命周期字段：

- `processed: false`：来源已经捕获，但还没有吸收到 wiki。
- `processed: true`：来源摘要和受影响的 wiki 页面已经更新。
- `raw_file`：原始捕获或附件的相对路径。
- `raw_sha256`：原始文件的哈希值。
- `possibly_outdated: true`：依赖该来源前需要重新检查。
- `canonical_source`：当剪藏、镜像或转载重复时，记录优先使用的原始 URL。

## Source Manifest

`wiki/.state/source-manifest.json` 由 `scripts/scan_sources.py` 生成。它记录：

- 相对路径
- SHA-256 哈希值
- 文件大小
- 修改时间

用它识别：

- `new`：之前没见过的新文件。
- `changed`：路径存在，但哈希值变化。
- `deleted`：manifest 里有记录，但文件已经不存在。
- `unchanged`：路径和哈希值都没变。

除非是在修复已知的坏扫描结果，否则不要手动编辑 manifest。

## Source Dependencies

`wiki/.state/source-dependencies.json` 由 `scripts/build_source_dependencies.py` 生成。它映射：

- 来源摘要到受影响的 wiki 页面。
- raw 文件到来源摘要。
- raw 文件到受影响的 wiki 页面。

当某个来源的哈希变化后，用它判断哪些页面需要重新吸收或复查。不要因为 raw 文件缺失就自动删除 wiki 页面。

## 个人写作

用户自己写的原始材料放在 `raw/personal/`，对应的来源摘要放在 `wiki/sources/`。

个人写作页可以包含：

- 用户自己的论点。
- 用户对某个概念的立场。
- 引用的外部证据。
- 局限性。
- 是否已被后续内容替代。

吸收个人写作时：

- 把用户观点写入相关概念页的 `## My Position`。
- 不增加外部证据 `source_count`。
- 不因为个人写作而提升置信度。
- 如果个人写作引用了外部来源，把那些外部来源单独链接出来。

## 图谱卫生

真正有用的图谱主要是整理后的 wiki 层。来源、元信息和输出文件的链接要有意控制：

- 来源摘要可以链接到受影响的 wiki 页面。
- wiki 页面应该通过 frontmatter 或 `Sources` 小节引用来源。
- 普通概念页避免链接到日志、索引、lint 报告或自动生成的 JSON 等维护文件。
- 如果 Obsidian 图谱太嘈杂，可以给生成类输出页加 `graph-excluded: true`。
