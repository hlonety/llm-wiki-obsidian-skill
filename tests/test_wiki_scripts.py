import importlib.util
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class WikiScriptTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.wiki = Path(self.tmp.name)
        (self.wiki / "concepts").mkdir()
        (self.wiki / "tools").mkdir()
        (self.wiki / "raw" / "articles").mkdir(parents=True)
        (self.wiki / "SCHEMA.md").write_text(
            textwrap.dedent(
                """
                # Wiki Schema

                ## Domain
                AI knowledge base.

                ## Tag Taxonomy
                - Areas: agent, prompt, evaluation, model, tool, workflow
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )
        (self.wiki / "index.md").write_text(
            "# AI Knowledge Index\n\n## Concepts\n- [[agentic-workflow]] - Existing page.\n",
            encoding="utf-8",
        )
        (self.wiki / "log.md").write_text("# Wiki Log\n", encoding="utf-8")
        (self.wiki / "concepts" / "agentic-workflow.md").write_text(
            textwrap.dedent(
                """
                ---
                title: Agentic Workflow
                created: 2026-04-28
                updated: 2026-04-28
                type: concept
                tags: [agent, workflow]
                sources: [raw/articles/karpathy-llm-wiki.md]
                ---

                An agentic workflow connects [[prompt-architecture]] with [[codex]] and [[missing-tool]].
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )
        (self.wiki / "concepts" / "prompt-architecture.md").write_text(
            textwrap.dedent(
                """
                ---
                title: Prompt Architecture
                created: 2026-04-28
                updated: 2026-04-28
                type: concept
                tags: [prompt]
                sources: [raw/articles/karpathy-llm-wiki.md]
                ---

                Prompt architecture shapes [[agentic-workflow]] behavior.
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )
        (self.wiki / "tools" / "codex.md").write_text(
            textwrap.dedent(
                """
                ---
                title: Codex
                created: 2026-04-28
                updated: 2026-04-28
                type: tool
                tags: [tool, agent]
                sources: []
                ---

                Codex is an agent tool connected to [[agentic-workflow]].
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.tmp.cleanup()

    def test_lint_reports_broken_link_and_missing_index_entry(self):
        lint_wiki = load_module("lint_wiki", ROOT / "scripts" / "lint_wiki.py")

        report = lint_wiki.lint_wiki(self.wiki)

        broken = [issue for issue in report["issues"] if issue["code"] == "broken-wikilink"]
        missing = [issue for issue in report["issues"] if issue["code"] == "missing-index-entry"]
        self.assertEqual(broken[0]["target"], "missing-tool")
        self.assertEqual({issue["page"] for issue in missing}, {"prompt-architecture", "codex"})
        self.assertEqual(report["summary"]["pages"], 3)

    def test_lint_reports_v02_knowledge_quality_issues(self):
        lint_wiki = load_module("lint_wiki", ROOT / "scripts" / "lint_wiki.py")
        (self.wiki / "concepts" / "old-model.md").write_text(
            textwrap.dedent(
                """
                ---
                title: Old Model
                aliases: []
                created: 2020-01-01
                updated: 2020-01-01
                type: concept
                tags: [model]
                sources: [raw/articles/a.md, raw/articles/b.md, raw/articles/c.md, raw/articles/d.md, raw/articles/e.md]
                source_count: 5
                confidence: medium
                domain_volatility: high
                ---

                Old model pages should be reviewed because fast-moving topics age quickly.
                They also become high-confidence candidates only after a human confirms the definition and sources.
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )
        (self.wiki / "concepts" / "tiny-page.md").write_text(
            textwrap.dedent(
                """
                ---
                title: Tiny Page
                aliases: []
                created: 2026-04-28
                updated: 2026-04-28
                type: concept
                tags: [agent]
                sources: []
                ---

                Too short.
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )
        (self.wiki / "concepts" / "retrieval-augmented-generation.md").write_text(
            textwrap.dedent(
                """
                ---
                title: Retrieval Augmented Generation
                aliases: [RAG, 检索增强生成]
                created: 2026-04-28
                updated: 2026-04-28
                type: concept
                tags: [agent]
                sources: []
                ---

                Retrieval augmented generation is related to [[agentic-workflow]].
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )
        (self.wiki / "concepts" / "rag.md").write_text(
            textwrap.dedent(
                """
                ---
                title: RAG
                aliases: [RAG]
                created: 2026-04-28
                updated: 2026-04-28
                type: concept
                tags: [agent]
                sources: []
                ---

                A duplicate short name for retrieval augmented generation.
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )
        (self.wiki / "concepts" / "personal-position.md").write_text(
            textwrap.dedent(
                """
                ---
                title: Personal Position
                aliases: []
                created: 2026-04-28
                updated: 2026-04-28
                type: concept
                tags: [agent]
                sources: [raw/articles/public-source.md, raw/personal/my-note.md]
                source_count: 2
                confidence: medium
                ---

                This page mixes public evidence with a personal writing note.
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )

        report = lint_wiki.lint_wiki(self.wiki)
        codes = {issue["code"] for issue in report["issues"]}

        self.assertIn("stale-page", codes)
        self.assertIn("stub-page", codes)
        self.assertIn("alias-overlap", codes)
        self.assertIn("candidate-high-needs-review", codes)
        self.assertIn("personal-source-counted", codes)

    def test_rebuild_index_groups_pages_by_type(self):
        rebuild_index = load_module("rebuild_index", ROOT / "scripts" / "rebuild_index.py")

        index = rebuild_index.build_index(self.wiki, title="AI Knowledge Index")

        self.assertIn("## Concepts", index)
        self.assertIn("- [[agentic-workflow]] - An agentic workflow connects", index)
        self.assertIn("- [[prompt-architecture]] - Prompt architecture shapes", index)
        self.assertIn("## Tools", index)
        self.assertIn("- [[codex]] - Codex is an agent tool", index)
        self.assertIn("Total pages: 3", index)


if __name__ == "__main__":
    unittest.main()
