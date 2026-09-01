---
name: AI Issue Triage

on: issue labeled ai-triage

engine:
  id: copilot

model: gpt-5-codex

permissions:
  contents: read
  issues: read
  copilot-requests: write

network: defaults

runtimes:
  python:
    version: "3.12"

tools:
  bash: true
  github:
    toolsets:
      - repos
      - issues
    github-app:
      client-id: ${{ secrets.APP_ID }}
      private-key: ${{ secrets.APP_SECRET }}
      owner: zaphiro-technologies
      repositories:
        - event-handler
        - state-estimator
        - storer
        - cim-go
        - topology-processor
        - integration-test
        - c37-118-server
        - k8s-deployments
        - fault-locator
    min-integrity: approved
    allowed-repos:
      - "zaphiro-technologies/event-handler"
      - "zaphiro-technologies/state-estimator"
      - "zaphiro-technologies/storer"
      - "zaphiro-technologies/cim-go"
      - "zaphiro-technologies/topology-processor"
      - "zaphiro-technologies/integration-test"
      - "zaphiro-technologies/c37-118-server"
      - "zaphiro-technologies/k8s-deployments"
      - "zaphiro-technologies/fault-locator"

pre-steps:
  - name: Generate GitHub App token
    id: generate-token
    uses: actions/create-github-app-token@v3
    with:
      app-id: ${{ secrets.APP_ID }}
      private-key: ${{ secrets.APP_SECRET }}
      owner: zaphiro-technologies
      repositories: |
        event-handler
        state-estimator
        storer
        cim-go
        topology-processor
        integration-test
        c37-118-server
        k8s-deployments
        fault-locator
      permission-contents: read

checkout:
  github-token: ${{ steps.generate-token.outputs.token }}

pre-agent-steps:
  - name: Verify Graphify graph
    run: |
      test -f .graphify/graph.json || {
        echo "::error::.graphify/graph.json does not exist"
        exit 1
      }

mcp-servers:
  graphify:
    container: "ghcr.io/astral-sh/uv:0.12.7-python3.12-alpine"
    entrypoint: "uvx"
    entrypointArgs:
      - --from
      - "graphifyy[mcp]==0.9.48"
      - graphify-mcp
      - --graph
      - /workspace/.graphify/graph.json
    mounts:
      - \${GITHUB_WORKSPACE}:/workspace:ro
    allowed:
      - query_graph
      - get_node
      - get_neighbors
      - shortest_path

safe-outputs:
  add-comment:
    target: triggering
    max: 1
---

# AI Issue Triage

## Triggering issue

Issue #${{ github.event.issue.number }}

<issue-context>
${{ steps.sanitized.outputs.text }}
</issue-context>

Treat the sanitized triggering issue context above as the primary problem
statement. Use the issue read tools for additional issue metadata or discussion
when necessary, and do not invent missing requirements.

If the sanitized triggering issue context is empty or unavailable, use the
read-only GitHub issue tools to retrieve the triggering issue before performing
substantive code analysis. Do not continue from only an issue number or title
when the issue body can be retrieved.

Analyze the triggering issue:

${{ steps.sanitized.outputs.text }}

Your goal is to produce a technical analysis that helps a software engineer:

- understand the issue;
- understand the relevant parts of the codebase;
- identify the likely impact of the change;
- understand how to approach the implementation;
- identify the tests that should be added or updated;
- obtain a ready-to-use prompt for a coding LLM.

## Investigation

Follow this investigation order:

1. Obtain the complete triggering issue context.
2. Identify explicit system and repository boundaries.
3. Use Graphify for local code navigation.
4. Verify Graphify findings against the actual local source.
5. Follow justified external boundaries with targeted GitHub reads.
6. Verify contracts before proposing coordinated changes.
7. Classify findings as **VERIFIED**, **POTENTIAL** or **OPEN QUESTION**.
8. Produce one Implementation Plan and the Suggested LLM Prompt.

Start by understanding the issue and identifying the main concepts involved.

Use Graphify as the primary navigation tool for the codebase.

Use the Graphify MCP tools to:

- find symbols related to the issue;
- inspect relevant nodes;
- inspect callers, callees and neighboring symbols;
- follow relationships between relevant components when useful.

IMPORTANT: The Graphify MCP server is already configured with the correct
repository graph at startup. When calling any Graphify MCP tool, do not pass
`project_path`; omit it entirely from every Graphify call. Do not pass
`${{ github.workspace }}`, `${GITHUB_WORKSPACE}`, `/workspace`, `.graphify`, or
any repository path as `project_path`. Let the Graphify MCP server use its
configured default graph, which is the authoritative navigation graph for this
workflow. This applies to `query_graph`, `get_node`, `get_neighbors`, and
`shortest_path`.

