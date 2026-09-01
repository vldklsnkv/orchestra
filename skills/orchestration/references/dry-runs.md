# Adaptive-v2 dry runs

These examples validate policy. Paths are illustrative; they are not task-specific
instructions.

## 1. Simple one-file bug -> solo owner-only

~~~text
SELECTIVE ROUTE
Mode: adaptive-v2
Strategy: solo
Topology: owner-only
Risk: low
Scope: tiny
Blast radius: isolated
Behavior impact: none
Novelty/uncertainty evidence: known architecture
Reversibility: trivial
Context freshness: fresh
Complexity: low
Uncertainty: low
Verifiability: objective
Task nature: mechanical/bounded
Decomposable: no
Parallel: no
Parallelizable: no
Independent review: no
Manager: no
Initial owner: Terra
Primary: Terra
Owner reason: low uncertainty, low blast radius, objective verification, bounded fix
Additional agent value: none
Execution budget: FAST
Verification plan: L0 -> L1
Verification floor: L1
Review value: low
Reviewer: none
Escalation condition: unexpected test failure, scope expansion, or unproven invariant
Context inheritance: none
Inheritance reason: none
~~~

Terra owns research, fix, focused test, correction, and verification. The graph is solo.
No worker, manager, or reviewer is spawned; the selected Terra owner itself is one
spawned owner invocation.

## 2. Connected medium feature -> solo owner-only

~~~text
Mode: adaptive-v2
Strategy: solo
Topology: owner-only
Risk: medium
Scope: medium
Blast radius: local
Behavior impact: internal
Novelty/uncertainty evidence: analogous verified path
Reversibility: localized
Context freshness: fresh
Complexity: medium
Uncertainty: medium
Verifiability: partial
Task nature: mixed
Decomposable: yes (research, implementation, tests are sequential stages)
Parallel: no
Parallelizable: no
Independent review: no
Manager: no
Initial owner: Sol
Primary: Sol
Owner reason: mixed task nature and partial verification; keep interpretation with Sol
Additional agent value: none
Execution budget: STANDARD
Verification plan: L0 -> L1 -> L2
Verification floor: L2
Review value: low
Reviewer: none
Escalation condition: hidden dependency, failed focused check, or architecture uncertainty
Context inheritance: none
Inheritance reason: none
~~~

The stages share one evolving implementation surface, so apparent decomposition does
not justify agent boundaries. One owner completes the connected task.

## 3. High-risk auth migration -> solo + high-value review

~~~text
Mode: adaptive-v2
Strategy: solo
Topology: owner-review
Risk: high
Scope: large
Blast radius: systemic
Behavior impact: data-affecting
Novelty/uncertainty evidence: new subsystem/unknown behavior/external dependency
Reversibility: stateful/migration
Context freshness: not established
Complexity: high
Uncertainty: high
Verifiability: partial
Task nature: reasoning-heavy architecture/problem-framing
Decomposable: no
Parallel: no
Parallelizable: no
Independent review: yes (high review value: auth and atomic migration invariants)
Manager: no
Initial owner: Sol
Primary: Sol
Owner reason: high uncertainty and systemic blast radius with less-than-objective verification
Additional agent value: independent fail-closed review
Execution budget: HEAVY
Verification plan: L0 -> L1 -> L2 -> L3
Verification floor: L3
Review value: high
Reviewer: fresh Sol / High
Escalation condition: further migration scope, hidden dependency, or invariant gap
Context inheritance: none
Inheritance reason: none
~~~

The owner implements and verifies, then sends an ARTIFACT HANDOFF to a fresh Sol
reviewer using `fork_turns: none`. There is no manager lane.

## 4. Five independent adapters -> parallel

~~~text
Mode: adaptive-v2
Strategy: parallel
Topology: orchestrated-parallel
Complexity: medium
Uncertainty: low
Risk: low
Verifiability: objective
Task nature: mechanical/bounded
Decomposable: yes (5 independent adapter/test deliverables)
Parallelizable: yes (non-overlapping files; no intermediate dependency)
Independent review: no
Manager: yes (decomposition and synthesis)
Initial owner: Terra
Owner reason: clear bounded deliverables with objective verification
Additional agent value: five unique independently accepted outputs
Context inheritance: none
Inheritance reason: none
~~~

