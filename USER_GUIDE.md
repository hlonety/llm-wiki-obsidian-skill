# LLM Wiki 使用说明

这份说明写给不太懂代码、主要想用 Obsidian 管理 AI 知识库的人。

## 这套东西解决什么问题

普通剪藏很容易变成资料仓库：文章很多，但下次提问时还是要重新翻。LLM Wiki 的做法是把知识库分成两层：

- `raw/`：原始资料层。文章、网页剪藏、PDF、截图、自己的长文都放这里，尽量不改。
- `wiki/`：理解和整理层。AI 读完原始资料后，把它整理成来源摘要、概念页、实体页、综合分析、问题答案。

你日常只需要记住一句话：

```text
raw 放证据，wiki 放理解。
```

## 完整目录长什么样

默认目录严格按照教程里的结构：

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

每个位置的作用：

- `raw/articles/`：长文章、Markdown 网页正文。
- `raw/clippings/`：Obsidian Web Clipper 或浏览器剪藏。
- `raw/images/`：截图、图表、图片。
- `raw/pdfs/`：PDF。
- `raw/notes/`：零散记录。
- `raw/personal/`：你自己写的文章、分析、投资笔记、观点。
- `wiki/sources/`：每个来源的摘要页。
- `wiki/concepts/`：概念页，比如 RAG、Agent Memory、Prompt Engineering。
- `wiki/entities/`：实体页，比如工具、模型、论文、人物、公司、数据集。
- `wiki/synthesis/`：跨来源综合分析、工作流、学习地图。
- `wiki/outputs/`：AI 给你生成的可保存答案、报告、表格、幻灯片大纲。
- `wiki/index.md`：知识库目录，AI 和人都优先看它。
- `wiki/log.md`：操作日志，记录知识库怎么演化。
- `wiki/overview.md`：健康仪表盘。
- `wiki/QUESTIONS.md`：长期问题清单。
- `CLAUDE.md`：行为准则。虽然叫 CLAUDE，但 Codex、Hermes、OpenCode 等也可以读。

## 第一次怎么建库

如果你在 Codex 里已经安装了这个 skill，可以直接说：

```text
使用 $llm-wiki-obsidian 在 /你的路径/knowledge-base 创建一个严格 raw/wiki 架构的 AI 知识库。
```

如果你会运行命令，也可以在这个 skill 仓库里执行：

```bash
python3 scripts/init_knowledge_base.py /你的路径/knowledge-base
```

然后在 Obsidian 里把 `/你的路径/knowledge-base` 当作 vault 打开。

## 在 Obsidian 里怎么日常使用

### 1. 先收集资料

看到有价值的文章、网页、PDF、截图，不要急着整理概念页。先放进 `raw/`：

- 网页文章：`raw/articles/`
- Web Clipper 剪藏：`raw/clippings/`
- PDF：`raw/pdfs/`
- 截图：`raw/images/`
- 临时笔记：`raw/notes/`
- 自己写的观点：`raw/personal/`

### 2. 让 AI 处理新资料

在 Codex、Claude Code、Claudian 插件或其他 agent 里说：

```text
使用 $llm-wiki-obsidian 扫描这个知识库的新 raw 文件，计算哈希值，然后把未处理资料整理进 wiki。
```

AI 应该做几件事：

- 识别 `raw/` 里新增或变化的文件。
- 在 `wiki/sources/` 生成来源摘要。
- 更新相关的 `wiki/concepts/`、`wiki/entities/` 或 `wiki/synthesis/`。
- 更新 `wiki/index.md`。
- 在 `wiki/log.md` 写一条记录。

### 3. 再向知识库提问

示例：

```text
基于我的 LLM Wiki，解释 RAG memory 和 compiled wiki memory 的区别，并引用相关 wiki 页面。
```

或者：

```text
基于这个知识库，整理一份“AI Agent 入门路线图”，如果值得长期保存，就放到 wiki/outputs/。
```

## Claudian 插件里怎么叫 Codex 使用

你可以用这种提示词：

```text
使用 $llm-wiki-obsidian 管理当前 Obsidian vault。
先读取 CLAUDE.md、wiki/index.md、wiki/log.md、wiki/overview.md、wiki/QUESTIONS.md。
然后扫描 raw/ 里的新文件，把需要处理的内容整理进 wiki/。
```

如果只想处理某个文件：

