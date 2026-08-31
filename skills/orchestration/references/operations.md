# Native operations

This reference operates Orchestra's policy on native Codex agents. There is no custom
router service, state machine, token estimator, or manager agent. In `adaptive-v2`, the
primary Sol / High session is the Router and final acceptor. The Router selects one
execution graph containing the initial owner, topology, and review requirement. It is
immutable between explicit escalation gates and otherwise executes without reselection.

## Deterministic adaptive-v2 routing

Evaluate owner signals and topology independently. Safety gates override economy.

### Initial-owner signals

The Router records only qualitative signals needed for the owner decision:

| Signal | Values and meaning |
|---|---|
| Uncertainty | `low`, `medium`, or `high` confidence in the task framing and expected path |
| Risk / blast radius | `low`, `medium`, or `high` impact if the interpretation or change is wrong |
| Verifiability | `objective`, `partial`, or `low` strength of tests, oracle, or acceptance evidence |
| Task nature / reasoning | `mechanical/bounded`, `reasoning-heavy architecture/problem-framing`, or `mixed` |

Complexity remains a low/medium/high telemetry field only; it never selects the owner.
Do not add numeric scoring, numeric thresholds, keyword rules, or another owner signal.

The exact initial-owner rule is:

- `Terra` requires all of: low uncertainty, low/medium risk or blast radius,
  high/objective verifiability, and mechanical/bounded task nature.
- `Sol` is selected for high uncertainty, reasoning-heavy architecture/problem-framing,
  high cost of a wrong interpretation, or high risk with less-than-high verifiability.
- Mixed or unresolved signals conservatively fall back to `Sol`.

Owner selection does not inspect decomposability, parallelism, strategy, or review need.
Those are separate dimensions of the same immutable graph.

### Topology and review graph

The selected Strategy executes this graph and cannot reselect the owner, parallelism, or
review requirement.

| Observable condition | Topology | Non-owner calls | Manager |
|---|---|---:|---|
| Connected work; low/medium risk; one evolving surface | `owner-only` | 0 | no |
| Connected high-risk work or explicit independent-review request | `owner-review` | 1 fresh reviewer after owner verification | no |
| At least two independent deliverables, non-overlapping ownership, no required intermediate dependency | `orchestrated-parallel` | one per justified lane | yes, for decomposition/synthesis |
| Named expertise/context boundary with a concrete unique deliverable | `owner-specialist` | 1 specialist by default | no |
| Dynamic decomposition, multi-lane synthesis, or unresolved routing ambiguity | `manager` | only justified lanes | yes |
| Decomposable but sequentially dependent/shared surface | `owner-only` | 0 | no |

`Non-owner calls` counts workers and reviewers, not the selected owner. A Terra
`owner-only` run therefore has zero non-owner calls but one spawned owner invocation.

Classify complexity as low/medium/high for telemetry, but do not route to a worker only
because complexity is high. Risk is high when failure can materially affect
privacy/security, protected data, irreversible operations, auth, payments/financial
correctness, destructive migrations, critical invariants, or another user-defined
high-impact boundary.

Parallelizable means all are true:

1. At least two deliverables can be accepted independently.
2. Ownership does not overlap.
3. No lane needs another lane's intermediate result.
4. Integration is smaller than the independent work.
5. Each lane has a specific expected information value.

If any condition fails, do not create fake parallelism. Sequential research,
implementation, tests, and correction stay with one owner.

A specialist call must name the expertise/context advantage and unique expected output.
Generic complexity, spare agent capacity, or the desire to "double check" are not
sufficient.

Review is selected independently from the owner and never replaces it. Parallelism is
selected independently from the owner and must preserve the genuine-parallel path when
deliverables, ownership, and dependencies are truly independent.

## Legacy fallback

`legacy` preserves the v0.4 selection behavior and all seven strategies:

- `solo`: Sol implements and verifies.
- `delegate`: one bounded Luna lane, then Sol verification.
- `expert`: one Terra lane for complex/high-risk work, then Sol verification.
- `parallel`: independent non-overlapping lanes, then Sol synthesis.
- `explore`: distinct hypotheses/evidence scopes, then Sol arbitration.
- `plan-execute`: architecture freezes before optional Luna execution.
- `diagnose-fix`: reproduce, evidence, hypothesis, experiment, causal fix, regression.

The `review` and `parallel` modifiers remain available. Legacy does not weaken context,
retry, permission, review, or terminal gates. Select it explicitly for compatibility or
a controlled comparison; never silently switch modes mid-run.

