from langchain_core.prompts import ChatPromptTemplate
from ..models.langchain_azure import langchain_azure_model
from ..prompts.input_data_prompt import INPUT_DATA_PROMPT
from ..data_models.input_data import InputDataNodeOutput

structured_model = langchain_azure_model.with_structured_output(InputDataNodeOutput)
chain = (
    ChatPromptTemplate.from_template(INPUT_DATA_PROMPT) |
    structured_model
)
