# Native operations

This reference operates Orchestra's policy on native Codex agents. There is no custom
router service, state machine, token estimator, or manager agent. In `adaptive-v2`, the
primary Sol / High session is the Router and final acceptor. The Router classifies domain
risk, independent scope, verified-context freshness, owner/model, strategy, budget,
verification floor, topology, and review value, then selects one execution graph. It is
immutable between explicit escalation gates and otherwise executes without reselection.

## Deterministic adaptive-v2 routing

Evaluate domain risk, scope, owner signals, topology, execution budget, verification, and
review value independently. Safety gates override economy; scope and verified evidence
determine machinery.

### Independent scope classification

Classify these dimensions before graph freeze. Domain risk is the consequence of a wrong
change and is not a substitute for any of them:

| Dimension | Qualitative values and evidence |
|---|---|
| Change size | `tiny`, `small`, `medium`, `large`; combine touched files/subsystems, contracts/schema, `production-vs-diagnostic`, `new-behavior-vs-instrumentation`, and `refactor-vs-additive` evidence. LOC is never sufficient alone. |
| Blast radius | `isolated`, `local`, `cross-component`, `systemic`; how far a mistake can propagate, separate from domain risk |
| Behavior impact | `none`, `shadow-only`, `internal`, `user-visible`, `data-affecting` |
| Novelty/uncertainty evidence | `known architecture`, `analogous verified path`, `previous verified iteration`, or `new subsystem/unknown behavior/external dependency` |
| Reversibility | `trivial`, `localized`, `stateful/migration`, or `destructive/high-cost` |

Do not infer a size or budget from LOC, risk, or one signal in isolation. A tiny or small
change can be high domain risk, and a low-risk large change can still require heavy
machinery because of its cross-component blast radius or verification floor.

### Minimal VERIFIED CONTEXT and freshness

Keep a minimal evidence record in the current task or handoff, never in a persistent
database:

~~~text
VERIFIED CONTEXT
Repo/worktree: <exact repository and worktree path>
Base: <exact HEAD, or proven descendant relationship>
Freshness proof: <same repo/worktree + exact HEAD plus relevant-path worktree/index check showing unchanged, or proven descendant plus relevant-path since-base and current worktree/index checks>
Relevant files: <path identities; hashes only where file identity matters>
Frozen artifacts: <identities/hashes only where artifact identity matters, or none>
Relevant config: <paths/keys; hash/version only where identity matters>
Architecture map/invariants: <canonical addresses and required invariants>
Evidence timestamp/source (optional): <command/task/handoff; timestamp is supporting only>
Context freshness: fresh | stale | not established
~~~

Same repo/worktree plus exact HEAD proves source freshness only with a relevant-path
worktree/index check showing those paths unchanged. A proven descendant requires checking
relevant-path changes since base plus the current worktree/index. Hash only identity-sensitive
files, config, or artifacts; do not hash everything by default. A relevant staged or
unstaged path change makes the record stale and forbids reuse; normal preflight resumes.
Timestamp or copied prose is never proof; when freshness is proven, do not reread known
architecture.

### Initial-owner signals

The Router records only qualitative signals needed for the owner decision:

| Signal | Values and meaning |
|---|---|
| Uncertainty | `low`, `medium`, or `high` confidence in the task framing and expected path |
| Risk | `low`, `medium`, or `high` domain/implementation impact if the interpretation or change is wrong |
| Blast radius | `isolated`, `local`, `cross-component`, or `systemic` propagation scope, recorded independently |
| Verifiability | `objective`, `partial`, or `low` strength of tests, oracle, or acceptance evidence |
| Task nature / reasoning | `mechanical/bounded`, `reasoning-heavy architecture/problem-framing`, or `mixed` |

Complexity remains a low/medium/high telemetry field only; it never selects the owner.
Do not add numeric scoring, numeric thresholds, keyword rules, or another owner signal.

The exact initial-owner rule is:

- `Terra` requires all of: low uncertainty, low/medium domain risk, isolated/local blast
  radius, high/objective verifiability, and mechanical/bounded task nature.
- `Sol` is selected for high uncertainty, reasoning-heavy architecture/problem-framing,
  high cost of a wrong interpretation, high domain risk or blast radius with less-than-high
  verifiability, or mixed signals.
- Mixed or unresolved signals conservatively fall back to `Sol`.

Owner selection does not inspect strategy, topology, execution budget, verification floor,
or review value. Those are separate dimensions of the same immutable graph.

