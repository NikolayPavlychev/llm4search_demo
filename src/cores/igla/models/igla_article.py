from dataclasses import dataclass

from langchain_core.documents import Document


@dataclass
class IglaArticle:
    source_code: str
    content: str
    metadata: dict

    def to_document(self) -> Document:
        self.metadata["source_code"] = self.source_code
        return Document(page_content=self.content, metadata=self.metadata)


@dataclass
class IglaArticleSegment:
    article: IglaArticle
    content: str
    metadata: dict

    def to_document(self) -> Document:
        return Document(page_content=self.content, metadata=self.metadata)
