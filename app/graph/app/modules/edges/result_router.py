import logging

from modules.data_models.graph_state import GraphState

logger = logging.getLogger(__name__)


def result_router(state: GraphState):
    logger.info("Call result_router...")
    logger.info(f"Next node: {state.next}")
    return state.next
