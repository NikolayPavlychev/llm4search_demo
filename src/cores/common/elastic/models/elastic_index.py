from dataclasses import dataclass


@dataclass
class ElasticIndexName:
    name: str

    def __str__(self) -> str:
        return self.name


@dataclass
class ElasticIndex:
    prefix: str
    name: ElasticIndexName

    def __str__(self) -> str:
        return f"{self.prefix}.index.doc.{self.name}"
