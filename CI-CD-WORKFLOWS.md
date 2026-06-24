# CI/CD Workflow Map

This document explains the public role of each GitHub Actions workflow used by
cookiecutter-repo-governance.

- [Scope](#scope)
- [Workflow Overview](#workflow-overview)
- [PR Gates](#pr-gates)
- [CI](#ci)
- [Release](#release)
- [SBOM](#sbom)
- [How They Interact](#how-they-interact)
- [Required Checks](#required-checks)

## Scope

This file is public and describes the visible workflow structure. It does not include secrets,
credential handling, or emergency operator procedures.

## Workflow Overview

cookiecutter-repo-governance currently separates automation into 4 workflows:

- `pr.yml` for required pull-request and merge-queue gates
- `ci.yml` for heavier pre-merge validation on protected branches and merge queue
- `cd.yml` for tagged release publication
- `sbom.yml` for advisory Software Bill of Materials generation

This split keeps required PR checks fast enough to use as branch-protection gates while moving
template validation, release publication, and supply-chain inspection into separate workflows.

## PR Gates

Workflow file: `.github/workflows/pr.yml`

Workflow name: `PR Gates`

Primary role:

- Run the required validation used by protected-branch pull requests and merge queues

Current responsibilities:

- Enforce GitFlow pull-request target rules
- Allow merge-queue events to inherit queued pull-request target validation
- Run Ruff lint checks on the primary and next supported Python lines
- Run meta guardrails before the broader test suite
- Run tests with coverage on the primary and next supported Python lines
- Run docstring lint checks on the primary supported Python line
- Run type checks for the post-generation hook module

This workflow runs on pull requests into protected branches and also on pushes to the working and
release-oriented branches that feed later validation.

## CI

Workflow file: `.github/workflows/ci.yml`

Workflow name: `CI`

Primary role:

- Run heavier pre-merge validation for protected-branch pull requests and merge queue entries

Current responsibilities:

- Run repository hygiene checks through `pre-commit`
- Run Ruff lint checks for hooks and tests
- Run unit tests for post-generation hook helpers
- Run integration and meta tests for rendered Cookiecutter output and repository documentation

This workflow runs on pull requests into `main` and `develop`, on `merge_group` for those same
protected branches, and manually via `workflow_dispatch`.

## Release

Workflow file: `.github/workflows/cd.yml`

Workflow name: `Release`

Primary role:

- Validate and publish tagged template releases

Current responsibilities:

- Validate the tagged Cookiecutter template with pre-commit checks and tests
- Publish a GitHub Release with generated release notes
- Avoid PyPI, distribution artifact, and hosted documentation publication

This workflow is tag-driven. It runs when a `v*.*.*` tag is pushed.

## SBOM

Workflow file: `.github/workflows/sbom.yml`

Workflow name: `SBOM`

Primary role:

- Generate an advisory Software Bill of Materials for the template-maintenance environment

Current responsibilities:

- Generate a CycloneDX SBOM from the Python development dependencies
- Upload the SBOM as a workflow artifact for maintainer inspection

This workflow runs on pull requests into `main` and `develop`, on pushes to those branches, and
manually via `workflow_dispatch`.

## How They Interact

The workflows intentionally do not form a single linear chain.

- `PR Gates` is the required branch-protection workflow.
- `CI` runs alongside `PR Gates` when protected-branch pull requests or merge-queue entries need
  the heavier repository-hygiene and template-validation set.
- `Release` does not run because `CI` succeeded; it runs only when a release tag is pushed.
- `SBOM` is advisory and does not publish releases.

That means a successful `ci.yml` run is a confidence signal, not a publication trigger by itself.

## Required Checks

Protected branches must require checks from `PR Gates`. They may also require checks from `CI` when
you want repository hygiene and rendered-template validation to block merges.

At the time of writing, the expected required checks are:

- `Guard PR target branch`

The natural next checks to require, if you want the heavier protected-branch gate to block merges on
GitHub too, are:

- `Repository hygiene checks`
- `Template validation on Python 3.13`
- `Template validation on Python 3.14`

The exact protected-branch settings and GitHub configuration details are maintained separately in
`.github/BRANCH-PROTECTION.md`.
