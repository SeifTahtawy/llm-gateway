# Run quality checks in one CI job

**Status** — Adopted and exercised during the CI milestone.

## Context and decision

Use one `quality_checks` job on pushes to `main` and pull requests targeting `main`. After dependency setup it runs Pytest, Ruff linting, Ruff formatting in check mode, and MyPy in sequence. See [the workflow](../.github/workflows/ci.yml).

## Why it fits this gateway

The checks share one setup and present one result for branch protection. The current project is small enough for sequential execution. Checking formatting without writing files makes CI report discrepancies and leaves formatting changes visible in the contributor's diff.

## Trade-offs and alternatives

- **Run separate parallel jobs.** This helps when checks take longer, need different environments, or should all report results despite one failing. It adds setup overhead and requires managing multiple required checks or an aggregate result.
- **Continue checking after a step fails.** This provides more feedback per run. Any implementation must preserve the failing result as a merge gate. The current sequence stops after a failure, so a contributor may need another run to see later failures.
- **Apply formatting automatically.** A bot can help a high-volume team if it has an explicit way to deliver fixes back to branches. Formatting files on the runner without returning the changes would leave the contributor's branch untouched.

The handover records successful runs after the original command-step key was corrected from `runs` to `run`.
