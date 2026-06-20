# Branch Protection

- [Purpose](#purpose)
- [Shared Protection Baseline](#shared-protection-baseline)
- [Default Branch](#default-branch)
{% if cookiecutter.branch_model == "GitFlow" -%}
- [Development Branch](#development-branch)
{% endif -%}
- [Maintenance Notes](#maintenance-notes)

## Purpose

Branch protections enforce review and validation before protected integration branches move.

## Shared Protection Baseline

Apply this baseline to protected branches:

- Require a {{ cookiecutter.__change_request_name }} before merging
- Dismiss stale approvals when new commits are pushed
- Require conversation resolution before merging
- Require status checks to pass before merging
- Block force pushes
- Block branch deletion
- Keep bypass actors empty unless there is a documented operational need

## Default Branch

Target branch: `{{ cookiecutter.default_branch }}`

Recommended additions:

- Require at least one approval
- Require code owner review when sensitive paths exist
- Require release-oriented checks for release and hotfix work

{% if cookiecutter.branch_model == "GitFlow" -%}
## Development Branch

Target branch: `{{ cookiecutter.development_branch }}`

Recommended additions:

- Require at least one approval
- Require the normal {{ cookiecutter.__change_request_name }} validation workflow
- Reserve direct pushes for documented emergency procedures only

{% endif -%}
## Maintenance Notes

Update this file whenever workflow names, required checks, branch names, or review policy changes.
