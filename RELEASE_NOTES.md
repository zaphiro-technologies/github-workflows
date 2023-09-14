# github-workflows Release Notes

## 0.0.2-dev - 2023-09-13

### Features

- add-to-project workflow: make project url configurable as input parameter (PR
  #33 by @chicco785)
- add-to-project workflow: make labels configurable as inputs (PR #27 by
  @chicco785)
- Markdown workflow: use customized prettier action (PR #19 by @chicco785)

### Bug Fixes

- Release-notes wf: fix default configuration to include only current PR among
  open PRs (PR #34 by @chicco785)
- Markdown workflow: support both .md and .MD extension for markdown files (PR
  #24 by @chicco785)
- Markdown workflow: include a step using a sed script to remove the added `-`
  by `stefanzweifel/changelog-updater-action@v1` (PR #20 by @chicco785)
- Clean up storage workflow: Add jq to artefact clean up script (PR #12 by
  @chicco785)

### Continuous Integration

- use new action for markdown (PR #15 by @chicco785)
- Add job to clean up artefacts on pr closure (PR #9 by @chicco785)
- Add workflow to clean-up action cache on PR closure (PR #8 by @chicco785)

### Refactoring

- release notes workflow: remove work around to fix broken lists (PR #28 by
  @chicco785)

## 0.0.1 - 2023-06-21

### Documentation

- fix workflows to work on `github-workflows` repository (PR #2 by @chicco785)
