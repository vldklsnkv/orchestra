---
name: orchestration
description: "Adaptive single-agent-first Codex orchestration with scoped specialists, artifact handoffs, and independent review."
---

# Orchestra Orchestration

Act as the primary Sol / High owner by default when Sol is the selected initial owner;
the primary session is also the Router and final acceptor. The Router selects one
execution graph containing the initial owner (`Sol` or `Terra`), the
solo/parallel topology, and the review requirement. The selected initial owner owns the
run's research, execution, tests, correction, and verification. Spawn the existing Terra
role when Terra is selected; add a non-owner agent only when the graph requires expected
information value from independent review, true parallelism, or a named
specialist/context boundary. Agent count is not a quality metric.

Read [references/role-contracts.md](references/role-contracts.md) before the first
delegation or review. Use [references/operations.md](references/operations.md) for the
adaptive decision table, spawn/preflight, context proxies, isolation, and maintainer
procedures. Use [references/dry-runs.md](references/dry-runs.md) as policy validation
examples, not task-specific policy.

## Confirm the primary session

Run the primary Codex session on gpt-5.6-sol with high reasoning. Verify model and
effort when runtime metadata exposes them. If either differs, tell the user to select
Sol / High and stop before delegation. If an auxiliary is selected and metadata omits
either field, ask the user to confirm Sol / High and stop until confirmed. A skill
cannot change the primary model; never claim that it did.

## Choose the mode and route before tools

`adaptive-v2` is the default. `legacy` preserves the v0.4 strategy-first worker routing
for compatibility and controlled comparison. Use `legacy` only when the user selects
it or an existing workflow explicitly depends on it; never silently fall back.

Before the first task tool call, classify the task without spawning a manager:
owner signals (uncertainty, risk/blast radius, verifiability, and task nature/reasoning),
complexity, decomposability, parallelizability, and need for independent review. For
obvious cases, apply the deterministic decision table in `operations.md`; do not
call an LLM merely to classify them.

Emit one short declaration:

~~~text
SELECTIVE ROUTE
Mode: adaptive-v2 | legacy
Strategy: solo | delegate | expert | parallel | explore | plan-execute | diagnose-fix
Topology: owner-only | owner-review | owner-specialist | orchestrated-parallel | manager
Uncertainty: low | medium | high
Risk: low | medium | high
Verifiability: objective | partial | low
Task nature: mechanical/bounded | reasoning-heavy architecture/problem-framing | mixed
Complexity: low | medium | high (telemetry only)
Decomposable: no | yes (<independent deliverables>)
Parallelizable: no | yes (<why dependencies are minimal>)
Independent review: no | yes (<mandatory trigger or expected value>)
Manager: no | yes (<dynamic decomposition, synthesis, or unresolved routing reason>)
Initial owner: Sol | Terra
Owner reason: <compact evidence-based reason>
Additional agent value: none | <specific new evidence, review, or specialist advantage>
Context inheritance: none | limited <N> | all (rare)
Inheritance reason: <required for limited <N> or all; otherwise none>
~~~

No task tool may precede this declaration. A later declaration may change routing only
when new evidence justifies it; record that evidence. Never silently downgrade risk or
substitute a mode, role, model, effort, review policy, inheritance policy, or initial
owner. The graph is immutable between explicit escalation gates. Strategy and executor
execute it; they do not reselect owner, topology, or review.

## Adaptive-v2 decision order

Initial-owner selection is qualitative and deterministic. It is independent from
decomposability, parallelism, strategy, and review selection; no score, numeric
threshold, or keyword rule is used:

- Select `Terra` only when all of these hold: low uncertainty, low/medium risk or blast
  radius, high/objective verifiability, and mechanical/bounded task nature.
- Select `Sol` when uncertainty is high, the task is reasoning-heavy
  architecture/problem-framing, the cost of a wrong interpretation is high, or risk is
  high with less-than-high verifiability.
- Resolve any mixed or unresolved signals conservatively to `Sol`.

1. Apply safety and permission gates. High risk never loses required review to save
   cost, latency, or context.
2. Independently select topology and review. If the result is high risk, choose `owner-review`:
   `owner -> artifact handoff -> independent reviewer -> gate`.
3. Otherwise, if work is sequentially coupled or shares one evolving implementation
   surface, choose `owner-only`: `owner -> verification -> stop`.
4. Choose `orchestrated-parallel` only for at least two independent deliverables with
   non-overlapping ownership and no required intermediate dependency.
5. Choose `owner-specialist` only when a named expertise or context boundary is likely
   to produce information the owner cannot obtain comparably in the hot path.
6. Choose `manager` only for genuinely dynamic decomposition, synthesis of independent
   workers, or routing ambiguity that the deterministic table cannot resolve.

One agent is a valid Orchestra result. A connected medium task remains with one owner;
do not split research, implementation, tests, and correction among sequential agents.

## Mandatory independent review

