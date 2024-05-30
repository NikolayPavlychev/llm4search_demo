from langchain_text_splitters import TextSplitter, CharacterTextSplitter

from src.service_modules.igla_pipeline_service.configs.igla_pipeline_config import IglaPipelineConfig, IglaSplitterType


class IglaArticleSplitterFactory:

    def create(self, config: IglaPipelineConfig) -> TextSplitter:
        if config.splitter_type == IglaSplitterType.CHARACTER_TEXT:
            if (
                    config.chunk_separator is None or config.chunk_size is None or config.chunk_overlap is None):
                raise ValueError(
                    "chunk_separator, chunk_size and chunk_overlap are required for character text splitter")
            else:
                return CharacterTextSplitter(separator=config.chunk_separator,
                                             chunk_size=config.chunk_size,
                                             chunk_overlap=config.chunk_overlap)
        else:
            raise ValueError(f"Unknown splitter type: {config.splitter_type}")
