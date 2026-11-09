# Use a dependency-free health endpoint

**Status** — Adopted in the application foundation.

## Context and decision

`GET /api/health` returns HTTP 200 and `{"status": "healthy"}` when the application handles the request. Its handler performs no network calls or dependency checks. See [the handler](../app/api/health.py) and [its endpoint test](../tests/test_health.py).

## Why it fits this gateway

The current gateway has no provider integrations, and a simple request gives a cheap signal that the API can serve traffic at that route. When providers are added, keeping this check local also lets operators distinguish an unresponsive gateway from an upstream outage.

## Trade-offs and alternatives

- **Add a separate readiness check.** This helps when traffic should wait for required initialization or a dependency that every request needs. A readiness check needs an explicit policy about which failures make the whole instance unable to serve traffic.
- **Track provider status separately.** Per-provider telemetry or a diagnostic endpoint helps when only some models are affected. Active probes add latency, can consume provider quota, and need timeout and failure policies. A single provider's failure may still leave other routes usable.
