# 教程覆盖度

用这份文件检查本 skill 是否至少覆盖 raw/wiki LLM Wiki 教程里的能力，并在此基础上增加更强的维护功能。

## 严格目录对齐

默认生成的知识库采用教程结构：

```text
knowledge-base/
  raw/
    articles/
    clippings/
    images/
    pdfs/
    notes/
    personal/
  wiki/
    index.md
    log.md
    overview.md
    QUESTIONS.md
    sources/
    concepts/
    entities/
    synthesis/
    outputs/
    templates/
  scripts/
    lint.py
  BOOTSTRAP_PROMPT.md
  UPGRADE_PROMPT.md
  CLAUDE.md
  AGENTS.md
  GEMINI.md
  HERMES.md
  OPENCLAW.md
  README.md
```

本 skill 额外在 `wiki/.state/` 下生成隐藏状态文件：

- `source-manifest.json`
- `source-dependencies.json`

这些文件用于 SHA-256 哈希扫描和影响分析，不改变教程截图里的可见目录结构。

## 功能对齐

- 原始资料固定放在 `raw/`，原则上只增不改。
- 单个来源的摘要放在 `wiki/sources/`。
- 稳定概念放在 `wiki/concepts/`。
- 人物、公司、工具、模型、论文、数据集等实体放在 `wiki/entities/`。
- 跨来源分析放在 `wiki/synthesis/`。
- 可复用答案、报告、幻灯片、图表和审计结果放在 `wiki/outputs/`。
- `wiki/index.md` 是 agent 进入 wiki 层后首先读取的文件。
- `wiki/log.md` 是只追加的演化日志。
- `wiki/overview.md` 是知识库健康仪表盘。
- `wiki/QUESTIONS.md` 是开放问题队列。
- `CLAUDE.md` 是行为契约，但内容必须可被非 Claude agent 使用。
- `AGENTS.md`、`GEMINI.md`、`HERMES.md`、`OPENCLAW.md` 是转发入口，负责把不同 agent 指回 `CLAUDE.md`。
- `BOOTSTRAP_PROMPT.md` 和 `UPGRADE_PROMPT.md` 用于初始化和系统升级。
- `scripts/lint.py` 是本知识库自己的健康检查入口。

## 超出教程的增强

- 用 `scripts/scan_sources.py` 做 SHA-256 扫描。
- 在 `wiki/.state/source-manifest.json` 中记录原始资料清单。
- 用 `scripts/build_source_dependencies.py` 生成来源依赖图。
- 支持从 raw 文件到 source note，再到 wiki page 的影响追踪。
- 支持来源生命周期字段：`processed`、`raw_file`、`raw_sha256`、`last_verified`、`possibly_outdated`、`canonical_source`、`language`、`domain`。
- 支持 Web Clipper 队列：原始剪藏在 `raw/clippings/`，来源摘要在 `wiki/sources/`，吸收前保持 `processed: false`。
- 检测重复来源 URL。
- 检测近似重复 slug。
- 检测非 kebab-case wikilink。
- 检测指向 `[[log]]`、`[[index]]` 等维护页的普通链接。
- 高置信度升级必须有人类显式确认。
- 个人写作不计入外部证据 `source_count`。
- 通过 `domain_volatility` 和 `last_reviewed` 做过期检查。
- 演化日志使用稳定动词：`reinforced`、`corrected`、`contradicted`、`re-ingested`、`personal-position`。
- Obsidian 适配层：Markdown properties、wikilinks、callouts、embeds、Bases、JSON Canvas、Obsidian CLI、Defuddle 都作为可选增强，详见 `references/obsidian-adapters.md`。
- 可选 Obsidian 模板：`templates/source-queue.base`、`templates/wiki-health.base`、`templates/concept-map.canvas`。
