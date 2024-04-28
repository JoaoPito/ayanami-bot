# This uses the API ftom OpenWeatherMap, it needs an API key set in an environment variable named "OPENWEATHERMAP_API_KEY"
# Be sure to install pip package with 'pip install pyowm'

from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langchain.agents import tool

wrapper = OpenWeatherMapAPIWrapper()

@tool
def get_weather(location: str) -> int:
    """Returns the weather in a specific city. Use format 'city,country code'."""
    return wrapper.run(location)

def create():
    return get_weather