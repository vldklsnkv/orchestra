---
name: orchestration
description: "Adaptive single-agent-first Codex orchestration with independent scope, verified context, qualitative budgets, cheap-first verification, scoped specialists, and evidence-driven review/escalation."
---

# Orchestra Orchestration

Act as the primary Sol / High owner by default when Sol is the selected initial owner;
the primary session is also the Router and final acceptor. The Router classifies domain
risk, independent change-scope dimensions, verified-context freshness, owner/model,
strategy, execution budget, verification floor, topology, and review value before
freezing one graph. The graph contains the initial owner (`Sol` or `Terra`), the
solo/parallel topology, the budget, and the review requirement. The selected initial
owner owns the run's research, execution, tests, correction, and verification. Spawn the
existing Terra role when Terra is selected; add a non-owner agent only when the graph
requires expected information value from independent review, true parallelism, or a
named specialist/context boundary. Agent count is not a quality metric.

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

Before the first task tool call, classify risk, all independent scope dimensions, context
freshness, owner/model, strategy, topology, budget, verification floor, and review value;
do not spawn a manager merely to classify an obvious case. Use the deterministic table in
`operations.md`; do not call an LLM merely to classify it.

Emit one short declaration:

~~~text
SELECTIVE ROUTE
Mode: adaptive-v2 | legacy; Strategy: solo | delegate | expert | parallel | explore | plan-execute | diagnose-fix; Topology: owner-only | owner-review | owner-specialist | orchestrated-parallel | manager
Risk: low | medium | high; uncertainty=<low|medium|high>; verifiability=<objective|partial|low>; task=<mechanical/bounded|reasoning-heavy architecture/problem-framing|mixed>
Scope: tiny | small | medium | large; Blast radius: isolated | local | cross-component | systemic; Behavior impact: none | shadow-only | internal | user-visible | data-affecting
Novelty/uncertainty evidence: known architecture | analogous verified path | previous verified iteration | new subsystem/unknown behavior/external dependency; Reversibility: trivial | localized | stateful/migration | destructive/high-cost
Context freshness: fresh | stale | not established; evidence=<minimal proof address or status>
Initial owner: Sol | Terra; Primary: <sticky initial owner/current executor>; Owner reason: <evidence>
Parallel: no | yes (<dependency reason>); Manager: no | yes (<decomposition/synthesis reason>)
Additional agent value: none | <specific review, parallel, or specialist evidence>
Execution budget: FAST | STANDARD | HEAVY
Verification plan: L0 -> L1 -> L2 -> L3; Verification floor: L0 | L1 | L2 | L3
Review value: low | medium | high; Reviewer: none | fresh Sol / High
Escalation condition: <evidence for FAST -> STANDARD -> HEAVY, or none>
Context inheritance: none | limited <N> | all (rare); Inheritance reason: <reason or none>
~~~

No task tool may precede this declaration. The graph is immutable until an explicit,
evidence-addressed escalation; never silently downgrade or reselect mode, role, model,
effort, owner, topology, budget, floor, review, or inheritance. Strategy and executor
execute it; they do not reselect owner, topology, budget, floor, or review. Route updates
use the compact escalation declaration below.

## Independent scope dimensions and verified context

Domain risk (`low|medium|high`) describes the consequence of a wrong change; it is not a
proxy for scope, blast radius, budget, or review. Before graph freeze record `Change size:
tiny|small|medium|large` from files/subsystems, contracts/schema,
`production-vs-diagnostic`, `new-behavior-vs-instrumentation`, and `refactor-vs-additive`
evidence (LOC is never sufficient alone); `Blast radius: isolated|local|cross-component|
systemic`; `Behavior impact: none|shadow-only|internal|user-visible|data-affecting`;
`Novelty/uncertainty evidence: known architecture|analogous verified path|previous
verified iteration|new subsystem/unknown behavior/external dependency`; and
`Reversibility: trivial|localized|stateful/migration|destructive/high-cost`.

### Minimal VERIFIED CONTEXT

Keep this compact record in the current task or handoff, not in a persistent database:

