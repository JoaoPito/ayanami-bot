from ai.ai_interface import AIInterface
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor
from langchain_core.messages import AIMessage, HumanMessage

MEMORY_KEY = 'chat_history'

class LangChainAI(AIInterface):
    chat_history = []

    def __init__(self, tools, params):
        self.model = params["ai_model"]
        self.temperature = params["temperature"]
        self.system_prompt = params["system"]
        self.tools = tools
        self.llm = ChatOpenAI(model=self.model, temperature=self.temperature).bind_tools(tools)
        self.prompt = self.__create_prompt__()
        self.agent_executor = AgentExecutor(agent=self.__create_agent__(), tools=tools, verbose=True)
        
    def __create_prompt__(self):
        return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                self.system_prompt,
            ),
            MessagesPlaceholder(variable_name=MEMORY_KEY), # history of messages, stays ABOVE user input
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"), # This serves to store tools results so that the LLM can use
        ]
        )
    
    def __create_agent__(self):
        return (
            {
                "input": lambda x: x["input"],
                "username": lambda x: x["username"],
                "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                    x['intermediate_steps']
                ),
                MEMORY_KEY: lambda x: x[MEMORY_KEY],
            }
            | self.prompt
            | self.llm
            | OpenAIToolsAgentOutputParser()
        )

    def __add_to_history__(self, input, result):
        self.chat_history.extend(
            [
                HumanMessage(content=input),
                AIMessage(content=result['output'],)
            ]
        )
        self.chat_history = self.chat_history[-20:]

    def __persist_history_log__(self):
        pass # Persist log to a file or DB

    def invoke(self, args):
        args[MEMORY_KEY] = self.chat_history
        result = self.agent_executor.invoke(args)
        self.__add_to_history__(args["input"], result)
        self.__persist_history_log__()
        return result
    
    def reset_history(self):
        self.chat_history = []
    
    def run(self):
        pass