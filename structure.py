├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── setup.py
├── pyproject.toml
├── src/
│   └── kg_generator/
│       ├── __init__.py
│       ├── config.py
│       ├── exceptions.py
│       ├── processors/
│       │   ├── __init__.py
│       │   └── pdf_processor.py
│       ├── knowledge_graph/
│       │   ├── __init__.py
│       │   └── generator.py
│       └── utils/
│           ├── __init__.py
│           └── logging.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_pdf_processor.py
│   └── test_knowledge_graph.py
└── examples/
    ├── __init__.py
    └── basic_usage.py

