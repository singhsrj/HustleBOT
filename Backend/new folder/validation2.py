from langchain.agents import initialize_agent, AgentType
from langchain.tools import DuckDuckGoSearchRun
from langchain.utilities import GoogleSerperAPIWrapper
from langchain_groq import ChatGroq
from langchain_core.tools import Tool
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
import json

load_dotenv()

# Load API keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize LLM
llm = ChatGroq(model="Gemma2-9b-It", groq_api_key=GROQ_API_KEY)

# Define search tools
search = GoogleSerperAPIWrapper(serper_api_key=os.getenv("SERPAPI_API_KEY"))
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
]

idea = input("What are we building today?")
idea = PromptTemplate("What are we building today?", "I want to build a {}.", idea)


# Updated prompt that accepts structured input
template = """
You are a startup evaluator AI using this feasibility framework:
- Problem-Solution Fit (30%)
- Market Opportunity (25%)
- Execution Feasibility (20%)
- Financial Feasibility (15%)
- Scalability & Sustainability (10%)

Use the input below to evaluate. Each factor is scored out of 10. Use web search if needed.

Startup Data:
{{
    "idea": "{idea}",
    "problem_solution_info": "{problem_solution_info}",
    "market_opportunity_info": "{market_opportunity_info}",
    "execution_feasibility_info": "{execution_feasibility_info}",
    "financial_feasibility_info": "{financial_feasibility_info}",
    "scalability_sustainability_info": "{scalability_sustainability_info}"
}}

Return:
- Subscores per factor
- Weighted Total Score (out of 10)
- Final Verdict (e.g., Highly Feasible, Moderately Feasible, Not Feasible)
- Improvement Suggestions
"""

prompt = PromptTemplate(
    input_variables=[
        "idea", "problem_solution_info", "market_opportunity_info",
        "execution_feasibility_info", "financial_feasibility_info",
        "scalability_sustainability_info"
    ],
    template=template
)

# Initialize agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)

def ask_for_missing_data():
    print("🔎 Please provide additional info for evaluation:\n")
    user_inputs = {
        "problem_solution_info": input("🧠 Problem-Solution Fit details: "),
        "market_opportunity_info": input("📊 Market Opportunity: "),
        "execution_feasibility_info": input("🛠 Execution Feasibility: "),
        "financial_feasibility_info": input("💰 Financial Feasibility: "),
        "scalability_sustainability_info": input("🌱 Scalability & Sustainability: "),
    }
    return user_inputs

def evaluate_startup_idea(idea_description):
    user_data = ask_for_missing_data()
    prompt_text = prompt.format(idea=idea_description, **user_data)
    response = agent.run(prompt_text)
    return response

# Example run
if __name__ == "__main__":
    idea = """An edtech platform for rural students offering offline-accessible, AI-powered gamified learning for STEM subjects in vernacular languages. It uses solar-powered devices and also offers teacher training kits."""
    result = evaluate_startup_idea(idea)
    print("\n🎯 Evaluation Result:\n")
    print(result)