## Role pins and preflight

| Role type | Model | Effort | Use |
|---|---|---|---|
| orchestra_luna_implementer | gpt-5.6-luna | max | Bounded specialist/mechanical lane |
| orchestra_terra_implementer | gpt-5.6-terra | high | Selected Terra owner, judgment-heavy specialist, or complex independent lane |
| orchestra_sol_reviewer | gpt-5.6-sol | high | Fresh independent review; requests read-only sandbox |

Select native context inheritance explicitly:

~~~text
agent_type: orchestra_luna_implementer | orchestra_terra_implementer | orchestra_sol_reviewer
fork_turns: none | <positive integer string N> | all
~~~

The interface defaults to `all` when omitted, so omission is forbidden. Default to
`none`; use `<N>` only for materially necessary recent turns. Use `all` only as a rare
fallback when reconstruction is unsafe because the exact full interaction history is
itself an explicitly addressed authoritative artifact that cannot be safely
paraphrased. Every packet still records every safety and scope boundary; inherited
turns are supplementary context only, and no unrecorded constraint may control an
allowed action. Independent review is always `none`.

Preflight only selected role types:

| Selected auxiliary | Required check |
|---|---|
| Sol owner-only | none |
| Terra selected owner | `--check --check-role terra` |
| Any Luna lane | `--check --check-role luna` |
| Any Terra lane | `--check --check-role terra` |
| Independent review | `--check --check-role sol` |

Run checks from the repository or resolve the installer relative to the installed
skill:

~~~sh
sh scripts/install-agents.sh --check --check-role luna
sh scripts/install-agents.sh --check --check-role terra --check-role sol
~~~

Public spawn/details metadata is authoritative for role and exposed model/effort. If
model or effort is omitted, inspect the exact native thread ID:

~~~sh
sh scripts/inspect-agent-runtime.sh <native-subagent-thread-id>
~~~

Missing, conflicting, unavailable, or unobservable evidence stops that lane; never
substitute a role.

## Installation and update

Plugin installation does not register user-owned companion TOMLs. Install or verify
them separately:

~~~sh
sh scripts/install-agents.sh
sh scripts/install-agents.sh --check
~~~

After a profile-changing update:

~~~sh
sh scripts/install-agents.sh --update
sh scripts/install-agents.sh --check
~~~

The installer is fail-closed, validates identity, refuses foreign or unsafe files,
checks for concurrent change, and keeps backups for replaced recognized profiles.

## Context and handoff operations

Before a Terra-owner or worker packet, verify:

1. A worker/specialist call has stated expected information value; a selected-owner call
   instead records the owner-selection reason.
2. Paths, symbols, ranges, commands, and evidence are task-relevant.
3. Settled facts replace transcript narration.
4. Allowed scope is exact and non-overlapping.
5. `DO NOT RESEARCH` prevents duplicate exploration.
6. The lane can verify its deliverable without reopening the repository.
7. `fork_turns` is explicit and any non-`none` reason is material.

Before review or a downstream lane, create `ARTIFACT HANDOFF` using the exact contract
in `role-contracts.md`. Send canonical addresses, not copied artifacts or owner
reasoning. The receiver follows this context ladder:

1. Handoff.
2. Targeted canonical file/artifact reads.
3. Compact expansion for one named missing fact.
4. Full historical context only under the rare strict `all` gate.

Do not impose hard token caps. When a soft budget is exposed, use it to reconsider
topology, duplicate references, and expansion—not to kill sound reasoning.

## Owner verification and integration

Worker reports and handoffs are claims. The owner inspects actual files, the complete
relevant diff, changed-file scope, requested checks, and runtime/artifact evidence.
Parallel synthesis belongs to the manager/owner and must preserve every lane's safety
boundary.

For `diagnose-fix`, keep reproduction and the discriminating experiment in final
evidence. For `plan-execute`, freeze architecture before delegation; new architecture
returns control to the owner.

## Review loop operations

1. Owner verifies the change and creates an evidence-only ARTIFACT HANDOFF.
2. Fresh reviewer uses `fork_turns: none` and receives the original task contract,
   acceptance criteria, constraints, exact diff/evidence, and minimum source addresses.
3. `ship` terminates immediately.
4. `rethink` stops corrections and returns to architecture/user.
5. `fix-first` permits one bounded correction by the same owner.
6. Owner re-verifies and sends a new fresh reviewer a targeted re-review packet. The
   affected surface and regression perimeter are checked before broader context.
