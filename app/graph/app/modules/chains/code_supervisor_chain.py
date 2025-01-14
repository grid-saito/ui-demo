from langchain_core.prompts import ChatPromptTemplate
from modules.models.langchain_azure import langchain_azure_model
from modules.prompts.code_supervisor_prompt import CODE_SUPERVISOR_PROMPT
from modules.data_models.next_node import CodeNextNode

structured_model = langchain_azure_model.with_structured_output(CodeNextNode)
chain = (
    ChatPromptTemplate.from_template(CODE_SUPERVISOR_PROMPT) |
    structured_model
)
