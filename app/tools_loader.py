from importlib import import_module
from langchain_core.tools import BaseTool

def load_tools_and_toolkits(tool_list=[], toolkit_list=[]):
    tools = [import_module(tool).create() for tool in tool_list]
    toolkits = []
    for toolkit in toolkit_list:
        toolkits = toolkits + import_module(toolkit).create().get_tools()
    return tools + toolkits
