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


def _branch_protection_check_names() -> list[str]:
    """Return check names documented in branch protection guidance."""
    branch_protection = (
        PROJECT_ROOT / '.github' / 'BRANCH-PROTECTION.md'
    ).read_text(encoding='utf-8')
    return re.findall(r'`([^`]+)`', branch_protection)


def _ci_workflow_check_names() -> list[str]:
    """Return emitted check names from the CI workflow."""
    ci_workflow = (WORKFLOWS_ROOT / 'ci.yml').read_text(encoding='utf-8')
    check_names = []

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

    return check_names


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


def _pr_workflow_check_names() -> list[str]:
    """Return emitted check names from the PR Gates workflow."""
    pr_workflow = (WORKFLOWS_ROOT / 'pr.yml').read_text(encoding='utf-8')
    pr_gate_match = re.search(
        r'pr-target-guard:.*?^\s+name:\s+([^\n]+)$',
        pr_workflow,
        flags=re.MULTILINE | re.DOTALL,
    )
    assert pr_gate_match is not None
    return [pr_gate_match.group(1).strip()]


def _public_cookiecutter_input_names() -> list[str]:
    """Return public Cookiecutter input names from cookiecutter.json."""
    config = json.loads(
        (PROJECT_ROOT / 'cookiecutter.json').read_text(encoding='utf-8'),
    )
    return [input_name for input_name in config if not input_name.startswith('__')]


def _readme_generated_paths() -> list[str]:
    """Return generated file paths documented in README.md."""
    readme = (PROJECT_ROOT / 'README.md').read_text(encoding='utf-8')
    section = readme.split('## Generated files', maxsplit=1)[1].split(
        '## Inputs',
        maxsplit=1,
    )[0]
    return re.findall(r'`([^`]+)`', section)


def _readme_input_names() -> list[str]:
    """Return Cookiecutter input names documented in README.md."""
    readme = (PROJECT_ROOT / 'README.md').read_text(encoding='utf-8')
    section = readme.split('## Inputs', maxsplit=1)[1].split(
        '## Usage',
        maxsplit=1,
    )[0]
    return re.findall(r'^- `([^`]+)`:', section, flags=re.MULTILINE)


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


def _template_file_paths() -> list[str]:
    """Return file paths in the Cookiecutter template source."""
    return sorted(
        path.relative_to(TEMPLATE_ROOT).as_posix()
        for path in TEMPLATE_ROOT.rglob('*')
        if path.is_file()
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


class TestBranchProtectionDocs:
    """Meta test suite for branch-protection documentation accuracy."""

    def test_branch_protection_documents_ci_check_names(self) -> None:
        """Test that branch protection documents current CI check names."""
        documented_names = _branch_protection_check_names()

        for check_name in _ci_workflow_check_names():
            assert check_name in documented_names

    def test_branch_protection_documents_pr_gate_check_names(self) -> None:
        """Test that branch protection documents current PR gate checks."""
        documented_names = _branch_protection_check_names()

        for check_name in _pr_workflow_check_names():
            assert check_name in documented_names


class TestReadmeGeneratedFileInventory:
    """Meta test suite for README generated-file inventory."""

    def test_readme_generated_paths_cover_template_source_files(self) -> None:
        """Test that README documents every template source file."""
        assert sorted(_readme_generated_paths()) == _template_file_paths()

    def test_readme_generated_paths_exist_in_template_source(self) -> None:
        """Test that README generated-file entries exist in the template."""
        for generated_path in _readme_generated_paths():
            assert (TEMPLATE_ROOT / generated_path).exists(), (
                f'README.md documents missing generated file {generated_path}'
            )


class TestReadmeInputs:
    """Meta test suite for README Cookiecutter input documentation."""

    def test_readme_inputs_cover_public_cookiecutter_inputs(self) -> None:
        """Test that README documents every public Cookiecutter input."""
        assert sorted(_readme_input_names()) == sorted(
            _public_cookiecutter_input_names(),
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
