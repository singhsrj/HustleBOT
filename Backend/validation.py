from langchain.agents import initialize_agent, tool, AgentType
from langchain.agents.agent_toolkits import FileManagementToolkit
from langchain.tools import DuckDuckGoSearchRun
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.utilities import GoogleSerperAPIWrapper
from langchain_groq import ChatGroq
from langchain_core.tools import Tool
from langchain.prompts import PromptTemplate
import os

from dotenv import load_dotenv
load_dotenv()

# 1. Set up API keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")


# 2. Initialize LLM (Groq)
llm = ChatGroq(model ="Gemma2-9b-It",groq_api_key=GROQ_API_KEY)

# 3. Define tools
search = GoogleSerperAPIWrapper(serper_api_key="a36c527309fe1bc741f80480d37b53b45277109d9b9bf91c1c00b57c12b6573c")
  # for real-time data
duck_search = DuckDuckGoSearchRun()

tools = [
    Tool(
        name="Web Search",
        func=search.run,
        description="Useful for fetching current market data, competitors, and validation stats"
    ),
    Tool(
        name="DuckDuckGo Search",
        func=duck_search.run,
        description="Good for fast searches about trends or problems"
    ),
    duck_search
]

# 4. Prompt Template for Evaluation
template = """
You are a startup evaluator AI using the following feasibility framework:
- Problem-Solution Fit (30%)
- Market Opportunity (25%)
- Execution Feasibility (20%)
- Financial Feasibility (15%)
- Scalability & Sustainability (10%)

Each sub-factor is rated from 1 to 10. Use web search tools if needed. If you lack data, ask for Human Input (return a message: "Requesting human input for {{factor}}").

At the end, return:
- Subscores per factor
- Weighted Total Score (out of 10)
- Final Verdict (e.g., Highly Feasible, Moderately Feasible, Not Feasible)
- Improvement Suggestions

Startup Idea: {{idea}}
"""


prompt = PromptTemplate(
    input_variables=["idea"],
    template=template
)

# 5. Create agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True 
)

# 6. Run agent
def evaluate_startup_idea(idea_description):
    prompt_text = prompt.format(idea=idea_description)
    response = agent.run(prompt_text)
    return response

# 7. Example usage
if __name__ == "__main__":
    idea = """An edtech platform for rural students offering offline-accessible, AI-powered gamified learning for STEM subjects in vernacular languages. It uses solar-powered devices and also offers teacher training kits."""
    result = evaluate_startup_idea(idea)
    print("\n🎯 Evaluation Result:\n")
    print(result)
