"""
:mod:`tests.meta.test_m_repository_docs` module.

Meta tests for repository documentation guardrails.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from functools import cache
from pathlib import Path

import pytest

from tests.pytest_helpers import PROJECT_ROOT
from tests.pytest_helpers import SUPPORTED_GIT_SERVICES
from tests.pytest_helpers import UNRESOLVED_TEMPLATE_PATTERNS
from tests.pytest_helpers import load_cookiecutter_config
from tests.pytest_helpers import local_markdown_links

# SECTION: PRAGMAS ========================================================== #

# pylint: disable=import-outside-toplevel,protected-access,unused-argument

# SECTION: CONSTANTS ======================================================== #


TEMPLATE_ROOT = PROJECT_ROOT / '{{cookiecutter.project_slug}}'
WORKFLOWS_ROOT = PROJECT_ROOT / '.github' / 'workflows'


# SECTION: INTERNAL FUNCTIONS =============================================== #


# -- Document Text Helpers -- #


@cache
def _branch_protection_text() -> str:
    """Return branch-protection guidance text."""
    return (PROJECT_ROOT / '.github' / 'BRANCH-PROTECTION.md').read_text(
        encoding='utf-8',
    )


@cache
def _readme_text() -> str:
    """Return repository README text."""
    return (PROJECT_ROOT / 'README.md').read_text(encoding='utf-8')


@cache
def _references_text() -> str:
    """Return repository references text."""
    return (PROJECT_ROOT / 'REFERENCES.md').read_text(encoding='utf-8')


@cache
def _release_checklist_text() -> str:
    """Return release checklist text."""
    return (PROJECT_ROOT / 'RELEASE-CHECKLIST.md').read_text(encoding='utf-8')


@cache
def _template_release_checklist_text() -> str:
    """Return template release-checklist source text."""
    return (TEMPLATE_ROOT / 'RELEASE-CHECKLIST.md').read_text(encoding='utf-8')


@cache
def _workflow_map_text() -> str:
    """Return CI/CD workflow-map text."""
    return (PROJECT_ROOT / 'CI-CD-WORKFLOWS.md').read_text(encoding='utf-8')


# -- Markdown Helpers -- #


def _documented_workflow_paths(markdown: str) -> tuple[Path, ...]:
    """Return GitHub Actions workflow paths documented in Markdown text."""
    return tuple(
        PROJECT_ROOT / workflow_path
        for workflow_path in re.findall(
            r'`?(\.github/workflows/[A-Za-z0-9_.-]+\.yml)`?',
            markdown,
        )
    )


def _markdown_h2_anchors(markdown: str) -> tuple[str, ...]:
    """Return second-level heading anchors from Markdown text."""
    return tuple(
        _markdown_heading_anchor(match.group(1))
        for line in _markdown_lines_outside_fenced_blocks(markdown)
        if (match := re.match(r'^##\s+(.+?)\s*#*$', line))
    )


def _markdown_has_h1(markdown: str) -> bool:
    """Return whether Markdown text has a first-level heading."""
    return any(
        line.startswith('# ')
        for line in _markdown_lines_outside_fenced_blocks(markdown)
    )


def _markdown_heading_anchor(heading_text: str) -> str:
    """Return the GitHub-style heading anchor for Markdown heading text."""
    normalized = re.sub(r'[`*_]', '', heading_text).casefold()
    normalized = re.sub(r'[^\w\s-]', '', normalized)
    return re.sub(r'\s+', '-', normalized.strip())


def _markdown_lines_outside_fenced_blocks(markdown: str) -> tuple[str, ...]:
    """Return Markdown lines outside fenced code blocks."""
    in_fenced_block = False
    lines: list[str] = []
    for line in markdown.splitlines():
        if line.startswith('```'):
            in_fenced_block = not in_fenced_block
            continue
        if not in_fenced_block:
            lines.append(line)
    return tuple(lines)


def _markdown_toc_anchors_before_first_h2(markdown: str) -> tuple[str, ...]:
    """Return local TOC anchors documented before the first second-level heading."""
    lines_before_first_h2: list[str] = []
    for line in _markdown_lines_outside_fenced_blocks(markdown):
        if line.startswith('## '):
            break
        lines_before_first_h2.append(line)
    return tuple(
        match.group(1)
        for line in lines_before_first_h2
        if (match := re.match(r'\s*- \[[^\]]+\]\(#([^)]+)\)', line))
    )


# -- Repository Inventory Helpers -- #


def _repository_markdown_files() -> tuple[Path, ...]:
    """Return root repository Markdown files outside the Cookiecutter template."""
    return (
        *sorted(PROJECT_ROOT.glob('*.md')),
        *sorted((PROJECT_ROOT / '.github').glob('*.md')),
    )


def _template_release_checklist_doc_paths() -> tuple[str, ...]:
    """Return documentation paths referenced by the template release checklist."""
    markdown_links = tuple(
        link.split('#', maxsplit=1)[0]
        for link in local_markdown_links(_template_release_checklist_text())
        if link.split('#', maxsplit=1)[0]
    )
    backtick_paths = tuple(
        path
        for path in re.findall(
            r'`([^`]+\.(?:md|yml|yaml))`',
            _template_release_checklist_text(),
        )
        if '{{' not in path
    )
    return tuple(sorted({*markdown_links, *backtick_paths}))


# -- README Parsers -- #


@cache
def _readme_generated_paths() -> tuple[str, ...]:
    """Return generated file paths documented in README.md."""
    section = (
        _readme_text()
        .split('## Generated files', maxsplit=1)[1]
        .split(
            '## Inputs',
            maxsplit=1,
        )[0]
    )
    return tuple(re.findall(r'`([^`]+)`', section))


@cache
def _readme_input_names() -> tuple[str, ...]:
    """Return Cookiecutter input names documented in README.md."""
    section = (
        _readme_text()
        .split('## Inputs', maxsplit=1)[1]
        .split(
            '## Usage',
            maxsplit=1,
        )[0]
    )
    return tuple(re.findall(r'^- `([^`]+)`:', section, flags=re.MULTILINE))


@cache
def _readme_maintainer_doc_entry(
    link_target: str,
) -> str:
    """Return the README maintainer-doc bullet for a link target."""
    section = (
        _readme_text()
        .split('### Maintainer Docs', maxsplit=1)[1]
        .split(
            '## License',
            maxsplit=1,
        )[0]
    )
    pattern = rf'(?ms)^- \[[^\]]+\]\({re.escape(link_target)}\):.*?(?=^- |\Z)'
    match = re.search(pattern, section)
    assert match is not None
    return match.group(0)


# -- Workflow and Check Parsers -- #


def _branch_protection_check_names() -> tuple[str, ...]:
    """Return check names documented in branch protection guidance."""
    return tuple(re.findall(r'`([^`]+)`', _branch_protection_text()))


@cache
def _ci_workflow_check_names() -> tuple[str, ...]:
    """Return emitted check names from the CI workflow."""
    ci_workflow = (WORKFLOWS_ROOT / 'ci.yml').read_text(encoding='utf-8')
    check_names: list[str] = []

    precommit_match = re.search(
        r'precommit:.*?^\s+name:\s+([^\n]+)$',
        ci_workflow,
        flags=re.MULTILINE | re.DOTALL,
    )
    assert precommit_match is not None
    check_names.append(precommit_match.group(1).strip())

    test_match = re.search(
        r'test:.*?^\s+name:\s+([^\n]+)$',
        ci_workflow,
        flags=re.MULTILINE | re.DOTALL,
    )
    assert test_match is not None
    test_name_template = test_match.group(1).strip()
    matrix_section = ci_workflow.split('matrix:', maxsplit=1)[1].split(
        'permissions:',
        maxsplit=1,
    )[0]
    python_versions = re.findall(
        r"^\s+- '([^']+)'$",
        matrix_section,
        flags=re.MULTILINE,
    )
    check_names.extend(
        test_name_template.replace('${{ matrix.python-version }}', python_version)
        for python_version in python_versions
    )

    return tuple(check_names)


@cache
def _pr_workflow_check_names() -> tuple[str, ...]:
    """Return emitted check names from the PR Gates workflow."""
    pr_workflow = (WORKFLOWS_ROOT / 'pr.yml').read_text(encoding='utf-8')
    check_names: list[str] = []
    job_names = re.findall(
        r'^\s{2}[a-z][a-z0-9-]*:\n(?:.*?\n)*?^\s{4}name:\s+([^\n]+)$',
        pr_workflow,
        flags=re.MULTILINE,
    )
    matrix_section = pr_workflow.split('matrix:', maxsplit=1)[1].split(
        'permissions:',
        maxsplit=1,
    )[0]
    python_versions = re.findall(
        r"'([^']+)'",
        matrix_section,
    )

    for job_name in job_names:
        if '${{ matrix.python-version }}' in job_name:
            check_names.extend(
                job_name.replace('${{ matrix.python-version }}', python_version)
                for python_version in python_versions
            )
            continue
        check_names.append(job_name.strip())

    return tuple(check_names)


@cache
def _workflow_map_file_paths() -> tuple[Path, ...]:
    """Return workflow file paths documented in CI-CD-WORKFLOWS.md."""
    return tuple(
        PROJECT_ROOT / workflow_path
        for workflow_path in re.findall(
            r'Workflow file: `([^`]+)`',
            _workflow_map_text(),
        )
    )


def _workflow_map_entries() -> tuple[tuple[Path, str], ...]:
    """Return workflow file/name pairs documented in CI-CD-WORKFLOWS.md."""
    return tuple(
        (PROJECT_ROOT / path, name)
        for path, name in re.findall(
            r'Workflow file: `([^`]+)`\s+Workflow name: `([^`]+)`',
            _workflow_map_text(),
        )
    )


@cache
def _workflow_map_overview_names() -> tuple[str, ...]:
    """Return workflow filenames documented in the workflow overview."""
    section = (
        _workflow_map_text()
        .split('## Workflow Overview', maxsplit=1)[1]
        .split(
            '## PR Gates',
            maxsplit=1,
        )[0]
    )
    return tuple(re.findall(r'`([^`]+\.yml)`', section))


@cache
def _workflow_map_required_check_names() -> tuple[str, ...]:
    """Return check names documented in the CI/CD workflow map."""
    section = _workflow_map_text().split('## Required Checks', maxsplit=1)[1]
    return tuple(re.findall(r'`([^`]+)`', section))


def _workflow_names() -> dict[Path, str]:
    """Return workflow display names keyed by workflow file path."""
    workflow_names: dict[Path, str] = {}
    for path in WORKFLOWS_ROOT.glob('*.yml'):
        workflow_text = path.read_text(encoding='utf-8')
        match = re.search(r'^name:\s+(.+)$', workflow_text, flags=re.MULTILINE)
        assert match is not None
        workflow_names[path] = match.group(1).strip()
    return workflow_names


# SECTION: TESTS ============================================================ #


class TestBranchProtectionDocs:
    """Meta test suite for branch-protection documentation accuracy."""

    @pytest.mark.parametrize(
        'check_name_source',
        [
            _ci_workflow_check_names,
            _pr_workflow_check_names,
        ],
        ids=lambda source: source.__name__.removeprefix('_').removesuffix(
            '_check_names',
        ),
    )
    def test_branch_protection_documents_check_names(
        self,
        check_name_source: Callable[[], tuple[str, ...]],
    ) -> None:
        """Test that branch protection documents current workflow check names."""
        documented_names = _branch_protection_check_names()

        for check_name in check_name_source():
            assert check_name in documented_names


class TestCiCdWorkflowMap:
    """Meta test suite for CI/CD workflow map accuracy."""

    def test_readme_cicd_workflow_map_entry_names_all_workflows(self) -> None:
        """Test that README summarizes every workflow covered by the CI/CD map."""
        readme_entry = _readme_maintainer_doc_entry('CI-CD-WORKFLOWS.md')

        for workflow_name in _workflow_map_overview_names():
            assert f'`{workflow_name}`' in readme_entry

    def test_workflow_map_documents_required_and_advisory_check_names(self) -> None:
        """Test that the CI/CD map documents current PR and CI check names."""
        documented_names = _workflow_map_required_check_names()
        expected_names = _pr_workflow_check_names() + _ci_workflow_check_names()

        for check_name in expected_names:
            assert check_name in documented_names

    def test_workflow_map_lists_all_github_actions_workflows(self) -> None:
        """Test that the CI/CD map covers every GitHub Actions workflow file."""
        actual_workflows = sorted(WORKFLOWS_ROOT.glob('*.yml'))
        documented_workflows = sorted(_workflow_map_file_paths())

        assert documented_workflows == actual_workflows

    def test_workflow_map_names_match_workflow_files(self) -> None:
        """Test that the CI/CD map names each workflow by its YAML name."""
        workflow_names = _workflow_names()

        for workflow_path, documented_name in _workflow_map_entries():
            assert workflow_names[workflow_path] == documented_name

    def test_workflow_overview_lists_all_github_actions_workflow_names(self) -> None:
        """Test that the CI/CD overview names every workflow file."""
        actual_names = sorted(path.name for path in WORKFLOWS_ROOT.glob('*.yml'))
        documented_names = sorted(_workflow_map_overview_names())

        assert documented_names == actual_names


class TestReadmeGeneratedFileInventory:
    """Meta test suite for README generated-file inventory."""

    def test_readme_generated_paths_cover_release_checklist_doc_references(
        self,
    ) -> None:
        """Test that README inventory covers docs referenced by release checklist."""
        documented_paths = set(_readme_generated_paths())
        expected_paths = {
            'RELEASE-CHECKLIST.md',
            *_template_release_checklist_doc_paths(),
        }

        assert expected_paths <= documented_paths

    def test_readme_generated_paths_cover_template_source_files(self) -> None:
        """Test that README documents every template source file."""
        template_paths = sorted(
            path.relative_to(TEMPLATE_ROOT).as_posix()
            for path in TEMPLATE_ROOT.rglob('*')
            if path.is_file()
        )

        assert sorted(_readme_generated_paths()) == template_paths

    @pytest.mark.parametrize('generated_path', _readme_generated_paths())
    def test_readme_generated_paths_exist_in_template_source(
        self,
        generated_path: str,
    ) -> None:
        """Test that README generated-file entries exist in the template."""
        assert (TEMPLATE_ROOT / generated_path).exists(), (
            f'README.md documents missing generated file {generated_path}'
        )


class TestReadmeInputs:
    """Meta test suite for README Cookiecutter input documentation."""

    def test_readme_inputs_cover_public_cookiecutter_inputs(self) -> None:
        """Test that README documents every public Cookiecutter input."""
        public_inputs = [
            input_name
            for input_name in load_cookiecutter_config()
            if not input_name.startswith('__')
        ]

        assert sorted(_readme_input_names()) == sorted(public_inputs)


class TestReferences:
    """Meta test suite for reference documentation coverage."""

    @pytest.mark.parametrize('git_service', SUPPORTED_GIT_SERVICES)
    def test_references_platforms_cover_supported_git_services(
        self,
        git_service: str,
    ) -> None:
        """Test that REFERENCES includes every supported Git hosting service."""
        heading = f'### {git_service}'

        assert heading in _references_text()


class TestReleaseChecklistTemplateDocs:
    """Meta test suite for generated release-checklist source references."""

    @pytest.mark.parametrize(
        'referenced_path',
        _template_release_checklist_doc_paths(),
        ids=str,
    )
    def test_release_checklist_doc_references_exist_in_template_source(
        self,
        referenced_path: str,
    ) -> None:
        """Test that release-checklist doc references exist in template source."""
        assert (TEMPLATE_ROOT / referenced_path).exists()


class TestRootMarkdown:
    """Meta test suite for root Markdown quality."""

    @pytest.mark.parametrize(
        'markdown_file',
        _repository_markdown_files(),
        ids=lambda path: path.relative_to(PROJECT_ROOT).as_posix(),
    )
    def test_root_markdown_toc_covers_second_level_headings(
        self,
        markdown_file: Path,
    ) -> None:
        """Test that root Markdown TOCs cover second-level headings."""
        markdown = markdown_file.read_text(encoding='utf-8')
        if not _markdown_has_h1(markdown):
            return

        h2_anchors = _markdown_h2_anchors(markdown)
        if not h2_anchors:
            return

        toc_anchors = _markdown_toc_anchors_before_first_h2(markdown)

        assert set(h2_anchors) <= set(toc_anchors), (
            f'{markdown_file.relative_to(PROJECT_ROOT)} has H2 headings missing '
            'from the opening table of contents'
        )

    @pytest.mark.parametrize(
        'markdown_file',
        _repository_markdown_files(),
        ids=lambda path: path.relative_to(PROJECT_ROOT).as_posix(),
    )
    def test_root_markdown_has_no_unresolved_template_syntax(
        self,
        markdown_file: Path,
    ) -> None:
        """Test that root Markdown contains no unresolved Jinja syntax."""
        markdown = markdown_file.read_text(encoding='utf-8')

        has_unresolved_syntax = any(
            pattern in markdown for pattern in UNRESOLVED_TEMPLATE_PATTERNS
        )

        assert not has_unresolved_syntax, (
            f'{markdown_file.relative_to(PROJECT_ROOT)} contains unresolved '
            'Cookiecutter or Jinja syntax'
        )

    @pytest.mark.parametrize(
        'markdown_file',
        _repository_markdown_files(),
        ids=lambda path: path.relative_to(PROJECT_ROOT).as_posix(),
    )
    def test_root_markdown_links_point_to_existing_files(
        self,
        markdown_file: Path,
    ) -> None:
        """Test that root local Markdown links resolve to repository files."""
        markdown = markdown_file.read_text(encoding='utf-8')

        for link in local_markdown_links(markdown):
            target = link.split('#', maxsplit=1)[0]
            if not target:
                continue
            assert (markdown_file.parent / target).exists(), (
                f'{markdown_file.relative_to(PROJECT_ROOT)} links to '
                f'missing target {link}'
            )


class TestWorkflowReferences:
    """Meta test suite for workflow-reference documentation accuracy."""

    @pytest.mark.parametrize(
        ('document_name', 'markdown'),
        [
            ('RELEASE-CHECKLIST.md', _release_checklist_text()),
            ('CI-CD-WORKFLOWS.md', _workflow_map_text()),
            ('.github/BRANCH-PROTECTION.md', _branch_protection_text()),
        ],
        ids=lambda case: case if isinstance(case, str) else None,
    )
    def test_documented_workflow_paths_exist(
        self,
        document_name: str,
        markdown: str,
    ) -> None:
        """Test that documented GitHub Actions workflow paths exist."""
        documented_paths = _documented_workflow_paths(markdown)
        assert documented_paths, f'{document_name} documents no workflow paths'

        for workflow_path in documented_paths:
            assert workflow_path.exists(), (
                f'{document_name} documents missing workflow '
                f'{workflow_path.relative_to(PROJECT_ROOT)}'
            )
