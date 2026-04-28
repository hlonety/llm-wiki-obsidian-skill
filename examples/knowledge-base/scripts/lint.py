#!/usr/bin/env python3
"""这个知识库的本地健康检查入口。

更完整的审计建议运行已安装 llm-wiki skill 仓库里的脚本：
python3 /path/to/llm-wiki-obsidian-skill/scripts/lint_wiki.py /path/to/knowledge-base
"""

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
