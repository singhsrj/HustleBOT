from langchain import LLMMathChain, SerpAPIWrapper
from langchain.agents import initialize_agent, Tool
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

# Load API keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")

# Initialize LLMs
llm = ChatGroq(model="Gemma2-9b-It", groq_api_key=GROQ_API_KEY)
llm_tool_runner = ChatGroq(model="Gemma2-9b-It", groq_api_key=GROQ_API_KEY)

# Initialize Tools
# search = SerpAPIWrapper(serpapi_api_key="a36c527309fe1bc741f80480d37b53b45277109d9b9bf91c1c00b57c12b6573c")
search = SerpAPIWrapper(serpapi_api_key="bde0b4e90e056c623473f16344e2dbb2eb495976cfbde5ec2217a98cbc3fb2a8")
llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)

tools = [
    Tool(
        name="Search",
        func=search.run,
        description="Use this tool to get real-time information from the internet. Ideal for researching current trends, news, market insights, or general knowledge.",
    ),
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="Use this tool to solve math problems or do numerical reasoning.",
    ),
]

# Initialize the Agent
agent = initialize_agent(
    tools=tools,
    llm=llm_tool_runner,
    agent="chat-zero-shot-react-description",
    verbose=True,handle_parsing_errors=True

)

idea_description = input("You: ")
if idea_description.lower() in ['exit', 'quit']:
    print("👋 Goodbye!")
    

problem_solution_fit_template=f""" Given the startup idea description below, evaluate its Problem-Solution Fit:

Startup Idea: {idea_description}

Answer the following:

Is this solving a clearly defined and urgent problem?

How likely are people to pay for this solution? Provide reasoning.

Is the problem widespread and relevant to a large or niche group?

Score the following:

Problem clarity and relevance (out of 8%)

Urgency of the problem (out of 10%)

User willingness to pay / validation (out of 12%)

Total score (out of 30%): ___% 
         
Just return the score , nothing more, nothing less """ 

problem_solution_fit = agent.run(problem_solution_fit_template)
def percent_to_float(percent_str):
    if percent_str.endswith('%'):
        return float(percent_str.strip('%'))
    else:
        return float(percent_str)



problem_solution_fit_score=percent_to_float(problem_solution_fit)

Market_Opportunity_template=f""" Evaluate the Market Opportunity for the following startup idea:

Startup Idea: {idea_description}

Questions to address:

What is the estimated market size? Is it growing or stagnant?

Who are the major competitors and how saturated is the space?

How unique, innovative, or differentiated is this idea?

Score the following:

Market size & growth potential (out of 10%)

Competitive landscape & positioning (out of 8%)

Innovation/Uniqueness (out of 7%)

Total score (out of 25%): ___% Just return the score , nothing more, nothing less """ 

Market_Opportunity = agent.run(Market_Opportunity_template)

Market_Opportunity_score = percent_to_float(Market_Opportunity)

Execution_Feasibility_template=""" Analyze Execution Feasibility of the startup idea:

Startup Idea: {idea_description}

Address the following:

Does the team or founder have the skills to build this?

Does the founder have domain experience or passion for this?

Are there major tech, operational, or logistic hurdles?

Score the following:

Team skills and complementarity (out of 8%)

Founder’s domain knowledge and passion (out of 7%)

Tech and operational feasibility (out of 5%)

Total score (out of 20%): ___%  .Just return the score , nothing more, nothing less """ 

Execution_Feasibility = agent.run(Execution_Feasibility_template)

Execution_Feasibility_score = percent_to_float(Execution_Feasibility)

Financial_Feasibility_template = """ Assess the Financial Feasibility of this startup concept:

Startup Idea: {idea_description}

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

Total score (out of 15%): ___%.Just return the score , nothing more, nothing less  """


Financial_Feasibility = agent.run(Financial_Feasibility_template)

Financial_Feasibility_score = percent_to_float(Financial_Feasibility)

total_score  = problem_solution_fit_score + Market_Opportunity_score + Execution_Feasibility_score + Financial_Feasibility_score

if total_score >= 60:
    print("The startup idea is feasible")
else:
    print("The startup idea is not feasible")


'''A platform called "FarmLink" that connects small-scale farmers in rural areas with urban buyers and local restaurants,enabling them to sell their produce directly at fair prices. The app uses geolocation, vernacular language support,and a simple interface to help farmers list available produce. It also provides logistics coordination and real-time demand prediction using AI. This reduces exploitation by middlemen, ensures fresh farm-to-table supply, and increases farmers' incomes.The startup targets Indian tier-2 and tier-3 cities, with potential to scale across other developing countries'''