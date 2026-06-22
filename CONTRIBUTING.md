# Contributing Guidelines

Version-controllable contributions toward improving [this project][README.md] (its source code,
documentation, etc.) are welcome via GItHub's pull request process. By submitting a pull request,
you acknowledge and agree to licensing your contribution to [Dagitali LLC][owner].

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change.

- [Ways to Contribute](#ways-to-contribute)
- [How to Contribute](#how-to-contribute)
- [Pull Request Process](#pull-request-process)
- [Protected-Branch Workflow](#protected-branch-workflow)
  - [Preferred Flow](#preferred-flow)
  - [Recommended Branch Mapping](#recommended-branch-mapping)
- [Protected-Branch Workflow](#protected-branch-workflow-1)
  - [Preferred Flow](#preferred-flow-1)
- [Maintainer Runbooks](#maintainer-runbooks)
- [Code of Conduct](#code-of-conduct)
- [Local Quality Gates](#local-quality-gates)

## Ways to Contribute

Not every valuable contribution needs to be code. cookiecutter-repo-governance also benefits from
codeless contributions, such as:

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
4. Open a pull request describing your changes.

## Pull Request Process

{% if cookiecutter.branch_model == "GitFlow" -%}
1. Do not commit or push directly to the protected `main` or
   `develop` branches. Work from a topic branch and open a
   pull request instead.
{% else -%}
1. Do not commit or push directly to the protected `main` branch. Work
   from a topic branch and open a pull request instead.
{% endif -%}
2. Update the [README] when user-facing behavior, support expectations, repository workflows, or
   examples change.
{% if cookiecutter.git_service == "GitHub" and cookiecutter.include_maintainer_runbooks == "yes" -%}
3. For release-affecting changes (CI, release automation, usage snippets, or stable public surface
   decisions), consult [.github/MAINTAINER-RUNBOOKS.md](.github/MAINTAINER-RUNBOOKS.md).
{% else -%}
3. Document release-affecting changes, CI changes, usage snippets, and stable public-surface
   decisions in the appropriate project-maintainer notes.
{% endif -%}
{% if cookiecutter.git_service == "GitHub" and cookiecutter.include_branch_protection_docs == "yes" -%}
4. For the protected-branch protection settings, required CI checks, and the exact GitHub
   configuration needed to disable direct pushes, consult
   [.github/BRANCH-PROTECTION.md](.github/BRANCH-PROTECTION.md).
{% else -%}
4. Keep protected-branch settings and required checks aligned with the repository's documented
   contribution and review process.
{% endif -%}
5. You may merge once the protected-branch protection requirements have been satisfied. The
{% if cookiecutter.branch_model == "GitFlow" -%}
   recommended baseline is one approval for `develop` and two
   approvals (one approval for small teams) for `main`. If you do not
   have permission to merge, request a maintainer review and handoff.
{% else -%}
   recommended baseline is one approval for `main`. If you do not have
   permission to merge, request a maintainer review and handoff.
{% endif -%}
{% if cookiecutter.include_release_docs == "yes" -%}
6. For release expectations and versioning rules, consult [RELEASE-POLICY.md](RELEASE-POLICY.md).
{% else -%}
6. Follow the repository's documented release expectations and versioning rules.
{% endif %}

{% if cookiecutter.branch_model == "GitFlow" -%}
## Protected-Branch Workflow

cookiecutter-repo-governance uses GitFlow-style branch roles with protected integration branches.

- Treat `feature/*`, `release/*`, and `hotfix/*` as working branches.
- Treat `develop` and `main` as
  GItHub-managed integration branches.
- Do not rely on `git flow feature finish` or `git flow release finish` as the authoritative way to
  update protected branches. Those commands create local merges, but protected branches and required
  checks are enforced in GItHub.

### Preferred Flow

1. Create a topic branch from the correct base branch.
2. Push the topic branch.
3. Open a pull request into the protected target branch. Feature branches should target `develop`;
   only `release/*` and `hotfix/*` should target `main`.
4. Let the required checks run against the proposed branch change.
5. Merge the pull request in GItHub after the branch protection requirements pass.

### Recommended Branch Mapping

- `feature/*` -> pull request into `develop`
- `release/*` -> pull request into `main`
- `hotfix/*` -> pull request into `main`

After a release or hotfix lands on `main`, sync that change back into `develop` deliberately rather
than assuming a local GitFlow finish command already made both protected branches authoritative.

For small/solo maintainer teams, using pull requests for both feature and release branches is still
normal once protected branches are enabled. The repository owner can keep the review workflow while
choosing lower-friction settings, such as fewer required approvals on `develop`, or an admin bypass
policy that is intentionally narrow and documented.
{% else -%}
## Protected-Branch Workflow

cookiecutter-repo-governance uses GitHub Flow-style topic branches with a protected `main` branch.

- Treat topic branches as working branches.
- Treat `main` as the protected integration and release branch.
- Keep topic branches short-lived and reviewable.
- Do not push directly to `main` except through a documented emergency
  procedure.

### Preferred Flow

1. Create a topic branch from the latest `main` branch.
2. Push the topic branch.
3. Open a pull request into `main`.
4. Let required checks run against the proposed branch change.
5. Merge the pull request in GItHub after
   the branch protection requirements pass.
6. Delete the topic branch after merge when it is no longer needed.

For small/solo maintainer teams, using pull requests is still useful
once protected branches are enabled. The review workflow keeps required checks and branch movement
visible even when a single maintainer owns the final merge decision.
{% endif %}

{% if cookiecutter.git_service == "GitHub" and cookiecutter.include_maintainer_runbooks == "yes" -%}
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

{% endif -%}
## Code of Conduct

All contributors are expected to read and follow [CODE_OF_CONDUCT.md].

## Local Quality Gates

Run the repository's documented local checks before opening a pull request.
If the project uses `pre-commit`, install and run the hooks with:

```bash
pre-commit install --install-hooks
pre-commit run
```

If the project uses another task runner, use its documented check command instead.

[Buy Me a Coffee]: https://buymeacoffee.com/djrlj694
[CODE_OF_CONDUCT.md]: CODE_OF_CONDUCT.md
[GitHub Sponsors]: https://github.com/sponsors/Dagitali
[owner]: https://dagitali.com
[README.md]: README.md
[SemVer]: http://semver.org
