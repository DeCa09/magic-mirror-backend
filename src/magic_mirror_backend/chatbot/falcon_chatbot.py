import os

from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

from langchain import HuggingFacePipeline
from langchain import PromptTemplate,  LLMChain

from chatbot.chatbot import Chatbot
from chatbot.prompt_templates import DEFAULT_PROMPT_TEMPLATE, DEFAULT_PROMPT_INPUT_VARS


DIR_PATH = os.path.dirname(os.path.realpath(__file__))
PATH_TO_MODEL_ARTIFACTS = os.path.join(DIR_PATH, "..", "..", "..", "model_artifacts",  "chatbot", "falcon")



class FalconChatbot(Chatbot):
    def __init__(self) -> None:
        tokenizer = AutoTokenizer.from_pretrained(PATH_TO_MODEL_ARTIFACTS)
        model = AutoModelForCausalLM.from_pretrained(PATH_TO_MODEL_ARTIFACTS, device_map="auto", trust_remote_code=True, load_in_8bit=True)
        
        chatbot_pipeline = pipeline(
            task="text-generation",
            model=model,
            tokenizer=tokenizer,
            device_map='auto',
            max_new_tokens=512,
            )

        llm = HuggingFacePipeline(pipeline=chatbot_pipeline)
        prompt = PromptTemplate(template=DEFAULT_PROMPT_TEMPLATE, input_variables=DEFAULT_PROMPT_INPUT_VARS)

        llm_chain = LLMChain(prompt=prompt, llm=llm)

        self.__chatbot = llm_chain

        print("Alles laueft wie geschmiert falcon brother.")



    def __call__(self, user_input: str) -> int:
        return self.__chatbot(user_input)
