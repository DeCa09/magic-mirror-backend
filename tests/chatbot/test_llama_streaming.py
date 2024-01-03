from chatbot.llama_streaming import LlamaChatbot

def test_llama_chatbot_object_creation() -> None:
    llama_chatbot = LlamaChatbot()
    assert llama_chatbot is not None


async def test_llama_chatbot_call_method() -> None:
    llama_chatbot = LlamaChatbot()
    question = "Who is the greatest footballer of all time?"
    assert await llama_chatbot.get_streaming_response(question) is not None