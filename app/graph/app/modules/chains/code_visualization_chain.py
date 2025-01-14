from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from modules.models.langchain_azure import langchain_azure_model
from modules.prompts.code_visualization_prompt import CODE_VISUALIZATION_PROMPT

chain = (
    ChatPromptTemplate.from_template(CODE_VISUALIZATION_PROMPT) |
    langchain_azure_model |
    StrOutputParser()
)
