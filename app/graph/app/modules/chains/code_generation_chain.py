from langchain_core.prompts import ChatPromptTemplate
from modules.models.langchain_azure import langchain_azure_model
from modules.prompts.code_generation_prompt import CODE_GENERATION_PROMPT
from modules.data_models.code import CodeNodeOutput

structured_model = langchain_azure_model.with_structured_output(CodeNodeOutput)
chain = (
    ChatPromptTemplate.from_template(CODE_GENERATION_PROMPT) |
    structured_model
)
