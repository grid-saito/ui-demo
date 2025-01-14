import streamlit as st
import pandas as pd
import numpy as np


def update_equipment_settings(units: list, max_output: list, startup_cost: list):
    """
    Updates the equipment settings table.

    Args:
        units (list): List of unit names.
        max_output (list): List of max output values for each unit.
        startup_cost (list): List of startup cost values for each unit.

    Returns:
        str: Confirmation message.
    """
    if len(units) != len(max_output) or len(units) != len(startup_cost):
        return "Error: All input lists must have the same length."

    st.session_state["equipment_settings"] = pd.DataFrame({
        "Units": units,
        "Max Output": max_output,
        "Startup Cost": startup_cost,
    })
    return "Equipment settings updated successfully."

# 2. Update Objective Function
def update_objective_function(objective: str):
    """
    Updates the selected objective function.

    Args:
        objective (str): The new objective function. Must be one of:
                         ["Minimize Cost", "Maximize Output", "Balance Demand and Supply"]

    Returns:
        str: Confirmation message.
    """
    valid_objectives = ["Minimize Cost", "Maximize Output", "Balance Demand and Supply"]
    if objective not in valid_objectives:
        return f"Error: '{objective}' is not a valid objective function."

    st.session_state["objective"] = objective
    return f"Objective function updated to '{objective}'."

# 3. Update Constraints
def update_constraints(demand: int, max_output: int):
    """
    Updates the constraints for demand and max output.

    Args:
        demand (int): The new demand value (between 500 and 1500).
        max_output (int): The new max output value per unit (between 100 and 1000).

    Returns:
        str: Confirmation message.
    """
    if not (500 <= demand <= 1500):
        return "Error: Demand must be between 500 and 1500."
    if not (100 <= max_output <= 1000):
        return "Error: Max Output must be between 100 and 1000."

    st.session_state["demand"] = demand
    st.session_state["max_output"] = max_output
    return f"Constraints updated: Demand={demand}, Max Output={max_output}."

# 4. Update Optimization Methods
def update_optimization_methods(methods: list):
    """
    Updates the list of selected optimization methods.

    Args:
        methods (list): List of selected methods. Must be a subset of:
                        ["Genetic Algorithm", "Simulated Annealing", "Linear Programming"]

    Returns:
        str: Confirmation message.
    """
    valid_methods = ["Genetic Algorithm", "Simulated Annealing", "Linear Programming"]
    invalid_methods = [method for method in methods if method not in valid_methods]

    if invalid_methods:
        return f"Error: Invalid methods: {', '.join(invalid_methods)}"

    st.session_state["selected_methods"] = methods
    return f"Optimization methods updated: {', '.join(methods)}."

# 5. Run Configuration
def run_configuration():
    """
    Runs the optimization configuration and appends the results to session state.

    Returns:
        str: Confirmation message.
    """
    if "configurations" not in st.session_state:
        st.session_state["configurations"] = []

    new_configuration = {
        "settings": {
            "demand": st.session_state.get("demand", 800),
            "max_output": st.session_state.get("max_output", 500),
            "objective": st.session_state.get("objective", "Minimize Cost"),
            "methods": st.session_state.get("selected_methods", []),
        },
        "results": pd.DataFrame(
            np.random.randint(0, 100, (10, 10)), columns=[f"Time {i}" for i in range(10)]
        ),
        "comparison": pd.DataFrame([
            {"Algorithm": method, "Objective Value": np.random.randint(8000, 12000), "Time (s)": np.random.uniform(0.5, 2.0)}
            for method in st.session_state.get("selected_methods", [])
        ]),
    }
    st.session_state["configurations"].append(new_configuration)
    return "Configuration run successfully."