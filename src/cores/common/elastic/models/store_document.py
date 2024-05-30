from langchain_core.documents import Document
from typing import Protocol


class StoreDocument(Protocol):

    def to_document(self) -> Document:
        pass
