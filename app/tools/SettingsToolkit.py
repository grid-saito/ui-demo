from langchain_core.tools import tool
import streamlit as st
from tools.BaseToolkit import BaseToolkit
import random
import pandas as pd
from utils import get_session_settings, save_session_settings


@tool
def set_demand_constraint_value(values: list) -> str:
    """Set the demand constraint value."""
    before_data = get_session_settings()
    #st.session_state.settings_before_change = before_data 
    after_data = before_data.copy()
    after_data["demand"] = values
    save_session_settings(after_data)
    
    return f"Demand constraint set to {values}"


@tool
def set_column_values(column_name: str, new_values: list) -> str:
    """
    Modify the values of a specific column in the equipment settings.

    Parameters:
        column_name (str): The name of the column to modify.
        new_values (list): A list of new values to assign to the column.

    Returns:
        str: Confirmation or error message.
    """
    thread_state = get_session_settings()
    #st.session_state.settings_before_change = thread_state
    thread_state[column_name] = new_values
    save_session_settings(thread_state)
    return f"Column '{column_name}' updated successfully."


@tool
def set_objective(value: str) -> str:
    """
    Set the optimization objective.

    Parameters:
        value (str): The optimization objective. Must be one of 'Minimize Cost', 'Maximize Output', or 'Balance'.

    Returns:
        str: Confirmation or error message.
    """
    thread_state = get_session_settings()
    valid_objectives = ["Minimize Cost", "Maximize Output", "Balance"]
    if value not in valid_objectives:
        return f"Invalid objective: {value}. Valid options are {', '.join(valid_objectives)}."

    thread_state["objective"] = value
    save_session_settings(thread_state)
    return f"Objective set to {value}"


@tool
def set_selected_methods(methods: list) -> str:
    """
    Set the list of selected optimization methods.

    Parameters:
        methods (list): A list of optimization methods.

    Returns:
        str: Confirmation message.
    """
    thread_state = get_session_settings()
    thread_state["selected_methods"] = methods
    save_session_settings(thread_state)
    return f"Selected methods set to {methods}"


@tool
def set_demand_forecast(low=500, high=1500):
    """
    Set the demand forecast.
    The default values of the low and high are 500 and 1500. 

    When given instructions to lower the demand forecast, set the high value to be smaller than 1500 and low to be smaller than 500. 
    When given instructions to higher the demand forecast, set the high value to be larger than 1500 and low to be larger than 500. 
    
    Parameters:
        low (int): lowest value for the forecast of the demand value 
        high (int): highest value for the forecast of the demand value 

    Returns:
        str: Confirmation message.
    """
    demand_data = []
    timestamps = st.session_state.external_data["demand_data"]["Timestamp"]
    for timestamp in timestamps:
        demand = random.randint(low, high)
        demand_data.append({
            "Timestamp": timestamp,
            "Demand": demand,
        })

    st.session_state.external_data["demand_data"] = pd.DataFrame(demand_data)
    return f"Demand forecast set to {low} to {high}"


# Toolkit Definition
class SettingsToolkit(BaseToolkit):
    def __init__(self):
        self.tools = {
            "set_demand": set_demand_constraint_value,
            "set_objective": set_objective,
            "set_selected_methods": set_selected_methods,
            "set_demand_forecast": set_demand_forecast,
            "set_column_values": set_column_values,
        }