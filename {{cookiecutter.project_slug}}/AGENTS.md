# AGENTS

- [General](#general)
  - [Repository Conventions](#repository-conventions)
- [Markup Languages](#markup-languages)
  - [Markdown](#markdown)
- [Programming Languages](#programming-languages)
  - [Python](#python)
- [Platforms](#platforms)
  - [`git`](#git)
  - [{{ cookiecutter.git_hosting_service }}](#{{ cookiecutter.git_hosting_service.lower().replace(' ', '-') }})
- [Software Engineering](#software-engineering)
  - [Release Readiness](#release-readiness)
  - [Spec-Driven Development](#spec-driven-development)

## General

### Repository Conventions

Follow the repository's existing style before introducing new patterns.

## Markup Languages

### Markdown

- Place a table of contents directly under the H1 heading before the first H2 heading.
- Use ATX headings.
- Prefer concise, policy-oriented prose for community health documents.
- Keep project policy files plain enough to read in source form.

## Programming Languages

### Python

- Organize modules with section comments in this format:

```python
# SECTION: CONSTANTS ======================================================== #
```

- Use focused subsections only when they make the file easier to scan.

## Platforms

### `git`

- Use topic branches for reviewable work.
- Use annotated tags for public releases.
- Avoid force pushes to protected integration branches.

### {{ cookiecutter.git_hosting_service }}

- Keep {{ cookiecutter.__change_request_name }} templates close to
  {{ cookiecutter.git_hosting_service }}'s native convention.
- Treat required checks and branch protections as the authoritative merge gate.
- Keep private operational material outside the public repository.

## Software Engineering

### Release Readiness

- Keep release-affecting changes aligned with [RELEASE-POLICY.md](RELEASE-POLICY.md).
- Update [RELEASE-CHECKLIST.md](RELEASE-CHECKLIST.md) when release execution changes.

### Spec-Driven Development

- Document public contracts before treating behavior as stable.
- Prefer small, reviewable changes with clear validation.
