import requests
import json
from langchain.agents import Tool
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_openai_tools_agent,tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import os
import datetime


def query(q):
    url = "https://google.serper.dev/search"
    payload=json.dumps({
        "q":q
    })
    headers ={
        'X-API-KEY':'a36c527309fe1bc741f80480d37b53b45277109d9b9bf91c1c00b57c12b6573c',
        'Content-Type': 'application/json',
    }

    response = requests.request("POST",url,headers=headers,data=payload)

    return(response.text)





from dotenv import load_dotenv

load_dotenv()
@tool
def get_system_time(format: str = "%Y-%m-%d %H:%M:%S"):
    '''Returns the current date and time int he specified format'''

    cuurent_time = datetime.datetime.now()
    formatted_time = cuurent_time.strftime(format)
    return formatted_time

tools = [
    Tool(
        name="search",
        func=query,
        description="Useful for when you need to answer question about current events."
    ),
    get_system_time
   
]
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# Choose the LLM that will drive the agent
llm = ChatGroq(model ="Gemma2-9b-It",groq_api_key=GROQ_API_KEY)

# Prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """You are a research assistant. Use your tools to answer questions.
        If you do not have a tool to answer the question, say so.
        You will be given a topic and your goal is that of finding highlights , that can be 
        within the documents you will analyze.
        Provide your answer as a bullet point.
        what is the reason someone is making such a claim.
        """),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)

# Construct the OpenAI Tools agent
agent = create_openai_tools_agent(llm, tools, prompt)

# Create an agent executor by passing in the agent and toolkit
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

response = agent_executor.invoke({"input":"current market trends on thift shopping "})
print(response)