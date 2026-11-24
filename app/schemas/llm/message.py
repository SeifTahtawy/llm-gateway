from enum import StrEnum

from pydantic import BaseModel, field_validator


class MessageRole(StrEnum):
    """Roles of messages in an LLM conversation."""

    USER = "user"
    ASSISTANT = "assistant"


class Message(BaseModel):
    """Text message in an LLM conversation."""

    role: MessageRole
    content: str

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Message content must not be empty or whitespace-only")
        return value
