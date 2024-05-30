import os
import sys

from dotenv import load_dotenv
from dotenv import dotenv_values

load_dotenv('/home/nikolaypavlychev/llm4search_dev/llm4search_dev/llm4search/.env')
config = dotenv_values()
sys.path.append(config['HOME'])
sys.path.append(config['SRC'])



import logging
from configparser import ConfigParser
from typing import Dict

from src.cores.common.elastic.clients.elastic_client import ElasticClient
from src.cores.common.elastic.configs.elastic_config import ElasticConfig
from src.cores.common.elastic.configs.elastic_vector_config import ElasticVectorConfig, EmbeddingsType
from src.cores.common.elastic.embeddings.elastic_embedding_factory import ElasticEmbeddingFactory
from src.cores.common.elastic.stores.elastic_vector_store_factory import ElasticVectorStoreFactory
from src.cores.common.web.web_api import WebApi
from src.cores.common.workers.singleton_worker import SingletonWorker
from src.cores.igla.models.source_code import SOURCE_CODE_TEST, SOURCE_CODE_IGLA, SOURCE_CODE_CHERRY_CAR
from src.service_modules.igla_pipeline_service.adapters.igla_document_adapter_factory import IglaDocumentAdapterFactory
from src.service_modules.igla_pipeline_service.configs.igla_pipeline_config import IglaPipelineConfig, IglaAdapterType, \
    IglaSplitterType
from src.service_modules.igla_pipeline_service.controllers.igla_pipeline_controller import IglaPipelineController
from src.service_modules.igla_pipeline_service.services.igla_processor import IglaProcessor
from src.service_modules.igla_pipeline_service.splitters.igla_article_splitter_factory import IglaArticleSplitterFactory

'''
Main igla pipeline application
1. http://0.0.0.0:8000 - api
2. http://0.0.0.0:8000/docs - swagger

load sources:
1. via api
curl --location --request POST 'http://0.0.0.0:8000/api/v1/igla-pipeline/crawl' \
--header 'Content-Type: application/json' \
--data-raw '[
  "igla", "cherry_car"
]'

2. via swagger  
http://0.0.0.0:8000/docs#/default/crawl_api_v1_igla_pipeline_crawl_post
[
  "test", "igla", "cherry_car"
] 

3. Check index via Kibana (http://localhost:5601/app/dev_tools#/console):
GET local.index.doc.test/_count
GET local.index.doc.igla/_count
GET local.index.doc.cherry_car/_count

GET local.index.doc.test/_search
GET local.index.doc.igla/_search
GET local.index.doc.cherry_car/_search

DELETE local.index.doc.test
DELETE local.index.doc.igla
DELETE local.index.doc.cherry_car
'''

config_file = "/home/nikolaypavlychev/llm4search_dev/llm4search_dev/llm4search/src/apps/igla_pipeline_app/local.ini"
config = ConfigParser()
config.read(config_file)

log_format = config.get("logging", "format", raw=True)
logging.basicConfig(level=logging.getLevelName(config.get("logging", "level")),
                    format=log_format)

app = WebApi(host=config.get("server", "host"), port=config.getint("server", "port"), log_format=log_format,
             config_file=config_file)


def get_pipeline_config(source_code: str) -> IglaPipelineConfig:
    config_section = f"pipeline_{source_code}"
    return IglaPipelineConfig(adapter_type=IglaAdapterType(config.get(config_section, "adapter_type")),
                              splitter_type=IglaSplitterType(config.get(config_section, "splitter_type")),
                              chunk_size=config.getint(config_section, "chunk_size"),
                              chunk_separator=config.get(config_section, "chunk_separator", fallback=" "),
                              chunk_overlap=config.getint(config_section, "chunk_overlap"),
                              batch_size=config.getint(config_section, "batch_size"),
                              file_path=config.get(config_section, "file_path", fallback=None),
                              folder_path=config.get(config_section, "folder_path", fallback=None)
                              )


pipeline_configs = dict(map(lambda source_code: (source_code, get_pipeline_config(source_code)),
                            [SOURCE_CODE_TEST, SOURCE_CODE_IGLA, SOURCE_CODE_CHERRY_CAR]))

elastic_config = ElasticConfig(url=config.get("elasticsearch", "url"),
                               index_prefix=config.get("elasticsearch", "index_prefix"))
elastic_vector_config = ElasticVectorConfig(
    embeddings_type=EmbeddingsType(config.get("vector_store", "embeddings_type")),
    hugging_face_hub_api_url=None)
elastic_client = ElasticClient(elastic_config)
elastic_embedding_factory = ElasticEmbeddingFactory()
elastic_vector_store_factory = ElasticVectorStoreFactory(elastic_client, elastic_config, elastic_vector_config,
                                                         elastic_embedding_factory)

splitter_factory = IglaArticleSplitterFactory()
adapter_factory = IglaDocumentAdapterFactory(configs=pipeline_configs, splitter_factory=splitter_factory)
singleton_worker = SingletonWorker()
pipeline_controller = IglaPipelineController(
    IglaProcessor(pipeline_configs, elastic_vector_store_factory, adapter_factory), singleton_worker)
app.add_controller(pipeline_controller)

if __name__ == "__main__":
    app.run()
