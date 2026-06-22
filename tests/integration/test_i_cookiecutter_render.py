"""Integration tests for rendering the repository governance Cookiecutter template."""

from __future__ import annotations

import re
from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import Any

import pytest

# SECTION: PRAGMAS ========================================================== #

# pylint: disable=import-outside-toplevel,protected-access,unused-argument

# SECTION: CONSTANTS ======================================================== #


PROJECT_ROOT = Path(__file__).resolve().parents[2]


# SECTION: INTERNAL FUNCTIONS =============================================== #


def _markdown_files(
    project: Path,
) -> list[Path]:
    """Return generated Markdown files below the rendered project."""
    return sorted(project.rglob('*.md'))


def _local_markdown_links(
    markdown: str,
) -> list[str]:
    """Return local Markdown link targets from a Markdown document."""
    links = []
    for target in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)', markdown):
        if (
            target.startswith(('http://', 'https://', 'mailto:', '#'))
            or target.startswith('<http')
        ):
            continue
        links.append(target.strip('<>'))
    return links


# SECTION: TESTS ============================================================ #


class TestCookiecutterContext:
    """Integration test suite for Cookiecutter context behavior."""

    @pytest.mark.parametrize(
        'hidden_key',
        [
            '__change_request_name',
            '__repo_base_urls',
            '__repo_paths',
            '__year',
        ],
    )
    def test_derived_variables_are_hidden_prompts(
        self,
        cookiecutter_config: dict[str, Any],
        hidden_key: str,
    ) -> None:
        """Test that derived variables are hidden Cookiecutter prompts."""
        assert hidden_key in cookiecutter_config

    @pytest.mark.parametrize(
        'public_key',
        [
            'change_request_name',
            'change_request_name_plural',
            '__change_request_name_plural',
            'repository_base_urls',
            'repository_paths',
            'year',
        ],
    )
    def test_derived_variables_are_not_public_prompts(
        self,
        cookiecutter_config: dict[str, Any],
        public_key: str,
    ) -> None:
        """
        Test that derived variables are not public prompts in the Cookiecutter
        configuration.
        """
        assert public_key not in cookiecutter_config

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
        render_project: Callable[..., Path],
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

        assert expected_text in issue_config
        if missing_text:
            assert missing_text not in issue_config

    def test_github_license_uses_current_year(
        self,
        render_project: Callable[..., Path],
    ) -> None:
        project = render_project(git_service='GitHub')

        assert f"Copyright {datetime.now().year}" in (
            project / 'LICENSE'
        ).read_text(
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
        render_project: Callable[..., Path],
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

        for expected_path in expected_paths:
            assert (project / expected_path).exists()

        for missing_path in missing_paths:
            assert not (project / missing_path).exists()

        assert expected_text in (project / 'CONTRIBUTING.md').read_text(
            encoding='utf-8',
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
        render_project: Callable[..., Path],
        git_service: str,
        expected_text: str,
        missing_text: str,
    ) -> None:
        """Test that release-note guidance matches the rendered host."""
        project = render_project(git_service=git_service)
        release_checklist = (project / 'RELEASE-CHECKLIST.md').read_text(
            encoding='utf-8',
        )

        assert expected_text in release_checklist
        assert missing_text not in release_checklist

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
        render_project: Callable[..., Path],
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
        render_project: Callable[..., Path],
        branch_model: str,
        expected_texts: list[str],
        missing_texts: list[str],
        expects_branch_mapping: bool,
    ) -> None:
        project = render_project(branch_model=branch_model)
        contributing = (project / 'CONTRIBUTING.md').read_text(encoding='utf-8')

        assert (
            '- [Protected-Branch Workflow](#protected-branch-workflow)'
            in contributing
        )
        assert '## Protected-Branch Workflow' in contributing
        for expected_text in expected_texts:
            assert expected_text in contributing
        for missing_text in missing_texts:
            assert missing_text not in contributing
        assert (
            ('### Recommended Branch Mapping' in contributing)
            is expects_branch_mapping
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
        render_project: Callable[..., Path],
        extra_context: dict[str, str],
        missing_paths: list[str],
        expected_paths: list[str],
    ) -> None:
        project = render_project(
            git_service='GitHub',
            **extra_context,
        )

        for missing_path in missing_paths:
            assert not (project / missing_path).exists()

        for expected_path in expected_paths:
            assert (project / expected_path).exists()


