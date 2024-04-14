# Import things that are needed generically
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool

@tool
def stringstub(query: str):
    """This is just here to test things"""
    return "Test"
