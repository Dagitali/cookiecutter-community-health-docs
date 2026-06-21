"""Integration tests for rendering the repository governance Cookiecutter template."""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import Any

import pytest

# SECTION: PRAGMAS ========================================================== #

# pylint: disable=import-outside-toplevel,protected-access,unused-argument

# SECTION: TEST SUITES ====================================================== #


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
                    '.github/PULL_REQUEST_TEMPLATE.md',
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
        'missing_path',
        [
            'RELEASE-POLICY.md',
            'RELEASE-CHECKLIST.md',
            'REFERENCES.md',
            'AGENTS.md',
            '.github/MAINTAINER-RUNBOOKS.md',
        ],
    )
    def test_optional_documents_can_be_removed(
        self,
        render_project: Callable[..., Path],
        missing_path: str,
    ) -> None:
        project = render_project(
            git_service='GitHub',
            include_release_docs='no',
            include_branch_protection_docs='no',
            include_maintainer_runbooks='no',
            include_references='no',
            include_agents_md='no',
        )

        assert not (project / missing_path).exists()


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
