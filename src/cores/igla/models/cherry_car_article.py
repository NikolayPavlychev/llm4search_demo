from dataclasses import dataclass

from langchain_core.documents import Document


@dataclass
class CherryCarArticle:
    source_code: str
    content: str
    metadata: dict

    def to_document(self) -> Document:
        self.metadata["source_code"] = self.source_code
        return Document(page_content=self.content, metadata=self.metadata)


@dataclass
class CherryCarArticleSegment:
    article: CherryCarArticle
    content: str
    metadata: dict

    def to_document(self) -> Document:
        return Document(page_content=self.content, metadata=self.metadata)
