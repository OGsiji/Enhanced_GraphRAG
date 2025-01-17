# # # examples/basic_usage.py
# # import os
# # from pathlib import Path
# # import asyncio
# # from dotenv import load_dotenv
# # from kg_generator.config import ProcessingConfig, FalkorDBConfig
# # from kg_generator.knowledge_graph.generator import KnowledgeGraphGenerator
# # from kg_generator.utils.logging import setup_logging


# # async def main():
# #     # Set up logging
# #     setup_logging()

# #     # Load environment variables
# #     load_dotenv()

# #     # Verify Google API key
# #     if not os.getenv("GOOGLE_API_KEY"):
# #         raise ValueError("GOOGLE_API_KEY not found in environment variables")

# #     # Initialize configurations
# #     processing_config = ProcessingConfig(
# #         chunk_size=1500,
# #         overlap=150,
# #         max_workers=4,
# #         batch_size=3,
# #         temp_dir="temp_processed",
# #     )

# #     falkordb_config = FalkorDBConfig(
# #         host=os.getenv("FALKORDB_HOST", "localhost"),
# #         port=int(os.getenv("FALKORDB_PORT", "6379")),
# #     )

# #     # Initialize KG Generator
# #     kg_generator = KnowledgeGraphGenerator(
# #         model_name="gemini-1.5-flash-001",
# #         falkordb_config=falkordb_config,
# #         processing_config=processing_config,
# #     )

# #     # Check for initial PDFs
# #     initial_pdf_dir = Path("/app/initial_pdfs")
# #     if not any(initial_pdf_dir.glob("*.pdf")):
# #         print(
# #             "No PDF files found in /app/initial_pdfs. Please add some initial PDF files."
# #         )
# #         return

# #     # Generate initial knowledge graph
# #     print("Generating initial knowledge graph...")
# #     await kg_generator.generate_knowledge_graph(
# #         pdf_dir=initial_pdf_dir, kg_name="new_graph"
# #     )

# #     # Check for additional PDFs
# #     additional_pdf_dir = Path("/app/additional_pdfs")
# #     if any(additional_pdf_dir.glob("*.pdf")):
# #         print("Processing additional PDFs...")
# #         kg_generator.update_knowledge_graph(additional_pdf_dir)
# #     else:
# #         print("No additional PDFs found in /app/additional_pdfs")

# #     # Example query
# #     response = kg_generator.query_knowledge_graph(
# #         "Answer random questions within the knowledge graph"
# #     )
# #     print(f"Query response: {response}")


# # if __name__ == "__main__":
# #     asyncio.run(main())


# import streamlit as st
# import os
# from pathlib import Path
# import asyncio
# import tempfile
# from dotenv import load_dotenv
# from kg_generator.config import ProcessingConfig, FalkorDBConfig, LinkConfig
# from kg_generator.knowledge_graph.generator import KnowledgeGraphGenerator
# from kg_generator.utils.logging import setup_logging
# import logging
# from .url import URL

# # Setup logging
# setup_logging()
# logger = logging.getLogger(__name__)

# # Load environment variables
# load_dotenv()

# def initialize_url_list():
#     """Initialize URL list in session state"""
#     if 'url_list' not in st.session_state:
#         st.session_state.url_list = URL()

# # Streamlit config and session state initialization
# st.set_page_config(page_title="Knowledge Graph Generator", layout="wide")

# if 'kg_generator' not in st.session_state:
#     st.session_state.kg_generator = None

# def initialize_kg_generator():
#     """Initialize the Knowledge Graph Generator with configurations"""
#     try:
#         if not os.getenv("GOOGLE_API_KEY"):
#             st.error("GOOGLE_API_KEY not found in environment variables!")
#             return None

#         # Initialize URL list
#         initialize_url_list()

#         processing_config = ProcessingConfig(
#             chunk_size=st.session_state.chunk_size,
#             overlap=st.session_state.overlap,
#             max_workers=st.session_state.max_workers,
#             batch_size=st.session_state.batch_size,
#             temp_dir="temp_processed"
#         )

#         falkordb_config = FalkorDBConfig(
#             host=os.getenv("FALKORDB_HOST", "localhost"),
#             port=int(os.getenv("FALKORDB_PORT", "6379")),
#             username=os.getenv("FALKORDB_USERNAME", ""),
#             password=os.getenv("FALKORDB_PASSWORD", "")
#         )

#         link_config = LinkConfig(
#             url=st.session_state.use_url,
#             pdf=st.session_state.use_pdf
#         )

#         return KnowledgeGraphGenerator(
#             model_name=st.session_state.model_name,
#             falkordb_config=falkordb_config,
#             processing_config=processing_config,
#             link_config=link_config
#         )
#     except Exception as e:
#         st.error(f"Error initializing KG Generator: {str(e)}")
#         return None

# def save_uploaded_files(uploaded_files):
#     """Save uploaded files to a temporary directory"""
#     if not uploaded_files:
#         return None

#     temp_dir = Path(tempfile.mkdtemp())
#     for uploaded_file in uploaded_files:
#         file_path = temp_dir / uploaded_file.name
#         with open(file_path, 'wb') as f:
#             f.write(uploaded_file.getvalue())
#     return temp_dir

# async def generate_kg(pdf_dir, kg_name):
#     """Generate knowledge graph from uploaded PDFs"""
#     try:
#         with st.spinner('Generating Knowledge Graph...'):
#             await st.session_state.kg_generator.generate_knowledge_graph(pdf_dir, kg_name)
#         st.success('Knowledge Graph generated successfully!')
#     except Exception as e:
#         st.error(f"Error generating Knowledge Graph: {str(e)}")

