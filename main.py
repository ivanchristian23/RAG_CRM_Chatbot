from fastapi import FastAPI, Request
from crm_extractor import get_contacts
from embed_store import build_vector_store, search
from query_llama import ask_llama

app = FastAPI()

@app.on_event("startup")
def startup():
    data = get_contacts()
    if not data:
        print("[ERROR] No CRM data returned. Vector store not built.")
    else:
        build_vector_store(data)


@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    question = body.get("question")
    context = "\n".join(search(question))
    answer = ask_llama(context, question)
    return {"response": answer}
