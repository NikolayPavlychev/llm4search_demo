from dataclasses import dataclass
from enum import Enum
from typing import Optional


class IglaAdapterType(Enum):
    FILE = "file"
    SITE = "site"
    PDF = "pdf"


class IglaSplitterType(Enum):
    CHARACTER_TEXT = "character_text"


@dataclass
class IglaPipelineConfig:
    adapter_type: IglaAdapterType
    splitter_type: IglaSplitterType
    chunk_separator: Optional[str]
    chunk_size: Optional[int]
    chunk_overlap: Optional[int]
    batch_size: int
    file_path: Optional[str]
    folder_path: Optional[str]