Set `Independent review: yes` for privacy/security, protected data, irreversible or
destructive operations, auth, payments or financial correctness, destructive
migrations, critical invariants, or an explicit user request for independent review.
Review may also be selected for a wide blast radius when its expected information value
is stated. Do not add review by habit to low-risk work.

Review is a graph dimension independent from initial owner selection and never replaces
the owner or counts as owner escalation. Parallelism is another independent dimension;
preserve the genuine-parallel path when its non-overlap and dependency conditions hold.

## Seven legacy-compatible strategies

The strategies remain available in both modes; adaptive-v2 changes their selection
frequency and keeps connected work `solo` by default. Strategy is the execution recipe
for the Router-selected graph; it cannot reselect the initial owner, topology, or review.

- `solo`: the selected initial owner implements and verifies; no implementation worker.
  Mandatory independent review may still add the `owner-review` topology.
- `delegate`: legacy bounded Luna implementation after Sol freezes the specification.
- `expert`: legacy Terra implementation for judgment-heavy or high-risk work.
- `parallel`: independent non-overlapping lanes with selected-owner synthesis.
- `explore`: distinct hypotheses or evidence scopes with selected-owner arbitration.
- `plan-execute`: settle architecture, then optionally delegate frozen mechanical work.
- `diagnose-fix`: reproduce, evidence, hypothesis, smallest discriminating experiment,
  causal fix, and regression verification.

In adaptive-v2, `delegate` and `expert` are exceptions requiring a concrete specialist
advantage; complexity alone does not force the connected implementation away from the
owner. Luna failure is not required before Terra when a specialist lane is justified.
Do not jump to a speculative fix while root cause remains unestablished.

## Sticky owner and explicit takeover

The initial owner remains sticky for research, execution, tests, correction, and
verification for the run. A Strategy, executor, reviewer, or optional worker cannot
silently override that owner. When `Terra` is the initial owner, primary Sol remains the
Router/final acceptor and verifies the handoff; Sol does not duplicate Terra's
implementation lane.

Only an evidence-backed owner escalation may change ownership. A materially higher
uncertainty, an architectural/strategic fork, an unexpected high-risk blast radius,
invalidated original framing, or the owner's inability to continue confidently opens the
gate. The only owner takeover is:

~~~text
Terra -> evidence-addressed ARTIFACT HANDOFF -> Sol takeover
~~~

The handoff must identify the evidence and unresolved decision. After takeover, Sol
remains owner; there is no automatic downgrade or oscillation. Sol may delegate to Terra
only as a bounded worker for a large, isolated, low-uncertainty mechanical workload when
the benefit exceeds handoff overhead; Sol remains owner, and this is neither escalation
nor an owner switch.

## Native context and worker packets

`fork_turns` is a native spawn decision, never an omitted default: choose exactly
`none`, a positive integer string `<N>`, or `all`. Default to `none`. Choose limited
`<N>` only when recent turns are materially necessary. Use `all` only as a deliberate
rare fallback when reconstruction is unsafe because the exact full interaction history
is itself an explicitly addressed authoritative artifact that cannot be safely
paraphrased. Independent review always uses `none`.

Every Luna worker and every Terra selected owner or specialist receives the compact
Context Packet defined in `role-contracts.md`:

~~~text
ROLE
OBJECTIVE
CURRENT STATE (authoritative facts)
CONSTRAINTS / INVARIANTS
ALLOWED SCOPE
FORBIDDEN ACTIONS
RELEVANT FILES / ARTIFACTS
EXPECTED OUTPUT / VERIFICATION
STOP / ESCALATION
~~~

For every inheritance mode, the packet is the complete authoritative safety and scope
boundary. Inherited turns are supplementary context only: they never supply or replace
a missing permission, ownership boundary, invariant, acceptance criterion, settled
fact, or other safety constraint. No unrecorded constraint may control an allowed
action.

## Artifact handoff

Before review or a downstream lane, create an evidence-addressed handoff:

~~~text
ARTIFACT HANDOFF
Objective: <observable outcome>
Acceptance criteria: <checks the next agent must apply>
Hard constraints: <safety, compatibility, permission, and scope boundaries>
Changed files: <exact paths, or none>
Diff references: <base/head, patch, symbols, or ranges>
Test / verification results: <exact commands and observed results>
Created artifacts: <canonical paths/IDs/hashes, or none>
Important invariants: <must remain true>
Unresolved risks: <known unknowns, or none>
Exact questions for next agent: <bounded questions>
~~~

Do not include chain of reasoning, owner confidence, a proposed reviewer verdict,
unnecessary conversation history, or a lossy summary in place of canonical artifacts.
The next agent uses the handoff, targeted file/artifact reads, compact expansion when
needed, and full history only as the rare last resort above.

## Independent review and bounded loop

With `Independent review: yes`, the owner first verifies the actual diff, changed-file
scope, tests, and artifacts. Then spawn a fresh Sol / High reviewer with
`fork_turns: none`. Give it the original task contract, acceptance criteria,
constraints, ARTIFACT HANDOFF, exact diff/evidence, and minimum source addresses. Never
anchor it with the owner's confidence, reasoning, or desired verdict.

