"""
:mod:`tests.integration.test_i_cookiecutter_render` module.

Integration tests for rendering the repository governance Cookiecutter
template.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from collections.abc import Iterable
from datetime import datetime
from pathlib import Path
from typing import Any

import pytest

from tests.pytest_helpers import SUPPORTED_GIT_SERVICES
from tests.pytest_helpers import UNRESOLVED_TEMPLATE_PATTERNS
from tests.pytest_helpers import local_markdown_links
from tests.pytest_helpers import markdown_files

# SECTION: PRAGMAS ========================================================== #

# pylint: disable=import-outside-toplevel,protected-access,unused-argument

# SECTION: TYPE ALIASES ===================================================== #


type RenderProject = Callable[..., Path]


# SECTION: INTERNAL FUNCTIONS =============================================== #


def _assert_paths(
    project: Path,
    *,
    existing: Iterable[str] = (),
    missing: Iterable[str] = (),
) -> None:
    """Assert rendered paths exist or are omitted under a project."""
    for expected_path in existing:
        assert (project / expected_path).exists(), f'{expected_path} was not rendered'

    for missing_path in missing:
        assert not (project / missing_path).exists(), (
            f'{missing_path} should not have been rendered'
        )


def _assert_text(
    text: str,
    *,
    contains: Iterable[str] = (),
    omits: Iterable[str] = (),
) -> None:
    """Assert text includes or omits expected snippets."""
    for expected_text in contains:
        assert expected_text in text

    for missing_text in omits:
        assert missing_text not in text


def _markdown_heading_anchor(
    heading_text: str,
) -> str:
    """Return the GitHub-style heading anchor for Markdown heading text."""
    normalized = re.sub(r'[`*_]', '', heading_text).casefold()
    normalized = re.sub(r'[^\w\s-]', '', normalized)
    return re.sub(r'\s+', '-', normalized.strip())


def _markdown_heading_anchors(
    markdown: str,
) -> set[str]:
    """Return heading anchors available in a Markdown document."""
    anchors: set[str] = set()
    in_fenced_block = False
    for line in markdown.splitlines():
        if line.startswith('```'):
            in_fenced_block = not in_fenced_block
            continue
        if in_fenced_block:
            continue
        match = re.match(r'#{1,6}\s+(.+?)\s*#*$', line)
        if match is not None:
            anchors.add(_markdown_heading_anchor(match.group(1)))
    return anchors


def _markdown_internal_links(
    markdown: str,
) -> tuple[str, ...]:
    """Return internal anchor links from a Markdown document."""
    return tuple(
        link.removeprefix('#').split('#', maxsplit=1)[0]
        for link in re.findall(r'(?<!!)\[[^\]]+\]\((#[^)]+)\)', markdown)
    )


# SECTION: TESTS ============================================================ #


class TestCookiecutterContext:
    """Integration test suite for Cookiecutter context behavior."""

    @pytest.mark.parametrize(
        ('prompt_key', 'expected_present'),
        [
            ('__change_request_name', True),
            ('__change_request_name_plural', False),
            ('__repo_base_urls', True),
            ('__repo_paths', True),
            ('__year', True),
            ('change_request_name', False),
            ('change_request_name_plural', False),
            ('repository_base_urls', False),
            ('repository_paths', False),
            ('year', False),
        ],
    )
    def test_derived_variable_prompt_visibility(
        self,
        cookiecutter_config: dict[str, Any],
        prompt_key: str,
        expected_present: bool,
    ) -> None:
        """Test that derived variable prompts expose only hidden inputs."""
        assert (prompt_key in cookiecutter_config) is expected_present

    def test_github_is_default_hosting_service(
        self,
        cookiecutter_config: dict[str, Any],
    ) -> None:
        """Test that GitHub is the default Git hosting service prompt value."""
        assert cookiecutter_config['git_service'][0] == 'GitHub'


class TestGitHostingServiceRendering:
    """Integration test suite for host-specific rendered output."""

    @pytest.mark.parametrize(
        ('include_discussions_link', 'expected_text', 'missing_text'),
        [
            (
                'yes',
                'https://github.com/example/example-project/discussions',
                '',
            ),
            (
                'no',
                'mailto:support@example.com',
                '/discussions',
            ),
        ],
    )
    def test_github_issue_config_discussions_link_is_optional(
        self,
        render_project: RenderProject,
        include_discussions_link: str,
        expected_text: str,
        missing_text: str,
    ) -> None:
        """Test that GitHub issue config can omit the Discussions link."""
        project = render_project(
            git_service='GitHub',
            include_discussions_link=include_discussions_link,
        )
        issue_config = (
            project / '.github' / 'ISSUE_TEMPLATE' / 'config.yml'
        ).read_text(encoding='utf-8')

        _assert_text(
            issue_config,
            contains=[expected_text],
            omits=[missing_text] if missing_text else (),
        )

    def test_github_license_uses_current_year(
        self,
        render_project: RenderProject,
    ) -> None:
        """Test that the rendered GitHub license uses the current year."""
        project = render_project(git_service='GitHub')

        assert f'Copyright {datetime.now().year}' in (project / 'LICENSE').read_text(
            encoding='utf-8',
        )

    @pytest.mark.parametrize(
        (
            'git_service',
            'extra_context',
            'expected_paths',
            'missing_paths',
            'expected_text',
        ),
        [
            (
                'GitHub',
                {
                    'include_funding': 'yes',
                    'sponsor_url': 'https://example.com/sponsor',
                },
                [
                    '.github/ISSUE_TEMPLATE/bug_report.yml',
                    '.github/ISSUE_TEMPLATE/config.yml',
                    '.github/ISSUE_TEMPLATE/feature_request.yml',
                    '.github/pull_request_template.md',
                    '.github/FUNDING.yml',
                    'RELEASE-POLICY.md',
                ],
                [
                    '.gitlab',
                ],
                'Open a pull request',
            ),
            (
                'GitLab',
                {},
                [
                    '.gitlab/issue_templates/Bug.md',
                    '.gitlab/merge_request_templates/Default.md',
                ],
                [
                    '.github',
                    '.bitbucket',
                ],
                'Open a merge request',
            ),
            (
                'Bitbucket',
                {},
                [
                    '.bitbucket/PULL_REQUEST_TEMPLATE.md',
                ],
                [
                    '.github',
                    '.gitlab',
                    '.azuredevops',
                ],
                'Open a pull request',
            ),
            (
                'Azure DevOps',
                {},
                [
                    '.azuredevops/pull_request_template.md',
                ],
                [
                    '.github',
                    '.gitlab',
                    '.bitbucket',
                ],
                'Open a pull request',
            ),
        ],
    )
    def test_host_specific_templates_are_rendered(
        self,
        render_project: RenderProject,
        git_service: str,
        extra_context: dict[str, str],
        expected_paths: list[str],
        missing_paths: list[str],
        expected_text: str,
    ) -> None:
        project = render_project(
            git_service=git_service,
            **extra_context,
        )

        _assert_paths(project, existing=expected_paths, missing=missing_paths)

        assert expected_text in (project / 'CONTRIBUTING.md').read_text(
            encoding='utf-8',
        )

    @pytest.mark.parametrize(
        ('git_service', 'expected_url'),
        [
            (
                'GitHub',
                'https://github.com/example/example-project',
            ),
            (
                'GitLab',
                'https://gitlab.com/example/example-project',
            ),
            (
                'Bitbucket',
                'https://bitbucket.org/example/example-project',
            ),
            (
                'Azure DevOps',
                'https://dev.azure.com/example/example-project/_git/example-project',
            ),
        ],
    )
    def test_repo_url_is_derived_from_hosting_context(
        self,
        render_project: RenderProject,
        git_service: str,
        expected_url: str,
    ) -> None:
        """Test that repository URLs derive from selected hosting settings."""
        project = render_project(git_service=git_service)
        readme = (project / 'README.md').read_text(encoding='utf-8')
        support = (project / 'SUPPORT.md').read_text(encoding='utf-8')

        assert f'- Repository: {expected_url}' in readme
        assert f'- Repository: {expected_url}' in support


class TestBranchModelRendering:
    """Integration test suite for branch-model-specific rendered output."""

    @pytest.mark.parametrize(
        (
            'branch_model',
            'expected_texts',
            'missing_texts',
            'expects_branch_mapping',
        ),
        [
            (
                'GitFlow',
                [
                    'uses GitFlow-style branch roles',
                ],
                [
                    'uses GitHub Flow-style topic branches',
                    'short-lived and reviewable',
                ],
                True,
            ),
            (
                'GitHub Flow',
                [
                    'uses GitHub Flow-style topic branches',
                    'short-lived and reviewable',
                ],
                [
                    'uses GitFlow-style branch roles',
                ],
                False,
            ),
        ],
    )
    def test_contributing_workflow_matches_branch_model(
        self,
        render_project: RenderProject,
        branch_model: str,
        expected_texts: list[str],
        missing_texts: list[str],
        expects_branch_mapping: bool,
    ) -> None:
        project = render_project(branch_model=branch_model)
        contributing = (project / 'CONTRIBUTING.md').read_text(encoding='utf-8')

        assert (
            '- [Protected-Branch Workflow](#protected-branch-workflow)' in contributing
        )
        assert '## Protected-Branch Workflow' in contributing
        _assert_text(contributing, contains=expected_texts, omits=missing_texts)
        assert (
            '### Recommended Branch Mapping' in contributing
        ) is expects_branch_mapping

    @pytest.mark.parametrize(
        ('branch_model', 'expected_text', 'missing_text'),
        [
            (
                'GitFlow',
                'back into `develop` when\n      using a GitFlow branch model',
                'short-lived branches targeting\n      `main`',
            ),
            (
                'GitHub Flow',
                'short-lived branches targeting\n      `main`',
                'back into `develop` when\n      using a GitFlow branch model',
            ),
        ],
    )
    def test_release_checklist_post_release_matches_branch_model(
        self,
        render_project: RenderProject,
        branch_model: str,
        expected_text: str,
        missing_text: str,
    ) -> None:
        """Test that post-release steps match the selected branch model."""
        project = render_project(branch_model=branch_model)
        release_checklist = (project / 'RELEASE-CHECKLIST.md').read_text(
            encoding='utf-8',
        )

        _assert_text(
            release_checklist,
            contains=[expected_text],
            omits=[missing_text],
        )


class TestGeneratedReleaseChecklist:
    """Integration test suite for generated release-checklist structure."""

    @pytest.mark.parametrize('git_service', SUPPORTED_GIT_SERVICES)
    def test_release_checklist_keeps_release_sections(
        self,
        render_project: RenderProject,
        git_service: str,
    ) -> None:
        """Test that generated release checklists keep the expected sections."""
        project = render_project(git_service=git_service)
        release_checklist = (project / 'RELEASE-CHECKLIST.md').read_text(
            encoding='utf-8',
        )

        _assert_text(
            release_checklist,
            contains=[
                '# Release Checklist And Stable-Line Maintenance',
                '- [Pre-Release](#pre-release)',
                '- [Release](#release)',
                '- [Post-Release](#post-release)',
                '- [Stable-Line Maintenance](#stable-line-maintenance)',
                '## Pre-Release',
                '## Release',
                '## Post-Release',
                '## Stable-Line Maintenance',
            ],
        )

    @pytest.mark.parametrize(
        ('git_service', 'expected_text', 'missing_text'),
        [
            (
                'GitHub',
                'Draft release notes using `.github/RELEASE-NOTES-TEMPLATE.md`.',
                'Draft release notes for the selected release channel.',
            ),
            (
                'GitLab',
                'Draft release notes for the selected release channel.',
                '.github/RELEASE-NOTES-TEMPLATE.md',
            ),
            (
                'Bitbucket',
                'Draft release notes for the selected release channel.',
                '.github/RELEASE-NOTES-TEMPLATE.md',
            ),
            (
                'Azure DevOps',
                'Draft release notes for the selected release channel.',
                '.github/RELEASE-NOTES-TEMPLATE.md',
            ),
        ],
    )
    def test_release_checklist_release_notes_match_host(
        self,
        render_project: RenderProject,
        git_service: str,
        expected_text: str,
        missing_text: str,
    ) -> None:
        """Test that release-note guidance matches the rendered host."""
        project = render_project(git_service=git_service)
        release_checklist = (project / 'RELEASE-CHECKLIST.md').read_text(
            encoding='utf-8',
        )

        _assert_text(
            release_checklist,
            contains=[expected_text],
            omits=[missing_text],
        )


class TestGeneratedDocumentLinks:
    """Integration test suite for generated document link consistency."""

    @pytest.mark.parametrize(
        'git_service',
        SUPPORTED_GIT_SERVICES,
    )
    def test_contributing_avoids_unrendered_operational_links(
        self,
        render_project: RenderProject,
        git_service: str,
    ) -> None:
        """Test that CONTRIBUTING avoids known links to unrendered files."""
        project = render_project(git_service=git_service)
        contributing = (project / 'CONTRIBUTING.md').read_text(encoding='utf-8')

        omitted_links = [
            'CI-CD-WORKFLOWS.md',
            '.github/workflows/pr.yml',
            'python-project-lifecycle',
        ]

        if git_service != 'GitHub':
            omitted_links.extend(
                [
                    '.github/MAINTAINER-RUNBOOKS.md',
                    '.github/BRANCH-PROTECTION.md',
                ],
            )

        _assert_text(contributing, omits=omitted_links)

    @pytest.mark.parametrize(
        'git_service',
        SUPPORTED_GIT_SERVICES,
    )
    def test_generated_markdown_links_point_to_existing_files(
        self,
        render_project: RenderProject,
        git_service: str,
    ) -> None:
        """Test that generated local Markdown links resolve to rendered files."""
        project = render_project(git_service=git_service)

        for markdown_file in markdown_files(project):
            markdown = markdown_file.read_text(encoding='utf-8')
            for link in local_markdown_links(markdown):
                target = link.split('#', maxsplit=1)[0]
                if not target:
                    continue
                assert (markdown_file.parent / target).exists(), (
                    f'{markdown_file.relative_to(project)} links to missing '
                    f'target {link}'
                )

    @pytest.mark.parametrize(
        'git_service',
        SUPPORTED_GIT_SERVICES,
    )
    def test_generated_markdown_links_point_to_existing_heading_anchors(
        self,
        render_project: RenderProject,
        git_service: str,
    ) -> None:
        """Test that generated internal Markdown links resolve to headings."""
        project = render_project(git_service=git_service)

        for markdown_file in markdown_files(project):
            markdown = markdown_file.read_text(encoding='utf-8')
            heading_anchors = _markdown_heading_anchors(markdown)
            for anchor in _markdown_internal_links(markdown):
                assert anchor in heading_anchors, (
                    f'{markdown_file.relative_to(project)} links to missing '
                    f'heading anchor #{anchor}'
                )

    @pytest.mark.parametrize(
        ('link_label', 'link_target'),
        [
            ('CONTRIBUTING.md', 'CONTRIBUTING.md'),
            ('SECURITY.md', 'SECURITY.md'),
            ('SUPPORT.md', 'SUPPORT.md'),
        ],
    )
    def test_readme_reference_links_are_valid(
        self,
        render_project: RenderProject,
        link_label: str,
        link_target: str,
    ) -> None:
        """Test that README reference links render as valid Markdown."""
        project = render_project(git_service='GitHub')
        readme = (project / 'README.md').read_text(encoding='utf-8')

        assert f'[{link_label}]: {link_target}' in readme
        assert f'[{link_label}]:' in readme
        assert f'[{link_label}] {link_target}' not in readme
        assert f'[{link_label}]: {link_target}]' not in readme


class TestGeneratedOutputQuality:
    """Integration test suite for rendered output quality gates."""

    @pytest.mark.parametrize(
        ('git_service', 'expected_paths', 'missing_paths'),
        [
            (
                'GitHub',
                [
                    '.github/ISSUE_TEMPLATE/bug_report.yml',
                    '.github/ISSUE_TEMPLATE/config.yml',
                    '.github/ISSUE_TEMPLATE/feature_request.yml',
                    '.github/pull_request_template.md',
                    '.github/RELEASE-NOTES-TEMPLATE.md',
                    '.github/MAINTAINER-RUNBOOKS.md',
                    '.github/BRANCH-PROTECTION.md',
                ],
                [
                    '.gitlab/issue_templates/Bug.md',
                    '.gitlab/merge_request_templates/Default.md',
                    '.bitbucket/PULL_REQUEST_TEMPLATE.md',
                    '.azuredevops/pull_request_template.md',
                ],
            ),
            (
                'GitLab',
                [
                    '.gitlab/issue_templates/Bug.md',
                    '.gitlab/merge_request_templates/Default.md',
                ],
                [
                    '.github/ISSUE_TEMPLATE/bug_report.yml',
                    '.github/pull_request_template.md',
                    '.bitbucket/PULL_REQUEST_TEMPLATE.md',
                    '.azuredevops/pull_request_template.md',
                ],
            ),
            (
                'Bitbucket',
                [
                    '.bitbucket/PULL_REQUEST_TEMPLATE.md',
                ],
                [
                    '.github/ISSUE_TEMPLATE/bug_report.yml',
                    '.github/pull_request_template.md',
                    '.gitlab/issue_templates/Bug.md',
                    '.azuredevops/pull_request_template.md',
                ],
            ),
            (
                'Azure DevOps',
                [
                    '.azuredevops/pull_request_template.md',
                ],
                [
                    '.github/ISSUE_TEMPLATE/bug_report.yml',
                    '.github/pull_request_template.md',
                    '.gitlab/issue_templates/Bug.md',
                    '.bitbucket/PULL_REQUEST_TEMPLATE.md',
                ],
            ),
        ],
    )
    def test_documented_host_specific_paths_match_rendered_output(
        self,
        render_project: RenderProject,
        git_service: str,
        expected_paths: list[str],
        missing_paths: list[str],
    ) -> None:
        """Test that documented host-specific paths match rendered output."""
        project = render_project(git_service=git_service)

        _assert_paths(project, existing=expected_paths, missing=missing_paths)

    @pytest.mark.parametrize(
        'git_service',
        SUPPORTED_GIT_SERVICES,
    )
    def test_rendered_markdown_has_no_unresolved_template_syntax(
        self,
        render_project: RenderProject,
        git_service: str,
    ) -> None:
        """Test that rendered Markdown contains no unresolved Jinja syntax."""
        project = render_project(git_service=git_service)
        for markdown_file in markdown_files(project):
            markdown = markdown_file.read_text(encoding='utf-8')
            assert not any(
                pattern in markdown for pattern in UNRESOLVED_TEMPLATE_PATTERNS
            ), (
                f'{markdown_file.relative_to(project)} contains unresolved '
                'Cookiecutter or Jinja syntax'
            )


class TestOptionalDocuments:
    """Integration test suite for optional generated documents."""

    @pytest.mark.parametrize(
        ('extra_context', 'missing_paths', 'expected_paths'),
        [
            (
                {'include_release_docs': 'no'},
                [
                    'RELEASE-POLICY.md',
                    'RELEASE-CHECKLIST.md',
                    '.github/RELEASE-NOTES-TEMPLATE.md',
                ],
                [
                    '.github/BRANCH-PROTECTION.md',
                    '.github/MAINTAINER-RUNBOOKS.md',
                ],
            ),
            (
                {'include_branch_protection_docs': 'no'},
                ['.github/BRANCH-PROTECTION.md'],
                [
                    'RELEASE-POLICY.md',
                    'RELEASE-CHECKLIST.md',
                    '.github/MAINTAINER-RUNBOOKS.md',
                ],
            ),
            (
                {'include_maintainer_runbooks': 'no'},
                ['.github/MAINTAINER-RUNBOOKS.md'],
                [
                    'RELEASE-POLICY.md',
                    'RELEASE-CHECKLIST.md',
                    '.github/BRANCH-PROTECTION.md',
                ],
            ),
            (
                {'include_references': 'no'},
                ['REFERENCES.md'],
                [
                    'RELEASE-POLICY.md',
                    'RELEASE-CHECKLIST.md',
                    '.github/BRANCH-PROTECTION.md',
                ],
            ),
            (
                {'include_agents_md': 'no'},
                ['AGENTS.md'],
                [
                    'RELEASE-POLICY.md',
                    'RELEASE-CHECKLIST.md',
                    '.github/BRANCH-PROTECTION.md',
                ],
            ),
            (
                {
                    'include_funding': 'no',
                    'sponsor_url': 'https://example.com/sponsor',
                },
                ['.github/FUNDING.yml'],
                [
                    'RELEASE-POLICY.md',
                    'RELEASE-CHECKLIST.md',
                    '.github/BRANCH-PROTECTION.md',
                ],
            ),
        ],
    )
    def test_optional_documents_can_be_removed(
        self,
        render_project: RenderProject,
        extra_context: dict[str, str],
        missing_paths: list[str],
        expected_paths: list[str],
    ) -> None:
        project = render_project(
            git_service='GitHub',
            **extra_context,
        )

        _assert_paths(project, existing=expected_paths, missing=missing_paths)


class TestReleaseNotesConfiguration:
    """Integration test suite for GitHub release-note configuration."""

    @pytest.mark.parametrize(
        ('category', 'labels'),
        [
            ('Breaking Changes', ['breaking-change', 'breaking']),
            ('Features', ['feature', 'enhancement']),
            ('Fixes', ['bug', 'bugfix', 'fix']),
            ('Documentation', ['documentation', 'docs']),
            ('Maintenance', ['chore', 'dependencies', 'ci']),
        ],
    )
    def test_release_notes_categories_include_expected_labels(
        self,
        release_config: str,
        category: str,
        labels: list[str],
    ) -> None:
        """Test that release-note categories keep expected labels."""
        assert f'title: {category}' in release_config
        for label in labels:
            assert f'- {label}' in release_config

    @pytest.mark.parametrize(
        'label',
        [
            'skip-release-notes',
            'internal',
        ],
    )
    def test_release_notes_exclude_internal_labels(
        self,
        release_config: str,
        label: str,
    ) -> None:
        """Test that release-note generation excludes internal labels."""
        assert f'- {label}' in release_config
