from langchain_core.prompts import ChatPromptTemplate
from modules.models.langchain_azure import langchain_azure_model
from modules.prompts.input_visualization_prompt import INPUT_VISUALIZATION_PROMPT
from modules.data_models.input_data import InputDataNodeOutput

structured_model = langchain_azure_model.with_structured_output(InputDataNodeOutput)
chain = (
    ChatPromptTemplate.from_template(INPUT_VISUALIZATION_PROMPT) |
    structured_model
)
