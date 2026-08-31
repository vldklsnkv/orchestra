# Native operations

This is the maintainer and operator reference for Orchestra's native custom-agent
workflow. Keep strategy choice separate from role choice: strategies organize work;
the three installed TOMLs pin execution and review roles.

## Role pins and spawn contract

| Role type | Model | Effort | Use |
|---|---|---|---|
| orchestra_luna_implementer | gpt-5.6-luna | max | Bounded or frozen implementation and bounded evidence lanes |
| orchestra_terra_implementer | gpt-5.6-terra | high | Expert reasoning or complex/high-risk implementation lanes |
| orchestra_sol_reviewer | gpt-5.6-sol | high | Optional fresh review; requests read-only sandbox |

Select native context inheritance for every lane explicitly:

~~~text
agent_type: orchestra_luna_implementer | orchestra_terra_implementer | orchestra_sol_reviewer
fork_turns: none | <positive integer string N> | all
~~~

The interface defaults to `all` when omitted, so omission is forbidden. Default to
`none`. Use `<N>` only for materially necessary recent turns and record the concise
reason in `SELECTIVE ROUTE` and the worker packet. Use `all` only as a deliberate rare
fallback when reconstruction from the packet is unsafe because the exact full interaction
history is itself an explicitly addressed authoritative artifact that cannot be safely
paraphrased. Every packet still records all safety and scope boundaries; no unrecorded
constraint may control an allowed action; inherited turns are supplementary context only.
Independent review is always `fork_turns: none`. Do not attach model or reasoning
overrides. Missing, conflicting, unavailable, or unobservable role/model/effort is a hard
stop; never substitute another role.

## Installation and exactness checks

Plugin installation does not register user-owned companion TOMLs. At installation or
update time, run from the repository:

~~~sh
sh scripts/install-agents.sh
sh scripts/install-agents.sh --check
~~~

From an installed skill, resolve the same script relative to the skill directory:

~~~sh
skill_dir=<directory-containing-this-SKILL.md>
installer="$skill_dir/../../scripts/install-agents.sh"
sh "$installer" --check
~~~

The installer is fail-closed, preflights all destinations before mutation, and performs
an exact post-install comparison. It never overwrites a differing profile by default.
After a plugin update, synchronize only recognized Orchestra profiles explicitly:

~~~sh
sh scripts/install-agents.sh --update
sh scripts/install-agents.sh --check
~~~

`--update` validates exact role/model/effort identity, refuses foreign or unsafe files,
checks for concurrent change after preflight, keeps a backup of every replaced profile,
and prints each backup path.

For task-scoped preflight, check only selected role types:

| Selected lanes/modifiers | Required check |
|---|---|
| Sol-only `solo` | None |
| Any Luna lane | `--check --check-role luna` |
| Any Terra lane | `--check --check-role terra` |
| `review` modifier | `--check --check-role sol` |
| Multiple role types | Combine the corresponding `--check-role` arguments |

Examples:

~~~sh
sh scripts/install-agents.sh --check --check-role luna
sh scripts/install-agents.sh --check --check-role terra --check-role sol
sh scripts/install-agents.sh --check --check-role luna --check-role terra
~~~

Unknown or missing role arguments fail before destination mutation. Cache a successful
check only for the current task and unchanged routing configuration.

## Strategy and lane preflight

Before tools, Sol declares the base strategy and the `parallel` and `review` modifiers.
Then perform these checks before spawning:

- `solo`: no auxiliary or companion check.
- `delegate`: one bounded Luna lane.
- `expert`: one Terra lane selected immediately.
- `parallel`: at least two independent lanes with non-overlapping ownership and no
  required intermediate dependency. Preflight each distinct role type once.
- `explore`: distinct hypotheses or evidence scopes. Duplicate investigations are a
  routing error.
- `plan-execute`: architecture reasoning finishes before the Luna packet is frozen.
  Use Terra for reasoning only when its added judgment is material.
- `diagnose-fix`: record reproduction and evidence before hypothesis testing; do not
  authorize a fix until a discriminating experiment confirms the cause.
- `review`: add the fresh Sol check only when review is declared.

Choose the inheritance decision before spawning; it is separate from strategy and role.
For every mode (`none`, limited `<N>`, or `all`), every worker receives a complete,
self-contained authoritative packet. It must record the objective; ownership and
allowed scope; constraints and invariants; evidence/artifact addresses; forbidden
actions; `DO NOT RESEARCH` boundaries; expected verification; and stop conditions.
Inherited turns are supplementary context only and can never supply or replace a
missing safety boundary, permission, ownership, invariant, acceptance criterion, or
settled fact. Use `all` only as a deliberate rare fallback when reconstruction from the
packet is unsafe because the exact full interaction history is itself an explicitly
addressed authoritative artifact that cannot be safely paraphrased; even then, the
packet records every safety and scope boundary. No unrecorded constraint may control an
allowed action. Do not use retained context as a substitute for exact ownership,
evidence addresses, or `DO NOT RESEARCH` boundaries.

Do not allocate agents merely because capacity exists. For a trivial task, the
preflight itself is evidence that `solo` is cheaper.

## Runtime routing evidence

