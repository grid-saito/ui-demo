COMPATIBILITY_CHECK_PROMPT = """
Evaluate the compatibility of the provided input data against the external data sources, including weather data, demand data, and plant status. 
Check if the input units in the input data are in operation. 
Check if the current weather conditions might influence the demand trend trajectory forecasted
Check if the powerplant types will be impacted by the weather that might risk of being not operational (for instance, severe weather might influence if coal can be replenshed or not)
Check any other conditions that might lead it to be incompatible

Dont check: demand data aligns with the provided locations. 
Dont check: All units listed in the input data have a corresponding status in the plant status data.
Dont check: Weather data availability for the specified locations in the input data.
Dont check: All units listed in the input data have a corresponding status in the plant status data



For each compatibility check, return the following information:
1. A description of what was checked.
2. The result of the check (check mark if compatible, X if not).
3. Any relevant explanation or reason if the check fails.
4. Recommended Action for fixing the check if it fails
5. make bold the row that failed to emphasize it

Ensure the output is structured as a checklist with clear labels and results.

Input Data: {input_data}
Demand Data: {demand_data}
Plant Status: {plant_status}
Weather Data: {weather_data}

Example Output:
Checklist:
1. The sum of the maxium output from the power plants is above the demand data
2. True
3. -
4. -

Provide the detailed checklist below:
"""
