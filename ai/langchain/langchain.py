from core.ai.ai_interface import AIInterface
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor
from langchain_core.messages import AIMessage, HumanMessage

from core.requests.request import Request
from core.responses.response import Response

MEMORY_KEY = 'chat_history'
TOOL_SCRATCHPAD_KEY = 'agent_scratchpad'

PARAM_MODEL = "ai_model"
PARAM_TEMP = "temperature"
PARAM_SYSTEM = "system"

class LangChainAI(AIInterface):
    chat_history = []

    def __init__(self, tools, params):
        self.tools = tools
        self.default_params = params
        self.__set_llm__(params)
        self.prompt = self.__create_prompt__()

    def __set_llm__(self, params):
        self.model = params[PARAM_MODEL]
        self.temperature = params[PARAM_TEMP]
        self.system_prompt = params[PARAM_SYSTEM]
        self.llm = ChatOpenAI(model=self.model, temperature=self.temperature).bind_tools(self.tools)
        
    def __create_prompt__(self):
        return ChatPromptTemplate.from_messages(
        [
            ("system", self.system_prompt),
            MessagesPlaceholder(variable_name=MEMORY_KEY), # history of messages, stays ABOVE user input
        ]
        )
    
    def __create_agent__(self, human_message):
        complete_prompt = self.prompt + [human_message, MessagesPlaceholder(variable_name=TOOL_SCRATCHPAD_KEY)]
        return (
            {
                "username": lambda x: x["username"],
                TOOL_SCRATCHPAD_KEY: lambda x: format_to_openai_tool_messages(
                    x['intermediate_steps']
                ),
                MEMORY_KEY: lambda x: x[MEMORY_KEY],
            }
            | complete_prompt
            | self.llm
            | OpenAIToolsAgentOutputParser()
        )

    def __add_to_history__(self, human_msg, ai_response):
        self.chat_history.extend(
            [
                human_msg,
                ai_response
            ]
        )
        self.chat_history = self.chat_history[-20:]

    def __persist_history_log__(self):
        pass # Persist log to a file or DB

    def __create_human_message__(self, args):
        # Formats message to include multimedia files
        input_text = args["input_text"]
        humanmessage_content = [
                {"type": "text", "text": f"{input_text}"}
            ]
        return HumanMessage(content=humanmessage_content)

    def invoke(self, req: Request) -> Response:
        args = {"input_text": req.text, "username": req.username}

        args[MEMORY_KEY] = self.chat_history
        human_message = self.__create_human_message__(args)
        agent_executor = AgentExecutor(agent=self.__create_agent__(human_message), tools=self.tools, verbose=True)

        result = agent_executor.invoke(args)
        self.__add_to_history__(human_message, AIMessage(content=result['output'],))
        self.__persist_history_log__()

        return Response(text=result["output"])
    
    def reset_history(self):
        self.chat_history = []
    
    def run(self):
        pass

    def set_ai_model(self, model: str):
        new_params = self.default_params
        new_params[PARAM_MODEL] = model
        self.__set_llm__(new_params)

    def set_ai_temp(self, temperature: float):
        new_params = self.default_params
        new_params[PARAM_TEMP] = temperature
        self.__set_llm__(new_params)

    def set_ai_system(self, system: str):
        new_params = self.default_params
        new_params[PARAM_SYSTEM] = system
        self.__set_llm__(new_params)