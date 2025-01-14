import logging

from modules.data_models.graph_state import GraphState

logger = logging.getLogger(__name__)


def code_execution_router(state: GraphState):
    if state.code_confirmation and state.code_success:
        return "result_polling_node"
    else:
        return "code_supervisor_node"
