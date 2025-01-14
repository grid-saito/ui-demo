from langchain_core.prompts import ChatPromptTemplate
from modules.models.langchain_azure import langchain_azure_model
from modules.prompts.input_supervisor_prompt import INPUT_SUPERVISOR_PROMPT
from modules.data_models.next_node import InputNextNode

structured_model = langchain_azure_model.with_structured_output(InputNextNode)
chain = (
    ChatPromptTemplate.from_template(INPUT_SUPERVISOR_PROMPT) |
    structured_model
)
