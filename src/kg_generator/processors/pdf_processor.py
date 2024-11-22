import os
from pathlib import Path
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from ..config import ProcessingConfig
from ..exceptions import PDFProcessingError
from unstructured.partition.pdf import partition_pdf
from graphrag_sdk.source import Source

logger = logging.getLogger(__name__)


class PDFProcessor:
    """Enhanced PDF processor with parallel processing capabilities"""

    def __init__(self, config: ProcessingConfig):
        self.config = config
        os.makedirs(self.config.temp_dir, exist_ok=True)

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from a PDF file"""
        try:
            elements = partition_pdf(
                filename=pdf_path,
                strategy="fast",
                includes_metadata=True,
                include_page_breaks=True,
            )
            return "\n".join([str(element) for element in elements])
        except Exception as e:
            logger.error(f"Error extracting content from PDF {pdf_path}: {str(e)}")
            raise PDFProcessingError(f"Failed to extract text: {str(e)}")

    def _process_single_pdf(self, pdf_file: Path) -> Optional[str]:
        """Process a single PDF file and return its output path"""
        try:
            text_content = self.extract_text_from_pdf(str(pdf_file))
            output_file = os.path.join(self.config.temp_dir, f"{pdf_file.stem}.txt")

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(text_content)

            logger.info(f"Processed {pdf_file.name} -> {output_file}")
            return output_file

        except Exception as e:
            logger.error(f"Failed to process {pdf_file.name}: {str(e)}")
            return None

    def process_pdf_batch(self, pdf_files: List[Path]) -> List[Source]:
        """Process a batch of PDFs in parallel and return Source objects"""
        sources = []

        with ThreadPoolExecutor(max_workers=self.config.max_workers) as executor:
            future_to_pdf = {
                executor.submit(self._process_single_pdf, pdf_file): pdf_file
                for pdf_file in pdf_files
            }

            for future in as_completed(future_to_pdf):
                pdf_file = future_to_pdf[future]
                try:
                    output_path = future.result()
                    if output_path:
                        sources.append(Source(output_path))
                        logger.info(f"Created Source object for {pdf_file.name}")
                except Exception as e:
                    logger.error(f"Error creating Source for {pdf_file.name}: {str(e)}")

        return sources
