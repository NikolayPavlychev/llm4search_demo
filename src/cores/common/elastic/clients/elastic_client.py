from elasticsearch import Elasticsearch

from src.cores.common.elastic.configs.elastic_config import ElasticConfig


class ElasticClient:
    elastic: Elasticsearch

    def __init__(self, config: ElasticConfig) -> None:
        self.elastic = Elasticsearch(config.url)