~~~text
VERIFIED CONTEXT
Repo/worktree: <exact repository and worktree path>
Base: <exact HEAD, or proven descendant relationship>
Freshness proof: <same repo/worktree + exact HEAD plus relevant-path worktree/index check showing unchanged, or proven descendant plus relevant-path since-base and current worktree/index checks>
Relevant files: <path identities; hashes only where file identity matters>
Frozen artifacts: <identities/hashes only where artifact identity matters, or none>
Relevant config: <paths/keys; hash/version only where identity matters>
Architecture map/invariants: <canonical addresses and required invariants>
Evidence timestamp/source (optional): <command, task, or handoff; timestamp is supporting only>
Context freshness: fresh | stale | not established
~~~

A minimal freshness proof is cheap but not HEAD alone: same repo/worktree plus exact HEAD
proves source freshness only with a relevant-path worktree/index check showing those paths
unchanged. A proven descendant requires checking relevant-path changes since base plus a
current worktree/index check. Hash only identity-sensitive files, config, or artifacts; do
not hash everything by default. A relevant staged or unstaged path change makes context stale
and forbids reuse; normal preflight resumes. Timestamp or copied prose never proves
freshness; when freshness is proven, do not reread known architecture.

## Adaptive-v2 decision order

Owner choice is qualitative, deterministic, and independent from strategy, topology,
budget, verification, and review; use no score, numeric threshold, or keyword rule. Select
`Terra` only when all of these hold: low uncertainty, low/medium risk, isolated/local blast,
high/objective verifiability, and mechanical/bounded work. `Sol` is selected for high
uncertainty, reasoning-heavy architecture, high cost of a wrong interpretation, high domain
risk or blast radius with less-than-high verifiability, or mixed signals; mixed or unresolved
signals conservatively fall back to `Sol`.

Freeze in this order: (1) safety/permission gates, risk, and all scope dimensions; (2)
freshness and owner/model; (3) one of the seven strategies and topology; (4) budget after
risk, scope, owner, and strategy; (5) verification floor and review value/reviewer. Safety
invariants bind every budget. Connected work stays `owner-only`; a single owner is valid.
One agent is a valid Orchestra result.

## Qualitative execution budgets

Risk controls confidence and required invariants; scope and evidence control machinery, and
no single signal (especially risk or LOC) chooses budget. `FAST` requires tiny/small,
isolated/local, bounded or shadow-only objective work, known architecture, high
reversibility, and fresh sufficient context—even at high risk. `STANDARD` covers medium or
interacting/production-internal work, moderate uncertainty, or focused evidence beyond FAST.
`HEAVY` covers large/systemic or cross-component production work, schema/migration/stateful
or destructive work, substantial architectural uncertainty, or a broad floor. Owner and
review remain independent: medium scope may review without HEAVY, and objective tiny high
risk work may remain FAST without a reviewer.

## Verification ladder and FAST contract

Use the cheapest falsifier first and continue to the floor derived from concrete invariants:
`L0` static sanity/diff/reasoning; `L1` focused test/compile/contract; `L2` targeted
integration/runtime/fixture; `L3` full corpus/build/regression/environments. Acceptance
must reach the floor; FAST never skips L2/L3. Cold or warm infrastructure changes order,
not permission to omit a floor. A cheap pass with an unproven critical invariant continues
to L2/L3.

The explicit FAST contract is:

~~~text
minimal freshness check -> one primary owner/executor -> bounded change -> L0 -> focused L1 -> manager/owner diff acceptance -> done
~~~

This contract ends only when no invariant floor or new evidence escalates it. FAST has no
deep architecture reconstruction, broad corpus, multiple worker roles, reviewer, or heavy
artifact ceremony absent an escalation signal.

## Review value and independent review

`Review value: low|medium|high` is independent from risk. `low` means objective output
identity and focused tests close the information gap; `medium` names one interpretation or
evidence gap; `high` requires an explicit request or material independent value (ambiguity,
plausible interpretations, non-objective verification, high-impact contract/judgment,
adversarial need, or bias risk). High domain risk alone must not force review when objective
focused tests/output identity close the gap; medium scope may use `owner-review` without
HEAVY. Review is mandatory only for an explicit request or a
named safety/contract boundary with high independent information value. Safety and invariant
checks remain mandatory. Review never replaces the sticky owner or counts as escalation;
parallelism requires genuine non-overlap.

