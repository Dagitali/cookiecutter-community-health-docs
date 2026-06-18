# cookiecutter-community-health-docs

A Cookiecutter template for generating project-tailored community health documents.

## Generated files

The template generates:

- `README.md`
- `LICENSE`
- `CODE_OF_CONDUCT.md`
- `CONTRIBUTING.md`
- `SECURITY.md`
- `SUPPORT.md`

GitHub-specific templates are optionally generated:

- `.github/ISSUE_TEMPLATE/bug_report.md`
- `.github/ISSUE_TEMPLATE/feature_request.md`
- `.github/PULL_REQUEST_TEMPLATE.md`

## Inputs

- `git_hosting_service`: `GitHub`, `GitLab`, `Bitbucket`, or `Azure DevOps`
- `include_issue_templates`: defaults to `yes` for GitHub, otherwise `no`
- `include_pull_request_template`: defaults to `yes` for GitHub, otherwise `no`

When a non-GitHub hosting service is selected, GitHub-specific templates are not generated.
