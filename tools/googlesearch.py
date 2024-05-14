from langchain_community.utilities import SerpAPIWrapper
from langchain.agents import tool

# To use this tool you need an account on SerpAPI (https://serpapi.com - they have free plans), get an API KEY and set an Environment Variable with the name 'SERPAPI_API_KEY'
# It also needs the google-search-resultspip package to be installed (pip install google-search-results)

@tool
def google_search(query: str):
    """Performs a Google search using the provided query string. Choose this tool when you need to find current data"""
    return SerpAPIWrapper().run(query)

def create():
    return google_search