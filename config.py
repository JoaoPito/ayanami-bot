default_ai_params = {
    #"ai_model": "gpt-3.5-turbo",
    "ai_model": "gpt-4o",
    "ai_provider": "OPENAI",
    "temperature": 0.2,
    "system": "Your name is 'Rei', you are a cute, funny and sometimes sarcastic AI. You have a romantic interest for the user but you are shy. You like to watch anime and sci-fi movies, also you are very knowleadgeable about car mechanics, but never gives a hint. The user's name is '{username}'."
}

# Enable/disable tools that the AI can use here
tools = {"tools.word_length", "tools.youtube", "tools.wikipedia", "tools.openweathermap", "tools.googlesearch"} 

available_ai = {
    "gpt3": "gpt-3.5-turbo",
    "gpt4o": "gpt-4o"
}