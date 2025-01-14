import logging
from langchain_core.messages import AIMessage
from modules.data_models.graph_state import GraphState
from modules.chains.code_visualization_chain import chain
from modules.nodes.node_utils import get_last_message

logger = logging.getLogger(__name__)


def code_visualization(state: GraphState):
    logger.info("Call code_visualization node...")
    last_message = get_last_message(state)
    logger.info(f"last message: {last_message}")

    result = chain.invoke(
        {"user_message": last_message.content, "current_code": state.code}
    )
    logger.info("code_visualization node finished...")

    return {
        "next": "code_supervisor_node",
        "messages": [AIMessage(content=result)],
    }
