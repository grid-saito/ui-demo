from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.callbacks.streamlit.streamlit_callback_handler import StreamlitCallbackHandler
from modules.models.langchain_azure import langchain_azure_model
from tools.VisualizationToolkit import VisualizationToolkit
from tools.SettingsToolkit import SettingsToolkit
from tools.SimulationsToolkit import SimulationsToolkit
import streamlit as st


class ChatBotChain:
    def __init__(self):
        # Initialize tools
        self.tools = self._load_tools()

        # Define the prompt template
        self.chat_bot_prompt_template = """
        Answer the user's questions based on the input_data. 
        If necessary, use the tools to modify or visualize the input data. 
        When displaying images, use format: ![name of graph](image.png)
        
        Query: {query}
        Chat History: {chat_history}
        Input Data: {input_data}
        """
        
        self.chat_bot_message_template = [
        (
            "system",
            """
            You are a helpful assistant. Answer the user's questions based on the {input_data}. 
            If necessary, use the tools to modify or visualize the input data. 
            When calling the set_column_values tool, make sure to pass the entire column values you have changed. 
            
            If you need to make changes to demand forecast, use the tool set_demand_forecast to set the values. 
            """,
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
        visualization_toolkit = VisualizationToolkit()
        settings_toolkit = SettingsToolkit()
        #simulations_toolkit = SimulationsToolkit()
        tools.extend(visualization_toolkit.get_tools())
        tools.extend(settings_toolkit.get_tools())
        #tools.extend(simulations_toolkit.get_tools())
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
        required_keys = ["query", "chat_history", "input_data"]
        
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
    visualization_toolkit = VisualizationToolkit()
    settings_toolkit = SettingsToolkit()
    #simulations_toolkit = SimulationsToolkit()
    results = []

    for tool_call in tool_calls:
        tool_name = tool_call.get("name")
        tool_args = tool_call.get("args", {})

        if tool_name in visualization_toolkit.get_tool_names():
            results.append(_execute_tool(visualization_toolkit, tool_name, tool_args))
        elif tool_name in settings_toolkit.get_tool_names():
            results.append(_execute_tool(settings_toolkit, tool_name, tool_args))
        #elif tool_name in simulations_toolkit.get_tool_names():
        #    results.append(_execute_tool(simulations_toolkit, tool_name, tool_args))

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
chain = ChatBotChain()