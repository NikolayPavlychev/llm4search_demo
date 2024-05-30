from dataclasses import dataclass


@dataclass
class ElasticAliasName:
    name: str

    def __str__(self) -> str:
        return self.name


@dataclass
class ElasticAlias:
    prefix: str
    name: ElasticAliasName

    def __str__(self) -> str:
        return f"{self.prefix}.alias.doc.{self.name}"
