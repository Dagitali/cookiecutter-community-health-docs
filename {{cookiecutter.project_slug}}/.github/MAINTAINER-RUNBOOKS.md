# Maintainer Runbooks

Maintainer-facing runbooks for working with protected branches, {{ cookiecutter.__change_request_name }}s, and
tagged releases.

- [Operating Model](#operating-model)
- [Feature Work](#feature-work)
- [Release Work](#release-work)
- [Hotfix Work](#hotfix-work)
{% if cookiecutter.branch_model == "GitFlow" -%}
- [Sync Default Branch Back To Development](#sync-default-branch-back-to-development)
{% endif -%}
- [Tagging](#tagging)
- [Solo-Maintainer Notes](#solo-maintainer-notes)
- [Keep Private Elsewhere](#keep-private-elsewhere)

## Operating Model

{{ cookiecutter.project_name }} uses {{ cookiecutter.branch_model }} with protected integration branches.

{% if cookiecutter.branch_model == "GitFlow" -%}
The important consequence is:

- Working happens on `feature/*`, `release/*`, and `hotfix/*`
- Authoritative integration happens through {{ cookiecutter.__change_request_name }}s
- Feature branches target `{{ cookiecutter.development_branch }}`
- Release and hotfix branches target `{{ cookiecutter.default_branch }}`
- `{{ cookiecutter.development_branch }}` and `{{ cookiecutter.default_branch }}` should be treated
  as hosted integration branches, not as branches that are finished locally and pushed afterward

Prefer `git flow ... start` for creating working branches. Do not treat `git flow ... finish` as a
cleanup step for this protected-branch workflow, because it performs local merges into integration
branches. After the authoritative {{ cookiecutter.__change_request_name }} merge, prefer manual
local branch cleanup instead.
{% else -%}
The important consequence is:

- Working happens on topic branches
- Authoritative integration happens through {{ cookiecutter.__change_request_name }}s
- Topic branches target `{{ cookiecutter.default_branch }}`
- `{{ cookiecutter.default_branch }}` should be treated as the hosted integration branch
{% endif %}

This file stays at the policy and high-level workflow layer. Sensitive operator details should live
outside the public repository.

## Feature Work

Use for normal development work.

{% if cookiecutter.branch_model == "GitFlow" -%}
1. Create a local feature branch from `{{ cookiecutter.development_branch }}`.
   Example: `git flow feature start my-change`
2. Commit focused changes locally on that feature branch.
3. Push the feature branch to the remote repository.
   Example: `git push -u origin feature/my-change`
4. Open a {{ cookiecutter.__change_request_name }} from the remote `feature/*` branch into
   `{{ cookiecutter.development_branch }}`.
5. Let required checks run on the hosted repository.
6. Merge the {{ cookiecutter.__change_request_name }} once required checks and review requirements
   pass.
7. Delete the remote feature branch after merge if it is no longer needed, and clean up your local
   branch when convenient.
{% else -%}
1. Create a local topic branch from `{{ cookiecutter.default_branch }}`.
2. Commit focused changes locally on that topic branch.
3. Push the topic branch to the remote repository.
4. Open a {{ cookiecutter.__change_request_name }} into `{{ cookiecutter.default_branch }}`.
5. Let required checks run on the hosted repository.
6. Merge the {{ cookiecutter.__change_request_name }} once required checks and review requirements
   pass.
7. Delete the remote topic branch after merge if it is no longer needed, and clean up your local
   branch when convenient.
{% endif %}

## Release Work

Use for release stabilization and promotion.

{% if cookiecutter.branch_model == "GitFlow" -%}
1. Create a local `release/<version>` branch from `{{ cookiecutter.development_branch }}`.
   Example: `git flow release start 1.2.0`
2. Commit release-targeted stabilization changes locally on that release branch.
3. Push the release branch to the remote repository.
   Example: `git push -u origin release/1.2.0`
4. Open a {{ cookiecutter.__change_request_name }} from the remote `release/*` branch into
   `{{ cookiecutter.default_branch }}`.
5. Merge the {{ cookiecutter.__change_request_name }} after required checks and review requirements
   pass.
6. Fetch the newly merged remote `{{ cookiecutter.default_branch }}` commit into your local
   repository.
7. Create an annotated release tag that points at the fetched default-branch commit.
8. Push the annotated release tag to the remote repository.
9. Sync the resulting remote `{{ cookiecutter.default_branch }}` state back into
   `{{ cookiecutter.development_branch }}` explicitly.
{% else -%}
1. Confirm the release scope and version.
2. Commit release-targeted stabilization changes on a topic branch.
3. Open a {{ cookiecutter.__change_request_name }} into `{{ cookiecutter.default_branch }}`.
4. Merge the {{ cookiecutter.__change_request_name }} after required checks and review requirements
   pass.
5. Create an annotated release tag that points at the fetched default-branch commit.
6. Push the annotated release tag to the remote repository.
{% endif %}

## Hotfix Work

Use for urgent fixes that must land on the released default branch first.

{% if cookiecutter.branch_model == "GitFlow" -%}
1. Create a local `hotfix/<version>` branch from `{{ cookiecutter.default_branch }}`.
   Example: `git flow hotfix start 1.2.1`
2. Apply and validate the fix locally on that hotfix branch.
3. Push the hotfix branch to the remote repository.
   Example: `git push -u origin hotfix/1.2.1`
4. Open a {{ cookiecutter.__change_request_name }} from the remote `hotfix/*` branch into
   `{{ cookiecutter.default_branch }}`.
5. Merge the {{ cookiecutter.__change_request_name }} after required checks and review requirements
   pass.
6. Create and push an annotated hotfix tag from the authoritative merged default-branch commit.
7. Sync the resulting remote `{{ cookiecutter.default_branch }}` state back into
   `{{ cookiecutter.development_branch }}` explicitly.
{% else -%}
1. Branch from the released `{{ cookiecutter.default_branch }}` state.
2. Apply the narrow fix and validation.
3. Open a {{ cookiecutter.__change_request_name }} into `{{ cookiecutter.default_branch }}`.
4. Merge the {{ cookiecutter.__change_request_name }} after required checks and review requirements
   pass.
5. Tag and publish the hotfix release when needed.
{% endif %}

{% if cookiecutter.branch_model == "GitFlow" -%}
## Sync Default Branch Back To Development

After a release or hotfix lands on `{{ cookiecutter.default_branch }}`, update
`{{ cookiecutter.development_branch }}` deliberately rather than assuming both protected branches
are already aligned.

Preferred sequence:

1. Fetch the latest remote `{{ cookiecutter.default_branch }}` and `{{ cookiecutter.development_branch }}`
   state.
2. Create a temporary sync branch from updated `{{ cookiecutter.development_branch }}`.
3. Merge the updated remote `{{ cookiecutter.default_branch }}` state into the sync branch.
4. Push the sync branch and open a {{ cookiecutter.__change_request_name }} into
   `{{ cookiecutter.development_branch }}`.
5. Merge on the hosted service once required checks pass.

{% endif -%}
## Tagging

- Use annotated tags for public releases.
- Tag the authoritative merged `{{ cookiecutter.default_branch }}` commit.
- Use `vMAJOR.MINOR.PATCH` tag names.
- Keep the tag annotation concise, verb-oriented, and release-focused.

## Solo-Maintainer Notes

It is normal for a solo maintainer to use {{ cookiecutter.__change_request_name }}s for both feature
and release branches once protected branches are enabled.

The {{ cookiecutter.__change_request_name }} still provides value even without another human
reviewer:

- Required checks run on the proposed branch change before the protected branch moves
- The hosted Git service becomes the authoritative merge surface for protected branches
- Release and branch history stay aligned with the repository protection model

For a solo-maintainer repository, it is reasonable to keep the policy lightweight:

- One required approval on the development branch, or an intentionally documented exception path
- Stricter review on the default branch only if that is useful for release discipline
- Narrow admin bypass only when necessary and documented in `.github/BRANCH-PROTECTION.md`

## Keep Private Elsewhere

Sensitive operator documentation should live outside the public repository.

Examples that should live in a truly private location include:

- Secrets and credential recovery procedures
- Emergency branch-protection bypass procedures
- Security-incident response details
- Account recovery or succession notes
