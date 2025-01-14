from langchain_core.prompts import ChatPromptTemplate
from ..models.langchain_azure import langchain_azure_model
from ..prompts.create_suggestions import CREATE_SUGGESTIONS_PROMPT 
from ..data_models.next_action import SuggestedActionsOutput 


structured_model = langchain_azure_model.with_structured_output(SuggestedActionsOutput)
chain = (
    ChatPromptTemplate.from_template(CREATE_SUGGESTIONS_PROMPT) |
    structured_model
)
