import os
from ai.langchain.langchain_factory import LangChainAIFactory
from chat.telegram.commands.ai import ChangeAICommand, MessageCommand, ResetCommand
from chat.telegram.commands.app import PingCommand, StartCommand
from chat.telegram.commands.auth import TryAuthenticateUserCommand
import ai.langchain.tools_loader as tools_loader

from auth.token_auth import TokenAuth

from chat.telegram.telegramchat_factory import TelegramChatFactory
import config

import logging

from data.users_db_builder import create_dbcontext

logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
        )

config_tools = config.tools
config_toolkits = config.toolkits
config_ai_params = config.default_ai_params
config_auth = config.auth_config

def main():
    chat = TelegramChatFactory().create(os.environ["TELEGRAM_BOT_TOKEN"])

    ai_tools = tools_loader.load_tools_and_toolkits(config_tools, config_toolkits)
    ai = LangChainAIFactory().create(ai_tools, config_ai_params)

    auth = TokenAuth(create_dbcontext(path="./users.db"), config_auth)

    # AI commands
    chat.add_command(MessageCommand(chat, ai, auth))
    chat.add_command(ResetCommand('reset', chat, ai, auth))
    chat.add_command(ChangeAICommand('switch_ai', config.available_ai, ai, chat, auth))

    # App commands
    chat.add_command(PingCommand('ping', chat, auth))

    # Auth commands
    chat.add_command(StartCommand('start', chat, auth))
    chat.add_command(TryAuthenticateUserCommand('auth', chat, auth))

    logging.info(f"> IMPORTANT: This session token is: '{auth.session_token}', use it to authenticate with '/auth TOKEN.'")

    ai.run()
    chat.run()

if __name__ == "__main__":
    main()
