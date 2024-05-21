from langchain.agents import tool
from langchain_community.agent_toolkits import FileManagementToolkit

# This toolkit includes Tools for reading, writing, copying, etc files (https://python.langchain.com/v0.1/docs/integrations/tools/filesystem/)

# if you wish you can configure a temporary directory with the 'tempfile' python package

ROOT_DIRECTORY = "./shared_files/"

def create():
    return FileManagementToolkit(root_dir=ROOT_DIRECTORY)  # If you don't provide a root_dir, operations will default to the current working directory