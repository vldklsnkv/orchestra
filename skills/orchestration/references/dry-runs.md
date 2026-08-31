# Strategy dry runs

These examples validate routing semantics without performing implementation. Paths and
symbols are illustrative. Each packet is intentionally narrow and complete enough to
show the lane boundary.

## 1. Tiny one-file bug -> solo

Decision:

~~~text
SELECTIVE ROUTE
Strategy: solo
Risk: low
Ambiguity: low
Decomposable: no
Implementation: Sol
Parallel: no
Review: no
~~~

Why: one localized null check with an obvious focused test costs less to inspect, fix,
and verify than to specify and preflight an auxiliary. No worker is spawned, so no
Context Packet exists. This is the required trivial-task no-agent case.

## 2. Bounded UI implementation -> delegate

Decision:

~~~text
SELECTIVE ROUTE
Strategy: delegate
Risk: low
Ambiguity: low
Decomposable: no
Implementation: Luna
Parallel: no
Review: no
~~~

Why: design, component API, ownership, and acceptance are settled; execution is
mechanical and objectively verifiable.

Luna Context Packet:

~~~text
GOAL
Add the specified loading state to ProfileCard and pass its focused snapshot test.
STRATEGY / ROLE
Strategy: delegate; Role: Luna bounded worker; Lane: profile-card-loading.
IMPLEMENTATION SPEC
Compose existing Spinner and Card variants; add isLoading without changing default UI.
RELEVANT FILES / SYMBOLS / RANGES
- Sources/UI/ProfileCard.swift: ProfileCard body and initializer.
- Tests/UI/ProfileCardTests.swift: loading-state snapshot case.
KNOWN FACTS
- Spinner and spacing tokens already exist in the shared UI library.
RELEVANT EVIDENCE
- Design acceptance: loading replaces content but preserves card size.
INTERFACES / INVARIANTS
- Existing initializer calls compile unchanged; tokens only.
OWNED FILES / SYMBOLS
- ProfileCard initializer/body; one focused test case.
DO NOT TOUCH
- Spinner, Card, token definitions, other profile screens.
DO NOT RESEARCH
- Component inventory and loading-state design; both are settled above.
VERIFICATION
- Run: focused ProfileCard tests. Success: all pass.
- Inspect: diff. Success: only owned symbols changed.
STOP / ESCALATION CONDITIONS
- Stop if backward compatibility requires a new architecture or token.
~~~

## 3. Risky architectural change -> expert + review

Decision:

~~~text
SELECTIVE ROUTE
Strategy: expert
Risk: high
Ambiguity: medium
Decomposable: no
Implementation: Terra
Parallel: no
Review: yes
~~~

Why: persistence migration changes high-risk invariants across releases. Terra is
selected immediately; independent acceptance is worth the review overhead.

Terra Context Packet:

~~~text
GOAL
Migrate encrypted session storage without data loss or downgrade ambiguity.
STRATEGY / ROLE
Strategy: expert; Role: Terra expert worker; Lane: session-storage-migration.
IMPLEMENTATION SPEC
Implement the approved versioned migration and atomic rollback boundary.
RELEVANT FILES / SYMBOLS / RANGES
- Sources/Auth/SessionStore.swift: load/save/migrate.
- Sources/Auth/SessionEnvelope.swift: schema version contract.
- Tests/Auth/SessionMigrationTests.swift: v1 fixtures and rollback cases.
KNOWN FACTS
- Schema v2 and key-rotation policy are approved; v1 remains readable for one release.
RELEVANT EVIDENCE
- ADR-014 sections 2-4; failing rollback fixture output in artifacts/migration.log.
INTERFACES / INVARIANTS
- Never write plaintext; atomic commit; failed migration preserves original bytes.
OWNED FILES / SYMBOLS
- SessionStore migration path, SessionEnvelope version decode, migration tests.
DO NOT TOUCH
- Keychain entitlements, account API, production secrets, unrelated auth UI.
DO NOT RESEARCH
- Chosen cipher, schema shape, and support window; ADR-014 settles them.
VERIFICATION
- Run: Auth migration suite. Success: v1/v2/rollback cases pass.
- Inspect: fixture bytes before/after failure. Success: identical originals.
STOP / ESCALATION CONDITIONS
- Stop with rethink if atomic rollback cannot preserve the invariant.
~~~

