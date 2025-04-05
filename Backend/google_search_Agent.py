# from langchain import OpenAI, LLMMathChain, SerpAPIWrapper
# from langchain.agents import initialize_agent, Tool, AgentExecutor
# from langchain_groq import ChatGroq
# import os
# import chainlit as cl

# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# SERP_API_KEY = os.getenv("SERP_API_KEY")

# @cl.on_chat_start
# def start():
#     llm = ChatGroq(model="Gemma2-9b-It", groq_api_key=GROQ_API_KEY)
#     llm1 = ChatGroq(model="Gemma2-9b-It", groq_api_key=GROQ_API_KEY)
#     search = SerpAPIWrapper()
#     llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)

#     tools = [
#         Tool(
#             name="Search",
#             func=search.run,
#             description="useful for when you need to answer questions about current events. You should ask targeted questions",
#         ),
#         Tool(
#             name="Calculator",
#             func=llm_math_chain.run,
#             description="useful for when you need to answer questions about math",
#         ),
#     ]
#     agent = initialize_agent(
#         tools, llm1, agent="chat-zero-shot-react-description", verbose=True
#     )
#     cl.user_session.set("agent", agent)


# @cl.on_message
# async def main(message):
#     agent = cl.user_session.get("agent")  # type: AgentExecutor
#     cb = cl.LangchainCallbackHandler(stream_final_answer=True)

#     await cl.make_async(agent.run)(message, callbacks=[cb])


from langchain import LLMMathChain, SerpAPIWrapper
from langchain.agents import initialize_agent, Tool, AgentExecutor
from langchain_groq import ChatGroq
import os
import chainlit as cl
from dotenv import load_dotenv
import json
load_dotenv()
# Load API keys from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")

@cl.on_chat_start
def start():
    # Initialize LLMs using ChatGroq (Gemma 2-9b-It)
    llm = ChatGroq(model="Gemma2-9b-It", groq_api_key=GROQ_API_KEY)
    llm_tool_runner = ChatGroq(model="Gemma2-9b-It", groq_api_key=GROQ_API_KEY)

    # Initialize SerpAPI (search) and Math tools
    search = SerpAPIWrapper(serpapi_api_key="a36c527309fe1bc741f80480d37b53b45277109d9b9bf91c1c00b57c12b6573c")
    llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)

    # Define tools with clear descriptions
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

    # Create the agent with tools and zero-shot reasoning
    agent = initialize_agent(
        tools=tools,
        llm=llm_tool_runner,
        agent="chat-zero-shot-react-description",
        verbose=True
    )

    # Store the agent in the session for later access
    cl.user_session.set("agent", agent)

@cl.on_message
async def main(message):
    # Retrieve the agent from session
    agent = cl.user_session.get("agent")  # type: AgentExecutor
    cb = cl.LangchainCallbackHandler(stream_final_answer=True)

    # Run the agent and capture the response
    response = await cl.make_async(agent.run)(message.content, callbacks=[cb])

    # Wrap response in JSON format
    json_response = {"response": response}
    print(json_response)
    # Send JSON response back to Chainlit chat UI (or wherever needed)
    await cl.Message(content=json.dumps(json_response, indent=2)).send()

