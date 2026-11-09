# Lock dependencies with uv

**Status** — Adopted in the application foundation and enforced during CI setup.

## Context and decision

Use uv to manage the environment and commit `uv.lock`. Keep runtime and development dependencies in separate groups. Target Python 3.12 in local development and CI, and install development tools with `uv sync --locked --dev`. The declared Python requirement is `>=3.12`, while the CI workflow exercises 3.12. See [project configuration](../pyproject.toml), [the Python version](../.python-version), and [CI setup](../.github/workflows/ci.yml).

## Why it fits this gateway

A committed lockfile makes dependency changes visible in review and gives local runs and CI the same resolution for equivalent environments. The locked sync catches a missing or stale lockfile during setup, before the quality checks run. Explicit Python setup avoids depending on the runner's default interpreter version.

## Trade-offs and alternatives

- **Install from dependency ranges on each run.** This can help a library test compatibility with freshly released dependencies. It also means the same gateway commit can see different transitive versions on different days.
- **Use pip with compiled requirements.** This suits teams whose build or deployment tooling already consumes requirements files. They still need a way to regenerate the resolved pins, keep the inputs in sync, and manage the interpreter and virtual environment.
- **Test a Python version matrix.** This pays off when a project promises support for several versions. A single 3.12 job keeps the feedback loop small and leaves other versions allowed by the metadata outside CI coverage.
