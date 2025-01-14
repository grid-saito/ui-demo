from modules.data_models.graph_state import GraphState


def exists_message(state: GraphState):
    return len(state.messages) >= 1 and state.messages[-1].content != ""


def get_last_message(state: GraphState):
    return state.messages[-1]
