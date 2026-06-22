# cookiecutter-repo-governance

A Cookiecutter template for rendering project-tailored software repository governance files.

- [Generated files](#generated-files)
- [Inputs](#inputs)
- [Usage](#usage)
- [Development](#development)
- [Documentation](#documentation)
  - [Community Health](#community-health)
  - [Maintainer Docs](#maintainer-docs)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Generated files

The template generates:

- `AGENTS.md`
- `CODE_OF_CONDUCT.md`
- `CONTRIBUTING.md`
- `LICENSE`
- `README.md`
- `REFERENCES.md`
- `RELEASE-CHECKLIST.md`
- `RELEASE-POLICY.md`
- `SECURITY.md`
- `SUPPORT.md`

Host-specific templates are optionally generated:

- Azure DevOps
  - `.azuredevops/pull_request_template.md`
- Bitbucket
  - `.bitbucket/PULL_REQUEST_TEMPLATE.md`
- GitHub
  - `.github/ISSUE_TEMPLATE/bug_report.yml`
  - `.github/ISSUE_TEMPLATE/config.yml`
  - `.github/ISSUE_TEMPLATE/feature_request.yml`
  - `.github/pull_request_template.md`
  - `.github/RELEASE-NOTES-TEMPLATE.md`
  - `.github/MAINTAINER-RUNBOOKS.md`
  - `.github/BRANCH-PROTECTION.md`
  - `.github/FUNDING.yml`
- GitLab
  - `.gitlab/issue_templates/Bug.md`
  - `.gitlab/merge_request_templates/Default.md`

## Inputs

- `project_name`: human-readable project name
- `project_slug`: generated output directory
- `project_description`: short project summary
- `owner`: organization or maintainer name
- `repo_namespace`: URL-safe repository owner, group, workspace, or organization namespace
- `repo_url`: canonical repository URL, derived from `git_service`,
  `repo_namespace`, and `project_slug` by default
- `default_branch`: default integration branch
- `development_branch`: development integration branch
- `branch_model`: `GitFlow` or `GitHub Flow`
- `support_email`: public support contact
- `security_email`: private vulnerability-reporting contact
- `conduct_email`: code-of-conduct contact
- `sponsor_url`: optional sponsor URL
- `license_name`: license family used by generated docs
- `git_service`: `GitHub`, `GitLab`, `Bitbucket`, or `Azure DevOps`
- `include_issue_templates`: defaults to `yes` for GitHub, otherwise `no`
- `include_pull_request_template`: defaults to `yes` for GitHub, otherwise `no`
- `include_release_docs`: defaults to `yes`
- `include_branch_protection_docs`: defaults to `yes`
- `include_maintainer_runbooks`: defaults to `yes`
- `include_references`: defaults to `yes`
- `include_agents_md`: defaults to `yes`
- `include_discussions_link`: defaults to `yes` for GitHub, otherwise `no`
- `include_funding`: defaults to `yes` when GitHub and `sponsor_url` are set

When a non-GitHub hosting service is selected, GitHub-specific templates are removed and the
matching host-specific templates are retained.

The generated docs derive the host-specific change-review term from `git_service`: GitLab
renders `merge request`; GitHub, Bitbucket, and Azure DevOps render `pull request`.

## Usage

```bash
pip install cookiecutter
cookiecutter gh:Dagitali/cookiecutter-repo-governance
```

For local development:

```bash
cookiecutter .
```

## Development

```bash
python -m pip install -e ".[dev]"
pytest
```

## Documentation

### Community Health

- [Code of Conduct](CODE_OF_CONDUCT.md): Community standards and expectations
- [Contributing Guidelines](CONTRIBUTING.md): How to contribute, report issues, and submit PRs
- [Security Policy](SECURITY.md): Responsible disclosure and vulnerability reporting
- [Support](SUPPORT.md): Where to get help

### Maintainer Docs

- [Release Policy And Versioning](RELEASE-POLICY.md): Release expectations, semantic-version-style
  rules, and deprecation posture
- [CI/CD Workflow Map](CI-CD-WORKFLOWS.md): Explanation of `pr.yml`, `ci.yml`, and `cd.yml`
- [Release Checklist And Stable-Line Maintenance](RELEASE-CHECKLIST.md): Release-readiness execution guidance and stable-line follow-up tracking
- [Maintainer Runbooks](.github/MAINTAINER-RUNBOOKS.md): Maintainer workflow guidance for protected
  branches and tag-driven releases

## License

cookiecutter-repo-governance is distributed under the MIT license.

## Acknowledgments

cookiecutter-repo-governance is inspired by common design and work patterns in open source projects,
aiming to increase productivity and reduce boilerplate code. Feedback and contributions are always
appreciated!
