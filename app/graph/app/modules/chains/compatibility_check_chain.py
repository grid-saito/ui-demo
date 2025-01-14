from langchain_core.prompts import ChatPromptTemplate
from modules.models.langchain_azure import langchain_azure_model
from modules.prompts.check_input_external_data_compatibility import COMPATIBILITY_CHECK_PROMPT
from modules.data_models.external_source import CompatibilityCheckResultOutput


structured_model = langchain_azure_model.with_structured_output(CompatibilityCheckResultOutput)
chain = (
    ChatPromptTemplate.from_template(COMPATIBILITY_CHECK_PROMPT) |
    structured_model
)
