from ai.ai_factory import AIFactory
from ai.langchain.langchain import LangChainAI

class LangChainAIFactory(AIFactory):
    def create(self, tools, params):
        return LangChainAI(tools, params)