# Release Checklist

Use this checklist when preparing a tagged cookiecutter-repo-governance release.

The generated project release checklist is maintained separately in the Cookiecutter template
directory.

- [Scope](#scope)
- [Pre-Release Checks](#pre-release-checks)
- [Template Rendering Checks](#template-rendering-checks)
- [Documentation Checks](#documentation-checks)
- [Release Preparation](#release-preparation)
- [Tagging](#tagging)
- [Post-Release Checks](#post-release-checks)
- [Implemented Improvements](#implemented-improvements)

## Scope

This checklist covers public releases of the Cookiecutter template repository. It is focused on
template correctness, generated governance documents, local maintenance tooling, and GitHub release
metadata.

It does not cover private operator procedures, credential handling, or project-specific release
steps for repositories generated from this template.

Releases do not publish to PyPI, do not publish Read the Docs documentation, and do not attach built
Python distribution artifacts.

## Pre-Release Checks

- [ ] Confirm the release scope is appropriate for the planned SemVer increment.
- [ ] Confirm `main` and `develop` are synced before tagging, or document why a release/hotfix
      sequence intentionally leaves follow-up sync work.
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
- [ ] Confirm rendered host-specific paths match documented paths exactly, including filename case.
- [ ] Confirm rendered Markdown does not contain unresolved Cookiecutter or Jinja syntax.
- [ ] Confirm rendered repository URLs, support contacts, security contacts, and branch names match
      the selected Cookiecutter inputs.

Generated-output smoke commands:

```bash
cookiecutter . --no-input
pytest tests/integration/test_i_cookiecutter_render.py
```

## Documentation Checks

- [ ] Confirm root community-health files do not contain Cookiecutter template variables.
- [ ] Confirm generated template files under the Cookiecutter template directory contain only
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
- [ ] Confirm generated GitHub release notes were reviewed against `.github/RELEASE-NOTES-TEMPLATE.md`.
- [ ] Confirm breaking changes, deprecated settings, generated file additions/removals, and
      migration notes are explicit.
- [ ] Confirm the release branch has been merged through the protected-branch workflow.

Recommended local commands:

```bash
make release-check
SKIP=no-commit-to-branch pre-commit run --all-files
ruff check hooks tests
pytest
```

## Tagging

- [ ] Check out the authoritative release commit on `main`.
- [ ] Confirm the tag points at the authoritative merged `main` commit.
- [ ] Create an annotated SemVer tag.
- [ ] Push the tag to GitHub.
- [ ] Confirm pushing the `v*.*.*` tag triggers `.github/workflows/cd.yml`.
- [ ] Confirm `.github/workflows/cd.yml` publishes the GitHub Release automatically from the pushed
      tag.

Example:

```bash
git fetch origin main
git tag -a v1.2.6 origin/main -m "Release v1.2.6"
git push origin v1.2.6
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

## Implemented Improvements

- [x] Add automated checks for unresolved Cookiecutter or Jinja syntax in rendered Markdown.
- [x] Add automated checks for generated local Markdown links.
- [x] Add automated checks for host-specific rendered paths.
- [x] Add independent optional-document render tests.
- [x] Make generated release-note checklist guidance host-aware.
- [x] Add a local `release-check` command target.
- [x] Add regression coverage for GitHub release-note categories.
- [x] Add automated checks that root Markdown has no unresolved Cookiecutter or Jinja syntax.
- [x] Add automated checks for root local Markdown links.
- [x] Add automated checks that README generated-file inventory points to template files.
- [x] Remove stale root `SUPPORT.md` reference to missing `REFERENCES.md`.
- [x] Make generated post-release checklist guidance branch-model-aware.
- [x] Add a CI/CD workflow map for the template repository workflows.
- [x] Add automated checks that the CI/CD workflow map lists every GitHub Actions workflow.
- [x] Update README maintainer docs to name every workflow covered by the CI/CD workflow map.
- [x] Add automated checks that README names every workflow from the CI/CD workflow map.
- [x] Add Git hosting platform references for every supported `git_service` option.
- [x] Add automated checks that REFERENCES covers every supported `git_service` option.
- [x] Add automated checks that README documents every public Cookiecutter input.
- [x] Add automated checks that README generated-file inventory covers every template source file.
- [x] Remove stale PR-gates advisory check examples from branch protection docs.
- [x] Add automated checks that branch protection docs list current PR Gates and CI check names.
- [x] Harmonize PR Gates workflow wording with the shared GitFlow workflow pattern.
- [x] Align PR Gates external-action note with the shared pinned-action security posture.
- [x] Update branch protection guidance for the expanded PR Gates check set.
- [x] Update CI/CD workflow map for the expanded PR Gates responsibilities.
- [x] Add a separate PR Gates meta-guardrail step and XML coverage output.
- [x] Broaden the PR Gates meta-guardrail step to the full meta test suite.
- [x] Normalize branch protection nested check-list indentation.
- [x] Align CI workflow triggers with the shared protected-branch validation model.
- [x] Update the CI/CD workflow map for the protected-branch CI trigger model.
