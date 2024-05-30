from typing import Dict

from src.cores.igla.models.source_code import SOURCE_CODE_TEST, SOURCE_CODE_IGLA, SOURCE_CODE_CHERRY_CAR
from src.service_modules.igla_pipeline_service.adapters.cherry_car_article_pdf_adapter import CherryCarArticlePdfAdapter
from src.service_modules.igla_pipeline_service.adapters.igla_document_adapter_base import IglaDocumentAdapterBase
from src.service_modules.igla_pipeline_service.adapters.igla_article_test_file_adapter import IglaArticleTestFileAdapter
from src.service_modules.igla_pipeline_service.adapters.igla_article_pdf_adapter import IglaArticlePdfAdapter
from src.service_modules.igla_pipeline_service.configs.igla_pipeline_config import IglaAdapterType, IglaPipelineConfig
from src.service_modules.igla_pipeline_service.splitters.igla_article_splitter_factory import IglaArticleSplitterFactory


class IglaDocumentAdapterFactory:
    def __init__(self, configs: Dict[str, IglaPipelineConfig], splitter_factory: IglaArticleSplitterFactory) -> None:
        self.__configs = configs
        self.__splitter_factory = splitter_factory

    def create(self, source_code: str) -> IglaDocumentAdapterBase:
        if (source_code not in self.__configs):
            raise ValueError(f"Unknown source code: {source_code}")

        config = self.__configs.get(source_code)
        splitter = self.__splitter_factory.create(config)

        if source_code == SOURCE_CODE_TEST:
            if config.file_path is None:
                raise ValueError("File path is required for file adapter")
            else:
                return IglaArticleTestFileAdapter(file_path=config.file_path,
                                                  splitter=splitter)
        elif source_code == SOURCE_CODE_CHERRY_CAR:
            if config.folder_path is None:
                raise ValueError("Folder path is required for pdf adapter")
            else:
                return CherryCarArticlePdfAdapter(pdf_path=config.folder_path,
                                                  splitter=splitter)
        elif source_code == SOURCE_CODE_IGLA:
            if config.folder_path is None:
                raise ValueError("Folder path is required for pdf adapter")
            else:
                return IglaArticlePdfAdapter(pdf_path=config.folder_path,
                                             splitter=splitter)
        else:
            raise ValueError(f"Unknown adapter type: {source_code}")
