from typing import Protocol

from langchain_core.documents import Document


class IglaDocument(Protocol):
    source: str

    def to_document(self) -> Document:
        pass


class IglaDocumentSegment(Protocol):

    def to_document(self) -> Document:
        pass
