import os
import sys
from multiprocessing import set_start_method

from dotenv import load_dotenv
from dotenv import dotenv_values

load_dotenv('/home/namenode/llm4search_repo/llm4search/.env')

config = dotenv_values()
sys.path.append(config['HOME'])
sys.path.append(config['SRC'])

os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "backend:native"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "garbage_collection_threshold:0.9"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "roundup_power2_divisions:[256:1,512:2,1024:4,>:8]"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:64"

import logging
from configparser import ConfigParser

from src.cores.common.elastic.clients.elastic_client import ElasticClient
from src.cores.common.elastic.configs.elastic_config import ElasticConfig
from src.cores.common.elastic.configs.elastic_vector_config import EmbeddingsType, ElasticVectorConfig
from src.cores.common.elastic.embeddings.elastic_embedding_factory import ElasticEmbeddingFactory
from src.cores.common.elastic.stores.elastic_vector_store_factory import ElasticVectorStoreFactory
from src.cores.common.web.web_api import WebApi
from src.service_modules.igla_chat_service.chat_models.chat_model_factory import ChatModelFactory
from src.service_modules.igla_chat_service.configs.igla_chat_config import ChatModelType, IglaChatConfig
from src.service_modules.igla_chat_service.controllers.igla_chat_controller import IglaChatController
from src.service_modules.igla_chat_service.services.igla_chat_service import IglaChatService

'''
Main igla pipeline application
1. http://0.0.0.0:8001 - api
2. http://0.0.0.0:8001/docs - swagger

load sources:
1. via api
curl -X 'POST' \
  'http://0.0.0.0:8001/api/v1/igla-chat/ask?question=Hello' \
  -H 'accept: application/json' \
  -d ''

2. via swagger  
http://0.0.0.0:8001/docs#/default/chat_api_v1_igla_chat_ask_post
"hello"

3. create alias local.alias.doc.igla via Kibana (http://localhost:5601/app/dev_tools#/console):
POST _aliases
{
  "actions": [
    {
      "add": {
        "indices": ["local.index.doc.test", "local.index.doc.igla", "local.index.doc.cherry_car"],
        "alias": "local.alias.doc.igla"
      }
    }
  ]
}
'''

config_file = "/home/nikolaypavlychev/llm4search_dev/llm4search_dev/llm4search/src/apps/igla_chat_app/local.ini"
config = ConfigParser()
config.read(config_file)

log_format = config.get("logging", "format", raw=True)
logging.basicConfig(level=logging.getLevelName(config.get("logging", "level")),
                    format=log_format)

app = WebApi(host=config.get("server", "host"), port=config.getint("server", "port"), log_format=log_format,
             config_file=config_file)

elastic_config = ElasticConfig(url=config.get("elasticsearch", "url"),
                               index_prefix=config.get("elasticsearch", "index_prefix"))
elastic_vector_config = ElasticVectorConfig(
    embeddings_type=EmbeddingsType(config.get("vector_store", "embeddings_type")),
    hugging_face_hub_api_url=None)
elastic_client = ElasticClient(elastic_config)
elastic_embedding_factory = ElasticEmbeddingFactory()
elastic_vector_store_factory = ElasticVectorStoreFactory(elastic_client, elastic_config, elastic_vector_config,
                                                         elastic_embedding_factory)

chat_config = IglaChatConfig(
    chat_model_type=ChatModelType(config.get("chat", "chat_model_type")),
    hugging_face_hub_api_url=config.get("chat", "hugging_face_hub_api_url", fallback=None),
    hugging_face_hub_api_token=config.get("chat", "hugging_face_hub_api_token", fallback=None),
    llm_hf_model_path=config.get("chat", "llm_hf_model_path"),
    task=config.get("chat", "task"),
    max_new_tokens=config.getint("chat", "max_new_tokens"),
    top_p=config.getfloat("chat", "top_p"),
    top_k=config.getint("chat", "top_k"),
    temperature=config.getfloat("chat", "temperature"),
    repetition_penalty=config.getfloat("chat", "repetition_penalty")
)

chat_service = IglaChatService(elastic_vector_store_factory, ChatModelFactory(chat_config))
app.add_controller(IglaChatController(chat_service))

if __name__ == "__main__":
  app.run()
  