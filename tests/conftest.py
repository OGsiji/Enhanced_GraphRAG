import pytest
from pathlib import Path
import tempfile
import shutil
from kg_generator.config import ProcessingConfig, FalkorDBConfig


@pytest.fixture
def processing_config():
    return ProcessingConfig(
        chunk_size=500, overlap=50, max_workers=2, batch_size=2, temp_dir="test_temp"
    )


@pytest.fixture
def falkordb_config():
    return FalkorDBConfig(host="localhost", port=6379)


@pytest.fixture
def temp_pdf_dir():
    """Create a temporary directory with test PDFs"""
    temp_dir = tempfile.mkdtemp()
    pdf_dir = Path(temp_dir) / "pdfs"
    pdf_dir.mkdir()

    # Create dummy PDF files for testing
    for i in range(3):
        (pdf_dir / f"test{i}.pdf").touch()

    yield pdf_dir

    shutil.rmtree(temp_dir)
