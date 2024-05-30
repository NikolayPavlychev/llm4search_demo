from abc import ABC, abstractmethod

from typing import AsyncIterator
from langchain_core.documents import Document
from langchain_text_splitters import TextSplitter
from src.cores.igla.models.igla_document import IglaDocument
from src.cores.igla.models.igla_document import IglaDocumentSegment


class IglaDocumentAdapterBase(ABC):

    def __init__(self, splitter: TextSplitter) -> None:
        self.__splitter = splitter

    async def aload_segments(self) -> AsyncIterator[IglaDocumentSegment]:
        async for doc in self._load_document():
            for segment in self.__splitter.split_documents(documents=[doc.to_document()]):
                yield self._create_document_segment(doc, segment)

    @abstractmethod
    def _create_document_segment(self, doc: IglaDocument, segment: Document) -> IglaDocumentSegment:
        pass

    @abstractmethod
    async def _load_document(self) -> AsyncIterator[IglaDocument]:
        pass
