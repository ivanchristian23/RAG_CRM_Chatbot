import requests

def ask_llama(context, question):
    prompt = f"""You are a helpful assistant for Microsoft Dynamics CRM data.

Context:
{context}

Q: {question}
A:"""

    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    })
    return response.json()["response"]
