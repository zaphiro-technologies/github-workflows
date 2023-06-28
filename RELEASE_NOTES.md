# github-workflows Release Notes

## 0.0.2-dev - 2023-06-28

### Features

- use customized prettier action (PR #19 by @chicco785)

### Bug Fixes

- include a step using a sed script to remove the added `-` by
  `stefanzweifel/changelog-updater-action@v1. (PR #20 by @chicco785)
- Add jq to artefact clean up script (PR #12 by @chicco785)

### Continuous Integration

- use new action for markdown (PR #15 by @chicco785)
- Add job to clean up artefacts on pr closure (PR #9 by @chicco785)
- Add workflow to clean-up action cache on PR closure (PR #8 by @chicco785)

### Documentation

- Fake pr 2 (PR #5 by @chicco785)
- fake pr 1 (PR #4 by @chicco785)

## 0.0.1 - 2023-06-21

### Documentation

- fix workflows to work on `github-workflows` repository (PR #2 by @chicco785)
