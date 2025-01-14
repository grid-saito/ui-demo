from tools.VisualizationToolkit import VisualizationToolkit
from tools.SettingsToolkit import SettingsToolkit
from tools.SimulationsToolkit import SimulationsToolkit


# --- Tool Processing ---
def process_tool_calls(tool_calls):
    """
    Process a list of tool calls and execute the appropriate tools.
    """
    visualization_toolkit = VisualizationToolkit()
    settings_toolkit = SettingsToolkit()
    simulations_toolkit = SimulationsToolkit()
    results = []

    for tool_call in tool_calls:
        tool_name = tool_call.get("name")
        tool_args = tool_call.get("args", {})

        if tool_name in visualization_toolkit.get_tool_names():
            results.append(_execute_tool(visualization_toolkit, tool_name, tool_args))
        elif tool_name in settings_toolkit.get_tool_names():
            results.append(_execute_tool(settings_toolkit, tool_name, tool_args))
        elif tool_name in simulations_toolkit.get_tool_names():
            results.append(_execute_tool(simulations_toolkit, tool_name, tool_args))

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