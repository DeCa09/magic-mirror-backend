import json
import asyncio

from fastapi import FastAPI, APIRouter # type: ignore
from fastapi.responses import StreamingResponse

from starlette.responses import StreamingResponse

from chatbot.llama_streaming import LlamaChatbot

import time # TODO: delete this shit


ROUTING_PREFIX = ""

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
    response = {"message": "Hello World from the streaming chatbot API!"}
    return response


@router.get("/chatbot")
async def stream_response_to_api(user_input:str):
    return StreamingResponse(_stream_token(user_input), media_type='text/event-stream')


async def _stream_token(user_input: str) -> StreamingResponse:
    """
    **Endpoint that returns the chatbot response.**

    ```
    Returns:
        StreamingResponse: chatbot response generator.
    ```
    """
    stream_start = time.time()
    # get handler
    handler = _get_response_generator()
    
    # trigger chatbot run
    print("TRIGGERING INPUT")
    start = time.time()
    
    llm_token_producer_task = asyncio.create_task(_trigger_chatbot_run(user_input))
    
    await asyncio.sleep(0.1)
    print("WHEN IS THIS HAPPENING")
    print(f"It happened {(time.time()-start):.2f} seconds after triggering the input!!!")
    
    async for token in handler.aiter(): # NOTE: changed this to use aiter instead of handler
        print(f"The token is in the API: {token}")
        yield token
        time.sleep(0.01)

    await llm_token_producer_task
        
    stream_end = time.time()
    print(f"The response streaming took: {(stream_end-stream_start):.2f} seconds!")
    print("DO I EVER GET HERE? :(")

def _get_response_generator():
    handler = llama_chatbot.get_callback_handler()
    return handler

    
async def _trigger_chatbot_run(user_input: str):
    llama_chatbot(user_input)


"""
SEE IF STREAMING WORKS
"""

@router.get("/fake_streamer_async")
async def fake_streamer_async():
    return StreamingResponse(_fake_async_streamer(), media_type='text/event-stream')

@router.get("/fake_streamer_not_async")
async def fake_streamer_not_async():
    return StreamingResponse(fake_data_streamer(), media_type='text/event-stream')


async def _fake_async_streamer():
    async for _ in asyncio.range(10):
        yield b'some fake data\n\n'
        await asyncio.sleep(1)


def fake_data_streamer():
    for _ in range(10):
        yield b'some fake data\n\n'
        time.sleep(1)


# needs to be at the end
app.include_router(router)
