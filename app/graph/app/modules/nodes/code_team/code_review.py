import logging
from langchain_core.messages import AIMessage
from modules.data_models.graph_state import GraphState
from modules.chains.code_visualization_chain import chain


logger = logging.getLogger(__name__)


def code_review(state: GraphState):
    logger.info("Call code_review node...\n\n")
    last_message = state["messages"][-1]
    logger.info(f"human message\n\n{last_message}\n\n")

    result = chain.invoke(
        {"user_message": last_message.content, "current_code": state["code"]}
    )
    logger.info(f"code_review node finished...\n\n")

    return {
        "next": "code_supervisor",
        "messages": [AIMessage(content=result.response_message)],
    }
