import logging
from typing import Optional

def setup_logging(level: int = logging.INFO, log_file: Optional[str] = None) -> None:
    """Configure logging with optional file output"""
    format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        level=level,
        format=format_str,
        handlers=[
            logging.StreamHandler(),
            *([] if log_file is None else [logging.FileHandler(log_file)])
        ]
    )