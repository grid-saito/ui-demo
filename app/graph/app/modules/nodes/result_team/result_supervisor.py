import logging

from const import result_node_description, result_supervisor_next_nodes
from langchain_core.messages import AIMessage
from modules.chains.result_supervisor_chain import chain
from modules.data_models.graph_state import GraphState
from modules.nodes.node_utils import get_last_message

logger = logging.getLogger(__name__)


def result_supervisor(state: GraphState):
    logger.info("Call result_supervisor node...")
    last_message = get_last_message(state)
    logger.info(f"last message: {last_message}")

    next_node = chain.invoke(
        {
            "message": last_message.content,
            "next_nodes": result_supervisor_next_nodes,
            "next_nodes_description": result_node_description,
        }
    )
    state.next = next_node.node_name
    logger.info(f"Next node: {next_node.node_name}")

    if next_node.node_name == "result_supervisor_node":
        state.messages = [
            AIMessage(
                content="指示を受け付けられませんでした。再度指示をお願いします。"
            )
        ]
    return state
