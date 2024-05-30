from langchain_core.embeddings import Embeddings
from langchain_community.embeddings import FakeEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceHubEmbeddings

from src.cores.common.elastic.configs.elastic_vector_config import ElasticVectorConfig, EmbeddingsType


class ElasticEmbeddingFactory:

    def create(self, config: ElasticVectorConfig) -> Embeddings:
        if (config.embeddings_type == EmbeddingsType.FAKE):
            return FakeEmbeddings(size=3)
        elif (config.embeddings_type == EmbeddingsType.HUGGING_FACE_HUB):
            if config.hugging_face_hub_api_url is None:
                raise ValueError("Hugging Face Hub API URL is required for embedding type: HUGGING_FACE_HUB")
            else:
                return HuggingFaceHubEmbeddings(model=config.hugging_face_hub_api_url)
        elif (config.embeddings_type == EmbeddingsType.HUGGING_FACE):
            return HuggingFaceEmbeddings(model_name=config.hf_model, encode_kwargs={'normalize_embeddings': True}, multi_process=False, show_progress=True)
        else:
            raise Exception(f"Unknown embedding type: {config.embeddings_type}")
