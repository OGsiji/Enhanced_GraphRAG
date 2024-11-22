import random
import json
from pathlib import Path
from typing import List, Union
import logging
import os
from ..config import ProcessingConfig, FalkorDBConfig
from ..exceptions import KnowledgeGraphError
from ..processors.pdf_processor import PDFProcessor
from graphrag_sdk.source import Source
from graphrag_sdk import KnowledgeGraph, Ontology
from graphrag_sdk.models.gemini import GeminiGenerativeModel
from graphrag_sdk.model_config import KnowledgeGraphModelConfig

logger = logging.getLogger(__name__)



class KnowledgeGraphGenerator:
    """Enhanced Knowledge Graph Generator with correct Source handling"""
    
    def __init__(
        self,
        model_name: str = "gemini-1.5-flash-001",
        falkordb_config: FalkorDBConfig = FalkorDBConfig(),
        processing_config: ProcessingConfig = ProcessingConfig()
    ):
        self.model = GeminiGenerativeModel(model_name=model_name)
        self.falkordb_config = falkordb_config
        self.config = processing_config
        self.kg = None
        self.pdf_processor = PDFProcessor(processing_config)

    def generate_knowledge_graph(
        self,
        pdf_dir: Union[str, Path],
        kg_name: str
    ) -> None:
        """Generate knowledge graph from PDF files"""
        try:
            pdf_files = list(Path(pdf_dir).glob("*.pdf"))
            if not pdf_files:
                raise KnowledgeGraphError("No PDF files found in directory")
                
            all_sources = []
            for i in range(0, len(pdf_files), self.config.batch_size):
                batch = pdf_files[i:i + self.config.batch_size]
                sources = self.pdf_processor.process_pdf_batch(batch)
                all_sources.extend(sources)
                
            if not all_sources:
                raise KnowledgeGraphError("No valid sources generated from PDFs")
            
            print(all_sources)
                
            ontology = self._generate_ontology(all_sources, kg_name)
            self._create_knowledge_graph(all_sources, ontology, kg_name)
            
        except Exception as e:
            logger.error(f"Error generating knowledge graph: {str(e)}")
            raise KnowledgeGraphError(f"Failed to generate knowledge graph: {str(e)}")

    def _generate_ontology(self, sources: List[Source], kg_name: str) -> Ontology:
        """Generate optimized ontology from sources"""
        try:
            sample_size = max(1, round(len(sources) * 0.1))
            sampled_sources = random.sample(sources, sample_size)
            logger.info(f"Using {sample_size} sources for ontology generation")

            boundaries = """
                    Extract key entities and relationships from the documents.
                    Focus on main concepts and their connections.
                    Avoid creating entities for minor details that can be attributes.
                    Each entity should have:
                    - A clear, unique identifier
                    - At least one relationship to another entity
                    - Specific attributes that define its properties
                """


            ontology = Ontology.from_sources(
                sources=sampled_sources,
                boundaries=boundaries,
                model=self.model
            )
            
            output_path = f"{kg_name}_ontology.json"
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(ontology.to_json(), f, indent=2)
            logger.info(f"Saved ontology to {output_path}")
            
            return ontology
            
        except Exception as e:
            logger.error(f"Failed to generate ontology: {str(e)}")
            raise KnowledgeGraphError(f"Failed to generate ontology: {str(e)}")

    def _create_knowledge_graph(
        self,
        sources: List[Source],
        ontology: Ontology,
        kg_name: str
    ) -> None:
        """Create and populate knowledge graph"""
        try:
            self.kg = KnowledgeGraph(
                name=kg_name,
                model_config=KnowledgeGraphModelConfig.with_model(
                    self.model,
                ),
                ontology=ontology,
                host=self.falkordb_config.host,
                port=self.falkordb_config.port,
                username=self.falkordb_config.username,
                password=self.falkordb_config.password
            )
            
            for i in range(0, len(sources), self.config.batch_size):
                batch = sources[i:i + self.config.batch_size]
                self.kg.process_sources(batch)
                logger.info(f"Processed batch {i//self.config.batch_size + 1}")
                
        except Exception as e:
            logger.error(f"Error creating knowledge graph: {str(e)}")
            raise KnowledgeGraphError(f"Failed to create knowledge graph: {str(e)}")
        
    def update_knowledge_graph(self, sources: List[Source]) -> None:
        """Update existing knowledge graph with new text files"""
        if not self.kg:
            raise ValueError("No knowledge graph exists. Please generate one first.")

        try:
            # Create Source objects from new text files
            new_sources = [
                Source(os.path.join(sources, file))
                for file in os.listdir(sources)
            ]

            if not new_sources:
                raise ValueError("No text sources found for update")
            
            for i in range(0, len(new_sources), self.config.batch_size):
                batch = new_sources[i:i + self.config.batch_size]
                self.kg.process_sources(batch)
                logger.info(f"Processed batch {i//self.config.batch_size + 1}")

        except Exception as e:
            logger.error(f"Error updating knowledge graph: {str(e)}")
            raise

    def query_knowledge_graph(self, query: str) -> str:
        """Query the knowledge graph"""
        if not self.kg:
            raise ValueError("No knowledge graph exists. Please generate one first.")
        
        chat = self.kg.chat_session()
        return chat.send_message(query)