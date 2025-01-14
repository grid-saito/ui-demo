from setuptools import setup, find_packages

setup(
    name="graph",  
    version="0.1.0",
    description="Graph module for managing super graphs and related logic.",
    packages=find_packages(), 
    install_requires=[
        "anthropic_bedrock",
        "boto3",
        "duckduckgo-search",
        "langchain",
        "langchainhub",
        "langchain-core",
        "langchain-cohere",
        "langchain-experimental",
        "langchain-openai",
        "langchain-community",
        "langchain-aws",
        "langchain-google-genai",
        "langgraph",
        "pytest",
        "python-dotenv",
        "black",
        "isort",
        "flake8",
        "injector",
        "opencv-python",
        "moviepy",
        "slack_bolt",
        "arxiv",
        "pypdf",
        "numexpr",
        "Pillow",
        "pandas",
        "requests",
        "yt-dlp",
        "unstructured",
        "azure-ai-documentintelligence",
        "pyautogen",
        "faiss-cpu",
        "selenium",
    ],
    python_requires=">=3.8",  # Specify Python version compatibility
)