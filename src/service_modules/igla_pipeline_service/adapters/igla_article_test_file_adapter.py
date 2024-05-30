from langchain_core.documents import Document
from langchain_text_splitters import TextSplitter

from src.cores.igla.models.source_code import SOURCE_CODE_TEST
from src.cores.igla.models.test_article import TestArticle, TestArticleSegment
from src.service_modules.igla_pipeline_service.adapters.igla_document_adapter_base import IglaDocumentAdapterBase
from typing import AsyncIterator
from langchain_community.document_loaders.text import TextLoader


class IglaArticleTestFileAdapter(IglaDocumentAdapterBase):

    def __init__(self, file_path: str, splitter: TextSplitter) -> None:
        super().__init__(splitter=splitter)
        self.__loader = TextLoader(file_path)

    def _create_document_segment(self, doc: TestArticle, segment: Document) -> TestArticleSegment:
        return TestArticleSegment(
            article=doc,
            content=segment.page_content,
            metadata=segment.metadata
        )

    async def _load_document(self) -> AsyncIterator[TestArticle]:
        async for article in self.__loader.alazy_load():
            yield TestArticle(
                source_code=SOURCE_CODE_TEST,
                metadata=article.metadata,
                content=article.page_content
            )
