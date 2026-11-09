# Compose the FastAPI app with routers

**Status** — Adopted in the application foundation.

## Context and decision

Keep a single FastAPI application in `app/main.py`. The entry point reads application metadata from settings and registers routers. Each route module defines its own handlers and router metadata. Uvicorn loads the assembled application as `app.main:app`. See [the entry point](../app/main.py) and [health router](../app/api/health.py).

## Why it fits this gateway

There is one application and one route group today. An explicit list of registered routers makes the API easy to trace and gives future route groups a clear home. The single application instance gives both Uvicorn and the endpoint test a common entry point.

## Trade-offs and alternatives

- **Define handlers directly on the app.** This saves a file and an import for a one-route prototype. It becomes harder to see where setup ends and request handling starts as route groups grow.
- **Use an application factory.** A factory makes sense when callers need independently configured app instances, distinct lifespans, or different dependency graphs in tests. Constructing the app at import time is simpler for one configuration per process, but the import also fixes the app instance and its metadata for that process.
