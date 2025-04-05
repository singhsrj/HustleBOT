from langgraph.graph import StateGraph, END
from typing import Dict, TypedDict, Optional
from ollama import Client
from serpapi import GoogleSearch
from tavily import TavilyClient
import langgraph


tavily_client_api= "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"
serp_client_api = "843c455cc99584a69ecb59a5fdb67c5e7845f4c89a484b2e192b5966a8f73e00"


# State to store conversation data
class ChatState(TypedDict):
    responses: Dict[str, str]
    current_question: int
    final_analysis: Optional[str]

# Initialize Ollama client
ollama_client = Client(host='http://localhost:11434')  # Default Ollama port

# Initialize tools
serp_client = GoogleSearch({"api_key": serp_client_api})
tavily_client = TavilyClient(api_key=tavily_client_api)

# Questions list
QUESTIONS = [
    "What specific problem are you solving, and why is it actually urgent right now?",
    "Have you validated this with real users? (e.g., interest, usage, willingness to pay)",
    "Who are your target customers, and how big is the market you're going after? Specify the size of competitors if any.",
    "What makes your solution unique compared to existing alternatives?",
    "Who's on your team, and what makes you the right people to build this?",
    "Do you have a clear plan or prototype for building and launching this product?",
    "Do you know how much it will cost to build and launch your MVP?",
    "How are you planning to fund it — personal funds, investors, grants?",
    "How will you make money (financial model), and can this grow into a large, repeatable business?",
    "Are there any legal, ethical, or regulatory risks you’re aware of?",
    "Bonus (optional): How do you plan to acquire your first 100 users/customers?"
]

# Function to call Ollama
def call_llm(prompt: str) -> str:
    response = ollama_client.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]

# Tool functions
def search_web(query: str) -> str:
    params = {"q": query, "num": 5}
    results = serp_client.get_json(params)
    return "\n".join([r["snippet"] for r in results.get("organic_results", [])])

def tavily_search(query: str) -> str:
    response = tavily_client.search(query, max_results=5)
    return "\n".join([r["content"] for r in response["results"]])

# Node to ask questions
def ask_question(state: ChatState) -> ChatState:
    if state["current_question"] >= len(QUESTIONS):
        return {"final_analysis": analyze_responses(state["responses"]), "current_question": END}
    
    question = QUESTIONS[state["current_question"]]
    prompt = f"Ask the user: {question}"
    response = call_llm(prompt)
    print(response)  # This will be sent to the user via FastAPI
    return state

# Node to process user response
def process_response(state: ChatState, user_input: str) -> ChatState:
    q_idx = state["current_question"]
    state["responses"][f"Q{q_idx + 1}"] = user_input
    
    # Use tools for specific questions
    if q_idx == 2:  # Market size and competitors
        market_info = tavily_search(f"market size and competitors for {user_input}")
        state["responses"]["Q3_enriched"] = market_info
    elif q_idx == 3:  # Uniqueness
        competitors = search_web(f"alternatives to {user_input}")
        state["responses"]["Q4_enriched"] = competitors
    
    state["current_question"] += 1
    return state

# Analysis function
def analyze_responses(responses: Dict[str, str]) -> str:
    # Simple scoring logic (customize as needed)
    scores = {
        "Problem-Solution Fit": 0.3 if len(responses.get("Q1", "")) > 20 and len(responses.get("Q2", "")) > 20 else 0,
        "Market Opportunity": 0.25 if (len(responses.get("Q3", "")) > 20 and len(responses.get("Q4", "")) > 20) else 0,
        "Execution Feasibility": 0.2 if (len(responses.get("Q5", "")) > 20 and len(responses.get("Q6", "")) > 20)else 0,
        "Financial Feasibility": 0.15 if (len(responses.get("Q7", "")) > 20 and len(responses.get("Q8", "")) > 20)else 0,
        "Scalability & Sustainability": 0.1 if (len(responses.get("Q9", "")) > 20 and len(responses.get("Q10", "")) > 20)else 0
    }
    total_score = sum(scores.values()) * 100
    return f"Analysis:\n{scores}\nTotal Score: {total_score:.2f}%"

# Build the graph
graph = StateGraph(ChatState)
graph.add_node("ask", ask_question)
graph.add_node("process", process_response)
graph.add_edge("ask", "process")
graph.add_conditional_edges("process", lambda state: "ask" if state["current_question"] != END else END)
graph.set_entry_point("ask")

# Compile the graph
app = graph.compile()