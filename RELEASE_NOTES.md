# GitHub Workflows Release Notes

## 0.0.3-dev - 2024-05-21

### Features

- license, docker, golang, release notes workflows: support SBOM generation,
  license compatibility check and vulnerability check (PR #116 by @chicco785)
- Add the deployment workflow (PR #115 by @cosimomeli)
- markdown workflow: Use quiet mode for link checker (PR #112 by @chicco785)
- golang workflow: add input variable for alert threshold (PR #101 by
  @chicco785)
- docker workflow: execute only if the pr actor is not dependabot or labels
  contains `docker` (PR #99 by @chicco785)
- golang workflow: skip code coverage if the actor is dependabot (PR #100 by
  @cosimomeli)
- markdown workflow: run spellcheck only on actually changed \*.md files (PR #96
  by @chicco785)
- Support different grammar check modalities (local and online) in the script
  (PR #89 by @chicco785)

### Continuous Integration

- Move sonarcloud checks to test job (PR #119 by @chicco785)

### Dependencies

- Bump golangci/golangci-lint-action from 5 to 6 (PR #117 by @dependabot[bot])
- Bump golangci/golangci-lint-action from 4 to 5 (PR #110 by @dependabot[bot])
- Bump mikepenz/action-gh-release from 0.2.0.pre.a03 to 1 (PR #106 by
  @dependabot[bot])
- Bump actions/add-to-project from 1.0.0 to 1.0.1 (PR #107 by @dependabot[bot])
- Bump DavidAnson/markdownlint-cli2-action from 15 to 16 (PR #105 by
  @dependabot[bot])
- Bump apache/skywalking-eyes from 0.5.0 to 0.6.0 (PR #104 by @dependabot[bot])
- Bump actions/add-to-project from 0.6.0 to 1.0.0 (PR #103 by @dependabot[bot])
- Bump actions/add-to-project from 0.5.0 to 0.6.0 (PR #97 by @dependabot[bot])
- Bump golangci/golangci-lint-action from 3 to 4 (PR #91 by @dependabot[bot])
- Bump EndBug/add-and-commit from 4 to 9 (PR #93 by @dependabot[bot])
- Bump dawidd6/action-download-artifact from 2 to 3 (PR #94 by @dependabot[bot])
- Bump stefanzweifel/git-auto-commit-action from 4 to 5 (PR #92 by
  @dependabot[bot])

## 0.0.2 - 2024-02-09

### Features

- Run release note, license management and markdown workflows only on ready for
  review PRs (PR #72 by @chicco785)
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

- Compute correctly PR number in the case of PR review (PR #88 by @chicco785)
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

### Dependencies

- Bump actions/setup-go from 4 to 5 (PR #86 by @dependabot[bot])
- Bump actions/upload-artifact from 3 to 4 (PR #82 by @dependabot[bot])

### Refactoring

- replace check speller with npx gramma (PR #80 by @chicco785)
- release notes workflow: remove work around to fix broken lists (PR #28 by
  @chicco785)

## 0.0.1 - 2023-06-21

### Documentation

- fix workflows to work on `github-workflows` repository (PR #2 by @chicco785)
