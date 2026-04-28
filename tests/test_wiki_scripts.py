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

    def test_init_knowledge_base_creates_strict_tutorial_layout(self):
        init_knowledge_base = load_module("init_knowledge_base", ROOT / "scripts" / "init_knowledge_base.py")
        target = self.wiki / "knowledge-base"

        created = init_knowledge_base.init_knowledge_base(target)

        expected_dirs = {
            "raw",
            "raw/articles",
            "raw/clippings",
            "raw/images",
            "raw/pdfs",
            "raw/notes",
            "raw/personal",
            "wiki",
            "wiki/sources",
            "wiki/concepts",
            "wiki/entities",
            "wiki/synthesis",
            "wiki/outputs",
            "wiki/templates",
            "scripts",
        }
        expected_files = {
            "wiki/index.md",
            "wiki/log.md",
            "wiki/overview.md",
            "wiki/QUESTIONS.md",
            "scripts/lint.py",
            "BOOTSTRAP_PROMPT.md",
            "UPGRADE_PROMPT.md",
            "CLAUDE.md",
            "AGENTS.md",
            "GEMINI.md",
            "HERMES.md",
            "OPENCLAW.md",
            "README.md",
        }

        self.assertTrue(expected_dirs.issubset(set(created["dirs"])))
        self.assertTrue(expected_files.issubset(set(created["files"])))
        for rel in expected_dirs:
            self.assertTrue((target / rel).is_dir(), rel)
        for rel in expected_files:
            self.assertTrue((target / rel).is_file(), rel)
        self.assertIn("raw/", (target / "CLAUDE.md").read_text(encoding="utf-8"))
        self.assertIn("wiki/", (target / "CLAUDE.md").read_text(encoding="utf-8"))
        for rel in ["AGENTS.md", "GEMINI.md", "HERMES.md", "OPENCLAW.md"]:
            text = (target / rel).read_text(encoding="utf-8")
            self.assertIn("CLAUDE.md", text)
            self.assertIn("$llm-wiki-obsidian", text)

        lint_wiki = load_module("lint_wiki", ROOT / "scripts" / "lint_wiki.py")
        lint_report = lint_wiki.lint_wiki(target)
        self.assertEqual(lint_report["summary"]["pages"], 0)
        self.assertNotIn("missing-frontmatter", {issue["code"] for issue in lint_report["issues"]})

    def test_strict_layout_paths_are_first_class(self):
        lint_wiki = load_module("lint_wiki", ROOT / "scripts" / "lint_wiki.py")
        scan_sources = load_module("scan_sources", ROOT / "scripts" / "scan_sources.py")
        build_source_dependencies = load_module("build_source_dependencies", ROOT / "scripts" / "build_source_dependencies.py")
        rebuild_index = load_module("rebuild_index", ROOT / "scripts" / "rebuild_index.py")
        kb = self.wiki / "knowledge-base"
        for rel in [
            "raw/articles",
            "wiki/sources",
            "wiki/concepts",
            "wiki/entities",
            "wiki/synthesis",
            "wiki/outputs",
            "wiki/templates",
        ]:
            (kb / rel).mkdir(parents=True, exist_ok=True)
        (kb / "CLAUDE.md").write_text(
            textwrap.dedent(
                """
                # LLM Behavior Contract

                ## Tag Taxonomy
                - Areas: `agent`, `llm`, `memory`, `workflow`
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )
        (kb / "wiki" / "index.md").write_text(
            "# Index\n\n## Concepts\n- [[llm-wiki]] - Compiled wiki memory.\n",
            encoding="utf-8",
        )
        (kb / "wiki" / "log.md").write_text("# Log\n", encoding="utf-8")
        (kb / "wiki" / "overview.md").write_text("# Overview\n", encoding="utf-8")
        (kb / "wiki" / "QUESTIONS.md").write_text("# Questions\n", encoding="utf-8")
        (kb / "raw" / "articles" / "karpathy.md").write_text("# Karpathy\n\nCompiled wiki memory.\n", encoding="utf-8")
        (kb / "wiki" / "sources" / "karpathy-llm-wiki.md").write_text(
            textwrap.dedent(
                """
                ---
                title: Karpathy LLM Wiki
                source_url: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
                captured: 2026-04-28
                type: source
                processed: true
                raw_file: raw/articles/karpathy.md
                raw_sha256: rawhash
                tags: []
                ---

                This source supports [[llm-wiki]].
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )
        (kb / "wiki" / "concepts" / "llm-wiki.md").write_text(
            textwrap.dedent(
                """
                ---
                title: LLM Wiki
                aliases: [compiled wiki memory]
                created: 2026-04-28
                updated: 2026-04-28
                type: concept
                status: growing
                tags: [llm, memory, workflow]
                sources: [wiki/sources/karpathy-llm-wiki.md]
                source_count: 1
                confidence: low
                domain_volatility: medium
                last_reviewed: 2026-04-28
                high_confirmed: false
                ---

                LLM Wiki keeps raw sources separate from synthesized wiki pages. The compiled wiki layer
                is updated over time, which makes future answers cheaper, more consistent, and easier to audit.
                It preserves source traceability, open questions, confidence notes, and evolution logs so agents
                can continue the work without rediscovering everything from scratch.
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )

        scan_report = scan_sources.scan_sources(kb)
        self.assertEqual(scan_report["manifest_path"], str((kb / "wiki" / ".state" / "source-manifest.json").resolve()))
        self.assertEqual(scan_report["manifest"]["roots"], ["raw"])
        self.assertEqual(scan_report["files"][0]["path"], "raw/articles/karpathy.md")

        deps_report = build_source_dependencies.build_source_dependencies(kb)
        deps = deps_report["dependencies"]
        self.assertEqual(
            build_source_dependencies.dependencies_path(kb),
            (kb / "wiki" / ".state" / "source-dependencies.json").resolve(),
        )
        self.assertIn("wiki/sources/karpathy-llm-wiki.md", deps)
        self.assertIn("raw/articles/karpathy.md", deps)
        self.assertIn("wiki/concepts/llm-wiki.md", deps["wiki/sources/karpathy-llm-wiki.md"]["wiki_pages"])
        self.assertIn("wiki/concepts/llm-wiki.md", deps["raw/articles/karpathy.md"]["wiki_pages"])

        lint_report = lint_wiki.lint_wiki(kb)
        codes = {issue["code"] for issue in lint_report["issues"]}
        self.assertNotIn("missing-schema", codes)
        self.assertEqual(lint_report["summary"]["pages"], 1)

        rebuilt_index = rebuild_index.build_index(kb, title="LLM Wiki Index")
        self.assertIn("- [[llm-wiki]]", rebuilt_index)
        self.assertNotIn("[[karpathy-llm-wiki]]", rebuilt_index)

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

    def test_scan_sources_detects_new_changed_and_deleted_files(self):
        scan_sources = load_module("scan_sources", ROOT / "scripts" / "scan_sources.py")
        source = self.wiki / "raw" / "articles" / "new-agent-note.md"
        source.write_text("# New Agent Note\n\nFirst version.\n", encoding="utf-8")

        first_report = scan_sources.scan_sources(self.wiki)
        self.assertEqual(first_report["summary"]["new"], 1)
        self.assertEqual(first_report["files"][0]["status"], "new")
        self.assertEqual(first_report["files"][0]["path"], "raw/articles/new-agent-note.md")
        self.assertEqual(len(first_report["files"][0]["sha256"]), 64)

        scan_sources.write_manifest(self.wiki, first_report["manifest"])
        source.write_text("# New Agent Note\n\nSecond version.\n", encoding="utf-8")
        changed_report = scan_sources.scan_sources(self.wiki)
        changed = [item for item in changed_report["files"] if item["path"] == "raw/articles/new-agent-note.md"][0]
        self.assertEqual(changed["status"], "changed")

        scan_sources.write_manifest(self.wiki, changed_report["manifest"])
        source.unlink()
        deleted_report = scan_sources.scan_sources(self.wiki)
        deleted = [item for item in deleted_report["files"] if item["path"] == "raw/articles/new-agent-note.md"][0]
        self.assertEqual(deleted["status"], "deleted")

    def test_lint_reports_source_lifecycle_and_link_hygiene(self):
        lint_wiki = load_module("lint_wiki", ROOT / "scripts" / "lint_wiki.py")
        sources = self.wiki / "10 Sources" / "articles"
        sources.mkdir(parents=True)
        (sources / "first-clip.md").write_text(
            textwrap.dedent(
                """
                ---
                title: First Clip
                source_url: https://example.com/clip
                captured: 2026-04-28
                type: source
                processed: false
                possibly_outdated: true
                raw_file: 10 Sources/articles/first-clip.html
                raw_sha256: abc123
                tags: []
                ---

                Raw capture waiting for ingest.
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )
        (sources / "second-clip.md").write_text(
            textwrap.dedent(
                """
                ---
                title: Second Clip
                source_url: https://example.com/clip/
                captured: 2026-04-28
                type: source
                processed: true
                tags: []
                ---

                Duplicate source URL after normalization.
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )
        (self.wiki / "concepts" / "rag-agent-memory.md").write_text(
            textwrap.dedent(
                """
                ---
                title: RAG Agent Memory
                aliases: []
                created: 2026-04-28
                updated: 2026-04-28
                type: concept
                tags: [agent, memory]
                sources: []
                ---

                This page links to a system page [[log]], uses a non-canonical target [[Prompt Architecture]],
                and overlaps heavily with a second concept slug.
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )
        (self.wiki / "concepts" / "agent-rag-memory.md").write_text(
            textwrap.dedent(
                """
                ---
                title: Agent RAG Memory
                aliases: []
                created: 2026-04-28
                updated: 2026-04-28
                type: concept
                tags: [agent, memory]
                sources: []
                ---

                A near duplicate slug for the same concept family.
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )

        report = lint_wiki.lint_wiki(self.wiki)
        codes = {issue["code"] for issue in report["issues"]}

        self.assertIn("unprocessed-source", codes)
        self.assertIn("possibly-outdated-source", codes)
        self.assertIn("duplicate-source-url", codes)
        self.assertIn("forbidden-wikilink", codes)
        self.assertIn("non-kebab-wikilink", codes)
        self.assertIn("near-duplicate-slug", codes)

    def test_build_source_dependencies_maps_raw_sources_to_pages(self):
        build_source_dependencies = load_module("build_source_dependencies", ROOT / "scripts" / "build_source_dependencies.py")
        sources = self.wiki / "10 Sources" / "articles"
        sources.mkdir(parents=True)
        raw_file = sources / "karpathy.html"
        raw_file.write_text("<article>Compiled wiki memory</article>\n", encoding="utf-8")
        (sources / "karpathy-llm-wiki.md").write_text(
            textwrap.dedent(
                """
                ---
                title: Karpathy LLM Wiki
                source_url: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
                captured: 2026-04-28
                type: source
                processed: true
                raw_file: 10 Sources/articles/karpathy.html
                raw_sha256: rawhash
                tags: []
                ---

                This source supports [[agentic-workflow]].
                """
            ).strip()
            + "\n",
            encoding="utf-8",
        )

        report = build_source_dependencies.build_source_dependencies(self.wiki)
        deps = report["dependencies"]

        self.assertIn("10 Sources/articles/karpathy-llm-wiki.md", deps)
        self.assertIn("10 Sources/articles/karpathy.html", deps)
        self.assertEqual(deps["10 Sources/articles/karpathy-llm-wiki.md"]["raw_file"], "10 Sources/articles/karpathy.html")
        self.assertIn("concepts/agentic-workflow.md", deps["10 Sources/articles/karpathy-llm-wiki.md"]["wiki_pages"])
        self.assertIn("concepts/agentic-workflow.md", deps["10 Sources/articles/karpathy.html"]["wiki_pages"])

        written = build_source_dependencies.write_dependencies(self.wiki, report)
        self.assertNotIn('"wiki":', written.read_text(encoding="utf-8"))


class SkillDocumentationTests(unittest.TestCase):
    def test_obsidian_adapter_reference_is_linked_and_attributed(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        optional = (ROOT / "references" / "optional-integrations.md").read_text(encoding="utf-8")
        adapter_path = ROOT / "references" / "obsidian-adapters.md"

        self.assertIn("references/obsidian-adapters.md", skill)
        self.assertTrue(adapter_path.is_file())

        adapter = adapter_path.read_text(encoding="utf-8")
        for required in [
            "kepano/obsidian-skills",
            "MIT",
            "obsidian-markdown",
            "obsidian-bases",
            "json-canvas",
            "obsidian-cli",
            "defuddle",
            "raw/wiki",
        ]:
            self.assertIn(required, adapter)

        self.assertIn("obsidian", optional)
        self.assertIn("defuddle", optional)

    def test_optional_obsidian_templates_are_valid_files(self):
        base_templates = [
            ROOT / "templates" / "source-queue.base",
            ROOT / "templates" / "wiki-health.base",
        ]
        canvas_template = ROOT / "templates" / "concept-map.canvas"

        for path in base_templates:
            text = path.read_text(encoding="utf-8")
            self.assertIn("views:", text)
            self.assertIn("filters:", text)

        import json

        canvas = json.loads(canvas_template.read_text(encoding="utf-8"))
        self.assertIn("nodes", canvas)
        self.assertIn("edges", canvas)
        node_ids = {node["id"] for node in canvas["nodes"]}
        self.assertEqual(len(node_ids), len(canvas["nodes"]))
        for edge in canvas["edges"]:
            self.assertIn(edge["fromNode"], node_ids)
            self.assertIn(edge["toNode"], node_ids)


if __name__ == "__main__":
    unittest.main()
