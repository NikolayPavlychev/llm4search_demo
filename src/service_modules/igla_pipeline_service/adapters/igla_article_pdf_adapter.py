from typing import AsyncIterator

from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_core.documents import Document
from langchain_text_splitters import TextSplitter

from src.cores.igla.models.igla_article import IglaArticle, IglaArticleSegment
from src.cores.igla.models.source_code import SOURCE_CODE_IGLA
from src.service_modules.igla_pipeline_service.adapters.igla_document_adapter_base import IglaDocumentAdapterBase
from src.service_modules.igla_pipeline_service.splitters.igla_article_splitter_factory import IglaArticleSplitterFactory


class IglaArticlePdfAdapter(IglaDocumentAdapterBase):
    def __init__(self, pdf_path: str, splitter: TextSplitter):
        super().__init__(splitter=splitter)
        self.__pdf_path = pdf_path
        self.__loader = PyPDFDirectoryLoader(path=pdf_path, recursive=True)

    def _create_document_segment(self, doc: IglaArticle, segment: Document) -> IglaArticleSegment:
        return IglaArticleSegment(
            article=doc,
            content=segment.page_content,
            metadata=segment.metadata
        )

    async def _load_document(self) -> AsyncIterator[IglaArticle]:
        async for article in self.__loader.alazy_load():
            yield IglaArticle(
                source_code=SOURCE_CODE_IGLA,
                metadata=article.metadata,
                content=article.page_content
            )
