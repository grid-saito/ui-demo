import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from chat_interface.input import interface as chat_interface
from streamlit_float import float_init
from states.threads import (store_current_thread,
                            reset_session_state,
                            retrieve_history,
                            init_session_state)
from css.sidebar import past_searches_style
from dotenv import load_dotenv
from streamlit_float import float_css_helper, float_parent
from panels.map import render_map, create_weather_data
from panels.weather import render_weather_panels
from panels.demand import render_demand_curves
from panels.equipment_states import render_plant_states
from data.generate_samples import generate_demand_data, generate_plant_status_data, generate_results_data
from chat_interface.input import append_to_chat_history
from services.graph import get_input_confirmation, chat_about_input_data, get_suggested_actions
from langchain_core.messages.ai import AIMessage
from utils import get_current_thread_data, get_session_settings, save_session_settings
from panels.demand import demand_constraint_settings_panel
load_dotenv()


def set_page_settings(): 
    st.set_page_config(layout="wide")
    float_init(theme=True, include_unstable_primary=False)
    past_searches_style()
    dialog_wide_settings()


def dialog_wide_settings():
    st.markdown(
        """
    <style>
    div[data-testid="stDialog"] div[role="dialog"]:has(.big-dialog) {
        width: 80vw;
        height: 80vh;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


def get_default_settings():
    return {
            "settings": {
                "units": ["Unit 1", "Unit 2", "Unit 3", "Unit 4", "Unit 5"],
                "location": ["Matsuyama", "Tokushima", "Muroto", "Kochi", "Kotohira"],
                "type": ["LNG", "Coal", "Coal", "Nuclear", "LNG"],
                "max_output": [100, 200, 300, 400, 500],
                "startup_cost": [10.0, 20.0, 30.0, 40.0, 50.0],
                "operating_cost": [5.0, 10.0, 15.0, 20.0, 25.0],
                "shutdown_cost": [2.0, 4.0, 6.0, 8.0, 10.0],
                "demand": [1300, 1400, 1500, 599, 699, 799, 899, 999, 1099, 1199, 1299, 1399, 1499, 598, 698, 798, 898, 998, 1098, 1198, 1298, 1398, 1498, 597, 697, 797, 897, 997, 1097, 1197]},
            "chat_history": [],
            "results": None,
        }

    


def initialize_default_simulation():
    thread_id = "run1"
    if thread_id not in st.session_state.threads:
        st.session_state.threads.append(thread_id)
        st.session_state.thread_data[thread_id] = get_default_settings()
        st.session_state.current_thread = thread_id
        st.session_state.settings_before_change = get_default_settings()["settings"]
        append_to_chat_history(AIMessage("I can help you with visualizing and modifying the settings. How can I help you today?")) 


def _get_thread_data_key(key: str):
    """
    Retrieve a specific key's value from the current thread's data in session state.
    """
    current_thread = st.session_state.current_thread
    return st.session_state.thread_data[current_thread][key]


def sidebar():
    if st.sidebar.button("New Simulation"):
        # Store current thread before resetting for a new one
        store_current_thread()
        reset_session_state()
        thread_id = f"run{len(st.session_state.threads) + 1}"
        st.session_state.threads.append(thread_id)
        st.session_state.thread_data[thread_id] = get_default_settings()
        st.session_state.current_thread = thread_id
        st.toast(f"New thread '{thread_id}' created.")

    if st.sidebar.button("Run Simulation", key=f"{st.session_state.current_thread}"):
        # with the button clicked in the ui, we sent to graph that the settings is confirmed
        st.session_state.is_executed = True
        thread_id = st.session_state.current_thread
        thread_data = st.session_state.thread_data[thread_id]
        external_data = st.session_state.external_data
        output, confirm_results = get_input_confirmation(thread_data,
                                                         external_data["demand_data"],
                                                         external_data["plant_status"], 
                                                         external_data["weather_data"]) 
        st.session_state.confirm_results = confirm_results
        st.session_state.compability_check_result = output
        append_to_chat_history(AIMessage("Simulation is running... ")) 
        
    if False in st.session_state.confirm_results: 
        @st.dialog("Compatibility test result")
        def show_result_failed(output):
            # Add status box for Failed
            st.markdown("""
                <div style="
                    background-color: #f8d7da;
                    color: #842029;
                    padding: 10px;
                    border-radius: 5px;
                    border: 1px solid #f5c2c7;
                    text-align: center;
                    font-weight: bold;
                    margin-bottom: 15px;
                ">
                    ❌ FAILED
                </div>
            """, unsafe_allow_html=True)
            
            st.write(output)
            st.write("---")
            st.subheader("Suggested actions:")
            next_action = st.pills("Pick an action", 
                     options=["Replace unit 5 with unit 9",
                              "Replace unit 5 with unit 6", 
                              "Remove unit 5 from the settings",
                              "Set the maximum output of unit 4 to 1000",
                              "Override"], 
                     selection_mode="single", 
                     label_visibility="collapsed")
            
            if next_action == "Replace unit 5 with unit 9":
                append_to_chat_history(AIMessage("Replace unit 5 with unit 9"))
                result = chat_about_input_data("Replace unit 5 with unit 9 in the settings, use the same settings for unit 9 with unit 5, but just set the unit name set to unit 9", 
                                               _get_thread_data_key("chat_history"), 
                                               _get_thread_data_key("settings"))
                append_to_chat_history(AIMessage(result["output"]))
                st.session_state.confirm_results = []
                st.rerun()
            st.html("<span class='big-dialog'></span>") 

            if next_action == "Override":
                st.session_state.confirm_results = [True, True, True, True, True]
                st.rerun()

        show_result_failed(st.session_state.compability_check_result)
        #append_to_chat_history(AIMessage(output))
        st.session_state.is_confirmed = False

    # this should show whether it passed or not
    # dev: this will run the graph and update the states to retrieve results from the optjob. for now, the graph doesnt do much
    # dev: for now, use fake results data
    # todo: retrive results the state to update the results
    if st.session_state.confirm_results and all(st.session_state.confirm_results):
        @st.dialog("Compatibility test result")
        def show_result_passed(output):
            # Add status box for Passed
            st.markdown("""
                <div style="
                    background-color: #d1e7dd;
                    color: #0f5132;
                    padding: 10px;
                    border-radius: 5px;
                    border: 1px solid #badbcc;
                    text-align: center;
                    font-weight: bold;
                    margin-bottom: 15px;
                ">
                    ✅ PASSED
                </div>
            """, unsafe_allow_html=True)
                
            st.write(output)
            st.html("<span class='big-dialog'></span>") 

        append_to_chat_history(AIMessage("Simulation passed all the tests")) 
        # append_to_chat_history(AIMessage(output)) 
        append_to_chat_history(AIMessage("Do you need help with analyzing the data?")) 
        results_data = generate_results_data(thread_data=get_current_thread_data())
        show_result_passed(st.session_state.output)
        thread_data = get_current_thread_data()
        thread_data["results"] = results_data.to_dict(orient="list")
        st.session_state.is_confirmed = True 
         
        # this updates the local streamlit session state
        thread_data = st.session_state.thread_data[st.session_state.current_thread]
        st.session_state.thread_data[st.session_state.current_thread] = thread_data
        st.session_state.confirm_results = []

    
    st.sidebar.markdown("---")
    for i, thread_id in enumerate(st.session_state.threads):
        if st.sidebar.button(thread_id, key=f"thread_{i}", use_container_width=True):
            store_current_thread()
            retrieve_history(thread_id)
            

def settings_panel():
    if st.session_state.current_thread:
        thread_data = get_current_thread_data() 
        results_exists = thread_data["results"] is not None
        tabs = st.tabs(["Settings"])

        # Settings Tab
        with tabs[0]:
            sub_tabs = st.tabs(["Equipment", "Objective", "Constraint", "Optimization Methods"])

            # Equipment Settings Tab
            with sub_tabs[0]:
                settings = get_session_settings()
                if settings:
                    equipment = pd.DataFrame({
                            "Units": settings["units"],
                            "Locations": settings["location"],
                            "Type": settings["type"],
                            "Startup Cost": settings["startup_cost"],
                            "Operating Cost": settings["operating_cost"],
                            "Shutdown Cost": settings["shutdown_cost"],
                            "Max Output": settings["max_output"]})
                
                    updated_equipment = st.data_editor(
                        equipment, 
                        use_container_width=True, 
                        key=f"{st.session_state.current_thread}_equipment", 
                        disabled=results_exists
                    )
                    settings["location"] = updated_equipment["Locations"].tolist() 
                    settings["startup_cost"] = updated_equipment["Startup Cost"].tolist()
                    settings["operating_cost"] = updated_equipment["Operating Cost"].tolist()
                    settings["shutdown_cost"] = updated_equipment["Shutdown Cost"].tolist()
                    settings["max_output"] = updated_equipment["Max Output"].tolist() 
                    save_session_settings(settings)

            # Objective Tab
            with sub_tabs[1]:
                st.write("### Objective Function")
                settings["objective"] = st.radio(
                    "Select Objective",
                    ["Minimize Cost", "Maximize Output", "Balance Demand and Supply"],
                    index=["Minimize Cost", "Maximize Output", "Balance Demand and Supply"].index(
                        settings.get("objective", "Minimize Cost"), 
                    ),
                    disabled=results_exists
                )
                save_session_settings(settings) 
            
            # Constraint Tab
            with sub_tabs[2]:
                st.write("### Constraints")
                settings = get_session_settings()
                demand_constraint_settings_panel(settings)
                
            # Optimization Methods Tab
            with sub_tabs[3]:
                st.write("### Optimization Methods")
                settings = get_session_settings()
                settings["methods"] = st.multiselect(
                    "Select Optimization Methods",
                    ["Genetic Algorithm", "Simulated Annealing", "Linear Programming"],
                    default=settings.get("methods", ["Genetic Algorithm"]),
                    disabled=results_exists
                )
                save_session_settings(settings)


def input_data_visualization_panel(results):
    settings = get_session_settings()
    equipment = pd.DataFrame({
                            "units": settings["units"],
                            "location": settings["location"],
                            "type": settings["type"],
                            "startup_cost": settings["startup_cost"],
                            "operating_cost": settings["operating_cost"],
                            "shutdown_cost": settings["shutdown_cost"],
                            "max_output": settings["max_output"]})
    tabs = st.tabs(["maps", "weather", "demand", "equpiment states", "result"])
     
    if settings["location"] != st.session_state.previous_location or settings["location"] is None:
        st.session_state.previous_location = settings["location"]
        weather_data, weather_data_w_unit_info = create_weather_data(equipment)
        st.session_state.external_data["weather_data"] = weather_data
        st.session_state.external_data["weather_data_w_unit_info"] = weather_data_w_unit_info

    with tabs[0]:
        render_map(st.session_state.external_data["weather_data_w_unit_info"])

    with tabs[1]:
        render_weather_panels(st.session_state.external_data["weather_data"])
    
    with tabs[2]:
        # Allow the user to select regions
        thread_data = get_current_thread_data()
        if st.session_state.external_data["demand_data"] is None:
            demand_data = generate_demand_data()
            st.session_state.external_data["demand_data"] = demand_data 
        else: 
            demand_data = st.session_state.external_data["demand_data"]
        
        render_demand_curves(demand_data, thread_data["results"])
   
    with tabs[3]:
        plant_status = generate_plant_status_data()
        render_plant_states(plant_status, settings["units"])
        st.session_state.external_data["plant_status"] = plant_status

    with tabs[4]:
        if results:
            cols = st.columns(2)
            with cols[0]:
                st.dataframe(results, use_container_width=True)
            with cols[1]:
                # Create the stacked bar chart using Plotly
                fig = go.Figure()

                # Iterate over all columns except 'Timestamp' to create bars
                df = pd.DataFrame(results)
                for col in df.columns[1:]:  # Skip the 'Timestamp' column
                    fig.add_trace(go.Bar(x=df["Timestamp"], y=df[col], name=col))

                # Update layout for the chart
                fig.update_layout(
                    xaxis_title="Time [day]",
                    yaxis_title="Output [kW]",
                    barmode="stack",  # Stack bars for comparison
                    title="Stacked Bar Chart of Unit Outputs",
                    xaxis=dict(tickangle=45),  # Rotate x-axis labels for better readability
                )

                # Display the chart in Streamlit
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("None")

def page():
    #st.write(get_current_node(st.session_state.current_thread))
    main_col, chat_col = st.columns([3, 1])
    with main_col:
        settings_css = float_css_helper(
                    width="61%",  # Full width of the column
                    height="100%",  # Fixed height
                    top="5rem",  # Floored at the bottom
                    z_index="1000",  # High z-index to prevent overlapping
                )
        float_parent(css=settings_css)
        if st.session_state.current_thread:
            tabs = st.tabs(["Visualization"])
            
            # Settings Tab
            with st.container(): 
                settings_panel()
            
            with st.container():
                with tabs[0]:
                    results = st.session_state.thread_data[st.session_state.current_thread]["results"]
                    input_data_visualization_panel(results)
                    
        else:
            st.write("No thread selected. Create or select a thread from the sidebar.")
    
    # Chat Interface on the right
    with chat_col:
        chat_interface()  # Render chat interface


set_page_settings()
init_session_state()
initialize_default_simulation()
sidebar()
page()