## Seven legacy-compatible strategies

The strategies remain available in both modes; adaptive-v2 changes their selection
frequency and keeps connected work `solo` by default. Strategy is the execution recipe
for the Router-selected graph; it cannot reselect the initial owner, topology, or review.

- `solo`: the selected initial owner implements and verifies; an explicit request or named
  safety/contract boundary with high independent value may add `owner-review`.
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
verification; strategy, executor, reviewer, and workers cannot silently override it. If
`Terra` starts, primary Sol remains Router/final acceptor and does not duplicate Terra's
lane. Only evidence of materially higher uncertainty, an architectural/strategic fork,
unexpected risk/blast, invalid framing, or inability to continue opens the owner gate:

~~~text
Terra -> evidence-addressed ARTIFACT HANDOFF -> Sol takeover
~~~

The handoff identifies evidence and the unresolved decision. After takeover Sol remains
owner; there is no automatic downgrade or oscillation. Sol may delegate Terra as a bounded
worker only for a large, isolated, low-uncertainty mechanical workload when benefit exceeds
handoff overhead; Sol remains owner and this is neither escalation nor an owner switch.

## Native context and worker packets

`fork_turns` is a native spawn decision and explicit: choose exactly `none`, a positive
integer string `<N>`, or `all`;
default to `none`, use limited `<N>` only when recent turns are materially necessary, and
use `all` only as the deliberate rare fallback where the exact full interaction history is
itself an explicitly addressed authoritative artifact that cannot be safely paraphrased.
Independent review uses `none`.

Every Luna worker and every Terra selected owner or specialist receives the compact
Context Packet defined in `role-contracts.md`:

~~~text
ROLE
OBJECTIVE
CURRENT STATE (authoritative facts)
VERIFIED CONTEXT
CONSTRAINTS / INVARIANTS
ALLOWED SCOPE
FORBIDDEN ACTIONS
RELEVANT FILES / ARTIFACTS
EXPECTED OUTPUT / VERIFICATION
STOP / ESCALATION
~~~

The packet carries a `VERIFIED CONTEXT` address, compact freshness proof/status, and only
identity-sensitive hashes. If relevant context changed, it says `Context freshness: stale`
and the owner performs normal preflight; a worker never silently reuses an invalid record.

For every inheritance mode, the packet is the complete authoritative safety and scope
boundary. Inherited turns are supplementary context only: they never supply or replace a
missing permission, ownership boundary, invariant, acceptance criterion, settled fact, or
other safety constraint; no unrecorded constraint may control an allowed action.

## Artifact handoff

Before review or a downstream lane, create this evidence-addressed handoff:

~~~text
ARTIFACT HANDOFF
Objective: <observable outcome>
Acceptance criteria: <checks the next agent must apply>
Hard constraints: <safety, compatibility, permission, and scope boundaries>
Changed files: <exact paths, or none>
Diff references: <base/head, patch, symbols, or ranges>
Verified context: <record address, identity-sensitive hashes, freshness proof/status>
Test / verification results: <exact commands and observed results>
Created artifacts: <canonical paths/IDs/hashes, or none>
Important invariants: <must remain true>
Unresolved risks: <known unknowns, or none>
Exact questions for next agent: <bounded questions>
~~~

Do not substitute chain of reasoning, owner confidence, a proposed verdict, unnecessary conversation history,
or a lossy summary for canonical artifacts. The next agent uses this handoff,
targeted reads, compact expansion when needed, and full history only under the rare `all`
gate above.

## Independent review and bounded loop

