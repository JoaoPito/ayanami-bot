class CommandBase:
    def __init__(self, name:str):
        self.name = name

    async def handle(self, **kwargs):
        pass
