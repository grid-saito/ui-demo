import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from langchain_core.tools import tool
import streamlit as st
from tools.BaseToolkit import BaseToolkit

# Initialize session state if not already done
if "thread_data" not in st.session_state:
    st.session_state.thread_data = {}
if "current_thread" not in st.session_state:
    st.session_state.current_thread = None


def get_data(relevant_data: str):
    """
    Retrieve data based on the relevant_data parameter.

    Parameters:
        relevant_data (str): Either "settings" or "results".

    Returns:
        pd.DataFrame: The corresponding data as a DataFrame.

    Raises:
        ValueError: If relevant_data is not "settings" or "results".
    """
    if st.session_state.current_thread is None:
        raise ValueError("No current thread selected.")
    
    thread_data = st.session_state.thread_data.get(st.session_state.current_thread, {})
    if relevant_data == "settings":
        data = thread_data.get("settings", {})
        # dont include demand in the data since it has different length than others
    elif relevant_data == "results":
        data = thread_data.get("results", {})
    else:
        raise ValueError(f"Invalid relevant_data value: {relevant_data}. Must be 'settings' or 'results'.")
    
    # Remove keys
    data_copy = data.copy()    
    data_copy.pop("demand", None)
    data_copy.pop("objective", None)
    data_copy.pop("methods", None)
    return pd.DataFrame(data_copy)

@tool
def scatter_plot(
    x: str, 
    y: str, 
    relevant_data: str, 
    color: str = None, 
    size: str = None, 
    title: str = "Scatter Plot", 
    hover_data: list = None
) -> str:
    """
    Creates a scatter plot.

    Parameters:
        x (str): Column name for x-axis.
        y (str): Column name for y-axis.
        relevant_data (str): Either "settings" or "results".
        color (str, optional): Column for color coding.
        size (str, optional): Column for point size.
        title (str, optional): Plot title. Defaults to "Scatter Plot".
        hover_data (list, optional): Columns to show on hover.

    """
    df = get_data(relevant_data)
    fig = px.scatter(df, x=x, y=y, color=color, size=size, title=title, hover_data=hover_data)
    image_path = "scatter_plot.png"
    fig.write_image(image_path)
    with st.expander("Scatter Plot"):
        st.image(image_path, caption="Scatter Plot", use_container_width=True)

@tool
def line_chart(
    x: str, 
    y: str, 
    relevant_data: str, 
    color: str = None, 
    title: str = "Line Chart"
) -> str:
    """
    Creates a line chart.

    Parameters:
        x (str): Column name for x-axis.
        y (str): Column name for y-axis.
        relevant_data (str): Either "settings" or "results".
        color (str, optional): Column for color coding.
        title (str, optional): Plot title. Defaults to "Line Chart".

    """
    df = get_data(relevant_data)
    fig = px.line(df, x=x, y=y, color=color, title=title)
    image_path = "line_chart.png"
    fig.write_image(image_path)
    with st.expander("Line Chart"):
        st.image(image_path, caption="Line Chart", use_container_width=True)

@tool
def bar_chart(
    x: str, 
    y: str, 
    relevant_data: str, 
    color: str = None, 
    title: str = "Bar Chart", 
    barmode: str = "group"
) -> str:
    """
    Creates a bar chart.

    Parameters:
        x (str): Column name for x-axis.
        y (str): Column name for y-axis.
        relevant_data (str): Either "settings" or "results".
        color (str, optional): Column for color coding.
        title (str, optional): Plot title. Defaults to "Bar Chart".
        barmode (str, optional): Bar mode (e.g., "group" or "stack"). Defaults to "group".

    """
    df = get_data(relevant_data)
    fig = px.bar(df, x=x, y=y, color=color, title=title, barmode=barmode)
    image_path = "bar_chart.png"
    fig.write_image(image_path)
    with st.expander("Bar Chart"):
        st.image(image_path, caption="Bar chart", use_container_width=True)

@tool
def histogram(
    x: str, 
    relevant_data: str, 
    color: str = None, 
    title: str = "Histogram", 
    nbins: int = 20
) -> str:
    """
    Creates a histogram.

    Parameters:
        x (str): Column name for the data.
        relevant_data (str): Either "settings" or "results".
        color (str, optional): Column for color coding.
        title (str, optional): Plot title. Defaults to "Histogram".
        nbins (int, optional): Number of bins. Defaults to 20.

    """
    df = get_data(relevant_data)
    fig = px.histogram(df, x=x, color=color, title=title, nbins=nbins)
    image_path = "histogram.png"
    fig.write_image(image_path)
    with st.expander("Histogram"):
        st.image(image_path, caption="Histogram", use_container_width=True)

@tool
def pie_chart(
    names: str, 
    values: str, 
    relevant_data: str, 
    title: str = "Pie Chart"
) -> str:
    """
    Creates a pie chart.

    Parameters:
        names (str): Column for slice names.
        values (str): Column for slice values.
        relevant_data (str): Either "settings" or "results".
        title (str, optional): Plot title. Defaults to "Pie Chart".

    """
    df = get_data(relevant_data)
    fig = px.pie(df, names=names, values=values, title=title)
    image_path = "pie_chart.png"
    fig.write_image(image_path)
    with st.expander("Pie Chart"):
        st.image(image_path, caption="Pie chart", use_container_width=True)


# Toolkit Definition
class VisualizationToolkit(BaseToolkit):
    def __init__(self):
        self.tools = {
            "scatter_plot": scatter_plot,
            "line_chart": line_chart,
            "bar_chart": bar_chart,
            "histogram": histogram,
            "pie_chart": pie_chart,
        }