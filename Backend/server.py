from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from graph import ChatState,QUESTIONS,app

from langgraph.graph import StateGraph, END
from typing import Dict, TypedDict, Optional
from ollama import Client
from serpapi import GoogleSearch
from tavily import TavilyClient
import tavily



fastapi_app = FastAPI()

# Initial state
initial_state = ChatState(responses={}, current_question=0, final_analysis=None)

class UserInput(BaseModel):
    message: str

# WebSocket for real-time chat
@fastapi_app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    state = initial_state.copy()
    
    # Start by asking the first question
    question_state = app.invoke(state)
    await websocket.send_text(f"Bot: {QUESTIONS[0]}")
    
    while True:
        user_input = await websocket.receive_text()
        state = app.invoke(state, config={"configurable": {"user_input": user_input}})
        
        if state["final_analysis"]:
            await websocket.send_text(f"Bot: {state['final_analysis']}")
            break
        else:
            next_question = QUESTIONS[state["current_question"]]
            await websocket.send_text(f"Bot: {next_question}")

if __name__ == "__main__":
    
    import uvicorn
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)