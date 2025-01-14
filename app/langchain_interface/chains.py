import streamlit as st 
import pandas as pd
from services.azure import chat_model
from tools.VisualizationToolkit import VisualizationToolkit
from tools.SettingsToolkit import SettingsToolkit
from tools.SimulationsToolkit import SimulationsToolkit
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain import hub


def _get_chat_model_w_tools():
    visual_toolkit = VisualizationToolkit()
    settings_toolkit = SettingsToolkit()
    #simulations_toolkit = SimulationsToolkit()
    
    tools = visual_toolkit.get_tools() + settings_toolkit.get_tools() # + simulations_toolkit.get_tool_names()
    prompt = hub.pull("hwchase17/openai-tools-agent")
    agent = create_openai_tools_agent(chat_model, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor


def _format_session_states():
    """
    Format the current session states into a structured and readable format.
    
    Returns:
        str: A formatted string representation of all session state values.
    """
    formatted_states = []

    for key, value in st.session_state.items():
        if isinstance(value, pd.DataFrame):
            # For DataFrames, include a summary of shape and column names
            formatted_states.append(f"{key}:\n  DataFrame with shape {value.shape} and columns {list(value.columns)}")
        elif isinstance(value, list):
            # For lists, show up to 3 items for brevity
            formatted_states.append(f"{key}:\n  List with {len(value)} items: {value[:3]}{'...' if len(value) > 3 else ''}")
        elif isinstance(value, dict):
            # For dicts, show key-value pairs up to 3 entries
            formatted_states.append(f"{key}:\n  Dict with keys: {list(value.keys())[:3]}{'...' if len(value) > 3 else ''}")
        else:
            # For other data types, show their value directly
            formatted_states.append(f"{key}: {value}")

    return "\n".join(formatted_states)



def chain():
    formatted_session_states = _format_session_states()
    prompt = f"""
    Answer the user's questions based on the below query, chat history, and session states. 
    If necessary, use the tools to modify or visualize the session states. 
    
    <session_states>
    {formatted_session_states}
    </session_states>
    """
    
    chain = _get_chat_model_w_tools()
    return chain


def create_response(query, chat_history): 
    formatted_session_states = _format_session_states()
    prompt = f"""
    Answer the user's questions based on the below query, chat history, and session states. 
    If necessary, use the tools to modify or visualize the session states. 
    
    <session_states>
    {formatted_session_states}
    </session_states>
    """
    
    chat_model_w_tools = _get_chat_model_w_tools()
    response = chat_model_w_tools.invoke({"input": query + prompt, 
                                         "chat_history": chat_history})
    return response