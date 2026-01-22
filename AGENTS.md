# Repository Agents

This repository contains a collection of GitHub Actions workflows designed to
automate various tasks within our GitHub infrastructure. These workflows act as
agents to handle CI/CD processes, project management, and code quality checks.

## Available Workflows

### Project & Issue Management

- **Project Management** (`add-to-project.yaml`): Automatically adds issues and
  Pull Requests to a specified GitHub Project. It handles setting status fields,
  assigning reviewers, and managing permissions for PR creators. Additionally,
  it manages stale issues by:
  - Marking issues as stale if they're older than a configurable threshold
    (default 60 days) and not planned for current or future iterations
  - Automatically removing the stale label if an issue is added to an iteration
  - Closing stale issues after a configurable grace period (default 7 days) if
    they remain unplanned and inactive
  - Supporting dry-run mode for testing without making changes Runs daily via
    schedule, with configurable parameters via workflow_dispatch.
- **Auto-approve & Auto-merge** (`approve-and-merge.yaml`): Scheduled to run
  daily, this agent automatically approves and merges Pull Requests created by
  Dependabot to keep dependencies up-to-date.
- **Validate PR** (`check-pr.yaml`): Ensures Pull Requests meet specific
  criteria involved in review processes.

### Build & Deploy

- **Container Deployment** (`deployment.yaml`): Reusable workflow for deploying
  containerized applications to various environments.
- **Docker Build** (`docker.yaml`): Reusable workflow to build and push Docker
  images.
- **Publish New Release** (`new-release.yaml`): Orchestrates the creation of new
  software releases, including tagging and release artifact generation.

### Code Quality & Testing

- **Golang Lint & Test** (`golang.yaml`): Provides linting and testing
  capabilities specifically for Go projects.
- **Python Lint & Test** (`python.yaml`): Provides linting and testing
  capabilities specifically for Python projects.
- **Base Lint** (`markdown.yaml`): Performs lint checks on Markdown files to
  ensure documentation standards.
- **License Management** (`license.yaml`): Checks for license compliance within
  the repository dependencies.
- **Test Artifact** (`test-upload.yaml`): A workflow to test artifact upload
  functionality.

### Housekeeping & Maintenance

- **Clean Up Docker Images** (`clean-up-docker.yaml`): Automatically deletes
  Docker images associated with a Pull Request when it is closed.
- **Clean Up Storage** (`clean-up-storage.yaml`): Cleans up storage and caches
  associated with a branch when its Pull Request is closed.
- **Update Trivy Cache** (`trivy-cache-update.yaml`): A scheduled job to update
  the Trivy vulnerability database cache daily.
- **Release Notes** (`release-notes.yaml`): Generates and manages release notes
  for the project.
