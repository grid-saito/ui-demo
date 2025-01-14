from langchain_core.tools import tool
import streamlit as st
from tools.BaseToolkit import BaseToolkit
from datetime import datetime, timedelta
import random
import pandas as pd
from typing import List
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
class DemandDataToolkit(BaseToolkit):
    def __init__(self):
        self.tools = {
            "set_demand": set_demand_constraint_value,
        }