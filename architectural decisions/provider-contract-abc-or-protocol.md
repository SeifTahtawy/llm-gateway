# Provider contract — ABC or Protocol

**Status** — Pending. The user will choose after the design discussion.

## Context

The gateway needs to expose consistent behavior while providers differ in request payloads, response formats, and errors. Provider adapters can translate those differences behind a contract expressed in gateway-owned types. This would let the calling code depend on the operation it needs and make it possible to substitute a provider or test double.

## Options and trade-offs

| Option | How it could help this gateway | Where it fits best and what it costs |
| --- | --- | --- |
| Abstract base class (`ABC`) | Makes membership explicit through inheritance. Python prevents instantiation of ordinary subclasses with unresolved abstract methods. A base class can also share behavior if the adapters turn out to need the same implementation. | Fits when one team owns the adapter hierarchy and needs a common lifecycle or meaningful shared behavior. Every ordinary implementation and fake must opt into that hierarchy. Signature compatibility still relies on static checking, and behavior needs tests. |
| `typing.Protocol` | Lets adapters and fakes satisfy the contract structurally through compatible member signatures checked by MyPy. Implementations can conform without importing or inheriting from the contract. | Fits when adapters are independent, wrap externally owned types, or primarily share a typed interface. Conformance needs a typed use site for static checking. Optional `@runtime_checkable` checks attribute presence and provides no signature validation. |
| Direct calls or untyped duck typing | Can keep a one-provider spike quick and expose what actually varies between providers. | Fits throwaway exploration. As a gateway adds providers, implicit expectations are easier to miss and can move translation and failure handling into the caller. |

See the Python 3.12 documentation on [abstract base classes](https://docs.python.org/3.12/library/abc.html#abc.abstractmethod) and [protocols](https://docs.python.org/3.12/library/typing.html#typing.Protocol).

## What will settle the choice

- Identify the first operation the caller needs and which request and response types the gateway owns.
- Decide whether adapters actually need shared behavior or only a common typed surface. Explain how a second adapter and a test fake would satisfy each option.
- Define the async call shape and where provider errors are translated. Discuss how streaming and cancellation would affect that boundary when introduced.
- Record the user's choice and reasoning before implementing the first contract. Use tests to verify behavioral promises such as error translation regardless of the typing mechanism.
