# Strategy dry runs

These routing examples validate policy; paths and symbols are illustrative. Packets use
the compact contract and are self-contained without a retained manager transcript.

## 1. Tiny one-file bug -> solo

~~~text
SELECTIVE ROUTE
Strategy: solo
Risk: low
Ambiguity: low
Decomposable: no
Implementation: Sol
Parallel: no
Review: no
Context inheritance: none
Inheritance reason: none
~~~

Why: a localized null check and focused test are cheaper to inspect and verify directly.
No worker is spawned, so no Context Packet exists.

## 2. Bounded UI implementation -> delegate

~~~text
SELECTIVE ROUTE
Strategy: delegate
Risk: low
Ambiguity: low
Decomposable: no
Implementation: Luna
Parallel: no
Review: no
Context inheritance: none
Inheritance reason: none
~~~

~~~text
ROLE
Role: Luna bounded worker; Strategy: delegate; Lane: profile-card-loading
Context inheritance: none
Inheritance reason: none
OBJECTIVE
Add ProfileCard loading state while preserving the default UI.
CURRENT STATE (authoritative facts)
- Spinner and spacing tokens exist; design acceptance replaces content but preserves size.
CONSTRAINTS / INVARIANTS
- Existing initializer calls compile unchanged; tokens only.
ALLOWED SCOPE
- Sources/UI/ProfileCard.swift initializer/body; Tests/UI/ProfileCardTests.swift case.
FORBIDDEN ACTIONS
- Do not modify Spinner, Card, token definitions, or other profile screens.
- DO NOT RESEARCH: component inventory and loading-state design are settled.
RELEVANT FILES / ARTIFACTS
- Sources/UI/ProfileCard.swift: ProfileCard body and initializer.
EXPECTED OUTPUT / VERIFICATION
- Run focused ProfileCard tests; inspect owned diff only.
STOP / ESCALATION
- Stop if compatibility needs a new architecture or token.
~~~

## 3. Risky architectural change -> expert + review

~~~text
SELECTIVE ROUTE
Strategy: expert
Risk: high
Ambiguity: medium
Decomposable: no
Implementation: Terra
Parallel: no
Review: yes
Context inheritance: none
Inheritance reason: none
~~~

Terra receives `none` and a packet owning `SessionStore` migration,
`SessionEnvelope` decoding, and migration tests. Current state points to ADR-014 and
the rollback fixture; constraints prohibit plaintext and require atomic byte-preserving
failure; `DO NOT RESEARCH` excludes cipher, schema, and support-window decisions.

After manager verification, the reviewer receives `fork_turns: none` and only:

~~~text
REVIEW OBJECTIVE
Accept or reject atomic encrypted v1-to-v2 migration.
AUTHORITATIVE CONSTRAINTS
- No plaintext; rollback preserves original bytes; v1 compatibility for one release.
EXACT CHANGE / EVIDENCE
- SessionStore, SessionEnvelope, migration-test diff; suite output and fixture hashes.
ACCEPTANCE CRITERIA
- v1/v2/rollback cases pass and failure leaves original bytes unchanged.
MINIMUM SOURCE ADDRESSES
- SessionStore.migrate, SessionEnvelope.decode, atomic-write helper, rollback tests.
FORBIDDEN ACTIONS / CONTEXT
- Do not edit or broaden scope. Do not receive the full manager transcript,
  implementation-agent reasoning, long discussions, or conclusion-framed summaries.
EXACT VERDICT RETURN
SOL REVIEW: ship | fix-first | rethink with decisive evidence and precise findings.
~~~

## 4. Five independent mechanical changes -> parallel

~~~text
SELECTIVE ROUTE
Strategy: parallel
Risk: low
Ambiguity: low
Decomposable: yes (5 independent lanes)
Implementation: Luna
Parallel: yes
Review: no
Context inheritance: none
Inheritance reason: none
~~~

