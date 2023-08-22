import os

from langchain import HuggingFacePipeline, LLMChain, PromptTemplate
from transformers import AutoTokenizer, LlamaForCausalLM, pipeline

from chatbot.chatbot import Chatbot

import time # TODO: DELETE LATER, ONLY FOR TRACKING TIME
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
PATH_TO_MODEL_ARTIFACTS = os.path.join(DIR_PATH, "..", "..", "..", "model_artifacts/")


"""
PROMPT STUFF
"""
B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"

DEFAULT_SYSTEM_PROMPT = """\
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."""


def get_prompt(instruction, new_system_prompt=DEFAULT_SYSTEM_PROMPT):
    SYSTEM_PROMPT = B_SYS + new_system_prompt + E_SYS
    prompt_template = B_INST + SYSTEM_PROMPT + instruction + E_INST
    return prompt_template


system_prompt = "You are an advanced assistant."
instruction = (
    "Reply very quickly, don't think too much about it.:\n\n {text}"
)
template = get_prompt(instruction, system_prompt)
# print(template)


class LlamaChatbot(Chatbot):
    def __init__(self) -> None:
        # load model
        tokenizer = AutoTokenizer.from_pretrained(PATH_TO_MODEL_ARTIFACTS)
        model = LlamaForCausalLM.from_pretrained(
            PATH_TO_MODEL_ARTIFACTS,
            use_safetensors=True,
            device_map="auto",
            load_in_8bit=True,
        )

        chatbot_pipeline = pipeline(
            task="text-generation",
            model=model,
            tokenizer=tokenizer,
            device_map="auto",
            max_new_tokens=512,
        )

        
        llm = HuggingFacePipeline(pipeline=chatbot_pipeline)
        prompt = PromptTemplate(template=template, input_variables=["text"])

        llm_chain = LLMChain(prompt=prompt, llm=llm)

        self.__chatbot = llm_chain
        
        print("Alles laueft wie geschmiert bro.")
        print("Quantized shit.")

    def __call__(self, user_input: str) -> int:
        beginning = time.time()
        print("The __call__ method has been executed.")
        print(
            f"This is the __chatbot property of the llama_chatbot object: {self.__chatbot}"
        )
        response = self.__chatbot(user_input)
        end = time.time() - beginning
        
        print(f"This is how much time the chatbot took: {end:.2f} seconds")
        return self.__chatbot(user_input)
