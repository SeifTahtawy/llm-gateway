# Centralize settings with Pydantic Settings

**Status** — Adopted in the application foundation.

## Context and decision

Define application metadata and debug mode as typed fields on `AppSettings`, with defaults and environment-variable overrides. Instantiate `settings` in the module and use it when building the app. See [the settings model](../app/core/config.py) and [its consumer](../app/main.py).

## Why it fits this gateway

One model makes configuration discoverable and gives local defaults and environment overrides the same validation path. For example, Pydantic Settings parses the debug environment value into a Boolean. One instance is sufficient for the current application and its stable process-level settings.

## Trade-offs and alternatives

- **Read environment variables directly.** This is reasonable for a tiny script with one or two string values. As settings grow, defaults, parsing, and error handling can get scattered across consumers.
- **Construct settings explicitly and pass them into an application factory.** This is useful for multiple app configurations in one process or tests that need distinct settings. It adds wiring. With the current module-level instance, the settings reflect the environment at import time, and invalid configuration can fail the import.
