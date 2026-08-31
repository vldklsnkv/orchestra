# Native Codex role contracts

## Primary owner and conditional manager: Router and initial owner

In `adaptive-v2`, primary Sol / High is the Router and final acceptor. The Router selects
one execution graph containing initial owner (`Sol` or `Terra`), topology, and review
requirement. The graph is immutable between explicit escalation gates. The selected
initial owner owns research, execution, tests, correction, and verification for the run;
primary Sol performs final acceptance without duplicating that execution lane.

The initial owner is `Terra` only for low uncertainty, low/medium risk or blast radius,
high/objective verifiability, and mechanical/bounded task nature. `Sol` is selected for
high uncertainty, reasoning-heavy architecture/problem-framing, high cost of a wrong
interpretation, high risk with less-than-high verifiability, or any mixed/unresolved
signals. This owner decision is independent from decomposability, parallelism, strategy,
and review.

The Router marks a manager topology only for dynamic decomposition, synthesis of
independent workers, or routing ambiguity that the deterministic table cannot resolve.
The selected owner performs decomposition and synthesis; primary Sol performs that
function only when Sol is the selected owner. This is a topology decision, not a
separate manager-agent spawn.

One owner is a successful Orchestra topology. Luna / Max and Terra / High are optional
workers or specialists unless Terra is the selected initial owner. Fresh Sol / High is an
independent reviewer only when risk or stated information value justifies it; a reviewer
never replaces the owner.

`legacy` retains the v0.4 contract: Sol manages and verifies, Luna implements bounded
or frozen work, Terra handles judgment-heavy or high-risk work, and fresh Sol review is
the `review` modifier. The three role profiles and seven strategy names remain stable.

## Route and native context contract

Before task tools, Sol emits `SELECTIVE ROUTE` with mode, strategy, topology, uncertainty,
risk/blast radius, verifiability, task nature/reasoning, complexity, decomposability,
parallelizability, independent review, manager use, initial owner, compact owner reason,
and additional-agent value, plus:

~~~text
Uncertainty: low | medium | high
Risk: low | medium | high (blast radius)
Verifiability: objective | partial | low
Task nature: mechanical/bounded | reasoning-heavy architecture/problem-framing | mixed
Complexity: low | medium | high (telemetry only)
Initial owner: Sol | Terra
Owner reason: <compact evidence-based reason>
Context inheritance: none | limited <N> | all (rare)
Inheritance reason: <required for limited <N> or all; otherwise none>
~~~

Use native `fork_turns` exactly: `none`, a positive integer string `<N>`,
or `all`. Default to `none`. Use limited `<N>` only when recent turns are materially
necessary; use `all` only as a deliberate rare fallback when reconstruction from the
packet is unsafe because the exact full interaction history is itself an explicitly
addressed authoritative artifact that cannot be safely paraphrased. A reviewer always
receives `none`.

Every packet is complete in every inheritance mode. Inherited turns are supplementary
context only. They never provide or replace a safety boundary, permission, ownership,
invariant, acceptance criterion, or settled fact missing from the packet; no unrecorded
constraint may control an allowed action.

## Compact owner/worker Context Packet

Every Luna or Terra prompt contains this self-contained contract:

~~~text
ROLE
Role: Luna bounded worker | Terra selected owner | Terra expert specialist
Strategy: <base strategy>; Lane: <unique lane name>
Context inheritance: none | <positive integer string N> | all
Inheritance reason: <required unless none>
Expected information value: <required unique value for a worker/specialist; not-applicable for a selected owner>
Initial owner: <Sol | Terra>; sticky for this run
Owner/topology/review selection: fixed by Router; do not reselect silently

OBJECTIVE
<Observable outcome or decision required.>

CURRENT STATE (authoritative facts)
- <settled fact, approved decision, exact failure, or evidence address>

CONSTRAINTS / INVARIANTS
- <interface, behavior, safety, compatibility, or parallel non-overlap constraint>

ALLOWED SCOPE
- <exact owned files/symbols or bounded evidence question>

FORBIDDEN ACTIONS
- Do not modify: <outside ownership>
- DO NOT RESEARCH: <settled areas, decisions, or other-lane evidence scopes>
- Do not retain or reconstruct unrelated transcript/history.

RELEVANT FILES / ARTIFACTS
- <path, symbol/range, command output, artifact, or evidence address>

EXPECTED OUTPUT / VERIFICATION
- Run: <exact command>. Success: <concrete result>.
- Inspect: <exact diff/artifact/runtime state>. Success: <concrete evidence>.

STOP / ESCALATION
- Stop if <ambiguity, ownership conflict, risk boundary, or invalidated approach>.
- Return control if the same failure repeats without new evidence.
~~~

Owners and workers preserve concurrent edits and never revert unrelated work. Parallel
lanes require non-overlapping `ALLOWED SCOPE`, distinct outputs, and distinct `DO NOT
RESEARCH`/evidence scopes.

## Worker return contract

