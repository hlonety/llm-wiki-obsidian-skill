#!/usr/bin/env python3
"""Initialize a strict Karpathy-style LLM Wiki knowledge-base layout."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any


RAW_DIRS = ["articles", "clippings", "images", "pdfs", "notes", "personal"]
WIKI_DIRS = ["sources", "concepts", "entities", "synthesis", "outputs", "templates", ".state"]


def init_knowledge_base(target_path: str | Path, overwrite: bool = False) -> dict[str, Any]:
    target = Path(target_path).expanduser().resolve()
    created_dirs: list[str] = []
    created_files: list[str] = []

    for rel in ["raw", *[f"raw/{name}" for name in RAW_DIRS], "wiki", *[f"wiki/{name}" for name in WIKI_DIRS], "scripts"]:
        path = target / rel
        path.mkdir(parents=True, exist_ok=True)
        created_dirs.append(rel)

    for rel, content in seed_files().items():
        path = target / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if overwrite or not path.exists():
            path.write_text(content, encoding="utf-8")
        created_files.append(rel)

    for rel, payload in state_files().items():
        path = target / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if overwrite or not path.exists():
            path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
        created_files.append(rel)

    return {"root": str(target), "dirs": created_dirs, "files": created_files}


def seed_files() -> dict[str, str]:
    today = date.today().isoformat()
    return {
        "wiki/index.md": f"""# LLM Wiki 索引

> Agent 读取 `CLAUDE.md` 后，应优先读取这个文件。
> 最后更新：{today}

## Sources 来源摘要

## Concepts 概念

## Entities 实体

## Synthesis 综合分析

## Outputs 输出
""",
        "wiki/log.md": f"""# Evolution Log 演化日志

## {today}

- initialized：创建严格 `raw/` + `wiki/` LLM Wiki 结构。
""",
        "wiki/overview.md": f"""# Knowledge Base Health Dashboard 知识库健康仪表盘

- 最近审计：{today}
- 待处理来源：0
- 可能过期来源：0
- 有争议页面：0
- 薄弱页面：0
""",
        "wiki/QUESTIONS.md": """# Questions 问题队列

## Open 未解决

- [ ] 这个知识库首先应该帮助回答什么问题？

## Resolved 已解决
""",
        "scripts/lint.py": """#!/usr/bin/env python3
\"\"\"这个知识库的本地健康检查入口。

更完整的审计建议运行已安装 llm-wiki skill 仓库里的脚本：
python3 /path/to/llm-wiki-obsidian-skill/scripts/lint_wiki.py /path/to/knowledge-base
\"\"\"

from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    raw = root / "raw"
    wiki = root / "wiki"
    missing = [str(path.relative_to(root)) for path in [raw, wiki, wiki / "index.md", root / "CLAUDE.md"] if not path.exists()]
    if missing:
        print("缺少必要路径：")
        for item in missing:
            print(f"- {item}")
        return 1
    print("基础结构检查通过。完整 lint、哈希和状态检查请使用 llm-wiki skill 脚本。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
""",
        "BOOTSTRAP_PROMPT.md": """# Bootstrap Prompt 初始化提示词

请使用 llm-wiki-obsidian skill 初始化和维护这个知识库。

开始前先读取 `CLAUDE.md`，再读取 `wiki/index.md`、`wiki/log.md`、`wiki/overview.md` 和 `wiki/QUESTIONS.md`。
所有原始资料保存在 `raw/`，不要改写证据。整理后的知识写入 `wiki/`。
""",
        "UPGRADE_PROMPT.md": """# Upgrade Prompt 升级提示词

请使用 llm-wiki-obsidian skill 按当前方法审计并升级这个知识库。

请检查 raw 文件哈希、来源生命周期字段、源依赖图、重复概念、断链、开放问题、过期页面和缺失索引项。
如果预计要修改超过 10 个文件，先提出迁移计划，再开始执行。
""",
        "CLAUDE.md": """# LLM Behavior Contract 行为准则

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
""",
        "AGENTS.md": agent_redirect("Codex / OpenAI 风格 agent"),
        "GEMINI.md": agent_redirect("Gemini CLI"),
        "HERMES.md": agent_redirect("Hermes"),
        "OPENCLAW.md": agent_redirect("OpenClaw"),
        "README.md": """# Knowledge Base 知识库

这是一个严格 raw/wiki 架构的 LLM Wiki 知识库。

- `raw/` 保存原始来源。
- `wiki/` 保存来源摘要、概念、实体、综合分析、输出、模板、日志和问题。
- `scripts/lint.py` 是本地基础健康检查入口。

完整的整理、审计、哈希扫描和源依赖图工作流，请使用 llm-wiki-obsidian skill。
""",
    }


def agent_redirect(agent_name: str) -> str:
    return f"""# {agent_name} 入口规则

请先读取并遵守 `CLAUDE.md`。这里的 `CLAUDE.md` 是本知识库的通用行为准则，不是 Claude 专用文件。

如果当前环境已安装 llm-wiki-obsidian skill，请使用 `$llm-wiki-obsidian`。

本知识库采用严格 `raw/` + `wiki/` 架构：

- 原始资料放在 `raw/`，不要改写证据。
- 整理后的知识放在 `wiki/`。
- 开始操作前读取 `wiki/index.md`、`wiki/log.md`、`wiki/overview.md` 和 `wiki/QUESTIONS.md`。
"""


def state_files() -> dict[str, Any]:
    return {
        "wiki/.state/source-manifest.json": {
            "version": 1,
            "generated_at": None,
            "roots": ["raw"],
            "files": {},
        },
        "wiki/.state/source-dependencies.json": {
            "version": 1,
            "generated_at": None,
            "dependencies": {},
            "pages": {},
        },
    }


def format_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# 知识库已初始化",
        "",
        f"根目录：`{report['root']}`",
        "",
        "## 目录",
        "",
    ]
    lines.extend(f"- `{item}`" for item in report["dirs"])
    lines.extend(["", "## 文件", ""])
    lines.extend(f"- `{item}`" for item in report["files"])
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Initialize a strict raw/wiki LLM Wiki knowledge base.")
    parser.add_argument("target", help="Directory to initialize, for example ./knowledge-base")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing seed files")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown")
    args = parser.parse_args(argv)

    report = init_knowledge_base(args.target, overwrite=args.overwrite)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))
    else:
        print(format_markdown(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
