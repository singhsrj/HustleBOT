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
search = SerpAPIWrapper(serpapi_api_key="a36c527309fe1bc741f80480d37b53b45277109d9b9bf91c1c00b57c12b6573c")
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


combined_evaluation_template = f"""
Evaluate the startup idea comprehensively across four dimensions: **Problem-Solution Fit, Market Opportunity, Execution Feasibility, and Financial Feasibility**.

Startup Idea: {idea_description}

---

### 🔍 Problem-Solution Fit:
Answer the following:
- Is this solving a clearly defined and urgent problem?
- How likely are people to pay for this solution? Provide reasoning.
- Is the problem widespread and relevant to a large or niche group?

Score:
- Problem clarity and relevance (out of 8%)
- Urgency of the problem (out of 10%)
- User willingness to pay / validation (out of 12%)

**Subtotal (Problem-Solution Fit): ___%**

---

### 📊 Market Opportunity:
Answer the following:
- What is the estimated market size? Is it growing or stagnant?
- Who are the major competitors and how saturated is the space?
- How unique, innovative, or differentiated is this idea?

Score:
- Market size & growth potential (out of 10%)
- Competitive landscape & positioning (out of 8%)
- Innovation/Uniqueness (out of 7%)

**Subtotal (Market Opportunity): ___%**

---

### 🛠️ Execution Feasibility:
Answer the following:
- Does the team or founder have the skills to build this?
- Does the founder have domain experience or passion for this?
- Are there major tech, operational, or logistic hurdles?

Score:
- Team skills and complementarity (out of 8%)
- Founder’s domain knowledge and passion (out of 7%)
- Tech and operational feasibility (out of 5%)

**Subtotal (Execution Feasibility): ___%**

---

### 💰 Financial Feasibility:
Answer the following:
- Are the expected startup costs reasonable and clearly estimated?
- Does the team have initial capital or access to it?
- Is the idea structured in a way that’s attractive to investors?
- Are potential funding sources identified (e.g., grants, VCs)?

Score:
- Startup cost estimation (out of 6%)
- Personal/team capital available (out of 4%)
- Investor readiness (out of 3%)
- Awareness of funding options (out of 2%)

**Subtotal (Financial Feasibility): ___%**

---

### ✅ Final Evaluation:
Add all the subtotals above.

**Total Score (out of 90%): ___%**

Just return the total score at the end — nothing more, nothing less.
"""




response = agent.run(combined_evaluation_template)
def percent_to_float(percent_str):
    if percent_str.endswith('%'):
        return float(percent_str.strip('%'))
    else:
        return float(percent_str)

response=percent_to_float(response)

print(response)
if response >= 60:
    print("The startup idea is feasible")
else:
    print("The startup idea is not feasible")


'''A platform called "FarmLink" that connects small-scale farmers in rural areas with urban buyers and local restaurants,enabling them to sell their produce directly at fair prices. The app uses geolocation, vernacular language support,and a simple interface to help farmers list available produce. It also provides logistics coordination and real-time demand prediction using AI. This reduces exploitation by middlemen, ensures fresh farm-to-table supply, and increases farmers' incomes.The startup targets Indian tier-2 and tier-3 cities, with potential to scale across other developing countries'''