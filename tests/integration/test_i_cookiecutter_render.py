"""Integration tests for rendering the community health Cookiecutter template."""

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
        'public_key',
        [
            'change_request_name',
            'change_request_name_plural',
            '__change_request_name_plural',
        ],
    )
    def test_change_request_variables_are_not_public_prompts(
        self,
        cookiecutter_config: dict[str, Any],
        public_key: str,
    ) -> None:
        """
        Test that change request variables are not public prompts in the
        Cookiecutter configuration.
        """
        assert public_key not in cookiecutter_config

    def test_change_request_variable_is_hidden_prompt(
        self,
        cookiecutter_config: dict[str, Any],
    ) -> None:
        """
        Test that the change request variable is a hidden prompt in the
        Cookiecutter configuration.
        """
        assert '__change_request_name' in cookiecutter_config


class TestGitHostingServiceRendering:
    """Integration test suite for host-specific rendered output."""

    @pytest.mark.parametrize(
        (
            'git_hosting_service',
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
                    '.github/ISSUE_TEMPLATE/bug_report.md',
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
        git_hosting_service: str,
        extra_context: dict[str, str],
        expected_paths: list[str],
        missing_paths: list[str],
        expected_text: str,
    ) -> None:
        project = render_project(
            git_hosting_service=git_hosting_service,
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
        project = render_project(git_hosting_service='GitHub')

        assert f"Copyright {datetime.now().year}" in (
            project / 'LICENSE'
        ).read_text(
            encoding='utf-8',
        )


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
            git_hosting_service='GitHub',
            include_release_docs='no',
            include_branch_protection_docs='no',
            include_maintainer_runbooks='no',
            include_references='no',
            include_agents_md='no',
        )

        assert not (project / missing_path).exists()