With `Independent review: yes`, the owner verifies the diff, scope, tests, and artifacts,
then gives a fresh Sol / High reviewer (`fork_turns: none`) the original contract,
handoff, exact evidence, and minimum source addresses—never owner confidence or a desired
verdict. The reviewer never implements and returns exactly `ship`, `fix-first`, or
`rethink`: `ship`: terminate review immediately; `rethink` returns to architecture/user;
`fix-first` permits the same owner to make one bounded correction followed by targeted
re-review of the affected surface and regression perimeter. The default is one review plus
one correction/re-review; one extra cycle requires new material risk or defect class
evidence. Never run an infinite reviewer loop.

## Stop, retry, and escalate deliberately

Luna returns `WORKER STOP` for an architectural choice, material ambiguity, wider scope,
judgment-heavy decision, high-risk invariant, or systemic verification problem outside
ownership. A specification defect allows at most one corrected Luna retry; misclassified
bounded work may go directly to Terra. Same failure without new evidence stops, invalidated
architecture returns `rethink`, and work continues only while it adds evidence, reduces
uncertainty, or completes bounded scope.

Budget escalation is monotonic and evidence-driven: `FAST -> STANDARD -> HEAVY`. Escalate
only for scope expansion, failed verification, invalid assumptions, unexpected behavior,
hidden dependency, flaky/non-deterministic evidence, new worker risk, or an invariant that
cannot be proved cheaply. Do not pre-escalate or silently downgrade. Emit a new route/budget
declaration naming the evidence:

~~~text
ORCHESTRA ROUTE
Evidence: <exact failure, changed scope, dependency, or invariant gap>
Risk: <low | medium | high>; Scope: <tiny | small | medium | large>; Blast radius: <isolated | local | cross-component | systemic>; Behavior impact: <none | shadow-only | internal | user-visible | data-affecting>
Context freshness: <fresh | stale | not established>; Initial owner: <Sol | Terra>; Primary: <sticky owner>
Parallel: <no | yes; reason>; Manager: <no | yes; reason>
Previous execution budget: <FAST | STANDARD | HEAVY>; Execution budget: <STANDARD | HEAVY>
Verification plan: <levels>; Verification floor: <L0 | L1 | L2 | L3>; Verification change: <minimum new level/reason>
Review value: <low | medium | high>; Reviewer: <none | fresh Sol / High>
Escalation condition: <next evidence condition, or none>
~~~

After failed verification, classify it as `code`, `harness`, `infrastructure`,
`flaky/non-deterministic`, or `specification/architecture`; apply the smallest correction
or discriminating check and rerun only the minimum required level. Never blindly rerun an
expensive command; repeated failure without new evidence follows the strategic checkpoint.

When stagnation, oscillation, or an invalidated core assumption is evidenced, emit:

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
Mode: adaptive-v2 | legacy; Strategy: <base>; Topology: <selected>
Routing: risk=<...>; scope=<...>; blast=<...>; behavior=<...>; context-freshness=<...>
Owner: initial=<Sol|Terra>; primary=<sticky owner>; reason=<evidence>; escalations=<count>
Execution budget: starting=<FAST|STANDARD|HEAVY>; final=<FAST|STANDARD|HEAVY>; escalations=<count>
Verification: plan=<L0 -> L1 -> L2 -> L3>; floor=<L0|L1|L2|L3>; result=<pass|fail|partial>
Review: value=<low|medium|high>; reviewer=<none|fresh Sol / High>; result-changed=<yes|no>
Parallel/manager: parallel=<yes|no>; manager=<yes|no>; workers=<count>; invocations=<count>
Result: complete | partial | blocked | rethink
Optional counts/host metrics: see `operations.md`; use `unavailable`, never inferred values.
~~~

Detailed optional counts remain in `operations.md`: owner switches/escalations, reviewer
and worker counts, retries, handoffs/reference slots, context reads, Review/Parallel ROI,
and directly exposed host metrics. `duplicate-reference-slots = reference-slots -
unique-references` is only a structural handoff proxy. Never infer tokens, duration, cost,
savings, or private transcript content. No analytics subsystem is introduced, and required
review or verification is never sacrificed to reduce agent calls.
The owner computes review ROI: `result-changed=yes` only when review causes correction,
rethink, or a different terminal decision; `correction-required=yes` only for `fix-first`.
