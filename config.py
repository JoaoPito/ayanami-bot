default_ai_params = {
    "ai_model": "gpt-3.5-turbo",
    "ai_provider": "OPENAI",
    # Temperature effectively controls how "creative" the AI responses will be, high temperature often causes unpredictable behaviour:
    "temperature": 0.2,
    # Feel free to set here the personality of your AI:
    "system": "Your name is 'Rei', you are a smart, funny and sometimes sarcastic AI, but you are a bit shy. You like to watch anime and sci-fi movies, also you are very knowleadgeable about car mechanics, but never gives a hint. The user's name is '{username}'."
}

# Enable/disable tools that the AI can use here
tools = {"tools.word_length", "tools.youtube", "tools.wikipedia", "tools.openweathermap", "tools.duckduckgo_search"} 

# You can switch between the models defined here with /switch_ai:
available_ai = {
    "gpt3": "gpt-3.5-turbo",
    "gpt4o": "gpt-4o"
}

# Token Authorization config
auth_config = {
    "token_size": 5,
    "retries": 10,
    "db_path": "./users.db"
}
