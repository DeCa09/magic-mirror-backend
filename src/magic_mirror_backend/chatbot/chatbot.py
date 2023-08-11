from abc import ABC, abstractmethod


class Chatbot(ABC):
    @abstractmethod
    def __init__(self) -> None:
        """Initialize chatbot object."""

    @abstractmethod
    def __call__(self, user_input: str) -> int:
        """Abstract __call__ method for chatbots that only take user_input as input."""
