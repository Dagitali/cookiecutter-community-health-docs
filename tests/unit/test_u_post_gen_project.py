"""Unit tests for Cookiecutter post-generation hook helpers."""

from __future__ import annotations

from pathlib import Path
from types import ModuleType

import pytest

# SECTION: PRAGMAS ========================================================== #

# pylint: disable=import-outside-toplevel,protected-access,unused-argument

# SECTION: CONSTANTS ======================================================== #


OPTION_DEFAULTS = {
    'include_issue_templates': True,
    'include_pull_request_template': True,
    'include_release_docs': True,
    'include_branch_protection_docs': True,
    'include_maintainer_runbooks': True,
    'include_references': True,
    'include_agents_md': True,
    'include_funding': True,
}


# SECTION: INTERNAL FUNCTIONS =============================================== #


def _create_generated_tree(
    project_root: Path,
) -> None:
    """Create the generated paths managed by the post-generation cleanup hook."""
    for directory in ['.gitlab', '.bitbucket', '.azuredevops']:
        _touch(project_root / directory / 'file.txt')

    for relative_path in [
        '.github/ISSUE_TEMPLATE/bug_report.yml',
        '.github/pull_request_template.md',
        '.github/BRANCH-PROTECTION.md',
        '.github/MAINTAINER-RUNBOOKS.md',
        '.github/FUNDING.yml',
        '.github/RELEASE-NOTES-TEMPLATE.md',
        'RELEASE-POLICY.md',
        'RELEASE-CHECKLIST.md',
        'REFERENCES.md',
        'AGENTS.md',
    ]:
        _touch(project_root / relative_path)


def _mkdir(
    path: Path,
) -> None:
    """Create a directory and its parent directories."""
    path.mkdir(parents=True, exist_ok=True)


