import pytest
from pydantic import ValidationError

from app.schemas.llm import TokenUsage


@pytest.mark.parametrize(
    ("measurements", "expected_input", "expected_output"),
    [
        ({"input_tokens": 12, "output_tokens": 5}, 12, 5),
        ({"input_tokens": 0}, 0, None),
        ({"output_tokens": 0}, None, 0),
    ],
)
def test_usage_preserves_reported_counts(
    measurements: dict[str, int],
    expected_input: int | None,
    expected_output: int | None,
) -> None:
    usage = TokenUsage.model_validate(measurements)

    assert usage.input_tokens == expected_input
    assert usage.output_tokens == expected_output


@pytest.mark.parametrize("field", ["input_tokens", "output_tokens"])
def test_usage_rejects_negative_counts(field: str) -> None:
    with pytest.raises(ValidationError) as exc:
        TokenUsage.model_validate({field: -1})

    assert exc.value.errors()[0]["loc"] == (field,)


def test_usage_requires_at_least_one_measurement() -> None:
    with pytest.raises(ValidationError):
        TokenUsage()
