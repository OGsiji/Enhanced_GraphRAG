# Use the official ARM64 image as base
FROM unclecode/crawl4ai:basic-arm64 as base

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


RUN mkdir -p initial_pdfs additional_pdfs temp_processed

ENV PYTHONUNBUFFERED=1
ENV FALKORDB_HOST=falkordb
ENV FALKORDB_PORT=6379

# Create streamlit config with updated settings
RUN mkdir -p /root/.streamlit
RUN echo '\
[server]\n\
port = 8501\n\
address = "0.0.0.0"\n\
enableXsrfProtection = false\n\
enableCORS = false\n\
\n\
[browser]\n\
gatherUsageStats = false\n\
serverAddress = "localhost"\n\
serverPort = 8501\n\
' > /root/.streamlit/config.toml

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "examples/basic_usage.py"]
