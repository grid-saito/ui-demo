from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from ..models.langchain_azure import langchain_azure_model
from ..prompts.result_visualization_prompt import RESULT_VISUALIZATION_PROMPT

chain = (
    ChatPromptTemplate.from_template(RESULT_VISUALIZATION_PROMPT) |
    langchain_azure_model |
    StrOutputParser()
)
