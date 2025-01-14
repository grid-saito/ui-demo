CHAT_BOT_PROMPT = """
    Answer the user's questions based on the input_data. 
    If necessary, use the tools to modify or visualize the input data. 

    Query: {query}
    Chat History: {chat_history}
    Input Data: {input_data}
"""