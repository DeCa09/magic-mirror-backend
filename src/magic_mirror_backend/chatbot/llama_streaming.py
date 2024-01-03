import os
import asyncio
from typing import Any, Dict, List, Literal, Union, cast

from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.manager import AsyncCallbackManager
from langchain.callbacks.base import AsyncCallbackHandler

from chatbot.chatbot import Chatbot
from chatbot.prompt_templates import DEFAULT_PROMPT_TEMPLATE, DEFAULT_PROMPT_INPUT_VARS

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
PATH_TO_MODEL_ARTIFACTS = os.path.join(DIR_PATH, "..", "..", "..", "model_artifacts",  "chatbot", "7B-chat", "llama_cpp")
MODEL_ARTIFACT_NAME = "llama-2-7b-chat.ggmlv3.q4_0.bin"


# CONSTANT FOR MODEL TO LOAD
MODEL_PATH = os.path.join(PATH_TO_MODEL_ARTIFACTS, MODEL_ARTIFACT_NAME)


# CONSTANTS FOR GPU CONFIG
N_GPU_LAYERS = 40  # Change this value based on your model and your GPU VRAM pool.
N_BATCH = 512  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.



class AsyncStreamingCallbackHandler(AsyncCallbackHandler):
    queue: asyncio.Queue[str]
    llm_run_is_done_flag: asyncio.Event
    
    def __init__(self):
        self.queue = asyncio.Queue()
        self.llm_run_is_done_flag = asyncio.Event()

    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.llm_run_is_done_flag.is_set() and self.queue.empty():
            raise StopAsyncIteration
        
        token = await self.queue.get()
        # TODO: see if we can do this more elegantly
        self.queue.task_done() 
        return token
        
    async def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        # init at beginning of run
        self.llm_run_is_done_flag.clear()
    
    
    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        #print(f"TOKI TOKI TOKI! ---> {token}")
        if token:
            self.queue.put_nowait(token)
    
    def on_llm_end(self, response, **kwargs: Any) -> None:
        self.llm_run_is_done_flag.set()


    def on_llm_error(self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any) -> None:
        self.llm_run_is_done_flag.set()


class LlamaChatbot(Chatbot):
    def __init__(self) -> None:
        self.callback_handler = AsyncStreamingCallbackHandler()
        self.callback_manager = AsyncCallbackManager([self.callback_handler])
        
        llm_chain = self.__setup_llm_chain()
        self.chatbot = llm_chain
        print("Laueft alles wie geschmiert bro mo no")
    
    def __setup_llm_chain(self):
        prompt = self.__get_prompt()
        llm = self.__get_llm()
        
        # TODO: DELETE later
        self.llm = llm
        
        llm_chain = LLMChain(prompt=prompt, llm=llm)
        
        return llm_chain
    
    
    def __get_prompt(self):
        prompt = PromptTemplate(template=DEFAULT_PROMPT_TEMPLATE, input_variables=DEFAULT_PROMPT_INPUT_VARS)
        return prompt
    
    def __get_llm(self):
        self.callback_manager = self.__get_callback_manager()
        
        llm = LlamaCpp(
            model_path=MODEL_PATH,
            n_gpu_layers=N_GPU_LAYERS,
            n_batch=N_BATCH,
            callback_manager=self.callback_manager,
            verbose=True,
            streaming=True,
            )
        return llm

    def __get_callback_manager(self):
        return self.callback_manager

    def get_callback_handler(self):
        return self.callback_handler


    """
    async def get_streaming_response(self, user_input: str):
        async_callback_handler = self.callback_handler

        self.chatbot.run(
            question=user_input,
            callbacks=[async_callback_handler]
            )

        async for token in async_callback_handler:
            print(f"next token is: {token}")
    """

    def __call__(self, user_input: str) -> None:
        self.chatbot.run(
            question=user_input,
            callbacks=[self.get_callback_handler()]
        )
