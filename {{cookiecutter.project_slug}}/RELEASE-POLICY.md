# Release Policy And Versioning

- [Scope](#scope)
- [Supported Release Line](#supported-release-line)
- [Versioning Model](#versioning-model)
- [Patch Releases](#patch-releases)
- [Minor Releases](#minor-releases)
- [Major Releases](#major-releases)
- [Deprecation Policy](#deprecation-policy)
- [Release Artifacts](#release-artifacts)
- [Release Notes](#release-notes)

## Scope

This document describes the public release policy for {{ cookiecutter.project_name }}, including
versioning expectations, release channels, deprecation posture, and release-note handling.

## Supported Release Line

{{ cookiecutter.project_name }} treats the latest stable release line as the supported public line
unless project documentation states otherwise.

The supported surface is documented user-facing behavior. Historical files, placeholder paths, and
undocumented implementation details are not stable contracts unless promoted in public docs.

## Versioning Model

{{ cookiecutter.project_name }} follows semantic-versioning-style expectations for public releases:

- `MAJOR` releases are for intentionally breaking public changes
- `MINOR` releases add backward-compatible public capability
- `PATCH` releases are for backward-compatible fixes and release-hygiene corrections

Version tags should use the format `v*.*.*`.

## Patch Releases

Patch releases are appropriate for:

- Bug fixes that preserve the documented public contract
- CI/CD or release-automation fixes that do not change the supported interface
- Documentation corrections that align public docs with actual stable behavior
- Compatibility fixes that preserve supported usage

## Minor Releases

Minor releases are appropriate for:

- New documented capabilities
- Additional supported platforms or runtimes
- Additive configuration options that remain backward compatible

## Major Releases

Major releases are appropriate when {{ cookiecutter.project_name }} intentionally breaks the
documented public contract. Major releases should include migration guidance.

## Deprecation Policy

When practical, deprecated public capabilities should remain available through at least one stable
minor release before removal. Immediate removal should be reserved for exceptional cases such as
security, legal, or clearly broken accidental surfaces.

## Release Artifacts

Public releases should produce:

- A Git tag for the released version
- A release announcement or release notes
- The tagged source used by downstream consumers

## Release Notes

Release notes should summarize:

- User-visible features or fixes
- Deprecations
- Breaking changes
- Notable compatibility or workflow changes
