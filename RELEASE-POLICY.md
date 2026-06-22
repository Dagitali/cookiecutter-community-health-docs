# Release Policy And Versioning

This document describes the public release policy for cookiecutter-repo-governance, including
versioning expectations, release artifacts, deprecation posture, and release-note handling.

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

This file is a public policy document. It explains what maintainers and contributors should expect
from cookiecutter-repo-governance releases, but it does not contain private operator steps,
credentials, or incident-response procedures.

## Supported Release Line

cookiecutter-repo-governance currently treats the latest released minor line as the supported public
line.

The supported surface is the documented Cookiecutter settings, generated file layout,
post-generation hook behavior, local maintenance commands, and repository governance files described
in the public documentation. Historical files, placeholder paths, and undocumented behavior are not
part of the stable contract unless they are promoted in the public docs.

## Versioning Model

cookiecutter-repo-governance follows semantic-versioning-style expectations for public releases:

- `MAJOR` releases are for intentionally breaking public template changes
- `MINOR` releases add backward-compatible template capabilities or generated files
- `PATCH` releases are for backward-compatible fixes, documentation corrections, and release-hygiene
  updates

Version tags use the format `v*.*.*` and are expected to be annotated tags.

While the project remains below `v1.0.0`, maintainers may still use minor releases for larger
template changes. Breaking or migration-relevant changes should be called out explicitly in release
notes regardless of the version number.

## Patch Releases

Patch releases are appropriate for changes such as:

- Bug fixes that preserve the documented template contract
- Rendering or post-generation hook fixes that do not change documented inputs incompatibly
- Documentation corrections that align public docs with actual behavior
- CI, test, or local-tooling fixes that preserve supported usage

Patch releases should avoid widening or narrowing the documented template surface unless the change
is purely a documentation correction for behavior that was already intentionally supported.

## Minor Releases

Minor releases are appropriate for changes such as:

- New Cookiecutter settings
- New generated governance documents
- New supported Git hosting service behavior
- Additive changes to generated issue, pull request, support, security, or release docs
- New repository-maintenance checks or workflows that remain backward compatible

Minor releases may expand the public surface, but they should not silently break existing documented
workflows.

## Major Releases

Major releases are appropriate when cookiecutter-repo-governance intentionally breaks the documented
public template contract.

Examples include:

- Removing a previously documented Cookiecutter setting
- Renaming generated files or directories incompatibly
- Removing support for a previously supported Git hosting service
- Changing default rendered behavior in a way that requires generated repositories to migrate

Major releases should be accompanied by explicit migration guidance.

## Deprecation Policy

cookiecutter-repo-governance prefers a documented deprecation period before removing a stable public
template capability.

When practical:

- Mark the capability as deprecated in user-facing docs
- Provide a replacement path when one exists
- Preserve the deprecated behavior through at least one minor release before removal

Immediate removal without a deprecation window should be reserved for exceptional cases such as
security, legal, or clearly broken accidental surfaces that were never intended to be stable.

## Release Artifacts

Public releases are expected to produce:

- An annotated Git tag for the released version
- A GitHub Release for announcement and release-note publication
- The tagged repository source used by Cookiecutter consumers

This repository is not currently released as a PyPI package.

## Release Notes

GitHub Releases are the canonical public release-history surface for cookiecutter-repo-governance.

Release notes should summarize:

- User-visible template features or fixes
- Cookiecutter input changes
- Generated file additions, removals, or behavior changes
- Deprecations
- Breaking changes
- Notable CI, support, security, or governance workflow changes

For release-readiness execution details, consult `RELEASE-CHECKLIST.md`. For branch protection and
required CI checks, consult `.github/BRANCH-PROTECTION.md`.
