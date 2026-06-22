# Support

Thank you for using cookiecutter-repo-governance.

- [Support Policy](#support-policy)
- [Supported Versions](#supported-versions)
- [Maintenance Expectations](#maintenance-expectations)
- [Where to Get Help](#where-to-get-help)
- [Response Targets](#response-targets)
- [Deprecation Policy](#deprecation-policy)
- [Support the Project](#support-the-project)

## Support Policy

cookiecutter-repo-governance is maintained as an open source Cookiecutter template with best-effort
community support.

The support baseline for the current stable line is:

- Supported Python versions: 3.13 and 3.14.
- Supported install surfaces: the repository template, Cookiecutter rendering workflow, generated
  governance documents, and documented local development commands.
- Supported collaboration channels: GitHub Discussions for usage and docs questions, GitHub Issues
  for confirmed bugs and concrete feature requests, and the security reporting path for private
  vulnerabilities.

Anything marked as placeholder, stubbed, defunct, or experimental in the repository docs should be
treated as out of the stable support promise until explicitly promoted.

## Supported Versions

The maintenance target is:

- The latest released minor line.
- The immediately previous minor line for critical regressions and security fixes, when practical.

Older versions may still work, but they should not be assumed to receive routine fixes.

## Maintenance Expectations

For the stable line, cookiecutter-repo-governance uses minor releases as the normal delivery vehicle
for new template options, generated-document changes, broader dependency updates, and deprecations.

Patch releases are intended for targeted, low-risk maintenance such as:

- Confirmed regressions in documented template behavior
- Security fixes
- Rendering, test, or local tooling breakages
- Docs or metadata corrections that are needed to keep the template usable

Backports are not guaranteed for every fix. When practical, critical regressions and security fixes
may be applied to the latest released minor line and the immediately previous minor line. Routine
feature work, behavior changes, and larger internal refactors are expected to land only on the
latest active minor line.

## Where to Get Help

- **Questions & Usage**: Please use [GitHub Discussions][discussions] for general questions, usage
  help, and best practices.
- **Docs Feedback & Examples**: Please use [GitHub Discussions][discussions] for documentation
  gaps, unclear sections, and example-sharing.
- **Bugs & Feature Requests**: Open an issue in the [GitHub Issues][issues] tracker using the
  repository issue forms.
- **Security Issues**: See [SECURITY.md] for responsible disclosure.
- **Documentation**: See [README.md], generated template files, and [REFERENCES.md] for guides and
  references.

In general:

- Use Discussions for questions, docs feedback, examples, and support conversations.
- Use Issues for confirmed bugs and concrete feature requests.
- Use rendered example output from the template when reporting generated-document issues.

## Response Targets

These are response targets, not guaranteed service-level agreements.

- Security reports: initial acknowledgement within 3 business days when received through the
  documented security channel.
- Confirmed bug reports and feature requests: initial triage target within 10 business days.
- Usage questions and docs discussions: response target within 10 business days when maintainer time
  allows.

Community contributions and peer support remain welcome even when maintainer response is delayed.

## Deprecation Policy

For the stable line, cookiecutter-repo-governance aims to avoid abrupt breaking changes to
documented public template surfaces.

- A deprecated Cookiecutter setting, generated file path, or documented local command should
  normally remain available for at least one minor release after deprecation notice.
- Deprecations should be called out in the changelog and nearby user-facing docs.
- Patch releases should not normally remove or materially redefine documented public behavior.
- Removal may happen sooner only for security, correctness, or ecosystem-compatibility reasons.

Internal, defunct, placeholder, or undocumented template paths are excluded from this deprecation
policy.

## Support the Project

If cookiecutter-repo-governance is useful in your work, you can support its ongoing maintenance
through the repository sponsor button.

- GitHub Sponsors: https://github.com/sponsors/Dagitali
- Buy Me a Coffee: https://buymeacoffee.com/djrlj694

Financial support helps fund maintenance, documentation, template examples, compatibility work, and
future governance-document improvements.

[discussions]: https://github.com/Dagitali/cookiecutter-repo-governance/discussions
[issues]: https://github.com/Dagitali/cookiecutter-repo-governance/issues
[README.md]: README.md
[REFERENCES.md]: REFERENCES.md
[SECURITY.md]: SECURITY.md
