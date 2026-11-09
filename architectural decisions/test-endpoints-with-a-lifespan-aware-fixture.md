# Test endpoints with a lifespan-aware fixture

**Status** — Adopted in the application foundation.

## Context and decision

Use a function-scoped Pytest fixture that yields a FastAPI TestClient from inside a context manager. The health test makes a request through the actual app and asserts both HTTP status and JSON body. See [the fixture and test](../tests/test_health.py).

## Why it fits this gateway

The test covers router registration and response handling through the application boundary. The context manager runs ASGI startup and shutdown around the test and closes the client afterward. It gives future endpoint tests a predictable lifecycle if resources are later managed through application lifespan.

## Trade-offs and alternatives

- **Call a handler directly.** Unit tests are useful for isolated logic and precise error cases. Routing, serialization, and the HTTP response still need endpoint coverage.
- **Reuse a fixture across tests.** A wider fixture scope can save setup time when startup is expensive. It increases the risk that state left behind by one test affects another. The current fixture creates a fresh client per test around the same imported app, so application-global state may still need explicit isolation.
- **Exercise a running server.** A live-server test is useful for behaviors that depend on sockets or deployment, such as how a client observes a streaming disconnect. It costs more to run and coordinate than the current in-process check.
