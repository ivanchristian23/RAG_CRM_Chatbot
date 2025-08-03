from fastapi import FastAPI, Request
# from crm_extractor import (
#     get_contacts, get_accounts,
#     get_activities, get_leads, get_opportunities
# )
from embed_store import search
from query_llama import ask_llama
# from chatbot_chain import get_chat_chain

app = FastAPI()

# Store in-memory session history
session_memory = {}

# chain = get_chat_chain()

# @app.on_event("startup")
# def startup():

# @app.post("/chat")
# async def chat(request: Request):
#     body = await request.json()
#     question = body.get("question")
#     context = "\n".join(search(question))
#     answer = ask_llama(context, question)
#     return {"response": answer}

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    question = body.get("question")
    session_id = body.get("session_id", "default")  # Default session if none given

    # Get chat history for this session
    chat_history = session_memory.get(session_id, [])

    # RAG context from vector search
    context = "\n".join(search(question))

    # Get model response with memory
    answer = ask_llama(context, question, chat_history)

    # Update memory
    chat_history.append((question, answer))
    session_memory[session_id] = chat_history

    return {"response": answer}

#Langchain version using ConversationalRetrievalChain
# @app.post("/chat")
# async def chat(request: Request):
#     body = await request.json()
#     question = body.get("question")
#     response = chain.invoke({"question": question})
#     print(response)
#     return {"response": response}

