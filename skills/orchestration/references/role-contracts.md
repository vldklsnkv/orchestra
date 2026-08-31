# Native Codex role contracts

Use these contracts with Orchestra's three namespaced, role-pinned native custom
agents. Do not add a role for every strategy. A strategy describes how work is
organized; a role describes which pinned agent is appropriate for a lane.

## Routing decision contract

Before task tools, Sol evaluates task size, ambiguity, reasoning complexity,
decomposability, risk or blast radius, objective verifiability, and orchestration
overhead. Emit:

~~~text
SELECTIVE ROUTE
Strategy: solo | delegate | expert | parallel | explore | plan-execute | diagnose-fix
Risk: low | medium | high
Ambiguity: low | medium | high
Decomposable: no | yes (<independent lane count>)
Implementation: Sol | Luna | Terra | Luna after architecture freeze | mixed
Parallel: no | yes
Review: no | yes
~~~

If orchestration overhead is comparable to the task, use `solo`. A later change must
name the new evidence. Never silently downgrade risk, add agents, or change roles.

## Role selection after strategy

- Sol / High is always manager and final acceptor.
- Luna / Max executes bounded or frozen specifications.
- Terra / High handles expert reasoning or implementation where judgment, complexity,
  risk, context, or blast radius is material.
- Fresh Sol / High is used only by the `review` modifier after manager verification.

Terra may be selected immediately. Do not require a failed Luna attempt. In
`plan-execute`, Sol or Terra may settle architecture, but Luna should execute the
mechanical frozen plan. In `explore`, give lanes distinct hypotheses or evidence
scopes. In `parallel`, ownership must not overlap.

## Context Packet contract

Every Luna or Terra prompt must contain this complete packet. Replace every
placeholder; use `none` only when it is genuinely empty.

~~~text
GOAL
<Observable outcome and why it matters.>

STRATEGY / ROLE
Strategy: <base strategy>
Role: Luna bounded worker | Terra expert worker
Lane: <unique lane name and its relationship to other lanes>

IMPLEMENTATION SPEC
<Frozen steps and decisions. For investigation lanes, state the hypothesis or evidence
scope and the required decision output instead of prescribing a conclusion.>

RELEVANT FILES / SYMBOLS / RANGES
- <path>: <symbol or narrow range and why it is relevant>

KNOWN FACTS
- <settled fact the worker may rely on>

RELEVANT EVIDENCE
- <command output, failure, artifact, or evidence location>

INTERFACES / INVARIANTS
- <signature, schema, behavior, safety boundary, or compatibility requirement>

OWNED FILES / SYMBOLS
- <exact file or symbol this lane may modify>

DO NOT TOUCH
- <files, symbols, state, data, or systems outside ownership>

DO NOT RESEARCH
- <already-settled repository areas or hypotheses that must not be rediscovered>

VERIFICATION
- Run: <exact command>
  Success: <concrete expected result>
- Inspect: <exact diff, artifact, or runtime state>
  Success: <concrete expected evidence>

STOP / ESCALATION CONDITIONS
- Stop if <lane-specific ambiguity, ownership, risk, or evidence condition>.
- Return control if the same failure repeats without new evidence.

RETURN
Return exact commands and actual evidence. A completion claim without evidence is
invalid.

WORK REPORT
STATUS: complete | partial | blocked | rethink
GOAL: <one-line restatement>
CHANGES: <file-by-file summary from the actual diff, or none>
EVIDENCE: <new facts and exact evidence locations>
VERIFIED: <exact commands and concrete output>
JUDGMENT CALLS: <decisions left open by the packet, or none>
GAPS: <unfinished work or none>
CONTEXT USED: files=<count>, ranges=<count>, evidence-items=<count>
~~~

Address context with paths, symbols, ranges, commands, and evidence locations. Do not
paste a repository-wide narrative when the worker can inspect a precise source slice.
Each parallel lane needs a distinct investigation scope and non-overlapping
`OWNED FILES / SYMBOLS`. Workers preserve concurrent edits and never revert unrelated work.

## Luna stop signal

Luna must not improvise across a material architectural boundary. When any stop
condition is met, return:

~~~text
WORKER STOP
TYPE: specification-error | misclassified | scope-conflict | systemic-failure | rethink
TRIGGER: <architectural choice, ambiguity, wider scope, judgment, invariant, or failure>
EVIDENCE: <exact file, range, command, or artifact>
OWNED WORK PRESERVED: <completed work and state>
MANAGER DECISION NEEDED: <precise decision or escalation>
SAFE NEXT STEP: <one bounded action, or none>
~~~

