# streamlit_app.py

import streamlit as st
import langgraph
from langgraph.graph import StateGraph, END
from typing import Dict, TypedDict, Optional
from ollama import Client
from serpapi import GoogleSearch
from tavily import TavilyClient
import langgraph

# Setup API keys and clients
tavily_client = TavilyClient(api_key="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")
serp_client = GoogleSearch({"api_key": "843c455cc99584a69ecb59a5fdb67c5e7845f4c89a484b2e192b5966a8f73e00"})
ollama_client = Client(host='http://localhost:11434')  # Ollama running locally

# LangGraph state type
class ChatState(TypedDict):
    responses: Dict[str, str]
    current_question: int
    final_analysis: Optional[str]

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

# === Utility functions ===

def call_llm(prompt: str) -> str:
    response = ollama_client.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]

def search_web(query: str) -> str:
    params = {"q": query, "num": 5}
    results = serp_client.get_json(params)
    return "\n".join([r["snippet"] for r in results.get("organic_results", [])])

def tavily_search(query: str) -> str:
    response = tavily_client.search(query, max_results=5)
    return "\n".join([r["content"] for r in response["results"]])

def ask_question(state: ChatState) -> ChatState:
    if state["current_question"] >= len(QUESTIONS):
        return {"final_analysis": analyze_responses(state["responses"]), "current_question": END}
    
    question = QUESTIONS[state["current_question"]]
    st.session_state['current_question_text'] = question
    return state

def process_response(state: ChatState, user_input: str) -> ChatState:
    q_idx = state["current_question"]
    state["responses"][f"Q{q_idx + 1}"] = user_input
    
    if q_idx == 2:
        market_info = tavily_search(f"market size and competitors for {user_input}")
        state["responses"]["Q3_enriched"] = market_info
    elif q_idx == 3:
        competitors = search_web(f"alternatives to {user_input}")
        state["responses"]["Q4_enriched"] = competitors
    
    state["current_question"] += 1
    return state

def analyze_responses(responses: Dict[str, str]) -> str:
    scores = {
        "Problem-Solution Fit": 0.3 * (len(responses.get("Q1", "")) > 20 and len(responses.get("Q2", "")) > 20),
        "Market Opportunity": 0.25 * (len(responses.get("Q3", "")) > 20 and len(responses.get("Q4", "")) > 20),
        "Execution Feasibility": 0.2 * (len(responses.get("Q5", "")) > 20 and len(responses.get("Q6", "")) > 20),
        "Financial Feasibility": 0.15 * (len(responses.get("Q7", "")) > 20 and len(responses.get("Q8", "")) > 20),
        "Scalability & Sustainability": 0.1 * (len(responses.get("Q9", "")) > 20 and len(responses.get("Q10", "")) > 20)
    }
    total_score = sum(scores.values()) * 100
    return f"Analysis:\n{scores}\n\nTotal Score: {total_score:.2f}%"

# === Streamlit App ===

st.set_page_config(page_title="Startup Pitch Evaluator", layout="centered")
st.title("🚀 Startup Evaluation Assistant")

if "chat_state" not in st.session_state:
    st.session_state.chat_state = {
        "responses": {},
        "current_question": 0,
        "final_analysis": None
    }

if "current_question_text" not in st.session_state:
    st.session_state.current_question_text = QUESTIONS[0]

# Display current question
if st.session_state.chat_state["current_question"] != END:
    st.subheader(f"Question {st.session_state.chat_state['current_question'] + 1}")
    st.write(st.session_state.current_question_text)
    user_input = st.text_area("Your Answer:", key="user_input", height=100)
    if st.button("Submit Answer"):
        st.session_state.chat_state = process_response(st.session_state.chat_state, user_input)
        st.session_state.chat_state = ask_question(st.session_state.chat_state)
        st.session_state.user_input = ""
        st.experimental_rerun()
else:
    st.success("✅ All questions answered.")
    st.write("🧠 Generating Final Analysis...")
    st.markdown(f"### {st.session_state.chat_state['final_analysis'] or analyze_responses(st.session_state.chat_state['responses'])}")
