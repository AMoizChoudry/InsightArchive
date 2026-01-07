import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import time

# 1. Path Fix: Ensure project root is in Python's path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

# 2. Load Environment Variables
env_path = ROOT_DIR / ".env"
load_dotenv(dotenv_path=env_path)

from core.rag_engine import search_docs

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_with_pdf(user_input: str):
    metrics = {"db_time": 0, "llm_time": 0} 
    
    messages = [
        {
            "role": "system", 
            "content": """You are a professional PDF analyst. 
            CRITICAL INSTRUCTION: You currently have NO internal knowledge of the uploaded documents. 
            You MUST call the 'search_pdf' tool for EVERY user question to retrieve facts from the database. 
            Do not tell the user you don't have documents until you have attempted at least one search."""
        },
        {"role": "user", "content": user_input}
    ]

    # --- THIS WAS MISSING ---
    tools = [{
        "type": "function",
        "function": {
            "name": "search_pdf",
            "description": "Search the PDF for specific information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query."}
                },
                "required": ["query"]
            }
        }
    }]

    # Start timing the first LLM call
    start_llm = time.perf_counter()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools # This was failing because 'tools' was undefined
    )
    
    msg = response.choices[0].message
    
    if msg.tool_calls:
        messages.append(msg)
        for tool_call in msg.tool_calls:
            if tool_call.function.name == "search_pdf":
                args = json.loads(tool_call.function.arguments)
                
                start_db = time.perf_counter()
                context = search_docs(args['query'])
                metrics["db_time"] = round(time.perf_counter() - start_db, 3)
                
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": "search_pdf",
                    "content": context
                })
        
        start_gen = time.perf_counter()
        final_res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        metrics["llm_time"] = round(time.perf_counter() - start_gen, 3)
        
        return final_res.choices[0].message.content, metrics
    
    # If no tool was called, we still need to record the initial LLM time
    metrics["llm_time"] = round(time.perf_counter() - start_llm, 3)
    return msg.content, metrics

if __name__ == "__main__":
    print(chat_with_pdf("What is the total revenue of the company?"))