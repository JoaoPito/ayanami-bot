class TelegramAppStub():
    handlers_added = {}
    is_running = False

    def add_handler(self, handler):
        command_text = list(handler.commands)[0]
        self.handlers_added[command_text] = handler

    def run_polling(self):
        self.is_running = True

    def call_handler(self, filters):
        self.handlers_added[filters].callback()