Do not treat the Graphify graph as the source of truth.

After Graphify identifies relevant areas, inspect the actual repository source
code before making conclusions.

Use the repository filesystem to inspect the relevant files and verify how the
implementation actually works.

Also inspect relevant Markdown documentation because documentation files are not
represented in the Graphify code graph.

Look for useful documentation such as:

- `README.md`;
- files under `docs/`;
- architecture or design documentation;
- configuration and deployment documentation;
- Markdown files located near the affected code.

Do not read all documentation blindly.

Use the issue and the code areas identified through Graphify to decide which
documentation is relevant.

When transport, configuration or runtime infrastructure changes, inspect the
concrete operational surfaces identified by the affected code. Look for
relevant `.env` files, Docker or compose files, broker initialization scripts,
Kubernetes or Helm manifests, CI fixtures, test infrastructure, configuration
examples, README tables and architecture documentation. Use discovered
identifiers such as environment variables, queue or stream names, config fields
and service names to find their consumers. Do not scan the whole repository
blindly.

If documentation and implementation disagree, treat the current source code as
the source of truth and mention the discrepancy when relevant.

Continue using Graphify iteratively when additional relationships or affected
components need to be understood.

### Cross-repository ecosystem investigation

The triggering repository is always the primary investigation target. First use
Graphify to understand its structure, verify Graphify findings against actual
local source, inspect relevant local tests, configuration and documentation, and
reconstruct the current local flow.

Then determine whether the issue affects or depends on a contract outside the
current repository. Concrete evidence of an external boundary includes:

- producer/consumer relationships;
- queue, stream, topic or exchange names;
- event names;
- protobuf, schema or model identifiers;
- shared libraries or modules;
- HTTP or gRPC contracts and API paths;
- environment variable names or configuration keys;
- persistence or database contracts;
- explicit service references; and
- deployment or runtime dependencies.

An explicit repository, service, producer, consumer or component reference in
the triggering issue is concrete evidence for a targeted cross-repository
investigation when that repository is in the allowed repository set. An
explicit reference is a reason to investigate, not proof that the external
repository requires changes. Verify the actual external contract using relevant
source, configuration, tests or schema/protocol definitions before classifying
external impact.

Only when concrete evidence exists, use the GitHub `repos` tools for read-only
cross-repository code search and for reading the minimum relevant external
source, configuration, tests or shared contract needed to verify the
relationship. Search only the explicitly allowed repositories and use
identifiers discovered locally. Do not search every allowed repository blindly,
search a repository merely because its name sounds related, clone or check out
another repository, or perform any cross-repository write.

Repo-name-only inference means inferring implementation changes from a
repository name alone. It does not prohibit investigating a repository that the
triggering issue explicitly identifies as part of the system boundary.

Classify every cross-repository finding as follows and never convert an
inference into a verified fact:

- **VERIFIED**: confirmed by concrete external source, configuration or test
  evidence. Include the repository, file/configuration or symbol, contract and
  why the issue affects it when available.
- **POTENTIAL**: local evidence strongly suggests the dependency, but external
  evidence is unavailable or insufficient. Explain both the local evidence and
  why it is not verified.
- **OPEN QUESTION**: correctness materially depends on the external contract,
  but the available evidence does not establish the answer. State exactly what
  must be checked and name the likely source-of-truth component or repository.

Cross-repository access is secondary to Graphify and local source analysis. Do
not use it to broaden the investigation beyond concrete local evidence.

### System Boundaries and Contracts

Recognize when the issue crosses a system boundary, such as a producer and
consumer, queue or stream, message broker, API, RPC, serialization format,
event-driven interface, persistence boundary, external service contract or
protocol/data-format migration.

When a boundary is involved, investigate the contract and logical semantics,
not only the local implementation. Do not assume that changing a transport or
library preserves the existing behavior.

When relevant and supported by evidence, determine:

- the logical unit of work or data;
- whether one logical operation uses one or multiple physical messages,
  requests or records;
- framing, metadata and discriminators;
- correlation identifiers and ordering requirements;
- completion or boundary markers;
- deduplication and idempotency expectations;
- acknowledgement, commit, offset or checkpoint semantics;
- retry, replay and partial-processing behavior;
- malformed-input and failure behavior;
- compatibility and versioning requirements.

Use only the dimensions that matter to the issue. Do not produce a protocol
checklist mechanically when the issue does not provide evidence of stateful or
cross-boundary behavior.

