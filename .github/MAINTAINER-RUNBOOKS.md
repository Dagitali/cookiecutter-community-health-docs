# Maintainer Runbooks

Maintainer-facing runbooks for working with protected branches, GitHub pull requests (PRs), and
tag-triggered releases.

- [Operating Model](#operating-model)
- [Feature Branch Runbook](#feature-branch-runbook)
- [Release Branch Runbook](#release-branch-runbook)
- [Hotfix Branch Runbook](#hotfix-branch-runbook)
- [Sync Main Back To Develop](#sync-main-back-to-develop)
- [Tagging](#tagging)
- [Solo-Maintainer Notes](#solo-maintainer-notes)
- [Keep Private Elsewhere](#keep-private-elsewhere)

## Operating Model

cookiecutter-repo-governance uses GitFlow-style branch names together with GitHub-protected
`develop` and `main` branches.

The important consequence is:

- Working happens on `feature/*`, `release/*`, and `hotfix/*`
- Authoritative integration happens through PRs
- PR targets should follow the GitFlow branch map enforced by the PR-gates workflow
- `develop` and `main` should be treated as GitHub-managed integration branches, not as branches
  that are finished locally and pushed afterward

Local `git flow feature finish` and `git flow release finish` may still be useful for personal
experimentation in a local clone, but they should not be treated as the final source of truth for
protected branches.

Prefer `git flow ... start` for creating working branches. Do not treat `git flow ... finish` as a
cleanup step for this protected-branch workflow, because it performs local merges into integration
branches. After the authoritative GitHub PR merge, prefer manual local branch cleanup instead.

This file stays at the policy and high-level workflow layer. Sensitive operator details should live
outside the public repository.

## Feature Branch Runbook

Use for normal development work.

1. Create a local feature branch from your local `develop` branch.
   Example: `git flow feature start my-change`
2. Commit your changes locally on that feature branch.
3. Push the feature branch to the remote GitHub repository.
   Example: `git push -u origin feature/my-change`
4. Open a PR from the remote `feature/*` branch into the remote `develop` branch. The PR-gates
   workflow rejects `feature/*` pull requests that target `main`.
5. Let `.github/workflows/pr.yml` and `.github/workflows/ci.yml` run on GitHub. For feature work,
   the heavier `ci.yml` checks run because the PR targets `develop`.
6. Merge the PR in GitHub once both workflows report the required checks for your target branch.
7. Delete the remote feature branch on GitHub after merge if it is no longer needed, and clean up
   your local branch when convenient.
   Preferred local cleanup: delete the local feature branch manually after updating your local
   branch state.

## Release Branch Runbook

Use for release stabilization and promotion.

1. Create a local `release/<version>` branch from your local `develop` branch.
   Example: `git flow release start 1.2.6`
2. Commit release-targeted stabilization changes locally on that release branch.
3. Push the release branch to the remote GitHub repository.
   Example: `git push -u origin release/1.2.6`
4. Open a PR from the remote `release/*` branch into the remote `main` branch. The PR-gates workflow
   reserves `main` for `release/*` and `hotfix/*` pull requests.
5. Merge the PR on GitHub after both `.github/workflows/pr.yml` and `.github/workflows/ci.yml`
   report the required checks for `main`.
6. Fetch the newly merged remote `main` commit into your local repository.
   Example: `git fetch origin main`
7. Create an annotated release tag locally that points at the fetched `main` commit.
   Example: `git tag -a v1.2.6 origin/main -m "Release v1.2.6"`
8. Push the annotated release tag to GitHub.
   Example: `git push origin v1.2.6`
9. Sync the resulting remote `main` state back into `develop` explicitly. See [Sync Main Back To
   Develop](#sync-main-back-to-develop).

## Hotfix Branch Runbook

Use for urgent production fixes that must land on `main` first.

1. Create a local `hotfix/<version>` branch from your local `main` branch.
   Example: `git flow hotfix start 1.2.6`
2. Apply and validate the fix locally on that hotfix branch.
3. Push the hotfix branch to the remote GitHub repository.
   Example: `git push -u origin hotfix/1.2.6`
4. Open a PR from the remote `hotfix/*` branch into the remote `main` branch. The PR-gates workflow
   reserves `main` for `release/*` and `hotfix/*` pull requests.
5. Merge the PR in GitHub after both `.github/workflows/pr.yml` and `.github/workflows/ci.yml`
   report the required checks for `main`.
6. Fetch the newly merged remote `main` commit into your local repository.
   Example: `git fetch origin main`
7. Create an annotated hotfix tag locally that points at the fetched `main` commit.
   Example: `git tag -a v1.2.6 origin/main -m "Release v1.2.6"`
8. Push the annotated hotfix tag to GitHub.
   Example: `git push origin v1.2.6`
9. Sync the resulting remote `main` state back into `develop` explicitly.
   See [Sync Main Back To Develop](#sync-main-back-to-develop).

## Sync Main Back To Develop

After a release or hotfix lands on `main`, update `develop` deliberately rather than assuming both
protected branches are already aligned.

Preferred sequence:

1. Fetch the latest remote `main` and `develop` state into your local repository.
   Example: `git fetch origin main develop`
2. Create a temporary local sync branch from your updated local `develop` branch.
   Example: `git switch develop && git pull --ff-only origin develop && git switch -c sync/main-into-develop`
3. Merge the updated remote `main` state into the local sync branch or directly into the local
   `develop` branch.
   Example: `git merge --no-ff origin/main`
4. Push the sync branch, and open a pull request into the remote `develop` branch.
   Example: `git push -u origin sync/main-into-develop`
5. Merge on GitHub once the required checks for `develop` pass, including `.github/workflows/ci.yml`
   if that heavier pre-merge workflow is part of your `develop` branch-protection rule.

## Tagging

- Use annotated tags for public releases.
- Tag the authoritative merged `main` commit.
- Use `vMAJOR.MINOR.PATCH` tag names.
- Keep the tag annotation concise, verb-oriented, and release-focused.

## Solo-Maintainer Notes

It is normal for a solo maintainer to use PRs for both feature and release branches once protected
branches are enabled.

The PR still provides value even without another human reviewer:

- Required checks run on the proposed branch change before the protected branch moves
- GitHub becomes the authoritative merge surface for protected branches
- Release and branch history stay aligned with the repository protection model

For a solo-maintainer repository, it is reasonable to keep the policy lightweight:

- One required approval on `develop`, or an intentionally documented exception path
- Stricter review on `main` only if that is useful for release discipline
- Narrow admin bypass only when necessary and documented in `.github/BRANCH-PROTECTION.md`

## Keep Private Elsewhere

Sensitive operator documentation should live outside the public repository.

Examples that should live in a truly private location include:

- Secrets and credential recovery procedures
- Emergency branch-protection bypass procedures
- Security-incident response details
- Account recovery or succession notes
