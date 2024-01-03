from chatbot.falcon_chatbot import FalconChatbot


def test_llama_chatbot_object_creation() -> None:
    falcon_chatbot = FalconChatbot()
    assert falcon_chatbot is not None


def test_llama_chatbot_call_method() -> None:
    falcon_chatbot = FalconChatbot()
    question = "Who is the greatest footballer of all time?"
    assert falcon_chatbot(question) is not None
