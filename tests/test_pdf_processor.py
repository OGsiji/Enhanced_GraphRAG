
# tests/test_pdf_processor.py
import pytest
from pathlib import Path
from kg_generator.processors.pdf_processor import PDFProcessor
from kg_generator.exceptions import PDFProcessingError
from unittest.mock import patch, MagicMock

def test_pdf_processor_initialization(processing_config):
    processor = PDFProcessor(processing_config)
    assert processor.config == processing_config
    assert Path(processing_config.temp_dir).exists()

@patch('kg_generator.processors.pdf_processor.partition_pdf')
def test_extract_text_from_pdf_success(mock_partition, processing_config):
    mock_partition.return_value = [MagicMock(str=lambda: "test content")]
    
    processor = PDFProcessor(processing_config)
    result = processor.extract_text_from_pdf("test.pdf")
    
    assert result == "test content"
    mock_partition.assert_called_once()

@patch('kg_generator.processors.pdf_processor.partition_pdf')
def test_extract_text_from_pdf_failure(mock_partition, processing_config):
    mock_partition.side_effect = Exception("PDF extraction failed")
    
    processor = PDFProcessor(processing_config)
    with pytest.raises(PDFProcessingError):
        processor.extract_text_from_pdf("test.pdf")

# def test_process_pdf_batch(temp_pdf_dir, processing_config):
#     processor = PDFProcessor(processing_config)
#     pdf_files = list(temp_pdf_dir.glob("*.pdf"))
    
#     with patch.object(processor, 