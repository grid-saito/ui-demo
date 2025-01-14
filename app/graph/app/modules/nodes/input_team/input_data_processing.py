import logging
from langchain_core.messages import AIMessage
from modules.data_models.graph_state import GraphState
from modules.chains.input_data_processing import chain

logger = logging.getLogger(__name__)


def input_data_processing(state: GraphState):
    logger.info("Call input_data node...")
    if len(state.messages) == 0:
        state.messages = [AIMessage(content="I can help you with processing and visualizing input data. How can I help you today?")]
    last_message = state.messages[-1]
    logger.info(f"last message: {last_message}")
    #print(last_message.content)
    #print(state.messages)
    #print(state.input_data)
    result = chain.invoke(
        {"query": last_message.content, 
        "chat_history": state.messages, 
        "input_data": state.input_data})
    
    output = result
    logger.info(f"input_data node result: {result}")

    return {
        "next": "input_confirmation_node",
        "messages": [AIMessage(content=output)],
    }