# References

- [Markup Languages](#markup-languages)
  - [Markdown](#markdown)
  - [YAML](#yaml)
- [Platforms](#platforms)
  - [EditorConfig](#editorconfig)
  - [`git`](#git)
  - [GitFlow](#gitflow)
  - [GitHub Flow](#github-flow)
  - [{{ cookiecutter.git_hosting_service }}](#{{ cookiecutter.git_hosting_service.lower().replace(' ', '-') }})
- [Programming Languages](#programming-languages)
  - [Python](#python)
- [Tools](#tools)
  - [pre-commit](#pre-commit)
- [Software Engineering](#software-engineering)
  - [Community Health](#community-health)
  - [Continuous Integration and Delivery](#continuous-integration-and-delivery)
  - [Licensing](#licensing)
  - [Logging](#logging)
  - [Release Notes and Changelogs](#release-notes-and-changelogs)
  - [Security](#security)
  - [Versioning](#versioning)

## Markup Languages

### Markdown

1. <https://daringfireball.net/projects/markdown/syntax>: Original Markdown syntax
2. <https://www.markdownguide.org/basic-syntax>: Markdown Guide: Basic Syntax
3. <https://www.markdownguide.org/cheat-sheet>: Markdown Guide: Cheat Sheet

### YAML

1. <https://stackoverflow.com/questions/22268952/what-is-the-difference-between-yaml-and-yml-extension>: `.yaml` and `.yml` extension discussion
2. <https://yaml.org/refcard.html>: YAML reference card
3. <https://yaml.org/spec/>: YAML specification

## Platforms

### EditorConfig

1. <https://editorconfig.org>: EditorConfig
2. <https://github.com/jokeyrhyme/standard-editorconfig>: Standard EditorConfig example

### `git`

1. <https://fileinfo.com/extension/gitattributes>: `.gitattributes` file extension reference
2. <https://git-scm.com>: `git`
3. <https://git-scm.com/book>: Pro Git book
4. <https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup>: First-time Git setup
5. <https://git-scm.com/docs>: `git` documentation
6. <https://git-scm.com/docs/gitattributes>: `gitattributes` documentation
7. <https://git-scm.com/docs/gitignore>: `gitignore` documentation
8. <https://gitforwindows.org>: Git for Windows
9. <https://github.com/git/git>: `git` source repository
10. <https://gitignore.io>: `.gitignore` template generator
11. <https://stackoverflow.com/questions/63241071/automate-git-merge-commit-message>: Automating Git merge commit messages
12. <https://www.atlassian.com/git/tutorials/inspecting-a-repository/git-tag>: Git tag tutorial
13. <https://www.atlassian.com/git/tutorials/setting-up-a-repository/git-config>: Git configuration tutorial

### GitFlow

1. <https://git-flow.readthedocs.io/en/latest/releases.html>: `git-flow` release command documentation
2. <https://github.com/nvie/gitflow>: `gitflow` extension repository
3. <https://gist.github.com/JamesMGreene/cdd0ac49f90c987e45ac>: GitFlow branch model summary
4. <https://nvie.com/posts/a-successful-git-branching-model/>: A successful Git branching model
5. <https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow>: Atlassian GitFlow workflow guide

### GitHub Flow

1. <https://docs.github.com/en/get-started/using-github/github-flow>: GitHub Flow
2. <https://medium.com/@roalcantara/a-guide-to-improve-the-git-hub-flow-and-commits-messages-b495461e1115>: GitHub Flow and commit message guidance

### {{ cookiecutter.git_hosting_service }}

{% if cookiecutter.git_hosting_service == "Azure DevOps" -%}
1. <https://learn.microsoft.com/en-us/azure/devops/repos/>: Azure Repos documentation
2. <https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies>: Branch policies and settings
3. <https://learn.microsoft.com/en-us/azure/devops/repos/git/pull-requests>: Pull requests in Azure Repos
{% elif cookiecutter.git_hosting_service == "Bitbucket" -%}
1. <https://support.atlassian.com/bitbucket-cloud/>: Bitbucket Cloud documentation
2. <https://support.atlassian.com/bitbucket-cloud/docs/create-a-pull-request/>: Pull requests in Bitbucket Cloud
3. <https://support.atlassian.com/bitbucket-cloud/docs/use-branch-permissions/>: Branch restrictions
{% elif cookiecutter.git_hosting_service == "GitLab" -%}
1. <https://docs.gitlab.com/>: GitLab documentation
2. <https://docs.gitlab.com/user/project/merge_requests/>: Merge requests
3. <https://docs.gitlab.com/user/project/repository/branches/protected/>: Protected branches
{% else -%}
1. <https://docs.github.com/>: GitHub documentation
2. <https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file>: GitHub community health files
3. <https://docs.github.com/en/pull-requests>: GitHub pull requests
4. <https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches>: GitHub branch protection rules
{% endif %}

## Programming Languages

### Python

1. <https://docs.python.org/3/>: Python documentation
2. <https://packaging.python.org/>: Python Packaging User Guide

## Tools

### pre-commit

1. <https://github.com/ScribeMD/pre-commit-hooks/blob/main/.pre-commit-config.yaml>: pre-commit configuration example
2. <https://github.com/pre-commit/pre-commit>: pre-commit repository
3. <https://pre-commit.com>: pre-commit documentation

## Software Engineering

### Community Health

1. <https://docs.github.com/en/communities>: GitHub community documentation
2. <https://docs.github.com/en/github/building-a-strong-community>: GitHub strong community guide
3. <https://lab.github.com/githubtraining/introduction-to-github>: Introduction to GitHub training
4. <https://www.bestpractices.dev/>: OpenSSF Best Practices Badge Program
5. <https://www.contributor-covenant.org/>: Contributor Covenant

### Continuous Integration and Delivery

1. <https://docs.github.com/en/actions>: GitHub Actions documentation
2. <https://en.wikipedia.org/wiki/CI/CD>: CI/CD
3. <https://github.com/badges/shields>: Shields badge service repository
4. <https://naereen.github.io/badges>: Markdown badge examples
5. <https://shields.io/>: Shields.io
6. <https://shields.io/category/version>: Shields.io version badges

### Licensing

1. <https://choosealicense.com/>: Choose a License
2. <https://spdx.org/licenses/>: SPDX License List

### Logging

1. <https://en.wikipedia.org/wiki/ISO_8601>: ISO 8601
2. <https://www.scalyr.com/blog/log-formatting-best-practices-readable>: Log formatting best practices

### Release Notes and Changelogs

1. <https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes>: GitHub automatically generated release notes
2. <https://keepachangelog.com/>: Keep a Changelog

### Security

1. <https://docs.github.com/en/code-security/getting-started/adding-a-security-policy-to-your-repository>: GitHub security policy documentation
2. <https://scorecard.dev/>: OpenSSF Scorecard
3. <https://www.cisa.gov/resources-tools/resources/coordinated-vulnerability-disclosure-process>: Coordinated Vulnerability Disclosure

### Versioning

1. <https://semver.org/>: Semantic Versioning
