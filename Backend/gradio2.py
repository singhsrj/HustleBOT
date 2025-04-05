import gradio as gr
from typing import Dict, TypedDict, Optional
from ollama import Client
from serpapi import GoogleSearch
from tavily import TavilyClient

# === Replace langgraph logic manually (not installed on PyPI) ===

class ChatState(TypedDict):
    responses: Dict[str, str]
    current_question: int
    final_analysis: Optional[str]

# === Init clients ===

tavily_client_api= "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"
serp_client_api = "843c455cc99584a69ecb59a5fdb67c5e7845f4c89a484b2e192b5966a8f73e00"

ollama_client = Client(host='http://localhost:11434')
serp_client = GoogleSearch({"api_key": serp_client_api})
tavily_client = TavilyClient(api_key=tavily_client_api)

QUESTIONS = [
    "What specific problem are you solving, and why is it actually urgent right now?",
    "Have you validated this with real users? (e.g., interest, usage, willingness to pay)?",
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
    params = {
        "engine": "google",
        "q": query,
        "api_key": "your_api_key_here",
        "num": 5
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    return "\n".join([r["snippet"] for r in results.get("organic_results", [])])

def tavily_search(query: str) -> str:
    response = tavily_client.search(query, max_results=15)
    return "\n".join([r["content"] for r in response["results"]])

def analyze_responses(responses: Dict[str, str]) -> str:
    scores = {
        "Problem-Solution Fit": 0.3 * (len(responses.get("Q1", "")) > 20 and len(responses.get("Q2", "")) > 20),
        "Market Opportunity": 0.25 * (len(responses.get("Q3", "")) > 20 and len(responses.get("Q4", "")) > 20),
        "Execution Feasibility": 0.2 * (len(responses.get("Q5", "")) > 20 and len(responses.get("Q6", "")) > 20),
        "Financial Feasibility": 0.15 * (len(responses.get("Q7", "")) > 20 and len(responses.get("Q8", "")) > 20),
        "Scalability & Sustainability": 0.1 * (len(responses.get("Q9", "")) > 20 and len(responses.get("Q10", "")) > 20)
    }
    total_score = sum(scores.values()) * 100
    return f"📊 Analysis Summary:\n{scores}\n\n💯 Total Score: {total_score:.2f}%"

# === Core Logic ===

def evaluate(user_input, state: ChatState):
    if state is None:
        state = {"responses": {}, "current_question": 0, "final_analysis": None}

    q_idx = state["current_question"]

    if q_idx < len(QUESTIONS):
        state["responses"][f"Q{q_idx + 1}"] = user_input

        if q_idx == 2:
            market_info = tavily_search(f"market size and competitors for {user_input}")
            state["responses"]["Q3_enriched"] = market_info
        elif q_idx == 3:
            competitors = search_web(f"alternatives to {user_input}")
            state["responses"]["Q4_enriched"] = competitors

        state["current_question"] += 1

    if state["current_question"] >= len(QUESTIONS):
        analysis = analyze_responses(state["responses"])
        state["final_analysis"] = analysis
        return analysis, "", gr.update(visible=False), gr.update(visible=True), state
    else:
        next_q = QUESTIONS[state["current_question"]]
        return next_q, "", gr.update(visible=True), gr.update(visible=False), state

def restart():
    return QUESTIONS[0], "", gr.update(visible=True), gr.update(visible=False), {"responses": {}, "current_question": 0, "final_analysis": None}

# === Gradio UI ===

with gr.Blocks(css="textarea { font-size: 16px; }") as demo:
    gr.Markdown("## 🚀 Startup Evaluation Assistant")
    gr.Markdown("Answer the questions below to get an analysis of your startup idea. Be as specific and detailed as possible.")

    state = gr.State()

    with gr.Column():
        question_display = gr.Textbox(label="Question", value=QUESTIONS[0], interactive=False, lines=2)
        chatbot = gr.Textbox(label="Your Answer", lines=6, placeholder="Type your response here...", show_copy_button=True)
        
        with gr.Row():
            submit = gr.Button("Submit")
            restart_btn = gr.Button("🔄 Restart", variant="secondary")

        final_output = gr.Textbox(label="Final Analysis", visible=False, lines=12, interactive=False, show_copy_button=True)

    submit.click(
        evaluate,
        inputs=[chatbot, state],
        outputs=[question_display, chatbot,chatbot, final_output, state]
    )

    restart_btn.click(
        restart,
        outputs=[question_display, chatbot, chatbot, final_output, state]
    )

demo.launch(share=True)
