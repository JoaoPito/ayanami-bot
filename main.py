import os
from app.app_builder import AyanamiAppBuilder
from app.commands import MessageCommand, ResetCommand
import app.tools_loader as tools_loader

from auth.token_auth import TokenAuth

from chat.telegramchat_factory import TelegramChatFactory
import config
from tests.ai.stubs import EmptyAIStub

import logging

logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
        )

config_tools = config.tools
config_ai_params = config.ai_model

def main():
    builder = AyanamiAppBuilder()

    chat = TelegramChatFactory().create(os.environ["TELEGRAM_BOT_TOKEN"])
    builder.set_chat(chat)

    #ai_tools = tools_loader.load_tools(config_tools)
    #ai = LangChainAIFactory().create(ai_tools, config_ai_params)
    ai = EmptyAIStub()
    builder.set_ai(ai)
    
    #builder.add_auth(TokenAuth())
    
    app = builder.build_app()

    app.add_command(MessageCommand(app))
    app.add_command(ResetCommand('reset'))

    app.run()

if __name__ == "__main__":
    main()