class TestGeneratedDocumentLinks:
    """Integration test suite for generated document link consistency."""

    @pytest.mark.parametrize(
        'git_service',
        [
            'GitHub',
            'GitLab',
            'Bitbucket',
            'Azure DevOps',
        ],
    )
    def test_contributing_avoids_unrendered_operational_links(
        self,
        render_project: Callable[..., Path],
        git_service: str,
    ) -> None:
        """Test that CONTRIBUTING avoids known links to unrendered files."""
        project = render_project(git_service=git_service)
        contributing = (project / 'CONTRIBUTING.md').read_text(encoding='utf-8')

        assert 'CI-CD-WORKFLOWS.md' not in contributing
        assert '.github/workflows/pr.yml' not in contributing
        assert 'python-project-lifecycle' not in contributing

        if git_service != 'GitHub':
            assert '.github/MAINTAINER-RUNBOOKS.md' not in contributing
            assert '.github/BRANCH-PROTECTION.md' not in contributing

    @pytest.mark.parametrize(
        'git_service',
        [
            'GitHub',
            'GitLab',
            'Bitbucket',
            'Azure DevOps',
        ],
    )
    def test_generated_markdown_links_point_to_existing_files(
        self,
        render_project: Callable[..., Path],
        git_service: str,
    ) -> None:
        """Test that generated local Markdown links resolve to rendered files."""
        project = render_project(git_service=git_service)

        for markdown_file in _markdown_files(project):
            markdown = markdown_file.read_text(encoding='utf-8')
            for link in _local_markdown_links(markdown):
                target = link.split('#', maxsplit=1)[0]
                if not target:
                    continue
                assert (markdown_file.parent / target).exists(), (
                    f'{markdown_file.relative_to(project)} links to missing '
                    f'target {link}'
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
        render_project: Callable[..., Path],
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
        render_project: Callable[..., Path],
        git_service: str,
        expected_paths: list[str],
        missing_paths: list[str],
    ) -> None:
        """Test that documented host-specific paths match rendered output."""
        project = render_project(git_service=git_service)

        for expected_path in expected_paths:
            assert (project / expected_path).exists()

        for missing_path in missing_paths:
            assert not (project / missing_path).exists()

    @pytest.mark.parametrize(
        'git_service',
        [
            'GitHub',
            'GitLab',
            'Bitbucket',
            'Azure DevOps',
        ],
    )
    def test_rendered_markdown_has_no_unresolved_template_syntax(
        self,
        render_project: Callable[..., Path],
        git_service: str,
    ) -> None:
        """Test that rendered Markdown contains no unresolved Jinja syntax."""
        project = render_project(git_service=git_service)
        unresolved_patterns = ('{{', '{%', '{#')

        for markdown_file in _markdown_files(project):
            markdown = markdown_file.read_text(encoding='utf-8')
            assert not any(pattern in markdown for pattern in unresolved_patterns), (
                f'{markdown_file.relative_to(project)} contains unresolved '
                'Cookiecutter or Jinja syntax'
            )


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
        category: str,
        labels: list[str],
    ) -> None:
        """Test that release-note categories keep expected labels."""
        release_config = (PROJECT_ROOT / '.github' / 'release.yml').read_text(
            encoding='utf-8',
        )

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
        label: str,
    ) -> None:
        """Test that release-note generation excludes internal labels."""
        release_config = (PROJECT_ROOT / '.github' / 'release.yml').read_text(
            encoding='utf-8',
        )

        assert f'- {label}' in release_config
