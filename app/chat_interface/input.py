import streamlit as st
from streamlit_float import float_css_helper, float_parent
from chat_interface.history import render_chat_history
from langchain_core.messages import AIMessage, HumanMessage
from services.graph import chat_about_input_data
from services.graph import chat_about_result_data
from utils import get_session_settings, save_session_settings
import plotly.graph_objects as go
from panels.demand import demand_forecast_dialog, demand_constraint_dialog


def confirm_changes(before_data: dict, after_data: dict) -> bool:
    """
    Show confirmation dialog and return whether changes were confirmed.

    Parameters:
        before_data (dict): Original data state
        after_data (dict): Modified data state

    Returns:
        bool: True if changes were confirmed, False otherwise
    """

    @st.dialog("Review Data Changes", width="large")
    def show_dialogue():
        # Create markdown table headers
        headers = ["Unit", "Location", "Type", "Max Output", "Startup Cost", "Operating Cost", "Shutdown Cost"]
        header_row = "| " + " | ".join(headers) + " |\n"
        divider_row = "|" + "|".join(["---" for _ in headers]) + "|\n"

        # Generate Before Table
        before_table = header_row + divider_row
        for i in range(len(before_data['units'])):
            row = []
            for key in ['units', 'location', 'type', 'max_output', 'startup_cost', 'operating_cost', 'shutdown_cost']:
                val = before_data[key][i]
                if after_data[key][i] != val:  # Highlight changed values in red
                    val = f"**:red[{val}]**"
                row.append(str(val))
            before_table += "| " + " | ".join(row) + " |\n"

        # Generate After Table
        after_table = header_row + divider_row
        for i in range(len(after_data['units'])):
            row = []
            for key in ['units', 'location', 'type', 'max_output', 'startup_cost', 'operating_cost', 'shutdown_cost']:
                val = after_data[key][i]
                if before_data[key][i] != val:  # Highlight changed values in green
                    val = f"**:green[{val}]**"
                row.append(str(val))
            after_table += "| " + " | ".join(row) + " |\n"

        # Display Tables Side by Side
        col1, col_arrow, col2 = st.columns([0.45, 0.1, 0.45])

        with col1:
            st.markdown("### Before Changes")
            st.markdown(before_table)

        with col_arrow:
            # Use custom HTML to position the arrow lower
            st.markdown(
                """
                <div style='display: flex; flex-direction: column; height: 100%; justify-content: flex-end;'>
                    <div style='margin-top: auto;'>
                        <span style='font-size: 24px; color: #666;'>➡️</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown("### After Changes")
            st.markdown(after_table)

        # Add buttons at the bottom
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Revert", type="secondary", use_container_width=True):
                # Revert changes logic
                thread_state = get_session_settings()
                chat_history = thread_state.get("chat_history", [])
                chat_history.append({
                    "role": "assistant",
                    "content": "The changes were reverted to previous state"
                })
                thread_state["chat_history"] = chat_history
                save_session_settings(thread_state)
                st.rerun()
        with col2:
            if st.button("Confirm", type="primary", use_container_width=True):
                thread_state = get_session_settings()
                chat_history = thread_state.get("chat_history", [])
                chat_history.append({
                    "role": "assistant",
                    "content": "Changes were confirmed"
                })
                thread_state["chat_history"] = chat_history
                save_session_settings(thread_state)
                st.session_state.settings_before_change = thread_state
                st.rerun()
        st.html("<span class='big-dialog'></span>") 
    show_dialogue()

# --- Main Chat Interface ---
def interface():
    """
    Main interface for the chat system. Handles user input, displays chat history,
    and processes AI responses.
    """
    render_chat_history()
    user_message = ""
    option_map = {
        0: "visualize",
        1: "modify"
    }
    with st.container():
        selection = st.segmented_control("Select Mode",
                                         options=option_map.values(), 
                                         selection_mode="single")
        user_message = st.chat_input("メッセージを送信する", key="chat_input")
        button_css = float_css_helper(width="2.2rem", bottom="4.5rem", transition=0)
        float_parent(css=button_css)
        if "selection" not in st.session_state:
            st.session_state.selection = selection
        st.session_state.selection = selection
    
    if user_message:
        _add_chat_message("user", user_message)
        if _get_thread_data_key("results") is None: 
            ai_response = chat_about_input_data(user_message, 
                                                _get_thread_data_key("chat_history"), 
                                                _get_thread_data_key("settings"))
            _add_chat_message("assistant", ai_response["output"])
            
            if st.session_state.selection == "modify":
                # todo: get the flow here correct by the demo
                after_change = get_session_settings(latest=True)
                before_change = st.session_state.settings_before_change
                
                # check using copy version whether changes were made or not 
                before_change_copy = {k: before_change[k] for k in [
                    'units', 'location', 'type', 'max_output', 
                    'startup_cost', 'operating_cost', 'shutdown_cost'
                ]}
                after_change_copy = {k: after_change[k] for k in [
                    'units', 'location', 'type', 'max_output', 
                    'startup_cost', 'operating_cost', 'shutdown_cost'
                ]}
                    
                if before_change_copy != after_change_copy:
                    confirm_changes(before_change_copy, after_change_copy)
                
                if "demand_forecast_dialogue_closed" not in st.session_state:
                    st.session_state["demand_forecast_dialogue_closed"] = False
                
                if "demand forecast" in user_message: 
                    demand_forecast_before = st.session_state.external_data["demand_data"]
                    # for the sake of the demo, we assume the demand forecast is the same as the before change
                    demand_forecast_after = demand_forecast_before
                    demand_forecast_dialog(demand_forecast_before, demand_forecast_after)
                    _add_chat_message("assistant", "Demand forecast has been changed, lets update the demand constraint.")
                    
                if "yes" in user_message:
                    demand_constraint_dialog()
        else: 
            ai_response = chat_about_result_data(user_message, 
                                                _get_thread_data_key("chat_history"),
                                                _get_thread_data_key("settings"),
                                                st.session_state["external_data"]["demand_data"],
                                                st.session_state["external_data"]["plant_status"],
                                                _get_thread_data_key("results"))
            _add_chat_message("assistant", ai_response["output"])
    
    # st.write(st.session_state.is_executed)
    if st.session_state.is_executed:
        if st.session_state.is_confirmed:
            #success_query = [
            #    "check that the total results output satisfies the forecasts",
            #    "what is the mape between the high forecast and total output",
            #    "suggest ways to change settings to satisfy the demand"
            #]
            # dev: no buttons for now
            success_query = []
            for query in success_query:
                if st.button(query, key=f"button_{query}"):  # Create a unique key for each button
                    ai_response = chat_about_input_data(
                        query + ". do not include any calculations you made, just return the results",
                        _get_thread_data_key("chat_history"),  # Function to get thread data
                        _get_thread_data_key("settings")      # Function to get settings
                    )
                    _add_chat_message("assistant", ai_response["output"])  # Function to add a chat message
        else: 
            fail_query = "replace the unit 5 with unit 6"
            if st.session_state.fail_query_button_visible: 
                if st.button(fail_query): 
                    ai_response = chat_about_input_data("replace the unit 5 with unit 6, use same the specifications for unit 6 as unit 5", 
                                                        _get_thread_data_key("chat_history"), 
                                                        _get_thread_data_key("settings"))
                    _add_chat_message("assistant", ai_response["output"])
                    st.session_state.fail_query_button_visible = False 
                 
    
# --- Chat Management ---
def _get_thread_data_key(key: str):
    """
    Retrieve a specific key's value from the current thread's data in session state.
    """
    current_thread = st.session_state.current_thread
    return st.session_state.thread_data[current_thread][key]


def append_to_chat_history(message):
    """
    Append a message to the chat history of the current thread.
    """
    current_thread = st.session_state.current_thread
    if "chat_history" not in st.session_state.thread_data[current_thread]:
        st.session_state.thread_data[current_thread]["chat_history"] = []
    
    st.session_state.thread_data[current_thread]["chat_history"].append(message)


def _add_chat_message(role, content):
    """
    Add a message to the chat display and save it to the session state chat history.
    """
    with st.chat_message(role):
        st.write(content)

    if role == "user":
        append_to_chat_history(HumanMessage(content))
    elif role == "assistant":
        append_to_chat_history(AIMessage(content))


# --- Response Display ---
def display_response(response):
    """
    Display the AI's response in the chat.
    """
    _add_chat_message("assistant", response)