The reviewer returns exactly `ship`, `fix-first`, or `rethink` and never implements.

- `ship`: terminate review immediately.
- `rethink`: stop local correction and return to architecture or the user.
- `fix-first`: the same owner makes one bounded correction, re-verifies, and sends a
  fresh reviewer a targeted re-review handoff covering the affected surface and
  regression perimeter first.

The default maximum is the initial review plus one correction and one targeted
re-review. One additional cycle is allowed only when the previous correction exposes a
new material risk or defect class; record that new evidence. Otherwise stop with
`rethink` or a strategic checkpoint. Never run an infinite reviewer loop.

## Stop, retry, and escalate deliberately

Luna must return `WORKER STOP` when it discovers an architectural choice, material
ambiguity, wider scope, judgment-heavy decision, high-risk invariant, or systemic
verification problem outside ownership.

- A specification defect allows at most one corrected Luna retry.
- Misclassified bounded work may escalate directly to Terra; no Luna retry is required.
- The same failure without new evidence stops.
- Evidence invalidating the architecture returns `rethink`.
- Continue only while a pass adds evidence, reduces uncertainty, or completes bounded
  work.

When stagnation is evidenced, emit:

~~~text
STRATEGIC CHECKPOINT
Trigger: <repeated failure or invalidated assumption>
Preserved: <completed work and reusable evidence>
Invalidated: <failed approach>
Next step: <materially different bounded action>
Success signal: <evidence required to continue>
~~~

## Context discipline and telemetry

Do not impose crude token caps. Minimize duplicated context with compact handoffs,
targeted reads, lazy expansion, explicit `fork_turns`, and terminal evidence gates. A
soft budget, when exposed, triggers topology/context review rather than automatic
termination of useful reasoning.

At completion or stop, emit only observable facts:

~~~text
ORCHESTRA RUN
Mode: adaptive-v2 | legacy
Strategy: <base strategy>
Topology: <selected topology>
Routing: uncertainty=<level>; risk/blast-radius=<level>; verifiability=<objective|partial|low>; task-nature=<mechanical/bounded|reasoning-heavy architecture/problem-framing|mixed>; complexity=<level>; decomposable=<yes/no>; parallelizable=<yes/no>; review-needed=<yes/no>; manager=<yes/no>
Initial owner: <Sol | Terra>
Owner reason: <compact evidence-based reason>
initial_owner: <Sol | Terra>
owner_selection_reason: <compact evidence-based reason>
owner_escalations: <count>
owner_switches: <count>
reviewer_count: <count>
worker_count: <count>
Owner: <Sol | Terra> (current sticky owner)
Agent invocations: <count of spawned agents, including a spawned Terra owner>
Roles: <selected roles, or owner-only>
Retries: <count>
Review ROI: invoked=<yes/no>; reason=<reason/none>; cycles=<count>; material-issues=<count/unavailable>; result-changed=<yes/no>; correction-required=<yes/no>
Parallel ROI: used=<yes/no>; reason=<reason/none>; independent-tasks=<count>; unique-useful-outputs=<count/unavailable>
Handoffs: count=<count>; chars=<count/unavailable>; reference-slots=<count>; unique-references=<count>; duplicate-reference-slots=<count/unavailable>
Context: targeted-reads=<count/unavailable>; repeated-reads=<count/unavailable>; expansions=<count/unavailable>; full-history=<count>
Host metrics: input_tokens=<value> cached_input_tokens=<value> output_tokens=<value> reasoning_tokens=<value> tool_calls=<value> duration=<value> | unavailable/not-exposed
Result: complete | partial | blocked | rethink
Verification: pass | fail | partial (<short evidence>)
~~~

`duplicate-reference-slots = reference-slots - unique-references` is only a handoff
reference-duplication proxy, not token or semantic duplication. Mark unavailable fields
as `unavailable/not-exposed` or `unavailable/not-tracked`; never infer tokens, duration,
cost, or savings, parse private transcripts, or manufacture precision.

The owner fields distinguish the initial Router choice from later evidence-backed
takeover: `owner_escalations` counts only the explicit Terra-to-Sol gate,
`owner_switches` counts actual owner changes, `reviewer_count` excludes workers, and
`worker_count` excludes the owner and reviewer. `Agent invocations` still includes a
spawned Terra owner, so an `owner-only` graph does not falsely report zero runtime calls.
Complexity is telemetry only; it never selects the owner. No analytics subsystem is
introduced.

The owner computes review ROI from observable actions: `result-changed=yes` only when a
review verdict causes correction, rethink, or a different terminal decision;
`correction-required=yes` only for `fix-first`. The independent reviewer is not asked to
compare against an owner conclusion it did not receive.

Orchestra optimizes quality + safety + cost + latency + context duplication. It never
sacrifices required review or verification merely to reduce agent calls.