Public spawn/details metadata is authoritative for selected role and exposed
model/effort. If model or effort is omitted, inspect the exact native thread ID:

~~~sh
skill_dir=<directory-containing-this-SKILL.md>
runtime_inspector="$skill_dir/../../scripts/inspect-agent-runtime.sh"
sh "$runtime_inspector" <native-subagent-thread-id>
~~~

For a disposable fixture or non-default session root:

~~~sh
sh "$runtime_inspector" --sessions-dir /absolute/path/to/sessions <native-subagent-thread-id>
~~~

The helper searches one exact rollout filename suffix and emits only allowlisted
routing fields. It rejects invalid IDs, zero or multiple matches, missing fields, and
conflicting model/effort/sandbox/permission/cwd values. It never prints prompts,
messages, environment variables, tokens, configuration, or arbitrary rollout payloads.

Accepted routing is Luna / max, Terra / high, and Sol / high. If public and local
evidence both exist, they must agree. The inspector is evidence, not a model-selection
fallback.

## Context efficiency checks

Before sending a worker packet, Sol verifies:

1. Every path, symbol, range, command, and evidence location is task-relevant.
2. `CURRENT STATE (authoritative facts)` contains settled conclusions, not a transcript.
3. `FORBIDDEN ACTIONS` preserves `DO NOT RESEARCH` and outside-ownership boundaries.
4. `ALLOWED SCOPE` is exact and does not overlap another active lane.
5. Investigation lanes test different hypotheses or evidence scopes.
6. The worker can verify its own deliverable without reopening the whole repository.
7. `fork_turns` is explicit and any non-`none` selection has a concise material reason.

Do not claim token savings. The observable goal is less duplicated exploration,
context transfer, agent use, review, and failed iteration. Report packet shape as file,
range, and evidence-item counts. Do not parse private transcripts or build a workaround
for metrics unavailable from the host.

## Parent verification and integration

Workers return structured reports, but Sol independently inspects actual files, the
complete relevant diff, changed-file scope, requested checks, and runtime or artifact
evidence. Parallel integration and combined verification always belong to Sol.

For `plan-execute`, freeze the implementation packet after the architecture decision;
if implementation exposes a new architectural choice, Luna stops and returns control.
For `diagnose-fix`, keep the reproduction and discriminating experiment in the final
evidence so the regression check proves the established cause, not merely a green test.

## Retry, escalation, and checkpoint operations

- A specification defect allows one corrected Luna retry at most.
- Misclassification allows direct Terra escalation without a Luna retry.
- The same failure without new evidence stops the lane.
- An invalidated architecture produces `rethink`.
- A route change requires a new `SELECTIVE ROUTE` block naming the new evidence.

Continue while a pass adds evidence, reduces uncertainty, completes bounded work, or
changes the observed failure. Emit the `STRATEGIC CHECKPOINT` from the main skill for
two materially similar no-progress corrections, an invalidated core assumption,
oscillation, or an architectural mismatch. The new step must change the hypothesis,
architecture, decomposition, verification method, or evidence-backed route. Never use
a checkpoint to bypass routing, review, permission, or acceptance rules.

## Read-only reviewer interpretation

The reviewer profile requests `sandbox_mode = read-only`. Capture observed sandbox and
permission profile types:

- Observed read-only sandbox: isolation is enforced.
- Broader host policy: continue only when hard isolation is not required, the prompt
  forbids edits, and Sol captures exact before/after repository and artifact state.
- Unobservable isolation, required hard isolation, or mutation: stop review and do not
  claim read-only isolation.

The reviewer independently inspects critical claims and returns exactly `ship`,
`fix-first`, or `rethink`. It never implements. Any correction discards the verdict,
requires manager verification, and uses a new fresh reviewer.

## Run metadata

At completion or stop, record only observable fields:

~~~text
ORCHESTRA RUN
Strategy: <strategy>
Roles: <roles>
Agents: <count>
Lanes: <lane role/model fork_turns; or Sol-only>
Escalations: <count>
Retries: <count>
Review: used | not-used
Packets: worker files=<count>, ranges=<count>, evidence-items=<count>; reviewer files=<count>, ranges=<count>, evidence-items=<count>
Host metrics: input_tokens=<value> cached_input_tokens=<value> output_tokens=<value> tool_calls=<value> duration=<value> | unavailable/not-exposed
Result: complete | partial | blocked | rethink
Verification: pass | fail | partial (<evidence>)
~~~

Record host metrics only when the host exposes the exact values. Otherwise write
`unavailable/not-exposed`; never infer, parse private transcripts, or extend the
inspector as a workaround. This record is intentionally lightweight and is not a
workflow engine or state machine.

## Maintainer verification

From the repository root, run:

~~~sh
python3 -m unittest discover -s tests -v
sh scripts/install-agents.sh --check
git diff --check
git status --short
git diff --stat
~~~

For pre-install validation without touching user configuration, point the installer at
a temporary directory, then compare source and installed plugin trees using the normal
local plugin installation workflow. The contract tests cover manifest versioning,
exact role pins, all seven strategies, both modifiers, Context Packets, stop rules,
dry-run examples, fail-closed installer fixtures, and shell syntax.