Five Luna packets, one per Adapter A-E, each use `fork_turns: none`, own only that
adapter/test pair, retain a deprecated forwarding alias, test a distinct focused suite,
and list the other adapters under `FORBIDDEN ACTIONS` / `DO NOT RESEARCH`. No lane needs
another's intermediate result; Sol owns integration.

## 5. Unknown regression -> diagnose-fix

~~~text
SELECTIVE ROUTE
Strategy: diagnose-fix
Risk: medium
Ambiguity: high
Decomposable: no
Implementation: Terra
Parallel: no
Review: no
Context inheritance: none
Inheritance reason: none
~~~

The Terra packet owns reconnect lifecycle, request dedupe only if causal evidence points
there, and focused tests. It requires `DIAGNOSIS` with reproduction, evidence,
falsifiable hypothesis, minimal discriminating experiment, and result. `DO NOT RESEARCH`
excludes cold-start and serialization. Only a confirmed experiment permits the fix.

## 6. Competing architectural approaches -> explore

~~~text
SELECTIVE ROUTE
Strategy: explore
Risk: medium
Ambiguity: high
Decomposable: yes (3 independent hypotheses)
Implementation: mixed
Parallel: yes
Review: no
Context inheritance: none
Inheritance reason: none
~~~

Polling, streaming, and durable-queue lanes receive distinct `none` packets. Each has a
bounded approach-specific evidence scope, owns no production files, preserves
at-least-once/recovery/no-loss invariants, and returns comparable evidence only. Sol
arbitrates against one rubric; consensus alone is not evidence.

## 7. Complex design then mechanical implementation -> plan-execute

~~~text
SELECTIVE ROUTE
Strategy: plan-execute
Risk: medium
Ambiguity: high
Decomposable: no
Implementation: Luna after architecture freeze
Parallel: no
Review: no
Context inheritance: none
Inheritance reason: none
~~~

After Sol freezes ADR-021, Luna gets a `none` packet owning `UploadState` and its
transition tests. Current state records the approved table; `DO NOT RESEARCH` excludes
state models, retry policy, and naming. Stop if the frozen table is inconsistent or
needs a new state.

## Context inheritance validation A-D

### A. Isolated specialist -> none

Mode: `fork_turns: none`.
Reason: no prior turn is material; independent work can start from the packet.
Boundary: the packet records the objective, exact allowed scope and ownership,
constraints, evidence addresses, forbidden actions, `DO NOT RESEARCH`, verification,
and stop conditions.

### B. Specialist + reviewer -> scoped/none and evidence-only

Specialist mode: `fork_turns: none`.
Specialist reason: its scoped packet is sufficient for the assigned implementation.
Specialist boundary: that packet records the objective, exact allowed scope and
ownership, constraints, evidence addresses, forbidden actions, `DO NOT RESEARCH`,
verification, and stop conditions.
Reviewer mode: `fork_turns: none`.
Reviewer reason: fresh evidence-only review needs no inherited turns.
Reviewer boundary: exact diff/evidence and minimum source addresses only; forbidden
context excludes the full manager transcript, implementation reasoning, long
discussions, and conclusion-framed summaries.

### C. Context-dependent continuation -> limited N

Mode: `fork_turns: "3"`.
Reason: the last `3` turns contain a still-active interactive artifact transition that
supplements the packet.
Boundary: the packet still records the objective, all settled facts, exact allowed
scope and ownership, constraints, evidence addresses, forbidden actions, `DO NOT
RESEARCH`, verification, and stop conditions. The inherited turns cannot supply a
missing boundary.

### D. Genuinely unsafe reconstruction -> deliberate all fallback

Mode: `fork_turns: all`.
Reason: the complete user-confirmed multi-turn decision transcript is the explicit
authoritative artifact, and its ordered revisions cannot safely be paraphrased.
Boundary: the packet still records the objective, exact allowed scope and ownership,
every constraint and safety boundary, the transcript's artifact address, forbidden
actions, `DO NOT RESEARCH`, verification, and stop conditions. No unrecorded
constraint controls an allowed action; inherited turns only supplement the packet.
This is exceptional, not a convenience default, and review remains `none`.
