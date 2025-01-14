import logging
from const import input_node_description, input_supervisor_next_nodes

from langchain_core.messages import AIMessage
from modules.chains.input_supervisor_chain import chain
from modules.data_models.graph_state import GraphState
from modules.nodes.node_utils import get_last_message, exists_message

logger = logging.getLogger(__name__)


def input_supervisor(state: GraphState) -> GraphState:
    logger.info("Call input_supervisor node...")

    if not exists_message(state):
        logger.info("No message. Transition to input_supervisor_node...")
        state.next = "input_supervisor_node"
        return state

    last_message = get_last_message(state)
    logger.info(f"last message: {last_message}")

    next_node = chain.invoke(
        {
            "message": last_message.content,
            "next_nodes": input_supervisor_next_nodes,
            "next_nodes_description": input_node_description,
        }
    )
    state.next = next_node.node_name
    state.input_data_confirmation = next_node.input_data_confirmation
    logger.info(f"Next node: {next_node.node_name}")

    if next_node.node_name == "input_supervisor_node":
        state.messages = [
            AIMessage(
                content="入力を受け付けられませんでした。再度入力をお願いします。"
            )
        ]
    return state