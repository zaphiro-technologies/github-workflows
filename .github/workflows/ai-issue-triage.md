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

Start by understanding the issue and identifying the main concepts involved.

Use Graphify as the primary navigation tool for the codebase.

Use the Graphify MCP tools to:

- find symbols related to the issue;
- inspect relevant nodes;
- inspect callers, callees and neighboring symbols;
- follow relationships between relevant components when useful.

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

If documentation and implementation disagree, treat the current source code as
the source of truth and mention the discrepancy when relevant.

Continue using Graphify iteratively when additional relationships or affected
components need to be understood.

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

Post exactly one comment on the triggering issue using the following structure:

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

#### Likely Changes

Describe the changes that would probably be required to implement the issue.

Reference concrete files, symbols or components whenever possible.

For each likely change, explain:

- what would change;
- why it would change;
- how it relates to the issue.

Do not include unrelated cleanup or refactoring.

#### Impact

Describe other components, callers, consumers, data flows or behaviors that
could be affected by the change.

Use Graphify relationships and the actual source code to identify the likely
impact.

Distinguish between:

- directly affected code;
- possible secondary impact.

Do not claim impact that cannot be supported by the repository.

#### Tests

Describe the tests that should be added or updated.

Include:

- the main expected behavior;
- regression coverage;
- relevant edge cases;
- integration or end-to-end tests when appropriate.

Reference existing test files or test patterns when they are relevant.

Prefer realistic tests over mocks when the existing repository makes that
practical.

#### Action Plan

Provide a concrete and ordered implementation plan for solving the issue.

The plan should be detailed enough that a software engineer could follow it step
by step.

For each step:

1. reference the relevant file, package or symbol when known;
2. explain what should be inspected or changed;
3. explain why the step is necessary;
4. mention dependencies on previous steps when relevant.

The plan should include:

- implementation steps;
- schema or configuration changes if required;
- compatibility considerations if relevant;
- tests to add or update;
- validation commands or checks when they can be inferred from the repository.

Keep the plan focused on the issue.

Avoid overengineering, speculative abstractions and unrelated refactors.

If multiple implementation approaches are possible, recommend the simplest
approach that is consistent with the current codebase and briefly explain why.

#### Suggested LLM Prompt

Provide a ready-to-copy prompt that a software engineer can give to a coding LLM
to implement the issue.

The prompt must be based only on information verified during this analysis.

Include:

- a concise description of the issue;
- the relevant files, packages and symbols;
- the current behavior;
- the expected behavior;
- the proposed action plan;
- important implementation constraints;
- tests that should be added or updated;
- relevant edge cases;
- any known compatibility requirements.

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
correct.

The generated prompt should be directly copy-pasteable.

Format it inside a fenced text block.

#### Open Questions

List anything that cannot be determined confidently from the issue, source code,
Graphify graph or documentation.

For each open question, briefly explain why it matters to the implementation.

Omit this section if there are no meaningful open questions.