# def main():
#     st.title("Knowledge Graph Generator")

#     # Initialize URL list
#     initialize_url_list()


#     # Sidebar configurations
#     with st.sidebar:
#         st.header("Configuration")

#         # Model settings
#         st.subheader("Model Settings")
#         if 'model_name' not in st.session_state:
#             st.session_state.model_name = "gemini-2.0-flash-exp"
#         st.session_state.model_name = st.text_input("Model Name", value=st.session_state.model_name)

#         # Processing settings
#         st.subheader("Processing Settings")
#         if 'chunk_size' not in st.session_state:
#             st.session_state.chunk_size = 1500
#         st.session_state.chunk_size = st.number_input("Chunk Size", value=st.session_state.chunk_size, min_value=100)

#         if 'overlap' not in st.session_state:
#             st.session_state.overlap = 150
#         st.session_state.overlap = st.number_input("Overlap", value=st.session_state.overlap, min_value=0)

#         if 'max_workers' not in st.session_state:
#             st.session_state.max_workers = 4
#         st.session_state.max_workers = st.number_input("Max Workers", value=st.session_state.max_workers, min_value=1)

#         if 'batch_size' not in st.session_state:
#             st.session_state.batch_size = 3
#         st.session_state.batch_size = st.number_input("Batch Size", value=st.session_state.batch_size, min_value=1)

#         # URL Management Section in Sidebar
#         st.subheader("URL Management")

#         # Add new URL
#         new_url = st.text_input("Add New URL")
#         if st.button("Add URL"):
#             if new_url:
#                 st.session_state.url_list.add_url(new_url)
#                 st.success(f"Added URL: {new_url}")
#             else:
#                 st.warning("Please enter a URL")

#         # Display and manage existing URLs
#         st.subheader("Current URLs")
#         urls = st.session_state.url_list.urls
#         for key, url in urls.items():
#             col1, col2 = st.columns([3, 1])
#             with col1:
#                 st.text(f"{key}: {url}")
#             with col2:
#                 if st.button("Remove", key=f"remove_{key}"):
#                     st.session_state.url_list.remove_url(key)
#                     st.experimental_rerun()

#         # Clear all URLs
#         if st.button("Clear All URLs"):
#             st.session_state.url_list.clear_urls()
#             st.experimental_rerun()


#         # Source settings
#         st.subheader("Source Settings")
#         if 'use_url' not in st.session_state:
#             st.session_state.use_url = False
#         st.session_state.use_url = st.checkbox("Process URLs", value=st.session_state.use_url)

#         if 'use_pdf' not in st.session_state:
#             st.session_state.use_pdf = True
#         st.session_state.use_pdf = st.checkbox("Process PDFs", value=st.session_state.use_pdf)

#         if 'kg_generator' not in st.session_state or st.session_state.kg_generator is None:
#             if st.session_state.use_url:
#                 st.session_state.kg_generator = initialize_kg_generator()
#                 if st.session_state.kg_generator:
#                     st.session_state.kg_generator.url_list = st.session_state.url_list


#         # Initialize button
#         if st.button("Initialize/Reset KG Generator"):
#             st.session_state.kg_generator = initialize_kg_generator()
#             if st.session_state.kg_generator:
#                 st.success("KG Generator initialized successfully!")

#         if st.session_state.use_url:
#             st.header("URL Processing Preview")
#             st.write("URLs to be processed:")
#             for url in st.session_state.url_list.get_all_urls():
#                 st.write(f"- {url}")

#     # Main content area
#     if st.session_state.kg_generator is None:
#         st.warning("Please initialize the KG Generator using the sidebar first!")
#         return

#     # File upload and KG generation
#     st.header("Generate Knowledge Graph")
#     kg_name = st.text_input("Knowledge Graph Name", value="new_graph")
#     uploaded_files = st.file_uploader("Upload PDF Files", type=['pdf'], accept_multiple_files=True)

#     if uploaded_files and st.button("Generate Knowledge Graph"):
#         pdf_dir = save_uploaded_files(uploaded_files)
#         if pdf_dir:
#             asyncio.run(generate_kg(pdf_dir, kg_name))

#     # Update existing KG
#     st.header("Update Existing Knowledge Graph")
#     update_files = st.file_uploader("Upload Additional PDF Files", type=['pdf'], accept_multiple_files=True, key="update")

#     if update_files and st.button("Update Knowledge Graph"):
#         if not st.session_state.kg_generator.kg:
#             st.error("No existing Knowledge Graph found. Please generate one first!")
#         else:
#             update_dir = save_uploaded_files(update_files)
#             if update_dir:
#                 try:
#                     with st.spinner('Updating Knowledge Graph...'):
#                         st.session_state.kg_generator.update_knowledge_graph(update_dir)
#                     st.success('Knowledge Graph updated successfully!')
#                 except Exception as e:
#                     st.error(f"Error updating Knowledge Graph: {str(e)}")

#     # Query interface
#     st.header("Query Knowledge Graph")
#     query = st.text_area("Enter your query")

#     if query and st.button("Send Query"):
#         if not st.session_state.kg_generator.kg:
#             st.error("No Knowledge Graph exists. Please generate one first!")
#         else:
#             try:
#                 with st.spinner('Processing query...'):
#                     response = st.session_state.kg_generator.query_knowledge_graph(query)
#                 st.subheader("Response:")
#                 st.write(response)
#             except Exception as e:
#                 st.error(f"Error processing query: {str(e)}")

# if __name__ == "__main__":
#     main()


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
