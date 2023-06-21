# Reusable GitHub Workflows

This repository hosts [re-usable github workflows][re-usable-github-workflows].

The repository includes:

- [add-to-project](.github/workflows/add-to-project.yaml) workflow: when a new
  issue or PR is added to a repository, it is also added to the [SynchroHub
  platform project](https://github.com/orgs/zaphiro-technologies/projects/2)
  with status `new`.
- [check-pr](.github/workflows/check-pr.yaml) workflow: when a new
  PR is added to a repository or any change occurs to the pr, the pr is
  validated to be sure that labels are valid.
- [markdown](.github/workflows/markdown.yaml) workflow: lint all markdown
  documents and checks that links referenced in the documents are valid.
- [release-notes](.github/workflows/release-notes.yaml) workflow: automatically
  updates release notes using PR titles and labels.

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

1. Ideally the workflow should be tested in this repository itself before
   being used in other repositories. In relation to this, it is then important
   that you trigger it with events such as `issues` or `pull_request` and that,
   for these events, that do not support input parameters, you find a way to
   pass default values. See [markdown](.github/workflows/markdown.yaml) workflow
   for one of the possible way to solve the issue.

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

Should you wish to advertise the re-usable workflow to your organization
developers in the `new action` page:

1. You need to create a template in the [`.github` repository][.github] in the
   folder [`workflow-templates`](https://github.com/zaphiro-technologies/.github/tree/main/workflow-templates):

    ```yaml
    name: Project Management
    on:
        issues:
            types:
            - labeled
        pull_request:
            branches: [ $default-branch ]
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
        "categories": [
            "Automation",
            "utilities"
        ]
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

[re-usable-github-workflows]: https://docs.github.com/en/actions/using-workflows/reusing-workflows
[octicon]: https://primer.style/design/foundations/icons/
[.github]: https://github.com/zaphiro-technologies/.github
[starter-workflows]: https://docs.github.com/en/actions/using-workflows/creating-starter-workflows-for-your-organization

change 2
