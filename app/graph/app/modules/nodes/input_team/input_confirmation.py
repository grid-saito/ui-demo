import logging
from langchain_core.messages import AIMessage
from modules.data_models.graph_state import GraphState
from modules.nodes.node_utils import get_last_message
from modules.chains.compatibility_check_chain import chain
from modules.data_models.external_source import CompatibilityCheckResultOutput
from typing import List


logger = logging.getLogger(__name__)


def _generate_ai_message(check_results: List[CompatibilityCheckResultOutput]):
    # Check for failed compatibility checks
    failed_checks = [result for result in check_results if not result.result]

    # Generate explanations table
    explanation_table = "| **Check** | **Result** | **Explanation** |\n|-----------|------------|-----------------|\n"
    for result in check_results:
        explanation_table += f"| {result.check} | {result.result} | {result.explanation or 'N/A'} |\n"

    # Generate actions message
    actions_message = "### Recommended Actions:\n"
    for result in failed_checks:
        actions_message += f"- **{result.check}:** {result.action}\n"

    message = "入力データが未承認です。入力データを修正または確認してください。" + "\n" + explanation_table + "\n" + actions_message
    return {
        "messages": [
            AIMessage(content=message),
        ]
    }


def parse_results(raw_data: dict) -> List[CompatibilityCheckResultOutput]:
    """
    Parse the 'results' field in raw_data, converting strings into Pydantic objects.
    """
    parsed_results = []
    for item in raw_data.results:
        parsed_results.append((item))
    
    return parsed_results


def input_confirmation(state: GraphState):
    # ユーザーの入力データを承認した場合に遷移するノード。コード生成状態に移行する。
    logger.info("Call input_confirmation node...")
    last_message = get_last_message(state)
    logger.info(f"last message: {last_message}")
    raw_output = chain.invoke({"input_data": state.input_data, 
                           "demand_data": state.demand_data, 
                           "plant_status": state.plant_status, 
                           "weather_data": state.weather_data})
    
    output = parse_results(raw_output)
    all_checks_passed = all(item.result for item in output)
    if all_checks_passed:
        return {
            "messages": [
                AIMessage(content="入力データを承認しました。コードを生成します。")
            ]
        }
    else:
        return _generate_ai_message(output)