Each Luna lane owns one adapter/test pair and lists the other adapters under
`FORBIDDEN ACTIONS` / `DO NOT RESEARCH`. Terra, the selected owner, synthesizes once;
primary Sol performs final acceptance without taking over the execution lane.

## 5. Non-decomposable refactor -> solo, no fake parallelism

~~~text
Mode: adaptive-v2
Strategy: solo
Topology: owner-only
Complexity: high
Uncertainty: high
Risk: medium
Verifiability: partial
Task nature: reasoning-heavy architecture/problem-framing
Decomposable: yes (conceptual stages only)
Parallelizable: no (shared symbols and intermediate decisions)
Independent review: no
Manager: no
Initial owner: Sol
Owner reason: reasoning-heavy shared-symbol refactor with partial verification
Additional agent value: none
~~~

High complexity does not itself create a worker. The owner keeps coupled research,
refactor, tests, and correction together.

## 6. Bounded specialist advantage -> delegate

~~~text
Mode: adaptive-v2
Strategy: delegate
Topology: owner-specialist
Complexity: medium
Uncertainty: low
Risk: low
Verifiability: objective
Task nature: mechanical/bounded
Decomposable: yes (one isolated migration generator)
Parallelizable: no
Independent review: no
Manager: no
Initial owner: Sol
Owner reason: Sol retains connected work while Luna supplies one bounded specialist artifact
Additional agent value: Luna can produce one frozen mechanical generator independently
Context inheritance: none
Inheritance reason: none
~~~

Luna receives one Context Packet and returns a unique deliverable. Sol keeps the rest
of the connected task and verification.

## 7. Judgment-heavy specialist -> expert

~~~text
Mode: adaptive-v2
Strategy: expert
Topology: owner-specialist
Complexity: high
Uncertainty: high
Risk: medium
Verifiability: partial
Task nature: reasoning-heavy architecture/problem-framing
Decomposable: yes (bounded protocol analysis)
Parallelizable: no
Independent review: no
Manager: no
Initial owner: Sol
Owner reason: reasoning-heavy protocol interpretation stays with Sol
Additional agent value: Terra supplies protocol-specific evidence under a narrow boundary
Context inheritance: none
Inheritance reason: none
~~~

Terra may be selected immediately; Luna failure is not required. Generic complexity
without the named protocol boundary would remain owner-only.

## 8. Competing hypotheses -> explore

~~~text
Mode: adaptive-v2
Strategy: explore
Topology: orchestrated-parallel
Complexity: high
Uncertainty: high
Risk: medium
Verifiability: partial
Task nature: reasoning-heavy architecture/problem-framing
Decomposable: yes (3 independent hypotheses)
Parallelizable: yes (read-only distinct evidence scopes)
Independent review: no
Manager: yes (comparative synthesis)
Initial owner: Sol
Owner reason: high uncertainty requires Sol arbitration across hypotheses
Additional agent value: three discriminating evidence sets
Context inheritance: none
Inheritance reason: none
~~~

Polling, streaming, and durable-queue lanes use distinct evidence scopes. Sol
arbitrates against one rubric; duplicate investigations are forbidden.

## 9. Architecture freeze then isolated execution -> plan-execute

~~~text
Mode: adaptive-v2
Strategy: plan-execute
Topology: owner-specialist
Complexity: high
Uncertainty: high
Risk: medium
Verifiability: partial
Task nature: reasoning-heavy architecture/problem-framing
Decomposable: yes (architecture decision; isolated mechanical generation)
Parallelizable: no
Independent review: no
Manager: no
Initial owner: Sol
Owner reason: architecture and interpretation precede any bounded mechanical delegation
Additional agent value: Luna executes the frozen table without reopening architecture
Context inheritance: none
Inheritance reason: none
~~~

If implementation exposes architecture, Luna returns `WORKER STOP` and control returns
to the owner.

## 10. Unknown regression -> diagnose-fix

~~~text
Mode: adaptive-v2
Strategy: diagnose-fix
Topology: owner-only
Complexity: high
Uncertainty: high
Risk: medium
Verifiability: partial
Task nature: reasoning-heavy architecture/problem-framing
Decomposable: no
Parallelizable: no
Independent review: no
Manager: no
Initial owner: Sol
Owner reason: unresolved cause and falsifiable diagnosis require Sol ownership
Additional agent value: none
~~~

