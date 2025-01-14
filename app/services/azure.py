from dotenv import load_dotenv
import os
import logging
from langchain_openai import AzureChatOpenAI

load_dotenv()
# Fetch the environment variables
AZURE_OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT_NAME = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")
AZURE_OPENAI_MODEL = os.environ.get("AZURE_OPENAI_MODEL")
OPENAI_API_VERSION = os.environ.get("OPENAI_API_VERSION")

# Log the environment variable values using logging.info
logging.info(f"AZURE_OPENAI_API_KEY: {AZURE_OPENAI_API_KEY[:5]}*****")  # Masked for security
logging.info(f"AZURE_OPENAI_ENDPOINT: {AZURE_OPENAI_ENDPOINT}")
logging.info(f"AZURE_OPENAI_DEPLOYMENT_NAME: {AZURE_OPENAI_DEPLOYMENT_NAME}")
logging.info(f"AZURE_OPENAI_MODEL: {AZURE_OPENAI_MODEL}")
logging.info(f"OPENAI_API_VERSION: {OPENAI_API_VERSION}")

# List of environment variables and their names
env_vars = [
    ("AZURE_OPENAI_API_KEY", AZURE_OPENAI_API_KEY),
    ("AZURE_OPENAI_ENDPOINT", AZURE_OPENAI_ENDPOINT),
    ("AZURE_OPENAI_DEPLOYMENT_NAME", AZURE_OPENAI_DEPLOYMENT_NAME),
    ("AZURE_OPENAI_MODEL", AZURE_OPENAI_MODEL),
    ("OPENAI_API_VERSION", OPENAI_API_VERSION)
]

# Check if all necessary environment variables are set
missing_vars = [name for name, value in env_vars if value is None]
if missing_vars:
    raise ValueError(f"The following environment variables must be set: {', '.join(missing_vars)}")

# Initialize the AzureChatOpenAI model
chat_model = AzureChatOpenAI(
    openai_api_key = AZURE_OPENAI_API_KEY,
    azure_deployment=AZURE_OPENAI_DEPLOYMENT_NAME,
    model=AZURE_OPENAI_MODEL,
    api_version=OPENAI_API_VERSION,
    streaming=True,
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)