```text
使用 $llm-wiki-obsidian 处理 raw/clippings/xxx.md。
请保留原文不改，在 wiki/sources/ 建来源摘要，并更新相关概念页。
```

如果想问问题并保存答案：

```text
使用 $llm-wiki-obsidian 回答这个问题：……
如果答案以后还会用到，请保存到 wiki/outputs/，并更新 wiki/index.md 和 wiki/log.md。
```

## 几个常用提示词

初始化：

```text
使用 $llm-wiki-obsidian 在当前目录创建严格 raw/wiki 架构的 AI 知识库。
```

扫描新资料：

```text
使用 $llm-wiki-obsidian 扫描 raw/，告诉我哪些文件是 new、changed、deleted，并更新 source-manifest。
```

批量整理：

```text
使用 $llm-wiki-obsidian 处理所有 processed: false 的来源，把它们整理进 wiki。
```

审计健康状态：

```text
使用 $llm-wiki-obsidian 审计这个知识库，检查断链、重复概念、未处理来源、过期页面、缺少索引的页面。
```

记录长期问题：

```text
使用 $llm-wiki-obsidian 把这个问题加入 wiki/QUESTIONS.md：……
```

反思和综合：

```text
使用 $llm-wiki-obsidian 基于现有 wiki 做一次反思，找出重复主题、矛盾、薄弱概念和下一步值得研究的问题。
```

## 哈希值是做什么的

哈希值可以理解成文件指纹。

当 `raw/` 里的文件变了，`scripts/scan_sources.py` 会发现它的 SHA-256 变了，然后标记为 `changed`。这样 AI 就知道：

- 这个来源可能需要重新阅读。
- 相关的 wiki 页面可能过期。
- 需要根据 `wiki/.state/source-dependencies.json` 找到受影响页面。

你不需要手动计算哈希。通常直接让 agent 扫描即可。

## processed 是什么

`processed` 表示来源有没有被整理进 wiki：

- `processed: false`：已经收集，但还没整理。
- `processed: true`：已经读过，并且相关 wiki 页面已经更新。

Web Clipper 剪藏进来的内容，默认应该先是 `processed: false`。等 AI 整理完，再改成 `true`。

## 个人写作怎么处理

你自己的文章、分析、投资笔记放在 `raw/personal/`。

AI 可以把你的观点整理到相关概念页的 `## My Position` 部分，但要注意：

- 个人观点不算外部证据。
- 不能因为你自己写了很多，就把某个概念的 `confidence` 提高。
- 如果你的文章引用了外部来源，外部来源要单独记录。

## 什么不要做

- 不要直接改 `raw/` 里的原始资料来“整理内容”。
- 不要把所有剪藏都堆进概念页。
- 不要让 AI 在没读 `CLAUDE.md` 和 `wiki/index.md` 的情况下乱改。
- 不要自动把 `confidence` 改成 `high`。
- 不要把个人观点当成外部证据。
- 不要为了一个路过的名词就新建页面。

## 日常维护节奏

可以按这个节奏：

- 每天：把有价值资料放进 `raw/`。
- 每周：让 AI 处理 `processed: false` 的来源。
- 每两周：做一次 lint/audit，修断链、重复页面和未处理来源。
- 每月：让 AI 做一次反思，找出知识缺口和下一批研究问题。

## 出问题时怎么看

让 agent 执行：

```text
使用 $llm-wiki-obsidian 审计这个知识库，并用通俗语言解释每个问题该怎么修。
```

常见问题：

- `broken-wikilink`：某个 `[[链接]]` 指向不存在的页面。
- `missing-index-entry`：页面存在，但没加入 `wiki/index.md`。
- `unprocessed-source`：来源还没整理。
- `possibly-outdated-source`：来源可能过期或变动过。
- `duplicate-source-url`：同一个 URL 被收集了多次。
- `near-duplicate-slug`：可能有重复概念页。
- `unconfirmed-high-confidence`：`confidence: high` 没有人类确认。

## qmd 是必须的吗

不是。

有些教程会用 `qmd query`、`qmd multi-get`、`qmd add` 这类命令来快速操作 Markdown 知识库。但这套 skill 不依赖 qmd。没有 qmd 时，Codex、Claude Code、Hermes、OpenCode 等 agent 可以用自己的文件读取、搜索、编辑能力完成同样的事。

## 一句话工作流

```text
先把资料放进 raw/，再让 AI 编译进 wiki/，最后用 wiki/ 回答和更新问题。
```