Reviewer packet after Sol verification:

~~~text
TASK CONTRACT
Preserve encrypted v1 sessions while migrating atomically to v2.
RELEVANT CHANGE SET
Exact diff for SessionStore, SessionEnvelope, and migration tests.
INTERFACES / CONSTRAINTS
- No plaintext; rollback preserves original bytes; v1 compatibility for one release.
VERIFICATION EVIDENCE
- Auth migration suite output and before/after fixture hashes.
MINIMUM SOURCE CONTEXT
- SessionStore.migrate, SessionEnvelope.decode, atomic-write helper, rollback tests.
~~~

## 4. Five independent mechanical changes -> parallel

Decision:

~~~text
SELECTIVE ROUTE
Strategy: parallel
Risk: low
Ambiguity: low
Decomposable: yes (5 independent lanes)
Implementation: Luna
Parallel: yes
Review: no
~~~

Why: five adapters have the same frozen rename but live in separate files, tests, and
symbols. No lane needs another's result. The host may schedule them in capacity-sized
batches without changing the independent-lane contract.

Context Packet template instantiated once per adapter A-E:

~~~text
GOAL
Rename Adapter<X>.legacyFetch to fetch under the frozen compatibility contract.
STRATEGY / ROLE
Strategy: parallel; Role: Luna bounded worker; Lane: adapter-<X> of five.
IMPLEMENTATION SPEC
Rename implementation and its focused test; retain deprecated forwarding alias.
RELEVANT FILES / SYMBOLS / RANGES
- Sources/Adapters/<X>.swift: Adapter<X>.legacyFetch.
- Tests/Adapters/<X>Tests.swift: legacy and new entry-point tests.
KNOWN FACTS
- New signature and deprecation window are approved.
RELEVANT EVIDENCE
- Compiler inventory lists exactly one implementation and one test file for this lane.
INTERFACES / INVARIANTS
- Deprecated alias forwards exactly; behavior and error mapping stay unchanged.
OWNED FILES / SYMBOLS
- Only the two <X> files and named symbols.
DO NOT TOUCH
- Adapters A-E belonging to other lanes; shared protocol; generated API docs.
DO NOT RESEARCH
- Rename rationale, other adapters, or shared protocol design.
VERIFICATION
- Run: focused Adapter<X> tests. Success: pass with deprecation coverage.
- Inspect: lane diff. Success: no cross-lane file changes.
STOP / ESCALATION CONDITIONS
- Stop if the shared protocol must change or another lane owns the same symbol.
~~~

## 5. Unknown regression -> diagnose-fix

Decision:

~~~text
SELECTIVE ROUTE
Strategy: diagnose-fix
Risk: medium
Ambiguity: high
Decomposable: no
Implementation: Terra
Parallel: no
Review: no
~~~

Why: the root cause is unknown and the failure crosses cache and network boundaries.
The packet authorizes diagnosis first, not a speculative patch.

Terra Context Packet:

~~~text
GOAL
Establish and fix the cause of duplicate requests after reconnect.
STRATEGY / ROLE
Strategy: diagnose-fix; Role: Terra expert worker; Lane: reconnect-duplication.
IMPLEMENTATION SPEC
Reproduce, gather evidence, state one falsifiable hypothesis, run the minimal discriminating
experiment, then fix only if confirmed and add a regression test.
RELEVANT FILES / SYMBOLS / RANGES
- Sources/Network/Reconnector.swift: reconnect and subscription lifecycle.
- Sources/Cache/RequestDeduper.swift: key insertion/removal.
- Tests/Network/ReconnectTests.swift: duplicate-request fixture.
KNOWN FACTS
- Regression begins after release 2.4; cold start does not reproduce.
RELEVANT EVIDENCE
- artifacts/reconnect-trace.json; exact failing test command and output.
INTERFACES / INVARIANTS
- One logical request per subscription; cancellation remains idempotent.
OWNED FILES / SYMBOLS
- Reconnector lifecycle, RequestDeduper only if causal evidence points there, focused tests.
DO NOT TOUCH
- Server, production cache data, unrelated retry policy.
DO NOT RESEARCH
- Cold-start path and serialization; existing traces exclude them.
VERIFICATION
- Reproduce first; record DIAGNOSIS block and discriminating result.
- After confirmed fix, rerun reproduction and focused network suite.
STOP / ESCALATION CONDITIONS
- Stop if the experiment is inconclusive or cause lies outside owned scope.
~~~

