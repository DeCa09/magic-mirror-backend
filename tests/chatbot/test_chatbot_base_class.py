import typing

import pytest

from chatbot.chatbot import Chatbot


@typing.no_type_check
def test_if_chatbot_object_creation_fails() -> None:
    with pytest.raises(TypeError):
        Chatbot()
