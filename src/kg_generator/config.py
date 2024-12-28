from dataclasses import dataclass
from typing import Optional


@dataclass
class ProcessingConfig:
    """Configuration for PDF processing"""

    chunk_size: int = 1000
    overlap: int = 100
    max_workers: int = 4
    batch_size: int = 3
    temp_dir: str = "temp_processed"


@dataclass
class LinkConfig:
    """Add link urls for processing"""

    url: str = True
    pdf: bool = True


@dataclass
class FalkorDBConfig:
    """Configuration for FalkorDB connection"""

    host: str = "localhost"
    port: int = 6379
    username: Optional[str] = None
    password: Optional[str] = None
