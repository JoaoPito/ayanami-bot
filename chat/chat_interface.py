class ChatInterface:
    filters = {}
    handlers = {}

    def __init__(self):
        pass

    def add_handler(self, name:str, handler):
        self.handlers[name] = handler
