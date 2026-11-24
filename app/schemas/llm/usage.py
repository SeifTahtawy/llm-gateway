from typing import Self
from pydantic import BaseModel, Field, field_validator, model_validator


class TokenUsage(BaseModel):
    """Token measurements reported by an LLM provider."""

    input_tokens: int | None = Field(default=None, ge=0)
    output_tokens: int | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def validate_measurements(self) -> Self:
        if self.input_tokens is None and self.output_tokens is None:
            raise ValueError("At least one token measurement must be provided")
        return self