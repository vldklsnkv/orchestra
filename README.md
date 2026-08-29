# Orchestra

Orchestra is a Codex plugin for Sol-led selective delivery. Run the primary task
on GPT-5.6 Sol with high reasoning; Orchestra declares a route before tools and
uses pinned native custom-agent profiles when delegation or review is justified.

| Route | Delivery |
| --- | --- |
| `solo` | Sol / High plans, implements, verifies, and accepts. |
| `delegate` | Luna / Max handles bounded work or Terra / High handles complex work; Sol verifies. |
| `audit` | Sol implements and verifies; a fresh read-only Sol / High reviews. |
| `full` | One selected implementer, Sol verification, then a fresh Sol review. |

Solo is the default. Luna is for fully specified routine work; Terra is for
judgment-heavy, high-risk, context-heavy, or wide-blast-radius work. The primary
Sol session always owns architecture, routing, verification, and acceptance.

## Install companion agents

Plugin installation does not register user-owned agent TOMLs automatically. Run:

```sh
sh scripts/install-agents.sh
sh scripts/install-agents.sh --check
```

Then start a new Codex task on Sol / High and invoke:

```text
Use $orchestra:orchestration to build this feature and verify it.
```

## Verify the source

```sh
python3 -m unittest discover -s tests -v
```

The routing design and safety tooling are adapted under MIT from
[Sol Advisor](https://github.com/DannyMac180/sol-advisor) v0.6.0. See
[NOTICE.md](NOTICE.md) for attribution.
