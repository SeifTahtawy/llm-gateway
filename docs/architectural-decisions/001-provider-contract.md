# ADR-001: Provider Contract — Protocol vs. Abstract Base Class

**Status:** Accepted
**Date:** November 12, 2026
**Project:** Multi-Provider LLM Gateway

## 1. Context

The LLM Gateway integrates multiple LLM providers, Each provider has different authentication mechanisms, request formats, response structures, and error-handling requirements.

To prevent provider-specific implementation details from leaking into application logic, the gateway will define a common provider contract.

We must decide whether to represent this contract using:

- **Abstract Base Class (ABC):** Nominal subtyping through explicit inheritance.
- **Protocol:** Structural subtyping based on interface compatibility.

The chosen approach should support provider interchangeability, static type checking, independent implementations, and straightforward testing without introducing unnecessary constraints.

## 2. Decision

**Use Python's `Protocol` to define the common LLM provider contract.**

Provider implementations will satisfy the contract through structural compatibility rather than mandatory inheritance.

MyPy will be used to verify interface compatibility at typed integration points.

The exact methods, parameters, and return types of the provider contract will be defined separately.

## 3. Alternatives Considered

### Option A: Abstract Base Class (ABC)

An ABC defines a common interface that provider implementations explicitly inherit.

**Advantages:**

- Explicit relationship between implementations and the contract.
- Runtime prevention of instantiating subclasses with unimplemented abstract methods.
- Support for shared implementation through inheritance.
- Static type checking through MyPy.

**Disadvantages:**

- Independently developed implementations may require inheritance changes or adapters.
- Introduces an inheritance dependency without a demonstrated need for shared behavior.

### Option B: Protocol

A Protocol defines an interface that implementations can satisfy without explicitly inheriting from it.

**Advantages:**

- Structural compatibility without inheritance coupling.
- Independent provider implementations.
- Compatibility with third-party implementations exposing the expected interface.
- Static type checking through MyPy.
- Straightforward creation of lightweight test doubles.

**Disadvantages:**

- No automatic runtime enforcement of interface conformance.
- Implicit conformance may make the relationship between implementations and the contract less obvious.
- Does not provide shared implementation through implicit conformance.
- Interface changes can require coordinated updates across implementations.

Both approaches support provider interchangeability, static checking, and test doubles.

## 4. Rationale

Protocol was selected for the following reasons:

**1. No shared implementation is currently required.**

The provider contract defines expected behavior rather than reusable implementation. An inheritance hierarchy would therefore provide limited additional value.

**2. Provider implementations should remain independent.**

Integrations may have significantly different internal implementations. Structural typing allows them to satisfy a shared contract without inheriting from a common base class.

**3. Static type checking is already available.**

MyPy is part of the project's development workflow and CI pipeline. Protocol compatibility can be verified where implementations are assigned, returned, or passed through appropriately typed interfaces.

**4. Implementation reuse should remain separate from the contract.**

Shared functionality such as HTTP client management, retry policies, and observability can be implemented through composition or dedicated components when needed.

Protocol provides the required interface compatibility with fewer inheritance constraints.

## 5. Consequences

### Positive

- Application logic can depend on a common provider interface rather than concrete implementations.
- Providers can implement the contract without inheriting from a shared base class.
- Independently developed implementations can satisfy the contract structurally.
- MyPy can detect incompatible interfaces at statically checked integration points.
- Test doubles can implement the required interface without inheriting from production classes.

### Negative / Trade-offs

- Protocols do not automatically enforce interface compatibility at runtime.
- Static type compatibility does not guarantee behavioral correctness.
- Changes to the contract may affect multiple provider implementations and consumers.
- Explicit type annotations and static checks are necessary to obtain reliable compatibility verification.
- Provider construction and selection still require a separate mechanism, such as a registry or factory.

## 6. Scope and Deferred Decisions

This ADR determines **how the provider contract is represented**, not the complete design of the provider interface.

The following decisions remain open:

- Exact provider methods and their signatures.
- Whether streaming and non-streaming operations share one contract.
- Normalized provider errors and exceptions.
- Provider selection, dependency injection, and lifecycle management.
- HTTP client ownership and connection pooling.
- Retry, timeout, and cancellation policies.
- Behavioral contract testing across provider implementations.

These concerns will be addressed independently as their requirements become concrete.

## 7. Reconsideration Criteria

This decision may be revisited if:

- Runtime enforcement of abstract-method implementation becomes an important requirement.
- Multiple providers require substantial shared behavior best expressed through inheritance.
- A controlled provider inheritance hierarchy provides demonstrable benefits.

Adopting Protocol does not prevent introducing an internal ABC for specific implementations if future requirements justify it.

## 8. Summary

**Decision:** Use `Protocol` for the common LLM provider contract.

**Reason:** The gateway requires a consistent interface and independent provider implementations, but does not currently require shared inherited behavior.

**Trade-off:** We accept the lack of automatic runtime interface enforcement in exchange for structural compatibility and reduced inheritance coupling, relying on MyPy and automated tests to verify implementations.
