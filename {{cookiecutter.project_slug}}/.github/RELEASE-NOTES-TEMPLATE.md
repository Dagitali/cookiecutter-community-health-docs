# {{ cookiecutter.project_name }} Release Notes Template

Use this template when drafting GitHub Release notes for tagged {{ cookiecutter.project_name }}
releases. GitHub Releases is the canonical release-history surface for the project when the
repository is hosted on GitHub.

- [Highlights](#highlights)
- [Breaking Changes](#breaking-changes)
- [Deprecations](#deprecations)
- [Fixes](#fixes)
- [Documentation And Maintenance](#documentation-and-maintenance)
- [Upgrade Notes](#upgrade-notes)
- [Support Boundary](#support-boundary)
- [Notes For Maintainers](#notes-for-maintainers)

## Highlights

- Summarize the most important user-visible changes in 2-5 bullets.
- Focus on what users can now do, what became more reliable, or what changed in support
  expectations.

## Breaking Changes

- List any breaking change explicitly.
- If none, write `None.`

## Deprecations

- List any newly deprecated settings, file paths, workflows, APIs, or supported behaviors.
- If none, write `None.`

## Fixes

- Summarize the most important bug fixes.
- Prefer behavior-focused language over internal implementation detail.

## Documentation And Maintenance

- Call out important docs improvements, CI changes, release automation changes, or contributor-facing
  maintenance work.

## Upgrade Notes

- Mention any required user action, dependency change, migration step, or compatibility expectation.
- If nothing special is required, write `No special upgrade steps.`

## Support Boundary

- Re-state any release-specific support or stability caveats when needed.
- Keep the message aligned with [README](../README.md) and [SUPPORT](../SUPPORT.md).

## Notes For Maintainers

- Cross-check generated GitHub release notes against this template.
- Make sure breaking changes and deprecations are never left only in generated summaries.
- Keep terminology consistent with the documented stable surface in the README.
