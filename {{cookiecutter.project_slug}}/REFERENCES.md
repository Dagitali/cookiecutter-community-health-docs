# References

- [Markup Languages](#markup-languages)
  - [Markdown](#markdown)
  - [YAML](#yaml)
- [Platforms](#platforms)
  - [EditorConfig](#editorconfig)
  - [`git`](#git)
  - [GitFlow](#gitflow)
  - [GitHub Flow](#github-flow)
  - [{{ cookiecutter.git\_hosting\_service }}](#-cookiecuttergit_hosting_service-)
- [Programming Languages](#programming-languages)
  - [Python](#python)
- [Tools](#tools)
  - [pre-commit](#pre-commit)
- [Software Engineering](#software-engineering)
  - [Community Health](#community-health)
  - [Continuous Integration and Delivery](#continuous-integration-and-delivery)
  - [Licensing](#licensing)
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

1. <https://git-scm.com/book>: Pro Git book
2. <https://git-scm.com/docs>: `git` documentation
3. <https://git-scm.com/docs/gitattributes>: `gitattributes` documentation
4. <https://git-scm.com/docs/gitignore>: `gitignore` documentation
5. <https://www.atlassian.com/git/tutorials/setting-up-a-repository/git-config>
6. <https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup>
7. <https://www.atlassian.com/git/tutorials/inspecting-a-repository/git-tag>
8. <https://stackoverflow.com/questions/63241071/automate-git-merge-commit-message>
9. <https://fileinfo.com/extension/gitattributes>

### GitFlow

1. <https://nvie.com/posts/a-successful-git-branching-model/>: A successful Git branching model
2. <https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow>: Atlassian GitFlow workflow guide
3. <https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow>
2. <https://github.com/nvie/gitflow>
3. <https://gist.github.com/JamesMGreene/cdd0ac49f90c987e45ac>
4. <https://medium.com/@roalcantara/a-guide-to-improve-the-git-hub-flow-and-commits-messages-b495461e1115>
5. <https://nvie.com/posts/a-successful-git-branching-model>
6. <https://git-flow.readthedocs.io/en/latest/releases.html>

### GitHub Flow

1. <https://docs.github.com/en/get-started/using-github/github-flow>: GitHub Flow

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

1. <https://github.com/pre-commit/pre-commit>: pre-commit GitHub repository
2. <https://pre-commit.com>: pre-commit documentation

## Software Engineering

### Community Health

1. <https://docs.github.com/en/communities>: GitHub: Building a strong community
2. <https://www.bestpractices.dev/>: OpenSSF Best Practices Badge Program
3. <https://www.contributor-covenant.org/>: Contributor Covenant

### Continuous Integration and Delivery

1. <https://docs.github.com/en/actions>: GitHub Actions documentation
2. <https://shields.io/>: Shields.io

### Licensing

1. <https://choosealicense.com/>: Choose a License
2. <https://spdx.org/licenses/>: SPDX License List

### Release Notes and Changelogs

1. <https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes>: GitHub automatically generated release notes
2. <https://keepachangelog.com/>: Keep a Changelog

### Security

1. <https://docs.github.com/en/code-security/getting-started/adding-a-security-policy-to-your-repository>: GitHub security policy documentation
2. <https://scorecard.dev/>: OpenSSF Scorecard
3. <https://www.cisa.gov/resources-tools/resources/coordinated-vulnerability-disclosure-process>: Coordinated Vulnerability Disclosure

### Versioning

1. <https://semver.org/>: Semantic Versioning
