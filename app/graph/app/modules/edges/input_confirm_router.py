import logging
from modules.data_models.graph_state import GraphState
from langgraph.graph import END


logger = logging.getLogger(__name__)


def input_confirm_router(state: GraphState):
    if state.input_data_confirmation:
        return END
    else:
        return "input_data_processing_node"
