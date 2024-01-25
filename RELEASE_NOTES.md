# GitHub Workflows Release Notes

## 0.0.2-dev - 2024-02-05

### Features

- golang: remove code coverage annotations (PR #76 by @hiimjako)
- markdown workflow: extend link checker configuration example to allow 429
  status (PR #62 by @chicco785)
- golang: add docker login on test and benchmark workflows (PR #64 by
  @cosimomeli)
- docker workflow: add git and build information as build arguments (PR #63 by
  @cosimomeli)
- add workflow to support license management (PR #58 by @chicco785)
- docker workflow: add `pre-build` step (PR #57 by @cosimomeli)
- markdown workflow: add optional spell checker (PR #44 by @chicco785)
- add-to-project workflow: add support to assign multiple teams as reviewers
  (comma separated without space) (PR #42 by @chicco785)
- Add Docker, Golang and Docker Clean Up workflows (PR #54 by @cosimomeli)
- markdown workflow: run jobs only when there are changes to markdown related
  files (PR #52 by @chicco785)
- add-to-project workflow: set PR on creation to `🏗 In progress` and when ready
  to `🔖 Ready` (PR #50 by @chicco785)
- markdown workflow: exclude `vendor` folder from links check (PR #47 by @tejo)
- markdown workflow: exclude `vendor` folder from checks (PR #46 by @tejo)
- add-to-project workflow: automatically add reviewers without need of
  CODEOWNERS (PR #37 by @chicco785)
- add-to-project workflow: automatically assign PR to its creator (PR #36 by
  @chicco785)
- add-to-project workflow: make project URL configurable as input parameter (PR
  #33 by @chicco785)
- add-to-project workflow: make labels configurable as inputs (PR #27 by
  @chicco785)
- Markdown workflow: use customised prettier action (PR #19 by @chicco785)

### Bug Fixes

- golang workflow: use current branch if base_ref not available (PR #74 by
  @cosimomeli)
- markdown workflow: support correctly `.prettierignore` (PR #65 by @chicco785)
- pr-check workflow: pass correctly `input.labels` (PR #67 by @chicco785)
- markdown workflow: fix check to enable/disable spellchecker (PR #55 by
  @chicco785)
- golang workflow: add shell configuration to enable `pipefail` for benchmark
  job (PR #56 by @cosimomeli)
- add-to-project workflow: Fix assignment of reviewers also when PR is still in
  draft mode (PR #40 by @chicco785)
- Release-notes workflow: fix default configuration to include only current PR
  among open PRs (PR #34 by @chicco785)
- Markdown workflow: support both `.md` and `.MD` extension for markdown files
  (PR #24 by @chicco785)
- Markdown workflow: include a step using a `sed` script to remove the added `-`
  by `stefanzweifel/changelog-updater-action@v1` (PR #20 by @chicco785)
- Clean up storage workflow: Add `jq` to artefact clean up script (PR #12 by
  @chicco785)

### Continuous Integration

- Add dependabot (PR #81 by @chicco785)
- Lower annotation pollution on PRs (PR #68 by @hiimjako)
- use new action for markdown (PR #15 by @chicco785)
- Add job to clean up artefacts on PR closure (PR #9 by @chicco785)
- Add workflow to clean-up action cache on PR closure (PR #8 by @chicco785)

### Refactoring

- release notes workflow: remove work around to fix broken lists (PR #28 by
  @chicco785)

## 0.0.1 - 2023-06-21

### Documentation

- fix workflows to work on `github-workflows` repository (PR #2 by @chicco785)
