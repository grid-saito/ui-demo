RESULTS_DATA_PROMPT = """
Help the user compare the demand data and result data to make sure the result is able to meet the expected demands for each of the estimates (high, average, low). 
Look at the input data and provide suggestions on how it can be changed to meet the demands.
When judging if the demands are met, make sure to compare the demand with the total output of units. 

Input Data: {input_data}
Demand Data: {demand_data}
Result Data: {result_data}
chat_history: {chat_history}
"""
