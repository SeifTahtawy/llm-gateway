# Require pull requests and passing CI on main

**Status** — Adopted as recorded in the November 9, 2026 handover.

## Context and decision

Require pull requests into `main` and require the `quality_checks` job to pass. An approving review is optional under the handover's final policy. The user disabled the approval requirement after it blocked a CI-passing test PR. The verification PR was left unmerged.

## Why it fits this gateway

The pull request creates a place to inspect the diff and the CI result. The required check protects the main branch from the known classes of issues covered by tests, lint, formatting, and typing. For a solo portfolio project, keeping human approval optional avoids requiring a second person to merge while allowing the user to ask for review.

## Trade-offs and alternatives

- **Require an approving review.** This helps teams with available reviewers and changes that need independent judgment, such as authentication and key handling. It can block a solo maintainer even when all automated checks pass.
- **Allow direct pushes with checks only after the push.** This lowers friction for disposable prototypes. A bad change reaches the branch before the check can report it.

Branch protection is configured in GitHub outside the repository. If the job name changes, update the required check setting as well. See [the workflow job](../.github/workflows/ci.yml).
