import logging

from langchain_core.messages import AIMessage
from modules.chains.code_visualization_chain import chain
from modules.data_models.graph_state import GraphState
from modules.nodes.node_utils import get_last_message

logger = logging.getLogger(__name__)


def code_execution(state: GraphState):
    logger.info("Call code_execution node...")
    last_message = get_last_message(state)
    logger.info(f"last message: {last_message}")

    if state.code_confirmation:
        try:
            exec(state.code.code, globals())
            state.optjob_model = globals()["model"]
            response_message = "コードの実行に成功しました。"
            return {
                "code_success": True,
                "messages": [AIMessage(content=response_message)],
                "optjob_job_id": response.data.id,
                "optjob_job_name": response.data.name,
            }
        except Exception as e:
            response_message = f"エラーが発生しました。\n\n{e}\n\n"
            return {
                "code_confirmation": False,
                "code_success": False,
                "messages": [AIMessage(content=response_message)],
            }
    else:
        response_message = "コードを実行しませんでした。"
        return {
            "messages": [AIMessage(content=response_message)],
        }
