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
        
    def __create_prompt__(self):
        return ChatPromptTemplate.from_messages(
        [
            ("system", self.system_prompt),
            MessagesPlaceholder(variable_name=MEMORY_KEY), # history of messages, stays ABOVE user input
        ]
        )
    
    def __create_agent__(self, human_message):
        complete_prompt = self.prompt + [human_message, MessagesPlaceholder(variable_name="agent_scratchpad")]
        return (
            {
                "username": lambda x: x["username"],
                "agent_scratchpad": lambda x: format_to_openai_tool_messages(
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
        input_text = args["input_text"]
        humanmessage_content = [
                {"type": "text", "text": f"{input_text}"}
            ]
        
        if "input_image" in args:
            input_image = args["input_image"]
            humanmessage_content.append({"type": "image_url", "image_url": {
                    "url": f"data:image/jpeg;base64,{input_image}"
                }})
        return HumanMessage(content=humanmessage_content)

    def invoke(self, args):
        args[MEMORY_KEY] = self.chat_history
        human_message = self.__create_human_message__(args)
        agent_executor = AgentExecutor(agent=self.__create_agent__(human_message), tools=self.tools, verbose=True)

        result = agent_executor.invoke(args)
        self.__add_to_history__(human_message, AIMessage(content=result['output'],))
        self.__persist_history_log__()
        return result
    
    def reset_history(self):
        self.chat_history = []
    
    def run(self):
        pass