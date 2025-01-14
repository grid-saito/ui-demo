import logging

from langchain_core.messages import AIMessage
from modules.chains.result_visualization_chain import chain
from modules.data_models.graph_state import GraphState
from modules.nodes.node_utils import get_last_message

logger = logging.getLogger(__name__)


def result_visualization(state: GraphState):
    # TODO: 本来はデータを可視化して返すイメージ
    logger.info("Call result_visualization node...")
    last_message = get_last_message(state)
    logger.info(f"last message: {last_message}")

    result = chain.invoke(
        {
            "user_message": last_message.content,
            "code": state.code,
            "current_result": state.optjob_result,
            "optjob_state": state.optjob_state,
            "optjob_optimization_state": state.optjob_optimization_state,
        }
    )
    logger.info(f"result_visualization node result: {result}")
    state.messages = [AIMessage(content=result)]
    return state
