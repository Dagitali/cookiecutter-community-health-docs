from pathlib import Path
import shutil


PROJECT_ROOT = Path.cwd()


def as_bool(value: str) -> bool:
    return value.strip().lower() in {"yes", "y", "true", "1"}


def remove_path(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def main() -> None:
    git_hosting_service = "{{ cookiecutter.git_hosting_service }}"
    include_issue_templates = as_bool("{{ cookiecutter.include_issue_templates }}")
    include_pull_request_template = as_bool("{{ cookiecutter.include_pull_request_template }}")

    if git_hosting_service != "GitHub":
        include_issue_templates = False
        include_pull_request_template = False

    if not include_issue_templates:
        remove_path(PROJECT_ROOT / ".github" / "ISSUE_TEMPLATE")

    if not include_pull_request_template:
        remove_path(PROJECT_ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md")

    github_dir = PROJECT_ROOT / ".github"
    if github_dir.exists() and not any(github_dir.iterdir()):
        github_dir.rmdir()


if __name__ == "__main__":
    main()
