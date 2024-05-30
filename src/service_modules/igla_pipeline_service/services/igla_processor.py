from typing import List, Dict

from src.cores.common.elastic.models.elastic_index import ElasticIndexName
from src.cores.common.elastic.stores.elastic_vector_store_factory import ElasticVectorStoreFactory
from src.service_modules.igla_pipeline_service.adapters.igla_document_adapter_factory import IglaDocumentAdapterFactory
from src.service_modules.igla_pipeline_service.configs.igla_pipeline_config import IglaPipelineConfig
from aiostream import stream
import logging


class IglaProcessor:
    def __init__(self, configs: Dict[str, IglaPipelineConfig], store_factory: ElasticVectorStoreFactory,
                 adapter_factory: IglaDocumentAdapterFactory) -> None:
        self.__configs = configs
        self.__store_factory = store_factory
        self.__adapter_factory = adapter_factory

    """
    Asynchronously processes a list of source codes, loading them from an adapter
        and then asynchronously loads documents for each source code into Elasticsearch. 
       Args:
           source_codes (List[str]): A list of source codes to be processed.
       Returns:
           None
    """

    async def process(self, source_codes: List[str]) -> None:
        try:
            for source_code in source_codes:
                if (source_code not in self.__configs):
                    raise ValueError(f"Unknown source code: {source_code}")

                logging.info(f"loading docs for source: {source_code}")
                adapter = self.__adapter_factory.create(source_code)
                vector_store = self.__store_factory.create(ElasticIndexName(name=source_code))
                logging.info(f"store and adapter created for source: {source_code}")
                async with stream.chunks(adapter.aload_segments(),
                                         self.__configs.get(source_code).batch_size).stream() as streamer:
                    async for batch in streamer:
                        await vector_store.aload_documents(batch)
                        logging.info(f"loaded {len(batch)} docs for {source_code} to elasticsearch")
                vector_store.refresh()
                logging.info(f"docs loaded for source: {source_code}")
        except Exception as e:
            logging.error(e, exc_info=True)
            raise e
