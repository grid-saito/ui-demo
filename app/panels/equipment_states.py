import streamlit as st
from itertools import zip_longest
import random


def render_plant_states(plant_status_data, simulated_units):
    """
    Render plant states in two rows with a thicker border for simulated units.
    """
    status_color = {
        "Active": "#5cb85c",
        "Maintenance": "#f0ad4e",
        "Standby": "#d9534f",
    }
    
    # Split plant statuses into two groups
    num_columns = len(plant_status_data) // 2 + len(plant_status_data) % 2
    grouped_data = [plant_status_data.iloc[i:i + num_columns] for i in range(0, len(plant_status_data), num_columns)]
    
    # Render each group in its own row
    for group in grouped_data:
        cols = st.columns(len(group))
        for col, (_, row) in zip(cols, group.iterrows()):
            is_simulated = row['unit_name'] in simulated_units
            border_style = "3px solid #007bff" if is_simulated else "1px solid #ddd"
            shadow_style = "0 4px 12px rgba(0, 0, 0, 0.2)" if is_simulated else "0 4px 8px rgba(0, 0, 0, 0.1)"
            
            # Get fuel capacity for this unit
            capacity = row['fuel_capacity']
            current_fuel = row["fuel_level"]
            fuel_percentage = (current_fuel / capacity) * 100
            
            # Define fuel level color based on percentage
            if fuel_percentage > 60:
                fuel_color = "#5cb85c"  # Green
            elif fuel_percentage > 30:
                fuel_color = "#f0ad4e"  # Orange
            else:
                fuel_color = "#d9534f"  # Red
            
            col.markdown(
                f"""
                <div style="
                    border: {border_style}; 
                    border-radius: 10px; 
                    padding: 10px; 
                    text-align: center; 
                    background: White; 
                    box-shadow: {shadow_style};
                ">
                    <h3 style="color: {status_color[row['status']]};">{row['unit_name']}</h3>
                    <p><strong>Status:</strong> <span style="color: {status_color[row['status']]};">{row['status']}</span></p>
                    <p><strong>Current Output:</strong> {row['output']} MW</p>
                    <p><strong>Last Maintenance:</strong> {row['last_maintenance']}</p>
                    <div style="margin: 5px 0;">
                        <div style="
                            width: 100%;
                            height: 20px;
                            background: #f0f0f0;
                            border-radius: 10px;
                            overflow: hidden;
                            border: 1px solid #ddd;
                            margin-top: 2px;
                        ">
                            <div style="
                                width: {fuel_percentage}%;
                                height: 100%;
                                background-color: {fuel_color};
                                transition: width 0.3s ease;
                            "></div>
                        </div>
                        <span style="font-size: 0.8em; color: {fuel_color};">
                            {current_fuel}/{capacity} tons ({fuel_percentage:.1f}%)
                        </span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )