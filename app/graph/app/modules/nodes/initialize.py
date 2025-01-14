import logging
from langchain_core.messages import AIMessage
from modules.data_models.graph_state import GraphState
from modules.chains.initialize_route_chain import chain
from const import initialize_next_nodes, input_node_description
from modules.nodes.node_utils import exists_message, get_last_message


logger = logging.getLogger(__name__)


def initialize(state: GraphState):
    """
    Stateの初期化と最初のノードの選択
    """
    logger.info("Call initialize node...")

    # メッセージがない場合は入力のスーパーバイザーに遷移する
    if not exists_message(state):
        logger.info("No initial message. Transition to input_supervisor...")
        state.next = "input_data_processing_node"
        #state.messages = [
        #    AIMessage(
        #        content="私は10UC問題に詳しいアシスタントです。どのような問題を解きますか？"
        #    )
        #]
        return state

    last_message = get_last_message(state)
    logger.info(f"last_message: {last_message}")

    next_node = chain.invoke(
        {
            "message": last_message.content,
            "next_nodes": initialize_next_nodes,
            "next_nodes_description": input_node_description,
        }
    )

    state.next = next_node.node_name
    logger.info(f"Next node: {next_node.node_name}")
    return state
