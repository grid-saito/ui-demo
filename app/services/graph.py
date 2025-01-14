from graph.app.modules.chains.input_data_processing import chain as input_data_processing_chain
from graph.app.modules.chains.results_data_processing import chain as result_data_processing_chain 
from graph.app.modules.chains.demand_data_processing import chain as demand_data_processing_chain
from graph.app.modules.chains.compatibility_check_chain import chain as compatibility_check_chain
from graph.app.modules.chains.suggested_actions_chain import chain as suggested_actions_chain
from graph.app.modules.data_models.external_source import CompatibilityCheckResultOutput
from typing import List


def _parse_data(raw_data: dict) -> List[CompatibilityCheckResultOutput]:
    """
    Parse the 'results' field in raw_data, converting strings into Pydantic objects.
    """
    parsed_results = []
    for item in raw_data.results:
        parsed_results.append((item))
    
    return parsed_results

def _parse_compatibility_results(data: List[CompatibilityCheckResultOutput]):
    """
    Parse compatibility results into a Markdown table for better readability in chat.

    Args:
        data (List[CompatibilityCheckResultOutput]): List of compatibility check results.

    Returns:
        tuple: A formatted Markdown table (string) and a list of booleans indicating results.
    """
    # Convert input data into a structured list for processing
    rows = [
        {
            "Check": item.check,
            "Result": "Pass" if item.result else "Fail",
            "Explanation": item.explanation or "N/A",
            "Action": item.action
        }
        for item in data
    ]

    # Build the Markdown table header
    table_md = "| Check | Result | Explanation | Action |\n"
    table_md += "|-------|--------|-------------|--------|\n"

    # Add each row to the Markdown table
    for row in rows:
        table_md += (
            f"| {row['Check']} | {row['Result']} | {row['Explanation']} | {row['Action']} |\n"
        )

    # Extract boolean results
    result_booleans = [item.result for item in data]

    return table_md, result_booleans



def get_input_confirmation(input_data, demand_data, plant_status, weather_data):
    raw_output = compatibility_check_chain.invoke({
        "input_data": input_data, 
        "demand_data": demand_data, 
        "plant_status": plant_status, 
        "weather_data": weather_data})
    output = _parse_data(raw_output)
    output_parsed, results = _parse_compatibility_results(output)
    return output_parsed, results


def chat_about_demand_data(query, chat_history, demand_constraint, demand_forecast):
    result = demand_data_processing_chain.invoke({"query": query,
                                                  "chat_history": chat_history,
                                                  "demand_constraint": demand_constraint, 
                                                  "demand_forecast": demand_forecast})
    return result


def chat_about_input_data(query, chat_history, input_data):
    result = input_data_processing_chain.invoke({"query": query,
                                                 "chat_history": chat_history,
                                                 "input_data": input_data})
    return result


def chat_about_result_data(query, chat_history, input_data, external_data, results, equipment_states):
    result = result_data_processing_chain.invoke({"query": query,
                                               "chat_history": chat_history,
                                               "input_data": input_data, 
                                               "demand_data": external_data, 
                                               "equipment_states": equipment_states,
                                               "result_data": results})
    return result


def get_suggested_actions(input_data, external_data, compability_check_result) -> List[str]: 
    result = suggested_actions_chain.invoke({"input_data": input_data,
                                             "demand_forecast": external_data["demand_data"],
                                             "equipment_states": external_data["plant_status"],
                                             "compability_check_result": compability_check_result})
    return result
