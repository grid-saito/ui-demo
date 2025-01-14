import logging
from langchain_core.messages import AIMessage
from modules.data_models.graph_state import GraphState
from modules.chains.input_data_chain import chain
from modules.data_models.input_data import INPUT_DATA_SCHEMA

logger = logging.getLogger(__name__)


def input_data(state: GraphState):
    logger.info("Call input_data node...")
    last_message = state.messages[-1]
    logger.info(f"last message: {last_message}")

    result = chain.invoke(
        {
            "user_message": last_message.content,
            "input_data_schema": INPUT_DATA_SCHEMA,
            "current_input_data": state.input_data,
        }
    )
    logger.info(f"input_data node result: {result}")

    return {
        "next": "input_supervisor_node",
        "messages": [AIMessage(content=result.response_message)],
        "input_data": result.input_data,
    }
