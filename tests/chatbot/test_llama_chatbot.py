from chatbot.llama_chatbot import LlamaChatbot


def test_llama_chatbot_object_creation() -> None:
    llama_chatbot = LlamaChatbot()
    assert llama_chatbot is not None


def test_llama_chatbot_call_method() -> None:
    llama_chatbot = LlamaChatbot()
    assert llama_chatbot("abc") == 3
