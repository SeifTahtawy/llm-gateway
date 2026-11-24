import pytest
from pydantic import ValidationError

from app.schemas.llm import Message, MessageRole


@pytest.mark.parametrize("content", ["", " \t\n"])
def test_message_rejects_blank_content(content: str) -> None:
    with pytest.raises(ValidationError):
        Message(role=MessageRole.USER, content=content)


def test_message_preserves_content_whitespace() -> None:
    content = "\n    return answer\n"
    message = Message(role=MessageRole.ASSISTANT, content=content)

    assert message.content == content
