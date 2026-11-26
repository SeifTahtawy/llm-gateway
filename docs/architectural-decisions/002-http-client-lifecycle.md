# ADR 002 — HTTP Client Ownership and Lifecycle Management

**Status:** Accepted  
**Date:** 2026-11-26

## 1. Context

The LLM Gateway communicates with multiple external LLM providers through HTTP APIs. It must efficiently handle concurrent generation requests while maintaining predictable resource management, separation of concerns, testability, and extensibility.

HTTP clients manage network connections and other resources that require explicit lifecycle management. Repeated connection establishment introduces avoidable latency and resource consumption through TCP and TLS handshakes.

An architectural decision is required regarding:

- HTTP client ownership and lifecycle.
- Connection pooling and resource reuse.
- Dependency injection.
- Resource isolation between providers.
- Concurrent reuse of provider instances.

The decision must preserve the provider-independent contract established in ADR 001.

## 2. Alternatives Considered

### 2.1. Request-Scoped HTTP Clients

Each generation request creates and closes its own HTTP client.

**Advantages:**

- Simple and explicit resource lifecycle.
- Automatic cleanup through context managers.
- No application-level HTTP client lifecycle management.

**Disadvantages:**

- No connection reuse across generation requests.
- Repeated connection establishment overhead.
- Increased resource consumption and connection churn under load.

**Conclusion:** Rejected because it prevents effective connection pooling across requests and conflicts with the gateway's performance objectives.

### 2.2. Provider-Owned Persistent HTTP Clients

Each provider constructs, owns, and manages a persistent HTTP client.

**Advantages:**

- Supports connection pooling and asynchronous concurrency.
- Encapsulates provider-specific infrastructure dependencies.
- Allows providers to independently select and configure their networking implementations.
- Produces more self-contained provider components.

**Disadvantages:**

- Distributes resource lifecycle management across providers.
- Introduces resource initialization and cleanup into provider responsibilities.
- The application must still coordinate provider shutdown.
- Dependency substitution during testing requires additional design.
- May require a separate provider lifecycle contract or management mechanism.

**Conclusion:** A valid architecture, particularly for independently distributed provider libraries. However, centralized resource management is more appropriate for the gateway's current requirements.

### 2.3. Application-Owned Persistent HTTP Clients

The application constructs, configures, and manages persistent HTTP clients. Providers receive their required clients through constructor dependency injection.

**Advantages:**

- Supports connection pooling and asynchronous concurrency.
- Centralizes resource ownership and lifecycle management.
- Makes provider dependencies explicit.
- Separates infrastructure lifecycle management from provider-specific behavior.
- Simplifies dependency substitution during testing.
- Preserves the existing generation-only provider contract.
- Integrates naturally with FastAPI's lifespan mechanism.

**Disadvantages:**

- Application dependency construction must know the concrete infrastructure requirements of each provider.
- Reduces encapsulation at the application composition boundary.
- Application initialization becomes more complex as dependencies increase.

**Conclusion:** Selected because centralized resource management, explicit dependencies, and testability outweigh the reduced encapsulation.

Provider-owned and application-owned persistent clients offer equivalent networking performance under identical configuration. The selection is primarily an architectural and resource ownership decision.

## 3. Connection Pool Allocation

Two connection pool allocation strategies were considered independently of client ownership.

### 3.1. Single Shared HTTP Client

All HTTP-based providers share one persistent HTTP client.

**Advantages:**

- Fewer resources to initialize and manage.
- Simpler application configuration.
- More flexible utilization of shared connection capacity.

**Disadvantages:**

- Providers compete for the same overall connection pool capacity.
- Slow requests to one provider may delay requests to another.
- Reduced isolation of provider-specific networking configuration and authentication.

### 3.2. Dedicated HTTP Client per Provider

Each HTTP-based provider receives its own persistent HTTP client and connection pool.

**Advantages:**

- Independent connection pool limits.
- Reduced resource contention between providers.
- Independent timeout, transport, and authentication configuration.
- Improved isolation from provider-specific latency degradation.

**Disadvantages:**

- Additional HTTP clients and connection pools to manage.
- Higher potential aggregate resource consumption.
- Unused connection capacity in one pool cannot automatically be borrowed by another.

**Conclusion:** Dedicated clients were selected to improve resource isolation.

For example, if Google saturates a shared connection pool with slow generation requests, incoming OpenAI requests may be forced to wait or encounter pool timeouts. Dedicated pools prevent this direct form of resource contention.

This follows the principle behind the Bulkhead Pattern, although providers continue to share application-level resources such as CPU, memory, and the event loop.

## 4. Decision

The gateway will use **application-owned persistent asynchronous HTTP clients, with one dedicated client per HTTP-based provider per application worker**.

The architecture will follow these principles:

- Use `httpx2.AsyncClient` for asynchronous HTTP communication.
- Construct and configure clients within the application's Composition Root.
- Manage client initialization and cleanup through FastAPI lifespan.
- Inject clients into concrete providers through their constructors.
- Reuse HTTP clients and provider instances across generation requests.
- Prohibit providers from closing borrowed HTTP clients.
- Preserve the existing `LLMInterface` Protocol.

## 5. Architectural Rationale

### 5.1. Resource Ownership and Separation of Concerns

The application owns infrastructure resources and is responsible for their creation, configuration, and cleanup.

Providers consume these resources and focus on their primary responsibilities: request translation, external API communication, response normalization, and provider-specific error handling.

A component that borrows a resource must not independently destroy it.

### 5.2. Composition Root and Dependency Injection

The Composition Root is responsible for constructing concrete implementations and assembling their dependencies.

Although it must know the infrastructure requirements of individual providers, this knowledge remains localized rather than spreading throughout the application.

Constructor injection also enables provider implementations to receive HTTP clients configured with HTTPX2's `MockTransport`, allowing deterministic testing without real external API calls.

No additional HTTP client abstraction or dependency injection framework is required.

### 5.3. Preservation of the Provider Contract

The existing provider contract defines behavior, not construction requirements.

HTTP-based providers require HTTP clients, while future local inference providers may require inference engines or entirely different dependencies.

These differences should be handled by the Composition Root rather than imposed on `LLMInterface`.

The orchestration layer remains dependent on the provider abstraction and does not need to know how individual providers are constructed or perform generation.

### 5.4. Concurrency Safety

Shared asynchronous HTTP clients support concurrent requests without requiring sequential execution.

However, reusable provider instances must avoid shared mutable request-specific state. Asynchronous tasks can interfere with one another across suspension points, even within a single thread.

Long-lived dependencies and configuration may be stored in instance attributes, while request-specific data must remain local to individual method invocations.

## 6. Consequences

### Positive

- Efficient connection reuse and reduced connection establishment overhead.
- Support for concurrent asynchronous HTTP communication.
- Centralized and predictable resource lifecycle management.
- Clear separation of resource ownership and consumption.
- Improved provider testability.
- Reduced connection pool contention between providers.
- Preservation of a minimal and implementation-independent provider contract.

### Negative

- The Composition Root must know concrete provider dependencies.
- Application initialization becomes more involved as infrastructure grows.
- Dedicated connection pools may increase aggregate resource consumption.
- Reusable providers must be designed for concurrent use.

These trade-offs are accepted because the gateway benefits more from centralized lifecycle management, explicit dependencies, testability, and resource isolation than from fully self-contained provider implementations.


