import json
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "orchestration"
AGENTS = ROOT / "agents"
INSTALLER = ROOT / "scripts" / "install-agents.sh"
INSPECTOR = ROOT / "scripts" / "inspect-agent-runtime.sh"


class OrchestraContractTests(unittest.TestCase):
    def test_manifest_contract(self):
        manifest = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text())
        self.assertEqual(manifest["name"], "orchestra")
        self.assertRegex(
            manifest["version"], r"^0\.2\.1(?:\+[0-9A-Za-z.-]+)?$"
        )
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertEqual(manifest["repository"], "https://github.com/vldklsnkv/orchestra")
        self.assertEqual(manifest["interface"]["displayName"], "Orchestra")

        for field in ("composerIcon", "logo"):
            asset = manifest["interface"][field]
            self.assertEqual(asset, "./assets/icon.png")
            self.assertTrue((ROOT / asset.removeprefix("./")).is_file())

        prompts = manifest["interface"]["defaultPrompt"]
        self.assertGreaterEqual(len(prompts), 1)
        self.assertLessEqual(len(prompts), 3)
        for prompt in prompts:
            self.assertLessEqual(len(prompt), 128)

    def test_exact_model_and_reasoning_profiles(self):
        expected = {
            "orchestra-luna-implementer.toml": {
                "name": "orchestra_luna_implementer",
                "model": "gpt-5.6-luna",
                "model_reasoning_effort": "max",
            },
            "orchestra-terra-implementer.toml": {
                "name": "orchestra_terra_implementer",
                "model": "gpt-5.6-terra",
                "model_reasoning_effort": "high",
            },
            "orchestra-sol-reviewer.toml": {
                "name": "orchestra_sol_reviewer",
                "model": "gpt-5.6-sol",
                "model_reasoning_effort": "high",
                "sandbox_mode": "read-only",
            },
        }
        self.assertEqual({path.name for path in AGENTS.glob("*.toml")}, set(expected))

        for filename, fields in expected.items():
            content = (AGENTS / filename).read_text()
            self.assertIn("developer_instructions = \"\"\"", content)
            for field, value in fields.items():
                match = re.search(rf'(?m)^{re.escape(field)} = "([^"]+)"$', content)
                self.assertIsNotNone(match, f"{filename}: missing {field}")
                self.assertEqual(match.group(1), value)

    def test_skill_enforces_sol_led_selective_routing(self):
        skill = (SKILL / "SKILL.md").read_text()
        contracts = (SKILL / "references" / "role-contracts.md").read_text()
        operations = (SKILL / "references" / "operations.md").read_text()

        self.assertTrue(skill.startswith("---\nname: orchestration\n"))
        self.assertIn("SELECTIVE ROUTE", skill)
        self.assertIn("gpt-5.6-sol with high reasoning", skill)
        self.assertIn("Luna / Max", skill)
        self.assertIn("Terra / High", skill)
        self.assertIn("fresh read-only Sol / High", skill)
        for route in ("solo", "delegate", "audit", "full"):
            self.assertIn(f"`{route}`", skill)
        for role in (
            "orchestra_luna_implementer",
            "orchestra_terra_implementer",
            "orchestra_sol_reviewer",
        ):
            self.assertIn(role, contracts)
            self.assertIn(role, operations)

    def test_skill_breaks_only_evidence_backed_stalled_loops(self):
        skill = (SKILL / "SKILL.md").read_text()
        operations = (SKILL / "references" / "operations.md").read_text()

        for content in (skill, operations):
            normalized = " ".join(content.lower().split())
            self.assertIn("STRATEGIC CHECKPOINT", content)
            self.assertIn("two consecutive materially similar", normalized)
            self.assertIn("materially different", normalized)
            self.assertIn("success signal", normalized)
            self.assertIn("preserve", normalized)

        skill_normalized = " ".join(skill.split())
        operations_normalized = " ".join(operations.split())
        self.assertIn("Do not abandon a productive path", skill_normalized)
        self.assertIn("stop and ask the user", skill_normalized)
        self.assertIn(
            "Never use a checkpoint to bypass", operations_normalized
        )

    def test_installer_is_fail_closed_and_selective(self):
        self.assertTrue(os.access(INSTALLER, os.X_OK))
        for script in (INSTALLER, INSPECTOR):
            syntax = subprocess.run(
                ["/bin/sh", "-n", str(script)], capture_output=True, text=True
            )
            self.assertEqual(syntax.returncode, 0, syntax.stderr)

        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "agents"
            install = subprocess.run(
                [str(INSTALLER), "--target-dir", str(target)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(install.returncode, 0, install.stderr)
            self.assertIn("INSTALL PASSED", install.stdout)

            check = subprocess.run(
                [str(INSTALLER), "--target-dir", str(target), "--check"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(check.returncode, 0, check.stderr)

            terra = target / "orchestra-terra-implementer.toml"
            terra.write_text(terra.read_text() + "\n# local conflict\n")
            before = terra.read_bytes()
            luna_only = subprocess.run(
                [
                    str(INSTALLER),
                    "--target-dir",
                    str(target),
                    "--check-role",
                    "luna",
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(luna_only.returncode, 0, luna_only.stderr)
            self.assertEqual(terra.read_bytes(), before)

            terra_only = subprocess.run(
                [
                    str(INSTALLER),
                    "--target-dir",
                    str(target),
                    "--check-role",
                    "terra",
                ],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(terra_only.returncode, 0)
            self.assertEqual(terra.read_bytes(), before)

    def test_attribution_and_documentation(self):
        notice = (ROOT / "NOTICE.md").read_text()
        readme = (ROOT / "README.md").read_text()
        license_text = (ROOT / "LICENSE").read_text()
        self.assertIn("DannyMac180/sol-advisor", notice)
        self.assertIn("37b75cad535abdd46531f0227483a8842d045ab8", notice)
        self.assertIn("Copyright (c) 2026 Daniel McAteer", license_text)
        self.assertIn("sh scripts/install-agents.sh", readme)


if __name__ == "__main__":
    unittest.main()
