# Release Checklist And Stable-Line Maintenance

Use this checklist for releases of {{cookiecutter.project_slug}}.

- [Pre-Release](#pre-release)
- [Release](#release)
- [Post-Release](#post-release)
- [Stable-Line Maintenance](#stable-line-maintenance)

## Pre-Release

- [ ] Confirm the release scope and version number.
- [ ] Verify that user-facing documentation matches supported behavior.
- [ ] Confirm tests and required checks pass on the release branch.
- [ ] Review [SECURITY.md](SECURITY.md) for unresolved release-blocking reports.
{% if cookiecutter.git_service == 'GitHub' -%}
- [ ] Draft release notes using `.github/RELEASE-NOTES-TEMPLATE.md`.
{% else -%}
- [ ] Draft release notes for the selected release channel.
{% endif %}

## Release

- [ ] Merge the release branch through the protected review process.
- [ ] Create an annotated `v*.*.*` tag on the released commit.
- [ ] Publish release notes.
- [ ] Verify generated artifacts or package outputs when the project ships them.

## Post-Release

{% if cookiecutter.branch_model == 'GitFlow' -%}
- [ ] Sync `{{ cookiecutter.default_branch }}` back into `{{ cookiecutter.development_branch }}` when
      using a GitFlow branch model.
{% else -%}
- [ ] Confirm release follow-up work is tracked through short-lived branches targeting
      `{{ cookiecutter.default_branch }}`.
{% endif %}
- [ ] Close or update release-tracking issues.
- [ ] Update follow-up maintenance items.

## Stable-Line Maintenance

- [ ] Keep public docs aligned with the supported surface.
- [ ] Review deprecated capabilities before each minor release.
- [ ] Keep branch protection and required checks current.
- [ ] Keep maintainer runbooks free of private credentials or sensitive operator details.
