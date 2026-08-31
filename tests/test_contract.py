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
    "VERIFIED CONTEXT",
    "CONSTRAINTS / INVARIANTS",
    "ALLOWED SCOPE",
    "FORBIDDEN ACTIONS",
    "RELEVANT FILES / ARTIFACTS",
    "EXPECTED OUTPUT / VERIFICATION",
    "STOP / ESCALATION",
)

HANDOFF_FIELDS = (
    "Objective:",
    "Acceptance criteria:",
    "Hard constraints:",
    "Changed files:",
    "Diff references:",
    "Verified context:",
    "Test / verification results:",
    "Created artifacts:",
    "Important invariants:",
    "Unresolved risks:",
    "Exact questions for next agent:",
)


class OrchestraContractTests(unittest.TestCase):
    def test_manifest_contract(self):
        manifest = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text())
        self.assertEqual(manifest["name"], "orchestra")
        self.assertRegex(manifest["version"], r"^0\.6\.0(?:\+[0-9A-Za-z.-]+)?$")
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertEqual(manifest["repository"], "https://github.com/vldklsnkv/orchestra")
        self.assertEqual(manifest["interface"]["displayName"], "Orchestra")
        self.assertIn("adaptive", manifest["description"].lower())
        self.assertIn("single-agent-first", manifest["description"].lower())
        self.assertIn("context", manifest["description"].lower())
        self.assertIn("budget", manifest["description"].lower())
        long_description = manifest["interface"]["longDescription"].lower()
        self.assertIn("sol or terra", long_description)
        self.assertIn("sticky owner", long_description)
        self.assertIn("fast", long_description)
        self.assertIn("verified context", long_description)

        for field in ("composerIcon", "logo"):
            asset = manifest["interface"][field]
            self.assertEqual(asset, "./assets/icon.png")
            self.assertTrue((ROOT / asset.removeprefix("./")).is_file())

        prompts = manifest["interface"]["defaultPrompt"]
        self.assertGreaterEqual(len(prompts), 1)
        self.assertLessEqual(len(prompts), 3)
        self.assertTrue(any("single-agent-first" in prompt.lower() for prompt in prompts))
        self.assertTrue(any("agent" in prompt.lower() for prompt in prompts))
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
        self.assertIn("A Luna failure is never a prerequisite", terra)
        self.assertIn("rethink signal", terra)
        self.assertIn("selected initial owner", terra)
        self.assertIn("Complexity alone never\nselects the owner", terra)
        self.assertIn("low/medium-risk, objectively verifiable mechanical work", terra)
        self.assertIn("Do not merely trust", reviewer)

    def test_skill_is_adaptive_single_agent_first(self):
        skill = (SKILL / "SKILL.md").read_text()
        contracts = (REFERENCES / "role-contracts.md").read_text()
        operations = (REFERENCES / "operations.md").read_text()

        self.assertTrue(skill.startswith("---\nname: orchestration\n"))
        self.assertIn("Act as the primary Sol / High owner by default", skill)
        self.assertIn("`adaptive-v2` is the default", skill)
        self.assertIn("`legacy` preserves the v0.4", skill)
        self.assertIn("SELECTIVE ROUTE", skill)
        self.assertIn("gpt-5.6-sol with high reasoning", skill)
        self.assertIn("One agent is a valid Orchestra result", skill)
        self.assertIn("do not call an LLM merely to classify", " ".join(skill.split()))
        for strategy in STRATEGIES:
            self.assertIn(f"`{strategy}`", skill)
        for role in (
            "orchestra_luna_implementer",
            "orchestra_terra_implementer",
            "orchestra_sol_reviewer",
        ):
            self.assertIn(role, contracts)
            self.assertIn(role, operations)

        self.assertIn("Review value and independent review", skill)
        self.assertIn("orchestrated-parallel", skill)
        self.assertIn("Luna failure is not required", skill)
        self.assertIn("Do not jump to a speculative", skill)
        self.assertIn("Deterministic adaptive-v2 routing", operations)
        self.assertIn("Primary owner and conditional manager", contracts)

    def test_adaptive_routing_topologies(self):
        dry_runs = (REFERENCES / "dry-runs.md").read_text()
        scenarios = {
            "simple": "## 1. Simple one-file bug -> solo owner-only",
            "connected": "## 2. Connected medium feature -> solo owner-only",
            "high_risk": "## 3. High-risk auth migration -> solo + high-value review",
            "parallel": "## 4. Five independent adapters -> parallel",
            "non_parallel": "## 5. Non-decomposable refactor -> solo, no fake parallelism",
        }
        slices = {}
        for name, heading in scenarios.items():
            start = dry_runs.index(heading)
            end = dry_runs.find("\n## ", start + len(heading))
            slices[name] = dry_runs[start: end if end != -1 else None]

        self.assertIn("Topology: owner-only", slices["simple"])
        self.assertIn("Independent review: no", slices["simple"])
        self.assertIn("Manager: no", slices["simple"])
        self.assertIn("No worker, manager, or reviewer is spawned", slices["simple"])
        self.assertIn("spawned owner invocation", slices["simple"])

        self.assertIn("Complexity: medium", slices["connected"])
        self.assertIn("Topology: owner-only", slices["connected"])
        self.assertIn("one owner", slices["connected"].lower())

        self.assertIn("Risk: high", slices["high_risk"])
        self.assertIn("Topology: owner-review", slices["high_risk"])
        self.assertIn("Independent review: yes", slices["high_risk"])

        self.assertIn("Parallelizable: yes", slices["parallel"])
        self.assertIn("non-overlapping files", slices["parallel"])
        self.assertIn("Manager: yes", slices["parallel"])

        self.assertIn("Parallelizable: no", slices["non_parallel"])
        self.assertIn("Topology: owner-only", slices["non_parallel"])
        self.assertIn("does not itself create a worker", slices["non_parallel"])

    def test_review_value_is_independent_from_high_risk(self):
        skill = (SKILL / "SKILL.md").read_text()
        operations = (REFERENCES / "operations.md").read_text()
        combined = " ".join((skill + operations).split()).lower()
        self.assertIn("review value: low|medium|high", combined)
        self.assertIn("high domain risk alone must not force review", combined)
        self.assertIn("high risk alone must not force review", combined)
        self.assertIn("objective focused tests", combined)
        self.assertIn("explicit review request or high independent review value", combined)
        self.assertIn("medium scope with high review value may", combined)
        self.assertNotIn("if the result is high risk, choose `owner-review`", combined)

    def test_owner_selection_is_qualitative_sticky_and_graph_independent(self):
        skill = (SKILL / "SKILL.md").read_text()
        operations = (REFERENCES / "operations.md").read_text()
        contracts = (REFERENCES / "role-contracts.md").read_text()
        combined = " ".join((skill + operations + contracts).split()).lower()

        for signal in (
            "uncertainty",
            "risk",
            "blast radius",
            "verifiability",
            "task nature / reasoning",
        ):
            self.assertIn(signal, combined)
        self.assertIn("complexity remains", combined)
        self.assertIn("never selects the owner", combined)
        self.assertIn("do not add numeric scoring", combined)
        self.assertIn("no score, numeric threshold, or keyword rule", combined)

        self.assertIn("initial owner: sol | terra", combined)
        self.assertIn("select `terra` only when all of these hold", combined)
        self.assertIn(
            "low uncertainty, low/medium domain risk, isolated/local blast radius,"
            " high/objective verifiability, and mechanical/bounded task nature",
            combined,
        )
        self.assertIn("`sol` is selected for high uncertainty", combined)
        self.assertIn(
            "high cost of a wrong interpretation, high domain risk or blast radius with less-than-high verifiability",
            combined,
        )
        self.assertIn("mixed or unresolved signals conservatively fall back to `sol`", combined)
        self.assertIn("owner selection does not inspect strategy, topology, execution budget", combined)
        self.assertIn("strategy and executor execute it; they do not reselect", combined)
        self.assertIn("immutable between explicit escalation gates", combined)

        self.assertIn("terra -> evidence-addressed artifact handoff -> sol takeover", combined)
        self.assertIn("after takeover sol remains owner", combined)
        self.assertIn("no automatic downgrade or oscillation", combined)
        self.assertIn("sol-to-terra", combined)
        self.assertIn("neither escalation nor an owner switch", combined)

    def test_owner_routing_matrix_covers_eight_cases(self):
        dry_runs = (REFERENCES / "dry-runs.md").read_text()
        matrix_start = dry_runs.index("## 13. Frozen initial-owner matrix")
        matrix = dry_runs[matrix_start:]

        expected_cases = (
            "Low-uncertainty mechanical",
            "High-uncertainty architecture",
            "Small high-blast/hard-to-verify",
            "Large clear mechanical",
            "Terra escalation",
            "Sol completes small implementation",
            "Genuine parallel decomposition",
            "Reviewer boundary",
        )
        for case in expected_cases:
            self.assertIn(f"| {case} |", matrix)

        exact_rows = (
            "| Low-uncertainty mechanical | uncertainty=low; domain risk=low; blast radius=isolated; verifiability=objective; task nature=mechanical/bounded | Terra | solo; no reviewer | Terra owns the complete run |",
            "| High-uncertainty architecture | uncertainty=high; reasoning-heavy architecture/problem-framing; verifiability=partial | Sol | solo | Sol owns research through verification |",
            "| Small high-blast/hard-to-verify | domain risk=high; blast radius=systemic; verifiability=low; review value=high | Sol | `owner-review` from independent value | reviewer does not replace owner or count as escalation |",
            "| Large clear mechanical | uncertainty=low; domain risk=medium; blast radius=isolated; verifiability=objective; task nature=mechanical/bounded | Terra | solo; no reviewer | Terra owns the large bounded implementation |",
            "| Terra escalation | materially higher uncertainty or architectural fork appears | Terra | same topology; owner changes only at evidence gate | `Terra -> evidence-addressed ARTIFACT HANDOFF -> Sol takeover`; Sol stays owner with no downgrade |",
            "| Sol completes small implementation | low scope but mixed interpretation | Sol | solo; no reviewer | completes without Terra handoff |",
            "| Genuine parallel decomposition | independent deliverables; non-overlap; no intermediate dependency | Sol | existing `orchestrated-parallel` path | parallel workers remain; owner does not change |",
            "| Reviewer boundary | any owner with explicit request or named safety/contract boundary with high independent value | Sol or Terra | owner-review | reviewer never replaces owner and `owner_escalations=0` |",
        )
        for row in exact_rows:
            self.assertIn(row, matrix)

        self.assertIn("selected-owner synthesis", (SKILL / "SKILL.md").read_text())
        self.assertIn("Terra, the selected owner, synthesizes once", dry_runs)

    def test_execution_budget_and_verification_matrix_covers_ten_cases(self):
        skill = (SKILL / "SKILL.md").read_text()
        operations = (REFERENCES / "operations.md").read_text()
        contracts = (REFERENCES / "role-contracts.md").read_text()
        dry_runs = (REFERENCES / "dry-runs.md").read_text()
        combined = " ".join((skill + operations + contracts).split()).lower()

        for dimension in (
            "change size",
            "blast radius",
            "behavior impact",
            "novelty/uncertainty evidence",
            "reversibility",
            "production-vs-diagnostic",
            "new-behavior-vs-instrumentation",
            "refactor-vs-additive",
            "verified context",
            "context freshness",
            "execution budget",
            "verification floor",
            "review value",
        ):
            self.assertIn(dimension, combined)
        for value in ("tiny", "small", "medium", "large"):
            self.assertIn(value, combined)
        for level in ("l0", "l1", "l2", "l3"):
            self.assertIn(level, combined)
        route_start = skill.index("SELECTIVE ROUTE")
        route_open = skill.rindex("~~~", 0, route_start)
        route_end = skill.index("~~~", route_start)
        route = skill[route_start:route_end]
        route_lines = [
            line for line in skill[route_open + 3 : route_end].splitlines()
            if line.strip() and line.strip() != "SELECTIVE ROUTE"
        ]
        self.assertLessEqual(len(route_lines), 14)
        self.assertEqual(route.count("Parallel:"), 1)
        self.assertNotIn("Parallelizable:", route)
        for field in (
            "Risk:",
            "Scope:",
            "Blast radius:",
            "Behavior impact:",
            "Context freshness:",
            "Execution budget:",
            "Initial owner:",
            "Primary:",
            "Parallel:",
            "Verification plan:",
            "Verification floor:",
            "Review value:",
            "Reviewer:",
            "Escalation condition:",
        ):
            self.assertIn(field, route)

        contracts_route_start = contracts.index("SELECTIVE ROUTE")
        contracts_route_open = contracts.index("~~~", contracts_route_start)
        contracts_route_end = contracts.index("~~~", contracts_route_open + 3)
        self.assertNotIn(
            "Parallelizable:",
            contracts[contracts_route_start:contracts_route_end],
        )
        for failure_class in (
            "code",
            "harness",
            "infrastructure",
            "flaky/non-deterministic",
            "specification/architecture",
        ):
            self.assertIn(failure_class, combined)

        matrix_start = dry_runs.index("## 14. Execution-budget and verification matrix")
        matrix = dry_runs[matrix_start:]
        headings = (
            "### Case 1: high risk + tiny shadow-only + verified -> FAST",
            "### Case 2: high risk + systemic production -> HEAVY",
            "### Case 3: low/medium risk + large cross-component -> not FAST",
            "### Case 4: small + unknown architecture -> at least STANDARD",
            "### Case 5: FAST unexpected test failure -> controlled escalation",
            "### Case 6: relevant staged/unstaged path change invalidates exact-HEAD context",
            "### Case 7: high risk objectively testable tiny mechanical -> reviewer not required",
            "### Case 8: medium scope + high review value -> review without HEAVY",
            "### Case 9: cold expensive infrastructure + cheap falsifier -> cheap first",
            "### Case 10: cheap pass + critical invariant needs integration -> continue to L2",
        )
        for heading in headings:
            self.assertIn(heading, matrix)

        self.assertIn("expected high risk, small/local/shadow-only behavior", matrix)
        self.assertIn("Clast-like parser/scorer shadow-instrumentation regression", matrix)
        self.assertIn("FAST, one sticky owner", matrix)
        self.assertIn("no reviewer unless new evidence", matrix)
        self.assertIn("Execution budget: FAST", matrix)
        self.assertIn("Execution budget: HEAVY", matrix)
        self.assertIn("Previous execution budget: FAST", matrix)
        self.assertIn("Execution budget: STANDARD", matrix)
        self.assertIn("Context freshness: stale", matrix)
        self.assertIn("review value: low", matrix.lower())
        self.assertIn("Review value: high", matrix)
        self.assertIn("cheap falsifier", matrix.lower())
        self.assertIn("continue to L2", matrix)
        self.assertIn("FAST never skips an L2 or L3 requirement", matrix)

    def test_verified_context_and_budget_escalation_are_non_persistent_and_monotonic(self):
        skill = (SKILL / "SKILL.md").read_text()
        operations = (REFERENCES / "operations.md").read_text()
        contracts = (REFERENCES / "role-contracts.md").read_text()
        combined = " ".join((skill + operations + contracts).split()).lower()

        for field in (
            "repo/worktree",
            "base",
            "relevant files",
            "frozen artifacts",
            "relevant config",
            "architecture map/invariants",
            "evidence timestamp/source",
        ):
            self.assertIn(field, combined)
        self.assertIn("not in a persistent database", combined)
        self.assertIn("minimal freshness proof", combined)
        self.assertIn(
            "same repo/worktree plus exact head proves source freshness only with a relevant-path worktree/index check showing those paths unchanged",
            combined,
        )
        self.assertIn(
            "proven descendant requires checking relevant-path changes since base plus the current worktree/index",
            combined,
        )
        self.assertIn("hash only identity-sensitive", combined)
        self.assertIn("do not hash everything by default", combined)
        self.assertIn("relevant staged or unstaged path change makes context stale", combined)
        self.assertIn("forbids reuse", combined)
        self.assertIn("restores normal preflight", combined)
        self.assertIn("do not reread known architecture", combined)
        self.assertIn("fast -> standard -> heavy", combined)
        self.assertIn("do not pre-escalate", combined)
        self.assertIn("never silently downgrade", combined)
        self.assertIn("new route/budget declaration", combined)
        self.assertIn("naming the evidence", combined)

    def test_exact_head_worktree_change_invalidates_context_reuse(self):
        documents = (
            (ROOT / "README.md").read_text()
            + (SKILL / "SKILL.md").read_text()
            + (REFERENCES / "operations.md").read_text()
            + (REFERENCES / "role-contracts.md").read_text()
            + (REFERENCES / "dry-runs.md").read_text()
        )
        normalized = " ".join(documents.split()).lower()
        self.assertIn(
            "exact-head proof plus relevant staged/unstaged path changed in worktree/index",
            normalized,
        )
        self.assertIn(
            "relevant staged or unstaged path change makes the exact-head context stale and forbids reuse",
            normalized,
        )
        self.assertIn(
            "same repo/worktree plus exact head proves source freshness only with a relevant-path worktree/index check",
            normalized,
        )
        self.assertIn(
            "a proven descendant requires checking relevant-path changes since base plus the current worktree/index",
            normalized,
        )

    def test_owner_telemetry_separates_switches_workers_and_reviewers(self):
        skill = (SKILL / "SKILL.md").read_text()
        operations = (REFERENCES / "operations.md").read_text()
        combined = " ".join((skill + operations).split()).lower()
        for field in (
            "initial_owner:",
            "owner_selection_reason:",
            "owner_escalations:",
            "owner_switches:",
            "reviewer_count:",
            "worker_count:",
        ):
            self.assertIn(field, combined)
        self.assertIn("`reviewer_count` excludes workers", combined)
        self.assertIn("`worker_count` excludes the owner and reviewer", combined)
        self.assertIn("a reviewer is not an owner switch or owner escalation", combined)
        self.assertIn("including a spawned terra owner", combined)
        self.assertIn("no analytics subsystem", combined)

        self.assertIn("| Terra selected owner | `--check --check-role terra` |", operations)
        self.assertIn(
            "Role: Luna bounded worker | Terra selected owner | Terra expert specialist",
            (REFERENCES / "role-contracts.md").read_text(),
        )
        self.assertIn(
            "not-applicable for a selected owner",
            (REFERENCES / "role-contracts.md").read_text(),
        )

    def test_artifact_handoff_contract_is_evidence_addressed(self):
        skill = (SKILL / "SKILL.md").read_text()
        contracts = (REFERENCES / "role-contracts.md").read_text()
        combined = skill + contracts
        for field in HANDOFF_FIELDS:
            self.assertIn(field, skill)
            self.assertIn(field, contracts)
        self.assertIn("ARTIFACT HANDOFF", combined)
        for excluded in (
            "chain of reasoning",
            "owner confidence",
            "unnecessary conversation history",
            "lossy summary",
        ):
            self.assertIn(excluded, skill.lower())
        normalized = " ".join(contracts.split()).lower()
        self.assertIn("canonical file and artifact references remain the source of truth", normalized)

    def test_review_loop_is_targeted_and_bounded(self):
        skill = (SKILL / "SKILL.md").read_text()
        contracts = (REFERENCES / "role-contracts.md").read_text()
        operations = (REFERENCES / "operations.md").read_text()
        dry_runs = (REFERENCES / "dry-runs.md").read_text()
        combined = " ".join((skill + contracts + operations + dry_runs).split()).lower()

        self.assertIn("`ship`: terminate review immediately", skill.lower())
        self.assertIn("same owner makes one bounded correction", combined)
        self.assertIn("targeted re-review", combined)
        self.assertIn("affected surface and regression perimeter", combined)
        self.assertIn("initial review plus one correction and one targeted re-review", combined)
        self.assertIn("new material risk or defect class", combined)
        self.assertIn("never run an infinite reviewer loop", skill.lower())

        reviewer_return = contracts[contracts.index("EXACT VERDICT RETURN"):]
        self.assertNotIn("RESULT CHANGED:", reviewer_return)
        self.assertIn("The owner computes review ROI", skill)
        self.assertIn("correction-required=yes` only for `fix-first`", skill)

    def test_legacy_fallback_preserves_seven_strategies(self):
        operations = (REFERENCES / "operations.md").read_text()
        dry_runs = (REFERENCES / "dry-runs.md").read_text()
        self.assertIn("## Legacy fallback", operations)
        self.assertIn("Mode: legacy", dry_runs)
        self.assertIn("selectable, not automatic", dry_runs)
        for strategy in STRATEGIES:
            self.assertIn(f"`{strategy}`", operations)

    def test_native_context_inheritance_contract(self):
        readme = (ROOT / "README.md").read_text()
        skill = (SKILL / "SKILL.md").read_text()
        contracts = (REFERENCES / "role-contracts.md").read_text()
        operations = (REFERENCES / "operations.md").read_text()
        combined = skill + contracts + operations
        normalized = " ".join(combined.split()).lower()

        self.assertIn("Context inheritance:", skill)
        self.assertIn("fork_turns` is a native spawn decision", skill)
        self.assertIn(
            "`none`, a positive integer string `<N>`,\nor `all`", contracts
        )
        self.assertIn("Default to `none`", combined)
        self.assertIn("only when recent turns are materially necessary", combined)
        self.assertIn("rare fallback", combined)
        self.assertIn("reviewer always receives `none`", normalized)
        self.assertIn("defaults to `all` when omitted", normalized)
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
        self.assertIn("every inheritance mode", skill)
        self.assertIn(
            "safety boundary, permission, ownership, invariant",
            " ".join(contracts.split()).lower(),
        )
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
        self.assertIn("CURRENT STATE (authoritative facts)", contracts)
        self.assertIn(
            "never infer, parse private transcripts",
            " ".join(operations.split()).lower(),
        )
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
        self.assertIn("same failure without new evidence", combined)
        self.assertIn("invalidating the architecture", combined)
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
        self.assertIn("full owner/manager transcript", contracts)
        self.assertIn("ORCHESTRA RUN", skill)
        for field in (
            "Mode:",
            "Strategy:",
            "Topology:",
            "Routing:",
            "Owner:",
            "Execution budget:",
            "Verification:",
            "Review:",
            "Result:",
        ):
            self.assertIn(field, skill)
        for field in (
            "Agent invocations:",
            "Retries:",
            "Review ROI:",
            "Parallel ROI:",
            "Handoffs:",
            "Context:",
            "Host metrics:",
        ):
            self.assertIn(field, operations)
        self.assertIn("unavailable/not-exposed", combined)
        self.assertIn("unavailable/not-tracked", combined)
        normalized = " ".join(combined.split()).lower()
        self.assertIn("never infer, parse private transcripts", normalized)
        self.assertIn("duplicate-reference-slots = reference-slots - unique-references", normalized)
        self.assertIn("not token or semantic duplication", normalized)
        for metric in (
            "input_tokens",
            "cached_input_tokens",
            "output_tokens",
            "reasoning_tokens",
            "tool_calls",
            "duration",
        ):
            self.assertIn(metric, combined)

    def test_telemetry_describes_actual_topology_and_roi(self):
        skill = (SKILL / "SKILL.md").read_text()
        operations = (REFERENCES / "operations.md").read_text()
        combined = " ".join((skill + operations).split()).lower()
        self.assertIn("owner-only means zero workers/reviewers", combined)
        self.assertIn("terra owner still counts as one spawned agent invocation", combined)
        for field in (
            "review roi: invoked=",
            "material-issues=",
            "result-changed=",
            "correction-required=",
            "parallel roi: used=",
            "independent-tasks=",
            "unique-useful-outputs=",
        ):
            self.assertIn(field, combined)
        self.assertIn("host token/context metrics are included only when directly exposed", combined)

    def test_dry_runs_cover_all_strategies_and_packets(self):
        dry_runs = (REFERENCES / "dry-runs.md").read_text()
        for strategy in STRATEGIES:
            self.assertIn(f"Strategy: {strategy}", dry_runs)

        self.assertIn("No worker, manager, or reviewer is spawned", dry_runs)
        self.assertIn("5 independent adapter/test deliverables", dry_runs)
        self.assertIn("Independent review: yes", dry_runs)
        self.assertIn("fork_turns: none", dry_runs)
        self.assertIn("smallest discriminating", dry_runs.lower())
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
        self.assertIn("Reason: the self-contained packet is sufficient", scenarios["A"])
        self.assertIn(expected_boundary, scenarios["A"])

        self.assertIn("Specialist mode: `fork_turns: none`", scenarios["B"])
        self.assertIn("Reviewer mode: `fork_turns: none`", scenarios["B"])
        self.assertIn("fresh evidence-only review", scenarios["B"])
        self.assertIn("full\nowner/manager transcript", scenarios["B"])

        self.assertIn('Mode: `fork_turns: "3"`', scenarios["C"])
        self.assertIn("last `3` turns", scenarios["C"])
        self.assertIn("Inherited turns cannot supply a", scenarios["C"])

        self.assertIn("Mode: `fork_turns: all`", scenarios["D"])
        normalized_d = " ".join(scenarios["D"].split())
        with self.subTest(document="dry-runs.md scenario D"):
            self.assertIn(
                "complete user-confirmed multi-turn decision transcript is the explicit authoritative artifact",
                normalized_d,
            )
            self.assertIn("transcript artifact address", normalized_d)
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

        reviewer_start = contracts.index("After owner verification, spawn exactly:")
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
