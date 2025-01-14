import os

from dotenv import load_dotenv

load_dotenv(verbose=True, dotenv_path=".env")

DEFAULT_OPENAI_MODEL = "gpt-4o-mini"
DEFAULT_GEMINI_MODEL = "gemini-1.5-flash"

# Azure OpenAI
OPENAI_API_TYPE = os.environ.get("OPENAI_API_TYPE")
OPENAI_API_VERSION = os.environ.get("OPENAI_API_VERSION")
AZURE_OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT_NAME = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")
AZURE_OPENAI_MODEL = os.environ.get("AZURE_OPENAI_MODEL", DEFAULT_OPENAI_MODEL)

AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME = os.environ.get(
    "AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME"
)
AZURE_OPENAI_EMBEDDINGS_MODEL = os.environ.get("AZURE_OPENAI_EMBEDDINGS_MODEL", "text-embedding-3-large")

# slack
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")

# Optjob
OPTJOB_HOST = "https://internal-optjob.renom.jp"
OPTJOB_PROJECT_ID = os.environ.get("OPTJOB_PROJECT_ID")
OPTJOB_JOB_QUEUE_ID = os.environ.get("OPTJOB_JOB_QUEUE_ID")
OPTJOB_TOKEN = os.environ.get("OPTJOB_TOKEN")