### Topology and review graph

The selected Strategy executes this graph and cannot reselect the owner, parallelism,
budget, verification floor, or review requirement.

| Observable condition | Topology | Non-owner calls | Manager |
|---|---|---:|---|
| Connected work; low/medium risk; one evolving surface | `owner-only` | 0 | no |
| Explicit review request or high independent review value | `owner-review` | 1 fresh reviewer after owner verification | no |
| At least two independent deliverables, non-overlapping ownership, no required intermediate dependency | `orchestrated-parallel` | one per justified lane | yes, for decomposition/synthesis |
| Named expertise/context boundary with a concrete unique deliverable | `owner-specialist` | 1 specialist by default | no |
| Dynamic decomposition, multi-lane synthesis, or unresolved routing ambiguity | `manager` | only justified lanes | yes |
| Decomposable but sequentially dependent/shared surface | `owner-only` | 0 | no |

`Non-owner calls` counts workers and reviewers, not the selected owner. A Terra
`owner-only` run therefore has zero non-owner calls but one spawned owner invocation.

Classify complexity as low/medium/high for telemetry, but do not route to a worker only
because complexity is high. Domain risk is high when failure can materially affect
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

### Execution budget selection

After domain risk, all scope dimensions, owner/model, and strategy classification, select
an independent `Execution budget: FAST | STANDARD | HEAVY`. Risk determines confidence
and required invariants; scope and verified evidence determine machinery. No single
signal—especially risk or LOC—may choose the budget alone.

| Budget | Qualitative gate |
|---|---|
| `FAST` | `tiny` or `small`, `isolated` or `local`, bounded/shadow-only and objectively verifiable, known architecture, high reversibility, and sufficient fresh verified context |
| `STANDARD` | `medium` or interacting local scope, production-internal behavior, moderate uncertainty, or focused evidence that exceeds the FAST contract without broad reconstruction |
| `HEAVY` | `large` or `systemic`, cross-component production behavior, schema/stateful or migration work, destructive/high-cost reversibility, substantial architectural uncertainty, or a required broad integration/corpus floor |

High domain risk does not disqualify a tiny mechanical or shadow-instrumentation change
from FAST when output identity is objective and every required invariant is covered. A
low-risk large change can still be HEAVY. Do not pre-escalate just in case and do not
silently downgrade.

### Verification ladder and floor

The Router derives a required floor from concrete invariants and starts with the cheapest
check able to falsify the change:

| Level | Evidence |
|---|---|
| `L0` | static sanity, diff inspection, deterministic reasoning |
| `L1` | focused test, compile, or contract check |
| `L2` | targeted integration/runtime check or representative fixture |
| `L3` | full corpus, full build, broad regression, or multiple environments |

Record both `Verification plan` and `Verification floor`. Acceptance must reach the
floor; FAST never skips an invariant requiring L2 or L3. Cold or warm infrastructure
changes order and early falsification only, never permission to omit the floor. If a
cheap pass leaves a critical invariant unproven, continue to L2/L3.

The FAST contract is:

~~~text
minimal freshness check -> one primary owner/executor -> bounded change -> L0 -> focused L1 -> manager/owner diff acceptance -> done
~~~

Absent an escalation signal, FAST does not perform deep architecture reconstruction,
broad corpus work, multiple worker roles, review, or heavy artifact ceremony.

### Review-value gate

`Review value: low | medium | high` is independent from implementation/domain risk. Review
is mandatory only for an explicit request or a named safety/contract boundary with high
independent information value:

- `low` means objective output identity and focused tests leave no material independent
  information gap; no fresh reviewer is selected absent an explicit request.
- `medium` means a reviewer may be useful for one named interpretation or evidence gap.
- `high` means fresh review is selected for an explicit request or material independent
  value: ambiguity, plausible interpretations, non-objective verification, high-impact
  contract/judgment, adversarial need, or bias risk.

High risk alone must not force review when a tiny mechanical change has objective focused
tests/output identity. Medium scope with high review value may use `owner-review` without
HEAVY. Required safety and invariant checks remain mandatory regardless of review value.

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
2. The packet carries a `VERIFIED CONTEXT` record or explicitly says freshness is not
   established; reuse has a minimal proof for exact repo/worktree/base, relevant-path
   changes, identity-sensitive hashes, and architecture invariants.