Sol records reproduction, evidence, falsifiable hypothesis, the smallest discriminating
experiment, result, causal fix, and regression verification. A speculative fix is not
allowed before causal evidence.

## 11. Review verdicts and bounded correction

Initial `ship` terminates immediately with one review cycle.

For `fix-first`, the same owner makes one bounded correction after recording the
post-review materiality decision. Assurance follows semantic impact, not diff size.

### Case 1: material architecture correction

An architecture conclusion used the wrong lineage assumption. The correction changes
evidence interpretation and the main conclusion.

`Class: MATERIAL` -> bounded correction -> owner verification -> fresh full independent
review. The architecture conclusion is the invalidated scope.

### Case 2: comment typo

A reviewer finds an incorrect comment while production behavior and the reviewed
implementation remain unchanged.

`Class: NON-MATERIAL` -> comment correction -> manager deterministic verification ->
`SHIP`. Full reviewer: not required.

### Case 3: artifact hash regeneration

Artifact content is unchanged and only its manifest hashes are regenerated.

`Class: NON-MATERIAL` -> manager verifies content identity and regenerated hashes -> no
reviewer.

### Case 4: provenance wording

The report says `run skipped`; the raw log proves `run interrupted during build`. The
experimental result, evidence interpretation, and conclusion do not change.

`Class: NON-MATERIAL` -> manager verifies the raw log and corrected provenance -> no full
reviewer.

### Case 5: local substantive fix

A reviewer finds a bug in one isolated function. The correction restores the unchanged
reviewed behavior contract; its neighboring paths, architecture, safety properties,
acceptance criteria, and main conclusion remain valid.

`Class: TARGETED` -> bounded correction -> owner verification -> targeted independent
re-review. The packet includes the original finding, exact function diff, relevant tests,
regression perimeter, and the explicit question whether the isolated bug is fixed.

### Case 6: second reviewer finds a new material defect

The second full reviewer finds a new security invariant violation. Its correction changes
substantive state, and the owner records why a scoped check cannot validate the affected
architecture.

`Class: MATERIAL` -> correction -> a third full review is allowed with the recorded
escalation reason.

### Case 7: second reviewer finds another minor issue

The second reviewer finds only a wording or provenance issue that does not change the
substantive state or conclusion.

`Class: NON-MATERIAL` -> deterministic manager verification -> no third full review.

### Case 8: tiny diff with huge semantic impact

A one-line security decision or production threshold change alters externally observable
behavior.

`Class: MATERIAL` despite diff size -> fresh full independent review.

### Case 9: large generated diff with no semantic impact

A manifest and generated artifacts change many lines, while deterministic comparison
proves source content and effective behavior are identical.

`Class: NON-MATERIAL` -> deterministic equivalence and hash verification -> no reviewer.

In every case the prior verdict remains valid for unchanged reviewed scope. The gate
invalidates only the surface semantically affected by the correction.

## 12. Legacy fallback

~~~text
Mode: legacy
Strategy: expert
Topology: manager
Complexity: high
Risk: high
Decomposable: no
Parallelizable: no
Independent review: yes
Manager: yes (legacy v0.4 worker routing selected explicitly)
Initial owner: Sol
Owner reason: legacy mode keeps its explicit Sol manager contract
Additional agent value: Terra implementation plus fresh Sol review
Context inheritance: none
Inheritance reason: none
~~~

Legacy runs use the v0.4 manager -> worker -> manager verification -> optional reviewer
shape with the same role pins, packets, retry gates, and seven strategies. This fallback
is selectable, not automatic.

## 13. Frozen initial-owner matrix

The Router chooses the initial owner independently from strategy, topology, budget,
verification floor, and review value. Each row describes a graph that is immutable until
an explicit escalation gate; Strategy only executes that graph.

