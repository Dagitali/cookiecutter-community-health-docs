# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

- [Community Health](#community-health)
- [Repository](#repository)
- [Contributing](#contributing)
- [Support](#support)
- [Security](#security)
- [License](#license)

## Community Health

This repository includes community health documents that describe contribution, security reporting,
support channels, release expectations, and expected behavior.

## Repository

- Owner: {{ cookiecutter.owner }}
- Hosting service: {{ cookiecutter.git_service }}
- Repository: {{ cookiecutter.repo_url }}
- Default branch: `{{ cookiecutter.default_branch }}`
{% if cookiecutter.branch_model == "GitFlow" -%}
- Development branch: `{{ cookiecutter.development_branch }}`
- Branch model: protected-branch GitFlow
{% else -%}
- Branch model: GitHub Flow
{% endif %}

## Contributing

See [CONTRIBUTING.md] before opening substantial issues or {{ cookiecutter.__change_request_name }}s.

## Support

For usage questions and support expectations, see [SUPPORT.md].

## Security

Do not open public issues for vulnerability reports. See [SECURITY.md].

## License

{{ cookiecutter.project_name }} is distributed under the {{ cookiecutter.license_name }} license.

[CONTRIBUTING.md]: CONTRIBUTING.md
[SECURITY.md]: SECURITY.md]
[SUPPORT.md] SUPPORT.md
