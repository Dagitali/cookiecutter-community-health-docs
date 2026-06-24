"""
:mod:`tests.integration.conftest` module.

Shared fixtures and helpers for pytest-based integration tests.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import pytest
from cookiecutter.main import cookiecutter  # type: ignore[import-untyped]

# SECTION: TYPE ALIASES ===================================================== #


type RenderProject = Callable[..., Path]


# SECTION: FIXTURES ========================================================= #


@pytest.fixture(name='release_config')
def release_config_fixture(
    project_root: Path,
) -> str:
    """Return the GitHub release-note configuration text."""
    return (project_root / '.github' / 'release.yml').read_text(encoding='utf-8')


@pytest.fixture(name='render_project')
def render_project_fixture(
    project_root: Path,
    tmp_path: Path,
) -> RenderProject:
    """Create a callable that renders the template into a temp directory."""

    def _render_project(**extra_context: str) -> Path:
        config_file = tmp_path / 'cookiecutter-config.yaml'
        config_file.write_text(
            '\n'.join(
                [
                    f'cookiecutters_dir: {tmp_path / "cookiecutters"}',
                    f'replay_dir: {tmp_path / "replay"}',
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
                str(project_root),
                no_input=True,
                output_dir=str(tmp_path),
                extra_context=context,
                config_file=str(config_file),
            ),
        )

    return _render_project
