# Branch Protection

This document defines the recommended GitHub branch protection configuration for protected
integration branches when {{ cookiecutter.project_name }} is operated with {{ cookiecutter.branch_model }}.

- [Purpose](#purpose)
- [Recommended Required Checks](#recommended-required-checks)
  - [Pull Request Baseline](#pull-request-baseline)
  - [Advisory Categories](#advisory-categories)
- [Shared Protection Baseline](#shared-protection-baseline)
  - [Branch Protections](#branch-protections)
- [Default Branch](#default-branch)
{% if cookiecutter.branch_model == "GitFlow" -%}
- [Development Branch](#development-branch)
{% endif -%}
- [How To Disallow Direct Pushes](#how-to-disallow-direct-pushes)
- [How To Update Required Checks](#how-to-update-required-checks)
- [Maintenance Notes](#maintenance-notes)

## Purpose

Branch protections exist to enforce three repository policies:

- No direct pushes to protected integration branches
- No merge into protected branches without review
- No merge into protected branches unless required validation checks pass

Local hooks can complement this policy, but GitHub branch protection is the authoritative enforcement
layer when this repository is hosted on GitHub.

## Recommended Required Checks

Choose the required-check baseline that matches how the repository accepts {{ cookiecutter.__change_request_name }}s.

If workflow jobs use a matrix, GitHub exposes expanded matrix job names in branch protection
settings rather than the template names shown in workflow YAML. Select those expanded names when
configuring required checks.

### Pull Request Baseline

Use this baseline for protected-branch merge gates. It covers the checks that should always run for
{{ cookiecutter.__change_request_name }} validation.

Recommended categories:

- Target-branch policy checks
- Repository hygiene checks
- Linting or formatting checks
- Tests for changed behavior
- Documentation checks when documentation is part of the supported surface

### Advisory Categories

Additional checks are still useful, and they can be made required when their signal is strong enough
to block protected-branch updates.

Common advisory categories include:

- Additional runtime or platform test jobs
- Expanded documentation validation
- Release or packaging validation
- Security scanning

## Shared Protection Baseline

Apply this baseline to protected branches:

- Require a {{ cookiecutter.__change_request_name }} before merging
- Dismiss stale approvals when new commits are pushed
- Require conversation resolution before merging
- Require status checks to pass before merging
- Require branches to be up to date before merging
- Block force pushes
- Block branch deletion
- Keep bypass actors empty if possible

In GitHub, these controls are typically split across {{ cookiecutter.__change_request_name }} rules,
status check rules, and branch protections.

### Branch Protections

- Block force pushes
- Block branch deletion
- If bypass cannot be empty, restrict it to a very small maintainer/admin set

## Default Branch

Target branch: `{{ cookiecutter.default_branch }}`

Recommended additions:

- Require at least one approval
- Require Code Owners review when sensitive paths exist
- Consider requiring signed commits
- Require release-oriented checks for release and hotfix work

{% if cookiecutter.branch_model == "GitFlow" -%}
## Development Branch

Target branch: `{{ cookiecutter.development_branch }}`

Recommended additions:

- Require at least one approval
- Require the normal {{ cookiecutter.__change_request_name }} validation workflow
- Require Code Owners review for sensitive paths when practical
- Reserve direct pushes for documented emergency procedures only

{% endif -%}
## How To Disallow Direct Pushes

The reliable way to disallow direct pushes is to protect the branch and require
{{ cookiecutter.__change_request_name }}s. CI alone cannot block a normal direct push after the fact,
because GitHub Actions runs only after the push exists.

In GitHub:

1. Open repository `Settings`.
2. Open `Branches`.
3. Open the branch protection rule for the protected branch.
4. Enable `Require a pull request before merging`.
5. Enable `Require status checks to pass before merging`.
6. Enable `Require branches to be up to date before merging`.
7. Enable `Block force pushes`.
8. Enable `Block deletions`.
9. Remove bypass actors unless there is a strict operational need.

## How To Update Required Checks

After workflow job names change, update protected-branch rules so required checks match the current
workflow job names.

In GitHub:

1. Open repository `Settings`.
2. Open `Branches`.
3. Open the branch protection rule for the protected branch.
4. Under `Require status checks to pass`, remove stale check names.
5. Add the current required checks.
6. Save the branch protection rule.
7. Repeat the same status-check set for other protected branches unless they intentionally use a
   different policy.

## Maintenance Notes

- Keep this file aligned with the repository workflow files.
- Keep branch-target guidance aligned with `CONTRIBUTING.md`.
- Update required check names whenever workflow job names change.
- Treat version-specific and platform-specific check names as current examples, not permanent
  policy.
