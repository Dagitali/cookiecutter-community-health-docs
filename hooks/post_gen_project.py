"""
:mod:`post_gen_project` module.

Post-generation cleanup for rendered repository governance projects.
"""

import shutil
from pathlib import Path

# SECTION: CONSTANTS ======================================================== #


PROJECT_ROOT = Path.cwd()


# SECTION: INTERNAL FUNCTIONS =============================================== #


def _as_bool(
    value: str,
) -> bool:
    """Convert a string value to a boolean."""
    return value.strip().lower() in {'yes', 'y', 'true', '1'}


def _remove_path(
    path: Path,
) -> None:
    """Remove a file or directory at the given path."""
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def _remove_empty_directory(
    path: Path,
) -> None:
    """Remove the directory at the given path if it is empty."""
    if path.exists() and path.is_dir() and not any(path.iterdir()):
        path.rmdir()


# SECTION: FUNCTIONS ======================================================== #


def main() -> None:
    """Main entry point for post-generation cleanup."""
    git_service = '{{ cookiecutter.git_service }}'
    include_issue_templates = _as_bool('{{ cookiecutter.include_issue_templates }}')
    include_pull_request_template = _as_bool(
        '{{ cookiecutter.include_pull_request_template }}',
    )
    include_release_docs = _as_bool('{{ cookiecutter.include_release_docs }}')
    include_branch_protection_docs = _as_bool(
        '{{ cookiecutter.include_branch_protection_docs }}',
    )
    include_maintainer_runbooks = _as_bool(
        '{{ cookiecutter.include_maintainer_runbooks }}',
    )
    include_references = _as_bool('{{ cookiecutter.include_references }}')
    include_agents_md = _as_bool('{{ cookiecutter.include_agents_md }}')
    include_funding = _as_bool('{{ cookiecutter.include_funding }}')

    if git_service != 'GitHub':
        include_issue_templates = False
        include_pull_request_template = False

    if git_service != 'GitHub':
        _remove_path(PROJECT_ROOT / '.github')

    if git_service != 'GitLab':
        _remove_path(PROJECT_ROOT / '.gitlab')

    if git_service != 'Bitbucket':
        _remove_path(PROJECT_ROOT / '.bitbucket')

    if git_service != 'Azure DevOps':
        _remove_path(PROJECT_ROOT / '.azuredevops')

    if git_service == 'GitHub' and not include_issue_templates:
        _remove_path(PROJECT_ROOT / '.github' / 'ISSUE_TEMPLATE')

    if git_service == 'GitHub' and not include_pull_request_template:
        _remove_path(PROJECT_ROOT / '.github' / 'pull_request_template.md')

    if not include_release_docs:
        _remove_path(PROJECT_ROOT / 'RELEASE-POLICY.md')
        _remove_path(PROJECT_ROOT / 'RELEASE-CHECKLIST.md')
        if git_service == 'GitHub':
            _remove_path(PROJECT_ROOT / '.github' / 'RELEASE-NOTES-TEMPLATE.md')

    if git_service == 'GitHub' and not include_branch_protection_docs:
        _remove_path(PROJECT_ROOT / '.github' / 'BRANCH-PROTECTION.md')

    if git_service == 'GitHub' and not include_maintainer_runbooks:
        _remove_path(PROJECT_ROOT / '.github' / 'MAINTAINER-RUNBOOKS.md')

    if not include_references:
        _remove_path(PROJECT_ROOT / 'REFERENCES.md')

    if not include_agents_md:
        _remove_path(PROJECT_ROOT / 'AGENTS.md')

    if git_service == 'GitHub' and not include_funding:
        _remove_path(PROJECT_ROOT / '.github' / 'FUNDING.yml')

    github_dir = PROJECT_ROOT / '.github'
    _remove_empty_directory(github_dir)


# SECTION: MAIN ENTRY POINT ================================================= #


if __name__ == '__main__':
    main()
