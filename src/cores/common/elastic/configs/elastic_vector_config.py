from dataclasses import dataclass
from enum import Enum
from typing import Optional


class EmbeddingsType(Enum):
    FAKE = "fake"
    HUGGING_FACE_HUB = "hugging_face_hub"
    HUGGING_FACE = "hugging_face"


@dataclass
class ElasticVectorConfig:
    embeddings_type: EmbeddingsType
    hf_model = 'sentence-transformers/all-mpnet-base-v2'
    hugging_face_hub_api_url: Optional[str]
