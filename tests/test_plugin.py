import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_DIR = ROOT / "plugins" / "onboard"
SCRIPTS = PLUGIN_DIR / "skills" / "onboard" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import check  # noqa: E402
import redact  # noqa: E402


def story(**overrides):
    value = {
        "id": "test-story",
        "langs": ["en"],
        "defaultLang": "en",
        "brief": {
            "recipient": "internal",
            "sharing": "external",
            "level": "medium",
            "skeleton": "giai-thich",
            "purpose": "test",
        },
        "meta": {"title": "Test", "footer": "Footer"},
        "steps": [{"title": "First"}, {"title": "Second"}],
    }
    value.update(overrides)
    return value


class PluginHardeningTests(unittest.TestCase):
    def test_plugin_identity_is_onboard(self):
        manifest = json.loads((PLUGIN_DIR / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(PLUGIN_DIR.name, "onboard")
        self.assertEqual(manifest["name"], "onboard")

    def test_external_renderable_values_are_scanned(self):
        value = story(
            steps=[
                {
                    "title": "Secrets",
                    "visual": {
                        "pattern": "stats",
                        "items": [{"label": "Key", "value": {"en": "api_key=SECRET"}}],
                    },
                },
                {
                    "title": "Custom",
                    "visual": {"pattern": "custom", "html": "<p>token=SECRET</p>"},
                },
            ]
        )
        report = check.static_check(value)
        self.assertTrue(report.errors)
        self.assertTrue(any("nhạy cảm" in error for error in report.errors))

    def test_unlisted_locale_values_are_scanned(self):
        value = story(meta={"title": {"en": "Visible", "fr": "api_key=SECRET"}})
        report = check.static_check(value)
        self.assertTrue(report.errors)

    def test_malformed_story_returns_structured_errors(self):
        for malformed in ([], {"steps": ["bad", "also bad"]}, {"langs": 3}):
            report = check.static_check(malformed)
            self.assertIsInstance(report, check.Report)
            self.assertTrue(report.errors)

    def test_hook_returns_actionable_failure_for_malformed_story(self):
        hook = PLUGIN_DIR / "hooks" / "../skills/onboard/scripts/hook_check.py"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "broken.story.json"
            path.write_text(json.dumps({"steps": ["bad", "also bad"]}), encoding="utf-8")
            payload = json.dumps({"tool_input": {"file_path": str(path)}})
            result = subprocess.run(
                [sys.executable, str(hook.resolve())],
                input=payload,
                capture_output=True,
                text=True,
                encoding="utf-8",
                env={**os.environ, "PYTHONUTF8": "1"},
                check=False,
            )
        self.assertEqual(result.returncode, 2)
        self.assertIn("lỗi cần sửa", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_calc_expression_and_input_id_are_checked(self):
        self.assertIsNotNone(check.expr_problems("1 +", set()))
        value = story(
            steps=[
                {
                    "title": "Calc",
                    "visual": {
                        "pattern": "calc",
                        "inputs": [{"id": 'x"><img src=x onerror=alert(1)>', "label": "X"}],
                        "outputs": [{"label": "Result", "expr": "1"}],
                    },
                },
                {"title": "Second"},
            ]
        )
        report = check.static_check(value)
        self.assertTrue(report.errors)

    def test_unknown_basis_is_rejected(self):
        value = story(
            brief={
                "recipient": "internal",
                "sharing": "internal",
                "level": "high",
                "skeleton": "giai-thich",
                "purpose": "test",
            },
            steps=[
                {"title": "Unknown", "basis": "wat", "sources": ["test"]},
                {"title": "Second", "sources": ["test"]},
            ],
        )
        report = check.static_check(value)
        self.assertTrue(report.errors)

    def test_redaction_covers_brief_bearer_and_paths_with_spaces(self):
        counts = {}
        value = {
            "brief": {"owner": "alice@example.com", "auth": "Authorization: Bearer sk_live_123"},
            "body": r"Path C:\Users\Alice\My Secret\password.txt",
        }
        output = redact.redact_json(value, [], [], counts)
        rendered = json.dumps(output, ensure_ascii=False)
        self.assertNotIn("alice@example.com", rendered)
        self.assertNotIn("sk_live_123", rendered)
        self.assertNotIn("My Secret\\password.txt", rendered)

    def test_reader_view_includes_footer(self):
        story_path = PLUGIN_DIR / "skills" / "onboard" / "examples" / "patterns-showcase.story.json"
        value = json.loads(story_path.read_text(encoding="utf-8"))
        value["meta"]["footer"] = "Footer survives review"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "story.json"
            path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
            env = os.environ.copy()
            env["PYTHONUTF8"] = "1"
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "reader_view.py"), str(path)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=env,
                check=False,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Footer survives review", result.stdout)

    def test_installer_force_keeps_existing_files_and_writes_nested_agents_file(self):
        installer = ROOT / "install" / "install.py"
        env = os.environ.copy()
        env["PYTHONUTF8"] = "1"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            destination = root / "skills"
            old_skill = destination / "onboard"
            old_skill.mkdir(parents=True)
            (old_skill / "user-note.txt").write_text("keep", encoding="utf-8")
            agents = root / "nested" / "AGENTS.md"
            result = subprocess.run(
                [sys.executable, str(installer), "--dest", str(destination), "--force", "--agents-md", str(agents)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=env,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual((old_skill / "user-note.txt").read_text(encoding="utf-8"), "keep")
            content = agents.read_text(encoding="utf-8")
            self.assertIn("<!-- ONBOARD:START -->", content)
            self.assertEqual(content.count("<!-- ONBOARD:START -->"), 1)


if __name__ == "__main__":
    unittest.main()
