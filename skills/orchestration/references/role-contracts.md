# Native Codex role contracts

## Primary owner and conditional manager: Router and initial owner

In `adaptive-v2`, primary Sol / High is the Router and final acceptor. The Router records
domain risk, independent scope dimensions, verified-context freshness, owner/model,
strategy, execution budget, verification floor, topology, and review value before
selecting one execution graph containing initial owner (`Sol` or `Terra`), topology,
budget, and review requirement. The graph is immutable between explicit escalation
gates. The selected initial owner owns research, execution, tests, correction, and
verification for the run; primary Sol performs final acceptance without duplicating that
execution lane.

The initial owner is `Terra` only for low uncertainty, low/medium domain risk,
isolated/local blast radius, high/objective verifiability, and mechanical/bounded task
nature. `Sol` is selected for high uncertainty, reasoning-heavy
architecture/problem-framing, high cost of a wrong interpretation, high domain risk or
blast radius with less-than-high verifiability, or any mixed/unresolved signals. This
owner decision is independent from strategy, topology, execution budget, verification
floor, and review value.

The Router marks a manager topology only for dynamic decomposition, synthesis of
independent workers, or routing ambiguity that the deterministic table cannot resolve.
The selected owner performs decomposition and synthesis; primary Sol performs that
function only when Sol is the selected owner. This is a topology decision, not a
separate manager-agent spawn.

One owner is a successful Orchestra topology. Luna / Max and Terra / High are optional
workers or specialists unless Terra is the selected initial owner. Fresh Sol / High is an
independent reviewer only when explicitly requested or when a named safety/contract
boundary creates high independent information value; high risk alone does not require
review when objective focused tests close the gap. A reviewer never replaces the owner.

`legacy` retains the v0.4 contract: Sol manages and verifies, Luna implements bounded
or frozen work, Terra handles judgment-heavy or high-risk work, and fresh Sol review is
the explicit `review` modifier (or named high-information safety/contract boundary; high
risk alone is not automatic). The three role profiles and seven strategy names remain stable.

## Route and native context contract

Before task tools, Sol emits the compact `SELECTIVE ROUTE` from `SKILL.md`; it must expose
the grouped scope evidence, context freshness/address, owner/primary, one parallel/manager
decision, budget/floor/plan, review value/reviewer, additional-agent value, escalation,
and inheritance. Detailed classification guidance remains in `operations.md`.

~~~text
SELECTIVE ROUTE
Mode: adaptive-v2 | legacy; Strategy: <seven strategies>; Topology: <selected topology>
Risk: <low|medium|high>; uncertainty=<...>; verifiability=<...>; task=<...>
Scope: <tiny|small|medium|large>; Blast radius: <...>; Behavior impact: <...>
Novelty/uncertainty evidence: <...>; Reversibility: <...>
Context freshness: <fresh|stale|not established>; evidence=<minimal proof address/status>
Initial owner: <Sol|Terra>; Primary: <sticky owner>; Owner reason: <evidence>
Parallel: <no|yes; reason>; Manager: <no|yes; reason>
Additional agent value: <none|specific evidence>
Execution budget: <FAST|STANDARD|HEAVY>
Verification plan: <levels>; Verification floor: <L0|L1|L2|L3>
Review value: <low|medium|high>; Reviewer: <none|fresh Sol / High>
Escalation condition: <evidence for FAST -> STANDARD -> HEAVY, or none>
Context inheritance: <none|limited N|all>; Inheritance reason: <reason or none>
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

## Scope, budget, and evidence contract

Before graph freeze, record the independent qualitative dimensions: `Change size:
tiny|small|medium|large` from files/subsystems, contracts/schema,
`production-vs-diagnostic`, `new-behavior-vs-instrumentation`, and
`refactor-vs-additive` shape (LOC is never sufficient alone); `Blast radius:
isolated|local|cross-component|systemic`; `Behavior impact: none|shadow-only|internal|
user-visible|data-affecting`; `Novelty/uncertainty evidence: known architecture,
analogous verified path, previous verified iteration, or new subsystem/unknown
behavior/external dependency`; and `Reversibility: trivial|localized|stateful/migration|
destructive/high-cost`. Blast radius is separate from domain risk.

The current task or handoff may carry this minimal record, but no persistent database is
introduced:

~~~text
VERIFIED CONTEXT
Repo/worktree: <exact repository and worktree path>
Base: <base HEAD, or proven descendant relationship>
Freshness proof: <same repo/worktree + exact HEAD plus relevant-path worktree/index check showing unchanged, or proven descendant plus relevant-path since-base and current worktree/index checks>
Relevant files: <path identities; hashes only where file identity matters>
Frozen artifacts: <identities/hashes only where artifact identity matters, or none>
Relevant config: <paths/keys; hash/version only where identity matters>
Architecture map/invariants: <canonical addresses and required invariants>
Evidence timestamp/source (optional): <command/task/handoff; timestamp is supporting only>
Context freshness: fresh | stale | not established
~~~

Same repo/worktree plus exact HEAD proves source freshness only with a relevant-path
worktree/index check showing those paths unchanged. A proven descendant requires relevant-path
changes since base plus the current worktree/index check. Hash only identity-sensitive
files/config/artifacts, not everything by default. A relevant staged or unstaged path change
makes context stale and forbids reuse; normal preflight resumes. Timestamp is optional
supporting evidence, never sufficient; with proven freshness do not reread known architecture.

After risk, scope, owner/model, and strategy classification, choose `Execution budget:
FAST|STANDARD|HEAVY`. FAST is limited to tiny/small isolated/local bounded or
shadow-only/objective work with known architecture, high reversibility, and sufficient
verified context; high domain risk alone does not disqualify it. STANDARD covers medium,
interacting, production-internal, or moderately uncertain work. HEAVY covers large,
systemic, cross-component production, schema/migration/stateful or destructive work,
substantial architecture uncertainty, or a broad verification floor. No single signal,
especially risk or LOC, chooses the budget alone.

The verification ladder is `L0` static sanity/diff/deterministic reasoning, `L1` focused
test/compile/contract, `L2` targeted integration/runtime/representative fixture, and
`L3` full corpus/full build/broad regression/multiple environments. Derive the floor from
concrete invariants; FAST never skips an L2/L3 requirement, and cold/warm infrastructure
never permits omitting it. Start with the cheapest falsifier.

Review value is separate from risk: `low|medium|high`. Fresh review is selected only for
an explicit request or independent information value (ambiguity, plausible
interpretations, non-objective verification, high-impact contract/judgment, adversarial
need, or bias risk). High risk alone must not force review for a tiny mechanical change
with objective focused tests/output identity. Medium scope with high review value may
review without HEAVY.

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

VERIFIED CONTEXT
- <record address, freshness proof/status, relevant identities, only needed hashes,
  architecture map/invariants, and optional source timestamp; say not established absent>

CONSTRAINTS / INVARIANTS
- <interface, behavior, safety, compatibility, or parallel non-overlap constraint>

ROUTE / BUDGET / VERIFICATION
- <risk, scope, blast radius, behavior impact, novelty evidence, reversibility>
- Execution budget: <FAST | STANDARD | HEAVY>; verification plan/floor: <levels>
- Review value/reviewer: <low|medium|high; none or fresh Sol / High>

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
- Start with the cheapest falsifier. After a failed check classify it as `code`,
  `harness`, `infrastructure`, `flaky/non-deterministic`, or
  `specification/architecture`; apply the smallest discriminating check and rerun only
  the minimum required level.
- Inspect: <exact diff/artifact/runtime state>. Success: <concrete evidence>.

STOP / ESCALATION
- Stop if <ambiguity, ownership conflict, risk boundary, or invalidated approach>.
- Return control if the same failure repeats without new evidence.
~~~

Owners and workers preserve concurrent edits and never revert unrelated work. Parallel
lanes require non-overlapping `ALLOWED SCOPE`, distinct outputs, and distinct `DO NOT
RESEARCH`/evidence scopes.

For FAST, the bounded contract is:

~~~text
minimal freshness check -> one primary owner/executor -> bounded change -> L0 -> focused L1 -> manager/owner diff acceptance -> done
~~~

FAST has no deep architecture reconstruction, broad corpus, multiple worker roles,
reviewer, or heavy artifact ceremony absent evidence-driven escalation. Escalate
monotonically `FAST -> STANDARD -> HEAVY` only for scope expansion, failed verification,
invalid architecture assumptions, unexpected behavior, hidden dependencies,
flaky/non-deterministic evidence, new worker risk, or inability to prove an invariant
cheaply. A route/budget update names the exact evidence and minimum new floor; no
pre-escalation or silent downgrade is allowed.

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
Verified context: <record address, identity-sensitive hashes, and freshness proof/status>
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

Before rerunning a failed verification, classify the failure as `code`, `harness`,
`infrastructure`, `flaky/non-deterministic`, or `specification/architecture`. Use the
smallest correction or discriminating check and rerun only the minimum required level;
do not blindly rerun an expensive command.

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