| Case | Owner signals | Initial owner | Topology / review | Required owner evidence |
|---|---|---|---|---|
| Low-uncertainty mechanical | uncertainty=low; domain risk=low; blast radius=isolated; verifiability=objective; task nature=mechanical/bounded | Terra | solo; no reviewer | Terra owns the complete run |
| High-uncertainty architecture | uncertainty=high; reasoning-heavy architecture/problem-framing; verifiability=partial | Sol | solo | Sol owns research through verification |
| Small high-blast/hard-to-verify | domain risk=high; blast radius=systemic; verifiability=low; review value=high | Sol | `owner-review` from independent value | reviewer does not replace owner or count as escalation |
| Large clear mechanical | uncertainty=low; domain risk=medium; blast radius=isolated; verifiability=objective; task nature=mechanical/bounded | Terra | solo; no reviewer | Terra owns the large bounded implementation |
| Terra escalation | materially higher uncertainty or architectural fork appears | Terra | same topology; owner changes only at evidence gate | `Terra -> evidence-addressed ARTIFACT HANDOFF -> Sol takeover`; Sol stays owner with no downgrade |
| Sol completes small implementation | low scope but mixed interpretation | Sol | solo; no reviewer | completes without Terra handoff |
| Genuine parallel decomposition | independent deliverables; non-overlap; no intermediate dependency | Sol | existing `orchestrated-parallel` path | parallel workers remain; owner does not change |
| Reviewer boundary | any owner with explicit request or named safety/contract boundary with high independent value | Sol or Terra | owner-review | reviewer never replaces owner and `owner_escalations=0` |

The Terra rows satisfy every Terra condition; the Sol rows are conservative where any
required signal is unresolved or less than high/objective. Budget and review are chosen
independently: high risk alone is not automatic review, and a reviewer is not an owner
switch or owner escalation.

## 14. Execution-budget and verification matrix

These ten policy cases keep domain risk, scope, evidence, verification, and review value
independent. They are dry runs, not hardcoded runtime routing.

| Case | Scope/evidence | Initial budget | Verification/review outcome |
|---|---|---|---|
| 1. High risk + tiny shadow-only + verified | tiny; local; shadow-only; known architecture; fresh context | `FAST` | solo; L0 -> focused L1; no reviewer unless new evidence |
| 2. High risk + systemic production | large; systemic; user-visible/data-affecting; stateful or destructive | `HEAVY` | L0 -> L1 -> L2 -> L3; review only when independent value is high |
| 3. Low/medium risk + large cross-component | large; cross-component; even with low/medium domain risk | not `FAST` (`HEAVY`) | broad integration floor follows concrete invariants |
| 4. Small + unknown architecture | small; novelty is new subsystem/unknown behavior; context not established | at least `STANDARD` | normal preflight before focused verification |
| 5. FAST unexpected test failure | FAST route receives new failure evidence | `STANDARD` after evidence | classify and perform the smallest discriminating check; no blind expensive rerun |
| 6. Relevant file change | exact-HEAD proof plus relevant staged/unstaged path changed in worktree/index | invalidated; normal preflight | stale context cannot be reused |
| 7. High risk objectively testable tiny mechanical | tiny; isolated; objective output identity; high reversibility | `FAST` | review value low; reviewer not required |
| 8. Medium scope + high review value | medium; local/interacting; specific independent judgment gap | `STANDARD` | `owner-review` may run without `HEAVY` |
| 9. Cold expensive infrastructure + cheap falsifier | any budget with a cheap L0/L1 falsifier | unchanged | cheap check runs first; cold/warm state never omits the floor |
| 10. Cheap pass + critical integration invariant | L0/L1 pass but acceptance names an integration invariant | unchanged | continue to required `L2`; FAST never skips it |

### Case 1: high risk + tiny shadow-only + verified -> FAST

~~~text
SELECTIVE ROUTE
Risk: high
Scope: tiny
Blast radius: local
Behavior impact: shadow-only
Novelty/uncertainty evidence: known architecture
Reversibility: trivial
Context freshness: fresh
Initial owner: Sol
Primary: Sol
Parallel: no
Execution budget: FAST
Verification plan: L0 -> focused L1
Verification floor: L1
Review value: low
Reviewer: none
Escalation condition: unexpected behavior, scope expansion, failed L1, or an unproven invariant
~~~

The high domain risk affects confidence and invariants, not machinery by itself. A
Clast-like parser/scorer shadow-instrumentation regression is a generic policy example:
expected high risk, small/local/shadow-only behavior, known and freshly verified context,
FAST, one sticky owner, focused L0/L1 verification, and no reviewer unless new evidence
raises independent review value. No parser, scorer, or product-specific routing logic is
encoded by this example.

