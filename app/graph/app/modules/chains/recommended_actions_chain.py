from langchain_core.prompts import ChatPromptTemplate
from ..models.langchain_azure import langchain_azure_model
from ..prompts.create_suggestions import RECOMMENDED_ACTIONS_PROMPT
from ..data_models.external_source import RecommendedActionsOutput


structured_model = langchain_azure_model.with_structured_output(RecommendedActionsOutput)
chain = (
    ChatPromptTemplate.from_template(RECOMMENDED_ACTIONS_PROMPT) |
    structured_model
)
