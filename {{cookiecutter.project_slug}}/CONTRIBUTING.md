# Contributing Guidelines

Version-controllable contributions toward improving [this project][README.md] (its source code,
documentation, etc.) are welcome via {{ cookiecutter.git_hosting_service }}'s
{{ cookiecutter.__change_request_name }} process. By submitting a
{{ cookiecutter.__change_request_name }}, you acknowledge and agree to licensing your contribution to
[{{ cookiecutter.owner }}][owner].

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change.

- [Ways to Contribute](#ways-to-contribute)
- [How to Contribute](#how-to-contribute)
- [{{ cookiecutter.__change_request_name | title }} Process](#{{ cookiecutter.__change_request_name.replace(' ', '-') }}-process)
- [Protected-Branch Workflow](#protected-branch-workflow)
  - [Preferred Flow](#preferred-flow)
  - [Recommended Branch Mapping](#recommended-branch-mapping)
- [Protected-Branch Workflow](#protected-branch-workflow-1)
  - [Preferred Flow](#preferred-flow-1)
- [Maintainer Runbooks](#maintainer-runbooks)
- [Code of Conduct](#code-of-conduct)
- [Local Quality Gates](#local-quality-gates)

## Ways to Contribute

Not every valuable contribution needs to be code. {{ cookiecutter.project_name }} also benefits
from codeless contributions, such as:

- Documentation corrections and clarity improvements
- Reproducible bug reports with environment details and sample inputs
- Validation of releases on supported operating systems and runtimes
- Examples, tutorials, and workflow suggestions
- Issue triage and feedback on feature proposals
- Answers to usage questions in community channels
{% if cookiecutter.sponsor_url -%}
- Sponsorship through [GitHub Sponsors] or [Buy Me a Coffee][Buy Me a Coffee]
{% endif %}

If you are looking for the lowest-friction way to help, strong documentation feedback and
reproducible bug reports are often as valuable as small code changes.

## How to Contribute

1. Open an issue to discuss substantial changes.
2. Fork the repository and create a feature branch.
3. Add or update tests and documentation when appropriate.
4. Open a {{ cookiecutter.__change_request_name }} describing your changes.

## {{ cookiecutter.__change_request_name | title }} Process

{% if cookiecutter.branch_model == "GitFlow" -%}
1. Do not commit or push directly to the protected `{{ cookiecutter.default_branch }}` or
   `{{ cookiecutter.development_branch }}` branches. Work from a topic branch and open a
   {{ cookiecutter.__change_request_name }} instead.
{% else -%}
1. Do not commit or push directly to the protected `{{ cookiecutter.default_branch }}` branch. Work
   from a topic branch and open a {{ cookiecutter.__change_request_name }} instead.
{% endif -%}
2. Update the [README] with details of changes to the action interface. This includes new inputs,
   outputs, runner environment behavior, examples, or version-support expectations.
3. For release-affecting changes (CI, release automation, usage snippets, or stable public surface
   decisions), consult [.github/MAINTAINER-RUNBOOKS.md](.github/MAINTAINER-RUNBOOKS.md).
4. For the protected-branch protection settings, required CI checks, and the exact GitHub
   configuration needed to disable direct pushes, consult
   [.github/BRANCH-PROTECTION.md](.github/BRANCH-PROTECTION.md).
5. You may merge once the protected-branch protection requirements have been satisfied. The
{% if cookiecutter.branch_model == "GitFlow" -%}
   recommended baseline is one approval for `{{ cookiecutter.development_branch }}` and two
   approvals (one approval for small teams) for `{{ cookiecutter.default_branch }}`. If you do not
   have permission to merge, request a maintainer review and handoff.
{% else -%}
   recommended baseline is one approval for `{{ cookiecutter.default_branch }}`. If you do not have
   permission to merge, request a maintainer review and handoff.
{% endif -%}
6. For release expectations and versioning rules, consult [RELEASE-POLICY.md](RELEASE-POLICY.md).
7. For the workflow split and trigger model, consult [CI-CD-WORKFLOWS.md](CI-CD-WORKFLOWS.md).

{% if cookiecutter.branch_model == "GitFlow" -%}
## Protected-Branch Workflow

{{ cookiecutter.project_name }} uses GitFlow-style branch roles with protected integration branches.

- Treat `feature/*`, `release/*`, and `hotfix/*` as working branches.
- Treat `{{ cookiecutter.development_branch }}` and `{{ cookiecutter.default_branch }}` as
  {{ cookiecutter.git_hosting_service }}-managed integration branches.
- Do not rely on `git flow feature finish` or `git flow release finish` as the authoritative way to
  update protected branches. Those commands create local merges, but protected branches and required
  checks are enforced in {{ cookiecutter.git_hosting_service }}.

### Preferred Flow

1. Create a topic branch from the correct base branch.
2. Push the topic branch.
3. Open a {{ cookiecutter.__change_request_name }} into the protected target branch. Feature
   branches should target `{{ cookiecutter.development_branch }}`; only `release/*` and `hotfix/*`
   should target `{{ cookiecutter.default_branch }}`.
4. Let `.github/workflows/pr.yml` provide the required PR checks.
5. Merge the {{ cookiecutter.__change_request_name }} in {{ cookiecutter.git_hosting_service }} after
   the branch protection requirements pass.

### Recommended Branch Mapping

- `feature/*` -> {{ cookiecutter.__change_request_name }} into `{{ cookiecutter.development_branch }}`
- `release/*` -> {{ cookiecutter.__change_request_name }} into `{{ cookiecutter.default_branch }}`
- `hotfix/*` -> {{ cookiecutter.__change_request_name }} into `{{ cookiecutter.default_branch }}`

After a release or hotfix lands on `{{ cookiecutter.default_branch }}`, sync that change back into
`{{ cookiecutter.development_branch }}` deliberately rather than assuming a local GitFlow finish
command already made both protected branches authoritative.

For small/solo maintainer teams, using {{ cookiecutter.__change_request_name }}s for both
feature and release branches is still normal once protected branches are enabled. The repository
owner can keep the review workflow while choosing lower-friction settings, such as fewer required
approvals on `{{ cookiecutter.development_branch }}`, or an admin bypass policy that is
intentionally narrow and documented.
{% else -%}
## Protected-Branch Workflow

{{ cookiecutter.project_name }} uses GitHub Flow-style topic branches with a protected
`{{ cookiecutter.default_branch }}` branch.

- Treat topic branches as working branches.
- Treat `{{ cookiecutter.default_branch }}` as the protected integration and release branch.
- Keep topic branches short-lived and reviewable.
- Do not push directly to `{{ cookiecutter.default_branch }}` except through a documented emergency
  procedure.

### Preferred Flow

1. Create a topic branch from the latest `{{ cookiecutter.default_branch }}` branch.
2. Push the topic branch.
3. Open a {{ cookiecutter.__change_request_name }} into `{{ cookiecutter.default_branch }}`.
4. Let required checks run against the proposed branch change.
5. Merge the {{ cookiecutter.__change_request_name }} in {{ cookiecutter.git_hosting_service }} after
   the branch protection requirements pass.
6. Delete the topic branch after merge when it is no longer needed.

For small/solo maintainer teams, using {{ cookiecutter.__change_request_name }}s is still useful
once protected branches are enabled. The review workflow keeps required checks and branch movement
visible even when a single maintainer owns the final merge decision.
{% endif %}

## Maintainer Runbooks

The repository keeps maintainer runbooks in
[.github/MAINTAINER-RUNBOOKS.md](.github/MAINTAINER-RUNBOOKS.md).

That file is intended for project-local operating procedures, such as:

- Feature branch integration under protected branches
- Release and hotfix branch finishing
- Syncing `main` back into `develop`
- Tagging and tag-triggered CD behavior

It lives under `.github/` because it is repository operations guidance rather than user-facing
action documentation.

Private operator procedures, credentials, incident-response steps, and recovery playbooks should
live outside the repository.

## Code of Conduct

All contributors are expected to read and follow [CODE_OF_CONDUCT.md].

## Local Quality Gates

python-project-lifecycle maintains one supported contributor local quality workflow. Contributors
should use:

```bash
pre-commit run
```

For local Git hooks, python-project-lifecycle uses a staged workflow:

```bash
pre-commit install --install-hooks
```

- `pre-commit` runs the fast hygiene and auto-fix hooks before a commit is created.
- `commit-msg` validates the commit message format.

[Buy Me a Coffee]: https://buymeacoffee.com/djrlj694
[CODE_OF_CONDUCT.md]: CODE_OF_CONDUCT.md
[GitHub Sponsors]: https://github.com/sponsors/Dagitali
[owner]: https://dagitali.com
[README.md]: README.md
[SemVer]: http://semver.org
