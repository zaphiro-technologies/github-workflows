# Reusable GitHub Workflows

This repository hosts [re-usable github
workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows).

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

Some of this workflows are configured as [starter workflows](https://docs.github.com/en/actions/using-workflows/creating-starter-workflows-for-your-organization)
in [.github](https://github.com/zaphiro-technologies/.github),
so that you can add them at any time from the actions page.

![Starter Actions](./screenshot.png)
