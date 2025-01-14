import logging
import time

from config import OPTJOB_PROJECT_ID
from const import result_node_description, result_supervisor_next_nodes
from langchain_core.messages import AIMessage
from modules.data_models.graph_state import GraphState
from modules.nodes.node_utils import get_last_message
from modules.optjob.client import get_job, get_job_result_as_str, optjob_client

logger = logging.getLogger(__name__)


def result_polling(state: GraphState):
    logger.info("Call result_polling node...")
    last_message = get_last_message(state)
    logger.info(f"last message: {last_message}")

    while True:
        time.sleep(10)
        job = get_job(state.optjob_job_id)
        logger.info(f"job data: {job.data}")
        if job.data.state.upper() == "SUCCEEDED":
            if job.data.optimization_state.upper() == "OPTIMIZED":
                result = get_job_result_as_str(state.optjob_job_id)
                state.optjob_result = result

            state.optjob_score = job.data.score
            state.optjob_state = job.data.state
            state.optjob_optimization_state = job.data.optimization_state
            break

    response_message = f"コードが終了しました。最適化計算の状態は{state.optjob_optimization_state}、スコアは{state.optjob_score}です。"
    state.messages = [AIMessage(content=response_message)]
    return state
