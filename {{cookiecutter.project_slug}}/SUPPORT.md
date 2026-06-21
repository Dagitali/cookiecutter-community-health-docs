# Support

- [Support Policy](#support-policy)
- [Supported Versions](#supported-versions)
- [Maintenance Expectations](#maintenance-expectations)
- [Where to Get Help](#where-to-get-help)
- [Response Targets](#response-targets)
- [Support the Project](#support-the-project)

## Support Policy

{{ cookiecutter.project_name }} is maintained as an open source project by {{ cookiecutter.owner }}.
Support is best-effort unless a separate written agreement says otherwise.

## Supported Versions

The current supported line is the latest released stable version. Unreleased development branches
may change without advance notice.

## Maintenance Expectations

Maintainers prioritize:

- Security reports
- Reproducible defects in supported releases
- Documentation fixes that reduce support load
- Compatibility issues on documented supported platforms

Feature requests and broad design discussions are welcome, but they may not receive the same
response priority as security or correctness issues.

## Where to Get Help

- Public support: {{ cookiecutter.support_email }}
- Repository: {{ cookiecutter.repo_url }}
- Security reports: {{ cookiecutter.security_email }}

## Response Targets

Response times are not guaranteed. Maintainers try to acknowledge security reports and reproducible
defects before general questions.

## Support the Project

{% if cookiecutter.sponsor_url -%}
Sponsorship is available at {{ cookiecutter.sponsor_url }}.
{% else -%}
No sponsorship channel is currently configured.
{% endif %}