Rules:

- A wrong or incomplete specification permits at most one corrected Luna retry.
- Misclassified bounded work escalates directly to Terra; a retry is not required.
- Repeated failure without new evidence stops the lane.
- Evidence that invalidates the architecture returns `rethink`, not another local fix.

## Luna / Max lane

Use for bounded implementation in `delegate`, mechanical lanes in `parallel`, bounded
evidence collection in `explore` or `diagnose-fix`, and execution after architecture
freeze in `plan-execute`.

Spawn exactly:

~~~text
agent_type: orchestra_luna_implementer
fork_turns: none
~~~

Do not attach model or reasoning overrides. Prompt:

~~~text
ROLE
Act as Orchestra's bounded worker. Execute only the supplied Context Packet. Do not
rediscover settled areas or make unassigned architectural choices.

<paste and complete the Context Packet contract>
~~~

## Terra / High lane

Use for `expert`, expert lanes in `parallel` or `explore`, difficult root-cause
reasoning in `diagnose-fix`, or architecture reasoning in `plan-execute`. Select it
immediately when complexity or risk is already evident.

Spawn exactly:

~~~text
agent_type: orchestra_terra_implementer
fork_turns: none
~~~

Do not attach model or reasoning overrides. Prompt:

~~~text
ROLE
Act as Orchestra's expert worker. Resolve the supplied judgment-heavy Context Packet
within its ownership and evidence boundaries. Do not widen scope silently.

<paste and complete the Context Packet contract>
~~~

## Parallel lane contract

Before spawning, Sol must prove all of the following:

- Each lane has a distinct observable deliverable.
- Owned files or symbols do not overlap.
- Investigation hypotheses or evidence scopes do not duplicate one another.
- No lane requires another lane's intermediate result to make progress.
- Integration and combined verification remain owned by Sol.
- Agent count reflects useful independent work, not available capacity.

If any condition fails, use a sequential strategy. Parallel lanes may use Luna, Terra,
or both according to lane complexity; role selection remains strategy-secondary.

## Diagnose-fix evidence gate

Before a fix, the active lane or Sol must record:

~~~text
DIAGNOSIS
Reproduction: <exact command or steps and observed failure>
Evidence: <relevant output or artifact>
Hypothesis: <falsifiable causal claim>
Experiment: <minimal action that distinguishes this cause>
Result: confirmed | rejected | inconclusive
~~~

Only `confirmed` permits the causal fix. `rejected` requires a different hypothesis;
`inconclusive` requires better evidence, not a speculative patch. After the fix, rerun
the reproduction as regression verification plus relevant focused checks.

## Fresh Sol / High review modifier

After manager verification, spawn a new native thread exactly:

~~~text
agent_type: orchestra_sol_reviewer
fork_turns: none
~~~

Do not attach model or reasoning overrides. Observe the actual role, pin, sandbox
policy, and permission profile. Prompt:

~~~text
ROLE
Act as the fresh independent reviewer. Remain strictly read-only: do not edit files,
implement fixes, or broaden scope. Do not trust summaries where direct inspection is
possible.

TASK CONTRACT
<User goal and acceptance conditions.>

RELEVANT CHANGE SET
<Exact allowed files plus complete relevant diff or explicit base/head revisions.>

INTERFACES / CONSTRAINTS
- <Compatibility, invariants, repository rules, safety boundaries, excluded scope.>

VERIFICATION EVIDENCE
- <command> -> <actual manager-session output or artifact location>

MINIMUM SOURCE CONTEXT
- <paths, symbols, and ranges required to independently test critical claims>

REVIEW
Inspect the actual files, relevant change set, evidence, and critical boundaries. Judge
correctness, completeness, regressions, scope discipline, interface preservation, test
adequacy, and material risk.

SOL REVIEW
VERDICT: ship | fix-first | rethink
REASON: <decisive evidence-based reason>
FINDINGS: <precise file references and required fixes, or none>
RESIDUAL RISK: <most important remaining risk, or none>
~~~

Any post-review correction invalidates the verdict. Sol reviewing Sol is context-clean
independent checking, not cross-model-family independence.

Use observed isolation, not requested isolation:

- With observed `read-only`, proceed with enforced isolation.
- If the host broadens it, proceed only when hard isolation is not required, the prompt
  forbids edits, and Sol records exact before/after repository and artifact state.
- If isolation is unobservable, hard isolation is required, or mutation occurs, stop
  the lane and do not claim read-only review.
