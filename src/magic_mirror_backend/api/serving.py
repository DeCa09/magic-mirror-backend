import json

from fastapi import FastAPI  # type: ignore

from chatbot.llama_chatbot import LlamaChatbot

app = FastAPI()


# load dummy model
llama_chatbot = LlamaChatbot()
print(json.dumps("Dummy model is loaded."))
print(type(llama_chatbot))


@app.get("/")
async def root() -> dict:
    """
    **Dummy endpoint that returns 'hello world' example.**

    ```
    Returns:
        dict: 'hello world' message.
    ```
    """
    response = {"message": "Hello World"}
    return response


@app.get("/chatbot")
async def chatbot(user_input: str) -> dict:
    """
    **Endpoint that returns the chatbot response.**

    ```
    Returns:
        dict: chatbot response message.
    ```
    """

    llama_chatbot = LlamaChatbot()
    response = llama_chatbot(user_input)

    return {"chatbot_response": response}
