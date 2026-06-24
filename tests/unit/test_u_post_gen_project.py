"""
:mod:`tests.unit.test_u_post_gen_project` module.

Unit tests for Cookiecutter post-generation hook helpers.
"""

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
    def test_coerces_string_values(
        self,
        post_gen_project_module: ModuleType,
        value: str,
        expected: bool,
    ) -> None:
        """Test that :func:`_as_bool` coerces supported string values."""
        assert post_gen_project_module._as_bool(value) is expected


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

    @pytest.mark.parametrize(
        ('target_name', 'directory', 'populated'),
        [
            ('target.txt', False, False),
            ('target', True, True),
        ],
    )
    def test_removes_existing_path(
        self,
        post_gen_project_module: ModuleType,
        path_factory: Callable[..., Path],
        target_name: str,
        directory: bool,
        populated: bool,
    ) -> None:
        """Test that :func:`_remove_path` removes existing files and trees."""
        target = path_factory(
            target_name,
            directory=directory,
            populated=populated,
        )

        post_gen_project_module._remove_path(target)

        assert not target.exists()

    def test_ignores_missing_path(
        self,
        post_gen_project_module: ModuleType,
        tmp_path: Path,
    ) -> None:
        """Test that :func:`_remove_path` ignores a missing path."""
        post_gen_project_module._remove_path(tmp_path / 'missing')
