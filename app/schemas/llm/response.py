from typing import Self

from pydantic import BaseModel, field_validator, model_validator

from app.schemas.llm.enums import FinishReason, ProviderName
from app.schemas.llm.usage import TokenUsage


class LLMResponse(BaseModel):
    """Provider-independent response from an LLM provider."""

    provider: ProviderName
    model: str
    content: str
    usage: TokenUsage | None = None
    finish_reason: FinishReason | None = None
    raw_finish_reason: str | None = None

    @field_validator("model")
    @classmethod
    def validate_model(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Model identifier must not be empty or whitespace-only")
        return value

    @field_validator("raw_finish_reason")
    @classmethod
    def validate_raw_finish_reason(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("Raw finish reason must not be empty or whitespace-only")
        return value

    @model_validator(mode="after")
    def validate_finish_reason(self) -> Self:
        if (
            self.raw_finish_reason is not None
            and self.finish_reason != FinishReason.OTHER
        ):
            raise ValueError("Raw finish reason requires finish reason to be OTHER")
        return self
