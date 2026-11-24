from typing import Protocol
from app.schemas.llm import LLMRequest, LLMResponse


class LLMInterface(Protocol):
    async def generate(self, request: LLMRequest) -> LLMResponse:
        """Generate a response based on the given request."""
        ...