7. A third review cycle is allowed only when correction evidence reveals a new material
   risk/defect class. Otherwise stop; repeated wording or summary drift is not a new
   class.

Do not use a new reviewer merely to reset the loop. Any correction invalidates the old
verdict. The owner never sends self-confidence, a desired verdict, or conclusion-framed
reasoning.

## Sticky owner and explicit escalation

The initial owner owns research, execution, tests, correction, and verification for the
run. Strategy and executor follow the Router-selected graph; neither may silently
override its owner, topology, or review requirement. If `Terra` is the initial owner,
primary Sol remains Router/final acceptor and does not duplicate Terra's implementation
lane.

Open the owner-escalation gate only for materially higher uncertainty, an
architectural/strategic fork, an unexpected high-risk blast radius, invalidated original
framing, or the owner's inability to continue confidently. Encode the takeover as an
evidence-addressed handoff:

~~~text
Terra -> evidence-addressed ARTIFACT HANDOFF -> Sol takeover
~~~

The handoff identifies the exact evidence, preserved work, and unresolved decision.
After takeover Sol remains owner. There is no automatic downgrade or oscillation. Sol to
Terra is permitted only as bounded worker delegation for a large, isolated,
low-uncertainty mechanical workload when its benefit exceeds handoff overhead; Sol
remains owner, and this is neither escalation nor an owner switch.

## Retry, escalation, and checkpoints

- One corrected Luna retry at most for a specification defect.
- A Terra owner may use only the evidence-addressed Terra-to-Sol takeover above; no
  automatic owner downgrade or oscillation is allowed.
- Sol-to-Terra is bounded worker delegation only and does not change ownership.
- Same failure without new evidence stops.
- Invalidated architecture returns `rethink`.
- Route changes require a new `SELECTIVE ROUTE` naming the new evidence.

Emit `STRATEGIC CHECKPOINT` for repeated no-progress correction, invalidated core
assumption, oscillation, or architectural mismatch. The next step must materially
change hypothesis, architecture, decomposition, verification method, or evidence-backed
route. Never use a checkpoint to bypass review, permissions, or acceptance gates.

## Read-only reviewer interpretation

- Observed read-only sandbox: isolation is enforced.
- Broader host policy: continue only when hard isolation is not required, the prompt
  forbids edits, and exact before/after state is captured.
- Unobservable isolation, required hard isolation, or mutation: stop review and do not
  claim read-only isolation.

## Honest telemetry and context-duplication proxy

Record the `ORCHESTRA RUN` template from `SKILL.md`. Counts must describe the actual
topology: owner-only means zero workers/reviewers, while a Terra owner still counts as
one spawned agent invocation. Preserve separate telemetry for `initial_owner`,
`owner_selection_reason`, `owner_escalations`, `owner_switches`, `reviewer_count`, and
`worker_count`.

For handoffs, count each file/artifact/evidence address occurrence as one
`reference-slot`. Normalize exact repeated addresses to count `unique-references`.
When both are measured:

~~~text
duplicate-reference-slots = reference-slots - unique-references
~~~

This is a narrow structural proxy. It does not measure repeated prose, semantic
duplication, tokens, or savings. Handoff chars, targeted reads, repeated reads, and
expansions are reported only when the exact payload/tool evidence makes them
observable; otherwise use `unavailable/not-tracked`.

Review ROI records invocation reason, cycles, material issues, whether the result
changed, and whether correction was required. The owner derives `result-changed=yes`
only when review causes correction, rethink, or a different terminal decision, and
`correction-required=yes` only from `fix-first`; the context-clean reviewer never
compares against an owner conclusion it did not receive. Parallel ROI records why work
was parallelized, independent task count, and unique useful outputs. Do not infer value
from agent count alone. A reviewer is not an owner switch or owner escalation; reviewer
and worker counts exclude the owner.

Host token/context metrics are included only when directly exposed: input, cached
input, output, reasoning tokens, tool calls, and duration. Otherwise write
`unavailable/not-exposed`; never infer, parse private transcripts, or build a workaround.

## Maintainer verification

From the canonical repository root:

~~~sh
python3 -m unittest discover -s tests -v
sh scripts/install-agents.sh --check
sh -n scripts/install-agents.sh
sh -n scripts/inspect-agent-runtime.sh
git diff --check
git status --short
git diff --stat
~~~

For pre-install validation without mutating user configuration, install profiles to a
temporary target directory and compare exact files. Verify source, marketplace copy,
installed cache, and Codex plugin listing separately; a source pass is not installation
proof.
