"""
:mod:`tests.meta.test_m_repository_docs` module.

Meta tests for repository documentation guardrails.
"""

from __future__ import annotations

import re
from pathlib import Path

# SECTION: PRAGMAS ========================================================== #

# pylint: disable=import-outside-toplevel,protected-access,unused-argument

# SECTION: CONSTANTS ======================================================== #


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_ROOT = PROJECT_ROOT / '{{cookiecutter.project_slug}}'


# SECTION: INTERNAL FUNCTIONS =============================================== #


def _local_markdown_links(
    markdown: str,
) -> list[str]:
    """Return local Markdown link targets from a Markdown document."""
    links = []

    inline_targets = re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)', markdown)
    reference_targets = re.findall(r'(?m)^\[[^\]]+\]:\s+(\S+)', markdown)

    for target in inline_targets + reference_targets:
        if (
            target.startswith(('http://', 'https://', 'mailto:', '#'))
            or target.startswith('<http')
        ):
            continue
        links.append(target.strip('<>'))

    return links


def _readme_generated_paths() -> list[str]:
    """Return generated file paths documented in README.md."""
    readme = (PROJECT_ROOT / 'README.md').read_text(encoding='utf-8')
    section = readme.split('## Generated files', maxsplit=1)[1].split(
        '## Inputs',
        maxsplit=1,
    )[0]
    return re.findall(r'`([^`]+)`', section)


def _repository_markdown_files() -> list[Path]:
    """Return root repository Markdown files outside the Cookiecutter template."""
    return sorted(PROJECT_ROOT.glob('*.md')) + sorted(
        (PROJECT_ROOT / '.github').glob('*.md'),
    )


# SECTION: TESTS ============================================================ #


class TestRootMarkdown:
    """Meta test suite for root Markdown quality."""

    def test_root_markdown_has_no_unresolved_template_syntax(self) -> None:
        """Test that root Markdown contains no unresolved Jinja syntax."""
        unresolved_patterns = ('{{', '{%', '{#')

        for markdown_file in _repository_markdown_files():
            markdown = markdown_file.read_text(encoding='utf-8')
            assert not any(pattern in markdown for pattern in unresolved_patterns), (
                f'{markdown_file.relative_to(PROJECT_ROOT)} contains unresolved '
                'Cookiecutter or Jinja syntax'
            )

    def test_root_markdown_links_point_to_existing_files(self) -> None:
        """Test that root local Markdown links resolve to repository files."""
        for markdown_file in _repository_markdown_files():
            markdown = markdown_file.read_text(encoding='utf-8')
            for link in _local_markdown_links(markdown):
                target = link.split('#', maxsplit=1)[0]
                if not target:
                    continue
                assert (markdown_file.parent / target).exists(), (
                    f'{markdown_file.relative_to(PROJECT_ROOT)} links to '
                    f'missing target {link}'
                )


class TestReadmeGeneratedFileInventory:
    """Meta test suite for README generated-file inventory."""

    def test_readme_generated_paths_exist_in_template_source(self) -> None:
        """Test that README generated-file entries exist in the template."""
        for generated_path in _readme_generated_paths():
            assert (TEMPLATE_ROOT / generated_path).exists(), (
                f'README.md documents missing generated file {generated_path}'
            )
