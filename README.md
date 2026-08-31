# Orchestra

Orchestra is an adaptive orchestration plugin for Codex. Its default `adaptive-v2`
mode is single-agent-first: one sticky initial owner (`Sol` or `Terra`) keeps connected
research, implementation, tests, correction, and verification in one lane. Primary Sol /
High is the Router and final acceptor for every graph without duplicating that lane.
Additional agents are used only for mandatory independent review, true parallelism, or
a named specialist/context advantage.

The previous v0.4 strategy-first behavior remains selectable as `legacy` for
compatibility and controlled comparison.

## Routing principles

1. Agent count is not a quality metric; one owner is a valid Orchestra result.
2. Every additional call must have expected information value.
3. Multi-agent topology is for independent review, true parallelism, or meaningful
   specialization.
4. Sequentially coupled coding work usually stays with one owner.
5. Orchestra optimizes quality, safety, cost, latency, and context duplication—not only
   tokens.
6. Required review and verification are never removed merely to save resources.

The Router applies qualitative owner signals and a separate topology/review decision
before tools. It classifies uncertainty, risk/blast radius, verifiability, task nature /
reasoning requirement, complexity, decomposability, parallelizability,
independent-review need, and manager need. Obvious cases do not use another LLM just for
classification.

Initial owner is `Terra` only when uncertainty is low, risk/blast radius is low or
medium, verifiability is high/objective, and the task is mechanical/bounded. `Sol` is
the conservative choice for high uncertainty, reasoning-heavy architecture or
problem-framing, high cost of a wrong interpretation, high risk with less-than-high
verifiability, or mixed/unresolved signals. Complexity is telemetry only and never
selects the owner; owner selection is independent from topology and review.

| Task shape | Default topology |
|---|---|
| Simple or connected standard work | `owner -> verification -> stop` |
| High-risk work | `owner -> artifact handoff -> independent reviewer -> gate` |
| Truly independent deliverables | `orchestrator -> workers -> synthesis` |
| Named expertise/context boundary | `owner -> bounded specialist -> owner verification` |
| Dynamic decomposition/synthesis | conditional manager topology |

High risk includes privacy/security, protected data, irreversible operations, auth,
payments or financial correctness, destructive migrations, critical invariants, and
explicit user requests for independent review.

## Strategies and legacy fallback

The existing strategies remain stable:

| Strategy | Delivery model |
|---|---|
| `solo` | The selected initial owner owns and verifies the connected task. |
| `delegate` | Bounded Luna lane when it has a concrete specialist advantage. |
| `expert` | Terra lane for a named judgment-heavy specialist boundary. |
| `parallel` | Independent, non-overlapping lanes; the selected owner synthesizes. |
| `explore` | Distinct hypotheses/evidence scopes; the selected owner arbitrates. |
| `plan-execute` | Architecture freezes before optional mechanical delegation. |
| `diagnose-fix` | Reproduce, evidence, experiment, causal fix, regression verify. |

In `adaptive-v2`, connected work stays `solo` even when it is medium or high complexity;
complexity alone does not justify delegation or change owner. Strategy executes the
Router-selected immutable graph and cannot reselect owner, parallelism, or review. In
`legacy`, v0.4 behavior remains available: Sol manages, Luna/Terra implements selected
work, Sol verifies, and fresh Sol review composes as a modifier. Fallback is explicit,
never silent.

The initial owner is sticky. If Terra cannot continue because materially higher
uncertainty, an architectural/strategic fork, unexpected high-risk blast radius,
invalidated framing, or inability to continue confidently appears, the only takeover is
`Terra -> evidence-addressed ARTIFACT HANDOFF -> Sol takeover`; Sol then remains owner.
Sol-to-Terra is only bounded worker delegation for a large, isolated, low-uncertainty
mechanical workload whose benefit exceeds handoff overhead, so it is neither escalation
nor an owner switch.

## Artifact handoff and context discipline

Reviewers and downstream workers receive an evidence-addressed ARTIFACT HANDOFF:

```text
objective
acceptance criteria
hard constraints
changed files
diff references
test / verification results
created artifacts
important invariants
unresolved risks
exact questions for next agent
```

