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
llm = ChatGroq(model="llama3-8b-8192", groq_api_key="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")
llm_tool_runner = ChatGroq(model="llama3-8b-8192", groq_api_key="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")
from langchain_ollama import ChatOllama

# Initialize the LLM (Ollama must be running locally)
qwen = ChatOllama(model="qwen2:1.5b")  # You can use other models like 'mistral', 'gemma', etc.
llama = ChatOllama(model="llama2:7b")

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Tools
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

        print(result['output'])
    except Exception as e:
        return None, f"❌ Error: {str(e)}"

idea_description = "Startup Idea: A mobile app that helps users find and book local yoga classes in their area."

evaluate_problem_solution_fit(idea_description)