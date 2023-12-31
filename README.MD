# Reusable GitHub Workflows

This repository hosts [re-usable github workflows][re-usable-github-workflows].

The repository includes:

- [add-to-project](.github/workflows/add-to-project.yaml) workflow: when a new
  issue or PR is added to a repository, it is also added - by default - to the
  [SynchroGuard platform project](https://github.com/orgs/zaphiro-technologies/projects/2)
  or to the project defined by `project-url` input parameter with status `new`.
  When a new PR is added, the PR is assigned to its creator. When a PR is set to
  ready, reviewers from `reviewers-team` input parameter (default value
  `backend-devs`) or `reviewers-individuals` (comma separated) are added.
- [check-pr](.github/workflows/check-pr.yaml) workflow: when a new PR is added
  to a repository or any change occurs to the PR, the PR is validated to be sure
  that labels are valid.
- [clean-up-storage](.github/workflows/clean-up-storage.yaml) workflow: when a
  new PR is closed, related cache and artefact are deleted.
- [markdown](.github/workflows/markdown.yaml) workflow: lint all markdown
  documents and checks that links referenced in the documents are valid. If
  `skip-spell-check: false`, also a spell checker is executed.
- [release-notes](.github/workflows/release-notes.yaml) workflow: automatically
  updates release notes using PR titles and labels.
- [golang](.github/workflows/golang.yaml) workflow: lint, test and benchmark Go
  Applications. The workflow includes authentication to Github Container
  Registry in case tests rely on private images. To retrieve the images, you
  need also to set
  [read permission](https://docs.github.com/en/packages/learn-github-packages/configuring-a-packages-access-control-and-visibility#ensuring-workflow-access-to-your-package)
  for the repository on the package.
- [docker](.github/workflows/docker.yaml) workflow: build and push Docker images
- [clean-up-docker](.github/workflows/clean-up-docker.yaml) workflow: when a PR
  is closed, related docker images and untagged ones are deleted
- [license](.github/workflows/license.yaml) workflow: add license in file
  headers and the license of dependencies.

Some of this workflows are configured as [starter workflows][starter-workflows]
in [`.github` repository][.github], so that you can add them at any time from
the actions page.

![Starter Actions](./screenshot.png)

## How to add a shared workflow to this repository

1. The new workflow need to be callable, i.e., include:

   ```yaml
   on:
     workflow_call:
   ```

   This type of trigger can also be used to specify input parameters as
   discussed in [re-usable github workflows][re-usable-github-workflows]
   documentation. In which case we recommend to also include default values.

1. Ideally the workflow should be tested in this repository itself before being
   used in other repositories. In relation to this, it is then important that
   you trigger it with events such as `issues` or `pull_request` and that, for
   these events, that do not support input parameters, you find a way to pass
   default values. See [markdown](.github/workflows/markdown.yaml) workflow for
   one of the possible way to solve the issue.

1. Once the new workflow is available in the main branch, you can call it using
   something like:

   ```yaml
   jobs:
     add-to-project:
       uses: zaphiro-technologies/github-workflows/.github/workflows/add-to-project.yaml@main
       secrets: inherit
   ```

   Of course, you can also test it from a branch, in which case you can replace
   `main` with the branch name.

## How to add a starter workflow to `.github` repository

Should you wish to advertise the re-usable workflow to your organisation
developers in the `new action` page:

1. You need to create a template in the [`.github` repository][.github] in the
   folder
   [`workflow-templates`](https://github.com/zaphiro-technologies/.github/tree/main/workflow-templates):

   ```yaml
   name: Project Management
   on:
     issues:
       types:
         - labeled
     pull_request:
       branches: [$default-branch]
       types:
         - labeled
     workflow_call:

   jobs:
     add-to-project:
       uses: zaphiro-technologies/github-workflows/.github/workflows/add-to-project.yaml@main
       secrets: inherit
   ```

1. You need to create a linked `.properties.json` file including the related
   metadata:

   ```yaml
   {
     "name": "Zaphiro Project Management",
     "description": "Zaphiro Project Management starter workflow.",
     "iconName": "octicon project",
     "categories": ["Automation", "utilities"],
   }
   ```

   For icons we leverage [octicon icons][octicon].

You can find more information in [starter workflows][starter-workflows]
documentation.

## References

- [re-usable github workflows][re-usable-github-workflows]
- [octicon icons][octicon]
- [`.github` repository][.github]
- [starter workflows][starter-workflows]

[re-usable-github-workflows]:
  https://docs.github.com/en/actions/using-workflows/reusing-workflows
[octicon]: https://primer.style/design/foundations/icons/
[.github]: https://github.com/zaphiro-technologies/.github
[starter-workflows]:
  https://docs.github.com/en/actions/using-workflows/creating-starter-workflows-for-your-organization
