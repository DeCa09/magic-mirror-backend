from chatbot.chatbot import Chatbot


class LlamaChatbot(Chatbot):
    def __init__(self) -> None:
        self.__chatbot = len  # TODO: dummy, so change this

    def __call__(self, user_input: str) -> int:
        print("The __call__ method has been executed.")
        print(
            f"This is the __chatbot property of the llama_chatbot object: {self.__chatbot}"
        )
        return self.__chatbot(user_input)
