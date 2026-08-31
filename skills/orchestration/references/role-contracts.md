# Native Codex role contracts

Strategies organize work; the three namespaced custom agents supply the pinned role for
a lane. Do not add roles or runtime infrastructure for a strategy.

## Routing and native context contract

Before task tools, Sol emits `SELECTIVE ROUTE` with strategy, risk, ambiguity,
decomposability, implementation, parallelism, review, and:

~~~text
Context inheritance: none | limited <N> | all (rare)
Inheritance reason: <required for limited <N> or all; otherwise none>
~~~

Use the native `fork_turns` contract exactly: `none`, a positive integer string `<N>`,
or `all`. It defaults to `all` only when omitted, so Orchestra must always select it
explicitly. Default `none`; use limited `<N>` only when recent turns are materially
necessary; use `all` only as a deliberate rare fallback when reconstruction from the
packet is unsafe because the exact full interaction history is itself an explicitly
addressed authoritative artifact that cannot be safely paraphrased. A reviewer always receives `none`.

Every worker packet is complete in every inheritance mode: `none`, `<N>`, or `all`.
Inherited turns are supplementary context only. They never provide or replace a safety boundary, permission, ownership, invariant, acceptance criterion, or settled fact missing from the packet; no unrecorded constraint may control an allowed action.

Sol / High remains manager and final acceptor. Luna / Max executes bounded or frozen
work, Terra / High handles material judgment, complexity, risk, context, or blast
radius, and fresh Sol / High is used only after manager verification for `review`.
Terra may be selected immediately; a failed Luna attempt is never required. Parallel
lanes have distinct deliverables, ownership, and evidence scopes.

## Compact worker Context Packet

Every Luna or Terra prompt contains this complete contract. Replace placeholders; use
`none` only where genuinely empty. It must be self-contained, not a manager transcript.

~~~text
ROLE
Role: Luna bounded worker | Terra expert worker
Strategy: <base strategy>; Lane: <unique lane name>
Context inheritance: none | <positive integer string N> | all
Inheritance reason: <required unless none>

OBJECTIVE
<Observable outcome or decision required.>

CURRENT STATE (authoritative facts)
- <settled fact, approved decision, exact failure, or evidence address>

CONSTRAINTS / INVARIANTS
- <interface, behavior, safety, compatibility, or parallel non-overlap constraint>

ALLOWED SCOPE
- <exact owned files or symbols; implementation steps or bounded evidence question>

FORBIDDEN ACTIONS
- Do not modify: <outside ownership>
- DO NOT RESEARCH: <settled areas, decisions, or other-lane evidence scopes>
- Do not retain or reconstruct unrelated transcript/history.

RELEVANT FILES / ARTIFACTS
- <path>: <symbol/range and relevance>
- <command output, artifact, or evidence location>

EXPECTED OUTPUT / VERIFICATION
- Run: <exact command>. Success: <concrete result>.
- Inspect: <exact diff/artifact/runtime state>. Success: <concrete evidence>.

STOP / ESCALATION
- Stop if <ambiguity, ownership conflict, risk boundary, or invalidated approach>.
- Return control if the same failure repeats without new evidence.
~~~

Use paths, symbols, ranges, commands, and evidence addresses rather than copied
repository prose. Parallel lanes require non-overlapping `ALLOWED SCOPE` and distinct
`DO NOT RESEARCH`/evidence scopes. Workers preserve concurrent edits and never revert
unrelated work. The completed packet itself always records the authoritative objective,
allowed scope, constraints, evidence/artifact addresses, forbidden actions, `DO NOT
RESEARCH` boundaries, verification, and stop conditions; inherited context cannot
weaken or fill in any of them.

## Worker return contract

~~~text
WORK REPORT
STATUS / RESULT: complete | partial | blocked | rethink
DECISION / VERDICT: <when applicable, otherwise none>
EVIDENCE / ARTIFACTS: <exact commands, output, paths, or addresses>
FILES CHANGED: <actual files, or none>
UNRESOLVED RISKS / AMBIGUITIES: <items, or none>
STOP / ESCALATION REASON: <reason, or none>
CONTEXT USED: files=<count>, ranges=<count>, evidence-items=<count> [optional]
~~~

This lightweight report describes the result; it is not a state machine.

## Stop signal and role lanes

On an architectural choice, material ambiguity, wider scope, judgment-heavy decision,
high-risk invariant, or systemic verification failure, return `WORKER STOP` with type,
trigger, exact evidence address, preserved owned work, manager decision needed, and one
safe next step. A specification defect permits at most one corrected Luna retry.
Misclassified bounded work escalates directly to Terra; a retry is not required.
Repeated failure without new evidence stops. Evidence invalidating the architecture
returns `rethink`, not another local fix.

Spawn Luna exactly:

~~~text
agent_type: orchestra_luna_implementer
fork_turns: <explicit none | positive integer string N | all>
~~~

Spawn Terra exactly:

~~~text
agent_type: orchestra_terra_implementer
fork_turns: <explicit none | positive integer string N | all>
~~~

Do not attach model or reasoning overrides. The prompt begins with `ROLE` and the
completed compact worker Context Packet.

For `diagnose-fix`, include a `DIAGNOSIS` block with reproduction, evidence,
falsifiable hypothesis, minimal discriminating experiment, and result. Only a
confirmed result permits the causal fix.

## Fresh Sol / High review modifier

After manager verification, spawn exactly:

~~~text
agent_type: orchestra_sol_reviewer
fork_turns: none
~~~

Do not attach model or reasoning overrides. The reviewer is behaviorally read-only and
receives this minimal evidence-focused packet:

~~~text
REVIEW OBJECTIVE
<Acceptance decision to independently check.>

AUTHORITATIVE CONSTRAINTS
- <invariants, interfaces, safety boundaries, excluded scope>

EXACT CHANGE / EVIDENCE
- <allowed files plus complete relevant diff/base-head and command output/artifact>

ACCEPTANCE CRITERIA
- <observable required behavior and regression checks>

MINIMUM SOURCE ADDRESSES
- <paths, symbols, and ranges needed to test critical claims>

FORBIDDEN ACTIONS / CONTEXT
- Do not edit, implement fixes, or broaden scope.
- Do not receive or request the full manager transcript, implementation-agent reasoning,
  long discussions, or conclusion-framed summaries.

EXACT VERDICT RETURN
SOL REVIEW
VERDICT: ship | fix-first | rethink
REASON: <decisive evidence-based reason>
FINDINGS: <precise addresses and required fixes, or none>
RESIDUAL RISK: <most important remaining risk, or none>
~~~

The reviewer inspects actual files and evidence rather than trusting a conclusion.
Any correction invalidates its verdict and requires manager re-verification and a fresh
review. Use observed sandbox policy: if read-only is not observed and hard isolation is
needed, stop review; otherwise record exact before/after state and never claim enforced
isolation.