3. Paths, symbols, ranges, commands, and evidence are task-relevant.
4. Settled facts replace transcript narration.
5. Allowed scope is exact and non-overlapping.
6. `DO NOT RESEARCH` prevents duplicate exploration.
7. The lane can verify its deliverable without reopening the repository.
8. `fork_turns` is explicit and any non-`none` reason is material.

Before review or a downstream lane, create `ARTIFACT HANDOFF` using the exact contract
in `role-contracts.md`. Send canonical addresses, not copied artifacts or owner
reasoning. The receiver follows this context ladder:

1. Handoff.
2. Targeted canonical file/artifact reads.
3. Compact expansion for one named missing fact.
4. Full historical context only under the rare strict `all` gate.

Do not impose hard token caps. When a soft budget is exposed, use it to reconsider
topology, duplicate references, and expansion—not to kill sound reasoning. A stale or
invalid context record restores normal preflight; it does not authorize a shortcut.

## Owner verification and integration

Worker reports and handoffs are claims. The owner inspects actual files, the complete
relevant diff, changed-file scope, requested checks, and runtime/artifact evidence.
Parallel synthesis belongs to the manager/owner and must preserve every lane's safety
boundary.

Run verification in ladder order: L0 static/diff sanity, the focused L1 falsifier, then
only the minimum L2/L3 needed to meet the concrete floor. Classify any failed verification
as `code`, `harness`, `infrastructure`, `flaky/non-deterministic`, or
`specification/architecture`; apply the smallest correction or discriminating check and
rerun only the minimum required level. Never blindly rerun an expensive command.

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
6. Before implementing the correction, the owner records its exact scope and applies the
   post-review materiality gate below; after correction, the owner confirms the class
   against the actual diff and evidence.
7. The class selects exactly one assurance action: fresh full review, targeted independent
   re-review, or deterministic owner verification.

| Class | Semantic impact | Required action |
|---|---|---|
| `MATERIAL` | Changes intended production behavior or an external contract; changes architecture, security/safety properties, or experiment hypothesis/definitions; changes evidence interpretation in a way that changes the main conclusion, crosses reviewed surfaces, or invalidates a critical boundary; changes acceptance criteria or main conclusion/verdict; or leaves a substantive implementation path without a bounded regression perimeter. It invalidates the full review or a critical boundary. | Bounded correction -> owner verification -> fresh full independent review |
| `TARGETED` | Changes one isolated substantive claim, function, boundary, test assumption, or isolated artifact interpretation while the accepted evidence meaning and main conclusion remain unchanged, restoring already-reviewed semantics. Architecture, intended behavior/contract, safety properties, acceptance criteria, and neighboring paths remain unchanged; affected surface and regression perimeter are bounded. | Bounded correction -> owner verification -> targeted independent re-review of the affected surface and regression perimeter |
| `NON-MATERIAL` | Comments, wording, formatting, typo, report phrasing, provenance description, deterministic manifest/hash regeneration, path/name metadata, or already-established factual representation with no substantive conclusion change | Bounded correction -> deterministic owner verification -> terminate without a reviewer |

Materiality is semantic, not proportional to line count: a one-line security, threshold,
or decision change can be `MATERIAL`; a large generated diff can be `NON-MATERIAL` only
when deterministic verification proves semantic equivalence. When ambiguous, use the
higher-assurance class justified by risk; a high-risk boundary may escalate `TARGETED` to
`MATERIAL`, but no change is automatically material. `MATERIAL` takes precedence whenever
one of its critical-boundary or invalidation conditions applies.

For `TARGETED`, the re-review packet contains the original relevant finding, exact
correction, minimal diff/context, affected surface, regression perimeter, and an explicit
bounded question. It does not restart the full task. For `NON-MATERIAL`, deterministic
verification must address the actual correction: for example raw-log comparison for
provenance, content identity plus regenerated-hash validation for manifests, or exact diff
inspection for comments/wording.

Record the gate visibly:

~~~text
POST-REVIEW MATERIALITY
Finding: <precise finding>
Correction scope: <exact bounded correction>
Semantic impact: <what reviewed meaning or behavior changes or remains unchanged>
Class: MATERIAL | TARGETED | NON-MATERIAL
Invalidated scope: <exact reviewed scope affected>
Action: fresh full independent review | targeted independent re-review | manager deterministic verification
Full reviewer: required | not required
~~~

