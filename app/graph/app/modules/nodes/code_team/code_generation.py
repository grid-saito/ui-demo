import logging

from langchain_core.messages import AIMessage
from modules.data_models.graph_state import GraphState
from modules.chains.code_generation_chain import chain
from modules.prompts.code_generation_prompt import OPTJOB_EXAMPLE_CODE
from modules.retrievers.or_retreiver import retriever, format_docs
from modules.nodes.node_utils import get_last_message

logger = logging.getLogger(__name__)


def code_generation(state: GraphState):
    logger.info("Call code_generation node...")
    last_message = get_last_message(state)
    logger.info(f"last message: {last_message}")

    result = chain.invoke(
        {
            "user_message": last_message.content,
            "input_data": state.input_data,
            "sample_code": OPTJOB_EXAMPLE_CODE,
            "context": retriever | format_docs,
        }
    )
    logger.info("code_generation node finished...")

    return {
        "next": "code_supervisor_node",
        "messages": [AIMessage(content=result.response_message)],
        "code": result.code,
    }
