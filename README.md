# Knowledge Graph Generator
Added crew4ai for URL extraction alongside unstructured.io for PDF extraction. crew4ai is a powerful tool that provides advanced capabilities for extracting structured data from unstructured sources such as web pages, documents, and more. With crew4ai, you can easily extract URLs from text and leverage them in your knowledge graph generation process. This integration enhances the functionality of the application by allowing you to incorporate web-based information into your knowledge graphs. By combining the power of crew4ai and unstructured.io, you can create comprehensive and dynamic knowledge graphs that capture information from both PDF documents and web sources.

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
git clone https://github.com/OGsiji/Enhanced_GraphRAG.git
cd Enhanced_GraphRAG
```

2. Create a `.env` file from the example:
```bash
touch .env
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

#Add Urls,
navigate
to src/kg_generator/url.py
this is where you can add/edit urls

## Select what to run

you can also set what to run whether url or pdfs in
src/kg_generator/config.py {LinkConfig.url} or {LinkConfig.pdf}

default is true
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
git clone https://github.com/OGsiji/Enhanced_GraphRAG.git
cd Enhanced_GraphRAG
```

2. Create a `.env` file from the example:
```bash
touch .env
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
