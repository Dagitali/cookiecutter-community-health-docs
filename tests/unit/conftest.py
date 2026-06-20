"""
:mod:`tests.unit.conftest` module.

Shared fixtures and helpers for pytest-based unit tests.
"""

from __future__ import annotations

import importlib.util
from collections.abc import Callable
from pathlib import Path
from types import ModuleType

import pytest

# SECTION: MARKERS ========================================================== #


# Directory-level marker for unit tests.
pytestmark = pytest.mark.unit


# SECTION: CONSTANTS ======================================================== #


PROJECT_ROOT = Path(__file__).resolve().parents[2]
POST_GEN_PROJECT_PATH = PROJECT_ROOT / 'hooks' / 'post_gen_project.py'


# SECTION: FIXTURES ========================================================= #


@pytest.fixture(name='path_factory')
def path_factory_fixture(
    tmp_path: Path,
) -> Callable[[str, bool, bool], Path]:
    """Create test files or directories under ``tmp_path``."""

    def _make_path(
        name: str,
        *,
        directory: bool = False,
        populated: bool = False,
    ) -> Path:
        target = tmp_path / name
        if directory:
            target.mkdir()
            if populated:
                (target / 'nested.txt').write_text('content', encoding='utf-8')
        else:
            target.write_text('content', encoding='utf-8')
        return target

    return _make_path


@pytest.fixture(name='post_gen_project_module')
def post_gen_project_module_fixture() -> ModuleType:
    """Load the Cookiecutter post-generation hook module from its file path."""
    spec = importlib.util.spec_from_file_location(
        'post_gen_project',
        POST_GEN_PROJECT_PATH,
    )
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