## 6. Competing architectural approaches -> explore

Decision:

~~~text
SELECTIVE ROUTE
Strategy: explore
Risk: medium
Ambiguity: high
Decomposable: yes (3 independent hypotheses)
Implementation: mixed
Parallel: yes
Review: no
~~~

Why: no implementation is authorized until Sol compares evidence for three competing
architectures. Each lane investigates a different hypothesis, not the whole repository.

Packets share invariants but differ in the addressed scope:

~~~text
GOAL
Determine whether event ingestion should use polling, streaming, or a durable queue.
STRATEGY / ROLE
Strategy: explore; Role: <Luna bounded evidence | Terra expert>; Lane: <polling | streaming | queue>.
IMPLEMENTATION SPEC
Evaluate only <lane approach> against the stated load, failure, and operations criteria;
return evidence and a recommendation, no production implementation.
RELEVANT FILES / SYMBOLS / RANGES
- docs/ingestion-requirements.md: load/failure criteria.
- <approach-specific existing module or benchmark only>.
KNOWN FACTS
- Peak rate, durability target, and operational budget are settled.
RELEVANT EVIDENCE
- Existing benchmark fixture and incident summary relevant to this approach.
INTERFACES / INVARIANTS
- At-least-once delivery; bounded recovery time; no data loss on restart.
OWNED FILES / SYMBOLS
- No production files; optional lane-local scratch benchmark only.
DO NOT TOUCH
- Production ingestion, schemas, infrastructure, other hypothesis scopes.
DO NOT RESEARCH
- Competing approaches owned by other lanes; product requirements already settled.
VERIFICATION
- Run: approach-specific benchmark or document check. Success: comparable evidence table.
STOP / ESCALATION CONDITIONS
- Stop if a missing product decision prevents comparison.
~~~

Sol arbitrates the three reports against one comparison rubric and either freezes a
decision or returns `rethink`; agent consensus alone is not evidence.

## 7. Complex design then mechanical implementation -> plan-execute

Decision:

~~~text
SELECTIVE ROUTE
Strategy: plan-execute
Risk: medium
Ambiguity: high
Decomposable: no
Implementation: Luna after architecture freeze
Parallel: no
Review: no
~~~

Why: Sol resolves the API and state-machine choices first. Once frozen, the code change
is repetitive and bounded, so Luna executes without repeating architecture research.

Luna Context Packet after freeze:

~~~text
GOAL
Implement the approved upload state machine and its transition tests.
STRATEGY / ROLE
Strategy: plan-execute; Role: Luna bounded worker; Lane: frozen-upload-state-machine.
IMPLEMENTATION SPEC
Implement ADR-021 transition table exactly; no state or transition design is open.
RELEVANT FILES / SYMBOLS / RANGES
- Sources/Upload/UploadState.swift: enum and transition reducer.
- Tests/Upload/UploadStateTests.swift: transition table cases.
- docs/ADR-021.md: approved table only, sections 3-4.
KNOWN FACTS
- State names, retry terminality, and cancellation semantics are frozen.
RELEVANT EVIDENCE
- Sol architecture decision record ADR-021 and acceptance matrix.
INTERFACES / INVARIANTS
- Exhaustive reducer; impossible transitions return typed error; no side effects.
OWNED FILES / SYMBOLS
- UploadState, transition reducer, focused tests.
DO NOT TOUCH
- Uploader transport, persistence, UI, ADR-021.
DO NOT RESEARCH
- Alternative state models, retry policy, naming; architecture is frozen.
VERIFICATION
- Run: UploadStateTests. Success: every approved transition and rejection passes.
- Inspect: implementation against ADR table. Success: exact one-to-one mapping.
STOP / ESCALATION CONDITIONS
- Stop if the frozen table is internally inconsistent or requires a new state.
~~~
