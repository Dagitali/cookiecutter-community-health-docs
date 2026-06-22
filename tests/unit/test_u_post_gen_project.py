"""Unit tests for Cookiecutter post-generation hook helpers."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from types import ModuleType

import pytest

# SECTION: PRAGMAS ========================================================== #

# pylint: disable=import-outside-toplevel,protected-access,unused-argument

# SECTION: TESTS ============================================================ #


class TestAsBool:
    """Unit test suite for :func:`_as_bool`."""

    @pytest.mark.parametrize(
        'value',
        [
            'yes',
            'Y',
            ' true ',
            '1',
        ],
    )
    def test_recognizes_truthy_values(
        self,
        post_gen_project_module: ModuleType,
        value: str,
    ) -> None:
        """Test that :func:`_as_bool` recognizes various truthy string values."""
        assert post_gen_project_module._as_bool(value)

    @pytest.mark.parametrize(
        'value',
        [
            'no',
            'false',
            '0',
            '',
        ],
    )
    def test_rejects_falsey_values(
        self,
        post_gen_project_module: ModuleType,
        value: str,
    ) -> None:
        """Test that :func:`_as_bool` rejects various falsey string values."""
        assert not post_gen_project_module._as_bool(value)


class TestRemoveEmptyDirectory:
    """Unit test suite for :func:`_remove_empty_directory`."""

    @pytest.mark.parametrize(
        ('target_name', 'populate_target', 'expected_exists'),
        [
            ('empty', False, False),
            ('non-empty', True, True),
        ],
    )
    def test_handles_directories(
        self,
        post_gen_project_module: ModuleType,
        path_factory: Callable[..., Path],
        target_name: str,
        populate_target: bool,
        expected_exists: bool,
    ) -> None:
        """Test that :func:`_remove_empty_directory` handles directories."""
        target = path_factory(
            target_name,
            directory=True,
            populated=populate_target,
        )

        post_gen_project_module._remove_empty_directory(target)

        assert target.exists() is expected_exists

    def test_ignores_file(
        self,
        post_gen_project_module: ModuleType,
        path_factory: Callable[..., Path],
    ) -> None:
        """Test that :func:`_remove_empty_directory` ignores a file."""
        target = path_factory('file.txt')

        post_gen_project_module._remove_empty_directory(target)

        assert target.exists()


class TestRemovePath:
    """Unit test suite for :func:`_remove_path`."""

    def test_removes_file(
        self,
        post_gen_project_module: ModuleType,
        path_factory: Callable[..., Path],
    ) -> None:
        """Test that :func:`_remove_path` removes a file."""
        target = path_factory('target.txt')

        post_gen_project_module._remove_path(target)

        assert not target.exists()

    def test_removes_directory_tree(
        self,
        post_gen_project_module: ModuleType,
        path_factory: Callable[..., Path],
    ) -> None:
        """Test that :func:`_remove_path` removes a directory tree."""
        target = path_factory('target', directory=True, populated=True)

        post_gen_project_module._remove_path(target)

        assert not target.exists()

    def test_ignores_missing_path(
        self,
        post_gen_project_module: ModuleType,
        tmp_path: Path,
    ) -> None:
        """Test that :func:`_remove_path` ignores a missing path."""
        post_gen_project_module._remove_path(tmp_path / 'missing')