### Case 2: high risk + systemic production -> HEAVY

~~~text
SELECTIVE ROUTE
Risk: high
Scope: large
Blast radius: systemic
Behavior impact: user-visible/data-affecting
Novelty/uncertainty evidence: new subsystem/unknown behavior/external dependency
Reversibility: stateful/migration
Context freshness: stale
Initial owner: Sol
Primary: Sol
Parallel: no
Execution budget: HEAVY
Verification plan: L0 -> L1 -> L2 -> L3
Verification floor: L3
Review value: high
Reviewer: fresh Sol / High
Escalation condition: further scope expansion or any unproven migration invariant
~~~

Systemic production behavior requires heavy machinery and its concrete L3 floor. Review
is justified here by the high-impact contract and independent judgment, not by a blanket
rule that high risk automatically selects review.

### Case 3: low/medium risk + large cross-component -> not FAST

~~~text
SELECTIVE ROUTE
Risk: medium
Scope: large
Blast radius: cross-component
Behavior impact: internal
Novelty/uncertainty evidence: analogous verified path
Reversibility: localized
Context freshness: fresh
Initial owner: Sol
Primary: Sol
Parallel: no
Execution budget: HEAVY
Verification plan: L0 -> L1 -> L2 -> L3
Verification floor: L2
Review value: medium
Reviewer: none
Escalation condition: integration failure or hidden dependency
~~~

Low or medium risk does not make a large cross-component change FAST. Scope and the
integration floor determine the machinery.

### Case 4: small + unknown architecture -> at least STANDARD

~~~text
SELECTIVE ROUTE
Risk: medium
Scope: small
Blast radius: local
Behavior impact: internal
Novelty/uncertainty evidence: new subsystem/unknown behavior/external dependency
Reversibility: localized
Context freshness: not established
Initial owner: Sol
Primary: Sol
Parallel: no
Execution budget: STANDARD
Verification plan: L0 -> L1 -> L2 as needed
Verification floor: L1
Review value: medium
Reviewer: none
Escalation condition: architecture remains unknown after normal preflight
~~~

Small scope alone is insufficient for FAST when architecture is unknown. Establish normal
preflight and a falsifiable focused check before considering any later route change.

### Case 5: FAST unexpected test failure -> controlled escalation

~~~text
ORCHESTRA ROUTE
Evidence: FAST focused L1 unexpectedly failed; classify as code, harness, infrastructure, flaky/non-deterministic, or specification/architecture
Risk: high | medium | low (preserve the prior declaration)
Scope: tiny | small | medium | large (preserve unless evidence expands it)
Blast radius: isolated | local | cross-component | systemic (preserve unless evidence expands it)
Behavior impact: none | shadow-only | internal | user-visible | data-affecting (preserve)
Context freshness: fresh | stale | not established (recheck)
Initial owner: Sol | Terra (sticky)
Primary: current sticky owner
Parallel: no | yes (preserve prior graph)
Previous execution budget: FAST
Execution budget: STANDARD
Verification plan: L0 -> focused L1 -> minimum new level
Verification floor: prior floor or raised floor
Verification change: smallest discriminating check, then the minimum required level
Review value: prior low | medium | high (reassess only with evidence)
Reviewer: prior reviewer or none
Escalation condition: next evidence condition, or none
~~~

The owner records the failure class, applies the smallest correction or discriminating
check, and reruns only the minimum required level. The route moves to STANDARD only on
this evidence; it is not pre-escalated and is never silently downgraded.

### Case 6: relevant staged/unstaged path change invalidates exact-HEAD context

~~~text
VERIFIED CONTEXT
Repo/worktree: /repo/worktree
Base: base HEAD or proven descendant
Freshness proof: exact HEAD plus relevant-path worktree/index check found a staged/unstaged change
Relevant files: src/owned-file (identity-sensitive path changed)
Frozen artifacts: none
Relevant config: unchanged
Architecture map/invariants: canonical map and invariant address
Evidence timestamp/source (optional): freshness proof after the prior handoff; timestamp supporting only
Context freshness: stale
~~~

A relevant staged or unstaged path change makes the exact-HEAD context stale and forbids reuse;
normal preflight resumes. The owner does not reread or trust the old architecture record until
a new minimal freshness proof succeeds. Ordinary paths are checked for change without hashing
by default.

