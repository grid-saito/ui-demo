from langchain_core.prompts import ChatPromptTemplate
from modules.data_models.next_node import ResultNextNode
from modules.models.langchain_azure import langchain_azure_model
from modules.prompts.result_supervisor_prompt import RESULT_SUPERVISOR_PROMPT

structured_model = langchain_azure_model.with_structured_output(ResultNextNode)
chain = (
    ChatPromptTemplate.from_template(RESULT_SUPERVISOR_PROMPT) |
    structured_model
)
