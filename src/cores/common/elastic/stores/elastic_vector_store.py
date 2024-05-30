from langchain_core.vectorstores import VectorStoreRetriever

from src.cores.common.elastic.clients.elastic_client import ElasticClient
from langchain_elasticsearch import ElasticsearchStore
from typing import List, Union, Any
from src.cores.common.elastic.configs.elastic_vector_config import ElasticVectorConfig
from src.cores.common.elastic.embeddings.elastic_embedding_factory import ElasticEmbeddingFactory
from src.cores.common.elastic.models.elastic_alias import ElasticAlias
from src.cores.common.elastic.models.elastic_index import ElasticIndex
from src.cores.common.elastic.models.store_document import StoreDocument

#https://api.python.langchain.com/en/latest/vectorstores/langchain_elasticsearch.vectorstores.ElasticsearchStore.html

class ElasticVectorStore:
    def __init__(self, index: Union[ElasticIndex, ElasticAlias], client: ElasticClient, config: ElasticVectorConfig,
                 embedding_factory: ElasticEmbeddingFactory) -> None:
        self.__index = index
        self.__config = config
        self.__store = ElasticsearchStore(
            embedding=embedding_factory.create(config),
            index_name=str(index),
            es_connection=client.elastic,
            distance_strategy="COSINE"
        )

    async def aload_documents(self, documents: List[StoreDocument]) -> List[str]:
        await self.__store.aadd_documents(list(map(lambda doc: doc.to_document(), documents)))

    def refresh(self) -> None:
        self.__store.client.indices.refresh(index=str(self.__index))

    def as_retriever(self, **kwargs: Any) -> VectorStoreRetriever:
        return self.__store.as_retriever(**kwargs)
    
    def similarity_search(self, **kwargs: Any):
        return self.__store.similarity_search(**kwargs)