### Case 7: high risk objectively testable tiny mechanical -> reviewer not required

~~~text
SELECTIVE ROUTE
Risk: high
Scope: tiny
Blast radius: isolated
Behavior impact: none
Novelty/uncertainty evidence: previous verified iteration
Reversibility: trivial
Context freshness: fresh
Execution budget: FAST
Verification plan: L0 -> focused L1
Verification floor: L1
Review value: low
Reviewer: none
~~~

Objective output identity and focused tests close the independent information gap. High
domain risk alone does not select a reviewer; required safety invariants still run.

### Case 8: medium scope + high review value -> review without HEAVY

~~~text
SELECTIVE ROUTE
Risk: medium
Scope: medium
Blast radius: local
Behavior impact: internal
Novelty/uncertainty evidence: analogous verified path
Reversibility: localized
Context freshness: fresh
Execution budget: STANDARD
Verification plan: L0 -> L1 -> L2
Verification floor: L2
Review value: high
Reviewer: fresh Sol / High
~~~

The specific interpretation or contract judgment justifies `owner-review`, while medium
scope and a targeted L2 floor remain STANDARD rather than HEAVY.

### Case 9: cold expensive infrastructure + cheap falsifier -> cheap first

~~~text
SELECTIVE ROUTE
Execution budget: STANDARD
Verification plan: cheap L0/L1 falsifier -> targeted L2 only if the floor requires it
Verification floor: L2
~~~

Even when the integration environment is cold and expensive, run the cheap falsifier
first. Cold/warm infrastructure changes order and early falsification, never permission
to omit the required L2 floor.

### Case 10: cheap pass + critical invariant needs integration -> continue to L2

~~~text
SELECTIVE ROUTE
Execution budget: FAST
Verification plan: L0 -> focused L1 -> required L2 integration
Verification floor: L2
~~~

Passing L0 and L1 does not finish the run when a critical integration invariant is named.
Continue to L2; FAST never skips an L2 or L3 requirement.

## Artifact handoff example

~~~text
ARTIFACT HANDOFF
Objective: preserve atomic encrypted v1-to-v2 migration
Acceptance criteria: v1, v2, and rollback tests pass; failure preserves original bytes
Hard constraints: no plaintext; v1 compatibility for one release
Changed files: Sources/SessionStore.swift; Tests/SessionStoreMigrationTests.swift
Diff references: base abc123..HEAD; SessionStore.migrate; rollback tests
Test / verification results: focused migration suite 8/8; diff check clean
Created artifacts: rollback fixture hash sha256:...
Important invariants: atomic write; byte-preserving failure
Unresolved risks: host interruption between rename and fsync
Exact questions for next agent: is fail-closed rollback proven for every error branch?
~~~

The handoff excludes full reasoning/history, owner confidence, and a proposed verdict.
The reviewer fetches the addressed diff, symbols, tests, and artifact directly.

## Context inheritance validation A-D

### A. Isolated specialist -> none

Mode: `fork_turns: none`.
Reason: the self-contained packet is sufficient.
Boundary: the packet records the objective, exact allowed scope and ownership,
constraints, evidence addresses, forbidden actions, verification, and stop conditions.

### B. Specialist + reviewer -> scoped/none and evidence-only

Specialist mode: `fork_turns: none`.
Reviewer mode: `fork_turns: none`.
Reason: fresh evidence-only review uses ARTIFACT HANDOFF and targeted reads, not the full
owner/manager transcript or implementation reasoning.

### C. Context-dependent continuation -> limited N

Mode: `fork_turns: "3"`.
Reason: the last `3` turns contain a still-active interactive artifact transition that
supplements the packet. Inherited turns cannot supply a missing boundary.

### D. Genuinely unsafe reconstruction -> deliberate all fallback

Mode: `fork_turns: all`.
Reason: the complete user-confirmed multi-turn decision transcript is the explicit
authoritative artifact and its ordered revisions cannot safely be paraphrased.
Boundary: the packet still records every constraint and safety boundary, objective,
exact scope and ownership, transcript artifact address, forbidden actions,
verification, and stop conditions. No unrecorded constraint controls an allowed
action; inherited turns only supplement the packet. Review remains `none`.
