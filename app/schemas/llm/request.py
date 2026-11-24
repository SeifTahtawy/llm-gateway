from pydantic import BaseModel, Field, field_validator

from app.schemas.llm.enums import ProviderName
from app.schemas.llm.message import Message


class LLMRequest(BaseModel):
    """Provider-independent request to an LLM provider."""

    provider: ProviderName
    model: str
    messages: list[Message] = Field(min_length=1)
    system_instruction: str | None = None
    temperature: float | None = Field(default=None, allow_inf_nan=False)
    max_output_tokens: int | None = Field(default=None, gt=0)

    @field_validator("model")
    @classmethod
    def validate_model(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Model identifier must not be empty or whitespace-only")
        return value

    @field_validator("system_instruction")
    @classmethod
    def validate_system_instruction(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            return None
        return value
