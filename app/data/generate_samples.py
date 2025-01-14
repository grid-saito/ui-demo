import random
import pandas as pd
from datetime import datetime, timedelta
import numpy as np


FUEL_CAPACITY = {
    "Unit 1": 1000,
    "Unit 2": 1200,
    "Unit 3": 800,
    "Unit 4": 1500,
    "Unit 5": 1000,
    "Unit 6": 1200,
    "Unit 7": 1300,
    "Unit 8": 900,
    "Unit 9": 1100,
    "Unit 10": 1400,
}

# Sample session state settings for Units
def get_session_state_settings():
    return {
        "Units": ["Unit 1", "Unit 2", "Unit 3", "Unit 4", "Unit 5"],
        "Max Output": [100, 200, 300, 400, 500],
    }


# Generate plant status data
def generate_plant_status_data():
    """
    Generate plant status data for 10 units, ensuring specific conditions:
    - Units 1-4 are 'Active'.
    - Unit 5 is 'Maintenance'.
    - Units 6-10 have randomly assigned statuses ('Active', 'Maintenance', 'Standby').

    Returns:
        pd.DataFrame: DataFrame containing plant status data.
    """
    units = [f"Unit {i}" for i in range(1, 11)]  # Units 1 to 10
    random.seed(42)
    max_outputs = [random.randint(100, 500) for _ in units]  # Random max outputs for each unit
    statuses = ["Active", "Maintenance", "Standby"]
    plant_status_data = []

    for i, (unit, max_output) in enumerate(zip(units, max_outputs), start=1):
        if i <= 4:  # Units 1-4 are 'Active'
            status = "Active"
        elif i == 5:  # Unit 5 is 'Maintenance'
            status = "Maintenance"
        else:  # Units 6-10 have random statuses
            status = random.choice(statuses)

        # Determine current output: only for 'Active' status
        current_output = random.randint(0, max_output) if status == "Active" else 0

        # Randomize maintenance dates
        last_maintenance = datetime.now() - timedelta(days=random.randint(30, 365))

        # Get fuel capacity from constant and generate random current fuel level
        capacity = FUEL_CAPACITY[unit]
        current_fuel = random.randint(int(capacity * 0.2), capacity)  # Always keep at least 20% fuel

        # Append the plant status data
        plant_status_data.append({
            "unit_name": unit,
            "status": status,
            "output": current_output,
            "max_output": max_output,
            "last_maintenance": last_maintenance.strftime("%Y-%m-%d"),
            "fuel_level": current_fuel,
            "fuel_capacity": capacity,
        })

    return pd.DataFrame(plant_status_data)

# Function to generate demand data
def generate_demand_data():
    demand_data = []
    timestamps = [(datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(0, 30, 1)]

    for timestamp in timestamps:
        demand = random.randint(500, 1500)  # Random demand values
        demand_data.append({
            "Timestamp": timestamp,
            "Demand": demand,
        })

    return pd.DataFrame(demand_data)


def generate_results_data(thread_data):
    """
    Generate results DataFrame with random data and timestamps, ensuring the required structure.

    Args:
        thread_data (dict): Dictionary to store results data.
        num_timesteps (int): Number of timesteps to generate results for.

    Returns:
        None: Updates the `thread_data` dictionary with the generated results.
    """

    if "settings" not in thread_data or "units" not in thread_data["settings"]:
        raise ValueError("Thread data must include 'settings' with a 'units' key.")
    timestamps = [(datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(0, 30, 1)]
    units = thread_data["settings"]["units"]  # Fetch unit names
    
    num_timestamps = len(timestamps)
    
    # Generate random values for each unit
    data = {
        "Timestamp": timestamps
    }
    for unit in units: 
        data[f"{unit}"] = [random.randint(100, 300) for _ in range(num_timestamps)]

    results = pd.DataFrame(data, columns=units)
    results.insert(0, "Timestamp", timestamps)
    return results