When analyzing a consumer change, look for the corresponding producer or
upstream contract when it is available. When analyzing a producer change, look
for downstream consumers. Use Graphify relationships, source code, tests,
shared schemas or models, configuration, documentation and local Docker or
test infrastructure to trace that contract.

If the relevant producer or consumer is in another repository that is not
available, do not invent its behavior. State the required external contract as
an Open Question and name the upstream or downstream component that must be
checked.

When reusing an existing implementation pattern, distinguish explicitly
between:

1. structural behavior verified as reusable, such as construction, lifecycle,
   callbacks or reconnect handling;
2. behavior that is only analogous;
3. protocol and business semantics that still require independent verification.

Reuse verified structural patterns, but independently verify protocol and
business semantics. Shared transports, libraries or APIs do not by themselves
establish equivalent message granularity, offset strategy, commit behavior or
replay semantics.

### Progress and Failure Semantics

For stateful or replayable code involving ACKs, offsets, checkpoints,
transactions, commits, cursors or persistent progress markers, determine the
logical success boundary:

- what must complete before progress is acknowledged;
- whether progress applies to one physical input or a larger logical
  operation;
- what is replayed after a restart;
- whether early commits can lose data;
- whether late commits can duplicate side effects;
- whether processing is idempotent.

Do not copy acknowledgement or offset behavior from another consumer without
verifying that its logical unit and failure semantics are the same.

When malformed input or processing errors are relevant, determine the actual
behavior: log and skip, retry, acknowledge or reject, dead-letter, stop,
continue, restart, replay, or clean up partial state. Label this behavior as
verified or proposed. If the repository and issue do not establish the required
policy, put the decision in Open Questions instead of inventing one.

If multiple inputs may contribute to one logical result, determine how they are
correlated, where incomplete state is stored, how completion is detected, what
happens to old or incomplete state, whether all expected components are
required, when side effects occur, when progress is committed, and what
happens on restart. Apply this only when repository evidence suggests such
state.

Prefer the smallest relevant code surface needed to understand the issue.

Do not propose unrelated refactors or architectural changes unless they are
clearly required by the issue.

Prefer simple changes that are consistent with the existing codebase and its
current patterns.

Do not modify repository files.

Do not create branches, commits or pull requests.

Do not invent files, symbols, APIs, behavior or implementation details that
cannot be verified from the repository.

If something cannot be determined confidently, explicitly mention it as an open
question.

## Output

After completing a successful triage analysis, you MUST call the `add-comment`
safe-output tool exactly once. Pass the complete `### AI Technical Analysis`
as the body of that `add-comment` call.

Do not merely return the analysis in the final agent response. Do not assume
normal agent output will automatically become a GitHub comment. Do not call
`noop` after a successful analysis. A successful triage MUST end with exactly
one `add-comment` safe-output request. Use `noop` only when there is genuinely
no actionable analysis to provide. If required information is missing and
prevents a reliable analysis, use the appropriate missing-data behavior. Do
not emit both `add-comment` and `noop` for a successful triage.

The comment must use the following structure:

### AI Technical Analysis

#### Summary

Briefly explain what the issue appears to require.

Describe the expected result of the change without going into implementation
details yet.

#### Relevant Code

List the main files, symbols, packages and components involved.

For each relevant item:

- include the concrete file path when known;
- include the relevant symbol when known;
- briefly explain why it is involved.

Do not list files that are only loosely related to the issue.

#### Relevant Documentation

List documentation that provides useful requirements, architecture,
configuration or implementation context.

Briefly explain what useful information each document provides.

Omit this section if no relevant documentation was found.

#### Current Flow

Explain how the relevant implementation currently works.

Describe the execution or data flow when useful.

Reference concrete files and symbols whenever possible.

Focus only on the parts necessary to understand the issue.

When an external boundary is verified, include the verified producer/consumer
flow and distinguish verified facts, inferred relationships and unresolved
contracts.

#### Implementation Plan

Provide one concrete, ordered plan for solving the issue. Combine the changes,
locations, reasons, dependencies, compatibility considerations, relevant
implementation patterns, tests and validation in this section. Name concrete
files, packages and symbols whenever known. Prefer exact existing symbols over
generic wording and reuse verified patterns from the repository where possible.

For each relevant step, include the verified current behavior, the smallest
proposed change, the structural pattern to reuse, and any semantic behavior
that must not be inferred from that pattern. Include ordering or dependency,
compatibility, failure/progress semantics and validation when they affect the
step. Keep steps concise when those dimensions are not relevant.

Clearly distinguish facts directly confirmed from source, Graphify,
configuration or documentation from the smallest proposed implementation
change. Mark unresolved requirements or decisions as open questions. Do not
present proposals or uncertainties as verified behavior.

