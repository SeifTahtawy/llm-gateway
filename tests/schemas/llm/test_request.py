import pytest
from pydantic import ValidationError

from app.schemas.llm import LLMRequest, Message, MessageRole, ProviderName

VALID_REQUEST = {
    "provider": "openai",
    "model": "chat-v1",
    "messages": [{"role": "user", "content": "Explain tides."}],
}


def test_request_normalizes_model_and_defaults_optional_parameters_to_none() -> None:
    request = LLMRequest.model_validate(VALID_REQUEST | {"model": "  chat-v1\t"})

    assert request.provider is ProviderName.OPENAI
    assert request.model == "chat-v1"
    assert request.messages == [
        Message(role=MessageRole.USER, content="Explain tides.")
    ]
    assert request.system_instruction is None
    assert request.temperature is None
    assert request.max_output_tokens is None


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("model", ""),
        ("model", " \t\n"),
        ("messages", []),
        ("provider", "unsupported"),
        ("temperature", float("nan")),
        ("temperature", float("inf")),
        ("temperature", float("-inf")),
        ("max_output_tokens", 0),
        ("max_output_tokens", -1),
    ],
)
def test_request_rejects_invalid_field(field: str, value: object) -> None:
    with pytest.raises(ValidationError) as exc:
        LLMRequest.model_validate(VALID_REQUEST | {field: value})

    assert exc.value.errors()[0]["loc"] == (field,)


def test_request_rejects_blank_content_in_nested_message() -> None:
    messages = [
        {"role": "user", "content": "Explain tides."},
        {"role": "assistant", "content": " \n"},
    ]
    with pytest.raises(ValidationError) as exc:
        LLMRequest.model_validate(VALID_REQUEST | {"messages": messages})

    assert exc.value.errors()[0]["loc"] == ("messages", 1, "content")


@pytest.mark.parametrize("instruction", ["", " \t\n"])
def test_request_normalizes_blank_system_instruction_to_none(instruction: str) -> None:
    request = LLMRequest.model_validate(
        VALID_REQUEST | {"system_instruction": instruction}
    )

    assert request.system_instruction is None


def test_request_preserves_meaningful_system_instruction() -> None:
    instruction = "\n  Answer in verse.  \n"
    request = LLMRequest.model_validate(
        VALID_REQUEST | {"system_instruction": instruction}
    )

    assert request.system_instruction == instruction


@pytest.mark.parametrize("temperature", [-0.5, 3.0])
def test_request_accepts_finite_temperatures_outside_provider_ranges(
    temperature: float,
) -> None:
    request = LLMRequest.model_validate(VALID_REQUEST | {"temperature": temperature})

    assert request.temperature == temperature
