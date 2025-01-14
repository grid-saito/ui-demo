import streamlit as st


# Function to add debug messages to logs
def add_debug_message(message):
    st.session_state["debug_logs"].append(message)


def get_current_thread_data():
    thread_data = st.session_state.thread_data[st.session_state.current_thread]
    return thread_data


def set_current_thread_data(thread_data):
    st.session_state.thread_data[st.session_state.current_thread] = thread_data


def get_session_settings(latest: bool = True):
    """
    Retrieve the last or second-to-last settings entry for the current thread.

    Parameters:
        latest (bool): If True, get latest settings, if False get previous settings

    Returns:
        dict: Settings dictionary
    """
    current_thread = st.session_state.get("current_thread")
    settings = st.session_state.thread_data[current_thread].get("settings")
    if latest is False:
        settings = st.session_state.settings_before_change
    return settings


def save_session_settings(thread_state: dict):
    """
    Append the new settings to the session state list only if they are different 
    from the last entry.
    
    Parameters:
        thread_state (dict): New settings to save
    """
    current_thread = st.session_state.get("current_thread")
    st.session_state.thread_data[current_thread]["settings"] = thread_state
    
