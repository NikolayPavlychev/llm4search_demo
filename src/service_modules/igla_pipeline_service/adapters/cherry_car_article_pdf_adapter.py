from typing import AsyncIterator
from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_core.documents import Document
from langchain_text_splitters import TextSplitter
from src.cores.igla.models.cherry_car_article import CherryCarArticle, CherryCarArticleSegment
from src.cores.igla.models.source_code import SOURCE_CODE_CHERRY_CAR
from src.service_modules.igla_pipeline_service.adapters.igla_document_adapter_base import IglaDocumentAdapterBase


class CherryCarArticlePdfAdapter(IglaDocumentAdapterBase):
    def __init__(self, pdf_path: str, splitter: TextSplitter):
        super().__init__(splitter=splitter)
        self.__loader = PyPDFDirectoryLoader(path=pdf_path, recursive=True)

    def _create_document_segment(self, doc: CherryCarArticle, segment: Document) -> CherryCarArticleSegment:
        return CherryCarArticleSegment(
            article=doc,
            content=segment.page_content,
            metadata=segment.metadata
        )

    async def _load_document(self) -> AsyncIterator[CherryCarArticle]:
        async for article in self.__loader.alazy_load():
            yield CherryCarArticle(
                source_code=SOURCE_CODE_CHERRY_CAR,
                metadata=article.metadata,
                content=article.page_content
            )
