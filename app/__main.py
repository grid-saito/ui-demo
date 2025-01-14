from services.graph import (run_graph, 
                            create_new_thread, 
                            sync_input_data_confirmation_with_graph, 
                            sync_data_with_graph)
from data.generate_samples import generate_demand_data, generate_plant_status_data
import streamlit as st
from panels.map import create_weather_data
import pandas as pd
from langchain_core.messages import HumanMessage

thread_id = "run1"
st.session_state.current_thread = thread_id
st.session_state.thread_data[thread_id] = {
            "settings": {
                "num_units": 5,
                "units": ["Unit 1", "Unit 2", "Unit 3", "Unit 4", "Unit 5"],
                "location": ["Matsuyama", "Kochi", "Iyo", "Miyaji", "Nagao"],
                "type": ["LNG", "Coal", "Coal", "Nuclear", "LNG"],
                "max_output": [100, 200, 300, 400, 500],
                "startup_cost": [10.0, 20.0, 30.0, 40.0, 50.0],
                "operating_cost": [5.0, 10.0, 15.0, 20.0, 25.0],
                "shutdown_cost": [2.0, 4.0, 6.0, 8.0, 10.0],
                "demand": [800, 900, 1000, 1100, 1200]}, 
            "chat_history": [],
            "results": None,
        }

thread_id = st.session_state.current_thread
thread_data = st.session_state.thread_data[thread_id]

settings_data = thread_data["settings"] 
create_new_thread(thread_id)
sync_data_with_graph(thread_id, "input_data", data=settings_data)
del settings_data["num_units"]

equipment = pd.DataFrame(settings_data)
weather_data = create_weather_data(equipment)
sync_data_with_graph(thread_id, "weather_data", weather_data.to_dict(orient="list"))

demand_data = generate_demand_data()
sync_data_with_graph(thread_id, "demand_data", demand_data.to_dict(orient="list"))
 
plant_status = generate_plant_status_data()
st.write(plant_status.to_dict(orient="dict"))
sync_data_with_graph(thread_id, "plant_status", plant_status.to_dict(orient="list"))

run_graph(thread_id, [HumanMessage("based on the demand data and plant status, is the current input data settings resonable?")])
run_graph(thread_id, [HumanMessage("what is the weather forecast of matsuyama?")])
run_graph(thread_id, [HumanMessage("what should i do with the demand settings?")])
run_graph(thread_id, [HumanMessage("should i change any of the unit settings based on the plant status?")])
sync_input_data_confirmation_with_graph(thread_id, input_data_confirmed=True)