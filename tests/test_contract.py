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
    "ROLE",
    "OBJECTIVE",
    "CURRENT STATE (authoritative facts)",
    "CONSTRAINTS / INVARIANTS",
    "ALLOWED SCOPE",
    "FORBIDDEN ACTIONS",
    "RELEVANT FILES / ARTIFACTS",
    "EXPECTED OUTPUT / VERIFICATION",
    "STOP / ESCALATION",
)


class OrchestraContractTests(unittest.TestCase):
    def test_manifest_contract(self):
        manifest = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text())
        self.assertEqual(manifest["name"], "orchestra")
        self.assertRegex(manifest["version"], r"^0\.4\.0(?:\+[0-9A-Za-z.-]+)?$")
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

    def test_native_context_inheritance_contract(self):
        readme = (ROOT / "README.md").read_text()
        skill = (SKILL / "SKILL.md").read_text()
        contracts = (REFERENCES / "role-contracts.md").read_text()
        operations = (REFERENCES / "operations.md").read_text()
        combined = skill + contracts + operations

        self.assertIn("Context inheritance:", skill)
        self.assertIn("fork_turns` is a native spawn decision", skill)
        self.assertIn(
            "`none`, a positive integer string `<N>`,\nor `all`", contracts
        )
        self.assertIn("Default to `none`", combined)
        self.assertIn("only when recent turns are materially necessary", combined)
        self.assertIn("rare fallback", combined)
        self.assertIn("reviewer always receives `none`", contracts)
        self.assertIn("defaults to `all` only when omitted", contracts)
        for name, document in (
            ("README.md", readme),
            ("SKILL.md", skill),
            ("role-contracts.md", contracts),
            ("operations.md", operations),
        ):
            with self.subTest(document=name):
                normalized = " ".join(document.split())
                self.assertIn(
                    "exact full interaction history is itself an explicitly addressed authoritative artifact",
                    normalized,
                )
                self.assertIn(
                    "no unrecorded constraint may control an allowed action",
                    normalized.lower(),
                )
                self.assertIn(
                    "inherited turns are supplementary context only",
                    normalized.lower(),
                )
        self.assertIn("none`, limited `<N>`, and `all`", skill)
        self.assertIn("safety boundary, permission, ownership, invariant", contracts)
        self.assertIn("every safety and scope boundary", operations)

    def test_context_packet_is_complete_and_addressed(self):
        skill = (SKILL / "SKILL.md").read_text()
        contracts = (REFERENCES / "role-contracts.md").read_text()
        operations = (REFERENCES / "operations.md").read_text()

        for field in PACKET_FIELDS:
            self.assertIn(field, skill)
            self.assertIn(field, contracts)
        for phrase in ("paths", "symbols", "ranges", "evidence"):
            self.assertIn(phrase, skill.lower())
        self.assertIn("DO NOT RESEARCH", contracts)
        self.assertIn("non-overlapping", contracts)
        self.assertIn("CURRENT STATE (authoritative facts)", operations)
        self.assertIn("Do not claim token savings", operations)
        for field in (
            "STATUS / RESULT:",
            "DECISION / VERDICT:",
            "EVIDENCE / ARTIFACTS:",
            "FILES CHANGED:",
            "UNRESOLVED RISKS / AMBIGUITIES:",
            "STOP / ESCALATION REASON:",
        ):
            self.assertIn(field, contracts)

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
        self.assertIn("full manager transcript", contracts)
        self.assertIn("ORCHESTRA RUN", skill)
        for field in (
            "Strategy:",
            "Roles:",
            "Agents:",
            "Escalations:",
            "Retries:",
            "Review:",
            "Lanes:",
            "Packets:",
            "Host metrics:",
            "Result:",
            "Verification:",
        ):
            self.assertIn(field, combined)
        self.assertIn("unavailable/not-exposed", combined)
        self.assertIn("never infer, parse private transcripts", combined)
        for metric in (
            "input_tokens",
            "cached_input_tokens",
            "output_tokens",
            "tool_calls",
            "duration",
        ):
            self.assertIn(metric, combined)

    def test_dry_runs_cover_all_strategies_and_packets(self):
        dry_runs = (REFERENCES / "dry-runs.md").read_text()
        for index, strategy in enumerate(STRATEGIES, start=1):
            self.assertIn(f"## {index}.", dry_runs)
            self.assertIn(f"Strategy: {strategy}", dry_runs)

        self.assertIn("No worker is spawned, so no Context Packet exists", dry_runs)
        self.assertIn("Decomposable: yes (5 independent lanes)", dry_runs)
        self.assertIn("Review: yes", dry_runs)
        self.assertIn("fork_turns: none", dry_runs)
        self.assertIn("minimal discriminating", dry_runs.lower())
        self.assertIn("arbitrates against one rubric", dry_runs)
        self.assertIn("DO NOT RESEARCH", dry_runs)

        scenarios = {}
        for label in (
            "A. Isolated specialist -> none",
            "B. Specialist + reviewer -> scoped/none and evidence-only",
            "C. Context-dependent continuation -> limited N",
            "D. Genuinely unsafe reconstruction -> deliberate all fallback",
        ):
            start = dry_runs.index(f"### {label}")
            next_heading = dry_runs.find("\n### ", start + 1)
            scenarios[label[0]] = dry_runs[start: next_heading if next_heading != -1 else None]

        expected_boundary = "objective, exact allowed scope and ownership"
        self.assertIn("Mode: `fork_turns: none`", scenarios["A"])
        self.assertIn("Reason: no prior turn is material", scenarios["A"])
        self.assertIn(expected_boundary, scenarios["A"])

        self.assertIn("Specialist mode: `fork_turns: none`", scenarios["B"])
        self.assertIn("Reviewer mode: `fork_turns: none`", scenarios["B"])
        self.assertIn("fresh evidence-only review", scenarios["B"])
        self.assertIn("full manager transcript", scenarios["B"])

        self.assertIn('Mode: `fork_turns: "3"`', scenarios["C"])
        self.assertIn("last `3` turns", scenarios["C"])
        self.assertIn("inherited turns cannot supply a", scenarios["C"])

        self.assertIn("Mode: `fork_turns: all`", scenarios["D"])
        normalized_d = " ".join(scenarios["D"].split())
        with self.subTest(document="dry-runs.md scenario D"):
            self.assertIn(
                "complete user-confirmed multi-turn decision transcript is the explicit authoritative artifact",
                normalized_d,
            )
            self.assertIn("transcript's artifact address", normalized_d)
            self.assertIn("every constraint and safety boundary", normalized_d)
            self.assertIn(
                "no unrecorded constraint controls an allowed action",
                normalized_d.lower(),
            )
            self.assertIn("inherited turns only supplement the packet", normalized_d.lower())

    def test_role_spawn_templates_localize_inheritance_modes(self):
        contracts = (REFERENCES / "role-contracts.md").read_text()

        expected_templates = {
            "orchestra_luna_implementer": "Spawn Luna exactly:",
            "orchestra_terra_implementer": "Spawn Terra exactly:",
        }
        for role, heading in expected_templates.items():
            start = contracts.index(heading)
            end = contracts.index("~~~", contracts.index("~~~", start) + 3) + 3
            template = contracts[start:end]
            self.assertIn(f"agent_type: {role}", template)
            self.assertIn(
                "fork_turns: <explicit none | positive integer string N | all>",
                template,
            )

        reviewer_start = contracts.index("After manager verification, spawn exactly:")
        reviewer_end = contracts.index("~~~", contracts.index("~~~", reviewer_start) + 3) + 3
        reviewer_template = contracts[reviewer_start:reviewer_end]
        self.assertIn("agent_type: orchestra_sol_reviewer", reviewer_template)
        self.assertIn("fork_turns: none", reviewer_template)
        self.assertNotIn("positive integer string N", reviewer_template)

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
