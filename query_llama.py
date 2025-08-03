import requests
from datetime import datetime

def format_history(history):
    """Convert list of (Q, A) to a formatted string"""
    if not history:
        return "None"
    return "\n".join([f"User: {q}\nAssistant: {a}" for q, a in history])

def ask_llama(context, question, chat_history=None):
    today = datetime.now().strftime("%Y-%m-%d")
    history_text = format_history(chat_history or [])

    prompt = f"""You are a helpful assistant for Microsoft Dynamics CRM data.
Today's date is {today}.

Context:
{context}

Previous Conversation:
{history_text}

User Question:
{question}

Answer:"""
    
    print("[DEBUG] Context:",context)


    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    })
    
    # response = requests.post("http://192.168.10.9:8000/generate",
    #                          json={
    #                              "prompt": prompt
    #                          })

    return response.json()["response"]
