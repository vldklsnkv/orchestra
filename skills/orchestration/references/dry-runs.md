# Adaptive-v2 dry runs

These examples validate policy. Paths are illustrative; they are not task-specific
instructions.

## 1. Simple one-file bug -> solo owner-only

~~~text
SELECTIVE ROUTE
Mode: adaptive-v2
Strategy: solo
Topology: owner-only
Complexity: low
Uncertainty: low
Risk: low
Verifiability: objective
Task nature: mechanical/bounded
Decomposable: no
Parallelizable: no
Independent review: no
Manager: no
Initial owner: Terra
Owner reason: low uncertainty, low blast radius, objective verification, bounded fix
Additional agent value: none
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
Complexity: medium
Uncertainty: medium
Risk: medium
Verifiability: partial
Task nature: mixed
Decomposable: yes (research, implementation, tests are sequential stages)
Parallelizable: no
Independent review: no
Manager: no
Initial owner: Sol
Owner reason: mixed task nature and partial verification; keep interpretation with Sol
Additional agent value: none
~~~

The stages share one evolving implementation surface, so apparent decomposition does
not justify agent boundaries. One owner completes the connected task.

## 3. High-risk auth migration -> solo + owner-review

~~~text
Mode: adaptive-v2
Strategy: solo
Topology: owner-review
Complexity: high
Uncertainty: high
Risk: high
Verifiability: partial
Task nature: reasoning-heavy architecture/problem-framing
Decomposable: no
Parallelizable: no
Independent review: yes (auth and atomic migration invariants)
Manager: no
Initial owner: Sol
Owner reason: high uncertainty and high blast radius with less-than-objective verification
Additional agent value: independent fail-closed review
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

For `fix-first`, the same owner makes one bounded correction, re-verifies, and creates a
new ARTIFACT HANDOFF. A fresh reviewer receives `Pass: targeted re-review`, checks the
affected surface and regression perimeter first, then returns `ship`, `fix-first`, or
`rethink`. Another cycle is forbidden unless the correction exposed a new material
defect class. Repeated summary or wording drift triggers stop/checkpoint, not another
reviewer.

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

The Router chooses the initial owner independently from topology and review. Each row
describes a graph that is immutable until an explicit escalation gate; Strategy only
executes that graph.

| Case | Owner signals | Initial owner | Topology / review | Required owner evidence |
|---|---|---|---|---|
| Low-uncertainty mechanical | uncertainty=low; risk/blast radius=low; verifiability=objective; task nature=mechanical/bounded | Terra | solo; no reviewer | Terra owns the complete run |
| High-uncertainty architecture | uncertainty=high; reasoning-heavy architecture/problem-framing; verifiability=partial | Sol | solo | Sol owns research through verification |
| Small high-blast/hard-to-verify | risk/blast radius=high; verifiability=low | Sol | existing `owner-review` policy | reviewer does not replace owner or count as escalation |
| Large clear mechanical | uncertainty=low; risk/blast radius=medium; verifiability=objective; task nature=mechanical/bounded | Terra | solo; no reviewer | Terra owns the large bounded implementation |
| Terra escalation | materially higher uncertainty or architectural fork appears | Terra | same topology; owner changes only at evidence gate | `Terra -> evidence-addressed ARTIFACT HANDOFF -> Sol takeover`; Sol stays owner with no downgrade |
| Sol completes small implementation | low scope but mixed interpretation | Sol | solo; no reviewer | completes without Terra handoff |
| Genuine parallel decomposition | independent deliverables; non-overlap; no intermediate dependency | Sol | existing `orchestrated-parallel` path | parallel workers remain; owner does not change |
| Reviewer boundary | any owner with mandatory independent review | Sol or Terra | owner-review | reviewer never replaces owner and `owner_escalations=0` |

The Terra rows satisfy every Terra condition; the Sol rows are conservative where any
required signal is unresolved or less than high/objective. A reviewer is not an owner
switch, and a parallel worker is not an owner escalation.

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
