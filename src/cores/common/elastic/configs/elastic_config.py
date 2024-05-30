from dataclasses import dataclass


@dataclass
class ElasticConfig:
    url: str
    index_prefix: str
