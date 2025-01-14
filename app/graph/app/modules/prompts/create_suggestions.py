CREATE_SUGGESTIONS_PROMPT = """
    The following is the result of the compatibility check.
    compability_check_result: {compability_check_result}

    Based on the result of the compatibility check, please suggest fixes to the input data to the user.
    input_data: {input_data}
    
    The following external data can be used as reference for the suggested fixes
    demand_forecast: {demand_forecast}
    state of the equipment: {equipment_states}

    Instructions: 
    - Please suggest actionable, specific fixes to the input data to the user (e.g. "Replace unit 5 with unit 9", "remove unit 5 from the settings", "set the maximum output of unit 4 to 1000")
    - Please make the suggestions as simple as possible.
    - create at least 4 suggestions.

    Here are some examples of suggested actions: 
    - Replace unit 5 with unit 9
    - Remove unit 5 from the settings
    - Replace unit 5 with unit 6
    - Set the maximum output of unit 4 to 1000
"""
