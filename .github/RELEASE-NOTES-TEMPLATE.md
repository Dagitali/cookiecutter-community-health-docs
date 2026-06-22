# Release Notes Template

Use this template when drafting GitHub Release notes for tagged cookiecutter-repo-governance
releases. GitHub Releases is the canonical release-history surface for the project.

- [Highlights](#highlights)
- [Breaking Changes](#breaking-changes)
- [Deprecations](#deprecations)
- [Fixes](#fixes)
- [Documentation and Maintenance](#documentation-and-maintenance)
- [Upgrade Notes](#upgrade-notes)
- [Support Boundary](#support-boundary)
- [Notes for Maintainers](#notes-for-maintainers)

## Highlights

- Summarize the most important user-visible changes in 2-5 bullets.
- Focus on generated template behavior, repository governance docs, and maintainer workflow changes.

## Breaking Changes

- List any breaking change explicitly.
- If none, write `None.`

## Deprecations

- List any newly deprecated Cookiecutter settings, generated file paths, or documented workflows.
- If none, write `None.`

## Fixes

- Summarize the most important bug fixes.
- Prefer behavior-focused language over internal implementation detail.

## Documentation and Maintenance

- Call out important docs improvements, CI changes, template validation changes, or
  contributor-facing maintenance work.

## Upgrade Notes

- Mention any required user action, changed Cookiecutter input, generated-file migration, or
  compatibility expectation.
- If nothing special is required, write `No special upgrade steps.`

## Support Boundary

- Re-state any release-specific support or stability caveats when needed.
- Keep the message aligned with `README.md` and `SUPPORT.md`.

## Notes for Maintainers

- Cross-check generated GitHub release notes against this template.
- Make sure breaking changes and deprecations are never left only in the auto-generated pull request
  summary.
- Keep terminology consistent with the documented template surface.
