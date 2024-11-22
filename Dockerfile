# Dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt \
    && pip list

# Copy source code and setup files
COPY src/ src/
COPY setup.py .
COPY pyproject.toml .

# Install the package
RUN pip install -e .

# Copy the rest of the application code
COPY examples/ examples/
COPY tests/ tests/

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FALKORDB_HOST=falkordb
ENV FALKORDB_PORT=6379

# Create directories for PDFs
RUN mkdir -p initial_pdfs additional_pdfs

# Run the application
CMD ["python", "examples/basic_usage.py"]
