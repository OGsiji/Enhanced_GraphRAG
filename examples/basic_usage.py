import streamlit as st
import os
from pathlib import Path
import asyncio
import tempfile
from dotenv import load_dotenv
from kg_generator.config import ProcessingConfig, FalkorDBConfig, LinkConfig
from kg_generator.knowledge_graph.generator import KnowledgeGraphGenerator
from kg_generator.utils.logging import setup_logging
from kg_generator.url import URL
import logging

# Setup logging and load environment variables
setup_logging()
logger = logging.getLogger(__name__)
load_dotenv()

# Initialize Streamlit configuration
st.set_page_config(page_title="Knowledge Graph Generator", layout="wide")


def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        "kg_generator": None,
        "model_name": "gemini-2.0-flash-exp",
        "chunk_size": 1500,
        "overlap": 150,
        "max_workers": 4,
        "batch_size": 3,
        "use_url": False,
        "use_pdf": True,
        "url_list": URL(),
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def create_kg_generator():
    """Create and return a new KG Generator instance"""
    try:
        if not os.getenv("GOOGLE_API_KEY"):
            st.error("GOOGLE_API_KEY not found in environment variables!")
            return None

        processing_config = ProcessingConfig(
            chunk_size=st.session_state.chunk_size,
            overlap=st.session_state.overlap,
            max_workers=st.session_state.max_workers,
            batch_size=st.session_state.batch_size,
            temp_dir="temp_processed",
        )

        falkordb_config = FalkorDBConfig(
            host=os.getenv("FALKORDB_HOST", "localhost"),
            port=int(os.getenv("FALKORDB_PORT", "6379")),
            username=os.getenv("FALKORDB_USERNAME", ""),
            password=os.getenv("FALKORDB_PASSWORD", ""),
        )

        link_config = LinkConfig(
            url=st.session_state.use_url, pdf=st.session_state.use_pdf
        )

        kg_generator = KnowledgeGraphGenerator(
            model_name=st.session_state.model_name,
            falkordb_config=falkordb_config,
            processing_config=processing_config,
            link_config=link_config,
        )

        # Set URL list if URL processing is enabled
        if st.session_state.use_url:
            kg_generator.url_list = st.session_state.url_list

        return kg_generator

    except Exception as e:
        st.error(f"Error creating KG Generator: {str(e)}")
        logger.error(f"KG Generator creation failed: {str(e)}")
        return None


def render_sidebar():
    """Render sidebar configuration"""
    with st.sidebar:
        st.header("Configuration")

        # Model settings
        st.subheader("Model Settings")
        st.session_state.model_name = st.text_input(
            "Model Name", value=st.session_state.model_name
        )

        # Processing settings
        st.subheader("Processing Settings")
        st.session_state.chunk_size = st.number_input(
            "Chunk Size", value=st.session_state.chunk_size, min_value=100
        )
        st.session_state.overlap = st.number_input(
            "Overlap", value=st.session_state.overlap, min_value=0
        )
        st.session_state.max_workers = st.number_input(
            "Max Workers", value=st.session_state.max_workers, min_value=1
        )
        st.session_state.batch_size = st.number_input(
            "Batch Size", value=st.session_state.batch_size, min_value=1
        )

        # URL Management
        st.subheader("URL Management")
        new_url = st.text_input("Add New URL")
        if st.button("Add URL") and new_url:
            st.session_state.url_list.add_url(new_url)
            st.success(f"Added URL: {new_url}")

        if st.session_state.url_list.urls:
            st.subheader("Current URLs")
            for key, url in st.session_state.url_list.urls.items():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.text(f"{key}: {url}")
                with col2:
                    if st.button("Remove", key=f"remove_{key}"):
                        st.session_state.url_list.remove_url(key)
                        st.rerun()

            if st.button("Clear All URLs"):
                st.session_state.url_list.clear_urls()
                st.rerun()

        # Source settings
        st.subheader("Source Settings")
        st.session_state.use_url = st.checkbox(
            "Process URLs", value=st.session_state.use_url
        )
        st.session_state.use_pdf = st.checkbox(
            "Process PDFs", value=st.session_state.use_pdf
        )

        # Initialize/Reset button
        if st.button("Initialize/Reset KG Generator"):
            st.session_state.kg_generator = create_kg_generator()
            if st.session_state.kg_generator:
                st.success("KG Generator initialized successfully!")


async def generate_knowledge_graph(pdf_dir, kg_name):
    """Generate knowledge graph with progress tracking"""
    try:
        with st.spinner("Generating Knowledge Graph..."):
            await st.session_state.kg_generator.generate_knowledge_graph(
                pdf_dir, kg_name
            )
        st.success("Knowledge Graph generated successfully!")
    except Exception as e:
        st.error(f"Error generating Knowledge Graph: {str(e)}")
        logger.error(f"Knowledge graph generation failed: {str(e)}")


def render_main_content():
    """Render main content area"""
    if st.session_state.kg_generator is None:
        st.warning("Please initialize the KG Generator using the sidebar first!")
        return

    # URL Preview
    if st.session_state.use_url and st.session_state.url_list.urls:
        st.header("URL Processing Preview")
        for url in st.session_state.url_list.get_all_urls():
            st.write(f"- {url}")

    # File upload and KG generation
    st.header("Generate Knowledge Graph")
    kg_name = st.text_input("Knowledge Graph Name", value="new_graph")
    uploaded_files = st.file_uploader(
        "Upload PDF Files", type=["pdf"], accept_multiple_files=True
    )

    if uploaded_files and st.button("Generate Knowledge Graph"):
        temp_dir = Path(tempfile.mkdtemp())
        for uploaded_file in uploaded_files:
            with open(temp_dir / uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getvalue())
        asyncio.run(generate_knowledge_graph(temp_dir, kg_name))

    # Update existing KG
    st.header("Update Existing Knowledge Graph")
    update_files = st.file_uploader(
        "Upload Additional PDF Files",
        type=["pdf"],
        accept_multiple_files=True,
        key="update",
    )

    if update_files and st.button("Update Knowledge Graph"):
        if not st.session_state.kg_generator.kg:
            st.error("No existing Knowledge Graph found. Please generate one first!")
        else:
            temp_dir = Path(tempfile.mkdtemp())
            for uploaded_file in update_files:
                with open(temp_dir / uploaded_file.name, "wb") as f:
                    f.write(uploaded_file.getvalue())
            try:
                with st.spinner("Updating Knowledge Graph..."):
                    st.session_state.kg_generator.update_knowledge_graph(temp_dir)
                st.success("Knowledge Graph updated successfully!")
            except Exception as e:
                st.error(f"Error updating Knowledge Graph: {str(e)}")
                logger.error(f"Knowledge graph update failed: {str(e)}")

    # Query interface
    st.header("Query Knowledge Graph")
    query = st.text_area("Enter your query")

    if query and st.button("Send Query"):
        if not st.session_state.kg_generator.kg and not st.session_state.use_url:
            st.error("No Knowledge Graph exists. Please generate one first!")
        else:
            try:
                with st.spinner("Processing query..."):
                    response = st.session_state.kg_generator.query_knowledge_graph(
                        query
                    )
                st.subheader("Response:")
                st.write(response)
            except Exception as e:
                st.error(f"Error processing query: {str(e)}")
                logger.error(f"Query processing failed: {str(e)}")


def main():
    st.title("Knowledge Graph Generator")
    init_session_state()
    render_sidebar()
    render_main_content()


if __name__ == "__main__":
    main()
