from fastapi import FastAPI  # type: ignore

app = FastAPI()


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
