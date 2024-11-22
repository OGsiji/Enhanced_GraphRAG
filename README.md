# Knowledge Graph Generator

A Python application that generates knowledge graphs from PDF documents using FalkorDB and Google's Gemini model. The Knowledge Graph generator extends the GraphRAG-SDK framework to
handle PDF files using the Unstructured-IO library.

## Prerequisites

- Docker
- Docker Compose
- Google API Key for Gemini model

## Project Structure

```
.
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── src/
│   └── kg_generator/
├── tests/
├── examples/
├── initial_pdfs/    # Mount point for initial PDF files
└── additional_pdfs/ # Mount point for additional PDF files to update the graph
```

## Quick Start

1. Clone the repository:
```bash
git clone 
cd knowledge-graph-generator
```

2. Create a `.env` file from the example:
```bash
cp .env .env
```

3. Edit the `.env` file and add your Google API key and other Important keys:
```
GOOGLE_API_KEY=your_google_api_key_here
```

4. Create PDF directories and add your PDF files:
```bash
mkdir initial_pdfs additional_pdfs
# Add initial PDFs
cp path/to/your/initial/pdfs/*.pdf initial_pdfs/
# Add additional PDFs (optional)
cp path/to/your/additional/pdfs/*.pdf additional_pdfs/
```

5. Build and run the containers:
```bash
docker-compose up --build
```

## Processing Flow

1. The system first processes all PDFs in the `initial_pdfs` directory to create the base knowledge graph
2. If any PDFs exist in the `additional_pdfs` directory, they will be processed and used to update the existing knowledge graph
3. Both directories are mounted as volumes, so you can add or remove PDFs without rebuilding the container

## Running Tests

To run the tests in a Docker container:

```bash
docker-compose run --rm kg_generator pytest
```
