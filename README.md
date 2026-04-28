# LLM Wiki Obsidian Skill

这是一个给 AI Agent 使用的 LLM Wiki 技能，用来维护严格 `raw/` + `wiki/` 架构的 Obsidian/Markdown 知识库。方法论来自 Andrej Karpathy 的 LLM Wiki 思路，并补充了哈希扫描、源依赖图、健康审计、置信度规则和个人写作规则。

如果你不太懂代码，先看中文教程：[USER_GUIDE.md](USER_GUIDE.md)。

## 适合什么场景

这个 skill 适合管理 AI 知识库，例如：

- LLM、Agent、RAG、Memory、MCP。
- Prompt、工作流、自动化。
- 模型、工具、论文、人物、公司、数据集。
- 学习笔记、网页剪藏、PDF、自己的分析文章。

## 它做什么

它让 agent 按下面的方式维护知识库：

- 把原始资料保存在 `raw/`，尽量不改。
- 把来源摘要、概念、实体、综合分析、长期答案保存在 `wiki/`。
- 用 Obsidian wikilink 和 YAML frontmatter 保持结构清晰。
- 跟踪来源、置信度、过期风险、矛盾观点和开放问题。
- 计算 raw 文件 SHA-256 哈希值，识别新增、变更、删除文件。
- 生成源依赖图，知道某个 raw 文件变化后会影响哪些 wiki 页面。
- 审计断链、重复 URL、近重复概念、未处理来源、索引缺失和高置信度误用。

## 安装

### Codex

在 Codex 里说：

```text
Install the skill from https://github.com/hlonety/llm-wiki-obsidian-skill
```

或者手动安装：

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/hlonety/llm-wiki-obsidian-skill ~/.codex/skills/llm-wiki-obsidian
```

安装后重启 Codex，新的 skill 才会自动进入技能列表。

### 其他 Agent

这个 skill 不绑定 Codex，也不强依赖 Claude Code 或 qmd。Claude Code、OpenCode、OpenClaw、Hermes、Gemini 风格 agent 或其他能读写文件的 agent，都可以读取本仓库的 `SKILL.md` 后执行。

常见用法：

- Claude Code：把仓库放进你的 skills/rules 位置，或在项目 `CLAUDE.md` 里引用本仓库的 `SKILL.md`。
- OpenCode / OpenClaw：把本仓库作为 rules/skills 文件夹，并要求 agent 先读 `SKILL.md`。
- Hermes：导入为 skill，或把 `SKILL.md` 内容包装成 Hermes skill。
- 其他 agent：把仓库 URL 发给 agent，让它先读 `SKILL.md` 再操作知识库。

## 快速开始

让 agent 创建一个知识库：

```text
使用 $llm-wiki-obsidian 在 ~/wiki/knowledge-base 创建一个严格 raw/wiki 架构的 AI 知识库。
```

或者直接运行脚本：

```bash
python3 scripts/init_knowledge_base.py ~/wiki/knowledge-base
```

把文章整理进知识库：

```text
使用 $llm-wiki-obsidian 把这篇文章加入我的 AI 知识库，并更新相关概念页：https://example.com/article
```

基于知识库提问：

```text
基于我的 LLM Wiki，解释 RAG memory 和 compiled wiki memory 的区别。
```

扫描 raw 文件：

```bash
python3 scripts/scan_sources.py ~/wiki/knowledge-base
python3 scripts/scan_sources.py ~/wiki/knowledge-base --write
```

生成源依赖图：

```bash
python3 scripts/build_source_dependencies.py ~/wiki/knowledge-base --write
```

审计知识库：

```bash
python3 scripts/lint_wiki.py ~/wiki/knowledge-base
```

重建索引：

```bash
python3 scripts/rebuild_index.py ~/wiki/knowledge-base --write
```

## 默认目录

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
    .state/
      source-manifest.json
      source-dependencies.json
  scripts/
    lint.py
  BOOTSTRAP_PROMPT.md
  UPGRADE_PROMPT.md
  CLAUDE.md
  README.md
```

`CLAUDE.md` 是教程兼容的行为准则文件，但不是 Claude 专用。Codex、Hermes、OpenCode 等 agent 也应该把它当作普通 Markdown 规则读取。

## 关键规则

- `confidence: high` 不能自动设置，必须经过人类明确确认。
- 个人写作可以记录你的立场，但不能计入外部 `source_count`。
- 快速变化的主题要用 `domain_volatility` 和 `last_reviewed` 跟踪过期风险。
- 长期答案、反思报告、对比表格、幻灯片大纲放在 `wiki/outputs/`。
- Web Clipper 或浏览器保存的内容先进入 `processed: false` 队列，之后批量整理。
- 文件名优先使用英文 lowercase kebab-case；中文名和别名放进 `title` 和 `aliases`。
- qmd 只是可选工具，不是必需依赖。

## 来源

灵感来自 Andrej Karpathy 的 LLM Wiki 原始方法：

https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

## 许可证

MIT
