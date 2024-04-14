from app.app import AyanamiApp
from app.app_builder import AyanamiAppBuilder
import app.tools_loader as tools_loader

from chat.telegram_chat import TelegramChat
from ai.langchain_ai import LangChainAI
from auth.token_auth import TokenAuth

import config

config_tools = config.tools
config_ai_params = config.ai_model

def main():
    builder = AyanamiAppBuilder()

    ai_tools = tools_loader.load_tools(config_tools)
    builder.add_ai(LangChainAI(ai_tools, config_ai_params))
    builder.add_chat(TelegramChat())
    builder.add_auth(TokenAuth())
    
    app = builder.build_app()

    app.run()

if __name__ == "__main__":
    main()
