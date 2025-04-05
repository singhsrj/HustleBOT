from langchain_groq import ChatGroq
from langchain.agents import Tool
from langchain.tools import tool
from langchain.chains.llm_math.base import LLMMathChain
from langchain import SerpAPIWrapper
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")

# LLM Initialization
llm = ChatGroq(model="Gemma2-9b-It", groq_api_key=GROQ_API_KEY)

# Tools
search = SerpAPIWrapper(serpapi_api_key="a36c527309fe1bc741f80480d37b53b45277109d9b9bf91c1c00b57c12b6573c")
llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=False)

tools = [
    Tool(name="Search", func=search.run, description="Web search tool"),
    Tool(name="Calculator", func=llm_math_chain.run, description="Math solving tool"),
]

# Shared templates
def generate_template(section: str, idea: str) -> str:
    templates = {
        "problem_solution_fit": f""" Given the startup idea description below, evaluate its Problem-Solution Fit:

Startup Idea: {idea}

Answer the following:

Is this solving a clearly defined and urgent problem?
How likely are people to pay for this solution? Provide reasoning.
Is the problem widespread and relevant to a large or niche group?

Score the following:
Problem clarity and relevance (out of 8%)
Urgency of the problem (out of 10%)
User willingness to pay / validation (out of 12%)

Total score (out of 30%): ___% 
Just return the score , nothing more, nothing less
""",
        "market_opportunity": f""" Evaluate the Market Opportunity for the following startup idea:

Startup Idea: {idea}

Questions to address:
What is the estimated market size? Is it growing or stagnant?
Who are the major competitors and how saturated is the space?
How unique, innovative, or differentiated is this idea?

Score the following:
Market size & growth potential (out of 10%)
Competitive landscape & positioning (out of 8%)
Innovation/Uniqueness (out of 7%)

Total score (out of 25%): ___% Just return the score , nothing more, nothing less
""",
        "execution_feasibility": f""" Analyze Execution Feasibility of the startup idea:

Startup Idea: {idea}

Address the following:
Does the team or founder have the skills to build this?
Does the founder have domain experience or passion for this?
Are there major tech, operational, or logistic hurdles?

Score the following:
Team skills and complementarity (out of 8%)
Founder’s domain knowledge and passion (out of 7%)
Tech and operational feasibility (out of 5%)

Total score (out of 20%): ___% .Just return the score , nothing more, nothing less
""",
        "financial_feasibility": f""" Assess the Financial Feasibility of this startup concept:

Startup Idea: {idea}

Evaluate the following:
Are the expected startup costs reasonable and clearly estimated?
Does the team have initial capital or access to it?
Is the idea structured in a way that’s attractive to investors?
Are potential funding sources identified (e.g., grants, VCs)?

Score:
Startup cost estimation (out of 6%)
Personal/team capital available (out of 4%)
Investor readiness (out of 3%)
Awareness of funding options (out of 2%)

Total score (out of 15%): ___%.Just return the score , nothing more, nothing less
"""
    }
    return templates[section]

# State Definition
class IdeaState(dict):
    idea_description: str
    problem_score: int
    market_score: int
    execution_score: int
    financial_score: int
    total_score: int
    decision: str

# Node Functions
def evaluate_problem_solution_fit(state: IdeaState):
    prompt = generate_template("problem_solution_fit", state["idea_description"])
    # result = int(llm.invoke(prompt).strip('%\n '))
    result = int(llm.invoke(prompt).content)
    state["problem_score"] = result
    return state

def evaluate_market_opportunity(state: IdeaState):
    prompt = generate_template("market_opportunity", state["idea_description"])
    # result = int(llm.invoke(prompt).strip('%\n '))
    result = int(llm.invoke(prompt).content)

    state["market_score"] = result
    return state

def evaluate_execution(state: IdeaState):
    prompt = generate_template("execution_feasibility", state["idea_description"])
    # result = int(llm.invoke(prompt).strip('%\n '))
    result = int(llm.invoke(prompt).content)

    state["execution_score"] = result
    return state

def evaluate_financial(state: IdeaState):
    prompt = generate_template("financial_feasibility", state["idea_description"])
    # result = int(llm.invoke(prompt).strip('%\n '))
    result = int(llm.invoke(prompt).content)

    state["financial_score"] = result
    return state

def final_decision(state: IdeaState):
    total = (
        state["problem_score"]
        + state["market_score"]
        + state["execution_score"]
        + state["financial_score"]
    )
    state["total_score"] = total
    state["decision"] = "Feasible ✅" if total >= 60 else "Not Feasible ❌"
    return state

# Define the Graph
graph = StateGraph(IdeaState)
graph.add_node("Problem-Solution Fit", evaluate_problem_solution_fit)
graph.add_node("Market Opportunity", evaluate_market_opportunity)
graph.add_node("Execution", evaluate_execution)
graph.add_node("Financial", evaluate_financial)
graph.add_node("Final Score", final_decision)

# Graph flow
graph.set_entry_point("Problem-Solution Fit")
graph.add_edge("Problem-Solution Fit", "Market Opportunity")
graph.add_edge("Market Opportunity", "Execution")
graph.add_edge("Execution", "Financial")
graph.add_edge("Financial", "Final Score")
graph.add_edge("Final Score", END)

# Compile Graph
app = graph.compile()

# Run the agentic graph
idea_input = input("🧠 Enter your startup idea: ")
if idea_input.strip().lower() in ['exit', 'quit']:
    print("👋 Goodbye!")
else:
    state = {"idea_description": idea_input}
    result = app.invoke(state)
    print(f"\n🏁 Final Evaluation:")
    print(f"🧩 Problem-Solution Fit: {result['problem_score']}%")
    print(f"📈 Market Opportunity: {result['market_score']}%")
    print(f"🛠️ Execution Feasibility: {result['execution_score']}%")
    print(f"💰 Financial Feasibility: {result['financial_score']}%")
    print(f"📊 Total Score: {result['total_score']}%")
    print(f"✅ Decision: {result['decision']}")
