from enum import StrEnum


class FinishReason(StrEnum):
    """Provider-independent reasons for generation to stop."""

    COMPLETED = "completed"
    MAX_TOKENS = "max_tokens"
    CONTENT_FILTER = "content_filter"
    OTHER = "other"


class ProviderName(StrEnum):
    """Names of LLM providers."""

    GOOGLE = "google"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
