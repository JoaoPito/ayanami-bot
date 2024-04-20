from ai.ai_interface import AIInterface

class EmptyAIStub(AIInterface):
    has_run = False

    def __init__(self):
        pass

    def run(self):
        self.has_run = True
