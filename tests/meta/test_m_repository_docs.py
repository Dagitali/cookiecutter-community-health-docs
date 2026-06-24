"""
:mod:`tests.meta.test_m_repository_docs` module.

Meta tests for repository documentation guardrails.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

# SECTION: PRAGMAS ========================================================== #

# pylint: disable=import-outside-toplevel,protected-access,unused-argument

# SECTION: CONSTANTS ======================================================== #


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_ROOT = PROJECT_ROOT / '{{cookiecutter.project_slug}}'
WORKFLOWS_ROOT = PROJECT_ROOT / '.github' / 'workflows'


# SECTION: INTERNAL FUNCTIONS =============================================== #


def _local_markdown_links(
    markdown: str,
) -> list[str]:
    """Return local Markdown link targets from a Markdown document."""
    links = []

    inline_targets = re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)', markdown)
    reference_targets = re.findall(r'(?m)^\[[^\]]+\]:\s+(\S+)', markdown)

    for target in inline_targets + reference_targets:
        if target.startswith(
            ('http://', 'https://', 'mailto:', '#'),
        ) or target.startswith('<http'):
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


def _readme_maintainer_doc_entry(
    link_target: str,
) -> str:
    """Return the README maintainer-doc bullet for a link target."""
    readme = (PROJECT_ROOT / 'README.md').read_text(encoding='utf-8')
    section = readme.split('### Maintainer Docs', maxsplit=1)[1].split(
        '## License',
        maxsplit=1,
    )[0]
    pattern = rf'(?ms)^- \[[^\]]+\]\({re.escape(link_target)}\):.*?(?=^- |\Z)'
    match = re.search(pattern, section)
    assert match is not None
    return match.group(0)


def _supported_git_services() -> list[str]:
    """Return public Git service options from cookiecutter.json."""
    config = json.loads(
        (PROJECT_ROOT / 'cookiecutter.json').read_text(encoding='utf-8'),
    )
    return config['git_service']


def _repository_markdown_files() -> list[Path]:
    """Return root repository Markdown files outside the Cookiecutter template."""
    return sorted(PROJECT_ROOT.glob('*.md')) + sorted(
        (PROJECT_ROOT / '.github').glob('*.md'),
    )


def _workflow_map_file_paths() -> list[Path]:
    """Return workflow file paths documented in CI-CD-WORKFLOWS.md."""
    workflow_map = (PROJECT_ROOT / 'CI-CD-WORKFLOWS.md').read_text(
        encoding='utf-8',
    )
    return [
        PROJECT_ROOT / workflow_path
        for workflow_path in re.findall(
            r'Workflow file: `([^`]+)`',
            workflow_map,
        )
    ]


def _workflow_map_overview_names() -> list[str]:
    """Return workflow filenames documented in the workflow overview."""
    workflow_map = (PROJECT_ROOT / 'CI-CD-WORKFLOWS.md').read_text(
        encoding='utf-8',
    )
    section = workflow_map.split('## Workflow Overview', maxsplit=1)[1].split(
        '## PR Gates',
        maxsplit=1,
    )[0]
    return re.findall(r'`([^`]+\.yml)`', section)


# SECTION: TESTS ============================================================ #


class TestCiCdWorkflowMap:
    """Meta test suite for CI/CD workflow map accuracy."""

    def test_readme_cicd_workflow_map_entry_names_all_workflows(self) -> None:
        """Test that README summarizes every workflow covered by the CI/CD map."""
        readme_entry = _readme_maintainer_doc_entry('CI-CD-WORKFLOWS.md')

        for workflow_name in _workflow_map_overview_names():
            assert f'`{workflow_name}`' in readme_entry

    def test_workflow_map_lists_all_github_actions_workflows(self) -> None:
        """Test that the CI/CD map covers every GitHub Actions workflow file."""
        actual_workflows = sorted(WORKFLOWS_ROOT.glob('*.yml'))
        documented_workflows = sorted(_workflow_map_file_paths())

        assert documented_workflows == actual_workflows

    def test_workflow_overview_lists_all_github_actions_workflow_names(self) -> None:
        """Test that the CI/CD overview names every workflow file."""
        actual_names = sorted(path.name for path in WORKFLOWS_ROOT.glob('*.yml'))
        documented_names = sorted(_workflow_map_overview_names())

        assert documented_names == actual_names


class TestReadmeGeneratedFileInventory:
    """Meta test suite for README generated-file inventory."""

    def test_readme_generated_paths_exist_in_template_source(self) -> None:
        """Test that README generated-file entries exist in the template."""
        for generated_path in _readme_generated_paths():
            assert (TEMPLATE_ROOT / generated_path).exists(), (
                f'README.md documents missing generated file {generated_path}'
            )


class TestReferences:
    """Meta test suite for reference documentation coverage."""

    def test_references_platforms_cover_supported_git_services(self) -> None:
        """Test that REFERENCES includes every supported Git hosting service."""
        references = (PROJECT_ROOT / 'REFERENCES.md').read_text(encoding='utf-8')

        for git_service in _supported_git_services():
            heading = f'### {git_service}'
            assert heading in references


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