def _touch(
    path: Path,
) -> None:
    """Create a file and its parent directories."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('content', encoding='utf-8')


# SECTION: TESTS ============================================================ #


class TestAsBool:
    """Unit test suite for :func:`_as_bool`."""

    @pytest.mark.parametrize(
        ('value', 'expected'),
        [
            ('yes', True),
            ('Y', True),
            (' true ', True),
            ('1', True),
            ('no', False),
            ('false', False),
            ('0', False),
            ('', False),
        ],
    )
    def test_converts_string_values(
        self,
        post_gen_project_module: ModuleType,
        value: str,
        expected: bool,
    ) -> None:
        """Test that :func:`_as_bool` converts supported string values."""
        assert post_gen_project_module._as_bool(value) is expected


class TestRemoveEmptyDirectory:
    """Unit test suite for :func:`_remove_empty_directory`."""

    @pytest.mark.parametrize(
        ('target_name', 'is_populated', 'expected_exists'),
        [
            ('empty', False, False),
            ('non-empty', True, True),
        ],
    )
    def test_handles_directories(
        self,
        post_gen_project_module: ModuleType,
        tmp_path: Path,
        target_name: str,
        is_populated: bool,
        expected_exists: bool,
    ) -> None:
        """Test that :func:`_remove_empty_directory` handles directories."""
        target = tmp_path / target_name
        _mkdir(target)
        if is_populated:
            _touch(target / 'nested.txt')

        post_gen_project_module._remove_empty_directory(target)

        assert target.exists() is expected_exists

    @pytest.mark.parametrize(
        'target_name',
        [
            'file.txt',
            'missing',
        ],
    )
    def test_ignores_files_and_missing_paths(
        self,
        post_gen_project_module: ModuleType,
        tmp_path: Path,
        target_name: str,
    ) -> None:
        """Test that :func:`_remove_empty_directory` ignores unsupported targets."""
        target = tmp_path / target_name
        if target.suffix:
            _touch(target)

        post_gen_project_module._remove_empty_directory(target)

        assert target.exists() is bool(target.suffix)


class TestRemovePath:
    """Unit test suite for :func:`_remove_path`."""

    @pytest.mark.parametrize(
        ('target_name', 'is_directory'),
        [
            ('target.txt', False),
            ('target', True),
            ('missing', None),
        ],
    )
    def test_removes_existing_paths_and_ignores_missing_paths(
        self,
        post_gen_project_module: ModuleType,
        tmp_path: Path,
        target_name: str,
        is_directory: bool | None,
    ) -> None:
        """Test that :func:`_remove_path` removes files and directory trees."""
        target = tmp_path / target_name
        if is_directory is True:
            _touch(target / 'nested.txt')
        elif is_directory is False:
            _touch(target)

        post_gen_project_module._remove_path(target)

        assert not target.exists()


class TestCleanupGeneratedProject:
    """Unit test suite for :func:`_cleanup_generated_project`."""

    @pytest.mark.parametrize(
        ('git_service', 'expected_paths', 'missing_paths'),
        [
            (
                'GitHub',
                ['.github/pull_request_template.md'],
                ['.gitlab', '.bitbucket', '.azuredevops'],
            ),
            (
                'GitLab',
                ['.gitlab'],
                ['.github', '.bitbucket', '.azuredevops'],
            ),
            (
                'Bitbucket',
                ['.bitbucket'],
                ['.github', '.gitlab', '.azuredevops'],
            ),
            (
                'Azure DevOps',
                ['.azuredevops'],
                ['.github', '.gitlab', '.bitbucket'],
            ),
        ],
    )
    def test_removes_non_selected_host_directories(
        self,
        post_gen_project_module: ModuleType,
        tmp_path: Path,
        git_service: str,
        expected_paths: list[str],
        missing_paths: list[str],
    ) -> None:
        """Test that cleanup preserves only the selected Git hosting service."""
        _create_generated_tree(tmp_path)

        post_gen_project_module._cleanup_generated_project(
            tmp_path,
            git_service,
            OPTION_DEFAULTS,
        )

        for expected_path in expected_paths:
            assert (tmp_path / expected_path).exists()
        for missing_path in missing_paths:
            assert not (tmp_path / missing_path).exists()

    @pytest.mark.parametrize(
        ('disabled_option', 'missing_paths'),
        [
            (
                'include_issue_templates',
                ['.github/ISSUE_TEMPLATE'],
            ),
            (
                'include_pull_request_template',
                ['.github/pull_request_template.md'],
            ),
            (
                'include_release_docs',
                [
                    'RELEASE-POLICY.md',
                    'RELEASE-CHECKLIST.md',
                    '.github/RELEASE-NOTES-TEMPLATE.md',
                ],
            ),
            (
                'include_branch_protection_docs',
                ['.github/BRANCH-PROTECTION.md'],
            ),
            (
                'include_maintainer_runbooks',
                ['.github/MAINTAINER-RUNBOOKS.md'],
            ),
            (
                'include_references',
                ['REFERENCES.md'],
            ),
            (
                'include_agents_md',
                ['AGENTS.md'],
            ),
            (
                'include_funding',
                ['.github/FUNDING.yml'],
            ),
        ],
    )
    def test_removes_disabled_optional_paths(
        self,
        post_gen_project_module: ModuleType,
        tmp_path: Path,
        disabled_option: str,
        missing_paths: list[str],
    ) -> None:
        """Test that cleanup removes files for disabled template options."""
        _create_generated_tree(tmp_path)
        options = OPTION_DEFAULTS | {disabled_option: False}

        post_gen_project_module._cleanup_generated_project(
            tmp_path,
            'GitHub',
            options,
        )

        for missing_path in missing_paths:
            assert not (tmp_path / missing_path).exists()

    def test_removes_empty_github_directory(
        self,
        post_gen_project_module: ModuleType,
        tmp_path: Path,
    ) -> None:
        """Test that cleanup removes an empty GitHub directory."""
        _mkdir(tmp_path / '.github')

        post_gen_project_module._cleanup_generated_project(
            tmp_path,
            'GitHub',
            OPTION_DEFAULTS,
        )

        assert not (tmp_path / '.github').exists()
