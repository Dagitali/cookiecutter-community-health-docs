"""
:mod:`tests.integration.conftest` module.

Shared fixtures and helpers for pytest-based integration tests.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest
from cookiecutter.main import cookiecutter

# SECTION: MARKERS ========================================================== #


# Directory-level marker for integration tests.
pytestmark = pytest.mark.integration


# SECTION: CONSTANTS ======================================================== #


PROJECT_ROOT = Path(__file__).resolve().parents[2]


# SECTION: FIXTURES ========================================================= #


@pytest.fixture(name='cookiecutter_config')
def cookiecutter_config_fixture() -> dict[str, Any]:
    """Load the template's Cookiecutter configuration."""
    return json.loads(
        (PROJECT_ROOT / 'cookiecutter.json').read_text(encoding='utf-8'),
    )


@pytest.fixture(name='render_project')
def render_project_fixture(
    tmp_path: Path,
) -> Callable[..., Path]:
    """Create a callable that renders the template into a temp directory."""

    def _render_project(**extra_context: str) -> Path:
        config_file = tmp_path / 'cookiecutter-config.yaml'
        config_file.write_text(
            '\n'.join(
                [
                    f"cookiecutters_dir: {tmp_path / 'cookiecutters'}",
                    f"replay_dir: {tmp_path / 'replay'}",
                ],
            ),
            encoding='utf-8',
        )

        context = {
            'project_name': 'Example Project',
            'project_slug': 'example-project',
            'owner': 'Example Org',
            'repo_namespace': 'example',
            'support_email': 'support@example.com',
            'security_email': 'security@example.com',
            'conduct_email': 'conduct@example.com',
        }
        context.update(extra_context)

        return Path(
            cookiecutter(
                str(PROJECT_ROOT),
                no_input=True,
                output_dir=str(tmp_path),
                extra_context=context,
                config_file=str(config_file),
            ),
        )

    return _render_project