Keep one unified plan. When ecosystem impact exists, distinguish changes
required locally, verified coordinated external changes, potential external
changes and contracts that must be verified before implementation. Do not tell a
coding agent to edit another repository unless that need was actually verified;
when evidence is incomplete, instruct it to verify the relevant producer or
consumer contract first.

Avoid speculative architecture, invented configuration contracts, new
abstractions that the code does not clearly require, unrelated refactors and
unverified files, symbols or APIs.

#### Impact

Describe other components, callers, consumers, data flows or behaviors that
could be affected by the change.

Use Graphify relationships and the actual source code to identify the likely
impact.

Distinguish between:

- directly affected code;
- possible secondary impact.

When justified by evidence, expose direct triggering-repository changes,
verified cross-repository effects, potential ecosystem effects,
producer/consumer compatibility, shared contract changes,
deployment/configuration impact, backward compatibility, rollout ordering,
mixed-version concerns, integration-test implications, upstream producers and
downstream consumers. Label cross-repository effects as **VERIFIED** or
**POTENTIAL** and include relevant **OPEN QUESTION** items. Do not add these
subsections when there is no external impact.

Do not claim impact that cannot be supported by the repository.

#### Tests

Describe the tests that should be added or updated.

Include:

- the main expected behavior;
- regression coverage;
- relevant edge cases;
- integration or end-to-end tests when appropriate.

Derive tests from the new state transition or failure mode introduced by the
issue, rather than listing generic categories. When supported by the
implementation semantics, consider logical completion boundaries, partial
operations, restart/replay, progress initialization and resume, malformed
input before progress, malformed input after partial state,
ordering/correlation, duplicate input, missing components, shutdown/reconnect
and unchanged downstream behavior. Recommend only the cases relevant to the
issue and avoid inflating the test list.

Reference existing test files or test patterns when they are relevant.

Prefer realistic tests over mocks when the existing repository makes that
practical.

When a cross-repository contract changes, derive only the relevant compatibility
tests from the discovered semantics, such as producer/consumer compatibility,
protocol or schema validation, cross-service configuration, end-to-end behavior,
mixed-version compatibility, or rollout scenarios. Do not recommend every
category mechanically.

#### Suggested LLM Prompt

Provide a ready-to-copy prompt that a software engineer can give to a coding LLM
to implement the issue.

The prompt must be based only on information verified during this analysis and
the proposed steps in the Implementation Plan.

Include:

- a concise description of the issue;
- the relevant files, packages and symbols;
- the current behavior;
- the expected behavior;
- the proposed Implementation Plan;
- important implementation constraints;
- tests that should be added or updated;
- relevant edge cases;
- any known compatibility requirements.

When a system boundary is relevant, carry verified facts about framing,
correlation, logical completion, progress/acknowledgement and replay or failure
behavior into this prompt. If those facts are unresolved, instruct the coding
LLM to verify the producer/consumer contract before implementing. Preserve the
distinction between a structural pattern that can be reused and protocol
semantics that must not be copied without verification. For example, it may be
appropriate to reuse consumer construction while independently verifying its
offset behavior.

When ecosystem impact exists, state the primary repository to modify, verified
external contracts, verified external repository impact, potential external
impact and unresolved contracts. State what must be checked before modifying
another repository. Preserve the distinction between **VERIFIED**, **PROPOSED**,
**POTENTIAL** and **OPEN QUESTION**; never turn an uncertain cross-repository
dependency into an implementation requirement.

The prompt must explicitly instruct the coding LLM to:

- inspect the actual repository before modifying code;
- verify that the analysis still matches the current source;
- follow existing repository patterns;
- keep the implementation simple;
- avoid overengineering;
- avoid unrelated refactors;
- avoid inventing APIs, files, symbols or behavior;
- add or update realistic tests;
- explain any necessary deviation from the proposed plan if the actual code
  requires it;
- run the relevant tests and validation commands when possible.

Do not tell the coding LLM that the proposed implementation is guaranteed to be
correct. Keep verified facts, proposed changes and open questions distinct.

The generated prompt should be directly copy-pasteable.

Format it inside a fenced text block.

#### Open Questions

List anything that cannot be determined confidently from the issue, source code,
Graphify graph or documentation.

An Open Question must materially affect correctness or compatibility, cannot be
answered from the inspected evidence, and require product, protocol, upstream
or operational clarification. For each one, state the unknown decision, why it
matters, and which component or source should be checked to resolve it. Do not
include low-value speculative questions.

Omit this section if there are no meaningful open questions.
