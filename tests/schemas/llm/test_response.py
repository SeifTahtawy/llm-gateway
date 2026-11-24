import pytest
from pydantic import ValidationError

from app.schemas.llm import FinishReason, LLMResponse, ProviderName, TokenUsage

VALID_RESPONSE = {"provider": "openai", "model": "chat-v1", "content": "Hello!"}


def test_response_preserves_complete_provider_metadata() -> None:
    raw_reason = "\tprovider_limit  "
    response = LLMResponse.model_validate(
        VALID_RESPONSE
        | {
            "model": " chat-v1\n",
            "usage": {"input_tokens": 8, "output_tokens": 2},
            "finish_reason": "other",
            "raw_finish_reason": raw_reason,
        }
    )

    assert response.provider is ProviderName.OPENAI
    assert response.model == "chat-v1"
    assert response.content == "Hello!"
    assert response.usage == TokenUsage(input_tokens=8, output_tokens=2)
    assert response.finish_reason is FinishReason.OTHER
    assert response.raw_finish_reason == raw_reason


@pytest.mark.parametrize("content", ["", " \t\n"])
def test_response_preserves_blank_content_without_metadata(content: str) -> None:
    response = LLMResponse.model_validate(VALID_RESPONSE | {"content": content})

    assert response.content == content
    assert response.usage is None
    assert response.finish_reason is None
    assert response.raw_finish_reason is None


@pytest.mark.parametrize("model", ["", " \t\n"])
def test_response_rejects_blank_model(model: str) -> None:
    with pytest.raises(ValidationError):
        LLMResponse.model_validate(VALID_RESPONSE | {"model": model})


def test_other_finish_reason_allows_omitted_raw_reason() -> None:
    response = LLMResponse.model_validate(VALID_RESPONSE | {"finish_reason": "other"})

    assert response.finish_reason is FinishReason.OTHER
    assert response.raw_finish_reason is None


@pytest.mark.parametrize(
    "reason",
    [
        None,
        FinishReason.COMPLETED,
        FinishReason.MAX_TOKENS,
        FinishReason.CONTENT_FILTER,
    ],
)
def test_raw_reason_requires_other_finish_reason(reason: FinishReason | None) -> None:
    with pytest.raises(ValidationError):
        LLMResponse.model_validate(
            VALID_RESPONSE | {"finish_reason": reason, "raw_finish_reason": "limit"}
        )


@pytest.mark.parametrize("raw_reason", ["", " \t\n"])
def test_response_rejects_blank_raw_finish_reason(raw_reason: str) -> None:
    with pytest.raises(ValidationError):
        LLMResponse.model_validate(
            VALID_RESPONSE | {"finish_reason": "other", "raw_finish_reason": raw_reason}
        )
