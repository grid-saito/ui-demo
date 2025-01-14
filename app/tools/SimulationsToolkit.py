import streamlit as st
from langchain_core.tools import tool
from tools.BaseToolkit import BaseToolkit
from data.generate_samples import generate_results_data


@tool
def create_new_simulation() -> str:
    """
    Creates a new simulation thread, initializes its data, and sets it as the current thread.

    Parameters:
        params (dict): A dictionary of simulation parameters. Unused here, but keeps the format consistent.

    Returns:
        str: A message indicating the creation of the new simulation.
    """
    new_simulation_name = f"run{len(st.session_state.thread_data) + 1}"

    st.session_state.thread_data[new_simulation_name] = {
        "settings": {
            "demand": 800,
            "max_output": 500,
            "objective": "Minimize Cost",
            "methods": ["Genetic Algorithm"],
            "equipment_settings": None,
        },
        "results": None,
        "chat_history": [],
    }

    st.session_state.current_thread = new_simulation_name
    return f"New simulation '{new_simulation_name}' created and selected."


@tool
def switch_to_simulation(thread_name: str) -> str:
    """
    Switches the current thread to an existing simulation thread.

    Parameters:
        - thread_name (str): The name of the thread to switch

    Returns:
        str: A message indicating success or failure of switching simulations.
    """
    simulation_name = thread_name
    if simulation_name in st.session_state.thread_data:
        st.session_state.current_thread = simulation_name
        return f"Switched to simulation '{simulation_name}'."
    else:
        return f"Simulation '{simulation_name}' does not exist."


@tool
def get_all_simulations() -> dict:
    """
    Retrieves a list of all available simulation names.

    Parameters:
        params (dict): Unused, but included for consistency with the format.

    Returns:
        dict: A dictionary containing all simulation names under the key 'simulations'.
    """
    return {"simulations": list(st.session_state.thread_data.keys())}


@tool
def get_current_simulation_data() -> dict:
    """
    Retrieves the data of the currently selected simulation thread.

    Parameters:
        None
        
    Returns:
        dict: Data for the current simulation thread, or an empty dictionary if no thread is selected.
    """
    if st.session_state.current_thread:
        return st.session_state.thread_data.get(st.session_state.current_thread, {})
    return {}

# dev: under construction
@tool
def run_simulation() -> str:
    """
    Runs a simulation for the current thread and generates results.

    Parameters:
        None
    Returns:
        str: A message indicating that the simulation was run.
    """
 # with the button clicked in the ui, we sent to graph that the settings is confirmed
    thread_id = st.session_state.current_thread
    thread_data = st.session_state.thread_data[thread_id]
    external_data = st.session_state.external_data
    return f"Simulation ran successfully."


# Toolkit Definition
class SimulationsToolkit(BaseToolkit):
    def __init__(self):
        super().__init__({
            "create_new_simulation": create_new_simulation,
            "switch_to_simulation": switch_to_simulation,
            "get_all_simulations": get_all_simulations,
            "get_current_simulation_data": get_current_simulation_data,
            "run_simulation": run_simulation
        })