class BaseToolkit:
    def __init__(self, tools=None):
        """
        Base class for creating toolkits.

        Args:
            tools (dict): A dictionary of tool names and their corresponding functions.
        """
        self.tools = tools or {}

    def get_tools(self):
        """
        Retrieves all tools as a list of functions.

        Returns:
            list: List of tool functions.
        """
        return list(self.tools.values())

    def get_tool_names(self):
        """
        Retrieves all registered tool names.

        Returns:
            list: List of tool names as strings.
        """
        return list(self.tools.keys())

    def execute(self, tool_name, **kwargs):
        """
        Executes a tool by its name with the given arguments.

        Args:
            tool_name (str): Name of the tool to execute.
            **kwargs: Arguments to pass to the tool.

        Returns:
            Any: Result of the tool execution.

        Raises:
            KeyError: If the tool name is not found in the toolkit.
        """
        if tool_name in self.tools:
            return self.tools[tool_name](**kwargs)
        else:
            raise KeyError(f"Tool '{tool_name}' not found in the toolkit.")