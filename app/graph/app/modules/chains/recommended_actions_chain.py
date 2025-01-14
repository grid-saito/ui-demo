from langchain_core.prompts import ChatPromptTemplate
from modules.models.langchain_azure import langchain_azure_model
from modules.prompts.create_suggestions import RECOMMENDED_ACTIONS_PROMPT
from modules.data_models.external_source import RecommendedActionsOutput


structured_model = langchain_azure_model.with_structured_output(RecommendedActionsOutput)
chain = (
    ChatPromptTemplate.from_template(RECOMMENDED_ACTIONS_PROMPT) |
    structured_model
)