The prior verdict remains valid for unchanged reviewed scope; only the semantically affected
scope is invalidated. The first full review is normal. A second full review is allowed after
a material correction. A third full review requires all three facts: the second reviewer
found a new material defect, its correction changes substantive state, and the owner records
why targeted verification is insufficient. This is an escalation gate rather than a numeric
cap, so a real critical defect can still receive another full review. Repeated wording,
provenance, deterministic artifact, or summary corrections do not qualify.

Do not use a new reviewer merely to reset the loop. The owner never sends self-confidence,
a desired verdict, or conclusion-framed reasoning.

## Sticky owner and explicit escalation

The initial owner owns research, execution, tests, correction, and verification for the
run. Strategy and executor follow the Router-selected graph; neither may silently
override its owner, topology, or review requirement. If `Terra` is the initial owner,
primary Sol remains Router/final acceptor and does not duplicate Terra's implementation
lane.

Open the owner-escalation gate only for materially higher uncertainty, an
architectural/strategic fork, an unexpected high domain-risk or blast-radius finding,
invalidated original framing, or the owner's inability to continue confidently. Encode the takeover as an
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
- Route and budget changes require a new `SELECTIVE ROUTE` or `ORCHESTRA ROUTE` naming
  the new evidence; never change them silently.

Execution-budget escalation is monotonic: `FAST -> STANDARD -> HEAVY`. Escalate only for
scope expansion, failed verification, an invalid architecture assumption, unexpected
behavior, a hidden dependency, flaky/non-deterministic evidence, new worker risk, or an
invariant that cannot be proved cheaply. Do not pre-escalate just in case. The update
must identify the exact evidence, previous/final budget, and minimum new verification:

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

After a failure, classify it before any rerun as `code`, `harness`, `infrastructure`,
`flaky/non-deterministic`, or `specification/architecture`. Apply the smallest correction
or discriminating check, then rerun only the minimum required level. If the same failure
repeats without new evidence, stop or emit a `STRATEGIC CHECKPOINT`; do not blindly rerun
an expensive command.

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

Record the compact `ORCHESTRA RUN` from `SKILL.md`. Optional detail keys remain here rather
than on every hot-path run: `Agent invocations:`, `Retries:`, `Review ROI:`, `Parallel ROI:`,
`Handoffs:`, `Context:`, and `Host metrics:`. Counts must describe actual topology:
owner-only means zero workers/reviewers, while a Terra owner still counts as one spawned
agent invocation. Preserve separate `initial_owner`, `owner_selection_reason`,
`owner_escalations`, `owner_switches`, `reviewer_count`, and `worker_count` (optional metadata
keys: `initial_owner:`, `owner_selection_reason:`, `owner_escalations:`, `owner_switches:`,
`reviewer_count:`, and `worker_count:`). Compact terminal
metadata records budget start/final/escalations, scope/context freshness, verification
plan/floor, review value, and escalation evidence; it is not an analytics system. The
`reviewer_count` excludes workers; `worker_count` excludes the owner and reviewer. Agent
invocations count spawned agents, including a spawned Terra owner.

For handoffs, count each file/artifact/evidence address occurrence as one
`reference-slot`. Normalize exact repeated addresses to count `unique-references`.
When both are measured:

~~~text
duplicate-reference-slots = reference-slots - unique-references
~~~

This is a narrow structural proxy, not token or semantic duplication. It does not measure
repeated prose, tokens, or savings. Handoff chars, targeted reads, repeated reads, and
expansions are reported only when the exact payload/tool evidence makes them
observable; otherwise use `unavailable/not-tracked`.

Optional forms include `Review ROI: invoked=<yes|no>; reason=<...>; cycles=<count>;
material-issues=<count>; result-changed=<yes|no>; correction-required=<yes|no>`,
`Parallel ROI: used=<yes|no>; reason=<...>; independent-tasks=<count>;
unique-useful-outputs=<count>`, `Handoffs:`,
`Context:`, and `Host metrics:`. Review ROI records invocation reason, cycles, material issues, whether the result
changed, and whether correction was required. The owner derives `result-changed=yes`
only when review causes correction, rethink, or a different terminal decision, and
`correction-required=yes` only from `fix-first`; the context-clean reviewer never
compares against an owner conclusion it did not receive. Parallel ROI records why work
was parallelized, independent task count, and unique useful outputs. Do not infer value
from agent count alone. A reviewer is not an owner switch or owner escalation; reviewer
and worker counts exclude the owner.

Host token/context metrics are included only when directly exposed: `input_tokens`,
`cached_input_tokens`, `output_tokens`, `reasoning_tokens`, `tool_calls`, and `duration`.
Otherwise write
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
