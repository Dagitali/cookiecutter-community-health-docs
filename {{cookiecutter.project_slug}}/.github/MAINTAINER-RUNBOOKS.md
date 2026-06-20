# Maintainer Runbooks

- [Operating Model](#operating-model)
- [Feature Work](#feature-work)
- [Release Work](#release-work)
- [Hotfix Work](#hotfix-work)
- [Sync Default Branch Back To Development](#sync-default-branch-back-to-development)
- [Keep Private Elsewhere](#keep-private-elsewhere)

## Operating Model

{{ cookiecutter.project_name }} uses {{ cookiecutter.branch_model }} with protected integration
branches.

{% if cookiecutter.branch_model == "GitFlow" -%}
- Working branches: `feature/*`, `release/*`, and `hotfix/*`
- Development integration branch: `{{ cookiecutter.development_branch }}`
- Release integration branch: `{{ cookiecutter.default_branch }}`
{% else -%}
- Working branches: topic branches
- Integration branch: `{{ cookiecutter.default_branch }}`
{% endif %}

## Feature Work

1. Create a topic branch from the appropriate integration branch.
2. Commit focused changes locally.
3. Push the branch and open a {{ cookiecutter.__change_request_name }}.
4. Merge only after required checks and review requirements pass.

## Release Work

1. Confirm the release scope and version.
2. Update release-facing docs.
3. Open the release {{ cookiecutter.__change_request_name }} against `{{ cookiecutter.default_branch }}`.
4. Tag the merged release commit with an annotated `v*.*.*` tag.
5. Publish release notes.

## Hotfix Work

1. Branch from the released `{{ cookiecutter.default_branch }}` state.
2. Apply the narrow fix and validation.
3. Open a {{ cookiecutter.__change_request_name }} against `{{ cookiecutter.default_branch }}`.
4. Tag and publish the hotfix release when needed.

## Sync Default Branch Back To Development

When using a development branch, sync `{{ cookiecutter.default_branch }}` back into
`{{ cookiecutter.development_branch }}` after release or hotfix work lands.

## Keep Private Elsewhere

Do not store secrets, credential rotation steps, account recovery procedures, or sensitive incident
response details in this public file.
