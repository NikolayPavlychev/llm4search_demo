
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, GPTQConfig
from auto_gptq import AutoGPTQForCausalLM

from langchain_community.chat_models.fake import FakeListChatModel
from langchain_community.chat_models.huggingface import ChatHuggingFace

from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline

from langchain_community.llms.fake import FakeListLLM
from langchain_core.language_models import BaseChatModel

from src.service_modules.igla_chat_service.configs.igla_chat_config import IglaChatConfig, ChatModelType


class ChatModelFactory:
    def __init__(self, config: IglaChatConfig) -> None:
        self.__config = config

    def create(self):
        if (self.__config.chat_model_type == ChatModelType.HUGGING_FACE_ENDPOINT):
            if (self.__config.hugging_face_hub_api_url is None or self.__config.hugging_face_hub_api_token is None):
                raise ValueError(
                    "Hugging Face Hub API URL and token are required for chat model type: HUGGING_FACE_ENDPOINT")
            else:
                llm = HuggingFaceEndpoint(
                    endpoint_url=self.__config.hugging_face_hub_api_url,
                    task=self.__config.task,
                    max_new_tokens=self.__config.max_new_tokens,
                    top_k=self.__config.top_k,
                    temperature=self.__config.temperature,
                    repetition_penalty=self.__config.repetition_penalty,
                    huggingfacehub_api_token=self.__config.hugging_face_hub_api_token
                )
                return ChatHuggingFace(llm=llm)
        elif (self.__config.chat_model_type == ChatModelType.FAKE):
            return FakeListChatModel(responses=["hello RAG", "world with RAG", "test with RAG"])
        elif (self.__config.chat_model_type == ChatModelType.HUGGING_FACE):
   
            gptq_config = GPTQConfig(bits=4, group_size=32, disable_exllama=True)
            model = AutoGPTQForCausalLM.from_quantized(self.__config.llm_hf_model_path, device_map="auto",
                                                       quantization_config=gptq_config, disable_exllama=True)
                                                                                 
            tokenizer = AutoTokenizer.from_pretrained(self.__config.llm_hf_model_path,
                                                      use_fast=True)
            #https://huggingface.co/docs/transformers/generation_strategies
            pipe = pipeline(
                    task=self.__config.task,
                    model=model,
                    tokenizer=tokenizer,
                    batch_size=1,
                    max_new_tokens=self.__config.max_new_tokens,
                    do_sample=True,
                    num_return_sequences=1,
                    # num_beams=4,
                    temperature=self.__config.temperature,
                    top_p=self.__config.top_p,
                    top_k=self.__config.top_k,
                    repetition_penalty=self.__config.repetition_penalty
                )
            local_llm=HuggingFacePipeline(pipeline=pipe)
            return local_llm

        else:
            raise Exception(f"Unknown chat model type: {self.__config.chat_model_type}")
