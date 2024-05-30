from typing import Union

from src.cores.common.elastic.clients.elastic_client import ElasticClient
from src.cores.common.elastic.configs.elastic_config import ElasticConfig
from src.cores.common.elastic.configs.elastic_vector_config import ElasticVectorConfig
from src.cores.common.elastic.embeddings.elastic_embedding_factory import ElasticEmbeddingFactory

from src.cores.common.elastic.models.elastic_alias import ElasticAliasName, ElasticAlias
from src.cores.common.elastic.models.elastic_index import ElasticIndex, ElasticIndexName
from src.cores.common.elastic.stores.elastic_vector_store import ElasticVectorStore


class ElasticVectorStoreFactory:
    def __init__(self, client: ElasticClient, elastic_config: ElasticConfig, vector_config: ElasticVectorConfig,
                 embedding_factory: ElasticEmbeddingFactory) -> None:
        self.__client = client
        self.__elastic_config = elastic_config
        self.__vector_config = vector_config
        self.__embedding_factory = embedding_factory

    def create(self, index_name: Union[ElasticIndexName, ElasticAliasName]) -> ElasticVectorStore:
        return ElasticVectorStore(index=self.__indexOrAlias(index_name), client=self.__client,
                                  config=self.__vector_config,
                                  embedding_factory=self.__embedding_factory)

    def __indexOrAlias(self, index_name: Union[ElasticIndexName, ElasticAliasName]) -> Union[
        ElasticIndex, ElasticAlias]:
        if isinstance(index_name, ElasticIndexName):
            return ElasticIndex(prefix=self.__elastic_config.index_prefix, name=index_name)
        elif isinstance(index_name, ElasticAliasName):
            return ElasticAlias(prefix=self.__elastic_config.index_prefix, name=index_name)
        else:
            raise ValueError(f"Invalid index name: {index_name}")
