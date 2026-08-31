import json
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "orchestration"
REFERENCES = SKILL / "references"
AGENTS = ROOT / "agents"
INSTALLER = ROOT / "scripts" / "install-agents.sh"
INSPECTOR = ROOT / "scripts" / "inspect-agent-runtime.sh"

STRATEGIES = (
    "solo",
    "delegate",
    "expert",
    "parallel",
    "explore",
    "plan-execute",
    "diagnose-fix",
)

PACKET_FIELDS = (
    "GOAL",
    "STRATEGY / ROLE",
    "IMPLEMENTATION SPEC",
    "RELEVANT FILES / SYMBOLS / RANGES",
    "KNOWN FACTS",
    "RELEVANT EVIDENCE",
    "INTERFACES / INVARIANTS",
    "OWNED FILES / SYMBOLS",
    "DO NOT TOUCH",
    "DO NOT RESEARCH",
    "VERIFICATION",
    "STOP / ESCALATION CONDITIONS",
)


class OrchestraContractTests(unittest.TestCase):
    def test_manifest_contract(self):
        manifest = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text())
        self.assertEqual(manifest["name"], "orchestra")
        self.assertRegex(manifest["version"], r"^0\.3\.0(?:\+[0-9A-Za-z.-]+)?$")
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertEqual(manifest["repository"], "https://github.com/vldklsnkv/orchestra")
        self.assertEqual(manifest["interface"]["displayName"], "Orchestra")
        self.assertIn("strategy", manifest["description"].lower())
        self.assertIn("context", manifest["description"].lower())

        for field in ("composerIcon", "logo"):
            asset = manifest["interface"][field]
            self.assertEqual(asset, "./assets/icon.png")
            self.assertTrue((ROOT / asset.removeprefix("./")).is_file())

        prompts = manifest["interface"]["defaultPrompt"]
        self.assertGreaterEqual(len(prompts), 1)
        self.assertLessEqual(len(prompts), 3)
        self.assertTrue(any("strategy" in prompt.lower() for prompt in prompts))
        self.assertTrue(any("context" in prompt.lower() for prompt in prompts))
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
            self.assertIn('developer_instructions = """', content)
            self.assertIn("evidence", content.lower())
            for field, value in fields.items():
                match = re.search(rf'(?m)^{re.escape(field)} = "([^"]+)"$', content)
                self.assertIsNotNone(match, f"{filename}: missing {field}")
                self.assertEqual(match.group(1), value)

        luna = (AGENTS / "orchestra-luna-implementer.toml").read_text()
        terra = (AGENTS / "orchestra-terra-implementer.toml").read_text()
        reviewer = (AGENTS / "orchestra-sol-reviewer.toml").read_text()
        self.assertIn("Context Packet", luna)
        self.assertIn("at most one corrected Luna retry", luna)
        self.assertIn("selected immediately", terra)
        self.assertIn("rethink signal", terra)
        self.assertIn("Do not merely trust", reviewer)

    def test_skill_is_strategy_first(self):
        skill = (SKILL / "SKILL.md").read_text()
        contracts = (REFERENCES / "role-contracts.md").read_text()
        operations = (REFERENCES / "operations.md").read_text()

        self.assertTrue(skill.startswith("---\nname: orchestration\n"))
        self.assertIn("Choose strategy before role", skill)
        self.assertIn("SELECTIVE ROUTE", skill)
        self.assertIn("gpt-5.6-sol with high reasoning", skill)
        self.assertIn("orchestration cost is comparable", skill)
        for strategy in STRATEGIES:
            self.assertIn(f"`{strategy}`", skill)
        for role in (
            "orchestra_luna_implementer",
            "orchestra_terra_implementer",
            "orchestra_sol_reviewer",
        ):
            self.assertIn(role, contracts)
            self.assertIn(role, operations)

        self.assertIn("Composable modifiers", skill)
        self.assertIn("`review`", skill)
        self.assertIn("`parallel`", skill)
        self.assertIn("Luna failure is not required", skill)
        self.assertIn("Do not jump to a speculative", skill)

    def test_context_packet_is_complete_and_addressed(self):
        skill = (SKILL / "SKILL.md").read_text()
        contracts = (REFERENCES / "role-contracts.md").read_text()
        operations = (REFERENCES / "operations.md").read_text()

        for field in PACKET_FIELDS:
            self.assertIn(field, skill)
            self.assertIn(field, contracts)
        for phrase in ("paths", "symbols", "ranges", "evidence locations"):
            self.assertIn(phrase, skill.lower())
        self.assertIn("distinct investigation scope", contracts)
        self.assertIn("prevents rediscovery", operations)
        self.assertIn("Do not claim token savings", operations)

    def test_stop_retry_and_rethink_contract(self):
        skill = (SKILL / "SKILL.md").read_text()
        contracts = (REFERENCES / "role-contracts.md").read_text()
        combined = " ".join((skill + contracts).split()).lower()

        self.assertIn("at most one corrected luna retry", combined)
        self.assertIn("no luna retry is required", combined)
        self.assertIn("same failure repeats without new evidence", combined)
        self.assertIn("invalidates the architecture", combined)
        self.assertIn("worker stop", combined)
        self.assertIn("strategic checkpoint", combined)
        self.assertIn("materially different", combined)

    def test_review_and_run_metadata_contract(self):
        skill = (SKILL / "SKILL.md").read_text()
        contracts = (REFERENCES / "role-contracts.md").read_text()
        operations = (REFERENCES / "operations.md").read_text()
        combined = skill + contracts + operations

        for verdict in ("ship", "fix-first", "rethink"):
            self.assertIn(f"`{verdict}`", skill)
        self.assertIn("Do not trust summaries", contracts)
        self.assertIn("ORCHESTRA RUN", skill)
        for field in (
            "Strategy:",
            "Roles:",
            "Agents:",
            "Escalations:",
            "Retries:",
            "Review:",
            "Context:",
            "Result:",
            "Verification:",
        ):
            self.assertIn(field, combined)
        self.assertIn("Do not fabricate token, duration, or cost metrics", skill)

    def test_dry_runs_cover_all_strategies_and_packets(self):
        dry_runs = (REFERENCES / "dry-runs.md").read_text()
        for index, strategy in enumerate(STRATEGIES, start=1):
            self.assertIn(f"## {index}.", dry_runs)
            self.assertIn(f"Strategy: {strategy}", dry_runs)

        self.assertIn("No worker is spawned, so no\nContext Packet exists", dry_runs)
        self.assertIn("Decomposable: yes (5 independent lanes)", dry_runs)
        self.assertIn("Review: yes", dry_runs)
        self.assertIn("Reviewer packet after Sol verification", dry_runs)
        self.assertIn("minimal discriminating", dry_runs.lower())
        self.assertIn("Sol arbitrates", dry_runs)
        self.assertIn("DO NOT RESEARCH", dry_runs)

    def test_no_obsolete_mode_contracts_in_shipped_text(self):
        shipped = [
            ROOT / "README.md",
            ROOT / "NOTICE.md",
            ROOT / ".codex-plugin" / "plugin.json",
            SKILL / "SKILL.md",
            SKILL / "agents" / "openai.yaml",
            *REFERENCES.glob("*.md"),
            *AGENTS.glob("*.toml"),
        ]
        combined = "\n".join(path.read_text() for path in shipped)
        obsolete = (
            "mode: solo | delegate | audit | full",
            "four exact modes",
            "audit/full",
            "delegate/full",
            "for `audit` and `full`",
        )
        for phrase in obsolete:
            self.assertNotIn(phrase, combined.lower())

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

            update = subprocess.run(
                [str(INSTALLER), "--target-dir", str(target), "--update"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(update.returncode, 0, update.stderr)
            self.assertIn("UPDATED:", update.stdout)
            backups = list(target.glob(".orchestra-terra-backup.*"))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_bytes(), before)
            self.assertEqual(
                terra.read_bytes(),
                (AGENTS / "orchestra-terra-implementer.toml").read_bytes(),
            )

            foreign_before = terra.read_text().replace(
                'name = "orchestra_terra_implementer"',
                'name = "foreign_terra_implementer"',
            )
            terra.write_text(foreign_before)
            refused = subprocess.run(
                [str(INSTALLER), "--target-dir", str(target), "--update"],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(refused.returncode, 0)
            self.assertEqual(terra.read_text(), foreign_before)

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
