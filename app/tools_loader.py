from importlib import import_module

def load_tools(tool_list):

    return [import_module(tool).create() for tool in tool_list]
