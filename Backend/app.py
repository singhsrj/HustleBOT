import re
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from templates import SUMMARY_TEMPLATE

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
GEMMINI_API_KEY = os.getenv("GEMMINI_API_KEY")

# Initialize LLMs
llm = ChatGroq(model="Gemma2-9b-It", groq_api_key=GROQ_API_KEY)
llm_tool_runner = ChatGroq(model="Gemma2-9b-It", groq_api_key=GROQ_API_KEY)
from langchain_ollama import ChatOllama

# Initialize the LLM (Ollama must be running locally)
qwen = ChatOllama(model="qwen2:1.5b")  # You can use other models like 'mistral', 'gemma', etc.

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

from langchain.agents import AgentExecutor

def evaluate_problem_solution_fit(idea_description: str):
    if idea_description.lower() in ['exit', 'quit']:
        return None, None, "Exited by user."

    # Problem evaluation prompt
    problem_solution_fit_template = f"""Given the startup idea description below, evaluate its Problem-Solution Fit:

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

Just return the score , nothing more, nothing less
"""

    try:
        # Custom executor to track intermediate steps
        executor = AgentExecutor(
            agent=agent.agent,
            tools=agent.tools,
            verbose=True,
            return_intermediate_steps=True,
            handle_parsing_errors=True
        )

        # Run the agent with the prompt
        result = executor.invoke({"input": problem_solution_fit_template})

        final_output = result['output']  # Agent's answer
        intermediate_steps = result['intermediate_steps']  # [(AgentAction, Observation), ...]

        # Log tool reasoning and results
        logs = ""
        for action, observation in intermediate_steps:
            logs += f"\n[Tool Used: {action.tool}]\nThought: {action.log}\nObservation: {observation}\n"

        # Try to parse score safely using regex
        match = re.search(r"(\d+(\.\d+)?)\s*%", final_output)
        parsed_score = float(match.group(1)) if match else None
        possible_scores = re.findall(r'(\d{1,2}\.?\d*)%', final_output)
        if possible_scores:
            score = float(possible_scores[0]) 
        
        summary_prompt = SUMMARY_TEMPLATE.format(logs=logs)
        summary = llm.invoke(summary_prompt) 
        return parsed_score, summary.content

    except Exception as e:
        return None, f"❌ Error: {str(e)}"

idea_description = "Startup Idea: A mobile app that helps users find and book local yoga classes in their area."

score, summary = evaluate_problem_solution_fit(idea_description)

print(f"\n🧠 Final Score: {score}/30\n")
# print("📝 Agent's Answer:\n", final_output)
# print("\n🔍 Intermediate Logs:\n", logs)
print(f"summary in points: {summary} ")
