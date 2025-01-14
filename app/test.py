from modules.prompts.chat_bot_prompt import CHAT_BOT_PROMPT
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from modules.models.langchain_azure import langchain_azure_model
from modules.prompts.code_visualization_prompt import CODE_VISUALIZATION_PROMPT


chain = (
    ChatPromptTemplate.from_template(CHAT_BOT_PROMPT) |
    langchain_azure_model |
    StrOutputParser()
)
print(chain)

result = chain.invoke(
    {"query": "", 
        "chat_history": "", 
        "input_data": ""})
print(result)