from app.app import AyanamiApp

class CommandBase:
    def __init__(self, name:str, app: AyanamiApp):
        self.name = name
        self.app = app

    async def handle(self, **kwargs):
        pass
