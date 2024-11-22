# examples/basic_usage.py
import os
from pathlib import Path
from dotenv import load_dotenv
from kg_generator.config import ProcessingConfig, FalkorDBConfig
from kg_generator.knowledge_graph.generator import KnowledgeGraphGenerator
from kg_generator.utils.logging import setup_logging


def main():
    # Set up logging
    setup_logging()

    # Load environment variables
    load_dotenv()

    # Verify Google API key
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY not found in environment variables")

    # Initialize configurations
    processing_config = ProcessingConfig(
        chunk_size=1500,
        overlap=150,
        max_workers=4,
        batch_size=3,
        temp_dir="temp_processed",
    )

    falkordb_config = FalkorDBConfig(
        host=os.getenv("FALKORDB_HOST", "localhost"),
        port=int(os.getenv("FALKORDB_PORT", "6379")),
    )

    # Initialize KG Generator
    kg_generator = KnowledgeGraphGenerator(
        model_name="gemini-1.5-flash-001",
        falkordb_config=falkordb_config,
        processing_config=processing_config,
    )

    # Check for initial PDFs
    initial_pdf_dir = Path("/app/initial_pdfs")
    if not any(initial_pdf_dir.glob("*.pdf")):
        print(
            "No PDF files found in /app/initial_pdfs. Please add some initial PDF files."
        )
        return

    # Generate initial knowledge graph
    print("Generating initial knowledge graph...")
    kg_generator.generate_knowledge_graph(
        pdf_dir=initial_pdf_dir, kg_name="pdf_knowledge_graph"
    )

    # Check for additional PDFs
    additional_pdf_dir = Path("/app/additional_pdfs")
    if any(additional_pdf_dir.glob("*.pdf")):
        print("Processing additional PDFs...")
        kg_generator.update_knowledge_graph(additional_pdf_dir)
    else:
        print("No additional PDFs found in /app/additional_pdfs")

    # Example query
    response = kg_generator.query_knowledge_graph(
        "What are the main topics discussed in the documents?"
    )
    print(f"Query response: {response}")


if __name__ == "__main__":
    main()
