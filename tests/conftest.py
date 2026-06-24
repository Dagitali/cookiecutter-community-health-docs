"""
:mod:`tests.conftest` module.

Shared fixtures for pytest-based tests.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from tests.pytest_helpers import PROJECT_ROOT
from tests.pytest_helpers import load_cookiecutter_config

# SECTION: FIXTURES ========================================================= #


@pytest.fixture(name='project_root')
def project_root_fixture() -> Path:
    """Return the repository root path."""
    return PROJECT_ROOT


@pytest.fixture(name='cookiecutter_config')
def cookiecutter_config_fixture() -> dict[str, Any]:
    """Load the template's Cookiecutter configuration."""
    return load_cookiecutter_config()
