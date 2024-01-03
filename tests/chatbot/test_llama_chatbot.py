from chatbot.llama_chatbot import LlamaChatbot


def test_llama_chatbot_object_creation() -> None:
    llama_chatbot = LlamaChatbot()
    assert llama_chatbot is not None


def test_llama_chatbot_call_method() -> None:
    llama_chatbot = LlamaChatbot()
    question = "Who is the greatest footballer of all time?"
    assert llama_chatbot(question) is not None
