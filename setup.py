from setuptools import setup, find_packages

setup(
    name="kg-generator",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "unstructured[pdf]",
        "python-dotenv",
        "redis",
        "google-generativeai",
        "graphrag_sdk[all]",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "black",
            "flake8",
            "mypy",
        ],
    },
    python_requires=">=3.10",
)
