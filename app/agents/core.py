from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain import hub
from app.rag_engine import rag_engine
from app.tools.tools import celestial_knowledge_search, get_astrology_metadata
from app.core.constants import SYSTEM_MESSAGES

class AstroAgent:
    def __init__(self):
        self.llm = rag_engine.get_llm(temperature=0.3)
        self.tools = [celestial_knowledge_search, get_astrology_metadata]
        self.prompt = hub.pull("hwchase17/openai-functions-agent")
        
        # Customize prompt with our system message
        self.system_message = SYSTEM_MESSAGES["NATAL"]
        
        self.agent = create_openai_functions_agent(self.llm, self.tools, self.prompt)
        self.executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True
        )

    async def run(self, query: str) -> str:
        """Runs the agent on a specific celestial query."""
        response = self.executor.invoke({"input": query})
        return response["output"]

# Initialize a global instance
astro_agent = AstroAgent()
