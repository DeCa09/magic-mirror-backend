import os
import sys
from typing import Dict, List, Any

from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.base import BaseCallbackHandler

from chatbot.chatbot import Chatbot
from chatbot.prompt_templates import DEFAULT_PROMPT_TEMPLATE, DEFAULT_PROMPT_INPUT_VARS


DIR_PATH = os.path.dirname(os.path.realpath(__file__))
PATH_TO_MODEL_ARTIFACTS = os.path.join(DIR_PATH, "..", "..", "..", "model_artifacts",  "chatbot", "7B-chat", "llama_cpp")
MODEL_ARTIFACT_NAME = "llama-2-7b-chat.ggmlv3.q4_0.bin"


# CONSTANT FOR MODEL TO LOAD
MODEL_PATH = os.path.join(PATH_TO_MODEL_ARTIFACTS, MODEL_ARTIFACT_NAME)

# TODO: delete in case this works.
# CONSTANTS FOR PROMPT AND PROMPT TEMPLATE
# PROMPT_TEMPLATE = """Question: {question}
# Answer: Provide a short answer but make sure that the answer is clear and correct."""
# LIST_OF_PROMPT_INPUT_VARS = ["question"]


# CONSTANTS FOR GPU CONFIG
N_GPU_LAYERS = 40  # Change this value based on your model and your GPU VRAM pool.
N_BATCH = 512  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.



class StreamingCallbackHandler(BaseCallbackHandler):
            
    def __iter__(self):
        self.generated_response = ''
        self.response_generation_finished = False
        return self
    
    def __next__(self):
        if self.response_generation_finished:
            raise StopIteration
        return self.generated_response
    
    
    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """Run when LLM starts running."""
        self.generated_response = ''
        sys.stdout.write("Initialized the Chatbot response.")
        sys.stdout.flush()

    
    def on_llm_new_token(self, token: str, **kwargs) -> str:
        self.generated_response +=token
        #sys.stdout.write(f"This is the response so far: {self.generated_response}")
        #sys.stdout.flush()

        
    def on_llm_end(self, response, **kwargs: Any) -> None:
        """Run when LLM ends running."""
        self.response_generation_finished = True


class LlamaChatbot(Chatbot):
    def __init__(self) -> None:
        llm_chain = self.__setup_llm_chain()
        self.chatbot = llm_chain
        print("Laueft alles wie geschmiert bro mo no")
    
    def __setup_llm_chain(self):
        prompt = self.__get_prompt()
        llm = self.__get_llm()
        
        llm_chain = LLMChain(prompt=prompt, llm=llm)
        
        return llm_chain
    
    
    def __get_prompt(self):
        prompt = PromptTemplate(template=DEFAULT_PROMPT_TEMPLATE, input_variables=DEFAULT_PROMPT_INPUT_VARS)
        return prompt
    
    def __get_llm(self):
        callback_manager = self.__get_callback_manager()
        
        llm = LlamaCpp(
            model_path=MODEL_PATH,
            n_gpu_layers=N_GPU_LAYERS,
            n_batch=N_BATCH,
            callback_manager=callback_manager,
            verbose=True,
            streaming=True,
            )
        return llm
    
    def __get_callback_manager(self):
        callback_manager = CallbackManager([StreamingCallbackHandler()])
        return callback_manager
    
        
    def __call__(self, user_input: str) -> None:
        return self.chatbot(user_input)

