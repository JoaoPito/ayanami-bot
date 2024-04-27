from ai.ai_interface import AIInterface

class EmptyAIStub(AIInterface):
    has_run = False

    def __init__(self):
        pass

    def run(self):
        self.has_run = True

class ConstantAIStub(AIInterface):
    def __init__(self, constant):
        self.constant = constant
        super().__init__()

    def run(self):
        pass

    def invoke(self, args):
        return {"input": args["input"], "output": self.constant}
