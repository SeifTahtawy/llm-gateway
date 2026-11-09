# Keep provider HTTP and TestClient transport separate

**Status** — Adopted in dependency configuration. Outbound provider calls are planned.

## Context and decision

Keep HTTPX as a runtime dependency for future asynchronous provider requests. Keep HTTPX2 in the development group to support the Starlette TestClient used by the FastAPI endpoint test. See [the dependency groups](../pyproject.toml) and [the TestClient fixture](../tests/test_health.py). The handover documents the reason for carrying both packages.

## Why it fits this gateway

The test transport follows the framework's TestClient dependency, while the eventual provider transport can be selected for the gateway's own needs. The dependency split keeps HTTPX2 outside the intended runtime dependency set and lets the two uses evolve independently.

## Trade-offs and alternatives

- **Use one client library for both roles.** This can reduce dependency and upgrade overhead when a single library meets the framework's test requirements and the provider adapters' runtime needs. Sharing a name or similar APIs is insufficient to establish compatibility.
- **Use a different test harness.** An async ASGI harness can help when tests need to share async resources with the application, and a live server can cover real network behavior. Either approach needs its own lifecycle setup and adds complexity to the current endpoint test.

Two similarly named packages can cause confusion during imports and upgrades. Review their roles against the lockfile and tests when updating the framework or changing the provider transport.
