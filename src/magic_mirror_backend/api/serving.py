import json

from fastapi import FastAPI, APIRouter # type: ignore
from fastapi.responses import StreamingResponse

from chatbot.llama_fast import LlamaChatbot

import time # TODO: delete this shit

ROUTING_PREFIX = "/chat"

app = FastAPI()
router = APIRouter(prefix=ROUTING_PREFIX)


# load llama model
llama_chatbot = LlamaChatbot()
print(json.dumps("Llama chatbot model is loaded."))
print(type(llama_chatbot))

@router.get("/")
async def root() -> dict:
    """
    **Dummy endpoint that returns 'hello world' example.**

    ```
    Returns:
        dict: 'hello world' message.
    ```
    """
    response = {"message": "Hello World from the chatbot API!"}
    return response



@router.get("/chatbot")
async def chatbot(user_input: str) -> StreamingResponse:
    """
    **Endpoint that returns the chatbot response.**

    ```
    Returns:
        StreamingResponse: chatbot response generator.
    ```
    """
    
    #start = time.time()
    #_get_response_generator(llama_chatbot(user_input)) # TODO: delete later
    #end = time.time()
    #print(f"Creating the generator took: {(end-start):.2f} seconds!")
    
    """
    print(f"Type of the response:\n  {type(response)}")
    print(f"This is the chatbot response:\n  {response}")
    """

    
    response = llama_chatbot(user_input)
    
    print(response)
    
    return {"chatbot_response": response}
    #return StreamingResponse(_get_response_generator(user_input),  media_type='text/event-stream')
    

def _get_response_generator(user_input: str):
    response = llama_chatbot(user_input)
    
    print("DEBUGGY BUG")
    #print(response)
    print(f"Type of the response obj:\n  {type(response)}")

    yield from response
    print("WE SLEEP")
    time.sleep(0.8)
    
    """
    for token in response:
        print("DEBUG AHEAD")
        #print(token)
        print(f"Type of the token obj:\n  {type(token)}")
        print(f"Token dict keys:\n  {token.keys()}")
        yield token
    """
    #yield response


"""
SEE IF STREAMING WORKS
"""
def fake_data_streamer():
    for _ in range(10):
        yield b'some fake data\n\n'
        time.sleep(1)


@router.get('/stream')
async def main():
    return StreamingResponse(fake_data_streamer(), media_type='text/event-stream')
    # or, use:
    #headers = {'X-Content-Type-Options': 'nosniff'}
    #return StreamingResponse(fake_data_streamer(), headers=headers, media_type='text/plain')


# needs to be at the end
app.include_router(router)
