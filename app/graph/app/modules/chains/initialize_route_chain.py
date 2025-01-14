from langchain_core.prompts import ChatPromptTemplate
from modules.models.langchain_azure import langchain_azure_model
from modules.prompts.initialize import INITIALIZE_PROMPT
from modules.data_models.next_node import NextNode

structured_model = langchain_azure_model.with_structured_output(NextNode)
chain = (
    ChatPromptTemplate.from_template(INITIALIZE_PROMPT) |
    structured_model
)