~~~text
WORK REPORT
STATUS / RESULT: complete | partial | blocked | rethink
DECISION / VERDICT: <when applicable, otherwise none>
EVIDENCE / ARTIFACTS: <exact commands, output, paths, or addresses>
FILES CHANGED: <actual files, or none>
UNRESOLVED RISKS / AMBIGUITIES: <items, or none>
STOP / ESCALATION REASON: <reason, or none>
UNIQUE CONTRIBUTION: <new evidence or deliverable unavailable from other lanes>
CONTEXT USED: files=<count>, ranges=<count>, evidence-items=<count>, expansions=<count/unavailable>
~~~

## Artifact handoff contract

Use this between an owner and reviewer or any downstream lane. Canonical file and
artifact references remain the source of truth; the handoff is an index, not a lossy
replacement.

~~~text
ARTIFACT HANDOFF
Objective: <observable outcome>
Acceptance criteria: <observable checks>
Hard constraints: <safety, compatibility, permission, and scope boundaries>
Changed files: <exact paths, or none>
Diff references: <base/head, patch, symbols, or ranges>
Test / verification results: <exact commands and observed results>
Created artifacts: <canonical paths/IDs/hashes, or none>
Important invariants: <must remain true>
Unresolved risks: <known unknowns, or none>
Exact questions for next agent: <bounded questions>
~~~

Exclude chain of reasoning, self-confidence, proposed verdicts, unnecessary full
conversation history, and repeated repository summaries. The next agent starts with
the handoff, performs targeted reads, and requests compact contextual expansion only
when a missing fact is material. Full history is the last resort under the strict
`fork_turns: all` gate.

## Stop signal and role lanes

On an architectural choice, material ambiguity, wider scope, judgment-heavy decision,
high-risk invariant, or systemic verification failure, return `WORKER STOP` with type,
trigger, exact evidence address, preserved owned work, owner/manager decision needed,
and one safe next step. A specification defect permits at most one corrected Luna
retry. A misclassified bounded worker lane can escalate directly to a Terra specialist;
that is not an owner switch and no Luna retry is required. Repeated failure without new
evidence stops. Evidence invalidating the architecture returns `rethink`, not another
local fix.

The initial owner is sticky: it owns research, execution, tests, correction, and
verification, and Strategy or executor cannot silently replace it. Open an owner gate
only for materially higher uncertainty, an architectural/strategic fork, unexpected
high-risk blast radius, invalidated original framing, or inability to continue
confidently. The only owner takeover is:

~~~text
Terra -> evidence-addressed ARTIFACT HANDOFF -> Sol takeover
~~~

After takeover Sol remains owner; no automatic downgrade or oscillation is allowed. A
Sol owner may delegate a large, isolated, low-uncertainty mechanical workload to Terra
only when the benefit exceeds handoff overhead. That bounded worker delegation leaves Sol
as owner and is not escalation or an owner switch.

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
completed Context Packet. For `diagnose-fix`, include reproduction, evidence,
falsifiable hypothesis, smallest discriminating experiment, and result; only confirmed
causal evidence permits the fix.

## Fresh Sol / High review

After owner verification, spawn exactly:

~~~text
agent_type: orchestra_sol_reviewer
fork_turns: none
~~~

Do not attach model or reasoning overrides. The reviewer receives:

~~~text
REVIEW OBJECTIVE
<Acceptance decision to independently check.>

ORIGINAL TASK CONTRACT
<User objective and authoritative acceptance criteria, without owner conclusions.>

AUTHORITATIVE CONSTRAINTS
- <invariants, interfaces, safety boundaries, excluded scope>

ARTIFACT HANDOFF
<Complete handoff contract with exact diff/evidence and unresolved risks.>

MINIMUM SOURCE ADDRESSES
- <paths, symbols, and ranges needed to test critical claims>

REVIEW SCOPE
Pass: initial | targeted re-review
Affected surface first: <required for targeted re-review>
Regression perimeter: <required for targeted re-review>

FORBIDDEN ACTIONS / CONTEXT
- Do not edit, implement fixes, or broaden scope.
- Do not receive or request the full owner/manager transcript, implementation reasoning,
  owner confidence, desired verdict, or conclusion-framed summary.

EXACT VERDICT RETURN
SOL REVIEW
VERDICT: ship | fix-first | rethink
REASON: <decisive evidence-based reason>
FINDINGS: <precise addresses and required fixes, or none>
MATERIAL ISSUES FOUND: <count>
RESIDUAL RISK: <most important remaining risk, or none>
CONTEXT USED: files=<count>, ranges=<count>, evidence-items=<count>, expansions=<count/unavailable>
~~~

The reviewer inspects actual files and evidence rather than trusting the handoff's
conclusions. `ship` terminates. `fix-first` allows the same owner one bounded correction
and a new fresh targeted re-review; the affected surface and regression perimeter are
checked before broader context. `rethink` returns to architecture. The default loop is
initial review plus one correction and one targeted re-review. Another cycle requires a
new material defect class exposed by the correction; otherwise stop. Any correction
invalidates the previous verdict. Review is independent from owner selection and never
replaces the owner or counts as owner escalation.

Use observed sandbox policy: if read-only is not observed and hard isolation is needed,
stop review; otherwise record exact before/after state and never claim enforced
read-only isolation.
