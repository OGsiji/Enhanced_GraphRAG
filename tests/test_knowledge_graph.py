import pytest
import os
from unittest.mock import MagicMock, patch
import logging
from kg_generator.knowledge_graph.generator import KnowledgeGraphGenerator
from dotenv import load_dotenv


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


def test_knowledge_graph_initialization(processing_config, falkordb_config):
    generator = KnowledgeGraphGenerator(
        model_name="gemini-1.5-flash-001",
        falkordb_config=falkordb_config,
        processing_config=processing_config,
    )

    assert generator.model is not None
    assert os.getenv("FALKORDB_HOST") == falkordb_config.host
    assert os.getenv("FALKORDB_PORT") == falkordb_config.port


@patch("kg_generator.knowledge_graph.generator.Source")
@patch("kg_generator.knowledge_graph.generator.Ontology")
@patch("kg_generator.knowledge_graph.generator.KnowledgeGraph")
def test_generate_knowledge_graph_success(
    mock_kg,
    mock_ontology,
    mock_source,
    temp_pdf_dir,
    processing_config,
    falkordb_config,
):
    generator = KnowledgeGraphGenerator(
        model_name="gemini-1.5-flash-001",
        falkordb_config=falkordb_config,
        processing_config=processing_config,
    )

    with patch.object(
        generator.pdf_processor, "process_pdf_batch"
    ) as mock_process_batch:
        # Mock the process_pdf_batch to return mock sources
        mock_source_instances = [MagicMock(), MagicMock()]
        mock_process_batch.return_value = mock_source_instances

        # Mock the Ontology's behavior
        mock_ontology_instance = mock_ontology.return_value
        mock_ontology_instance.to_json.return_value = {
            "entities": [{"id": "entity1"}],
            "relationships": [{"source": "entity1", "target": "entity2"}],
        }

        # Run the generator
        generator.generate_knowledge_graph(temp_pdf_dir, "test_kg")

        # Assertions
        assert mock_process_batch.called
        mock_ontology.from_sources.assert_called_once_with(
            sources=ANY, boundaries=ANY, model=generator.model
        )
        mock_ontology_instance.to_json.assert_called_once()


def test_query_knowledge_graph_without_initialization(
    processing_config, falkordb_config
):
    generator = KnowledgeGraphGenerator(
        model_name="gemini-1.5-flash-001",
        falkordb_config=falkordb_config,
        processing_config=processing_config,
    )

    with pytest.raises(ValueError, match="No knowledge graph exists"):
        generator.query_knowledge_graph("Test query")
