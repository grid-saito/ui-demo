from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.callbacks.streamlit.streamlit_callback_handler import StreamlitCallbackHandler
from modules.models.langchain_azure import langchain_azure_model
from tools.DemandDataToolkit import DemandDataToolkit
import streamlit as st


class DemandDataProcessingChain:
    def __init__(self):
        # Initialize tools
        self.tools = self._load_tools()

        # Define the prompt template
        self.chat_bot_prompt_template = """
            Help the user update the demand constraint data. 
            Use the demand_forecast value as reference. 

            Demand constraint: {demand_constraint}
            Demand forecast: {demand_forecast}
            
            When user asks to set the demand constraint to a high estimate, take the demand forecast and add 150 units to it and pass the value to the set_demand_constraint_value tool.
            When user asks to set the demand constraint to a low estimate, take the demand forecast and subtract 150 units from it and pass the value to the set_demand_constraint_value tool.
            """
        
        self.chat_bot_message_template = [
        (
            "system",
             self.chat_bot_prompt_template,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
        ]
         
        # Initialize the agent executor
        self.agent_executor = self._get_chat_model_w_tools()

        # Define the pipeline for the chain
        self.chain = self.agent_executor
        

    def _load_tools(self):
        """
        Load all tools from the toolkits and return them as a combined list.
        """
        tools = []
        demand_data_toolkit = DemandDataToolkit()
        tools.extend(demand_data_toolkit.get_tools())
        return tools


    def _get_chat_model_w_tools(self):
        """
        Create the AgentExecutor with tools and the model.
        """
        agent = create_openai_tools_agent(
            langchain_azure_model,
            self.tools,
            #ChatPromptTemplate.from_template(self.chat_bot_prompt_template)
            ChatPromptTemplate.from_messages(self.chat_bot_message_template)
        )
        agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)
        return agent_executor


    def invoke(self, inputs: dict):
        """
        Invoke the chain with required inputs.
        """
        required_keys = ["query", "chat_history", "demand_constraint", "demand_forecast"]
        
        # Validate input dictionary
        for key in required_keys:
            if key not in inputs:
                raise ValueError(f"Missing required key: {key}")
        
        # Pass the inputs to the chain
        st_callback = StreamlitCallbackHandler(st.container())
        result = self.chain.invoke(inputs, callbacks=[st_callback])
        return result


# --- Tool Processing ---
def process_tool_calls(tool_calls):
    """
    Process a list of tool calls and execute the appropriate tools.
    """
    demand_data_toolkit = DemandDataToolkit()
    results = []

    for tool_call in tool_calls:
        tool_name = tool_call.get("name")
        tool_args = tool_call.get("args", {})

        if tool_name in demand_data_toolkit.get_tool_names():
            results.append(_execute_tool(demand_data_toolkit, tool_name, tool_args))

    return results


def _execute_tool(tool_registry, tool_name, tool_args):
    """
    Execute a single tool using the provided registry, tool name, and arguments.
    """
    try:
        result = tool_registry.execute(tool_name, **tool_args)
        print(f"Tool '{tool_name}' executed successfully: {result}")
        return result
    except Exception as e:
        print(f"Error executing tool '{tool_name}': {e}")
        return f"Error: {e}"


# Instantiate the ChatBotChain
chain = DemandDataProcessingChain()