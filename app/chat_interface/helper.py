import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from chat_interface.history import get_chat_history, update_chat_history

# dev: want to get the user started on the chat interface, halfway through implementation. come back later


def initial_message():
    # Display the assistant's initial message
    with st.chat_message("assistant"): 
        st.write("What can I do for you today?")
    
    # Define the button actions
    actions = {
        "Set Input Settings": "set_input_settings",
        "Visualize Settings Data": "visualize_settings_data",
        "Visualize Results Data": "visualize_results_data",
        "Analyze Data": "analyze_data",
    }

    with st.chat_message("assistant"): 
        # Arrange buttons in two columns
        col1, col2 = st.columns(2)
        with col1:
            for label, action in list(actions.items())[:2]:  # First half of the buttons
                if st.button(label, key=action):  # Unique key to avoid conflicts
                    handle_user_action(action)
        with col2:
            for label, action in list(actions.items())[2:]:  # Second half of the buttons
                if st.button(label, key=action):  # Unique key to avoid conflicts
                    handle_user_action(action)


def handle_user_action(action):
    if action == "set_input_settings":
        st.write("Set Input Settings action triggered.")
    elif action == "visualize_settings_data":
        st.write("Visualizing Settings Data...")
    elif action == "visualize_results_data":
        st.write("Visualizing Results Data...")
    elif action == "analyze_data":
        st.write("Analyzing Data...")