The handoff is an index into canonical files and artifacts, not a replacement for them.
It excludes chain of reasoning, owner confidence, proposed verdicts, unnecessary
conversation history, and repeated repository summaries. The receiver starts with the
handoff, performs targeted reads, requests compact expansion only when needed, and uses
full history only as a rare last resort.

Native `fork_turns` is always explicit: `none` by default, limited `N` only for
materially necessary recent turns, and `all` only when the exact full interaction
history is itself an explicitly addressed authoritative artifact that cannot be safely
paraphrased. Every packet still records all safety/scope boundaries; no unrecorded
constraint may control an allowed action, and inherited turns are supplementary
context only. Reviewers always use `none`.

## Independent review loop

A fresh Sol / High reviewer gets the original task contract, acceptance criteria,
constraints, exact diff/evidence, minimum source addresses, and the artifact handoff—
not the owner's confidence or desired verdict.

- `ship`: terminate immediately.
- `rethink`: return to architecture or the user.
- `fix-first`: the same owner makes one bounded correction, re-verifies, and sends a
  new fresh reviewer a targeted re-review of the affected surface and regression
  perimeter.

The default maximum is initial review plus one correction and one targeted re-review.
One extra cycle requires a newly exposed material defect class; otherwise Orchestra
stops instead of creating an infinite review loop.

## Honest telemetry

The terminal `ORCHESTRA RUN` records actual mode, strategy, topology, owner signals,
`initial_owner`, `owner_selection_reason`, `owner_escalations`, `owner_switches`,
`reviewer_count`, `worker_count`, spawned-agent count (including a spawned Terra owner),
roles, retries, review ROI,
parallel ROI, handoff/context proxies, result, and verification. Review is independent
from owner selection and never replaces the owner or counts as escalation.

Review ROI records why review ran, cycles, material issues, whether the result changed,
and whether correction was required. Parallel ROI records why work was parallelized,
independent task count, and unique useful outputs.

Context duplication uses a narrow structural proxy: total handoff reference slots minus
unique normalized references. This is not token or semantic duplication. Exact token,
cache, reasoning, tool-call, duration, and handoff-size metrics are reported only when
the host exposes or directly measures them; otherwise they are
`unavailable/not-exposed` or `unavailable/not-tracked`. Orchestra never invents token or
cost savings.

## Roles

- **Sol / High Router and final acceptor** selects the graph and owns a run when Sol is
  the selected initial owner.
- **Luna / Max** executes bounded, frozen specialist work.
- **Terra / High** owns a run when the exact mechanical/bounded Terra rule holds, or
  handles a bounded specialist/worker lane.
- **Fresh Sol / High reviewer** independently returns `ship`, `fix-first`, or `rethink`
  in a requested read-only sandbox.

No new roles or runtime infrastructure are introduced by adaptive-v2.

## Installation

Install the plugin through the normal local Codex plugin workflow. Companion profiles
are user-owned configuration and are installed separately:

```sh
sh scripts/install-agents.sh
sh scripts/install-agents.sh --check
```

After an update that changes profiles, synchronize only recognized Orchestra profiles
with recoverable backups:

```sh
sh scripts/install-agents.sh --update
sh scripts/install-agents.sh --check
```

Start a new Codex task on GPT-5.6 Sol with high reasoning, then invoke:

```text
Use $orchestra:orchestration to choose a topology, execute this task, and verify it.
```

The skill cannot switch the already-running primary model.

## Development and verification

```sh
python3 -m unittest discover -s tests -v
sh scripts/install-agents.sh --check
sh -n scripts/install-agents.sh
sh -n scripts/inspect-agent-runtime.sh
git diff --check
```

The contract suite covers adaptive routing, high-risk review, real parallelism, no fake
parallelism, bounded targeted re-review, artifact handoff, legacy fallback, telemetry,
role pins, context inheritance, installer safety, and all seven strategies.

Orchestra is released under the MIT License. The original role and safety tooling are
adapted from [Sol Advisor](https://github.com/DannyMac180/sol-advisor) v0.6.0; see
[NOTICE.md](NOTICE.md) for attribution.
