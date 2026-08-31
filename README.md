# Orchestra

Orchestra is a Codex plugin for risk-gated, Sol-led delivery. It keeps one primary agent responsible for architecture and acceptance, then adds implementation or review agents only when the task's complexity and blast radius justify them.

The goal is selective orchestration rather than maximum delegation. Straightforward work stays in one session. Broad, high-risk, or judgment-heavy work receives a clearly declared route, pinned agent roles, parent verification, and—when required—a fresh final review.

## Routing modes

Every Orchestra task declares one of four routes before task tools are used:

| Route | Delivery model |
| --- | --- |
| `solo` | Sol / High plans, implements, verifies, and accepts the work. |
| `delegate` | Luna / Max handles bounded routine work, or Terra / High handles complex work; Sol verifies the result. |
| `audit` | Sol implements and verifies, then a fresh read-only Sol / High reviewer inspects the accumulated change. |
| `full` | One selected implementer completes the work, Sol verifies it, and a fresh Sol reviewer performs final acceptance review. |

`solo` is the default. Orchestra escalates only when the observed risk supports it and never silently substitutes a different model, effort, role, or review policy.

## Agent responsibilities

- **Sol / High** owns intent, architecture, route selection, task decomposition, verification, escalation, and final acceptance.
- **Luna / Max** handles bounded, fully specified implementation work where speed and execution are the main concerns.
- **Terra / High** handles judgment-heavy, context-heavy, high-risk, or wide-blast-radius implementation.
- **Fresh Sol / High reviewer** performs behavioral read-only review for `audit` and `full`, returning `ship`, `fix-first`, or `rethink`.

Delegated work substitutes for primary-agent implementation; it is not duplicated for appearance. Worker reports are treated as claims until the primary session verifies the actual diff and evidence.

## Installation

Install the Orchestra plugin through the normal local Codex plugin workflow. Companion agent profiles are user-owned configuration and are not registered automatically by plugin installation.

From the repository, install and verify the pinned profiles:

```sh
sh scripts/install-agents.sh
sh scripts/install-agents.sh --check
```

The installer is selective and fail-closed. It validates profile identity and refuses to proceed when required files or expected contracts do not match.

Start a new Codex task on GPT-5.6 Sol with high reasoning, then invoke:

```text
Use $orchestra:orchestration to declare a route, build this feature, and verify it.
```

Orchestra confirms the primary model and effort before any delegated lane. If runtime metadata cannot prove them, it asks the user to confirm Sol / High rather than assuming.

## Review and safety model

- Routes are declared in a machine-auditable `SELECTIVE ROUTE` block.
- Only agents selected by that route are preflighted and spawned.
- Workers receive explicit ownership, interfaces, constraints, and verification requirements.
- The primary session independently checks changed-file scope, tests, runtime evidence, and repository state.
- Evidence-backed stagnation triggers a strategic checkpoint: preserve progress, invalidate the failed approach, and begin a bounded new cycle only with a materially different next step and success signal.
- A reviewer never implements its own fixes. `fix-first` returns the work to the designated implementation lane and requires a new fresh review.
- Observed sandbox and permission limits are reported accurately; Orchestra does not claim enforced isolation when it is unavailable.

## Development and verification

Run the contract suite:

```sh
python3 -m unittest discover -s tests -v
```

Inspect runtime metadata for a specific agent session when the host exposes it:

```sh
sh scripts/inspect-agent-runtime.sh --help
```

Orchestra is released under the MIT License. The routing design and safety tooling are adapted from [Sol Advisor](https://github.com/DannyMac180/sol-advisor) v0.6.0; see [NOTICE.md](NOTICE.md) for attribution.
