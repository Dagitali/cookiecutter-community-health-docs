# Release Checklist

Use this checklist when preparing a tagged cookiecutter-repo-governance release.

- [Scope](#scope)
- [Pre-Release Checks](#pre-release-checks)
- [Template Rendering Checks](#template-rendering-checks)
- [Documentation Checks](#documentation-checks)
- [Release Preparation](#release-preparation)
- [Tagging](#tagging)
- [Post-Release Checks](#post-release-checks)

## Scope

This checklist covers public releases of the Cookiecutter template repository. It is focused on
template correctness, generated governance documents, local maintenance tooling, and GitHub release
metadata.

It does not cover private operator procedures, credential handling, or project-specific release
steps for repositories generated from this template.

## Pre-Release Checks

- [ ] Confirm the release scope is appropriate for the planned SemVer increment.
- [ ] Confirm `README.md`, `CONTRIBUTING.md`, `SUPPORT.md`, and `RELEASE-POLICY.md` describe the
      current repository behavior.
- [ ] Confirm `.github/BRANCH-PROTECTION.md` reflects current CI job names and protected branches.
- [ ] Confirm `.github/RELEASE-NOTES-TEMPLATE.md` reflects the release-note style for this
      template.
- [ ] Confirm `.github/release.yml` categorizes release-note entries correctly.

## Template Rendering Checks

- [ ] Render the template with default inputs.
- [ ] Render at least one GitHub configuration.
- [ ] Render at least one non-GitHub configuration.
- [ ] Confirm provider-specific directories are kept or removed as expected.
- [ ] Confirm rendered Markdown does not contain unresolved Cookiecutter or Jinja syntax.
- [ ] Confirm rendered repository URLs, support contacts, security contacts, and branch names match
      the selected Cookiecutter inputs.

## Documentation Checks

- [ ] Confirm root community-health files do not contain Cookiecutter template variables.
- [ ] Confirm generated template files under `{{cookiecutter.project_slug}}/` contain only
      intentional Cookiecutter variables.
- [ ] Confirm root documentation links point to existing root files.
- [ ] Confirm generated documentation links point to files that will exist after rendering.
- [ ] Confirm issue templates, pull request templates, funding metadata, branch protection docs, and
      maintainer runbooks use cookiecutter-repo-governance terminology.

## Release Preparation

- [ ] Run repository hygiene checks.
- [ ] Run Python lint checks.
- [ ] Run the test suite.
- [ ] Run or review `.github/workflows/sbom.yml` as an advisory supply-chain check, and confirm the
      `sbom` artifact was generated if the workflow was run.
- [ ] Review untracked files and confirm all release-intended files are committed.
- [ ] Update release notes using `.github/RELEASE-NOTES-TEMPLATE.md`.
- [ ] Confirm the release branch has been merged through the protected-branch workflow.

Recommended local commands:

```bash
SKIP=no-commit-to-branch pre-commit run --all-files
ruff check hooks tests
pytest
```

## Tagging

- [ ] Check out the authoritative release commit on `main`.
- [ ] Create an annotated SemVer tag.
- [ ] Push the tag to GitHub.
- [ ] Confirm pushing the `v*.*.*` tag triggers `.github/workflows/cd.yml`.
- [ ] Confirm `.github/workflows/cd.yml` publishes the GitHub Release automatically from the pushed
      tag.

Example:

```bash
git fetch origin main
git tag -a v0.3.0 origin/main -m "Release v0.3.0"
git push origin v0.3.0
```

## Post-Release Checks

- [ ] Confirm the `.github/workflows/cd.yml` `Publish GitHub release` job completed successfully.
- [ ] If `.github/workflows/sbom.yml` was run for the release, review the uploaded `sbom` artifact
      for obvious dependency or tooling surprises.
- [ ] Confirm the GitHub Release exists and has accurate release notes.
- [ ] Confirm release notes call out breaking changes, deprecations, and upgrade notes when
      applicable.
- [ ] Confirm `main` has been synced back into `develop` after release or hotfix work.
- [ ] Confirm follow-up maintenance issues are filed for deferred work.
