import json

from fastapi import FastAPI # type: ignore

from chatbot.falcon_chatbot import FalconChatbot


app = FastAPI()

# load llama model
falcon_chatbot = FalconChatbot()
print(json.dumps("Falcon chatbot model is loaded."))
print(type(falcon_chatbot))

@app.get("/")
async def root() -> dict:
    """
    **Dummy endpoint that returns 'hello world' example.**

    ```
    Returns:
        dict: 'hello world' message.
    ```
    """
    response = {"message": "Hello World from the falcon API!"}
    return response



@app.get("/chatbot")
async def chatbot(user_input: str):
    """
    **Endpoint that returns the chatbot response.**

    ```
    Returns:
        StreamingResponse: chatbot response generator.
    ```
    """
    
    response = falcon_chatbot(user_input)
    print(response)

    return {"chatbot_response": response}

