# Orchestra

Orchestra is a small strategy-first orchestration plugin for Codex. Sol / High remains
the manager and final acceptor, but it chooses how to organize work before choosing a
worker. Delegated lanes explicitly select native `fork_turns` and receive narrow,
addressed Context Packets so they can use known facts and evidence without repeating
repository-wide discovery.

Orchestra optimizes total useful work, not agent count. It does not claim token or time
savings without measured host evidence.

## Strategies

| Strategy | Delivery model |
|---|---|
| `solo` | Sol implements and verifies when orchestration overhead is not worthwhile. |
| `delegate` | Sol freezes bounded work, Luna / Max implements, Sol verifies. |
| `expert` | Sol scopes complex or high-risk work, Terra / High handles it, Sol verifies. |
| `parallel` | Independent non-overlapping lanes run concurrently; Sol integrates. |
| `explore` | Distinct hypotheses or evidence scopes are investigated; Sol arbitrates. |
| `plan-execute` | Sol or Terra settles architecture, then Luna executes the frozen plan. |
| `diagnose-fix` | Reproduce, evidence, hypothesis, experiment, fix, regression verification. |

Two modifiers compose with those strategies:

- `review` adds a fresh read-only Sol / High reviewer after manager verification.
- `parallel` adds independent lanes where ownership and intermediate dependencies do
  not overlap. The base `parallel` strategy is used when this is the task's main shape.

Terra can be selected immediately when complexity is evident. Luna never needs to fail
first. Trivial work stays `solo`; a reviewer is not added by habit.

## Roles

- **Sol / High** owns intent, architecture, strategy, decomposition, Context Packets,
  verification, escalation, arbitration, and final acceptance.
- **Luna / Max** executes bounded, fully specified or architecture-frozen work.
- **Terra / High** handles judgment-heavy, complex, high-risk, context-heavy, or
  wide-blast-radius reasoning and implementation.
- **Fresh Sol / High reviewer** independently inspects critical claims in a requested
  read-only sandbox and returns `ship`, `fix-first`, or `rethink`.

No additional agent roles are required by the seven strategies.

## Context policy and packets

Before every spawn, Orchestra records one native inheritance choice: `none`, a positive
integer-string `N`, or `all`. `none` is the default; limited `N` is allowed only when
recent turns are materially necessary; use `all` only as a deliberate rare fallback when
reconstruction from the packet is unsafe because the exact full interaction history is
itself an explicitly addressed authoritative artifact that cannot be safely paraphrased.
Any non-`none` choice has a concise reason. Reviewers always use `none`; omission is
forbidden because the native interface defaults it to `all`. Every packet still records
all safety and scope boundaries; no unrecorded constraint may control an allowed action,
and inherited turns are supplementary context only.

Every worker gets an explicit self-contained packet containing:

```text
ROLE
OBJECTIVE
CURRENT STATE (authoritative facts)
CONSTRAINTS / INVARIANTS
ALLOWED SCOPE
FORBIDDEN ACTIONS
RELEVANT FILES / ARTIFACTS
EXPECTED OUTPUT / VERIFICATION
STOP / ESCALATION
```

Paths, symbols, ranges, commands, and evidence locations are preferred over long prose.
`FORBIDDEN ACTIONS` includes `DO NOT RESEARCH` and exact outside ownership. Parallel
lanes require non-overlapping ownership and distinct evidence scopes. Review is a
minimal evidence-focused packet; it excludes manager transcripts, implementation-agent
reasoning, long discussions, and conclusion-framed summaries.

## Routing and stop rules

Before task tools, Orchestra emits a compact `SELECTIVE ROUTE` containing strategy,
risk, ambiguity, decomposability, implementation role, parallelism, and review use.

Luna stops when a supposedly bounded lane exposes architecture, material ambiguity,
substantially wider scope, judgment-heavy decisions, high-risk invariants, or a systemic
failure outside ownership. A specification defect permits one corrected Luna retry at
most. Misclassification can escalate directly to Terra. Repeated failure without new
evidence stops; an invalidated architecture returns `rethink`.

`diagnose-fix` does not permit a speculative patch before a minimal discriminating
experiment establishes the cause.

## Lightweight run record

At completion or stop, Orchestra records strategy, agents, each lane's role/model and
`fork_turns`, retries/escalations, review, packet file/range/evidence counts, result,
and verification. It records `input_tokens`, `cached_input_tokens`, `output_tokens`,
`tool_calls`, and `duration` only when directly exposed by the host; otherwise it writes
`unavailable/not-exposed` and never infers or parses private transcripts.

## Installation

Install the plugin through the normal local Codex plugin workflow. Companion profiles
are user-owned configuration and are installed separately:

```sh
sh scripts/install-agents.sh
sh scripts/install-agents.sh --check
```

The installer is selective and fail-closed. It validates exact profiles and refuses to
overwrite conflicts by default. After a plugin update, explicitly synchronize recognized
Orchestra profiles with a recoverable backup:

```sh
sh scripts/install-agents.sh --update
sh scripts/install-agents.sh --check
```

`--update` refuses foreign, unsafe, or identity-mismatched files and prints the backup
path for every replaced profile.

Start a new Codex task on GPT-5.6 Sol with high reasoning, then invoke:

```text
Use $orchestra:orchestration to choose a strategy, execute this task, and verify it.
```

The skill cannot switch the already-running primary model. It verifies Sol / High when
metadata is available and stops before delegation when the prerequisite is unconfirmed.

## Development and verification

```sh
python3 -m unittest discover -s tests -v
sh scripts/install-agents.sh --check
```

The contract suite covers the manifest, exact three-role pins, seven strategies,
modifiers, native inheritance policy, compact packets, escalation rules, targeted
dry-run examples, installer behavior, and shell syntax. Runtime metadata can be
inspected with:

```sh
sh scripts/inspect-agent-runtime.sh --help
```

Orchestra is released under the MIT License. The original role and safety tooling are
adapted from [Sol Advisor](https://github.com/DannyMac180/sol-advisor) v0.6.0; see
[NOTICE.md](NOTICE.md) for attribution.
