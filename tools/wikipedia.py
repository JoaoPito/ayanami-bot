# pip install wikipedia is needed for this tool

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

def create():
    return WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())