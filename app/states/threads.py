import streamlit as st


# Initialize session state
def init_session_state():
    if "threads" not in st.session_state:
        st.session_state.threads = []
    if "current_thread" not in st.session_state:
        st.session_state.current_thread = None
    if "thread_data" not in st.session_state:
        st.session_state.thread_data = {}
    if "compatibility_info_message" not in st.session_state:
        st.session_state.compatibility_info_message = ""
    if "external_data" not in st.session_state:
        st.session_state.external_data = {}
        st.session_state.external_data["demand_data"] = None
    if "previous_location" not in st.session_state:
        st.session_state.previous_location = None
    if "weather_data" not in st.session_state:
        st.session_state.previous_location = None
    if "weather_data_w_unit_info" not in st.session_state:
        st.session_state.previous_location = None
    if "is_confirmed" not in st.session_state:
        st.session_state.is_confirmed = False
    if "settings_before_change" not in st.session_state:
        st.session_state.settings_before_change = {}
    if "is_executed" not in st.session_state:
        st.session_state.is_executed = False
    if "dialogue_message" not in st.session_state: 
        st.session_state.dialogue_message = ""
    if "fail_query_button_visible" not in st.session_state:
        st.session_state.fail_query_button_visible = False
    if "confirm_results" not in st.session_state:
        st.session_state.confirm_results = []
    if "output" not in st.session_state:
        st.session_state.output = None
# Reset session state
def reset_session_state():
    st.session_state.current_thread = None


# Store current thread, including chat history and all settings
def store_current_thread():
    """
    Stores the current thread's data in session state, including settings, results, and chat history.
    Ensures the full structure of the settings is preserved.
    """
    current_thread = st.session_state.current_thread

    if current_thread:
        # Retrieve the current thread data
        thread_data = st.session_state.thread_data[current_thread]
        st.session_state.thread_data[current_thread] = {
            "settings": {
                "units": thread_data["settings"].get("units"),
                "location": thread_data["settings"].get("location"),
                "max_output": thread_data["settings"].get("max_output"),
                "type": thread_data["settings"].get("type"),
                "startup_cost": thread_data["settings"].get("startup_cost"),
                "operating_cost": thread_data["settings"].get("operating_cost"),
                "shutdown_cost": thread_data["settings"].get("shutdown_cost"),
                "demand": thread_data["settings"].get("demand"),
                "objective": thread_data["settings"].get("objective"),
                "methods": thread_data["settings"].get("methods"),
            },
            "results": thread_data.get("results"),
            "chat_history": thread_data.get("chat_history", []),
        }
        st.session_state.settings_before_change = st.session_state.thread_data[current_thread]["settings"]


# Retrieve thread history, including chat history
def retrieve_history(thread_name):
    if thread_name in st.session_state.threads:
        st.session_state.current_thread = thread_name
