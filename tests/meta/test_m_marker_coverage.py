"""
:mod:`tests.meta.test_m_marker_coverage` module.

Guardrails for pytest scope-marker coverage.
"""

from __future__ import annotations

import pytest

import tests.conftest as root_conftest
from tests.pytest_helpers import TESTS_ROOT

# SECTION: PRAGMAS ========================================================== #

# pylint: disable=import-outside-toplevel,protected-access,unused-argument

# SECTION: FIXTURES ========================================================= #


@pytest.fixture(name='registered_markers')
def registered_markers_fixture(
    pytestconfig: pytest.Config,
) -> set[str]:
    """Return marker names registered in the active pytest configuration."""
    return {
        marker.split(':', maxsplit=1)[0] for marker in pytestconfig.getini('markers')
    }


# SECTION: TESTS ============================================================ #


def test_root_collection_hook_covers_existing_test_suite_directories() -> None:
    """Test that the root marker hook covers every active test-suite directory."""
    suite_directories = {
        path.name
        for path in TESTS_ROOT.iterdir()
        if path.is_dir()
        if any(path.rglob('test_*.py'))
    }

    assert suite_directories <= root_conftest.DIRECTORY_MARKERS.keys()


@pytest.mark.parametrize(
    'marker_name',
    sorted(root_conftest.DIRECTORY_MARKERS),
    ids=str,
)
def test_root_collection_hook_uses_registered_pytest_markers(
    registered_markers: set[str],
    marker_name: str,
) -> None:
    """Test that root marker-hook entries use registered pytest markers."""
    assert marker_name in registered_markers
