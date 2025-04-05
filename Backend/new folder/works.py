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
    verbose=True
)

# Store all responses in a dictionary
conversation_log = {}

# CLI loop
print("🚀 Agent is ready. Type your question below (or 'exit' to quit):")
while True:
    
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        print("👋 Goodbye!")
        break

    response = agent.run(user_input)
    print(f"🤖 Agent: {response}\n")

    # Store the conversation
    conversation_log[user_input] = response

# Optionally, write the log to a JSON file
with open("conversation_log.json", "w") as f:
    json.dump(conversation_log, f, indent=2)

print("📁 All responses saved to 'conversation_log.json'")
print(json.dumps(conversation_log, indent=2))