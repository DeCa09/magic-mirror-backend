import json
import os
import logging
import time

from fastapi import APIRouter, FastAPI, UploadFile, File
from starlette.background import BackgroundTasks

from utils.scripts.inference import audio_transcription_model

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ROUTING_PREFIX = "/transcription"

app = FastAPI()
router = APIRouter(prefix=ROUTING_PREFIX)

@router.get("/")
async def root() -> dict:
    """
    **Dummy endpoint that returns 'hello world' example.**

    ```
    Returns:
        dict: 'hello world' message.
    ```
    """
    return {"message": "Hello World from the transcription API!"}


@router.post("/transcribe")
async def get_transcription(audio_data: UploadFile = File(...)) -> dict[str, str]:
    """
    **Endpoint implementing the audio transcription logic.**

    ```
    Args:
        audio_file[UploadFile]: 
    Returns:
        dict[str, str]: Dictionary containing 'transcription' as a key, and the transcription of the audio as the value.
    ```
    """
    start = time.time()
    file_content = await audio_data.read()    
    
    with open(audio_data.filename, 'wb') as outputfile:
        outputfile.write(file_content)
    
    result = audio_transcription_model.transcribe(audio_data.filename)
    end = time.time()
    print(f"Transcription took: {(end-start):.2f} seconds.")
    logger.info(f"Transciption result: {result['text']}")
    print(result['text'])
    
    BackgroundTasks(_remove_file(audio_data.filename))
    
    return {"transcription": result['text']}

def _remove_file(file_path: str) -> None:
    os.unlink(file_path)

# needs to be at the end
app.include_router(router)
