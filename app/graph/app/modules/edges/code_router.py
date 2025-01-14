import logging

from modules.data_models.graph_state import GraphState

logger = logging.getLogger(__name__)


def code_router(state: GraphState):
    logger.info("Call code_router...")
    logger.info(f"Next node: {state.next}")
    return state.next
