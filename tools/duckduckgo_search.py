from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

# For more configs: https://api.python.langchain.com/en/latest/utilities/langchain_community.utilities.duckduckgo_search.DuckDuckGoSearchAPIWrapper.html

def create():
    wrapper = DuckDuckGoSearchAPIWrapper(region="pt-br", max_results=5, safesearch='moderate')
    return DuckDuckGoSearchRun(api_wrapper=wrapper)