from ...config import (AZURE_OPENAI_API_KEY, AZURE_OPENAI_DEPLOYMENT_NAME,
                    AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME,
                    AZURE_OPENAI_EMBEDDINGS_MODEL, AZURE_OPENAI_ENDPOINT,
                    AZURE_OPENAI_MODEL)
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings

langchain_azure_model = AzureChatOpenAI(
    azure_deployment=AZURE_OPENAI_DEPLOYMENT_NAME,
    model=AZURE_OPENAI_MODEL,
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
)

# dev: comment out for now, not using
langchain_azure_embeddings_model = AzureOpenAIEmbeddings(
    azure_deployment=AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME,
)
