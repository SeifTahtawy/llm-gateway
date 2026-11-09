# Keep the full health path in its router

**Status** — Adopted in the application foundation.

## Context and decision

The health router declares `/api/health` in the route decorator. The application includes that router without adding a path prefix. See [the route declaration](../app/api/health.py) and [router registration](../app/main.py).

## Why it fits this gateway

With one endpoint, the complete URL is easy to find alongside its handler. The application entry point only needs to register the router, and the endpoint test can exercise the same path that clients call.

## Trade-offs and alternatives

- **Share a prefix through a parent router or at registration.** This keeps a common prefix such as `/api/v1` in one place and helps when several route groups share versioning or dependencies. Readers must follow the registration to reconstruct the full path.
- **Set a prefix on each feature router.** This keeps a shared segment visible inside the module and avoids repeating it across several related handlers. It adds little value for a module with only one endpoint.

If several gateway routers later repeat a version or API prefix, reconsider where it is applied while preserving URLs that clients already use.
