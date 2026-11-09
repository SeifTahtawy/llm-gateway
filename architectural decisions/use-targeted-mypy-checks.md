# Use targeted MyPy checks

**Status** — Adopted in project configuration.

## Context and decision

Run MyPy on `app` and `tests` with Python 3.12 as the target. Require annotations on function definitions, check untyped function bodies, and enable warnings for returns inferred as `Any` from functions declared to return a concrete type and for unused configuration sections. Full strict mode is deferred. See [MyPy settings](../pyproject.toml) and [the CI invocation](../.github/workflows/ci.yml).

## Why it fits this gateway

Typing both application and test code builds a consistent baseline ahead of the provider contract. The selected rules put immediate emphasis on signatures and type information flowing across boundaries, while leaving room to raise the bar as adapters expose new failure modes.

## Trade-offs and alternatives

- **Enable full strict mode from the start.** This can make sense when contributors already use strict typing and the dependencies have suitable type information. It catches more issues but can require extra wrappers or annotations when upstream libraries are weakly typed.
- **Apply stricter checks to selected modules.** This helps when typed boundaries, such as provider contracts, benefit from stronger guarantees while integration code still needs gradual adoption. The extra configuration needs clear ownership and a reason for each difference.
