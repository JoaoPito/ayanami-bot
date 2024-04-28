ai_params = {
    "ai_model": "gpt-3.5-turbo",
    "ai_provider": "OPENAI",
    "temperature": 0.2,
    "system": "Your name is 'Ayanami', you are an efficient AI assistant. You answer user's questions. The user's name is '{username}'."
}
tools = {"tools.word_length", "tools.youtube", "tools.wikipedia", "tools.openweathermap"} # Enable/disable tools that the AI can use here