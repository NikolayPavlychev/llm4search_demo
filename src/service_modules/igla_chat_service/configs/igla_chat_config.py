from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ChatModelType(Enum):
    FAKE = "fake"
    HUGGING_FACE_ENDPOINT = "hugging_face_endpoint"
    HUGGING_FACE = "hugging_face"


@dataclass
class IglaChatConfig:
    chat_model_type: ChatModelType
    llm_hf_model_path: str
     
    task: str
    max_new_tokens: int
    top_k: int
    top_p: float
    temperature: float
    repetition_penalty: float
    
    hugging_face_hub_api_url: Optional[str]
    hugging_face_hub_api_token: Optional[str]
    
